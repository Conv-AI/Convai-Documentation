---
title: Transcription events
description: Reference for final-user-transcription, vad-stt-started, and vad-stt-stopped — payload fields, VAD gate behavior, and how to build a listening indicator.
last_reviewed: "2026-06-11"
---

Transcription events deliver the text of what the user said and signal when the Speech-to-Text (STT) service is actively processing audio. Use them to build chat-history displays, live "listening" indicators, and push-to-talk feedback.

## `final-user-transcription`

Sent once the STT service has produced a final (non-interim) transcript of the user's utterance. The event fires after VAD has confirmed the user stopped speaking.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "final-user-transcription",
    "text": "Hello, how are you today?",
    "speaker_id": "user_123",
    "speaker_name": "Alice",
    "participant_id": "participant_456",
    "message_id": "msg_789"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"final-user-transcription"`. |
| `text` | string | The transcribed text of the user's utterance. |
| `speaker_id` | string \| null | Optional identifier for the speaker. Present in multi-participant sessions. |
| `speaker_name` | string \| null | Optional display name of the speaker. |
| `participant_id` | string \| null | Optional transport-level participant identifier. |
| `message_id` | string \| null | Optional identifier for this specific message, useful for deduplication. |

**Recommended action:** Append `text` to your conversation history or chat UI. The optional speaker fields are useful in multi-participant shared sessions.

## `vad-stt-started`

Sent when the VAD (Voice Activity Detection) gating processor confirms speech and unmutes the STT service. This event indicates that the server is now actively transcribing the user's audio. The `pre_roll_ms` field shows how much audio captured before detection was prepended to the stream so that the start of the utterance is not clipped.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "vad-stt-started",
    "timestamp": "2024-01-15T10:30:45.123Z",
    "pre_roll_ms": 1500
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"vad-stt-started"`. |
| `timestamp` | string | ISO 8601 timestamp of when the STT service was unmuted. |
| `pre_roll_ms` | integer | Amount of audio pre-roll (in milliseconds) prepended to the stream before the detected speech onset. |

**Recommended action:** Show a "listening" or "transcribing" indicator in your UI.

## `vad-stt-stopped`

Sent when the VAD gating processor mutes the STT service after the hangover period expires. This event marks the end of a speech segment — the user has stopped speaking and the STT gate has closed.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "vad-stt-stopped",
    "timestamp": "2024-01-15T10:30:48.456Z",
    "reason": "hangover_elapsed",
    "audio_duration_ms": 3200
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"vad-stt-stopped"`. |
| `timestamp` | string | ISO 8601 timestamp of when the STT service was muted. |
| `reason` | string | Reason the STT gate closed. `"hangover_elapsed"` is the normal value when the post-speech hangover period completed. |
| `audio_duration_ms` | integer \| null | Total duration of audio processed in this segment, in milliseconds. May be `null` if the duration was not measured. |

**Recommended action:** Remove the "listening" indicator. A `final-user-transcription` event will follow shortly after the gate closes.

## VAD and STT configuration

The VAD gate thresholds — confidence, start time, stop time, and minimum volume — are configured per session using the `vad_params` field of the `/connect` request. See [VAD parameters](../endpoints/vad-params.md) for the full field reference.

## Related pages

{% content-ref url="server-events.md" %}
[Server events overview](server-events.md)
{% endcontent-ref %}

{% content-ref url="../endpoints/vad-params.md" %}
[VAD parameters](../endpoints/vad-params.md)
{% endcontent-ref %}
