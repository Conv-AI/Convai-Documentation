---
title: Connection API reference
description: Look up room joining, roster edits, current targeting APIs, identity options, validation failures, and recovery after lost acknowledgements.
last_reviewed: "5.0.0-pre.1"
---

Use `ConvaiManager` to connect to a room, choose which scene characters belong to it, and change the addressed character. Inspect the active roster through `ConvaiRoomManager.CurrentMultiCharacterSession`.

## Connection and roster members

| Member | Contract |
| --- | --- |
| `ConnectAsync(RoomSessionConnectOptions options, CancellationToken cancellationToken = default)` | Returns `IConvaiOperation<RoomSession>`. Use `JoinExistingMultiCharacterRoom` for an existing roster room. |
| `SetCharactersToConnect(IEnumerable<ConvaiCharacter> characters)` | Sets the manager’s selection. An active roster room reconciles membership as the selection or scene ownership changes. |
| `UseAllCharactersForConnection()` | Returns to automatic selection of manager-owned characters. |
| `Events.OnRoomRosterChanged` | Reports `Joined`, `Left`, or `Refused` for live roster edits. |
| `TalkToAsync(ConvaiCharacter character)` / `ClearConversationTargetAsync()` | Return `IConvaiOperation<InteractionTargetResult>`. Await the operation to observe confirmation or failure. |
| `ConversationTarget` | Local component for the confirmed target when one exists. |
| `ConvaiRoomManager.CurrentMultiCharacterSession` | Read-only roster state and membership events. The property is `null` when the room has no roster. |

## Connection options

The options below live in `Convai.Runtime.Room.RoomSessionConnectOptions`.

| Field | Contract |
| --- | --- |
| `JoinExistingMultiCharacterRoom` | `false` by default. When `true`, joins an existing roster without sending a character roster. |
| `RoomSessionId` / `SharedSessionKey` | Supply exactly one locator for a join. |
| `MaxNumParticipants` | A positive value requests a participant limit when establishing a shared session. |
| `CharacterSessionId` / `RosterCharacterSessionIds` | Optional saved session IDs for the active character and other selected characters on connect. |
| `TurnTaking` | Per-connection turn-taking options. |
| `EndUserId`, `EndUserName`, `EndUserMetadata` | Connection-scoped [end-user identity](../long-term-memory/end-user-identity.md). |

## Validation and failures

A room opened with one selected active character has no roster. Create a roster with at least two active selected characters and unique IDs. Roster members use Live character versions. The SDK enforces a 50-character ceiling for ordinary roster rooms. Account limits and the group-conversation preview have separate limits.

Inspect the `ConvaiOperationException.Code` on connect failures. For live roster changes, inspect `OnRoomRosterChanged` and its `Reason`. The SDK may retry a stale roster edit after refreshing its roster view. When it cannot establish the outcome by the canonical deadline, it disconnects the session. See [Characters joining and leaving](update-the-roster.md).

## Related reference

{% content-ref url="room-session-reference.md" %}
[Room session reference](room-session-reference.md)
{% endcontent-ref %}
{% content-ref url="update-the-roster.md" %}
[Characters joining and leaving](update-the-roster.md)
{% endcontent-ref %}
