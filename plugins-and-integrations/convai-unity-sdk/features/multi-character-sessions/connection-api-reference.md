---
title: Multi-character connection API reference
description: Reference for the multi-character connection operations, their join and connect option types, and every exception each operation can throw.
last_reviewed: "4.6.0"
---

This page lists the multi-character members of `IConvaiRoomConnectionService`, the `MultiCharacterJoinOptions` type, the multi-character fields on `RoomSessionConnectOptions`, and the exceptions and timeouts each operation produces. All types are in the `Convai.Runtime.Room` namespace.

***

## `IConvaiRoomConnectionService` — multi-character members

Defined in `SDK/Runtime/Room/IConvaiRoomConnectionService.cs:68-147`. Access the service through `ConvaiManager.ActiveManager.TryGetRoomConnectionService(out IConvaiRoomConnectionService roomService)`.

| Member | Signature | Returns |
| --- | --- | --- |
| `CurrentMultiCharacterSession` | `MultiCharacterRoomSession CurrentMultiCharacterSession { get; }` | The canonical roster for the current room, or `null` for a single-character room. |
| `JoinMultiCharacterRoomAsync` | `JoinMultiCharacterRoomAsync(MultiCharacterJoinOptions options, CancellationToken cancellationToken = default)` | `IConvaiOperation<RoomSession>` |
| `SetInteractionTargetAsync` | `SetInteractionTargetAsync(IConvaiCharacterAgent character, CancellationToken cancellationToken = default)` | `IConvaiOperation<InteractionTargetResult>` |
| `SetInteractionTargetAsync` | `SetInteractionTargetAsync(string membershipId, CancellationToken cancellationToken = default)` | `IConvaiOperation<InteractionTargetResult>` |
| `ClearInteractionTargetAsync` | `ClearInteractionTargetAsync(CancellationToken cancellationToken = default)` | `IConvaiOperation<InteractionTargetResult>` |
| `AddCharacterAsync` | `AddCharacterAsync(IConvaiCharacterAgent character, string characterSessionId = null, CancellationToken cancellationToken = default)` | `IConvaiOperation<CharacterRosterUpdateResult>` |
| `RemoveCharacterAsync` | `RemoveCharacterAsync(string membershipId, string replacementTargetMembershipId = null, CancellationToken cancellationToken = default)` | `IConvaiOperation<CharacterRosterUpdateResult>` |
| `RemoveCharacterAsync` | `RemoveCharacterAsync(IConvaiCharacterAgent character, string replacementTargetMembershipId = null, CancellationToken cancellationToken = default)` | `IConvaiOperation<CharacterRosterUpdateResult>` |

See [Operation & Stream Types](../../scripting-reference/operation-and-stream-types.md) for how to consume `IConvaiOperation<T>`. Result and exception types are documented on [Multi-character room session reference](room-session-reference.md).

***

## Concurrency gates

`ConvaiRoomManager` serializes each command family through its own `SemaphoreSlim(1, 1)`, defined in `SDK/Runtime/Adapters/Networking/ConvaiRoomManager.Connection.cs:27-28`. At most one roster mutation and one interaction-target change are in flight at a time.

| Gate | Guards |
| --- | --- |
| `_rosterMutationGate` | `AddCharacterAsync`, both `RemoveCharacterAsync` overloads |
| `_interactionTargetMutationGate` | Both `SetInteractionTargetAsync` overloads, `ClearInteractionTargetAsync` |

A second call to an operation in the same family waits for the first to finish rather than running concurrently.

***

## Exceptions and timeouts

Every operation faults its `IConvaiOperation<T>` rather than throwing synchronously. Handle the exception on the awaited task.

### Preconditions common to every operation

| Condition | Exception | Message |
| --- | --- | --- |
| No multi-character room is active | `InvalidOperationException` | `No multi-character room session is active.` |
| The multi-character room changed while a command was waiting on its gate | `InvalidOperationException` | `The multi-character room changed while this update was waiting.` |
| The room data channel is not ready | `InvalidOperationException` | `The room data channel is not ready.` |

### `JoinMultiCharacterRoomAsync`

