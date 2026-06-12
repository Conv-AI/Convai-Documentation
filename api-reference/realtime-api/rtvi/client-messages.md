---
title: RTVI client messages
description: "Understand client messages in the Realtime API: the RTVI envelope format, server-response acknowledgments, and all 12 supported message types."
last_reviewed: "2026-06-11"
---

Client messages are JSON commands that your application sends to Convai during an active Realtime API session. Each message uses a two-field envelope with a `type` string that identifies the operation and an optional `data` object that carries the payload. Convai sends a `server-response` acknowledgment for every message it receives, whether the operation succeeded, failed, or is still processing. Both LiveKit and WebSocket transports support the full set of client messages without restriction.

## Message envelope

Every client message uses the same two-field format regardless of transport.

```json
{
  "type": "<message-type>",
  "data": { }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Message type identifier. See [Supported message types](#supported-message-types) for the full list. |
| `data` | object | No | Message-specific payload. Omit or send an empty object when the message type takes no data fields. |

The wire encoding of this envelope differs by transport. LiveKit wraps the message in an additional outer envelope and sends it on the `rtvi-ai` data channel. See [RTVI message protocol](../core-concepts/rtvi-protocol.md) for per-transport wire formats.

## Server-response acknowledgment

Convai sends a `server-response` message for every client message it receives. This response arrives as a flat JSON object — it is not wrapped in the outer RTVI envelope.

```json
{
  "type": "server-response",
  "event_type": "<original-client-type>",
  "status": "success",
  "message": null,
  "extras": { }
}
```

| Field | Description |
|---|---|
| `event_type` | The `type` value of the client message that triggered this response. For parse errors and missing-type errors — where no original type is available — this field holds the error category (`"parse-error"` or `"validation-error"`) instead. Handler-level errors preserve the original message type. |
| `status` | Processing outcome: `"success"`, `"error"`, `"processing"`, or `"pending"`. |
| `message` | Human-readable description of the result or error. `null` when not applicable. |
| `extras` | Event-specific data such as token counts, toggle state, or diagnostic fields. `null` when not applicable. |

## Supported message types

The Realtime API accepts 12 message types.

| Type | Description |
|---|---|
| `user_text_message` | Simulates typed user input, bypassing speech-to-text entirely. |
| `trigger-message` | Notifies the bot of a named event or narrative trigger. |
| `update-scene-metadata` | Updates descriptive scene context used for action grounding. |
| `update-template-keys` | Updates string variables used in bot prompt templates. |
| `context-update` | Appends, replaces, or resets the runtime dynamic context. |
| `tts-toggle` | Enables or disables text-to-speech audio output. |
| `stt-toggle` | Mutes or unmutes speech-to-text microphone input. |
| `kill-pipeline` | Terminates the active session pipeline. |
| `interrupt-bot` | Interrupts the bot's current speech turn. |
| `force-user-stopped-speaking` | Manually signals that the user has stopped speaking. |
| `reset-idle-timer` | Resets the idle-timeout counter for the session. |
| `update-dynamic-info` | Updates dynamic context text; superseded by `context-update` for new integrations. |

## Message type pages

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>user_text_message</strong><br>Send typed text as user input, bypassing speech-to-text.</td>
<td><a href="user-text-message.md">user-text-message.md</a></td>
</tr>
<tr>
<td><strong>trigger-message</strong><br>Fire named events and narrative triggers during a session.</td>
<td><a href="trigger-message.md">trigger-message.md</a></td>
</tr>
<tr>
<td><strong>Scene messages</strong><br>Update descriptive scene context and prompt template variables.</td>
<td><a href="scene-messages.md">scene-messages.md</a></td>
</tr>
<tr>
<td><strong>context-update</strong><br>Append, replace, or reset runtime dynamic context.</td>
<td><a href="context-update-message.md">context-update-message.md</a></td>
</tr>
<tr>
<td><strong>Control messages</strong><br>Toggle audio, interrupt the bot, and manage session lifecycle.</td>
<td><a href="control-messages.md">control-messages.md</a></td>
</tr>
<tr>
<td><strong>Client message errors</strong><br>Error responses for malformed, invalid, or unrecognized messages.</td>
<td><a href="client-message-errors.md">client-message-errors.md</a></td>
</tr>
</tbody>
</table>

{% content-ref url="../core-concepts/rtvi-protocol.md" %}
[RTVI message protocol](../core-concepts/rtvi-protocol.md)
{% endcontent-ref %}
