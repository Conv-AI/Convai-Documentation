---
title: Chat over the SSE transport
description: Send text to a Convai character over Server-Sent Events, keep the API key on your server, play the character's voice and run the client under Node.
last_reviewed: "2.0.2"
icon: tower-broadcast
---

Chat with a Convai character over the SSE transport: text in, with the reply streamed back as text and, optionally, as speech. Each message is one HTTP `POST` whose response is a stream of events, and nothing stays open between messages. There is no WebRTC, no room and no microphone, so the SSE transport also runs under Node. Use this page to set up a chat, keep your API key off the page, play the character's voice, or call a character from a server.

{% hint style="warning" %}
The interaction API behind the SSE transport is in beta. It is reachable in production at `https://interaction-api.convai.com/v1/interactions`, at staging (`https://interaction-api-stg.convai.com/v1/interactions`), and on self-hosted deployments.
{% endhint %}

## Prerequisites

- The Convai Web SDK installed. See [Web SDK quickstart](quickstart.md).
- An interaction API URL: the production or staging endpoint above, your self-hosted endpoint, or your own server route that forwards to one.

## Connect and send a message

Supplying `interactionApiUrl` selects the SSE transport when `transport` is omitted. You can also set `transport: 'sse'` explicitly.

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import { useConvaiClient } from '@convai/web-sdk/react';
import { ConvaiWidget } from '@convai/web-widget/react';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    interactionApiUrl: 'YOUR_INTERACTION_API_URL',
  });

  return <ConvaiWidget convaiClient={client} />;
}
```
{% endcode %}
{% endtab %}

{% tab title="TypeScript" %}
{% code title="src/main.ts" %}
```typescript
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  interactionApiUrl: 'YOUR_INTERACTION_API_URL',
});

client.on('characterSessionId', (id) => console.log('session', id));
client.on('messagesChange', (messages) => {
  const last = messages.at(-1);
  if (last) console.log(last.type, last.content);
});
client.on('botTurnCompleted', () => console.log('reply finished'));

await client.connect();
client.sendUserTextMessage('Say hello in exactly five words.');
```
{% endcode %}
{% endtab %}
{% endtabs %}

Two configurations make `connect()` throw:

| Configuration | Error |
|---|---|
| `transport: 'sse'` without `interactionApiUrl` | `interactionApiUrl is required when using the SSE transport` |
| `transport: 'sse'` with `enableVideo: true` | `The SSE transport supports text interactions only` |

### Key behaviours

- **`connect()` makes no network request.** It marks the session ready and emits `connect` and `botReady` at once. The first request goes out when you send a message.
- **The character session ID arrives on the first interaction.** There is no `/connect` handshake, so the server assigns the ID on the first message and the client emits `characterSessionId`. The event can fire again on later messages with the same value, so treat it as idempotent.
- **An API key travels as `Authorization: Bearer …`, an auth token as `API-AUTH-TOKEN`.** When you supply both, the SDK sends only `authToken`. Up to 1.9.3 the SDK sent `authToken` as a Bearer value too, which the interaction API rejects with `401`.
- **`botTurnCompleted` marks the end of a reply.** `turnEnd` never fires on SSE, because it depends on the character's speaking state, which this transport does not report.
- **Microphone, video, screen share and lip sync do nothing on this transport.** Speech output is the exception; see [Play the character's voice](#play-the-characters-voice).

## Keep the API key on a server route

An API key in browser code is visible to anyone who opens the page. Point `interactionApiUrl` at a route on your own server instead. The route adds the key, pins the character, and streams the response back unbuffered so text arrives as it is generated.

{% code title="api/interactions.ts" %}
```ts
// A Vercel Edge function; any server that can stream a response works.
export const config = { runtime: 'edge' };

