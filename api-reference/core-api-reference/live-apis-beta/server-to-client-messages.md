---
title: Server-to-client messages
description: Complete reference for all messages Convai sends to the client over a WebRTC data channel in Live APIs, including fields, types, and recommended actions.
---

The Convai Live API server sends these messages over the WebRTC data channel during an active session. Each message type signals a distinct event — an acknowledgment, a bot state change, animation data, or a session limit. See the [Message Glossary](message-glossary.md) for a summary of all message types and their envelope formats.

{% hint style="info" %}
All server messages except `server-response` use the RTVI envelope format shown under [`interaction-created`](#interaction-created). Subsequent examples in this page show only the inner `data` payload for clarity.
{% endhint %}

## server-response

`server-response` is sent for every client-to-server message to acknowledge receipt and report the processing outcome. It uses the **direct (legacy) format** — not the RTVI envelope — so the fields appear at the top level of the JSON object, not nested under `data`.

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
| `type` | string | Always `"server-response"` |
| `event_type` | string | The client message type that triggered this response |
| `status` | string | Processing status: `"success"`, `"error"`, `"processing"`, or `"pending"` |
| `message` | string \| null | Human-readable description of the result |
| `extras` | object \| null | Additional event-specific data |

**Status values**

| Value | Meaning |
|---|---|
| `"success"` | Message processed successfully |
| `"error"` | An error occurred; see `message` for details |
| `"processing"` | Message is being processed asynchronously |
| `"pending"` | Message received but processing delayed |

**`extras` fields by event type**

| `event_type` | `extras` fields |
|---|---|
| `context-update` | `token_count`, `static_token_count`, `runtime_token_count`, `max_tokens`, `static_max_tokens`, `runtime_max_tokens`, `remaining_tokens`, `content` |
| `tts-toggle` | `enabled` |
| `stt-toggle` | `muted` |
| `trigger-message` | `trigger_name`, `has_speak_tag` |
| `user_text_message` | `text` |
| `kill-pipeline` | `room_name` |

**Error example**

```json
{
  "type": "server-response",
  "event_type": "tts-toggle",
  "status": "error",
  "message": "TTS bypass filter not available"
}
```

**Validation error — invalid JSON**

```json
{
  "type": "server-response",
  "event_type": "parse-error",
  "status": "error",
  "message": "Failed to parse message: invalid JSON or UTF-8 encoding"
}
```

**Validation error — missing type field**

```json
{
  "type": "server-response",
  "event_type": "validation-error",
  "status": "error",
  "message": "Message missing required 'type' field"
}
```

**Validation error — unknown message type**

```json
{
  "type": "server-response",
  "event_type": "unknown-message-type",
  "status": "error",
  "message": "Unknown message type: unknown-message-type",
  "extras": {
    "supported_types": ["trigger-message", "context-update", "tts-toggle"]
  }
}
```

**Recommended action:** Check the `status` field on every `server-response`. Handle `"error"` responses by reading `message` and updating your UI. Use the `extras` fields to reflect current state — for example, updating a mute indicator when `event_type` is `stt-toggle`.

---

## interaction-created

Sent early in the session lifecycle when an interaction ID is created. This is the first message that carries the full RTVI envelope.

**Full RTVI envelope**

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "interaction-created",
    "interaction_id": "int_abc123def456",
    "character_session_id": "cs_xyz789"
  }
}
```

**Inner `data` payload**

```json
{
  "type": "interaction-created",
  "interaction_id": "int_abc123def456",
  "character_session_id": "cs_xyz789"
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"interaction-created"` |
| `interaction_id` | string | Unique identifier for this interaction session |
| `character_session_id` | string | Character session identifier |

**Recommended action:** Store `interaction_id` for analytics, logging, or session tracking.

---

## usage-limit-reached

Sent when a usage quota is exceeded. Handle this message to display appropriate feedback and close the session.

```json
{
  "type": "usage-limit-reached",
  "quota_type": "minutes",
  "message": "You have exceeded your monthly quota"
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"usage-limit-reached"` |
| `quota_type` | string | Type of quota exceeded, for example `"minutes"` or `"api_calls"` |
| `message` | string | Human-readable message explaining the limit |

**Recommended action:** Display the `message` to the user and gracefully end the session.

---

## bot-turn-completed

Sent when the bot reaches a terminal turn state: it finished speaking, was interrupted by the user, or aborted because required output could not be delivered.

```json
{
  "type": "bot-turn-completed",
  "was_interrupted": false
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"bot-turn-completed"` |
| `was_interrupted` | boolean | `true` if the user interrupted the bot; `false` if the turn completed normally |
| `was_aborted` | boolean | Optional. `true` if the turn ended because required bot output could not be delivered |
| `error_reason` | string | Optional. Machine-readable abort reason; currently `"audio_delivery_failed"` |

`was_aborted` and `error_reason` are additive optional fields. Normal completions omit them.

**Recommended action:** Update UI state and re-enable user input controls when this message arrives.

---

## bot-emotion

Sent when the bot expresses an emotion. Use this to trigger avatar animations or update visual feedback elements.

```json
{
  "type": "bot-emotion",
  "emotion": "happy",
  "scale": 2
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"bot-emotion"` |
| `emotion` | string | Emotion name, for example `"happy"`, `"sad"`, `"excited"`, or `"angry"` |
| `scale` | integer | Intensity level: `1` = subtle, `2` = moderate, `3` = intense |

**Recommended action:** Trigger the corresponding avatar expression or animation for the received `emotion` and `scale`.

---

## behavior-tree-response

Sent with behavior tree data for character AI behavior.

```json
{
  "type": "behavior-tree-response",
  "bt_code": "...",
  "bt_constants": "...",
  "narrative_section_id": "section_1"
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"behavior-tree-response"` |
| `bt_code` | string | Behavior tree code |
| `bt_constants` | string | Constants for the behavior tree |
| `narrative_section_id` | string | Current narrative section identifier |

---

## moderation-response

Sent when content moderation has processed user input.

```json
{
  "type": "moderation-response",
  "result": false,
  "user_input": "the flagged content",
  "reason": "Inappropriate language"
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"moderation-response"` |
| `result` | boolean | `true` if content passed moderation; `false` if blocked |
| `user_input` | string | The input text that was moderated |
| `reason` | string \| null | Reason for blocking; `null` if content passed |

**Recommended action:** If `result` is `false`, optionally display feedback to the user indicating the input was blocked.

---

## action-response

Sent with an ordered list of actions or animations the bot wants to perform. Actions reference only the objects, characters, and action types declared in `action_config` at connect time. See the [Connect API](connect-api.md) for details on `action_config`.

```json
{
  "type": "action-response",
  "actions": [
    { "name": "Move To", "target": "cube" },
    { "name": "Wave" }
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"action-response"` |
| `actions` | object[] | Ordered array of actions to trigger |
| `actions[].name` | string | Action or animation identifier |
| `actions[].target` | string | Optional target object or character name |

**Recommended action:** Iterate over `actions` in order and trigger the corresponding animations or behaviors on your avatar or scene.

---

## final-user-transcription

Sent with the finalized transcription of what the user said in the current turn.

```json
{
  "type": "final-user-transcription",
  "text": "Hello, how are you today?",
  "speaker_id": "user_123",
  "speaker_name": "Alice",
  "participant_id": "participant_456"
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"final-user-transcription"` |
| `text` | string | The transcribed text |
| `speaker_id` | string \| null | Identifier for the speaker |
| `speaker_name` | string \| null | Display name of the speaker |
| `participant_id` | string \| null | Participant identifier |

**Recommended action:** Display `text` in a chat UI or append it to the conversation history.

---

## visemes

Sent frequently during bot speech with lip-sync data for avatar mouth animation. Values represent blend weights for each mouth shape.

```json
{
  "type": "visemes",
  "visemes": {
    "sil": 0.0,
    "pp": 0.8,
    "ff": 0.0,
    "th": 0.0,
    "dd": 0.0,
    "kk": 0.0,
    "ch": 0.0,
    "ss": 0.0,
    "nn": 0.0,
    "rr": 0.0,
    "aa": 0.2,
    "e": 0.0,
    "ih": 0.0,
    "oh": 0.0,
    "ou": 0.0
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"visemes"` |
| `visemes` | object | Map of viseme keys to blend weights (`0.0`–`1.0`) |

**Viseme keys**

| Key | Phonemes |
|---|---|
| `sil` | Silence |
| `pp` | P, B, M |
| `ff` | F, V |
| `th` | TH |
| `dd` | T, D |
| `kk` | K, G |
| `ch` | CH, J, SH |
| `ss` | S, Z |
| `nn` | N, L |
| `rr` | R |
| `aa` | A |
| `e` | E |
| `ih` | I |
| `oh` | O |
| `ou` | U, W |

**Recommended action:** Apply the viseme weights to avatar lip-sync blend shapes each time this message arrives.

---

## neurosync-blendshapes

Sent with a single frame of facial animation blendshape data (251 values per frame).

```json
{
  "type": "neurosync-blendshapes",
  "blendshapes": [0.0, 0.1, 0.05, 0.0]
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"neurosync-blendshapes"` |
| `blendshapes` | float[] | Array of 251 blendshape values, each in the range `0.0`–`1.0` |

**Recommended action:** Apply the blendshape values to the avatar facial rig for the current frame.

---

## chunked-neurosync-blendshapes

Sent with multiple frames of blendshape data batched into a single message. Use this message type instead of `neurosync-blendshapes` when the server sends batched data for efficiency.

```json
{
  "type": "chunked-neurosync-blendshapes",
  "blendshapes": [
    [0.0, 0.1, 0.05],
    [0.02, 0.12, 0.04],
    [0.01, 0.09, 0.06]
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"chunked-neurosync-blendshapes"` |
| `blendshapes` | float[][] | Array of blendshape frames; each frame contains 251 values in the range `0.0`–`1.0` |

**Recommended action:** Queue the frames and apply them sequentially to produce smooth facial animation.

---

## blendshape-turn-stats

Sent at the end of a bot turn with statistics about the blendshape generation for that turn. Use this for debugging or analytics.

```json
{
  "type": "blendshape-turn-stats",
  "stats": {
    "total_blendshapes": 150,
    "total_audio_bytes": 48000,
    "total_turn_duration_ms": 3000.0,
    "total_audio_duration_ms": 2800.0,
    "fps": 50.0,
    "was_interrupted": false
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"blendshape-turn-stats"` |
| `stats.total_blendshapes` | integer | Total blendshape frames generated in the turn |
| `stats.total_audio_bytes` | integer | Total audio data size in bytes |
| `stats.total_turn_duration_ms` | float | Total turn duration in milliseconds |
| `stats.total_audio_duration_ms` | float | Total audio duration in milliseconds |
| `stats.fps` | float | Blendshape frames per second |
| `stats.was_interrupted` | boolean | `true` if the turn was interrupted before completion |

---

## user-idle-warning

Sent when the user has been idle for a configured period, warning that disconnection is approaching.

```json
{
  "type": "user-idle-warning",
  "remaining_seconds": 300,
  "message": "You've been idle. You will be disconnected in 5 minutes."
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"user-idle-warning"` |
| `remaining_seconds` | integer | Seconds remaining before the session is disconnected |
| `message` | string \| null | Optional human-readable warning message |

**Recommended action:** Display the warning to the user and prompt for activity, or send a `reset-idle-timer` message to reset the idle timer.

---

## llm-no-response

Sent when the LLM explicitly decides not to respond to user input.

```json
{
  "type": "llm-no-response",
  "reason": "abstain"
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"llm-no-response"` |
| `reason` | string \| null | Reason for no response; `"abstain"` indicates the model chose not to speak |

**Recommended action:** Update your UI to indicate the bot chose not to respond, or handle the event silently depending on your UX requirements.

---

## audio-data

Sent when audio is routed through the data channel instead of (or in addition to) the standard WebRTC audio track. This message is only received when `audio_routing` is set to `"data_only"` or `"both"` in the `audio_config` of the `/connect` request.

```json
{
  "type": "audio-data",
  "sample_rate": 48000,
  "channels": 1,
  "audio": "AAEAAg==...",
  "includes_wav_header": false
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"audio-data"` |
| `sample_rate` | integer | Audio sample rate in Hz, for example `16000`, `24000`, or `48000` |
| `channels` | integer | Number of audio channels: `1` = mono, `2` = stereo |
| `audio` | string | Base64-encoded audio data (raw PCM or WAV with header) |
| `includes_wav_header` | boolean | `true` if the audio payload includes a 44-byte WAV header; `false` for raw PCM |

For complete decoding steps, playback implementation, and configuration options see [Audio Data via Data Channel](audio-data-via-data-channel.md).

---

## Related pages

{% content-ref url="message-glossary.md" %}
[Message Glossary](message-glossary.md)
{% endcontent-ref %}

{% content-ref url="connect-api.md" %}
[Connect API](connect-api.md)
{% endcontent-ref %}

{% content-ref url="audio-data-via-data-channel.md" %}
[Audio Data via Data Channel](audio-data-via-data-channel.md)
{% endcontent-ref %}
