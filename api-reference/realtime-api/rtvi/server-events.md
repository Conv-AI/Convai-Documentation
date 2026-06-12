---
title: RTVI server events
description: Direction model, RTVI server-message envelope, transport routing rules, conditional events, and a complete reference index of every server-to-client event type.
last_reviewed: "2026-06-11"
---

The Realtime API sends events to your client during an active session. Every event arrives inside a standard RTVI envelope and carries a `type` field that identifies the event category.

## Event envelope

Most server events use the RTVI server-message envelope.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "<event-type>",
    "<payload-field>": "<value>"
  }
}
```

| Field | Value | Description |
|---|---|---|
| `label` | `"rtvi-ai"` | Always this value. Identifies the message as a Convai RTVI event. |
| `type` | `"server-message"` | Always this value for Convai custom events. |
| `data.type` | varies | The specific event type, for example `"bot-turn-completed"`. |
| `data.*` | varies | Payload fields specific to the event. |

**Exception — `server-response`:** The acknowledgment Convai sends for every client message is not wrapped in the outer envelope. It is sent as a flat JSON object. See [RTVI message protocol](../core-concepts/rtvi-protocol.md) for the full `server-response` shape.

## Transport routing

Most server events are delivered on all transports unless stated otherwise.

| Transport | Delivery mechanism |
|---|---|
| LiveKit | Data channel (`rtvi-ai` label) |
| WebSocket (`/chat`) | JSON text frame |

The `audio-data` event is an exception: it is only sent when you configure `audio_routing: "data_only"` or `audio_routing: "both"` in `audio_config` on `/connect`, and it is only supported on the LiveKit transport.

## Conditional events

Some events only fire under specific conditions.

| Event | Condition |
|---|---|
| `vad-stt-started` | Only sent when the VAD STT gating processor is active. |
| `vad-stt-stopped` | Only sent when the VAD STT gating processor is active. |
| `audio-data` | Only sent when `audio_routing` is `"data_only"` or `"both"` in `/connect`. |

## Event categories

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Session events</strong><br>Interaction lifecycle, usage limits, and idle-timeout warnings.</td>
<td><a href="session-events.md">session-events.md</a></td>
</tr>
<tr>
<td><strong>Turn events</strong><br>Bot speaking state, turn completion, and LLM no-response signals.</td>
<td><a href="turn-events.md">turn-events.md</a></td>
</tr>
<tr>
<td><strong>Transcription events</strong><br>Final user transcription and VAD-based STT gate open/close events.</td>
<td><a href="transcription-events.md">transcription-events.md</a></td>
</tr>
<tr>
<td><strong>Animation events</strong><br>Viseme lip-sync data and NeuroSync facial blendshape frames.</td>
<td><a href="animation-events.md">animation-events.md</a></td>
</tr>
<tr>
<td><strong>AI behavior events</strong><br>Behavior tree responses, content moderation results, and bot emotion.</td>
<td><a href="ai-behavior-events.md">ai-behavior-events.md</a></td>
</tr>
<tr>
<td><strong>Audio data event</strong><br>Raw audio chunks delivered via the data channel instead of the audio track.</td>
<td><a href="audio-data-event.md">audio-data-event.md</a></td>
</tr>
</tbody>
</table>

## All server events — quick reference

| Event type | Category | Description |
|---|---|---|
| `interaction-created` | Session | Interaction ID created for this session. |
| `usage-limit-reached` | Session | A usage quota has been exceeded. |
| `user-idle-warning` | Session | User has been idle; disconnection is approaching. |
| `bot-started-speaking` | Turn | Bot began speaking. |
| `bot-stopped-speaking` | Turn | Bot audio stream ended. |
| `bot-turn-completed` | Turn | Bot turn fully resolved (completed, interrupted, or aborted). |
| `llm-no-response` | Turn | LLM chose not to generate a response. |
| `final-user-transcription` | Transcription | Final text of what the user said. |
| `vad-stt-started` | Transcription | STT gate opened; transcription is active. |
| `vad-stt-stopped` | Transcription | STT gate closed; transcription has stopped. |
| `visemes` | Animation | Per-phoneme lip-sync blend weights. |
| `neurosync-blendshapes` | Animation | Full 251-value facial blendshape frame. |
| `chunked-neurosync-blendshapes` | Animation | Batched list of blendshape frames. |
| `behavior-tree-response` | AI behavior | Behavior tree data for character AI. |
| `moderation-response` | AI behavior | Content moderation result for user input. |
| `bot-emotion` | AI behavior | Bot's current emotional state with intensity. |
| `audio-data` | Audio | Raw audio chunk via data channel (conditional). |
