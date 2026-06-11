---
title: Control messages
description: Reference for the six Realtime API control messages that toggle audio, interrupt the bot, terminate the pipeline, and manage session timing.
last_reviewed: "2026-06-11"
---

Control messages manage the audio pipeline and session lifecycle during an active Realtime API session. The six control message types are `tts-toggle`, `stt-toggle`, `kill-pipeline`, `interrupt-bot`, `force-user-stopped-speaking`, and `reset-idle-timer`. None require session reconnection — send them at any point after the session is established.

## tts-toggle

`tts-toggle` enables or disables text-to-speech audio output from the bot. When TTS is disabled, the bot continues processing input but produces no audio output.

### Message format

```json
{
  "type": "tts-toggle",
  "data": {
    "enabled": false
  }
}
```

### Data fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `enabled` | bool | Yes | — | `true` enables TTS output. `false` disables it. |

### Server response

```json
{
  "type": "server-response",
  "event_type": "tts-toggle",
  "status": "success",
  "message": "TTS disabled",
  "extras": {
    "enabled": false
  }
}
```

`extras.enabled` reflects the new TTS state after the toggle.

## stt-toggle

`stt-toggle` mutes or unmutes speech-to-text microphone input. When STT is muted, audio from the microphone is not transcribed or sent to the bot.

### Message format

```json
{
  "type": "stt-toggle",
  "data": {
    "muted": true
  }
}
```

### Data fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `muted` | bool | Yes | — | `true` mutes the microphone. `false` unmutes it. |

### Server response

```json
{
  "type": "server-response",
  "event_type": "stt-toggle",
  "status": "success",
  "message": "STT muted",
  "extras": {
    "muted": true
  }
}
```

`extras.muted` reflects the new STT mute state after the toggle.

## kill-pipeline

`kill-pipeline` terminates the active session pipeline. The session ends immediately and the room closes.

{% hint style="danger" %}
This message ends the session permanently. The room closes and cannot be reopened — you must establish a new session to resume.
{% endhint %}

### Message format

```json
{
  "type": "kill-pipeline",
  "data": {}
}
```

### Data fields

This message takes no data fields. Send an empty object or omit `data`.

### Server response

```json
{
  "type": "server-response",
  "event_type": "kill-pipeline",
  "status": "success",
  "message": "Pipeline killed successfully",
  "extras": {
    "room_name": "convai-a1b2c3d4"
  }
}
```

`extras.room_name` is the name of the room that was terminated.

## interrupt-bot

`interrupt-bot` stops the bot's current speech turn immediately. Use it when the user starts speaking and your application handles interruption manually, or when application logic needs to stop the bot at a precise moment.

### Message format

```json
{
  "type": "interrupt-bot",
  "data": {}
}
```

### Data fields

This message takes no data fields. Send an empty object or omit `data`.

### Server response

Convai returns a `server-response` with `status: "success"`. No additional extras fields are documented for this message type.

## force-user-stopped-speaking

`force-user-stopped-speaking` manually signals that the user has stopped speaking, without waiting for voice activity detection to fire. Use it in push-to-talk implementations to trigger end-of-utterance processing exactly when the user releases the talk button.

### Message format

```json
{
  "type": "force-user-stopped-speaking",
  "data": {}
}
```

### Data fields

This message takes no data fields. Send an empty object or omit `data`.

### Server response

Convai returns a `server-response` with `status: "success"`. No additional extras fields are documented for this message type.

## reset-idle-timer

`reset-idle-timer` resets the session's idle-timeout counter. Use it to prevent an idle timeout from closing a session when the application is still active but the user has paused speaking for an extended period.

### Message format

```json
{
  "type": "reset-idle-timer",
  "data": {}
}
```

### Data fields

This message takes no data fields. Send an empty object or omit `data`.

### Server response

Convai returns a `server-response` with `status: "success"`. No additional extras fields are documented for this message type.

{% content-ref url="client-messages.md" %}
[Client messages overview](client-messages.md)
{% endcontent-ref %}

{% content-ref url="client-message-errors.md" %}
[Client message errors](client-message-errors.md)
{% endcontent-ref %}
