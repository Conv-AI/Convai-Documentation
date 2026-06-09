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

{% hint style="info" %}
`action_config` is the one exception: it is supplied in the `/connect` HTTP request body, not sent over the data channel at runtime. See [action\_config at /connect](#action_config-at-connect).
{% endhint %}

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

## action\_config at /connect

Action affordances are supplied at connect time in the `action_config` field of the `/connect` HTTP request body. This is the authoritative action contract for the session. It cannot be updated at runtime over the data channel.

```json
{
  "character_id": "00000000-0000-0000-0000-000000000000",
  "action_config": {
    "actions": ["Move To", "Pick Up", "Drop", "Follow"],
    "objects": [
      { "name": "cube", "description": "A red cube on the table" },
      { "name": "lever", "description": "A metal lever on the wall" }
    ],
    "characters": [
      { "name": "Player", "bio": "The current user" },
      { "name": "Guard", "bio": "A nearby guard" }
    ],
    "current_attention_object": "cube"
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `actions` | string[] | No | Action names the bot may use. |
| `objects` | object[] | No | Objects the bot may reference. Each entry has `name` and `description`. |
| `characters` | object[] | No | Characters the bot may reference. Each entry has `name` and `bio`. |
| `current_attention_object` | string | No | Initial attention object. Must match one of the `objects[].name` values. |

**Notes:**

- `actions`, `objects`, and `characters` define the complete set of action affordances for the session.
- `scene_description` (a separate `/connect` field) provides descriptive context only. It does not authorize actions or targets.
- `current_attention_object` must exactly match one of the `objects[].name` values.

See [Connect API](connect-api.md) for the full `/connect` request reference.

---

## trigger-message

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

## user\_text\_message

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

## update-template-keys

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

## update-scene-metadata

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

## update-dynamic-info

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

## context-update

Updates the bot's runtime dynamic context with full control over mode, token budget, and LLM triggering. This is the preferred message for runtime context management.

```json
{
  "type": "context-update",
  "data": {
    "text": "New context information",
    "mode": "append",
    "run_llm": "auto",
    "current_attention_object": "torch",
    "remove_static": false
  }
}
```

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | Yes, unless `mode` is `"reset"` | — | The context text to apply. |
| `mode` | string | No | `"append"` | How to apply the context. See [Mode values](#mode-values). |
| `run_llm` | string | No | `"auto"` | Whether to trigger an LLM response after the update. See [run\_llm values](#run_llm-values). |
| `current_attention_object` | string or object | No | — | Updates the active attention object for action-reference grounding. |
| `remove_static` | boolean | No | `false` | For `"reset"` mode only: when `true`, also clears the static context. |

### Mode values

| Value | Behavior |
|---|---|
| `"append"` | Adds `text` to existing runtime dynamic context. |
| `"replace"` | Replaces existing runtime dynamic context with `text`. |
| `"reset"` | Clears runtime dynamic context. Also clears static context if `remove_static` is `true`. `text` is not required. |

### run\_llm values

| Value | Behavior |
|---|---|
| `"true"` | Always trigger a bot response after the update. |
| `"false"` | Never trigger a bot response. |
| `"auto"` | Convai decides whether to trigger a response based on context. |

### Token budget

Dynamic context uses an estimated token budget:

| Partition | Budget |
|---|---|
| `static_text` (session-level context supplied at connect time) | 20,000 estimated tokens |
| Runtime `text` (from `append` and `replace` updates) | 30,000 estimated tokens |
| Combined dynamic context | 50,000 estimated tokens |

When runtime `text` exceeds its 30,000-token budget, Convai trims the oldest runtime context updates and retains the newest updates that fit within the budget.

`static_text` is session and environment context supplied for this connection. It is preserved across `reset` calls unless `remove_static` is `true`.

### Attention update rules

- `current_attention_object` is validated against the connected session's `action_config.objects`.
- Send either the object name string or the full object payload.
- Send an empty string (`""`) to clear the current attention object.
- Updating `current_attention_object` regenerates the system prompt, even when `run_llm` is `"false"`.

### Success response

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

### Error response

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

## tts-toggle

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

## stt-toggle

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

## interrupt-bot

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

## force-user-stopped-speaking

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

## reset-idle-timer

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
