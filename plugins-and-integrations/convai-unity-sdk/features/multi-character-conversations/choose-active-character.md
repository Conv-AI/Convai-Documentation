---
title: Choose the active character
description: >-
  Route player input to the intended Convai character using raycasts, interface
  controls, triggers, or other application-owned selection logic.
last_reviewed: "4.6.0"
---

Choose which character receives subsequent player input by mapping your application's selection policy to the room's acknowledged interaction-target operation. The SDK supplies the routing API; your Unity project decides whether a raycast, interface control, trigger, proximity rule, or another signal requests the change.

## Prerequisites

- A connected room with a non-null `CurrentMultiCharacterSession`
- At least two `CharacterRoomMembership` entries in the session
- Familiarity with [How multi-character conversations work](how-it-works.md)

## Add a shared target selector

Create one selector component and route every selection policy through it. The component resolves the local character's current membership, waits for Convai's acknowledgement, and logs the canonical route returned by the operation.

{% code title="Assets/Scripts/MultiCharacterTargetSelector.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using System;
using System.Threading.Tasks;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public sealed class MultiCharacterTargetSelector : MonoBehaviour
{
    [SerializeField] private ConvaiManager manager;

    private bool requestInFlight;

    public bool IsRoutingConfirmed { get; private set; } = true;
    public string LastAcknowledgedMembershipId { get; private set; } = string.Empty;

    public async void SelectCharacter(ConvaiCharacter character)
    {
        try
        {
            await SelectCharacterAsync(character);
        }
        catch (Exception exception)
        {
            Debug.LogError($"Interaction target update failed: {exception.Message}", this);
        }
    }

    public async void ClearTarget()
    {
        if (requestInFlight)
            return;

        requestInFlight = true;
        try
        {
            IConvaiRoomConnectionService roomService = GetRoomService();
            IsRoutingConfirmed = false;
            InteractionTargetResult result = await roomService.ClearInteractionTargetAsync();
            LastAcknowledgedMembershipId = result.ActiveMembershipId;
            IsRoutingConfirmed = true;
            Debug.Log(
                $"Interaction target cleared: active={result.ActiveMembershipId}, " +
                $"routeEpoch={result.RouteEpoch}");
        }
        catch (Exception exception)
        {
            Debug.LogError(
                $"Interaction target clear failed; routing is unconfirmed: {exception.Message}",
                this);
        }
        finally
        {
            requestInFlight = false;
        }
    }

    private async Task SelectCharacterAsync(ConvaiCharacter character)
    {
        if (requestInFlight || character == null)
            return;

        requestInFlight = true;
        try
        {
            IConvaiRoomConnectionService roomService = GetRoomService();
            MultiCharacterRoomSession session = roomService.CurrentMultiCharacterSession
                ?? throw new InvalidOperationException("No multi-character room is active.");
            CharacterRoomMembership membership = session.FindByCharacter(character)
                ?? throw new InvalidOperationException("The character is not in the current room.");

            if (membership.Status != CharacterRoomStatus.Ready)
                throw new InvalidOperationException(
                    $"The character is not ready. Current status: {membership.Status}.");

            IsRoutingConfirmed = false;
            InteractionTargetResult result = await roomService
                .SetInteractionTargetAsync(membership.MembershipId);

            LastAcknowledgedMembershipId = result.ActiveMembershipId;
            IsRoutingConfirmed = true;
            Debug.Log(
                $"Interaction target acknowledged: active={result.ActiveMembershipId}, " +
                $"routeEpoch={result.RouteEpoch}");
        }
        finally
        {
            requestInFlight = false;
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
}
```
{% endcode %}

Add `MultiCharacterTargetSelector` to a scene `GameObject` and assign the `ConvaiManager`. Calls made while another target command is awaiting acknowledgement are ignored by this example so the interface cannot queue repeated selections. Gate player input while `IsRoutingConfirmed` is `false`; a timeout means the request outcome is unknown, not that the previous target is still active.

{% hint style="warning" %}
Do not use `SetExplicitConversationTarget` to switch a connected room. That method changes startup ownership and records a pending ownership reconnect. Use `SetInteractionTargetAsync` for live routing.
{% endhint %}

## Select with a center-screen raycast

The raycast only decides which local character the player selected. The shared selector performs the room operation.

{% code title="Assets/Scripts/CenterRaycastCharacterPicker.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using Convai.Runtime.Components;
using UnityEngine;

public sealed class CenterRaycastCharacterPicker : MonoBehaviour
{
    [SerializeField] private Camera viewCamera;
    [SerializeField] private MultiCharacterTargetSelector targetSelector;
    [SerializeField, Min(1f)] private float maximumDistance = 15f;
    [SerializeField] private LayerMask targetLayers = ~0;

    public void SelectCenterRaycastTarget()
    {
        if (viewCamera == null || targetSelector == null)
            return;

        Ray ray = viewCamera.ViewportPointToRay(new Vector3(0.5f, 0.5f));
        if (!Physics.Raycast(
                ray,
                out RaycastHit hit,
                maximumDistance,
                targetLayers,
                QueryTriggerInteraction.Ignore))
            return;

        ConvaiCharacter character = hit.collider.GetComponentInParent<ConvaiCharacter>();
        if (character != null)
            targetSelector.SelectCharacter(character);
    }
}
```
{% endcode %}

Attach the picker to your input controller, assign the camera and selector, and invoke `SelectCenterRaycastTarget` from the input action that confirms a selection. Each selectable character needs a collider on the configured target layers.

## Select from interface controls

Bind a Unity UI `Button` without adding another routing implementation:

{% stepper %}
{% step %}
### Add the selection callback

In the button's **On Click ()** list, add the `GameObject` containing `MultiCharacterTargetSelector`.
{% endstep %}

{% step %}
### Choose the character method

Select `MultiCharacterTargetSelector.SelectCharacter` and assign the `ConvaiCharacter` that the button represents as the object argument.
{% endstep %}

{% step %}
### Add an optional clear control

Bind another button to `MultiCharacterTargetSelector.ClearTarget` when the interface needs a state where player input is not routed to any character.
{% endstep %}
{% endstepper %}

## Apply another selection policy

Other policies call the same `SelectCharacter` method. The policy controls when to request a route, while the selector keeps acknowledgement and error handling consistent.

| Policy | Request the target when |
| --- | --- |
| Trigger volume | The player enters a character's interaction region |
| Proximity | A ready character becomes the nearest eligible membership |
| Gameplay state | A mission, dialogue choice, or facilitator control names the next character |
| Direct interface | The player selects a portrait, list row, or world-space control |

Avoid changing targets every frame. Request a route when the selected character changes, and keep the current target during an active player or character turn if your experience should not redirect that turn mid-conversation.

## Verify the acknowledged target

After the operation completes, treat `InteractionTargetResult.ActiveMembershipId` and the session's `ActiveMembershipId` as canonical. The session also raises `InteractionTargetChanged` with the previous and current memberships.

If an operation faults, re-read the session before updating the interface. A rejected acknowledgement can apply a newer canonical membership before raising the exception. A timeout has no confirmed result, so stop accepting input until a later canonical acknowledgement or reconnect establishes the route.

{% hint style="success" %}
The Console reports `Interaction target acknowledged` with the selected membership ID. Subsequent player input is routed to that membership without reconnecting the room.
{% endhint %}

`ConvaiManager.ActiveConversationCharacter` remains the startup ownership target and does not update after a live route change. Clearing the target affects future player input but does not stop audio that is already playing.

## Next steps

{% content-ref url="manage-characters-at-runtime.md" %}
[Manage characters at runtime](manage-characters-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="transcripts-and-events.md" %}
[Handle multi-character transcripts and events](transcripts-and-events.md)
{% endcontent-ref %}

{% content-ref url="room-connection-api.md" %}
[Multi-character room connection API](room-connection-api.md)
{% endcontent-ref %}
