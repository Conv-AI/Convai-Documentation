---
title: Characters joining and leaving
description: Control automatic and scripted roster changes in an existing room, preserve a valid replacement target, and handle refused or ambiguous updates.
last_reviewed: "5.0.0-pre.1"
---

A connected multi-character room can accept new manager-owned, selected characters during play. Change scene ownership or the manager’s selected character list to add or remove a character.

## Automatic membership changes

An active character selected in **Characters Joining the Room** can join without a reconnect. It still needs a unique Character ID, a **Live** character version, and account capacity. It enters as `Starting`; wait for readiness before routing input. A successful join logs `'<name>' joined the room without reconnecting.`

Disabling a character keeps its existing seat while it remains owned and selected. Targeting skips the inactive local character; re-enabling reuses the seat. This does not establish any billing or service-capacity exemption.

Destroying the character, dropping manager ownership, or unticking it in **Characters Joining the Room** removes it through the live roster. A successful removal logs `'<name>' left the room without reconnecting.` The automatic planner declines any change that would empty the room before sending it.

## A single-character room cannot grow

A connection created with one active selected character has no roster. Activate at least two selected characters before connecting when the scene needs live additions. The Inspector warns **This room will not be able to grow** when selected inactive characters leave only one active entry; use **Enable It** or **Enable Them** before the next connection.

Changes to the player or **Initial Character** affect connection setup and queue a reconnect rather than a roster edit. Classic rooms and the opt-in [group conversation preview](../group-conversation/README.md) have different prerequisites.

## Change the selected characters from code

Call `ConvaiManager.SetCharactersToConnect` with the full set that should remain in the room. An active selected character owned by the manager can join. To remove one, omit it from the list. The SDK retains the current target if it remains eligible, or chooses a ready replacement when removing it. Keep at least one eligible member selected.

```csharp
// In a method that has the manager and these scene character references:
manager.SetCharactersToConnect(new[] { currentCharacter, incomingCharacter });
```

Wait for `OnRoomRosterChanged` and handle `Refused` before treating a character as seated. When the new character is ready, call `TalkToAsync` if it should receive the player’s next input. See [Multi-character usage examples](usage-examples.md#scripted-roster-handover).

## Handle results and timeouts

A roster edit can fail because the roster changed, the sender lacks permission, or the outgoing target has no eligible replacement. Read `RoomRosterChanged.Reason` for the refusal. The SDK reconciles a `stale_roster_epoch` refusal once before reporting a second refusal for that character.

If lifecycle and route events establish the outcome of a roster edit with a missing acknowledgement, the SDK uses that authoritative state at the deadline. If the outcome remains ambiguous, the SDK retires and disconnects the room. Call `ConvaiManager.ConnectAsync` if the application should begin a new connection.

## Roster limits

The SDK caps an ordinary roster at 50 characters. Account limits can be lower. The separate [group conversation preview](../group-conversation/README.md) accepts two to four characters.

## Next steps

{% content-ref url="usage-examples.md" %}
[Multi-character usage examples](usage-examples.md)
{% endcontent-ref %}
{% content-ref url="handle-roster-events.md" %}
[Handle room events](handle-roster-events.md)
{% endcontent-ref %}