| Condition | Exception | Message |
| --- | --- | --- |
| `options` is `null` | `ArgumentNullException` | — (`options`) |
| Convai rejects the join or the underlying connect attempt otherwise fails | `ConvaiOperationException` | The backend session error code and message. |

`JoinMultiCharacterRoomAsync` converts `options` to a `RoomSessionConnectOptions` with `JoinExistingMultiCharacterRoom` set to `true`, then calls the same connect path as `ConnectAsync` (`ConvaiRoomManager.Connection.cs:58-66`). It does not send a roster, so the roster-validation exceptions in [Connect-time roster validation](#connect-time-roster-validation) do not apply to it — but it inherits `ConnectAsync`'s other failure modes, including a `ConvaiOperationException` for a rejected or unreachable connection. See [Join an existing multi-character session](join-an-existing-session.md#troubleshooting) for the join-specific causes and their fixes.

### `SetInteractionTargetAsync`

`SetInteractionTargetAsync` has two overloads: one takes an `IConvaiCharacterAgent`, the other takes a `membershipId` string. Both share the same timeout and acknowledgement-failure behavior; only the not-a-member check differs by parameter.

| Condition | Exception | Message |
| --- | --- | --- |
| The character overload's `character` is not a member of the current room | `ArgumentException` | `The character is not a member of the current room.` (`character`) |
| The membership-ID overload's `membershipId` is not part of the current room | `ArgumentException` | `The membership is not part of the current room.` (`membershipId`) |
| The target membership was removed while the command waited on the gate | `InvalidOperationException` | `The interaction target was removed while this update was waiting.` |
| No acknowledgement within 10 seconds | `TimeoutException` | `Timed out waiting for the interaction-target acknowledgement.` |
| Convai's acknowledgement reports a non-success status | `InvalidOperationException` | The backend message, or `Interaction target update failed.` when Convai reported none. |

### `ClearInteractionTargetAsync`

`ClearInteractionTargetAsync` sends an empty target, so the "removed while waiting" check does not apply. It shares the same timeout and acknowledgement-failure behavior as the two `SetInteractionTargetAsync` overloads above.

{% hint style="info" %}
Clearing the interaction target does not interrupt audio a character is already playing. It only stops new player input from being routed to that character.
{% endhint %}

### `AddCharacterAsync`

| Condition | Exception | Message |
| --- | --- | --- |
| `character` is `null` | `ArgumentNullException` | — (`character`) |
| `character.CharacterId` is empty | `ArgumentException` | `The character must have a character ID.` (`character`) |
| The local character instance is already a member of the room | `ArgumentException` | `This local character instance is already a member of the current room. Use another instance when adding a clone.` (`character`) |
| The same local character was added while this command waited on the gate | `InvalidOperationException` | `The local character was added while this roster update was waiting.` |
| No acknowledgement within 15 seconds | `TimeoutException` | `Timed out waiting for the character-roster-update acknowledgement.` |
| Convai's acknowledgement reports a non-success status | `CharacterRosterUpdateException` | The backend message, or `Character roster update failed.` when Convai reported none. See [Multi-character room session reference](room-session-reference.md#characterrosterupdateexception). |

### `RemoveCharacterAsync`

`RemoveCharacterAsync` has two overloads: one takes a `membershipId` string, the other takes an `IConvaiCharacterAgent`. Both share the replacement-target and gate-race checks; only the not-a-member check differs by parameter.

| Condition | Exception | Message |
| --- | --- | --- |
| The character overload's `character` is `null` | `ArgumentNullException` | — (`character`) |
| The membership-ID overload's `membershipId` is not part of the current room | `ArgumentException` | `The membership is not part of the current room.` (`membershipId`) |
| The character overload's `character` is not a member of the current room | `ArgumentException` | `The character is not a member of the current room.` (`character`) |
| `replacementTargetMembershipId` is not part of the current room | `ArgumentException` | `The replacement target is not part of the current room.` (`replacementTargetMembershipId`) |
| `replacementTargetMembershipId` equals the membership being removed | `ArgumentException` | `The replacement target cannot be the membership being removed.` (`replacementTargetMembershipId`) |
| The membership being removed was removed while this command waited on the gate | `InvalidOperationException` | `The character membership was removed while this roster update was waiting.` |
| The replacement target was removed while this command waited on the gate | `InvalidOperationException` | `The replacement target was removed while this roster update was waiting.` |
| No acknowledgement within 15 seconds | `TimeoutException` | `Timed out waiting for the character-roster-update acknowledgement.` |
| Convai's acknowledgement reports a non-success status | `CharacterRosterUpdateException` | The backend message, or `Character roster update failed.` when Convai reported none. |

{% hint style="warning" %}
A replacement target must already be a member of the room and must not be the membership being removed. The roster can never become empty: removing the active membership without a valid replacement leaves the target cleared rather than deleting the last membership.
{% endhint %}

***

## Connect-time roster validation

A scene that registers two or more characters builds its roster during `ConnectAsync`, before any of the operations above run. The SDK validates that roster in `RoomConnectionRuntimeAdapter.ApplyMultiCharacterTopology` and throws a `ConvaiOperationException` for each condition below. An outer handler in the same adapter (`RoomConnectionRuntimeAdapter.cs:328-341`) catches every exception raised during connect and re-wraps it into a `ConnectionFailure` carrying `SessionErrorCodes.ConnectionFailed`. The caller sees a `ConvaiOperationException` with the **original message** below, but its `Code` is `ConnectionFailed` — the original codes (`ConnectionBadRequest`, `ConfigCharacterIdMissing`) are not observable at the call site.

| Condition | Message (Code at the call site is always `ConnectionFailed`) |
| --- | --- |
| More than 50 characters registered | `Multi-character rooms support at most 50 characters.` |
| A null or repeated character reference | `Multi-character roster contains null or duplicate character references.` |
| A character with no Character ID | `Every character in a multi-character room requires a Character ID.` |
| Two characters resolving to the same character-session ID | `Character session IDs must be unique within a multi-character roster.` |

This validation runs only when building a roster at connect. `JoinMultiCharacterRoomAsync` sends no roster, so it never raises these exceptions.

***

## `MultiCharacterJoinOptions`

`MultiCharacterJoinOptions` is a serializable class passed to `JoinMultiCharacterRoomAsync`. Defined in `SDK/Runtime/Room/TurnTakingOptions.cs:404-432`.

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `RoomSessionId` | `string` | `null` | The durable room identifier returned by the creating client's connect call. Use this or `SharedSessionKey`, not both. |
| `SharedSessionKey` | `string` | `null` | An alternative developer-controlled locator for the room. Use this or `RoomSessionId`, not both. |
| `EndUserId` | `string` | `null` | A stable developer identifier for the joining player. |
| `EndUserMetadata` | `IReadOnlyDictionary<string, object>` | `null` | Additional metadata for the end user. |
| `TurnTaking` | `TurnTakingOptions` | `TurnTakingOptions.CreateHandsFreeDefault()` | The turn-taking configuration for the joining participant. See [Turn-taking modes](../../core-concepts/turn-taking-modes.md). |

Joining converts these fields into a `RoomSessionConnectOptions` with `JoinExistingMultiCharacterRoom` set to `true` and sends connect mode `join` with no character roster.

***

## `RoomSessionConnectOptions` — multi-character fields

`RoomSessionConnectOptions` is the options type accepted by `ConnectAsync(RoomSessionConnectOptions, CancellationToken)`. Defined in `SDK/Runtime/Room/TurnTakingOptions.cs:329-358`. The table below covers the fields relevant to multi-character sessions only; see [ConvaiManager API](../../scripting-reference/convaimanager-api.md#roomsessionconnectoptions-fields) for the complete field list.

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `SharedSessionKey` | `string` | `null` | Optional shared session key used to group multiplayer participants into the same room. |
| `RoomSessionId` | `string` | `null` | Durable multi-character room identifier used when joining an existing room. Set through `MultiCharacterJoinOptions` for normal use rather than directly. |
| `JoinExistingMultiCharacterRoom` | `bool` | `false` | Selects a topology-free human join rather than building and sending a roster. |
| `MaxNumParticipants` | `int` | `0` | Optional maximum number of participants for the shared session. |

***

## Related reference

{% content-ref url="room-session-reference.md" %}
[Multi-character room session reference](room-session-reference.md)
{% endcontent-ref %}

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Build your first multi-character session](quick-start.md)
{% endcontent-ref %}
