---
title: Multi-character usage examples
description: Implement look-to-address targeting and a scripted roster swap so a Unity scene manages which character in a room the player addresses.
last_reviewed: "4.6.0"
---

Two worked patterns show how an application drives a multi-character session once a room is connected: routing player input by where they are looking, and swapping one character for another mid-scenario without ever leaving the room without a valid target. Both patterns are application code written against the public connection API — neither ships as part of the SDK.

{% hint style="info" %}
Both examples assume a connected multi-character session with `IConvaiRoomConnectionService.CurrentMultiCharacterSession` already populated. See [Build your first multi-character session](quick-start.md) if the room is not connected yet.
{% endhint %}

## Look-to-address targeting

**Context:** A scene with several characters standing in different locations. The player should address whichever character they are currently facing, without every small head turn interrupting a character mid-answer.

### The rules this pattern enforces

A camera-forward raycast identifies which character the player is currently facing. A short grace period debounces the result, so a brief glance away does not immediately move the interaction target. Before switching, the script checks whether the character currently holding the target is still speaking, and defers the switch until that turn ends.

### Implementation

{% code title="Assets/Scripts/LookToAddressTargeting.cs" %}
```csharp
using System;
using System.Threading;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public class LookToAddressTargeting : MonoBehaviour
{
    [SerializeField] private Camera _lookCamera;
    [SerializeField] private LayerMask _characterLayerMask;
    [SerializeField] private float _maxLookDistance = 10f;
    [SerializeField] private float _lookAwayGracePeriod = 1.5f;

    private IConvaiRoomConnectionService _roomService;
    private ConvaiCharacter _addressedCharacter;
    private ConvaiCharacter _candidateCharacter;
    private float _candidateStableSince;
    private bool _switchInFlight;

    private readonly CancellationTokenSource _lifetime = new();

    public void Attach(IConvaiRoomConnectionService roomService, ConvaiCharacter initialTarget)
    {
        _roomService = roomService;
        _addressedCharacter = initialTarget;
    }

    private void Update()
    {
        if (_roomService?.CurrentMultiCharacterSession == null) return;

        ConvaiCharacter looked = ResolveLookedAtCharacter();
        if (looked != _candidateCharacter)
        {
            _candidateCharacter = looked;
            _candidateStableSince = Time.time;
        }

        if (_candidateCharacter == null || _candidateCharacter == _addressedCharacter) return;
        if (Time.time - _candidateStableSince < _lookAwayGracePeriod) return;

        TrySwitchTarget(_candidateCharacter);
    }

    private ConvaiCharacter ResolveLookedAtCharacter()
    {
        if (!Physics.Raycast(_lookCamera.transform.position, _lookCamera.transform.forward,
                out RaycastHit hit, _maxLookDistance, _characterLayerMask))
            return null;

        return hit.collider.GetComponentInParent<ConvaiCharacter>();
    }

    private async void TrySwitchTarget(ConvaiCharacter target)
    {
        if (_switchInFlight) return;
        if (_addressedCharacter != null && _addressedCharacter.IsSpeaking) return;

        _switchInFlight = true;
        try
        {
            InteractionTargetResult result = await _roomService.SetInteractionTargetAsync(target, _lifetime.Token);
            if (result.Changed) _addressedCharacter = target;
        }
        catch (InvalidOperationException error)
        {
            Debug.LogError($"[MultiCharacter] Could not switch target: {error.Message}");
        }
        catch (ArgumentException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
        }
        catch (TimeoutException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
        }
        finally
        {
            _switchInFlight = false;
        }
    }

    private void OnDestroy()
    {
        _lifetime.Cancel();
        _lifetime.Dispose();
    }
}
```
{% endcode %}

`ConvaiCharacter.IsSpeaking` and the `OnSpeechStarted`/`OnSpeechStopped` events are scoped to the character instance the SDK resolved the speech event to, so checking `IsSpeaking` here reads the correct character even when the room holds two clones of it. `Update` re-evaluates every frame, so once the addressed character stops speaking, the next frame's check passes and the pending switch to the new candidate proceeds without extra wiring.

### Expected outcome

While the player looks steadily at a character for `_lookAwayGracePeriod` seconds, `SetInteractionTargetAsync` moves the interaction target to that character and `InteractionTargetResult.Changed` reports `true`. A player who glances at a different character mid-answer does not interrupt the one currently speaking — the switch waits until `IsSpeaking` is `false` before it runs.

## Scripted roster swap mid-scenario

**Context:** A training scenario where one character leaves partway through and a second character takes over as the person the player is addressing — for example, a supervisor stepping out and a safety instructor continuing the session.

### The rules this pattern enforces

