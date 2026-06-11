---
title: ConnectResponse field reference
description: Complete field reference for the connect response body, including types, transport-conditional fields, and descriptions of every returned value.
last_reviewed: "2026-06-11"
---

`ConnectResponse` is the JSON body returned by a successful `POST /connect` call. All fields are present in every response, though some are `null` depending on the transport in use.

## Fields

| Field | Type | Always present | Description |
|---|---|---|---|
| `session_id` | `string (UUID)` | Yes | Unique token that identifies this session record. Pass to `POST /disconnect` to end the session. |
| `request_trace_id` | `string` | Yes | Server-side trace identifier for this `/connect` request. Use this value when reporting issues to Convai support to correlate logs, telemetry, and session records. |
| `character_session_id` | `string (UUID)` | Yes | Conversation session identifier. Persist this value and pass it back as `character_session_id` in a future `/connect` call to resume the conversation history. |
| `room_url` | `string` | Yes | Transport-specific room URL. For LiveKit, this is the LiveKit server base URL. For WebSocket, this is the `wss://` URL to connect to directly. |
| `room_name` | `string \| null` | LiveKit only | Room name within the LiveKit SFU. Pass this value to your LiveKit client SDK along with `token`. `null` for Daily and WebSocket transports. |
| `token` | `string` | Yes | Participant authentication token for the room. For LiveKit, this is a signed JWT. For WebSocket, this field is an empty string (no token required). |
| `end_user_id` | `string \| null` | No | The `end_user_id` provided in the request, echoed back. `null` when not provided. |
| `end_user_metadata` | `object \| null` | No | The `end_user_metadata` provided in the request, echoed back. `null` when not provided or when `end_user_id` was absent. |

## Transport-specific behavior

The `room_url`, `room_name`, and `token` fields behave differently depending on the transport selected in the request.

| Transport | `room_url` | `room_name` | `token` |
|---|---|---|---|
| `livekit` | LiveKit server base URL | LiveKit room name | Signed LiveKit participant JWT |
| `daily` | Daily room URL | `null` | Daily access token |
| `websocket` | WebSocket URL (`wss://…/chat?session_id=…`) | `null` | Empty string |

## Connecting a LiveKit client

After a successful `/connect` call with the LiveKit transport, use these three response fields to connect:

1. `room_url` — the LiveKit server URL
2. `room_name` — the room to join
3. `token` — the participant JWT

```javascript
const room = new LivekitClient.Room();
await room.connect(data.room_url, data.token, {
  // Some clients require room_name separately; others derive it from the token.
});
```

## Saving the character session identifier

Save `character_session_id` from the response if you intend to resume the conversation in a later session. This identifier lets Convai reload the conversation history when you pass it back in a future `/connect` request.

```json
{
  "character_session_id": "f7a8b9c0-e29b-41d4-a716-446655440001"
}
```

See [Resume a conversation](resume-conversation.md) for the full workflow.

## Next steps

{% content-ref url="connect-request-reference.md" %}
[ConnectRequest field reference](connect-request-reference.md)
{% endcontent-ref %}

{% content-ref url="resume-conversation.md" %}
[Resume a conversation](resume-conversation.md)
{% endcontent-ref %}

{% content-ref url="../identifiers.md" %}
[Session and character identifiers](../identifiers.md)
{% endcontent-ref %}
