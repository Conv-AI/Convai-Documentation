---
description: Get a Convai character speaking in your app in under five minutes.
icon: forward-fast
---

# Quickstart

### Prerequisites

* A Convai account with an API key — get one at [convai.com](https://convai.com)
* A Character ID from your Convai dashboard
* Node.js 18+ and a React project (Vite, Next.js, or CRA)

### Install

```bash
npm install @convai/web-sdk
```

### Your first conversation (React)

This is the minimum code to connect to a character and exchange text messages.

```tsx
import { useConvaiClient } from '@convai/web-sdk';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    // Recommended: a stable id per end user. It keys the character's
    // long-term memory for that person across sessions.
    endUserId: 'user-123',
  });

  const handleConnect = async () => {
    try {
      await client.connect();
    } catch (err) {
      // connect() rejects with a server reason — surface it, don't swallow it.
      // e.g. "LTM speaker limit reached" means this API key hit its
      // long-term-memory speaker cap for new endUserIds.
      console.error('Connect failed:', err);
    }
  };

  const handleSend = () => {
    client.sendUserTextMessage('Hello! Who are you?');
  };

  return (
    <div>
      <p>Status: {client.activity}</p>

      {!client.state.isConnected ? (
        <button onClick={handleConnect}>Connect</button>
      ) : (
        <button onClick={handleSend}>Say hello</button>
      )}

      <ul>
        {client.chatMessages
          .filter(m => m.type === 'bot-output' || m.type === 'user-llm-text')
          .map(m => (
            <li key={m.id}>
              <strong>{m.type.startsWith('user') ? 'You' : 'Bot'}:</strong> {m.content}
            </li>
          ))}
      </ul>
    </div>
  );
}
```

#### What this does

1. `useConvaiClient` creates a persistent client instance and wires up React state.
2. `client.connect()` opens a WebRTC session. The character is ready once `client.isBotReady` is `true`.
3. `client.sendUserTextMessage` sends text to the character; responses arrive as `chatMessages`.
4. `client.activity` is a string showing the current state: `"Idle"`, `"Connecting..."`, `"Connected"`, `"Listening"`, `"Thinking"`, or `"Speaking"`.

### Drop-in widget

If you want a fully built chat UI (voice + text), use `ConvaiWidget`:

```tsx
import { useConvaiClient } from '@convai/web-sdk';
import { ConvaiWidget } from '@convai/web-sdk/react';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    startWithAudioOn: false, // ask for mic permission only when user enters voice mode
  });

  return <ConvaiWidget convaiClient={client} />;
}
```

The widget handles connection, microphone, voice mode, and message display out of the box.

### Add a talking 3D character

Two config lines turn on the facial-animation stream for a 3D avatar:

```tsx
const client = useConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableLipsync: true,
  blendshapeConfig: { format: 'mha' }, // 'mha' (MetaHuman 251) or 'arkit' (61)
});

// client.blendshapeQueue now buffers per-frame blendshape values,
// synchronized with the bot's speech — feed them to your renderer.
```

See Lipsync & Blendshapes for the render-loop integration, character mapping, and the patterns that make it feel natural (fades, blink ownership, per-channel gains). The `examples/react-three-fiber` demo is a complete, production-style reference: a MetaHuman-style character in a lit room with lipsync, procedural blink/gaze/head tracking, body animation, SDK-driven actions, and a scripted intro scene.

### Troubleshooting first connects

| Symptom                                              | Cause / fix                                                                                                                                                          |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `connect()` rejects with `LTM speaker limit reached` | The API key hit its long-term-memory speaker cap; reuse an existing `endUserId` or raise the limit in the dashboard.                                                 |
| Character connects but stays silent on triggers      | `sendTriggerMessage` resolves triggers by their **dashboard name** (e.g. `'Welcome'`), not the trigger's UUID — an unknown name is silently ignored.                 |
| No blendshape frames                                 | `enableLipsync: true` missing, or the widget/session was started before the config change — reload after config edits.                                               |
| Duplicate/garbled bot text in a custom chat UI       | Render `bot-llm-text` messages; `bot-output` events are TTS progress ticks (same `segment_id` re-sent per tick) — the SDK dedupes them in `chatMessages` since v1.5. |

### Vanilla JavaScript

No React? Use `ConvaiClient` directly:

```ts
import { ConvaiClient } from '@convai/web-sdk/core';
import { AudioRenderer } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
});

// Play bot audio through speakers
const audio = new AudioRenderer(client.room);

client.on('botReady', () => {
  console.log('Character is ready');
  client.sendUserTextMessage('Hello!');
});

client.on('message', (msg) => {
  if (msg.type === 'bot-output') {
    console.log('Bot:', msg.content);
  }
});

await client.connect();
```

### Next steps

* Configuration reference — all `ConvaiConfig` options
* React integration — hooks, widget, custom UI
* Lipsync & blendshapes — drive a 3D character's face
* Actions & triggers — let the character act, and script beats with `sendTriggerMessage`
* Events reference — every event the client emits
* Voice & audio controls — mic, camera, screen share
