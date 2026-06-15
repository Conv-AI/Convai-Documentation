---
title: trigger-message
description: Reference for the trigger-message client message type, including saved-trigger, inline event, and scripted speech payload modes.
last_reviewed: "2026-06-15"
---

`trigger-message` notifies Convai of a saved Narrative Design trigger or inline narrative text during an active session. Send exactly one payload mode at a time: `trigger_name` for saved triggers, or `trigger_message` for inline events and scripted speech.

## Message format

Saved trigger:

```json
{
  "type": "trigger-message",
  "data": {
    "trigger_name": "enemy_spotted"
  }
}
```

Inline event:

```json
{
  "type": "trigger-message",
  "data": {
    "trigger_message": "An enemy unit has entered the training area from the north gate."
  }
}
```

Scripted speech:

```json
{
  "type": "trigger-message",
  "data": {
    "trigger_message": "<speak>Attention: the north gate is now open.</speak>"
  }
}
```

## Data fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `trigger_name` | string | Conditional | N/A | Saved trigger name to fire. Use this field by itself. |
| `trigger_message` | string | Conditional | N/A | Inline event text or scripted speech payload. Use this field by itself. |

Exactly one of `trigger_name` or `trigger_message` must be present. Do not send both fields in the same `trigger-message` payload. Do not send an empty `data` object.

For scripted speech, wrap the text in `<speak>...</speak>` before sending `trigger_message`. Unity SDK callers should not write these tags manually; `InvokeSpeech("text")` adds them internally.

## Server response

```json
{
  "type": "server-response",
  "event_type": "trigger-message",
  "status": "success",
  "message": "Trigger message processed successfully",
  "extras": {
    "trigger_name": "enemy_spotted",
    "has_speak_tag": false
  }
}
```

| Field | Type | Description |
|---|---|---|
| `extras.trigger_name` | string | The `trigger_name` value from the original request. |
| `extras.has_speak_tag` | bool | Present only when the trigger resolved to context text. `true` when the trigger handler contains a speak tag that delivers audio output directly, bypassing the LLM. `false` otherwise. When no context text was generated, this field is absent from the response. |

## When to use trigger-message

`trigger-message` is appropriate when an external event in the application needs to influence the bot's behavior without being framed as user speech. Common uses include:

- Invoking a saved Narrative Design trigger with `trigger_name`.
- Notifying Convai when a player enters a new zone or completes an objective with `trigger_message`.
- Sending exact scripted speech with a `<speak>...</speak>` `trigger_message`.

For injecting situational text into the bot's context window, use [`context-update`](context-update-message.md) instead.

{% content-ref url="client-messages.md" %}
[Client messages overview](client-messages.md)
{% endcontent-ref %}
