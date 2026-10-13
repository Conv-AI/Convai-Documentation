---
title: Use the WebSocket transport
description: Connect a Convai character over a WebSocket instead of WebRTC, register the transport, and play the character's voice in React or plain TypeScript.
last_reviewed: "1.9.1"
icon: webhook
---

Switch a Convai Web SDK session from the default WebRTC transport, built on LiveKit, to a WebSocket transport built on Pipecat. Use this page when your deployment cannot use WebRTC or when you are testing the WebSocket path.

## How the transport is selected

`ConvaiConfig.transport` takes `"livekit"` (the default) or `"websocket"`. Both transports start with the same `POST /connect` request to Convai. With `"websocket"`, the SDK reads the WebSocket URL from the `room_url` field of the response and opens it through a registered WebSocket session.

The WebSocket session is not built into `ConvaiClient`. Only the `@convai/web-sdk/vanilla/websocket` subpath imports the Pipecat packages, and importing it registers the session with `ConvaiClient` as a side effect. An application that never imports that subpath does not load Pipecat code.

## Register the transport and connect

Import `@convai/web-sdk/vanilla/websocket` once, before `connect()` runs, and set `transport: 'websocket'`. React applications import the same subpath; the package has no React-specific WebSocket entry point.

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import '@convai/web-sdk/vanilla/websocket';
import { useConvaiClient, ConvaiWidget } from '@convai/web-sdk/react';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    transport: 'websocket',
  });

  return <ConvaiWidget convaiClient={client} />;
}
```
{% endcode %}
{% endtab %}

{% tab title="TypeScript" %}
{% code title="src/main.ts" %}
```typescript
import '@convai/web-sdk/vanilla/websocket';
import { ConvaiClient, AudioRenderer } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  transport: 'websocket',
});

const audio = new AudioRenderer(client.room);
client.on('botAudioTrack', (track: MediaStreamTrack) => audio.attachWebSocketTrack(track));
client.on('disconnect', () => audio.detachWebSocketTrack());

await client.connect();
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Play the character's voice

On the WebSocket transport the character's audio does not arrive through the LiveKit room, so a room-based audio renderer plays nothing. The SDK emits the bot audio as a `MediaStreamTrack` on the `botAudioTrack` event instead.

| Integration | What plays the audio |
|---|---|
| `useConvaiClient` in React | The hook creates a hidden `<audio data-convai-ws>` element and attaches each `botAudioTrack` to it. No extra code is needed. The React `ConvaiWidget` mute button mutes that element. |
| Vanilla TypeScript | Your code. Subscribe to `botAudioTrack` and call `attachWebSocketTrack(track)` on an `AudioRenderer`, as in the example above, or set the track on your own `<audio>` element. |

{% hint style="warning" %}
The vanilla `createConvaiWidget()` helper creates a room-based `AudioRenderer` only. With `transport: 'websocket'`, subscribe to `botAudioTrack` yourself, or the character is silent.
{% endhint %}

## Microphone behaviour

The microphone default differs between transports:

| Transport | Microphone after `connect()` |
|---|---|
| `"livekit"` | Off unless `startWithAudioOn` is `true`. |
| `"websocket"` | On, because the Pipecat session initializes the audio stream during `connect()`. The SDK mutes it right after connecting when `startWithAudioOn` is `false`. |

On the WebSocket transport, `connect()` always asks for microphone permission — even with `startWithAudioOn: false` — and does not resolve until the user answers the browser prompt. Pipecat opens the recorder whenever it initialises, so there is no WebSocket session without the prompt. Request access from a user gesture before connecting. For text with no microphone at all, use the SSE transport.

Leave `startWithAudioOn` unset on the WebSocket transport only when the page may start listening as soon as it connects. Muting through `audioControls` on this transport disables the local audio track, so Convai receives silence.

## Differences from the LiveKit transport

| Behaviour | `"livekit"` | `"websocket"` |
|---|---|---|
| `uploadFile()` | Supported | Not supported. It requires a LiveKit room and throws `[ConvaiClient] uploadFile: not connected to a LiveKit room` without one. |
| Ready-signal timeout | `error` fires with `bot-ready not received within 45000ms` if the character never signals readiness | No timeout; the WebSocket session reports readiness itself. |
| Bot audio | Played through the room by `AudioRenderer` or `ConvaiWidget` | Delivered on `botAudioTrack` |
| Vision frames | Video tracks published to the room | Sent over the WebSocket only when `enableVideo` is `true` and `visionInputConfig.enabled` is not `false` |
| `client.room` | The connected LiveKit room | Present but never connected |

## Troubleshooting

### Connect fails because the transport is not registered

**Symptom:** `connect()` rejects with this error:

```text
[ConvaiClient] WebSocket transport is not registered. Add `import '@convai/web-sdk/vanilla/websocket'` before calling connect().
```

**Cause:** The configuration sets `transport: 'websocket'`, but no module imported `@convai/web-sdk/vanilla/websocket`.

**Fix:** Add the side-effect import to a module that loads before `connect()` runs.

**Verify:** `connect()` resolves and `botReady` fires.

### Connect fails without a WebSocket URL

**Symptom:** `connect()` rejects with `No WebSocket URL returned from /connect endpoint (expected room_url)`.

**Cause:** Convai returned a `/connect` response without a `room_url`.

**Fix:** Check that the `url` option points at a Convai realtime endpoint that supports the WebSocket transport, or remove `url` to use the default.

**Verify:** `connect()` resolves.

### The connection closes during connect

**Symptom:** `connect()` rejects with `WebSocket disconnected before connect completed`.

**Cause:** The WebSocket closed before the transport reported that it was connected.

**Fix:** Retry the connection, and check network rules that block WebSocket traffic to Convai.

**Verify:** `connect()` resolves.

## Next steps

{% content-ref url="error-handling.md" %}
[Handle errors and disconnects](error-handling.md)
{% endcontent-ref %}

{% content-ref url="event-reference.md" %}
[Web SDK event reference](event-reference.md)
{% endcontent-ref %}

{% content-ref url="vanilla-typescript/best-practices-and-type-definitions.md" %}
[Configuration and type reference](vanilla-typescript/best-practices-and-type-definitions.md)
{% endcontent-ref %}
