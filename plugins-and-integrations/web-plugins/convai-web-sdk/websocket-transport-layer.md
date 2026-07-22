---
description: >-
  The SDK defaults to WebRTC for real-time voice conversations. In environments
  where WebRTC is unavailable, you can opt in to a WebSocket-based transport
  instead.
icon: webhook
---

# WebSocket Transport Layer

WebSocket transport is useful in mobile webviews with WebRTC restrictions, corporate networks that block UDP, or any platform where WebRTC is unsupported. It uses Pipecat under the hood and is fully opt-in — the pipecat packages are never bundled unless you explicitly import the transport subpath.

***

### When to use WebSocket transport

| Situation                                | Recommendation                                         |
| ---------------------------------------- | ------------------------------------------------------ |
| Standard web app                         | WebRTC (default) — lower latency, better audio quality |
| Mobile webview with WebRTC restrictions  | WebSocket                                              |
| Corporate network blocking UDP/STUN/TURN | WebSocket                                              |
| Bundle must not include `@pipecat-ai`    | WebRTC (default — no extra import needed)              |
| Fallback or testing path                 | WebSocket                                              |

***

### Setup

The WebSocket transport is **opt-in**. The pipecat packages (`@pipecat-ai/client-js`, `@pipecat-ai/websocket-transport`) are never bundled unless you explicitly import the transport subpath.

#### React

```tsx
// 1. Register the transport — must be imported before connect() is called
import '@convai/web-sdk/vanilla/websocket';

import { useConvaiClient, ConvaiWidget } from '@convai/web-sdk/react';

export default function App() {
  const client = useConvaiClient({
    apiKey: '...',
    characterId: '...',
    transport: 'websocket',
  });

  return <ConvaiWidget convaiClient={client} />;
}
```

#### Vanilla JS

```ts
// 1. Register the transport
import '@convai/web-sdk/vanilla/websocket';

import { ConvaiClient } from '@convai/web-sdk/vanilla';
import { createConvaiWidget } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: '...',
  characterId: '...',
  transport: 'websocket',
});

createConvaiWidget(document.body, { convaiClient: client as any });
```

The import order matters — register before constructing the client.

***

### Bundle isolation

`ConvaiClient` itself contains zero pipecat imports. The WebSocket implementation lives entirely in the `@convai/web-sdk/vanilla/websocket` subpath. A bundler (Vite, webpack, Rollup) that sees no import of that subpath will not include `@pipecat-ai/client-js` or `@pipecat-ai/websocket-transport` in any chunk.

```
@convai/web-sdk/vanilla         → zero pipecat code
@convai/web-sdk/react           → zero pipecat code
@convai/web-sdk/vanilla/websocket → pipecat code (opt-in only)
```

If you call `connect()` with `transport: "websocket"` without importing the subpath first, the SDK throws a clear error:

```
[ConvaiClient] WebSocket transport is not registered.
Add `import '@convai/web-sdk/vanilla/websocket'` before calling connect().
```

***

### Feature comparison

| Feature                | WebRTC (default) | WebSocket          |
| ---------------------- | ---------------- | ------------------ |
| Works without UDP      | ✗                | ✓                  |
| Requires `@pipecat-ai` | ✗                | ✓ (opt-in subpath) |
| Mobile webview support | Varies           | Better             |

{% hint style="info" %}
File upload for websocket transport layer: coming soon
{% endhint %}

***

### Microphone behaviour

On WebRTC, the microphone is activated explicitly via `audioControls.enableAudio()` or the `startWithAudioOn` config flag.

On WebSocket, the Pipecat transport initialises the audio stream during `connect()`. The SDK defaults to mic-on at connection time and mutes immediately if `startWithAudioOn: false`:

```ts
// Mic starts muted — user unmutes via the widget or audioControls
const client = new ConvaiClient({
  transport: 'websocket',
  startWithAudioOn: false,
  ...
});
```

***

### API reference

#### Config

| Field       | Type                       | Default     | Description                                                               |
| ----------- | -------------------------- | ----------- | ------------------------------------------------------------------------- |
| `transport` | `"livekit" \| "websocket"` | `"livekit"` | Default uses WebRTC; `"websocket"` opts in to Pipecat WebSocket transport |

#### Static method

```ts
import { ConvaiClient } from '@convai/web-sdk/vanilla';

// Called automatically by the websocket subpath import.
// Only needed if you are registering a custom WebSocket transport implementation.
ConvaiClient.registerWebSocketTransport(factory);
```

`registerWebSocketTransport` accepts a factory with signature:

```ts
(onMessage: (payload: Uint8Array) => void, enableMic: boolean) => IWebSocketSession
```

This lets you swap in a custom WebSocket session implementation if needed.