The incoming character is added to the roster and given time to reach `Ready` before anything else changes, so the swap never routes input to a character that cannot yet respond. The outgoing character is then removed with `replacementTargetMembershipId` set to the incoming character's membership, so the removal and the target change happen in one command and the room is never left without a valid interaction target.

### Implementation

{% code title="Assets/Scripts/RosterSwapController.cs" %}
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public class RosterSwapController : MonoBehaviour
{
    private readonly CancellationTokenSource _lifetime = new();

    public async void SwapCharacter(
        IConvaiRoomConnectionService roomService,
        MultiCharacterRoomSession session,
        ConvaiCharacter outgoing,
        ConvaiCharacter incoming)
    {
        CharacterRoomMembership incomingMembership;
        try
        {
            CharacterRosterUpdateResult addResult =
                await roomService.AddCharacterAsync(incoming, cancellationToken: _lifetime.Token);
            incomingMembership = addResult.Added[0];
        }
        catch (ArgumentException error)
        {
            Debug.LogError($"[MultiCharacter] Could not add {incoming.CharacterId}: {error.Message}");
            return;
        }
        catch (CharacterRosterUpdateException error)
        {
            Debug.LogError($"[MultiCharacter] Add rejected ({error.Code}): {error.Message}");
            return;
        }
        catch (InvalidOperationException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
            return;
        }
        catch (TimeoutException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
            return;
        }

        if (!await WaitForReadyAsync(session, incomingMembership.MembershipId))
        {
            Debug.LogWarning($"[MultiCharacter] {incoming.CharacterId} did not become ready before the swap.");
            return;
        }

        CharacterRoomMembership outgoingMembership = session.FindByCharacter(outgoing);
        if (outgoingMembership == null)
        {
            Debug.LogWarning("[MultiCharacter] The outgoing character is not a member of the room.");
            return;
        }

        try
        {
            CharacterRosterUpdateResult removeResult = await roomService.RemoveCharacterAsync(
                outgoingMembership.MembershipId,
                incomingMembership.MembershipId,
                _lifetime.Token);
            Debug.Log($"[MultiCharacter] Active target is now {removeResult.ActiveMembershipId}.");
        }
        catch (ArgumentException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
        }
        catch (CharacterRosterUpdateException error)
        {
            Debug.LogError($"[MultiCharacter] Roster update rejected ({error.Code}): {error.Message}");
        }
        catch (InvalidOperationException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
        }
        catch (TimeoutException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
        }
    }

    private static Task<bool> WaitForReadyAsync(MultiCharacterRoomSession session, string membershipId)
    {
        CharacterRoomMembership existing = session.FindByMembershipId(membershipId);
        if (existing != null && existing.Status != CharacterRoomStatus.Starting)
            return Task.FromResult(existing.Status == CharacterRoomStatus.Ready);

        var readySource = new TaskCompletionSource<bool>();

        void OnStatusChanged(CharacterRoomMembership membership)
        {
            if (membership.MembershipId != membershipId) return;
            if (membership.Status == CharacterRoomStatus.Starting) return;

            session.CharacterStatusChanged -= OnStatusChanged;
            readySource.TrySetResult(membership.Status == CharacterRoomStatus.Ready);
        }

        session.CharacterStatusChanged += OnStatusChanged;
        return readySource.Task;
    }

    private void OnDestroy()
    {
        _lifetime.Cancel();
        _lifetime.Dispose();
    }
}
```
{% endcode %}

{% hint style="warning" %}
Add the incoming character before removing the outgoing one. Removing first, even with a replacement target queued for a later call, briefly leaves the roster without the character you intend to hand the conversation to.
{% endhint %}

### Expected outcome

`AddCharacterAsync` returns the incoming character's new membership, and `WaitForReadyAsync` resolves once `CharacterStatusChanged` reports it as `Ready` or `Failed`. `RemoveCharacterAsync` then removes the outgoing membership and, in the same acknowledged command, moves `ActiveMembershipId` to the incoming membership — `CharacterRosterUpdateResult.ActiveMembershipId` reports the new target directly, with no separate call to `SetInteractionTargetAsync` needed. The roster holds at least one member throughout the swap.

The command is atomic from the caller's point of view, but not from an event subscriber's. The SDK applies the removal before it applies the new target, so `InteractionTargetChanged` fires twice: once with `current` as `null` while the outgoing membership is removed, then again with the incoming membership. Code that reacts to a `null` target by, for example, dimming an interface should debounce it rather than treat it as the end of the conversation.

## Next steps

{% content-ref url="update-the-roster.md" %}
[Add and remove characters at runtime](update-the-roster.md)
{% endcontent-ref %}

{% content-ref url="switch-the-interaction-target.md" %}
[Switch the interaction target](switch-the-interaction-target.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot multi-character sessions](troubleshooting.md)
{% endcontent-ref %}
