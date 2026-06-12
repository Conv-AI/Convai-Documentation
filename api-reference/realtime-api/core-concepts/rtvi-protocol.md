---
title: RTVI message protocol
description: "Understand the RTVI message protocol: envelope structure for each transport, the direction model, and server-response status values."
last_reviewed: "2026-06-11"
---

RTVI (Real-Time Voice Interface) is the message protocol that client applications use to send commands to Convai and receive events in return during an active session. Every message has a defined type, a direction, and an envelope format that varies slightly by transport.

## Message direction

RTVI messages flow in two directions. Each direction uses a different envelope structure.

| Direction | Who sends | Purpose |
|---|---|---|
| Client → Server | Your application | Trigger actions, update context, control audio, or end the session. |
| Server → Client | Convai | Deliver transcriptions, emotions, animations, status events, and acknowledgments. |

The server sends a `server-response` acknowledgment for every client message it receives. This acknowledgment confirms whether the message was processed, is being processed asynchronously, or failed.

## Client-to-server format

Client messages use a consistent two-field envelope regardless of transport.

```json
{
  "type": "<message-type>",
  "data": { }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Message type identifier, for example `"trigger-message"` or `"tts-toggle"`. |
| `data` | object | No | Message-specific payload. Omit or send an empty object when the message type takes no payload. |

The wire encoding of this envelope differs by transport. See [Transport wire formats](#transport-wire-formats) below.

## Server-to-client format

Most server messages arrive inside an outer RTVI envelope that identifies the label and message class.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "<message-type>",
    "<payload-field>": "<value>"
  }
}
```

| Field | Value | Description |
|---|---|---|
| `label` | `"rtvi-ai"` | Always this value. Identifies messages as belonging to the Convai RTVI layer. |
| `type` | `"server-message"` | Always this value for Convai custom messages. |
| `data.type` | varies | The actual message type, for example `"bot-turn-completed"` or `"bot-emotion"`. |
| `data.*` | varies | Payload fields specific to the message type. |

The `server-response` message is an exception. It is sent as a flat object without the outer `label`/`type` wrapper — see [Server response acknowledgment](#server-response-acknowledgment) below.

## Server response acknowledgment

Convai sends a `server-response` message for every client message it receives. The response confirms whether the message was accepted, failed, or is queued for asynchronous processing.

```json
{
  "type": "server-response",
  "event_type": "<original-client-type>",
  "status": "success",
  "message": "<optional human-readable description>",
  "extras": { }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"server-response"`. |
| `event_type` | string | The `type` value of the client message that triggered this response. |
| `status` | string | Processing outcome. See status values below. |
| `message` | string \| null | Optional human-readable description of the result or error. |
| `extras` | object \| null | Optional event-specific data, such as token counts or toggle state. |

**Status values:**

| Value | Meaning |
|---|---|
| `"success"` | Message was processed successfully. |
| `"error"` | Processing failed. Check `message` for the reason. |
| `"processing"` | Message was accepted and is being processed asynchronously. |
| `"pending"` | Message was received but processing has been delayed. |

## Transport wire formats

The client-to-server envelope encoding differs by transport. The server normalizes all formats to the same internal representation before routing.

| Transport | Wire format | Notes |
|---|---|---|
| LiveKit | `{"label": "rtvi-ai", "type": "<msg-type>", "data": {...}}` | Send on the `rtvi-ai` data channel. The `label` field is required. |
| WebSocket (`/chat`) — direct | `{"type": "<msg-type>", "data": {...}}` | Standard format. Send as a JSON text frame. |
| WebSocket (`/chat`) — wrapped | `{"type": "client-message", "data": {"t": "<msg-type>", "d": {...}}}` | Alternative format. The server automatically unwraps this to the direct format. |
| Daily | Same as LiveKit | Send on the `rtvi-ai` data channel with the `label` field present. |

## Related concepts

{% content-ref url="session-lifecycle.md" %}
[Session lifecycle](session-lifecycle.md)
{% endcontent-ref %}

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}
