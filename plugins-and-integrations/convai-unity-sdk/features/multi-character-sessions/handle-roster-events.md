---
title: Handle room events
description: Subscribe to roster and interaction-target events in a shared Unity room, and rely on the order the SDK guarantees between them.
last_reviewed: "4.6.0"
---

Subscribe to `ConvaiManager.Events.OnRoomRosterChanged` to react to a character joining or leaving a connected room, including a refused edit and its reason. Use this page when your scene needs to update UI, logging, or gameplay state as characters come and go instead of polling the roster.

## Prerequisites

- A connected multi-character session. See [Build your first multi-character session](quick-start.md).
- A `ConvaiManager` reference, for `Events.OnRoomRosterChanged`.

## Subscribe to OnRoomRosterChanged

`ConvaiManager.Events.OnRoomRosterChanged` is `Action<RoomRosterChanged>`, and fires every time a connected room's roster is edited during play — whether the change came from a character appearing or disappearing in the scene, or from an explicit `AddCharacterAsync`/`RemoveCharacterAsync` call.

| `RoomRosterChanged` field | Type | Description |
| --- | --- | --- |
| `Change` | `RoomRosterChange` | `Joined`, `Left`, or `Refused`. |
| `MembershipId` | `string` | The affected room membership. Empty for a join that never got one. |
| `CharacterId` | `string` | Convai Character ID of the character this is about. |
| `CharacterName` | `string` | Display name, for logs and UI. |
| `RosterSize` | `int` | How many characters the room holds after this change. |
| `Reason` | `string` | Why the edit was refused. Empty unless `Change` is `Refused`. |

```csharp
private void OnEnable()
{
    ConvaiManager manager = ConvaiManager.ActiveManager;
    if (manager == null || !manager.IsInitialized) return;
    manager.Events.OnRoomRosterChanged += HandleRosterChanged;
}

private void OnDisable()
{
    ConvaiManager manager = ConvaiManager.ActiveManager;
    if (manager == null) return;
    manager.Events.OnRoomRosterChanged -= HandleRosterChanged;
}

private void HandleRosterChanged(RoomRosterChanged e)
{
    switch (e.Change)
    {
        case RoomRosterChange.Joined:
            Debug.Log($"[MultiCharacter] {e.CharacterName} joined. Roster now has {e.RosterSize}.");
            break;
        case RoomRosterChange.Left:
            Debug.Log($"[MultiCharacter] {e.CharacterName} left. Roster now has {e.RosterSize}.");
            break;
        case RoomRosterChange.Refused:
            Debug.LogWarning($"[MultiCharacter] {e.CharacterName} could not join or leave: {e.Reason}");
            break;
    }
}
```

`ConvaiManager.Events` throws while the manager is still starting up. It becomes available at the end of the manager's own `Awake`, so `OnEnable` and `Start` are both safe places to subscribe — another component's `Awake` is not, because Unity gives no ordering guarantee between two `Awake` calls. Guard on `ConvaiManager.IsInitialized` where you cannot control the order.

A character joining a live room is a world event, not a chat event — a nameplate over the character is usually the right place to show it, not the chat field. `ConvaiCharacter.RoomMembershipStatus` reports `Starting` while a given character is still being announced by the service, if you need the per-character state alongside the event.

Also relevant on `ConvaiManager.Events`: `OnConversationTargetChanged` reports the conversation moving between characters, including its `Requested`/`Confirmed`/`Failed` phase, and `OnConversationAvailabilityChanged` reports whether the addressed character can hear the player yet. See [Conversation targeting](../conversation-targeting/README.md) and [Conversation availability](../conversation-availability/README.md).

## The lower-level session events

`MultiCharacterRoomSession` — read from `IConvaiRoomConnectionService.CurrentMultiCharacterSession` — exposes the same facts as plain C# events, one level below `ConvaiManager.Events`. Reach for these only when a script already holds a `MultiCharacterRoomSession` reference and needs `CharacterRoomMembership` objects directly rather than the IDs `OnRoomRosterChanged` reports.

| Event | Signature | Raised when |
| --- | --- | --- |
| `CharacterAdded` | `Action<CharacterRoomMembership>` | A membership is added to the room after it was already connected. |
| `CharacterRemoved` | `Action<CharacterRoomMembership>` | A membership is removed from the room. |
| `CharacterStatusChanged` | `Action<CharacterRoomMembership>` | A membership transitions into `Ready` or `Failed`, or a new membership is inserted into the roster. |
| `InteractionTargetChanged` | `Action<CharacterRoomMembership, CharacterRoomMembership>` | The canonical active membership changes; the current membership is `null` when the target is cleared. |

