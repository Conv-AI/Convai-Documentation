---
title: Client message errors
description: Reference for the three error responses Convai returns for malformed, structurally invalid, or unrecognized client messages in the Realtime API.
last_reviewed: "2026-06-11"
---

When a client message cannot be parsed, is missing the required `type` field, or uses an unrecognized message type, Convai returns a `server-response` with `status: "error"`. These are not separate message types — they use the standard `server-response` format with an `event_type` field that identifies the error category.

## Error response format

All three error categories follow the same `server-response` structure.

```json
{
  "type": "server-response",
  "event_type": "<error-category>",
  "status": "error",
  "message": "<fixed error string>",
  "extras": { }
}
```

The `event_type` field identifies which error occurred. The `message` field contains a fixed string — match it exactly when writing error handling logic. The `extras` field carries additional diagnostic data that varies by error category.

## parse-error

Convai returns `parse-error` when the raw bytes sent by the client cannot be decoded as valid UTF-8 JSON.

```json
{
  "type": "server-response",
  "event_type": "parse-error",
  "status": "error",
  "message": "Failed to parse message: invalid JSON or UTF-8 encoding",
  "extras": null
}
```

**Cause:** sending binary data that is not valid UTF-8, sending malformed JSON such as unbalanced braces or unquoted keys, or encoding the payload with the wrong character set.

## validation-error

Convai returns `validation-error` when the message is valid JSON but does not contain a `type` field.

```json
{
  "type": "server-response",
  "event_type": "validation-error",
  "status": "error",
  "message": "Message missing required 'type' field",
  "extras": {
    "received_message": {
      "data": {
        "text": "Hello"
      }
    }
  }
}
```

| Field | Description |
|---|---|
| `extras.received_message` | The message object as received by the server, included to help identify the missing or misspelled field. |

**Cause:** the message envelope is valid JSON but the `type` key is absent or misspelled at the top level.

## unknown-message-type

Convai returns this error when the `type` value is present but does not match any of the 12 accepted type strings. Unlike parse-error and validation-error, the `event_type` field echoes back the unrecognized type string that was sent — it is not the fixed value `"unknown-message-type"`.

```json
{
  "type": "server-response",
  "event_type": "my-custom-message",
  "status": "error",
  "message": "Unknown message type: my-custom-message",
  "extras": {
    "supported_types": [
      "user_text_message",
      "trigger-message",
      "update-template-keys",
      "update-scene-metadata",
      "update-dynamic-info",
      "context-update",
      "tts-toggle",
      "stt-toggle",
      "kill-pipeline",
      "interrupt-bot",
      "force-user-stopped-speaking",
      "reset-idle-timer"
    ]
  }
}
```

| Field | Description |
|---|---|
| `extras.supported_types` | The complete list of accepted type strings as recognized by the server. |

The `message` field contains the exact type string that was received, formatted as `"Unknown message type: <received-type>"`.

## Supported types list

The `extras.supported_types` array contains all 12 accepted type strings. `update-dynamic-info` appears in this list because it is a legacy alias maintained for server-side compatibility — it is not recommended for new integrations.

{% content-ref url="client-messages.md" %}
[Client messages overview](client-messages.md)
{% endcontent-ref %}
