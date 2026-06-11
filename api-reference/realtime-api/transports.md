---
title: Choose a transport
description: Understand how LiveKit, Daily, and WebSocket transport protocols differ, when to choose each, and how RTVI messages route over each connection.
last_reviewed: "2026-06-11"
---

The Realtime API supports three transport protocols. You choose the transport at connect time by setting the `transport` field in your `POST /connect` request body. Once the session is established, the protocol is fixed for its lifetime.

## Available transports

| Transport | Value in `transport` field | Protocol | Best for |
|---|---|---|---|
| LiveKit | `livekit`, `internal`, `external` | WebRTC via LiveKit SFU | Most integrations. Supports bidirectional audio, data channels, and optional video tracks. The `room_name` field in the `/connect` response identifies the specific room. |
| Daily | `daily` | WebRTC via Daily | Integrations already built on Daily's infrastructure. Audio and data channels work the same way as LiveKit. |
| WebSocket | `websocket` | WebSocket over the `/chat` endpoint | Server-side or constrained environments where a full WebRTC stack is unavailable. The `/connect` response returns a `room_url` containing the `wss://` endpoint and `?session_id=...` parameter to connect to. |

The `transport` field defaults to `livekit` when omitted from the request body.

{% hint style="info" %}
The values `internal` and `external` are accepted aliases for `livekit`. Both map to LiveKit and produce identical behavior. Use `livekit` in new integrations — `internal` and `external` exist for backward compatibility with older clients.
{% endhint %}

The value `sse` appears in the transport mapping but is explicitly rejected during request validation. Submitting `"transport": "sse"` returns a `422 Unprocessable Entity` error.

## Default transport

When you omit the `transport` field, the server selects `livekit`. The `/connect` response includes `room_url` (the LiveKit server URL), `room_name` (the provisioned room name), and `token` (the LiveKit JWT). Pass `room_url` and `token` to the LiveKit client SDK to join. For WebSocket sessions, `room_url` contains the `wss://` endpoint with `?session_id=...` and `room_name` is not present.

## RTVI message routing

RTVI messages follow different paths depending on which transport you chose at connect time.

| Transport | How to send RTVI messages |
|---|---|
| LiveKit | Publish a UTF-8 JSON string on the LiveKit data channel after joining the room with `room_url` and `token`. |
| Daily | Publish a UTF-8 JSON string on the Daily data channel after joining the room with `room_url` and `token`. |
| WebSocket | Connect to the `room_url` from the `/connect` response (a `wss://` URL with `?session_id=...`) and send JSON frames directly over the WebSocket. |

For LiveKit and Daily, RTVI messages flow through the shared WebRTC data channel alongside the audio tracks. For WebSocket, messages flow directly over the `/chat` connection without a separate room.

## Next steps

{% content-ref url="quick-start.md" %}
[Connect your first character](quick-start.md)
{% endcontent-ref %}

{% content-ref url="identifiers.md" %}
[Session and character identifiers](identifiers.md)
{% endcontent-ref %}
