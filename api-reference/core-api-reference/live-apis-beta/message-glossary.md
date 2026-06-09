---
description: >-
  Complete glossary of all message types available in Convai's Live APIs for
  real-time communication between clients and the server.
---

# Message Glossary

## Overview

This glossary provides a comprehensive reference for all message types used in Convai's Live APIs. Messages flow bidirectionally between your client application and the Convai server over WebRTC data channels.

---

## Message Directions

| Direction           | Description                                                            |
| ------------------- | ---------------------------------------------------------------------- |
| **Client → Server** | Messages you send to trigger actions, update state, or control the bot |
| **Server → Client** | Messages you receive for events, state changes, and real-time data     |

---

## Message Format

### Client → Server Messages

Messages sent from the client to the server use this structure:

```json
{
  "type": "<message-type>",
  "data": { ... }
}
```

- `type` _(string, required)_: The message type identifier
- `data` _(object, optional)_: Message payload (structure varies by type)

### Server → Client Messages

Messages sent from the server to the client are wrapped in an RTVI envelope:

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "<message-type>",
    ...payload fields
  }
}
```

- `label` _(string)_: Always `"rtvi-ai"`
- `type` _(string)_: Always `"server-message"` for custom server messages
- `data` _(object)_: Contains the actual message with its own `type` and payload fields

{% hint style="info" %}
In the detailed message documentation pages, examples show only the inner `data` payload for clarity.
{% endhint %}

---

## Server Response Messages

For every client-to-server message, the server automatically sends a `server-response` message to acknowledge receipt and indicate the processing status. This is similar to HTTP response codes in REST APIs.

**Example Response:**

```json
{
  "type": "server-response",
  "event_type": "context-update",
  "status": "success",
  "message": "Context updated successfully (append mode)",
  "extras": {
    "token_count": 1523,
    "max_tokens": 50000,
    "remaining_tokens": 48477
  }
}
```

| Field        | Type   | Description                                                            |
| ------------ | ------ | ---------------------------------------------------------------------- |
| `event_type` | string | The original client message type that triggered this response          |
| `status`     | string | Processing status: `"success"`, `"error"`, `"processing"`, `"pending"` |
| `message`    | string | Human-readable description of the result (optional)                    |
| `extras`     | object | Additional event-specific data (optional)                              |

**Status Values:**

- `"success"` - Message processed successfully
- `"error"` - An error occurred (see `message` for details)
- `"processing"` - Message is being processed asynchronously
- `"pending"` - Message received but processing delayed

---

## Client → Server Messages

| Message Type                  | Purpose                                    | Details Page                                                                             |
| ----------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------- |
| `action_config`               | Configure actions at connection time       | See [Connect API](connect-api.md)                                                        |
| `trigger-message`             | Trigger narrative events or send context   | [client-to-server-messages.md](client-to-server-messages.md#trigger-message)             |
| `user_text_message`           | Send text input as user                    | [client-to-server-messages.md](client-to-server-messages.md#user_text_message)           |
| `update-template-keys`        | Update prompt template variables           | [client-to-server-messages.md](client-to-server-messages.md#update-template-keys)        |
| `update-scene-metadata`       | Update scene objects                       | [client-to-server-messages.md](client-to-server-messages.md#update-scene-metadata)       |
| `update-dynamic-info`         | Update dynamic context (basic)             | [client-to-server-messages.md](client-to-server-messages.md#update-dynamic-info)         |
| `context-update`              | Update runtime context (with mode control) | [client-to-server-messages.md](client-to-server-messages.md#context-update)              |
| `tts-toggle`                  | Enable/disable bot audio                   | [client-to-server-messages.md](client-to-server-messages.md#tts-toggle)                  |
| `stt-toggle`                  | Mute/unmute speech recognition             | [client-to-server-messages.md](client-to-server-messages.md#stt-toggle)                  |
| `interrupt-bot`               | Stop bot speech immediately                | [client-to-server-messages.md](client-to-server-messages.md#interrupt-bot)               |
| `force-user-stopped-speaking` | Signal end of user speech (push-to-talk)   | [client-to-server-messages.md](client-to-server-messages.md#force-user-stopped-speaking) |
| `reset-idle-timer`            | Reset idle timeout monitoring              | [client-to-server-messages.md](client-to-server-messages.md#reset-idle-timer)            |

---

## Server → Client Messages

| Message Type                    | Purpose                                     | Format                 | Details Page                                                                               |
| ------------------------------- | ------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------ |
| `server-response`               | Response for every client message           | Direct (legacy)        | [server-to-client-messages.md](server-to-client-messages.md#server-response)               |
| `interaction-created`           | Interaction ID created                      | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#interaction-created)           |
| `usage-limit-reached`           | Quota exceeded notification                 | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#usage-limit-reached)           |
| `bot-turn-completed`            | Bot finished speaking                       | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#bot-turn-completed)            |
| `bot-emotion`                   | Bot emotion for avatar                      | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#bot-emotion)                   |
| `behavior-tree-response`        | Behavior tree data                          | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#behavior-tree-response)        |
| `moderation-response`           | Content moderation result                   | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#moderation-response)           |
| `action-response`               | Actions/animations to trigger               | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#action-response)               |
| `final-user-transcription`      | User speech transcription                   | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#final-user-transcription)      |
| `visemes`                       | Lip-sync data                               | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#visemes)                       |
| `neurosync-blendshapes`         | Facial animation data                       | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#neurosync-blendshapes)         |
| `chunked-neurosync-blendshapes` | Batched facial animation                    | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#chunked-neurosync-blendshapes) |
| `blendshape-turn-stats`         | Turn statistics                             | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#blendshape-turn-stats)         |
| `user-idle-warning`             | Idle timeout warning                        | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#user-idle-warning)             |
| `llm-no-response`               | LLM chose not to respond                    | Server-message wrapped | [server-to-client-messages.md](server-to-client-messages.md#llm-no-response)               |
| `audio-data`                    | Audio chunks via data channel (custom mode) | Server-message wrapped | See [Audio Data via Data Channel](audio-data-via-data-channel.md)                          |

**Format Key:**

- **Server-message wrapped**: Uses the full RTVI envelope format with `"type": "server-message"` and event data nested in `data.type` and subsequent fields
- **Direct (legacy)**: Uses `data` as a flat object with the event type and fields at the top level

{% hint style="info" %}
All client messages receive a `server-response` acknowledgment with success/error status and additional data.
{% endhint %}

---

## Common Response Extras by Event Type

When you receive a `server-response` message, the `extras` field may contain event-specific data:

| Event Type          | Extras Fields                                              |
| ------------------- | ---------------------------------------------------------- |
| `context-update`    | `token_count`, `max_tokens`, `remaining_tokens`, `content` |
| `tts-toggle`        | `enabled`                                                  |
| `stt-toggle`        | `muted`                                                    |
| `trigger-message`   | `trigger_name`, `has_speak_tag`                            |
| `user_text_message` | `text`                                                     |

---

## Error Response Examples

### Invalid JSON

```json
{
  "type": "server-response",
  "event_type": "parse-error",
  "status": "error",
  "message": "Failed to parse message: invalid JSON or UTF-8 encoding"
}
```

### Missing Type Field

```json
{
  "type": "server-response",
  "event_type": "validation-error",
  "status": "error",
  "message": "Message missing required 'type' field"
}
```

### Unknown Message Type

```json
{
  "type": "server-response",
  "event_type": "unknown-message-type",
  "status": "error",
  "message": "Unknown message type: unknown-message-type",
  "extras": {
    "supported_types": ["trigger-message", "context-update", "tts-toggle", ...]
  }
}
```

---

## Message Categories

### Context & State Management

Messages for managing conversation context and bot state:

- `context-update` - Unified context updates with mode control
- `update-dynamic-info` - Basic dynamic context updates
- `update-template-keys` - Update prompt template variables
- `update-scene-metadata` - Update scene object descriptions

### Audio Control

Messages for controlling audio input and output:

- `tts-toggle` - Enable/disable text-to-speech output
- `stt-toggle` - Mute/unmute speech-to-text input
- `interrupt-bot` - Interrupt current bot speech
- `force-user-stopped-speaking` - Signal end of user speech

### Interaction & Events

Messages for triggering events and sending user input:

- `trigger-message` - Trigger narrative events or contextual actions
- `user_text_message` - Send text as user input

### Session Management

Messages for managing the session lifecycle:

- `reset-idle-timer` - Reset idle timeout

### Animation & Visual Feedback

Messages containing animation and visual data:

- `bot-emotion` - Emotion data for avatar expressions
- `visemes` - Lip-sync blendshape data
- `neurosync-blendshapes` - Facial animation blendshapes (single frame)
- `chunked-neurosync-blendshapes` - Batched facial animation blendshapes
- `action-response` - Actions and animations to perform

### Transcription & Text

Messages containing text and transcription data:

- `final-user-transcription` - Final transcription of user speech

### System Events

Messages about system state and events:

- `server-response` - Acknowledgment of client messages
- `interaction-created` - Session interaction ID created
- `bot-turn-completed` - Bot turn finished
- `usage-limit-reached` - Usage quota exceeded
- `user-idle-warning` - User idle timeout warning
- `llm-no-response` - LLM chose not to respond

### Voice Activity Detection

Messages from the VAD-based STT gating system:

- `vad-stt-started` - STT service started transcribing
- `vad-stt-stopped` - STT service stopped transcribing
- `vad-stt-debug` - VAD debug events (debug mode only)

---

## Related Documentation

- [Connect API](connect-api.md) - Establish a live session
- [Client to Server Messages](client-to-server-messages.md) - Detailed client message reference
- [Server to Client Messages](server-to-client-messages.md) - Detailed server message reference
- [Audio Data via Data Channel](audio-data-via-data-channel.md) - Custom audio handling
- [Metrics](metrics.md) - Performance metrics and monitoring

---
