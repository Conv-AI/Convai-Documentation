---
description: >-
  This page shows how to wire up a simple DOM-based chat UI using vanilla
  TypeScript.
---

# Building a Custom UI (TypeScript)

## Example HTML

```html
<div id="status">Disconnected</div>
<button id="connect">Connect</button>

<div id="chat"></div>

<input id="input" type="text" placeholder="Type message..." disabled />
<button id="send" disabled>Send</button>
```

***

## TypeScript Implementation

```ts
import {
  ConvaiClient,
  type ConvaiClientState,
  type ChatMessage
} from '@convai/web-sdk/vanilla';

const client = new ConvaiClient();

const statusEl = document.getElementById('status') as HTMLDivElement;
const connectBtn = document.getElementById('connect') as HTMLButtonElement;
const chatEl = document.getElementById('chat') as HTMLDivElement;
const inputEl = document.getElementById('input') as HTMLInputElement;
const sendBtn = document.getElementById('send') as HTMLButtonElement;

// State updates
client.on('stateChange', (state) => {
  updateStatus(state);
  updateControls(state);
});

// New messages
client.on('message', (msg) => {
  if (msg.type === 'user-transcription' || msg.type === 'bot-llm-text') {
    addMessageToUI(msg);
  }
});

function updateStatus(state: ConvaiClientState) {
  if (!state.isConnected) return statusEl.textContent = 'Disconnected';
  statusEl.textContent = state.agentState;
}

function updateControls(state: ConvaiClientState) {
  const connected = state.isConnected;
  connectBtn.disabled = connected;
  inputEl.disabled = !connected;
  sendBtn.disabled = !connected;
}

function addMessageToUI(msg: ChatMessage) {
  const div = document.createElement('div');
  div.className = msg.type === 'user-transcription' ? 'user' : 'bot';
  div.textContent = msg.content;
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

// Connect logic
connectBtn.addEventListener('click', async () => {
  await client.connect({
    apiKey: 'your-api-key',
    characterId: 'your-character-id',
    // endUserId: 'user-uuid', // Optional for memory
  });
});

// Send message
function sendMessage() {
  const text = inputEl.value.trim();
  if (text) {
    client.sendUserTextMessage(text);
    inputEl.value = '';
  }
}

sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});
```

***

## Adding Audio/Video Controls

```ts
await client.audioControls.toggleAudio();
await client.videoControls.toggleVideo();
await client.screenShareControls.toggleScreenShare();
```
