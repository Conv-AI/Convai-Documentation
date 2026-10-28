---
title: Group conversation component reference
description: Look up group scene settings, member aliases, spatial and timing overrides, events, commands, and the meaning of their returned outcomes.
last_reviewed: "5.0.0-preview"
---

Add **Convai > Group Conversation** to opt a room into the preview at connect. `ConvaiGroupConversation` lives in `Convai.Runtime.GroupConversation`. The component validates client configuration; service availability still requires confirmation from the account/service owner.

## Inspector settings

| Section / field | Meaning and limit |
| --- | --- |
| Scene / Player Display Name | How the group refers to the player; up to 64 characters; empty uses the service default |
| Scene / Scene Brief | Required shared situation, up to 4,000 characters |
| Topics | Up to 20 entries; topic ID up to 64, text up to 500 characters |
| Topic Id | Unique; blank authored IDs become `t1`, `t2`, and so on. Do not use the reserved `free-` prefix |
| Topic Starter | Optional roster member; empty lets the service choose |
| Members / Character | Optional per-member settings; must reference the room roster |
| Members / Aliases | Up to 5 per character, each up to 32 characters |
| Spatial / Anchor | Explicit group centre or the characters' centre when the session begins |
| Spatial Query Layers | Layers for visibility and player gaze queries |
| Gaze / Drive Gaze | Enables conversation gaze through the installed gaze module |

Scene brief, display name, topics, aliases, anchor, query layers, and overrides configure the next connect. `DriveGaze` can update the installed gaze director during play. Multiple enabled group components cause a warning; only the newest drives the room.

## Spatial and timing overrides

Only enabled overrides are sent. The Inspector initializes values from the SDK's copy of service defaults; this is not proof the deployed service has the same defaults.

| Override | Initial value |
| --- | --- |
| Hearing Range M | 10 metres |
| Pause Hysteresis M | 2 metres |
| Address Radius M | 5 metres |
| Group Radius M | 4 metres |
| Gaze Dwell Threshold | 0.6 of the press |
| Lull Seconds | 30 |
| Player Reply Wait Seconds | 8 |
| Reply To Question Window Seconds | 8 |
| Empty Transcript Timeout Seconds | 4; override enabled by the SDK to allow microphone drain |
| Greeting Reentry Seconds | 60 |
| Line Timeout Seconds | 20 |

Values must be finite and positive, except pause hysteresis can be zero. Distances are at most 1,000 metres, timings at most 3,600 seconds, and gaze dwell threshold at most 1. Set a nullable public override property to null to stop sending that override.

## State and events

| Public member | Meaning |
| --- | --- |
| `Active` | Current enabled component, or null |
| `Status`, `State` | Latest service status and recognized state |
| `LastPlayerUtterance` | Latest resolved player addressing decision |
| `LastSnapshot` | Latest local spatial measurement, not necessarily sent |
| `IsStarted` | Client-ready was sent after readiness or its timeout |
| `MissedEventCount`, `LateEventCount` | Sequence diagnostics for the current session |
| `GroupRadius`, `HearingRange` | Connected setting, or next-connect setting when no session exists |
| `TryGetCharacter(membershipId, out character)` | Resolve a local scene character from group membership |

Events are raised on the main thread: `Started`, `Stopped`, `StateChanged`, `LineStarted`, `LineAddresseeResolved`, `LineEnded`, `PlayerUtteranceResolved`, and `CommandFailed`. Payloads are immutable snapshots. Inspect inference/supersession flags when using recovered line state; an event alone is not an audio-playback receipt.

## Commands

| Method | Purpose |
| --- | --- |
| `PauseAsync()` | Pause after the current line; the latest pre-start pause/resume request is retained |
| `ResumeAsync()` | Resume the conversation |
| `NextTopicAsync()` | Advance authored topics; refused before start |
| `SetTopicAsync(string id, string text, ConvaiCharacter starter = null)` | Change topic after the current line |
| `SendSceneEventAsync(string text, SceneEventReaction reaction, params ConvaiCharacter[] audience)` | Share a world event with selected members, or everyone for an empty audience |

All return `IConvaiOperation<ServerCommandResult>`. `SceneEventReaction` is `None` or `Volunteer`; the latter permits service-selected reaction rather than forcing a specific line. Invalid member arguments are refused instead of silently broadening the audience.

Inspect `Status`, `Reason`, and `WasSent`. Outcomes include `Succeeded`, `Failed`, `Unanswered`, `NotConnected`, and `Refused`; completion alone is not success. Common reasons include `no_session`, `conversation_not_started`, `command_timeout`, `session_closed`, `superseded`, and `payload_too_large`. Avoid logging `Extras`, which may contain private text.

Cancelling a command stops the caller's wait; it cannot retract a command already sent. After an unanswered result, inspect current state before repeating a command.

## Next steps

{% content-ref url="troubleshooting.md" %}
[Troubleshoot group conversation](troubleshooting.md)
{% endcontent-ref %}
{% content-ref url="simulator-and-debug-overlay.md" %}
[Simulator and debug overlay](simulator-and-debug-overlay.md)
{% endcontent-ref %}
