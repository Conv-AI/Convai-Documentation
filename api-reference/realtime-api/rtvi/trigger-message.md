---
title: trigger-message
description: Reference for the trigger-message client message type, including the optional trigger_name and trigger_message fields and server-response extras.
last_reviewed: "2026-06-11"
---

`trigger-message` notifies Convai of a named event or narrative trigger during an active session. Use it to signal game events, advance story state, or inject contextual prompts without relying on user speech. Both `trigger_name` and `trigger_message` are optional — the bot's configured trigger handlers on the character determine what happens when the message arrives.

## Message format

```json
{
  "type": "trigger-message",
  "data": {
    "trigger_name": "enemy_spotted",
    "trigger_message": "An enemy unit has entered the training area from the north gate."
  }
}
```

## Data fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `trigger_name` | string | No | `null` | The name of the trigger to fire. Matched against configured trigger handlers on the character. |
| `trigger_message` | string | No | `null` | A message string passed to the trigger handler alongside the trigger name. |

Both fields are optional. Sending an empty `data` object `{}` or omitting either field is valid.

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

- Notifying the bot when a player enters a new zone or completes an objective.
- Advancing the bot through a scripted narrative step.
- Injecting contextual prompts from application logic without user interaction.

For injecting situational text into the bot's context window, use [`context-update`](context-update-message.md) instead.

{% content-ref url="client-messages.md" %}
[Client messages overview](client-messages.md)
{% endcontent-ref %}
