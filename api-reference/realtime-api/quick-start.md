---
title: Connect your first character
description: Build a live session with a Convai character: authenticate, join a room, send an RTVI message, and close the session using the Realtime API.
last_reviewed: "2026-06-11"
---

This tutorial walks through connecting to a Convai character using the Realtime API. You authenticate, start a session with `POST /connect`, join a LiveKit room, send an RTVI text message, and close the session with `POST /disconnect`.

## Prerequisites

- A Convai account with an API key
- A character UUID — obtain it from the Convai dashboard
- The LiveKit client SDK installed in your environment (for step 2)

This walkthrough uses the LiveKit transport, which is the default. See [Choose a transport](transports.md) if your integration requires Daily or WebSocket instead.

{% stepper %}
{% step %}
### Authenticate and start the session

Send a `POST /connect` request with your `character_id` in the request body and your API key in the `X-API-Key` header. Convai provisions a LiveKit room and returns credentials.

The base URL for all Realtime API requests is <code class="expression">space.vars.live_server_url</code>.

```bash
curl -X POST https://live.convai.com/connect \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"character_id": "CHARACTER_ID"}'
```

A successful response returns these fields. Copy `session_id`, `room_url`, and `token` — you will use them in the next steps.

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "request_trace_id": "req_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
  "character_session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "room_url": "https://your-instance.livekit.cloud",
  "room_name": "room-abc123def",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
{% endstep %}

{% step %}
### Join the LiveKit room

Use the `room_url` and `token` from the previous response to join the room via the LiveKit client SDK. The Convai character agent joins the same room automatically.

```javascript
// pseudocode — adapt to your LiveKit client SDK version
import { Room } from 'livekit-client';

const room = new Room();
await room.connect(connectResponse.room_url, connectResponse.token);
console.log('Joined room:', connectResponse.room_name);
```

The LiveKit SDK handles the WebRTC negotiation. Audio from your microphone is sent to the character, and the character's audio responses arrive on the room's audio track.
{% endstep %}

{% step %}
### Send an RTVI text message

To send text as the user without microphone audio, publish a `user_text_message` RTVI message on the LiveKit data channel. Convai processes the text and the character responds as if the user had spoken it.

```json
{
  "type": "user_text_message",
  "data": {
    "text": "Hello, who are you?"
  }
}
```

Serialize this object as a UTF-8 JSON string and send it on the LiveKit data channel. The character agent responds with audio on the room's audio track and sends a `server-response` acknowledgment on the data channel.
{% endstep %}

{% step %}
### Close the session

When the conversation is complete, call `POST /disconnect` with the `session_id` from step 1 as a query parameter. This terminates the session and releases its resources.

```bash
curl -X POST "https://live.convai.com/disconnect?session_id=SESSION_ID"
```

A successful response confirms the session is closed.

```json
{
  "status": "success",
  "message": "Session disconnected successfully"
}
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Confirm that `/disconnect` returned `{"status": "success", "message": "Session disconnected successfully"}` before releasing your LiveKit room resources.
{% endhint %}

{% hint style="warning" %}
`POST /disconnect` does not require authentication. Any caller who knows a valid `session_id` can terminate that session. Keep `session_id` values confidential within your application.
{% endhint %}

## Next steps

{% content-ref url="authentication.md" %}
[Authenticate to the Realtime API](authentication.md)
{% endcontent-ref %}

{% content-ref url="transports.md" %}
[Choose a transport](transports.md)
{% endcontent-ref %}
