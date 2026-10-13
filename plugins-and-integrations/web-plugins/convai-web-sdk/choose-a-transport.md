---
title: Choose a transport
description: Decide between SSE, WebRTC and WebSocket for a Convai Web SDK app, see the recommended SSE chat with a realtime voice mode and why, and set up any of them.
last_reviewed: "1.9.2"
icon: route
---

The Convai Web SDK reaches a character over three transports, and one `ConvaiClient` can use any of them. Use this page to pick one, or to combine SSE and realtime the way we recommend.

* **SSE** is for simpler chat: text input, with text or audio output. Each message is one HTTP request.
* **Realtime (WebRTC, the default)** is for conversations: voice in and out, video, screen share, lip sync and low latency. The session stays open while you are connected.
* **WebSocket** carries realtime voice where WebRTC is blocked, such as some webviews and networks that block UDP. See [Use the WebSocket transport](websocket-transport-layer.md).

{% hint style="warning" %}
The interaction API that SSE uses is in beta. It is reachable at staging (`https://interaction-api-stg.convai.com/v1/interactions`) and on self-hosted deployments; a production host is planned. See [Chat over the SSE transport](sse-transport.md).
{% endhint %}

## Compare the transports

| | Realtime (WebRTC) | WebSocket | SSE |
| --- | --- | --- | --- |
| Text in, streamed text out | Yes | Yes | Yes |
| Character speech (TTS) | Yes, as an audio track | Yes | Yes, as PCM chunks your page plays |
| Voice in (microphone) | Yes | Yes | No |
| Interrupt by speaking | Yes | Yes | No; `sendInterruptMessage()` stops a reply |
| Video and screen share | Yes | No | No |
| Lip sync blendshapes | Yes | Yes | No |
| Connection | A room, open for the session | A socket, open for the session | Nothing open between messages |
| Microphone permission prompt | When the mic turns on | When the mic turns on | Never |
| Network | WebRTC, TURN relay by default | WebSocket | Plain HTTPS |
| Runs under Node or serverless | No | No | Yes |
| Selected by | `url` (default) | `transport: 'websocket'` | `interactionApiUrl` or `transport: 'sse'` |

## Recommended: SSE for chat, realtime for voice mode

Start each conversation on SSE, and move it to realtime only when the user chooses to talk. The Convai Playground runs its character chat this way in production.

* **Most turns are typed.** On SSE nothing is held open between messages. A realtime session keeps a room and the character's pipeline running while it is connected, idle or not, until the server closes it for inactivity.
* **The chat opens at once and asks for nothing.** SSE's `connect()` makes no network request and never prompts for the microphone. Realtime connects a room and waits for the character to join first, which takes a few seconds.
* **It works on more networks.** SSE is ordinary HTTPS. Restrictive networks can block WebRTC.
* **The character can still speak.** With TTS on, SSE streams each reply's speech on the same response.
* **Voice mode keeps the conversation.** Reconnecting the same client on realtime with the same character session ID carries the conversation over, and leaving voice mode does the reverse.

### Set up the text chat on SSE

Point `interactionApiUrl` at the interaction API, or at your own server route that adds the API key so the key never reaches the browser. Keep bot audio off until the user turns it on, and play the `audioData` chunks yourself. Each chunk is base64 signed 16-bit little-endian PCM with no WAV header; read `sample_rate` and `channels` from the chunk.

