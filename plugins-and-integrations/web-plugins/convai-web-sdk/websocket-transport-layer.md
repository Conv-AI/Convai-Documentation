---
title: Use the WebSocket transport
description: Connect a Convai character over a WebSocket instead of WebRTC, register the transport, and hear the character's voice in React or plain TypeScript.
last_reviewed: "2.0.2"
icon: webhook
---

Switch a Convai Web SDK session from the default WebRTC transport, built on LiveKit, to a WebSocket transport built on Pipecat. Use this page when your deployment cannot use WebRTC or when you are testing the WebSocket path.

{% hint style="info" %}
Use version 1.9.2 or later on hosted Convai. Hosted Convai's `/connect` returns a `ws://` URL for this transport, but the endpoint accepts only `wss://`. Version 1.9.1 and earlier fail to connect, and the browser reports close code `1006`. Version 1.9.2 upgrades `ws://` to `wss://` when the `/connect` URL or the page uses https; a local http setup keeps `ws://`.
{% endhint %}

## How the transport is selected

`ConvaiConfig.transport` takes `"livekit"` (the default) or `"websocket"`. Both transports start with the same `POST /connect` request to Convai. With `"websocket"`, the SDK reads the WebSocket URL from the `room_url` field of the response and opens it through a registered WebSocket session.

The WebSocket session is not built into `ConvaiClient`. Only the `@convai/web-sdk/vanilla/websocket` subpath imports the Pipecat packages, and importing it registers the session with `ConvaiClient` as a side effect. An application that never imports that subpath does not load Pipecat code.

## Install the Pipecat packages

The WebSocket session runs on two Pipecat packages. They are optional peer dependencies of the SDK, so your package manager does not install them for you. Add them next to the SDK:

```bash
npm install @convai/web-sdk @pipecat-ai/client-js @pipecat-ai/websocket-transport
```

Without them, importing `@convai/web-sdk/vanilla/websocket` fails with `Could not resolve "@pipecat-ai/client-js"`.

## Register the transport and connect

Import `@convai/web-sdk/vanilla/websocket` once, before `connect()` runs, and set `transport: 'websocket'`. React applications import the same subpath; the package has no React-specific WebSocket entry point.

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import '@convai/web-sdk/vanilla/websocket';
import { useConvaiClient } from '@convai/web-sdk/react';
import { ConvaiWidget } from '@convai/web-widget/react';

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
import { ConvaiClient } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  transport: 'websocket',
});

await client.connect();
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Play the character's voice

The transport plays the voice; no wiring is needed. Pipecat's WebSocket transport plays the character's audio through its own Web Audio player, straight to the speakers, in React and plain TypeScript alike. The examples above are complete: they need no `AudioRenderer` and no `botAudioTrack` listener.

The `botAudioTrack` event does not fire on this transport. The Pipecat transport exposes only the local microphone track, so there is no character track to attach. Any `botAudioTrack` listener or `AudioRenderer` you keep from older code is harmless; it never receives a track.

To silence the character, call `setCharacterMuted(true)`. On the WebSocket transport this needs version 1.9.2 or later, and speech made while muted is dropped, not queued. See [Mute the character's voice](mute-the-characters-voice.md).

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
| Bot audio | Played through the room by `AudioRenderer` or `ConvaiWidget` | Played by the Pipecat transport itself; `botAudioTrack` does not fire |
| Time to `botReady` | About 4 to 7 seconds in our tests | About 17 to 21 seconds in our tests |
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

### The connection closes with code 1006 on hosted Convai

**Symptom:** The WebSocket closes during connect, and the browser reports close code `1006`.

**Cause:** Version 1.9.1 or earlier opened the `ws://` URL that hosted Convai returns, and the endpoint accepts only `wss://`.

**Fix:** Upgrade `@convai/web-sdk` to 1.9.2 or later.

**Verify:** `connect()` resolves and `botReady` fires.

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
