---
title: Realtime API
description: Connect your application to a Convai character in real time, send voice and text, and receive AI responses through LiveKit or WebSocket.
last_reviewed: "2026-06-11"
---

The Realtime API gives your application a persistent, bidirectional session with a Convai character that handles voice input, AI processing, and audio output in real time. Start a session with `POST /connect`, choose a transport protocol, join the resulting room, and exchange RTVI messages to send text or control the session. Sessions end with a call to `POST /disconnect`.

{% hint style="info" %}
**New to the Realtime API?** Follow [Connect your first character](quick-start.md) for an end-to-end walkthrough: authenticate, connect, send a message, and close the session.
{% endhint %}

### Get started

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Connect your first character</strong><br>End-to-end walkthrough: authenticate, join a room, send an RTVI message, and close the session.</td>
<td><a href="quick-start.md">quick-start.md</a></td>
</tr>
<tr>
<td><strong>Authenticate to the Realtime API</strong><br>Use X-API-Key or API-AUTH-TOKEN and understand how the server resolves the API key.</td>
<td><a href="authentication.md">authentication.md</a></td>
</tr>
<tr>
<td><strong>Choose a transport</strong><br>LiveKit and WebSocket — what each provides and when to use it.</td>
<td><a href="transports.md">transports.md</a></td>
</tr>
<tr>
<td><strong>Session and character identifiers</strong><br>Reference for session_id, character_session_id, end_user_id, and request_trace_id.</td>
<td><a href="identifiers.md">identifiers.md</a></td>
</tr>
<tr>
<td><strong>HTTP error codes</strong><br>Complete error code values, HTTP status mapping, and WebSocket close codes.</td>
<td><a href="error-codes.md">error-codes.md</a></td>
</tr>
</tbody>
</table>

### Core concepts

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Core concepts</strong><br>Session lifecycle, RTVI message protocol, and end-user identity.</td>
<td><a href="core-concepts/">core-concepts</a></td>
</tr>
</tbody>
</table>

### Endpoints

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Endpoints</strong><br>Reference for every Realtime API endpoint: connect, disconnect, and WebSocket chat.</td>
<td><a href="endpoints/">endpoints</a></td>
</tr>
</tbody>
</table>

### RTVI messages

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>RTVI client messages</strong><br>JSON commands your application sends to Convai during an active session.</td>
<td><a href="rtvi/client-messages.md">rtvi/client-messages.md</a></td>
</tr>
<tr>
<td><strong>RTVI server events</strong><br>Events the server sends to your client during a session, with envelope format and full reference index.</td>
<td><a href="rtvi/server-events.md">rtvi/server-events.md</a></td>
</tr>
</tbody>
</table>

### Features

Each feature is enabled through fields in the `POST /connect` request body or by sending RTVI messages during an active session.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Character actions</strong><br>Declare what physical actions a character can perform and receive structured instructions per turn.</td>
<td><a href="features/character-actions/">character-actions</a></td>
</tr>
<tr>
<td><strong>Dynamic context</strong><br>Inject live session data — game state, learner progress, environment changes — without reconnecting.</td>
<td><a href="features/dynamic-context/">dynamic-context</a></td>
</tr>
<tr>
<td><strong>File upload</strong><br>Send images to Convai during a LiveKit session and include visual context in the AI response.</td>
<td><a href="features/file-upload/">file-upload</a></td>
</tr>
</tbody>
</table>

## Supported transports

You specify the transport in the `transport` field of the `POST /connect` request body. The field defaults to `livekit` when omitted.

| Transport | Accepted `transport` values | Protocol |
|---|---|---|
| LiveKit | `livekit`, `internal`, `external` | WebRTC via LiveKit SFU |
| WebSocket | `websocket` | WebSocket over the `/chat` endpoint |

The value `sse` is not accepted and the server returns a `422 Unprocessable Entity` error if you submit it. See [Choose a transport](transports.md) for guidance on selecting the right protocol for your product.
