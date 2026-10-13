---
title: Get started with vanilla TypeScript
description: Install the Convai Web SDK in a project without a UI framework, connect a client to a character, and add the optional chat widget.
last_reviewed: "1.9.0"
---

Connect to a Convai character from plain TypeScript or JavaScript, with no React or other UI framework. Use this page when you set up the SDK in a framework-free project for the first time. At the end, your page holds a connected client and, optionally, the prebuilt chat widget.

## Prerequisites

- A project with a package manager and a bundler that resolves npm packages.
- A Convai account, an API key from <code class="expression">space.vars.dashboard_url</code>, and a character ID.

## Install the package

The vanilla API is part of the single `@convai/web-sdk` package. There is no separate package to install.

{% tabs %}
{% tab title="npm" %}
```bash
npm install @convai/web-sdk
```
{% endtab %}

{% tab title="pnpm" %}
```bash
pnpm add @convai/web-sdk
```
{% endtab %}

{% tab title="yarn" %}
```bash
yarn add @convai/web-sdk
```
{% endtab %}
{% endtabs %}

Import from `@convai/web-sdk/vanilla`. It exports `ConvaiClient`, the SDK's own `AudioRenderer` class, `createConvaiWidget`, `destroyConvaiWidget`, and every core type. `ConvaiClient` is also available from `@convai/web-sdk/core`.

## Create and connect a client

Pass the configuration to the constructor, subscribe to events, then call `connect()`. Wait for `botReady` before you send the first message.

{% code title="src/main.ts" %}
```typescript
import { ConvaiClient } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  endUserId: 'user-uuid', // optional: enables long-term memory and per-user analytics
});

client.on('stateChange', (state) => {
  console.log('Agent state:', state.agentState);
});

client.on('message', (message) => {
  console.log(message.type, message.content);
});

client.on('botReady', () => {
  client.sendUserTextMessage('Hello!');
});

try {
  await client.connect();
} catch (error) {
  console.error('Connect failed:', error);
}
```
{% endcode %}

`connect()` requires `characterId` and either `apiKey` or `authToken`. Without them it throws `Either apiKey or authToken is required, and characterId is required`. You can also omit the constructor argument and pass the configuration to `connect(config)` instead.

Set `enableVideo: true` to open a video connection that supports camera and screen share. With the default `false`, the connection is audio only.

{% hint style="danger" %}
An API key in client-side code is readable by anyone who opens the page. For a public page, create a short-lived auth token on your server and pass `authToken` instead. See [Connect with an auth token](../auth-tokens.md).
{% endhint %}

## Play the character's audio

The chat widget plays the character's voice for you. If you build your own UI on the default WebRTC transport, create an `AudioRenderer` for the client's room. Without it, the character's audio is never attached to the page.

```typescript
import { AudioRenderer } from '@convai/web-sdk/vanilla';

client.on('connect', () => {
  const audioRenderer = new AudioRenderer(client.room);
  // Call audioRenderer.destroy() when you tear the session down.
});
```

See [Build a custom UI in TypeScript](building-a-custom-ui-typescript.md) for the full pattern, including the WebSocket transport.

## Add the chat widget

`createConvaiWidget(container, options)` mounts a ready-made chat and voice UI into a DOM element and returns a widget handle. The widget connects the client the first time it is clicked, and uses `reconnect()` when it is opened again after a disconnect.

```typescript
import { ConvaiClient, createConvaiWidget } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableVideo: true,
});

const widget = createConvaiWidget(document.body, {
  convaiClient: client,
  showVideo: true,
  showScreenShare: true,
});

// When you remove the widget:
widget.destroy(); // or destroyConvaiWidget(widget)
```

Pass either an existing `convaiClient`, or credentials and a character ID so the widget creates the client itself. Without either, `createConvaiWidget` throws `Either convaiClient or (apiKey or authToken) and characterId must be provided`.

| Option | Type | Default | Description |
|---|---|---|---|
| `convaiClient` | `ConvaiClient` | none | Client the widget drives. |
| `apiKey`, `authToken`, `characterId` | `string` | none | Used only when `convaiClient` is omitted, to create a client. |
| `enableVideo`, `startWithVideoOn` | `boolean` | `false` | Forwarded to the client the widget creates. |
| `enableLipsync`, `enableEmotion` | `boolean` | `false` | Forwarded to the client the widget creates. |
| `blendshapeConfig` | `object` | none | Forwarded to the client the widget creates. |
| `showVideo` | `boolean` | `true` | Shows the camera toggle in settings. Applies only to a video connection. |
| `showScreenShare` | `boolean` | `true` | Shows the screen-share toggle in settings. Applies only to a video connection. |
| `defaultVoiceMode` | `boolean` | `true` | Opens the widget in voice mode. |
| `onConnect` | `() => void` | none | Called after the client connects. |
| `onDisconnect` | `() => void` | none | Called after the client disconnects. |
| `onMessage` | `(message: ChatMessage) => void` | none | Called with the newest chat message. |

When the widget creates the client itself, it forwards only the options in the table. To set any other `ConvaiConfig` field, create the client yourself and pass it as `convaiClient`.

The returned handle exposes `element` (the widget's root element), `client`, and `destroy()`.

## Verify the connection

Load the page, then open the widget or call `connect()`. The `stateChange` handler logs `connected` once the session is up, and the character answers the first message after `botReady` fires.

## Next steps

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ConvaiClient reference</strong><br>Every property, method, and control interface of the client.</td>
<td><a href="convaiclient-core-api.md">convaiclient-core-api.md</a></td>
</tr>
<tr>
<td><strong>Handle events and messages in TypeScript</strong><br>Subscribe to state, messages, and transcription, and render the conversation.</td>
<td><a href="events-and-message-handling.md">events-and-message-handling.md</a></td>
</tr>
<tr>
<td><strong>Add lip sync in vanilla TypeScript</strong><br>Play streamed blendshape frames on a three.js character.</td>
<td><a href="real-time-lipsync.md">real-time-lipsync.md</a></td>
</tr>
<tr>
<td><strong>Build a custom UI in TypeScript</strong><br>Wire your own chat interface, audio playback, and media controls.</td>
<td><a href="building-a-custom-ui-typescript.md">building-a-custom-ui-typescript.md</a></td>
</tr>
<tr>
<td><strong>Configuration and type reference</strong><br>Every configuration field, state field, and exported entry point.</td>
<td><a href="best-practices-and-type-definitions.md">best-practices-and-type-definitions.md</a></td>
</tr>
<tr>
<td><strong>Blendshape channel order reference</strong><br>The channel order of the ARKit and MetaHuman blendshape frames.</td>
<td><a href="mappings-reference.md">mappings-reference.md</a></td>
</tr>
</tbody>
</table>
