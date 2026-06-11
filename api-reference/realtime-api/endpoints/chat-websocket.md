---
title: WebSocket /chat
description: Reference for WebSocket /chat: query parameter, one-connection-per-session constraint, close codes 1008 and 1011, and RTVI message flow.
last_reviewed: "2026-06-11"
---

`WebSocket /chat` is the realtime conversation transport endpoint for sessions created with `transport="websocket"`. After a successful `POST /connect`, connect a WebSocket client directly to the `room_url` returned in the response. All conversation messages, audio, and control events flow over this connection using the RTVI envelope format.

## Endpoint

**`WebSocket`** <code class="expression">space.vars.live_server_url</code>`/chat?session_id=<SESSION_ID>`

## Connection requirements

This endpoint only accepts sessions created with `transport="websocket"` in the `/connect` request. Connecting with a session that was created using a `daily` or `livekit` transport closes the connection immediately with close code `1008`.

Only one WebSocket connection per session is permitted at a time. Attempting a second connection while one is active closes the new connection with close code `1008` and the reason `"Session already has an active connection. Only one WebSocket per session allowed."`.

The `room_url` field in the `ConnectResponse` for a WebSocket session already contains the full connection URL, including the `session_id` query parameter (for example, `wss://live.convai.com/chat?session_id=<uuid>`). Pass `room_url` directly to your WebSocket client — do not append `session_id` again.

## Authentication

No authentication header is required. Authentication is inherited from the session established by `POST /connect`.

## Query parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `session_id` | string (UUID) | Yes | The session identifier returned by `/connect` |

## Close codes

The server sends one of the following close codes when a connection cannot be established or must be terminated abnormally.

### Close code 1008

`1008` indicates a policy violation. Do not retry with the same `session_id`; call `POST /connect` to start a new session.

| Reason | Cause |
|---|---|
| `"Session not found in cache or database"` | No session matching `session_id` was found. The session may have expired or never existed. |
| `"Session not found in database"` | Session data was present in cache but could not be validated in the database. |
| `"Session metadata incomplete. Please reconnect via /connect"` | The session is missing required metadata fields. |
| `"User authentication failed. Please reconnect via /connect"` | User credentials associated with the session could not be resolved. |
| `"Character not found or not accessible. Please reconnect via /connect"` | The character linked to the session no longer exists or is not accessible to the API key. |
| `"Session expired. Please reconnect via /connect"` | The session's end time has passed. |
| `"Session transport mismatch. Please reconnect via /connect"` | The session was created with a transport other than `websocket`. |
| `"Session already has an active connection. Only one WebSocket per session allowed."` | Another WebSocket connection is already active for this session. Close the existing connection before reconnecting. |

### Close code 1011

`1011` indicates an unexpected server error.

| Reason | Cause |
|---|---|
| `"Session data incomplete. Please reconnect via /connect"` | Cached session data is missing required fields. Start a new session with `POST /connect`. |

Unhandled server exceptions also produce close code `1011` with the exception message as the reason string, which varies depending on the error.

## Message size

The server enforces a maximum inbound message size of `16 MB`. For audio streaming, keep individual audio messages at or below `10 MB`, which accommodates approximately one minute of audio at 128 kbps.

## RTVI message flow

All messages exchanged over this WebSocket use the RTVI (Realtime Voice Interaction) envelope format.

**Client → server messages** use this structure:

```json
{
  "type": "<message-type>",
  "data": { ... }
}
```

`type` is required. `data` is optional; its shape depends on the message type.

**Server → client messages** use the RTVI server-message envelope:

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "<message-type>",
    ...payload fields
  }
}
```

The server sends a `server-response` message in response to every client message. The `status` field in `server-response` is one of `"success"`, `"error"`, `"processing"`, or `"pending"`.

## Usage example

A safety-training application connects a WebSocket client after calling `POST /connect` with `transport="websocket"`.

```javascript
// connectResponse is the JSON body from POST /connect
// room_url already contains the full URL including session_id
const ws = new WebSocket(connectResponse.room_url);

ws.addEventListener("open", () => {
  console.log("Connected to Convai realtime session");
});

ws.addEventListener("message", (event) => {
  const envelope = JSON.parse(event.data);
  if (envelope.label === "rtvi-ai" && envelope.type === "server-message") {
    const msg = envelope.data;
    console.log("Received:", msg.type, msg);
  }
});

ws.addEventListener("close", (event) => {
  if (event.code === 1008) {
    console.error("Session rejected:", event.reason);
    // Call POST /connect to start a new session before retrying
  }
});

// Send a text message as user input
ws.send(JSON.stringify({
  type: "user_text_message",
  data: { text: "Explain the fire evacuation procedure." },
}));
```

On `open`, the session is live. Incoming `server-message` envelopes carry the bot's responses, transcriptions, and control events. On close code `1008`, discard the session and reconnect via `POST /connect`.

## Next steps

{% content-ref url="connect.md" %}
[POST /connect](connect.md)
{% endcontent-ref %}

{% content-ref url="disconnect.md" %}
[POST /disconnect](disconnect.md)
{% endcontent-ref %}

{% content-ref url="../transports.md" %}
[Choose a transport](../transports.md)
{% endcontent-ref %}