export default async function handler(request: Request): Promise<Response> {
  if (request.method !== 'POST') return new Response(null, { status: 405 });
  const body = await request.json();

  const upstream = await fetch(process.env.CONVAI_INTERACTION_API_URL!, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.CONVAI_API_KEY}`,
      Accept: 'text/event-stream',
      'Content-Type': 'application/json',
    },
    // Pin the character here, so the route cannot be used for any other one.
    body: JSON.stringify({ ...body, character_id: process.env.CONVAI_CHARACTER_ID }),
    signal: request.signal,
  });

  return new Response(upstream.body, {
    status: upstream.status,
    headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache, no-transform' },
  });
}
```
{% endcode %}

In the browser, pass placeholders for the key and character, because the route supplies the real values:

{% code title="src/chat.ts" %}
```ts
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: 'proxied',
  characterId: 'proxied',
  interactionApiUrl: `${window.location.origin}/api/interactions`,
});
```
{% endcode %}

Set `CONVAI_API_KEY`, `CONVAI_CHARACTER_ID` and `CONVAI_INTERACTION_API_URL` as server environment variables only. A `VITE_` or `NEXT_PUBLIC_` prefix bundles them into the page.

## Play the character's voice

Speech is off by default on SSE. With `ttsEnabled: true`, the same response that carries the reply's text also carries its speech as `audioData` events. `toggleTts(enabled)` changes the setting for the next message.

The SDK emits the audio but does not play it, and neither `ConvaiWidget` nor `createConvaiWidget()` plays it for you. Each `audioData` chunk has these fields:

- `audio`: base64-encoded signed 16-bit little-endian PCM, with no WAV header.
- `sample_rate` and `channels`: read them from every chunk when you build audio buffers rather than hard-coding them.

This player schedules the chunks back to back with Web Audio, starts muted, and unmutes from a speaker button:

{% code title="src/voice.ts" %}
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
const sources = new Set<AudioBufferSourceNode>();

function stopVoice() {
  sources.forEach((s) => s.stop());
  sources.clear();
  endsAt = 0;
}

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
  source.onended = () => sources.delete(source);
  sources.add(source);
  const startAt = Math.max(endsAt, ctx.currentTime + 0.04);
  source.start(startAt);
  endsAt = startAt + buffer.duration;
});

// Wire this to a speaker button. Browsers start audio only from a user gesture.
function setBotMuted(muted: boolean) {
  botMuted = muted;
  if (muted) stopVoice();
  else void ctx.resume();
  client.toggleTts(!muted);
}

function send(text: string) {
  stopVoice(); // a new message cuts off the last reply's voice
  client.sendUserTextMessage(text);
}

await client.connect();
```
{% endcode %}

In React, subscribe in an effect instead: `useEffect(() => client.on('audioData', play), [client])`. `on()` returns the unsubscribe function, so the effect cleans up after itself.

### Playback notes

- **Unlock audio on a gesture.** Call `AudioContext.resume()` from a click or key press, or the browser keeps the context suspended and plays nothing.
- **Stop queued audio when the user sends.** `botTurnCompleted` fires when the last chunk has been delivered, not when it has finished playing, so the previous reply can still be speaking.
- **Text and audio arrive independently.** `bot-llm-text` messages and `audioData` chunks do not wait for each other.
- **There is no speaking state.** `isSpeaking` means little without a microphone. Drive any speaking indicator from your own sources' `onended`.

## Use the client under Node or on a server

SSE needs neither WebRTC nor a DOM, so it is the only transport that runs outside a browser: Node scripts, server-side rendering, serverless functions, CI checks and batch jobs. Import `@convai/web-sdk/core` there. The root and `@convai/web-sdk/react` entry points load browser-only code.

{% code title="ask.mjs" %}
```js
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: process.env.CONVAI_API_KEY,
  characterId: 'YOUR_CHARACTER_ID',
  interactionApiUrl: 'YOUR_INTERACTION_API_URL',
});

client.on('botTurnCompleted', async () => {
  const reply = client.chatMessages.filter((m) => m.type === 'bot-llm-text').at(-1);
  console.log(reply?.content);
  await client.disconnect();
});

await client.connect();
client.sendUserTextMessage('Summarize your role in one sentence.');
```
{% endcode %}

{% hint style="info" %}
Your own typed messages do not appear in `chatMessages` as user entries; the transcript fills from server-sent messages, as on the other transports. Render the user's input from your own state.
{% endhint %}

## API reference

| Property / Method | Type | Description |
|---|---|---|
| `transport` | `"livekit" \| "websocket" \| "sse"` | Selects the transport. Resolves to `"sse"` when omitted and `interactionApiUrl` is set; otherwise `"livekit"`. |
| `interactionApiUrl` | `string` | The interaction API endpoint, or your server route that forwards to it. Required for SSE. |
| `ttsEnabled` | `boolean` | Generates speech for each reply. Defaults to `false` on SSE. |
| `toggleTts(enabled)` | `(enabled: boolean) => void` | Turns speech on or off for the next message. |
| `sendUserTextMessage(text, options?)` | `(text: string, options?: SendUserTextMessageOptions) => void` | Sends one text message as one `POST`. |
| `sendInterruptMessage()` | `() => void` | Stops the reply in progress. |
| `characterSessionId` event | `(id: string) => void` | Emits the session ID the server assigned. Can repeat with the same value. |
| `audioData` event | `(data: AudioDataEvent) => void` | Emits one speech chunk: `audio` (base64 PCM), `sample_rate`, `channels`, `includes_wav_header` (always `false`). |
| `botTurnCompleted` event | `(data: unknown) => void` | Fires when a reply has been fully delivered. |

## Next steps

To decide between SSE and the realtime transports, and to set up the recommended SSE chat with a realtime voice mode, see [Choose a transport](choose-a-transport.md).