{% code title="chat.ts" %}
```ts
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  interactionApiUrl: 'YOUR_INTERACTION_API_URL',
  ttsEnabled: false,
});

const ctx = new AudioContext();
let botMuted = true;
let endsAt = 0;

client.on('audioData', ({ audio, sample_rate, channels }) => {
  if (botMuted) return;
  const bytes = Uint8Array.from(atob(audio), (c) => c.charCodeAt(0));
  const view = new DataView(bytes.buffer);
  const frames = bytes.length / 2 / channels;
  const buffer = ctx.createBuffer(channels, frames, sample_rate);
  for (let ch = 0; ch < channels; ch++) {
    const out = buffer.getChannelData(ch);
    for (let i = 0; i < frames; i++) out[i] = view.getInt16((i * channels + ch) * 2, true) / 0x8000;
  }
  const source = ctx.createBufferSource();
  source.buffer = buffer;
  source.connect(ctx.destination);
  const startAt = Math.max(endsAt, ctx.currentTime + 0.04);
  source.start(startAt);
  endsAt = startAt + buffer.duration;
});

// Wire this to a speaker button. Unmuting from a click lets the browser start audio.
function setBotMuted(muted: boolean) {
  botMuted = muted;
  if (!muted) void ctx.resume();
  client.toggleTts(!muted);
}

await client.connect();
client.sendUserTextMessage('Hello!');
```
{% endcode %}

`botTurnCompleted` fires when the last chunk has been delivered, so a reply's voice can still be playing when the user sends again. Stop the queued sources on send so the old reply does not talk over the new one.

### Move the conversation to realtime for voice mode

Save the character session ID, then reconnect the same client on realtime with it. Turn TTS on and unmute the microphone once connected. The microphone can take a few seconds to go live, so show its state from the `audioStateChange` event on `client.audioControls`.

{% code title="voice-mode.ts" %}
```ts
let sessionId: string | undefined;
client.on('characterSessionId', (id) => {
  sessionId = id;
});

async function enterVoiceMode() {
  await client.disconnect();
  await client.connect({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    characterSessionId: sessionId,
    startWithAudioOn: false,
    ttsEnabled: false,
  });
  client.toggleTts(true);
  await client.audioControls.unmuteAudio();
}

async function exitVoiceMode() {
  await client.audioControls.muteAudio();
  await client.disconnect();
  await client.connect({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    interactionApiUrl: 'YOUR_INTERACTION_API_URL',
    characterSessionId: sessionId,
    ttsEnabled: false,
  });
}
```
{% endcode %}

{% hint style="info" %}
`disconnect()` clears the client's per-connection state. Keep the transcript in your own state across the switch, and append the next connection's messages, removing duplicates by `id`. Spoken turns arrive as `user-transcription` messages.
{% endhint %}

## Build on one transport

The recommendation is a default. Each transport also works on its own.

### Realtime only

Use realtime from the first message when voice is the main way people use your app, such as a talking avatar, a voice assistant or a kiosk, or when you need video, screen share or lip sync. The connection wait happens once, up front, and every turn after it has realtime latency. The prebuilt `ConvaiWidget` works this way; start with the [Web SDK quickstart](quickstart.md).

{% code title="realtime.ts" %}
```ts
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  startWithAudioOn: true,
});

await client.connect();
```
{% endcode %}

### SSE only

Use SSE alone when your app never listens to the user, such as a chat window, a support widget or a form assistant, with or without the character's voice. SSE is also the only transport that runs outside a browser, so use it for server-side integrations, CI checks and batch jobs. Import `@convai/web-sdk/core` there; the root and `/react` entry points load browser-only code. The setup is the text chat above without voice mode.

### WebSocket instead of WebRTC

Where this page says realtime, the WebSocket transport can stand in when WebRTC is unavailable. It carries voice and lip sync but not video. See [Use the WebSocket transport](websocket-transport-layer.md).

## Decide quickly

| Your app | Use |
| --- | --- |
| Is mainly a chat, with talking as an option | SSE with a realtime voice mode (recommended) |
| Is mainly spoken: an avatar, a voice assistant or a kiosk | Realtime only |
| Needs video, screen share or lip sync | Realtime only, or switch to realtime for those parts |
| Only takes typed input, with or without spoken replies | SSE only |
| Runs on a server, in CI or in a batch job | SSE only |
| Needs voice where WebRTC is blocked | WebSocket |
