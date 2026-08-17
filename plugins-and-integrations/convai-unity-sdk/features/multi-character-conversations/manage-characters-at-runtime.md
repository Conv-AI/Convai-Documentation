---
title: Manage characters at runtime
description: >-
  Add and remove Convai characters from a connected Unity room while preserving
  readiness checks and a valid interaction target.
last_reviewed: "4.6.0"
---

Add or remove character memberships without disconnecting the shared room. Use this pattern when a character enters or leaves an active training scenario and application logic must wait for canonical roster acknowledgements and character readiness.

## Prerequisites

- A room that started with at least two active characters and has a non-null `CurrentMultiCharacterSession`
- A future character with a distinct non-empty **Character ID**
- The future character included in the bootstrap's explicit character list but inactive at startup
- A ready replacement character when the membership being removed is the active interaction target

{% hint style="warning" %}
`AddCharacterAsync` only works when a multi-character session already exists. A legacy room that started with one character cannot be converted at runtime; reconnect with at least two active startup characters instead.
{% endhint %}

## Add a roster controller

The controller below activates an owned character, yields once so its runtime components can register, sends the add operation, and then waits for that membership's `Ready` or `Failed` status. Its remove path supplies a ready replacement when the departing membership is active.

{% code title="Assets/Scripts/MultiCharacterRosterController.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public sealed class MultiCharacterRosterController : MonoBehaviour
{
    [SerializeField] private ConvaiManager manager;
    [SerializeField] private ConvaiCharacter characterToAdd;
    [SerializeField] private ConvaiCharacter characterToRemove;
    [SerializeField] private ConvaiCharacter replacementCharacter;

    public async void AddConfiguredCharacter()
    {
        try
        {
            CharacterRoomMembership membership = await AddCharacterAsync(characterToAdd);
            Debug.Log(
                $"Character ready: membership={membership.MembershipId}, " +
                $"roster={GetSession().Characters.Count}");
        }
        catch (CharacterRosterUpdateException exception)
        {
            Debug.LogError(
                $"Roster add rejected: code={exception.Code}, message={exception.Message}",
                this);
        }
        catch (Exception exception)
        {
            Debug.LogError($"Roster add failed: {exception.Message}", this);
        }
    }

    public async void RemoveConfiguredCharacter()
    {
        try
        {
            await RemoveCharacterAsync(characterToRemove, replacementCharacter);
            Debug.Log($"Character removed: roster={GetSession().Characters.Count}");
        }
        catch (CharacterRosterUpdateException exception)
        {
            Debug.LogError(
                $"Roster removal rejected: code={exception.Code}, message={exception.Message}",
                this);
        }
        catch (Exception exception)
        {
            Debug.LogError($"Roster removal failed: {exception.Message}", this);
        }
    }

    private async Task<CharacterRoomMembership> AddCharacterAsync(ConvaiCharacter character)
    {
        if (character == null)
            throw new ArgumentNullException(nameof(character));

        IConvaiRoomConnectionService roomService = GetRoomService();
        MultiCharacterRoomSession session = GetSession(roomService);

        if (!character.gameObject.activeSelf)
            character.gameObject.SetActive(true);
        if (!character.enabled)
            character.enabled = true;

        // Yield once so the character's runtime modules can register before admission.
        await Task.Yield();

        CharacterRosterUpdateResult result = await roomService.AddCharacterAsync(character);
        if (result.Added.Count != 1)
            throw new InvalidOperationException(
                $"Expected one added membership, received {result.Added.Count}.");

        CharacterRoomMembership membership = result.Added[0];
        await WaitForMembershipReadyAsync(session, membership, TimeSpan.FromSeconds(60));
        return membership;
    }

    private async Task RemoveCharacterAsync(
        ConvaiCharacter character,
        ConvaiCharacter replacement)
    {
        if (character == null)
            throw new ArgumentNullException(nameof(character));

        IConvaiRoomConnectionService roomService = GetRoomService();
        MultiCharacterRoomSession session = GetSession(roomService);
        CharacterRoomMembership membership = session.FindByCharacter(character)
            ?? throw new InvalidOperationException("The character is not in the current roster.");

        string replacementMembershipId = null;
        if (membership.MembershipId == session.ActiveMembershipId)
        {
            CharacterRoomMembership replacementMembership = session.FindByCharacter(replacement)
                ?? throw new InvalidOperationException(
                    "Assign a replacement character from the current roster.");

            if (replacementMembership.Status != CharacterRoomStatus.Ready)
                throw new InvalidOperationException("The replacement character is not ready.");

            replacementMembershipId = replacementMembership.MembershipId;
        }

        CharacterRosterUpdateResult result = await roomService.RemoveCharacterAsync(
            membership.MembershipId,
            replacementMembershipId);

        if (result.Removed.Count != 1)
            throw new InvalidOperationException(
                $"Expected one removed membership, received {result.Removed.Count}.");
    }

    private static async Task WaitForMembershipReadyAsync(
        MultiCharacterRoomSession session,
        CharacterRoomMembership membership,
        TimeSpan timeout)
    {
        if (membership.Status == CharacterRoomStatus.Ready)
            return;
        if (membership.Status == CharacterRoomStatus.Failed)
            throw new InvalidOperationException(
                $"Character startup failed: {membership.FailureCode ?? "unknown"}.");

        var completion = new TaskCompletionSource<bool>(
            TaskCreationOptions.RunContinuationsAsynchronously);

        void HandleStatusChanged(CharacterRoomMembership changed)
        {
            if (!ReferenceEquals(changed, membership))
                return;

            if (changed.Status == CharacterRoomStatus.Ready)
                completion.TrySetResult(true);
            else if (changed.Status == CharacterRoomStatus.Failed)
                completion.TrySetException(new InvalidOperationException(
                    $"Character startup failed: {changed.FailureCode ?? "unknown"}."));
        }

        session.CharacterStatusChanged += HandleStatusChanged;
        using var timeoutSource = new CancellationTokenSource(timeout);
        using CancellationTokenRegistration registration = timeoutSource.Token.Register(
            () => completion.TrySetCanceled(timeoutSource.Token));

        try
        {
            // Recheck after subscribing so a status change cannot be missed.
            HandleStatusChanged(membership);
            await completion.Task;
        }
        catch (OperationCanceledException)
        {
            throw new TimeoutException(
                $"Timed out waiting for membership {membership.MembershipId} to become ready.");
        }
        finally
        {
            session.CharacterStatusChanged -= HandleStatusChanged;
        }
    }

    private IConvaiRoomConnectionService GetRoomService()
    {
        ConvaiManager runtimeManager = manager != null ? manager : ConvaiManager.ActiveManager;
        if (runtimeManager == null ||
            !runtimeManager.TryGetRoomConnectionService(out IConvaiRoomConnectionService roomService))
            throw new InvalidOperationException("The room connection service is unavailable.");

        return roomService;
    }

    private MultiCharacterRoomSession GetSession() => GetSession(GetRoomService());

    private static MultiCharacterRoomSession GetSession(IConvaiRoomConnectionService roomService) =>
        roomService.CurrentMultiCharacterSession
        ?? throw new InvalidOperationException("No multi-character room is active.");
}
```
{% endcode %}

Add `MultiCharacterRosterController` to a scene `GameObject`. Assign the manager, the inactive character to add, the character that will leave, and a ready character that can become the replacement target.

## Add the inactive character

Invoke `AddConfiguredCharacter` from your gameplay rule or a Unity UI `Button`. The method activates the local character, submits `AddCharacterAsync`, and waits until `CharacterStatusChanged` reports `Ready`.

The returned `CharacterRosterUpdateResult` is an admission acknowledgement. It can contain a membership whose status is still `Starting`, so do not expose that character as selectable until its readiness wait completes.

If the new character should resume a known conversation, use the `AddCharacterAsync` overload's `characterSessionId` argument. A fresh add leaves that argument empty.

## Remove a character

Invoke `RemoveConfiguredCharacter` after assigning **Character To Remove** and **Replacement Character**. A replacement is required by this example only when the departing membership matches `ActiveMembershipId`.

`RemoveCharacterAsync` removes the membership from the shared room. It does not destroy or deactivate the local `GameObject`. Apply that presentation change after the acknowledgement when your scene no longer needs the object.

Passing no replacement for an active removal allows the canonical target to become empty. Supplying a ready replacement keeps subsequent player input routed to a valid membership.

## Observe roster changes

The same `MultiCharacterRoomSession` raises `CharacterAdded`, `CharacterStatusChanged`, `CharacterRemoved`, and, when the active membership changes, `InteractionTargetChanged`. `RosterEpoch` advances with canonical roster state.

Roster and target commands are serialized and acknowledgement-based. Catch `CharacterRosterUpdateException` to read Convai's safe `Code`, and handle `TimeoutException`, cancellation, or a changed session without assuming the requested mutation applied.

After reconnect, reacquire `CurrentMultiCharacterSession` and attach listeners to the new session instance. Do not retain membership IDs or event subscriptions from the previous connection.

## Verify the roster lifecycle

Run a `2 → 3 → 2` check:

1. Start with two active, ready memberships.
2. Add the inactive character and wait for the `Character ready` message.
3. Remove one membership and provide the remaining ready character as replacement when needed.
4. Confirm the room session ID did not change and the final roster count is `2`.

{% hint style="success" %}
The roster changes without disconnecting the room. The added membership reaches `Ready`, the removed membership is no longer returned by `FindByCharacter`, and `ActiveMembershipId` resolves to a remaining membership or is empty by design.
{% endhint %}

## Next steps

{% content-ref url="session-and-roster-api.md" %}
[Multi-character session and roster API](session-and-roster-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-limits.md" %}
[Troubleshoot multi-character conversations](troubleshooting-and-limits.md)
{% endcontent-ref %}

{% content-ref url="audio-and-media-api.md" %}
[Multi-character audio and media API](audio-and-media-api.md)
{% endcontent-ref %}