{% code title="Assets/Scripts/MultiCharacterEventLogger.cs" %}
```csharp
using Convai.Runtime.Room;
using UnityEngine;

public class MultiCharacterEventLogger : MonoBehaviour
{
    private MultiCharacterRoomSession _session;

    public void Attach(MultiCharacterRoomSession session)
    {
        Detach();
        _session = session;
        if (_session == null) return;

        _session.CharacterAdded += HandleCharacterAdded;
        _session.CharacterRemoved += HandleCharacterRemoved;
        _session.CharacterStatusChanged += HandleCharacterStatusChanged;
        _session.InteractionTargetChanged += HandleInteractionTargetChanged;
    }

    public void Detach()
    {
        if (_session == null) return;

        _session.CharacterAdded -= HandleCharacterAdded;
        _session.CharacterRemoved -= HandleCharacterRemoved;
        _session.CharacterStatusChanged -= HandleCharacterStatusChanged;
        _session.InteractionTargetChanged -= HandleInteractionTargetChanged;
        _session = null;
    }

    private void HandleCharacterAdded(CharacterRoomMembership membership) =>
        Debug.Log($"[MultiCharacter] Added {membership.CharacterId} ({membership.MembershipId}).");

    private void HandleCharacterRemoved(CharacterRoomMembership membership) =>
        Debug.Log($"[MultiCharacter] Removed {membership.CharacterId} ({membership.MembershipId}).");

    private void HandleCharacterStatusChanged(CharacterRoomMembership membership) =>
        Debug.Log($"[MultiCharacter] {membership.CharacterId} is now {membership.Status}.");

    private void HandleInteractionTargetChanged(CharacterRoomMembership previous, CharacterRoomMembership current) =>
        Debug.Log($"[MultiCharacter] Target changed from {previous?.MembershipId ?? "none"} to {current?.MembershipId ?? "none"}.");

    private void OnDestroy() => Detach();
}
```
{% endcode %}

## The ordering guarantee when the active character is removed

Removing the membership that currently holds the interaction target produces two events in a fixed order: `InteractionTargetChanged` fires first, with the removed membership as `previous` and `null` as `current`, and `CharacterRemoved` fires second. Code that reacts to `CharacterRemoved` can rely on the interaction target already being cleared by the time it runs — no separate check of `ActiveMembershipId` is needed to avoid a stale read.

{% hint style="warning" %}
This cleared-target `InteractionTargetChanged` does not advance `RouteEpoch`. Removal clears `ActiveMembershipId` directly instead of going through the epoch-guarded target update, so a subscriber that reacts to target changes only by comparing `RouteEpoch` misses this event. Key any such logic off the event itself, not off a `RouteEpoch` change, if it must also react to a target cleared by removal.
{% endhint %}

Passing a replacement target does not suppress that first event. The SDK applies the removal before it applies the new target, so a removal with a replacement fires `InteractionTargetChanged` twice: once with `null` as `current`, then again with the replacement membership. Treat a `null` current target as a transition rather than a terminal state.

A related ordering guarantee applies to additions: when a new membership is inserted, `CharacterAdded` fires before `CharacterStatusChanged` for that same membership. `CharacterAdded` also fires exactly once for a given membership even when Convai's lifecycle message for it arrives before the roster-update acknowledgement does — the SDK deduplicates the two paths rather than raising the event twice.

{% hint style="info" %}
`CharacterAdded` does not fire for the characters present when the room first connects — those memberships are already in `session.Characters` by the time the session object exists. Read the initial roster directly instead of waiting for `CharacterAdded` events for it; the event is for characters added after the room is already up.
{% endhint %}

## Unsubscribe when the session ends

`MultiCharacterRoomSession` is replaced on every reconnect, so a handler attached to one session instance stops receiving events once that instance is discarded. Detach in `OnDisable` or `OnDestroy`, and reattach to the new `CurrentMultiCharacterSession` after `IConvaiRoomConnectionService.Connected` fires again.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `CharacterAdded` never fires for a character the scene started with | Those memberships were populated when the session object was created, not through the runtime-addition code path. | Read `session.Characters` right after connecting instead of waiting for `CharacterAdded`. |
| `InteractionTargetChanged` fires with `current` as `null` unexpectedly | The membership holding the target was removed. This event fires whether or not a replacement target was supplied. | Expected behavior. Pass `replacementTargetMembershipId` to [Characters joining and leaving](update-the-roster.md#remove-a-character-from-the-roster) so a second event immediately restores a target, and treat the `null` as a transition. |
| An event you expected does not fire at all | The underlying acknowledgement was a stale or duplicate one and was discarded because `RosterEpoch` or `RouteEpoch` had already advanced past it. | Read `session.RosterEpoch` / `session.RouteEpoch` and compare against the state you expected before assuming the event was lost. |

## Next steps

{% content-ref url="../conversation-targeting/README.md" %}
[Conversation targeting](../conversation-targeting/README.md)
{% endcontent-ref %}

{% content-ref url="update-the-roster.md" %}
[Characters joining and leaving](update-the-roster.md)
{% endcontent-ref %}

{% content-ref url="character-identity.md" %}
[Character identity](character-identity.md)
{% endcontent-ref %}
