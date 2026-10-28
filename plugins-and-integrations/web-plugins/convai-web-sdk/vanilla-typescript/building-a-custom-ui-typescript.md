---
title: Build a custom UI in TypeScript
description: Build your own chat interface on the Convai Web SDK in plain TypeScript, with connection status, messages, the character's voice, and media controls.
last_reviewed: "2.0.2"
---

Build a chat interface of your own on top of `ConvaiClient` instead of using the prebuilt widget. Use this page when the widget does not fit your design. At the end, your page connects, shows the conversation, plays the character's voice, and toggles the microphone.

## Prerequisites

- `@convai/web-sdk` installed. See [Get started with vanilla TypeScript](README.md).
- A Convai API key or auth token, and a character ID.

## Add the markup

{% code title="index.html" %}
```html
<div id="status">disconnected</div>
<button id="connect">Connect</button>
<button id="mic" disabled>Unmute</button>

<div id="chat"></div>

<input id="input" type="text" placeholder="Type a message" disabled />
<button id="send" disabled>Send</button>

<script type="module" src="/src/main.ts"></script>
```
{% endcode %}

## Wire the client

The script below connects on click, keeps the controls in step with `stateChange`, renders the conversation from `messagesChange`, and plays the character's voice through `AudioRenderer`.

{% code title="src/main.ts" %}
```typescript
import {
  AudioRenderer,
  ConvaiClient,
  type ChatMessage,
  type ConvaiClientState,
} from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
});

const statusEl = document.getElementById('status') as HTMLDivElement;
const connectBtn = document.getElementById('connect') as HTMLButtonElement;
const micBtn = document.getElementById('mic') as HTMLButtonElement;
const chatEl = document.getElementById('chat') as HTMLDivElement;
const inputEl = document.getElementById('input') as HTMLInputElement;
const sendBtn = document.getElementById('send') as HTMLButtonElement;

let audioRenderer: AudioRenderer | null = null;

client.on('stateChange', (state: ConvaiClientState) => {
  statusEl.textContent = state.isConnected ? state.agentState : 'disconnected';
  connectBtn.disabled = state.isConnected || state.isConnecting;
  micBtn.disabled = !state.isConnected;
});

client.on('botReady', () => {
  inputEl.disabled = false;
  sendBtn.disabled = false;
});

client.on('messagesChange', (messages: ChatMessage[]) => {
  const shown = messages.filter(
    (m) =>
      (m.type === 'user-llm-text' ||
        m.type === 'user-transcription' ||
        m.type === 'bot-llm-text' ||
        m.type === 'bot-output') &&
      m.content.trim(),
  );
  chatEl.replaceChildren(
    ...shown.map((m) => {
      const div = document.createElement('div');
      div.className = m.type.startsWith('user') ? 'user' : 'bot';
      div.textContent = m.content;
      return div;
    }),
  );
  chatEl.scrollTop = chatEl.scrollHeight;
});

// Play the character's voice on the default WebRTC transport.
client.on('connect', () => {
  audioRenderer ??= new AudioRenderer(client.room);
});

client.on('disconnect', () => {
  audioRenderer?.destroy();
  audioRenderer = null;
  inputEl.disabled = true;
  sendBtn.disabled = true;
});

connectBtn.addEventListener('click', async () => {
  try {
    await client.connect();
  } catch (error) {
    statusEl.textContent = error instanceof Error ? error.message : 'connect failed';
  }
});

function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;
  client.sendUserTextMessage(text);
  inputEl.value = '';
}

sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage();
});

micBtn.addEventListener('click', async () => {
  try {
    await client.audioControls.toggleAudio();
    micBtn.textContent = client.audioControls.isAudioMuted ? 'Unmute' : 'Mute';
  } catch (error) {
    console.error('Microphone toggle failed:', error);
  }
});
```
{% endcode %}

On the default WebRTC transport the microphone starts off unless you set `startWithAudioOn: true`, so the first click asks the browser for microphone permission. Media control methods are async and reject when the browser denies the device, so keep them inside `try`.

{% hint style="warning" %}
Without an `AudioRenderer`, a custom UI on the WebRTC transport connects and receives text, but the character's voice never plays. The chat widget creates one for you; a custom UI must create its own.
{% endhint %}

## Play audio on the WebSocket transport

With `transport: 'websocket'`, the transport plays the voice; no wiring is needed. Pipecat's WebSocket transport plays the character's audio through its own Web Audio player, so a custom UI needs no `AudioRenderer` and no `botAudioTrack` listener:

```typescript
import '@convai/web-sdk/vanilla/websocket';
import { ConvaiClient } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  transport: 'websocket',
});

await client.connect(); // the character's voice plays with no extra code
```

The `botAudioTrack` event does not fire on this transport, so an `AudioRenderer` created for it stays silent and does no harm.

See [Use the WebSocket transport](../websocket-transport-layer.md) for the rest of the setup.

## Add camera and screen share controls

Camera and screen share need a video connection. Set `enableVideo: true` in the client configuration, then call the controls:

```typescript
await client.videoControls.toggleVideo();
await client.screenShareControls.toggleScreenShare();
```

Read `client.videoControls.isVideoEnabled` and `client.screenShareControls.isScreenShareActive` to label the buttons, or subscribe to `videoStateChange` and `screenShareStateChange` on the same control objects.

## Verify the UI

Click **Connect**. The status shows `connected`, the input enables once the character is ready, and a typed message is answered both in the chat and aloud. Click the microphone button and speak: your words appear as a transcription and the character replies.

## Next steps

{% content-ref url="events-and-message-handling.md" %}
[Handle events and messages in TypeScript](events-and-message-handling.md)
{% endcontent-ref %}

{% content-ref url="convaiclient-core-api.md" %}
[ConvaiClient reference](convaiclient-core-api.md)
{% endcontent-ref %}

{% content-ref url="real-time-lipsync.md" %}
[Add lip sync in vanilla TypeScript](real-time-lipsync.md)
{% endcontent-ref %}
