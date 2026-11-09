---
title: Connection API reference
description: Look up room joining, roster edits, current targeting APIs, identity options, validation failures, and recovery after lost acknowledgements.
last_reviewed: "5.0.0-preview"
---

Use `IConvaiRoomConnectionService` for joining and roster edits, and `ConvaiManager` for conversation targeting. Room types live in `Convai.Runtime.Room`; manager components live in `Convai.Runtime.Components`.

## Connection and roster members

Retrieve the service with `ConvaiManager.TryGetRoomConnectionService(out IConvaiRoomConnectionService roomService)`. The signatures below omit namespaces for readability.

| Member | Signature or result |
| --- | --- |
| `CurrentMultiCharacterSession` | `MultiCharacterRoomSession`; null for a single-character room |
| `JoinMultiCharacterRoomAsync` | `(MultiCharacterJoinOptions options, CancellationToken cancellationToken = default)` → `IConvaiOperation<RoomSession>` |
| `AddCharacterAsync` | `(IConvaiCharacterAgent character, string characterSessionId = null, CancellationToken cancellationToken = default)` → `IConvaiOperation<CharacterRosterUpdateResult>` |
| `RemoveCharacterAsync` | `(string membershipId, string replacementTargetMembershipId = null, CancellationToken cancellationToken = default)` → `IConvaiOperation<CharacterRosterUpdateResult>` |
| `RemoveCharacterAsync` | `(IConvaiCharacterAgent character, string replacementTargetMembershipId = null, CancellationToken cancellationToken = default)` → the same result |

See [Operation & Stream Types](../../scripting-reference/operation-and-stream-types.md) for consuming operations and [Room session reference](room-session-reference.md) for results.

## Conversation targeting in 5.0

Use `ConvaiManager.TalkToAsync(ConvaiCharacter)` and `ConvaiManager.ClearConversationTargetAsync()`, both returning `IConvaiOperation<InteractionTargetResult>`. Their operations are not cancellable; calling `Cancel` does not retract a target command. Use **Chosen By > Manual** for persistent scripted targeting, otherwise Look At or Proximity may choose another target.

The former room-service `SetInteractionTargetAsync` overloads and `ClearInteractionTargetAsync` are removed. There is no equivalent public membership-ID-only target setter; the manager API requires a local `ConvaiCharacter`. Clearing a target does not by itself interrupt already-playing audio.

## Validation and failures

Await operations and handle failures on their returned tasks. Joining with null options produces `ArgumentNullException`; rejected or unreachable connection attempts produce `ConvaiOperationException`. Joining creates no new roster and does not wait for the initial character's readiness.

### AddCharacterAsync

Checks include the following, in source order:

| Condition | Failure |
| --- | --- |
| Null character | `ArgumentNullException` |
| Empty Character ID | `ArgumentException` |
| Specific/pinned character version | `ConvaiOperationException` with `ConnectionBadRequest`; use Live |
| No multi-character session | `InvalidOperationException` |
| Same local instance already present | `ArgumentException`; do not add it again |
| Roster would exceed 50 characters | `InvalidOperationException`; account limits may be lower |
| Another member uses the same Character ID | `ArgumentException`; each needs a distinct ID |
| Room or local membership changed while waiting | `InvalidOperationException` |
| Data channel unavailable | `InvalidOperationException` |
| Service refusal | `CharacterRosterUpdateException` with the reported code |
| Member removed before the add could seat it | `CharacterRosterUpdateException`, `removed_before_seated` |

The version check happens before the no-session check. Adding another component with the same Character ID is not supported.

### RemoveCharacterAsync

The character overload rejects a null character. Both overloads reject a nonmember, a replacement that is not in the room, or a replacement equal to the removed member. A changed room, removed membership, or unavailable channel can produce `InvalidOperationException` while the command waits.

With no explicit replacement, 5.0 chooses at send time: keep the current target if it remains, otherwise select another Ready, enabled local member. Pass a Ready replacement when the destination matters. A service can refuse a routed-member removal with `replacement_target_required` or `replacement_target_unavailable`; handle those codes rather than assuming a target will clear or removal will succeed.

The automatic live-roster path declines a change that would empty the room before sending. Explicit removal has no equivalent client-side last-member guard; service acceptance is a separate contract.

### Connect-time roster validation

A creating client checks the full roster before sending it. It rejects more than 50 characters, null/repeated component references, duplicate Character IDs, missing IDs, Specific/pinned versions, and duplicate character-session IDs. These failures surface as `ConvaiOperationException` with `ConnectionFailed` while retaining the diagnostic message.

For pinned versions the message is:

```text
Pinned character versions require a single-character connection. Use Live for multi-character rosters, which accept only bare Character IDs.
```

The 50-character maximum is a client ceiling, not an account entitlement. A join sends no roster, so it does not run these roster-building checks.

## Exceptions and timeouts

Roster mutations are serialized. The caller-facing roster wait can time out after 15 seconds while the SDK continues waiting for the authoritative response and keeps the mutation gate held. Cancelling the caller's wait also cannot retract a command already sent.

A separate canonical deadline is 30 seconds from command registration, not 30 additional seconds after the caller timeout. At that deadline, lifecycle join/leave evidence can settle a roster operation only when it proves the result without leaving route ambiguity. A lost target acknowledgement triggers one state probe after 3 seconds.

If the outcome remains ambiguous, the SDK retires the room and disconnects before reopening input. It does not reconnect automatically from this fail-closed recovery. Inspect the final session state, resolve the cause, and call `ConnectAsync` again to establish a new session. Do not treat a caller timeout as permission to issue duplicate mutations immediately.

## MultiCharacterJoinOptions

Defined in `SDK/Runtime/Room/TurnTakingOptions.cs`.

| Field | Default | Meaning |
| --- | --- | --- |
| `RoomSessionId` | null | Durable room locator; use this or SharedSessionKey |
| `SharedSessionKey` | null | Developer-controlled alternative locator |
| `EndUserId` | null | Stable joining-user identity |
| `EndUserName` | null | Typed name; overrides metadata `name` and player-name fallback |
| `EndUserMetadata` | null | Additional JSON-compatible metadata |
| `TurnTaking` | Hands-free defaults | Joining participant's input policy |

Joining converts these options to `RoomSessionConnectOptions` with `JoinExistingMultiCharacterRoom = true` and no roster.

## RoomSessionConnectOptions

The same file defines the connect options. Relevant fields are `SharedSessionKey`, `RoomSessionId`, `JoinExistingMultiCharacterRoom` (false by default), `MaxNumParticipants` (0 by default), `EndUserId`, `EndUserName`, and `EndUserMetadata`. Use `MultiCharacterJoinOptions` for ordinary joins. Identity is copied and validated for the connect attempt; see [End-user identity](../long-term-memory/end-user-identity.md).

## Related reference

{% content-ref url="room-session-reference.md" %}
[Room session reference](room-session-reference.md)
{% endcontent-ref %}
{% content-ref url="update-the-roster.md" %}
[Characters joining and leaving](update-the-roster.md)
{% endcontent-ref %}
