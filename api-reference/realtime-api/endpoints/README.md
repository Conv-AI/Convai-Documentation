---
title: Endpoints
description: Reference pages for every Realtime API endpoint, covering request fields, response fields, shared sessions, and conversation resumption.
---

The endpoints section documents the public surface of the Realtime API in detail. Start with the `POST /connect` reference, which is the only HTTP endpoint needed to establish a realtime session.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>POST /connect</strong><br>Endpoint anatomy: method, URL, auth, request and response shapes, and all HTTP error codes.</td>
<td><a href="connect.md">connect.md</a></td>
</tr>
<tr>
<td><strong>ConnectRequest field reference</strong><br>Every request body field with its type, default, constraints, and allowed values.</td>
<td><a href="connect-request-reference.md">connect-request-reference.md</a></td>
</tr>
<tr>
<td><strong>ConnectResponse field reference</strong><br>Every response field with transport-conditional presence and descriptions.</td>
<td><a href="connect-response-reference.md">connect-response-reference.md</a></td>
</tr>
<tr>
<td><strong>Shared sessions</strong><br>Create and join a shared session; configure participant limits; handle 409 conflicts.</td>
<td><a href="shared-sessions.md">shared-sessions.md</a></td>
</tr>
<tr>
<td><strong>Resume a conversation</strong><br>Pass a prior session identifier to restore conversation history in a new session.</td>
<td><a href="resume-conversation.md">resume-conversation.md</a></td>
</tr>
<tr>
<td><strong>Audio output configuration</strong><br>WAV header, sample rate, chunk duration, and audio routing mode reference.</td>
<td><a href="audio-config.md">audio-config.md</a></td>
</tr>
<tr>
<td><strong>VAD parameters</strong><br>Voice activity detection fields, defaults, and per-character override behavior.</td>
<td><a href="vad-params.md">vad-params.md</a></td>
</tr>
<tr>
<td><strong>POST /disconnect</strong><br>Teardown endpoint: parameters, auth requirements, response format, and unauthenticated risk.</td>
<td><a href="disconnect.md">disconnect.md</a></td>
</tr>
<tr>
<td><strong>WebSocket /chat</strong><br>WebSocket transport endpoint: query parameter, one-connection constraint, and close codes.</td>
<td><a href="chat-websocket.md">chat-websocket.md</a></td>
</tr>
</tbody>
</table>
