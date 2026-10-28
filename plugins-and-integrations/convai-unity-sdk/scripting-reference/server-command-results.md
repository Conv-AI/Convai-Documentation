---
title: Server command results
description: Distinguish sent, acknowledged, refused, and unanswered room commands, and understand result-correlation limits in shared conversations.
last_reviewed: "5.0.0-preview"
---

A command accepted by local code may still be refused or unanswered by the service. APIs returning `IConvaiOperation<ServerCommandResult>` expose that distinction. Await the operation, then inspect `Status`; a successfully completed operation can contain a failed or unsent command result.

## Result status

| `ServerCommandStatus` | Meaning |
| --- | --- |
| `Succeeded` | The service answered that it completed the command |
| `Failed` | The service refused it; inspect Reason |
| `Unanswered` | Sent, but no answer arrived |
| `NotConnected` | No usable connection/session, or a group-specific send/start failure |
| `NotTarget` | Not sent because the character is not the target or routing is changing |
| `Refused` | Locally refused or superseded before sending |

`WasSent` is true only for Succeeded, Failed, and Unanswered. `CommandType`, `Reason`, `CharacterId`, `ParticipantId`, and `Extras` describe the outcome. Unanswered does not prove failure: the service may have received the command without returning a correlatable answer.

Reasons include `payload_too_large`, `superseded`, and `conversation_not_started` for local refusal. Group flows can also report `command_timeout`, `session_closed`, `no_session`, `send_failed`, or `group_conversation_starting`. The result's status and reason should drive recovery together. Resending an oversized payload unchanged will not help.

## Result correlation

The service does not echo a universal request ID. Matching uses command type, answering character, and a command-specific echoed ID when available, then oldest-first ordering. Context updates can carry an update ID; saved narrative triggers can carry a trigger name. Group context responses use an envelope ID mapped back to the update/member.

All clients in a shared room receive the answers. Without a distinguishing echoed ID, an answer can complete another player's same-kind command to the same character. Do not use these results as an exactly-once transaction guarantee.

## Observe raw answers

`ConvaiManager.Events.OnServerCommandResultReceived` emits `ServerCommandResultReceived` from `Convai.Domain.DomainEvents.Runtime`. It includes `CommandType`, raw `Status`, `Succeeded`, `Reason`, `Message`, `Extras`, character/participant IDs, and timestamp. It also receives parse/validation errors and other players' answers.

Prefer the per-send result when available. The raw event is useful for diagnostics but does not, by itself, identify which local call caused the answer. `Message` and `Extras` can repeat player text; avoid logging them indiscriminately.

## Related pages

- [Narrative Design scripting reference](../features/narrative-design/scripting-narrative-design.md)
- [Dynamic context scripting API](../features/dynamic-context/dynamic-context-scripting-api.md)
- [Session events](session-events.md)
