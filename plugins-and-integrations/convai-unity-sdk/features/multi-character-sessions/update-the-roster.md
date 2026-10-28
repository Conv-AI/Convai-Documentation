---
title: Characters joining and leaving
description: Control automatic and scripted roster changes in an existing room, preserve a valid replacement target, and handle refused or ambiguous updates.
last_reviewed: "5.0.0-preview"
---

A connected multi-character room can accept new manager-owned, selected characters during play. Use the automatic roster for ordinary scene lifecycle changes; use explicit add/remove operations when application logic owns the transition.

## Automatic membership changes

An active character selected in **Characters Joining the Room** can join without a reconnect. It still needs a unique Character ID, a **Live** character version, and account capacity. It enters as `Starting`; wait for readiness before routing input. A successful join logs `'<name>' joined the room without reconnecting.`

Disabling a character keeps its existing seat while it remains owned and selected. Targeting skips the inactive local character; re-enabling reuses the seat. This does not establish any billing or service-capacity exemption.

Destroying the character, dropping manager ownership, or unticking it in **Characters Joining the Room** removes it through the live roster. A successful removal logs `'<name>' left the room without reconnecting.` The automatic planner declines any change that would empty the room before sending it.

## A single-character room cannot grow

A connection created with one active selected character has no roster. Activate at least two selected characters before connecting when the scene needs live additions. The Inspector warns **This room will not be able to grow** when selected inactive characters leave only one active entry; use **Enable It** or **Enable Them** before the next connection.

Changes to the player or **Initial Character** affect connection setup and queue a reconnect rather than a roster edit. Classic rooms and the opt-in [group conversation preview](../group-conversation/README.md) have different prerequisites.

## Add a character explicitly

Retrieve `IConvaiRoomConnectionService` with `ConvaiManager.TryGetRoomConnectionService`, then await:

```csharp
// Method-body fragment; roomService, incoming, and cancellationToken are supplied.
CharacterRosterUpdateResult result = await roomService.AddCharacterAsync(
    incoming, cancellationToken: cancellationToken);
if (result.Added.Count == 0)
    throw new InvalidOperationException("No membership was returned for the add.");
await result.Added[0].WaitUntilReadyAsync(cancellationToken);
```

`characterSessionId` optionally resumes an earlier conversation. It does not permit duplicate Character IDs. Adding the same component twice or another component with the same ID is refused. Specific/pinned versions raise `ConvaiOperationException`; use **Live**.

Choose one owner for the add. Do not activate a manager-owned selected object for automatic joining and simultaneously issue a competing explicit add. Read the current session first if another path may already have seated it. See [Multi-character usage examples](usage-examples.md) for a helper that handles an already-present member.

## Remove a character from the roster

Await `RemoveCharacterAsync(characterOrMembershipId, replacementTargetMembershipId, cancellationToken)`. Pass a Ready member's ID when the handover destination matters. It must be in the room and different from the outgoing member.

With no explicit replacement, 5.0 chooses at send time: retain the current target if it remains, otherwise choose another Ready, enabled local member. The service can refuse the request with `replacement_target_required` or `replacement_target_unavailable`. Do not assume removal will clear the target or that it will be accepted without a replacement.

An acknowledged removal with a replacement produces one `InteractionTargetChanged(outgoing, replacement)` event, then `CharacterRemoved`; there is no intermediate null callback. Explicit removal has no client-side last-member guard equivalent to the automatic planner, so handle the service's response.

## Handle results and timeouts

Catch `CharacterRosterUpdateException` before its base `InvalidOperationException`, and inspect `Code`. Also handle argument errors, `ConvaiOperationException`, timeout, and caller cancellation. Known roster codes include:

| Code | Action |
| --- | --- |
| `roster_epoch_mismatch` | Read current state and reassess the intended edit |
| `unauthorized_sender` | Resolve room-management permission |
| `replacement_target_required` | Supply an eligible Ready replacement |
| `replacement_target_unavailable` | Refresh the roster and select an available replacement |
| `removed_before_seated` | The add lost its member before seating; reassess scene ownership and state |

A 15-second caller timeout does not release the roster gate immediately. The SDK waits for authoritative evidence until the 30-second canonical deadline measured from registration. If the result or route remains ambiguous, it retires and disconnects the room; it does not automatically reconnect. See [Connection API reference](connection-api-reference.md#exceptions-and-timeouts).

## Roster limits

The SDK caps a classic roster at 50 characters both at connect and on add. Account limits may be lower. Connect validation surfaces `ConvaiOperationException`; an add over this ceiling raises `InvalidOperationException`. Select only the characters needed for the conversation. The separate group mode supports 2–4 members, not the classic ceiling.

## Next steps

{% content-ref url="usage-examples.md" %}
[Multi-character usage examples](usage-examples.md)
{% endcontent-ref %}
{% content-ref url="handle-roster-events.md" %}
[Handle room events](handle-roster-events.md)
{% endcontent-ref %}
