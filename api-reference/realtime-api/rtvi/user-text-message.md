---
title: user_text_message
description: Reference for the user_text_message client message type that sends typed text as user input, bypassing speech-to-text processing.
last_reviewed: "2026-06-11"
---

`user_text_message` sends a text string to Convai as if the user had spoken it. The message bypasses the speech-to-text pipeline entirely, making it suitable for text-only interfaces, automated testing, and scenarios where typed input should drive the character's response without microphone audio.

## Message format

```json
{
  "type": "user_text_message",
  "data": {
    "text": "What is the evacuation procedure for sector 7?"
  }
}
```

{% hint style="info" %}
The type string uses an underscore: `user_text_message`. Most other client message types use hyphens. This inconsistency is intentional in the Realtime API.
{% endhint %}

## Data fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | Yes | — | The text string to deliver as user input. Convai processes this as if the user spoke the text. |

## Server response

Convai returns a `server-response` with the echoed text in `extras.text`.

```json
{
  "type": "server-response",
  "event_type": "user_text_message",
  "status": "success",
  "message": "User text message processed",
  "extras": {
    "text": "What is the evacuation procedure for sector 7?"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `extras.text` | string | The `text` value from the original request, echoed back. |

## Relationship to audio input

Audio input passes through the speech-to-text pipeline before reaching the language model. `user_text_message` skips that step and delivers the string directly. The bot cannot distinguish between text sent via `user_text_message` and text transcribed from microphone audio.

{% content-ref url="client-messages.md" %}
[Client messages overview](client-messages.md)
{% endcontent-ref %}
