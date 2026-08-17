---
title: Multi-character session and roster API
description: Reference multi-character session, membership, status, event, targeting result, roster result, and failure types in the Unity SDK.
last_reviewed: "4.6.0"
---

`MultiCharacterRoomSession` is the client-side projection of the canonical room roster. It exposes connection-scoped memberships, readiness, active routing, Convai epochs, roster events, and acknowledgement result types.

## `CharacterRoomStatus`

| Value | Integer | Meaning |
| --- | --- | --- |
| `Starting` | `0` | Convai admitted the membership, but the character has not signaled readiness |
| `Ready` | `1` | The character signaled that it can interact |
| `Failed` | `2` | Character provisioning failed; inspect `FailureCode` |

An acknowledged add begins at `Starting` unless readiness or failure has already been observed. Do not treat roster admission as readiness.

## `CharacterRoomMembership`

One membership binds a Convai roster entry to a local `IConvaiCharacterAgent` when a matching local instance is available.

| Property | Type | Description |
| --- | --- | --- |
| `MembershipId` | `string` | Convai room membership ID used for targeting and removal |
| `CharacterId` | `string` | Convai character ID |
| `SessionId` | `string` | Session identifier supplied for this roster entry |
| `CharacterSessionId` | `string` | Character-session ID used for resume and repeated-instance disambiguation |
| `ParticipantIdentity` | `string` | LiveKit identity assigned to this membership for the current connection |
| `IsInitial` | `bool` | Whether this entry is the initial character |
| `ProvisioningStatus` | `string` | Provisioning status returned for the membership |
| `Character` | `IConvaiCharacterAgent` | Bound local character instance, or `null` when no local instance is available |
| `Status` | `CharacterRoomStatus` | Current client readiness state |
| `FailureCode` | `string` | Failure code when `Status` is `Failed` |
| `ParticipantId` | `string` | Transport participant ID observed for this connection; it can be empty before binding or readiness |

`MembershipId`, `CharacterSessionId`, `ParticipantIdentity`, and `ParticipantId` are different identities. Do not substitute the character ID for any of them.

## `MultiCharacterRoomSession` properties

| Property | Type | Description |
| --- | --- | --- |
| `RoomSessionId` | `string` | Durable multi-character room session identifier |
| `ActiveMembershipId` | `string` | Membership currently selected for future player input; empty when no target is active |
| `RouteEpoch` | `int` | Canonical target-routing epoch for the current connection |
| `RosterEpoch` | `int` | Canonical roster epoch for the current connection |
| `PartialDispatch` | `bool` | Whether the room response reports partial roster dispatch; inspect each membership for its outcome |
| `Characters` | `IReadOnlyList<CharacterRoomMembership>` | Read-only projection of current roster members |
| `InitialCharacter` | `CharacterRoomMembership` | Initial membership, or the first response entry when no entry is marked initial |
| `IsReady` | `bool` | Whether `InitialCharacter.Status` is `Ready` |

`IsReady` reports initial-character readiness only. Secondary memberships can remain `Starting` or become `Failed` while `IsReady` is `true`.

## Session methods

```csharp
Task WaitUntilReadyAsync(CancellationToken cancellationToken = default);

CharacterRoomMembership FindByCharacter(IConvaiCharacterAgent character);

CharacterRoomMembership FindByMembershipId(string membershipId);
```

`WaitUntilReadyAsync` completes when the initial membership becomes ready. It raises `InvalidOperationException` if the initial character fails, and it honors the supplied cancellation token.

`FindByCharacter` matches the local instance by reference. `FindByMembershipId` performs an exact membership-ID lookup. Both return `null` when no match exists.

There is no public lookup method for participant identity or participant ID. Iterate `Characters` and compare the appropriate membership property when correlating transcript or audio data.

## Session events

| Event | Signature | Raised when |
| --- | --- | --- |
| `CharacterStatusChanged` | `Action<CharacterRoomMembership>` | A membership becomes ready or failed; also raised for a newly added starting membership |
| `CharacterAdded` | `Action<CharacterRoomMembership>` | A new membership enters the canonical client roster |
| `CharacterRemoved` | `Action<CharacterRoomMembership>` | A membership leaves the canonical client roster |
| `InteractionTargetChanged` | `Action<CharacterRoomMembership, CharacterRoomMembership>` | A newer route epoch is applied, even when the target is unchanged; active-member removal can also raise it without advancing the route epoch |

The previous or current target argument can be `null`. Clearing a target produces a `null` current membership. Removing the active membership can also raise a target change before `CharacterRemoved`.

Session events are not replayed. Inspect `Characters` and `ActiveMembershipId` immediately after subscribing to establish current state.

## `InteractionTargetResult`

| Property | Type | Description |
| --- | --- | --- |
| `CommandId` | `string` | Client-generated acknowledgement correlation ID |
| `ActiveMembershipId` | `string` | Canonical active membership after the acknowledgement |
| `PreviousMembershipId` | `string` | Membership active before the acknowledged command |
| `RouteEpoch` | `int` | Canonical route epoch after the acknowledgement |
| `Changed` | `bool` | Whether the acknowledgement advanced the canonical route and changed the target |

Use the returned `ActiveMembershipId` or the session's updated value as the source of truth. Do not update UI optimistically before the operation succeeds.

## `CharacterRosterUpdateResult`

| Property | Type | Description |
| --- | --- | --- |
| `CommandId` | `string` | Client-generated acknowledgement correlation ID |
| `Added` | `IReadOnlyList<CharacterRoomMembership>` | Memberships admitted by this command |
| `Removed` | `IReadOnlyList<CharacterRoomMembership>` | Memberships removed by this command |
| `ActiveMembershipId` | `string` | Canonical active target after the roster update |
| `RouteEpoch` | `int` | Canonical route epoch after the roster update |
| `RosterEpoch` | `int` | Canonical roster epoch after the roster update |

An item in `Added` is admitted, not necessarily ready. Observe its `Status` and `CharacterStatusChanged` before routing player input to it.

## `CharacterRosterUpdateException`

`CharacterRosterUpdateException` derives from `InvalidOperationException` and is raised when Convai rejects a roster command.

| Property | Type | Description |
| --- | --- | --- |
| `Code` | `string` | Machine-readable rejection code returned with the acknowledgement |
| `Message` | `string` | Rejection detail inherited from `Exception` |

Cancellation and acknowledgement timeout use `OperationCanceledException` and `TimeoutException`, not `CharacterRosterUpdateException`.

## Lifetime and identity constraints

- Reacquire `CurrentMultiCharacterSession` after every reconnect.
- Treat membership objects, membership IDs, participant identities, participant IDs, `RouteEpoch`, and `RosterEpoch` as connection-scoped.
- Keep character ID, character-session ID, membership ID, participant identity, and participant ID in separate fields.
- Use distinct character IDs when application behavior depends on character-ID-keyed events or audio controls.
- Do not construct membership or roster-result objects directly. The service creates them from canonical room responses and acknowledgements.

## Related reference

Use the connection service to change the fields represented by these models.

{% content-ref url="room-connection-api.md" %}
[Multi-character room connection API](room-connection-api.md)
{% endcontent-ref %}

Use transcript speaker metadata to correlate room turns with memberships.

{% content-ref url="transcripts-and-events.md" %}
[Handle multi-character transcripts and events](transcripts-and-events.md)
{% endcontent-ref %}
