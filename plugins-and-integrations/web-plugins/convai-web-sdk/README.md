---
title: Convai Web SDK
description: Find the setup guides, feature how-tos, and API reference for the Convai Web SDK, which connects web apps to Convai characters by voice and text.
---

The Convai Web SDK, published on npm as `@convai/web-sdk`, connects a web page to a Convai character for real-time voice and text conversation, with optional camera, screen share, lip sync, actions, and emotions. It ships React bindings, a framework-free client, and a prebuilt chat widget for both. These pages describe release <code class="expression">space.vars.web_sdk_version</code>.

{% embed url="https://youtu.be/fK8R0SzuvNI" %}
Build browser-based conversational avatars with the Convai Web SDK, three.js, and React.
{% endembed %}

## Start here

The quickstart builds a first conversation in React. The two getting-started pages cover installation and the widget for each path; pick the one that matches your app.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Web SDK quickstart</strong><br>Connect to a character from React, send a message, and read its reply.</td>
<td><a href="quickstart.md">quickstart.md</a></td>
</tr>
<tr>
<td><strong>Get started with React</strong><br>Install the package, add the chat widget, and turn on camera and screen share.</td>
<td><a href="react/README.md">react/README.md</a></td>
</tr>
<tr>
<td><strong>Get started with vanilla TypeScript</strong><br>Create a client without a framework and mount the vanilla widget.</td>
<td><a href="vanilla-typescript/README.md">vanilla-typescript/README.md</a></td>
</tr>
</tbody>
</table>

## Add features

Each feature page shows the configuration and the client calls for one capability, for React and vanilla code alike.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Drive facial animation with blendshapes</strong><br>Stream lip sync frames and apply them to a 3D character's morph targets.</td>
<td><a href="lipsync-and-blendshape/README.md">lipsync-and-blendshape/README.md</a></td>
</tr>
<tr>
<td><strong>Handle character actions</strong><br>Receive semantic actions or run client tools and return their results.</td>
<td><a href="actions.md">actions.md</a></td>
</tr>
<tr>
<td><strong>Use character emotions</strong><br>Read the character's emotion and set its state of mind.</td>
<td><a href="emotions.md">emotions.md</a></td>
</tr>
<tr>
<td><strong>Update character context at runtime</strong><br>Send scene state, template keys, and files during a session.</td>
<td><a href="dynamic-context.md">dynamic-context.md</a></td>
</tr>
<tr>
<td><strong>Use long-term memory</strong><br>Let a character remember each person across sessions, and manage those memories.</td>
<td><a href="long-term-memory.md">long-term-memory.md</a></td>
</tr>
<tr>
<td><strong>Connect with an auth token</strong><br>Keep the API key on your server and connect the browser with a token.</td>
<td><a href="auth-tokens.md">auth-tokens.md</a></td>
</tr>
<tr>
<td><strong>Handle errors and disconnects</strong><br>Tell failures, disconnect reasons, and acknowledgments apart, and reconnect.</td>
<td><a href="error-handling.md">error-handling.md</a></td>
</tr>
<tr>
<td><strong>Choose a transport</strong><br>Pick SSE, WebRTC or WebSocket, or combine SSE chat with a realtime voice mode.</td>
<td><a href="choose-a-transport.md">choose-a-transport.md</a></td>
</tr>
<tr>
<td><strong>Chat over the SSE transport</strong><br>Stream text and optional speech over HTTP, with no WebRTC or microphone.</td>
<td><a href="sse-transport.md">sse-transport.md</a></td>
</tr>
<tr>
<td><strong>Use the WebSocket transport</strong><br>Connect over WebSocket instead of WebRTC.</td>
<td><a href="websocket-transport-layer.md">websocket-transport-layer.md</a></td>
</tr>
<tr>
<td><strong>Connect to a self-hosted deployment</strong><br>Point the SDK at your own hosts instead of api.convai.com.</td>
<td><a href="self-hosted-deployments.md">self-hosted-deployments.md</a></td>
</tr>
<tr>
<td><strong>Mute the character's voice</strong><br>Silence the character for the listener while it keeps speaking.</td>
<td><a href="mute-the-characters-voice.md">mute-the-characters-voice.md</a></td>
</tr>
<tr>
<td><strong>Host several characters in one room</strong><br>Connect a roster, switch who answers, and change members live (beta).</td>
<td><a href="multi-character-rooms.md">multi-character-rooms.md</a></td>
</tr>
<tr>
<td><strong>Connect to a character version</strong><br>Use a draft, the latest release, or a tag, and manage versions (beta).</td>
<td><a href="character-versioning.md">character-versioning.md</a></td>
</tr>
<tr>
<td><strong>Connect to a published text chat</strong><br>Run a credential-free, text-only chat from a publication grant.</td>
<td><a href="published-text-chat.md">published-text-chat.md</a></td>
</tr>
<tr>
<td><strong>Render links and link previews</strong><br>Show links the character sends, with optional site cards.</td>
<td><a href="link-previews.md">link-previews.md</a></td>
</tr>
</tbody>
</table>

## Look up the API

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ConvaiClient reference</strong><br>Every property, method, and control interface on the client.</td>
<td><a href="vanilla-typescript/convaiclient-core-api.md">vanilla-typescript/convaiclient-core-api.md</a></td>
</tr>
<tr>
<td><strong>Configuration and type reference</strong><br>Every connection option, the package entry points, and the shared types.</td>
<td><a href="vanilla-typescript/best-practices-and-type-definitions.md">vanilla-typescript/best-practices-and-type-definitions.md</a></td>
</tr>
<tr>
<td><strong>Web SDK event reference</strong><br>Every event the client emits, with its payload.</td>
<td><a href="event-reference.md">event-reference.md</a></td>
</tr>
<tr>
<td><strong>Read raw transport messages</strong><br>Inspect every incoming frame on each transport through rawMessage.</td>
<td><a href="raw-messages.md">raw-messages.md</a></td>
</tr>
<tr>
<td><strong>useConvaiClient hook reference</strong><br>What the React hook returns and which fields re-render.</td>
<td><a href="react/useconvaiclient-hook.md">react/useconvaiclient-hook.md</a></td>
</tr>
</tbody>
</table>

The SDK is not the legacy `convai-web-sdk` package documented under [Convai Web SDK (Legacy)](../convai-web-sdk-1/README.md). The two have different APIs, so code written for one does not run on the other.
