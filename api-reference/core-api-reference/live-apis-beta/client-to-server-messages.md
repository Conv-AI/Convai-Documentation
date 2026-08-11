---
title: Client-to-server messages
description: Reference for all messages a client sends to Convai's Live API server over the WebRTC data channel, including payloads, fields, and response details.
---

All client-to-server messages are sent as JSON over the WebRTC data channel established after a successful `/connect` call. For message format conventions, status codes returned by the server, and a full index of all message types in both directions, see the [Message Glossary](message-glossary.md).

## Message envelope

Every client-to-server message uses this envelope:

```json
{
  "type": "<message-type>",
  "data": { ... }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | The message type identifier. |
| `data` | object | No | Message payload. Structure varies by message type. Omit for messages with no payload. |

The server acknowledges every client message with a `server-response` message. See [Server response](#server-response) below.

## Server response

The server sends a `server-response` message for every client-to-server message it receives, regardless of type.

```json
{
  "type": "server-response",
  "event_type": "tts-toggle",
  "status": "success",
  "message": "TTS enabled",
  "extras": {
    "enabled": true
  }
}
```

| Field | Type | Description |
|---|---|---|
| `event_type` | string | The client message type that triggered this response. |
| `status` | string | Processing status: `"success"`, `"error"`, `"processing"`, or `"pending"`. |
| `message` | string or null | Human-readable description of the result. |
| `extras` | object or null | Additional event-specific data. Structure varies by event type. |

**Status values:**

| Value | Meaning |
|---|---|
| `"success"` | Message processed successfully. |
| `"error"` | An error occurred. Check `message` for details. |
| `"processing"` | Message is being processed asynchronously. |
| `"pending"` | Message received but processing is delayed. |

---

## Interaction & events

### trigger-message

Triggers a narrative event, sends contextual information to the bot, or initiates specific bot behaviors.

```json
{
  "type": "trigger-message",
  "data": {
    "trigger_name": "greeting",
    "trigger_message": "User entered the room"
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `trigger_name` | string | No | Name or identifier of the trigger. |
| `trigger_message` | string | No | Context or message content for the trigger. |

**Use cases:**

- Notify the bot of in-scene events, such as a player entering an area or completing a quest.
- Send contextual triggers to drive narrative flow.
- Initiate specific bot behaviors tied to named triggers.

**Server response extras:**

| Field | Type | Description |
|---|---|---|
| `trigger_name` | string | The trigger name echoed from the request. |
| `has_speak_tag` | boolean | Whether the trigger message contained a speak tag. |

---

### user\_text\_message

Sends text as user input, simulating speech without audio.

```json
{
  "type": "user_text_message",
  "data": {
    "text": "Hello, how are you?"
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | string | Yes | The text to send as user input. |

**Server response extras:**

| Field | Type | Description |
|---|---|---|
| `text` | string | The text echoed from the request. |

---

## Context & state

### update-template-keys

Updates template variables used in the bot's system prompt.

```json
{
  "type": "update-template-keys",
  "data": {
    "template_keys": {
      "player_name": "Alice",
      "current_level": "5",
      "location": "Forest"
    }
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `template_keys` | object | Yes | Key-value pairs of template variable names and their updated string values. |

**Use cases:**

- Update dynamic prompt variables such as player name, stats, or game state.
- Customize bot responses based on the current session state.

---

### update-scene-metadata

Updates the descriptive scene context the bot knows about, including in-scene objects and their descriptions.

```json
{
  "type": "update-scene-metadata",
  "data": {
    "scene_metadata": [
      { "name": "torch", "description": "A flaming torch on the wall" },
      { "name": "door", "description": "A locked wooden door" },
      { "name": "chest", "description": "An old treasure chest" }
    ]
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `data.scene_metadata` | object[] | Yes | Array of scene objects to describe. |
| `data.scene_metadata[].name` | string | Yes | Object identifier. |
| `data.scene_metadata[].description` | string | Yes | Human-readable description of the object. |

**Use cases:**

- Update interactable objects in the scene as the environment changes.
- Adjust environment context for the bot without modifying action affordances.

{% hint style="warning" %}
`update-scene-metadata` updates descriptive context only. It does not modify the authoritative `action_config.objects` list supplied at `/connect` time. To change which objects the bot may act on, reconnect with a new `action_config`.
{% endhint %}

---

### update-dynamic-info

Updates dynamic information injected into the bot's system prompt. Use this for basic single-field context updates. For mode-controlled updates with token budget tracking, use [`context-update`](#context-update) instead.

```json
{
  "type": "update-dynamic-info",
  "data": {
    "dynamic_info": {
      "text": "The user just completed the dragon quest and received a golden sword."
    }
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `dynamic_info.text` | string | Yes | Dynamic context text to inject into the system prompt. |

---

### context-update

Updates the bot's runtime dynamic context with full control over mode, token budget, and LLM triggering. This is the preferred message for runtime context management.

```json
{
  "type": "context-update",
  "data": {
    "text": "New context information",
    "mode": "append",
    "run_llm": "auto",
    "current_attention_object": "torch",
    "action_config": {
      "objects": [
        { "name": "torch", "description": "A flaming torch on the wall" }
      ]
    },
    "remove_static": false
  }
}
```

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | Yes, unless `mode` is `"reset"` | — | The context text to apply. |
| `mode` | string | No | `"append"` | How to apply the context. |
| `run_llm` | string | No | `"auto"` | Whether to trigger an LLM response after the update. |
| `current_attention_object` | string or object | No | — | Updates the active attention object for action-reference grounding. |
| `action_config` | object | No | — | Replaces the provided action affordance lists for the active session. See below. |
| `remove_static` | boolean | No | `false` | For `"reset"` mode only: when `true`, also clears the static context. |

**Updating action affordances mid-session**

`action_config` accepts the same structure as the [Connect API](connect-api.md#request-body). Only the lists you provide are replaced — sending just `objects` leaves `actions` and `characters` untouched. Use this when the scene changes and the character's affordances change with it.

{% hint style="warning" %}
Adding an object to `scene_description` or to `text` does **not** make it targetable. Only `action_config` grants affordances. See [Response contract and parsing](response-contract-and-parsing.md#how-actions-are-separated).
{% endhint %}

**Mode values**

| Value | Behavior |
|---|---|
| `"append"` | Adds `text` to existing runtime dynamic context. |
| `"replace"` | Replaces existing runtime dynamic context with `text`. |
| `"reset"` | Clears runtime dynamic context. Also clears static context if `remove_static` is `true`. `text` is not required. |

**run\_llm values**

| Value | Behavior |
|---|---|
| `"true"` | Always trigger a bot response after the update. |
| `"false"` | Never trigger a bot response. |
| `"auto"` | Convai decides whether to trigger a response based on context. |

**Token budget**

Dynamic context uses an estimated token budget:

| Partition | Budget |
|---|---|
| `static_text` (session-level context supplied at connect time) | 20,000 estimated tokens |
| Runtime `text` (from `append` and `replace` updates) | 30,000 estimated tokens |
| Combined dynamic context | 50,000 estimated tokens |

When runtime `text` exceeds its 30,000-token budget, Convai trims the oldest runtime context updates and retains the newest updates that fit within the budget.

`static_text` is session and environment context supplied for this connection. It is preserved across `reset` calls unless `remove_static` is `true`.

**Attention update rules**

- `current_attention_object` is validated against the connected session's `action_config.objects`.
- Send either the object name string or the full object payload.
- Send an empty string (`""`) to clear the current attention object.
- Updating `current_attention_object` regenerates the system prompt, even when `run_llm` is `"false"`.

**Success response**

On success, the server returns a `server-response` with the following `extras`:

```json
{
  "type": "server-response",
  "event_type": "context-update",
  "status": "success",
  "message": "Context updated successfully (append mode)",
  "extras": {
    "token_count": 1523,
    "static_token_count": 200,
    "runtime_token_count": 1323,
    "max_tokens": 50000,
    "static_max_tokens": 20000,
    "runtime_max_tokens": 30000,
    "remaining_tokens": 48477,
    "content": "full context text here..."
  }
}
```

| Field | Type | Description |
|---|---|---|
| `token_count` | integer | Current total estimated tokens in dynamic context. |
| `static_token_count` | integer | Estimated tokens from static dynamic context. |
| `runtime_token_count` | integer | Estimated tokens from runtime dynamic context. |
| `max_tokens` | integer | Combined dynamic context budget (50,000 estimated tokens). |
| `static_max_tokens` | integer | Static dynamic context budget (20,000 estimated tokens). |
| `runtime_max_tokens` | integer | Runtime dynamic context budget (30,000 estimated tokens). |
| `remaining_tokens` | integer | Estimated tokens remaining before the combined limit is reached. |
| `content` | string | Full retained runtime dynamic context text. |

Legacy `word_count`, `static_word_count`, `runtime_word_count`, `max_words`, and `remaining_words` fields may appear for older clients. The token fields are authoritative.

**Error response**

When a token limit is exceeded, the server returns a `server-response` with `"status": "error"`:

```json
{
  "type": "server-response",
  "event_type": "context-update",
  "status": "error",
  "message": "Failed to process context-update: 1 validation error for DynamicInfo\nValue error, Dynamic info static_text token limit exceeded. static_text: 20001 estimated tokens, Maximum: 20000 tokens."
}
```

- Validation checks apply to the static, runtime, and combined estimated-token limits independently.
- When combined dynamic context exceeds 40,000 estimated tokens, Convai logs a server-side warning.
- Error messages include the estimated-token breakdown for both partitions.

---

## Vision

Vision messages query or consume the session's vision ring buffer. Frames enter that buffer from the WebRTC video track (LiveKit) once `vision_input_config` is set on [`/connect`](connect-api.md). These RTVI control messages do not publish image bytes themselves.

### vision-status

Queries the current vision buffer state without attaching frames or triggering the LLM. Use this after enabling vision, after camera-off, or whenever you need confirmation that frames are available before calling `vision-trigger`.

```json
{
  "type": "vision-status",
  "data": {
    "update_id": "vision-status-1"
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `update_id` | string | No | Client correlation id. Echoed in the ack and used for duplicate replay. If omitted, a top-level message `id` is used when present. |

**Success response**

```json
{
  "type": "server-response",
  "event_type": "vision-status",
  "status": "success",
  "message": "Vision status",
  "extras": {
    "vision_status_outcome": "frames_available",
    "active_source": "participant-id",
    "active_source_label": "webcam",
    "last_frame_age_ms": 120,
    "update_id": "vision-status-1",
    "duplicate": false,
    "vision_buffer": {
      "enabled": true,
      "status": "frames_available",
      "retained_frames": 3,
      "buffer_frames": 8,
      "frames_per_turn": 5,
      "first_frame_pts": 1001,
      "last_frame_pts": 1003,
      "last_frame_age_ms": 120,
      "first_frame_index": -3,
      "source_active": true,
      "source_label": "webcam",
      "selected_participant": "participant-id",
      "sampling_windows": [
        { "count": 3, "interval_ms": 300 },
        { "count": 2, "interval_ms": 1500 }
      ]
    }
  }
}
```

| Field | Type | Description |
|---|---|---|
| `vision_status_outcome` | string | High-level buffer outcome. |
| `active_source` | string \| null | Selected participant id, when a source is active. |
| `active_source_label` | string \| null | Human-readable source label, when known. |
| `last_frame_age_ms` | integer \| null | Age of the newest retained frame in milliseconds. |
| `vision_buffer` | object | Client-safe ring-buffer snapshot. Never includes image bytes. |
| `update_id` | string | Echoed when supplied on the request. |
| `duplicate` | boolean | `true` when this ack is a replay of a previous `update_id`. |

**`vision_status_outcome` / `vision_buffer.status` values**

| Value | Meaning |
|---|---|
| `frames_available` | Source is active and the buffer has retained frames. |
| `buffer_empty` | Source is active, but no frames are retained yet. |
| `no_active_video` | No active visual source is selected. |
| `vision_not_enabled` | Vision is not enabled for this session. |

**Use cases:**

- Confirm frames landed after the user enabled camera or screen share.
- Inspect buffer depth / sampling windows before issuing a `vision-trigger`.
- Detect camera-off / stale feed without attaching frames.

---

### vision-trigger

Attaches buffered vision frames into LLM context and optionally triggers a bot turn. Frames are never auto-attached by this message alone when vision is disabled or the buffer is empty with no text.

```json
{
  "type": "vision-trigger",
  "data": {
    "respond_mode": "auto",
    "text": "What changed on screen?",
    "frame_indices": [-1, -1],
    "update_id": "vision-trigger-1"
  }
}
```

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `respond_mode` | string | No | Session default for `vision` | `"silent"`, `"auto"`, or `"must_respond"`. Invalid explicit values return an error ack. |
| `text` | string | No | Default vision prompt when LLM runs | Optional instruction attached with the frames. When present, text-only triggers can still proceed even if the buffer is empty. |
| `frame_indices` | integer[] | No | Default dual-horizon selection | Relative indices into the retained buffer. `-1` is the newest frame. Duplicate indices collapse to one frame. |
| `frame_ids` | integer[] | No | — | Absolute frame presentation timestamps (`attached_frame_pts` / `vision-status` pts values). Takes precedence over `frame_indices` when both are set. |
| `update_id` | string | No | — | Client correlation id. Echoed in the ack and used for duplicate replay. If omitted, a top-level message `id` is used when present. |

**`respond_mode` values**

| Value | Behavior |
|---|---|
| `"silent"` | Attach frames only. Does not invoke the LLM. |
| `"auto"` | Attach frames and invoke the LLM only when the bot is idle and the user is not speaking. Otherwise the request is downgraded silently without attaching. |
| `"must_respond"` | Attach frames and invoke the LLM. If the bot is busy, Convai interrupts first. If the user is speaking, attach/reserve frames and respond after the user turn. |

Connect-time `respond_modes.vision` seeds the default when `respond_mode` is omitted.

**Success response**

```json
{
  "type": "server-response",
  "event_type": "vision-trigger",
  "status": "success",
  "message": "Vision trigger invoked LLM",
  "extras": {
    "requested_respond_mode": "auto",
    "actual_respond_mode": "auto",
    "requested_run_llm": "auto",
    "actual_run_llm": "auto",
    "llm_triggered": true,
    "downgraded": false,
    "downgrade_reason": null,
    "interrupted": false,
    "vision_trigger_outcome": "attached",
    "vision_attach_outcome": "attached",
    "vision_frames_attached": 1,
    "vision_image_tokens_est": 258,
    "attached_frame_pts": [42],
    "frame_binding": "frame_indices",
    "requested_frame_indices": [-1, -1],
    "active_source": "participant-id",
    "active_source_label": "webcam",
    "last_frame_age_ms": 80,
    "update_id": "vision-trigger-1",
    "duplicate": false,
    "vision_buffer": {
      "enabled": true,
      "status": "frames_available",
      "retained_frames": 1
    }
  }
}
```

| Field | Type | Description |
|---|---|---|
| `requested_respond_mode` | string | Resolved request mode, or `"invalid"`. |
| `actual_respond_mode` | string | Mode actually applied after idle/busy gates. |
| `requested_run_llm` / `actual_run_llm` | string | `"true"`, `"false"`, or `"auto"`. |
| `llm_triggered` | boolean | Whether an LLM turn was started. |
| `downgraded` | boolean | Whether the request was reduced (busy bot, empty buffer, etc.). |
| `downgrade_reason` | string \| null | Why the request was downgraded, when applicable. |
| `interrupted` | boolean | `true` when `must_respond` interrupted an in-progress bot turn. |
| `vision_trigger_outcome` | string | Final outcome for the trigger. |
| `vision_attach_outcome` | string | Attach result when frames were selected. |
| `vision_frames_attached` | integer | Number of frames attached. |
| `vision_image_tokens_est` | integer | Estimated image tokens for the attach. |
| `attached_frame_pts` | integer[] | PTS values of attached frames. |
| `frame_binding` | string | How frames were chosen (`default`, `frame_indices`, `frame_ids`). |
| `requested_frame_indices` / `requested_frame_ids` | array \| null | Echo of the request selection fields. |
| `vision_buffer` | object | Buffer snapshot after handling the trigger. |

**Common `vision_trigger_outcome` values**

| Value | Meaning |
|---|---|
| `attached` | Frames were attached. |
| `deduped_stub` | Frames matched the previous attach and were stubbed. |
| `stale_skipped` | Buffer was considered stale and no text was supplied. |
| `frames_available` | Buffer has frames, but the trigger did not attach (for example `auto` while bot is busy). |
| `buffer_empty` | Source active, no retained frames, and no text. |
| `no_active_video` | No active visual source, and no text. |
| `vision_not_enabled` | Vision is not enabled for the session. |
| `invalid_respond_mode` | Explicit `respond_mode` was not one of the allowed values. |
| `frame_id_evicted` / `invalid_frame_ids` / `invalid_frame_indices` / `invalid_frame_indices_range` / `rate_limited` | Frame binding failed. |

{% hint style="info" %}
`update_id` makes retries safe: a repeated `vision-status` or `vision-trigger` with the same id replays the prior ack with `"duplicate": true` and does not attach or trigger again.
{% endhint %}

**Use cases:**

- Ask the character to comment on the current camera or screen feed.
- Silently prime vision context (`respond_mode: "silent"`) ahead of a later user turn.
- Re-attach specific recent frames via `frame_indices` or `frame_ids`.

---

## Audio control

### tts-toggle

Enables or disables the bot's text-to-speech audio output.

```json
{
  "type": "tts-toggle",
  "data": {
    "enabled": true
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `enabled` | boolean | Yes | `true` to enable TTS output. `false` to disable it. |

**Server response extras:**

| Field | Type | Description |
|---|---|---|
| `enabled` | boolean | The enabled state echoed from the request. |

**Use cases:**

- Mute bot audio during cutscenes or narrated sequences.
- Toggle audio output for accessibility requirements.

---

### stt-toggle

Mutes or unmutes speech-to-text microphone input processing.

```json
{
  "type": "stt-toggle",
  "data": {
    "muted": true
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `muted` | boolean | Yes | `true` to stop listening. `false` to resume listening. |

**Server response extras:**

| Field | Type | Description |
|---|---|---|
| `muted` | boolean | The muted state echoed from the request. |

**Use cases:**

- Implement push-to-talk input by muting STT when the button is not held.
- Disable voice input during moments where user speech should not be processed.

---

### interrupt-bot

Immediately stops the bot's current speech.

```json
{
  "type": "interrupt-bot"
}
```

No `data` payload is required.

**Use cases:**

- Allow a user to interrupt the bot mid-speech.
- Stop bot audio immediately when an in-scene event requires silence.

---

### force-user-stopped-speaking

Signals to the server that the user has finished speaking. Use this in push-to-talk implementations to end the speech segment explicitly.

```json
{
  "type": "force-user-stopped-speaking"
}
```

No `data` payload is required.

**Use cases:**

- Signal end-of-speech when the push-to-talk button is released.
- Provide a manual end-of-speech signal when VAD is not used.

---

## Session management

### reset-idle-timer

Resets the user idle timeout countdown. Send this to signal user activity and prevent idle disconnection.

```json
{
  "type": "reset-idle-timer",
  "data": {}
}
```

No `data` payload is required. The server ignores any `data` content.

**Use cases:**

- Reset the timer when the user performs a UI action such as a click or keypress.
- Detect user activity outside of voice interaction (for example, mouse movement) and prevent idle timeout.
- Keep a session alive during extended non-voice interactions.

---

### usage-toggle

Enables or disables streaming of informational `usage-update` messages to this client.

```json
{
  "type": "usage-toggle",
  "data": {
    "enabled": true
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `enabled` | boolean | Yes | `true` resumes `usage-update` streaming, `false` stops it. |

{% hint style="info" %}
This only controls whether the server **pushes** usage messages to your client. It never affects server-side usage tracking, aggregation, or billing, which continue unconditionally. `usage-update` messages are only available when the session is running in debug mode with usage tracking enabled.
{% endhint %}

**Use cases:**

- Stop the real-time cost stream when a debug usage panel is hidden.
- Reduce data-channel traffic for clients that do not render live usage.

---

### kill-pipeline

Terminates the session and closes the connection.

```json
{
  "type": "kill-pipeline"
}
```

No `data` payload is required.

**Use cases:**

- Cleanly end a session when the user exits the experience.
- Release resources without waiting for an idle timeout.

---

## Next steps

{% content-ref url="message-glossary.md" %}
[Message Glossary](message-glossary.md)
{% endcontent-ref %}

{% content-ref url="connect-api.md" %}
[Connect API](connect-api.md)
{% endcontent-ref %}

{% content-ref url="audio-data-via-data-channel.md" %}
[Audio Data (via data channel)](audio-data-via-data-channel.md)
{% endcontent-ref %}
