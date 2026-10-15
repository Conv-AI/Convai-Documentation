---
title: Build a custom UI in React
description: Replace the prebuilt widget with your own React components for messages and controls while the Convai Web SDK keeps handling audio and state.
last_reviewed: "2.0.0"
---

Build your own conversation interface in React on top of `useConvaiClient` instead of rendering `ConvaiWidget`. Use this page when the widget's layout does not fit your app. At the end, your components show the conversation, send text, and control the microphone, camera, and screen share.

## Prerequisites

- A React app with the Convai Web SDK installed. See [Get started with React](README.md).
- One `useConvaiClient` call for the conversation. Create the client once, near the top of the tree, and pass it down; each call to the hook creates a separate client with its own connection.

## Play the character's audio

Without the widget, nothing plays the character's voice on the default LiveKit transport. Render `AudioRenderer` inside `AudioContext.Provider` with the client's room.

{% code title="src/App.tsx" %}
```tsx
import { useConvaiClient } from '@convai/web-sdk/react';
import { AudioRenderer, AudioContext } from '@convai/web-widget/react';
import { Conversation } from './Conversation';

export default function App() {
  const convaiClient = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
  });

  return (
    <AudioContext.Provider value={convaiClient.room}>
      <AudioRenderer />
      <Conversation convaiClient={convaiClient} />
    </AudioContext.Provider>
  );
}
```
{% endcode %}

`AudioRenderer` and `AudioContext` from `@convai/web-widget/react` are LiveKit's `RoomAudioRenderer` and `RoomContext` under SDK names. `AudioContext` here is not the browser's Web Audio `AudioContext`; import it under another name if the same file also uses Web Audio.

With `transport: "websocket"`, the Pipecat transport plays the voice itself through Web Audio, and `AudioRenderer` is not needed.

## Render the messages

`chatMessages` holds every message type the SDK records. For a chat view, keep the user's typed text and transcribed speech and the character's text.

{% code title="src/Conversation.tsx" %}
```tsx
import { useState } from 'react';
import type { useConvaiClient } from '@convai/web-sdk/react';

type Client = ReturnType<typeof useConvaiClient>;

const SHOWN = new Set(['user-llm-text', 'user-transcription', 'bot-llm-text', 'bot-output']);

export function Conversation({ convaiClient }: { convaiClient: Client }) {
  const [text, setText] = useState('');
  const canSend = convaiClient.state.isConnected && convaiClient.isBotReady;

  const send = () => {
    if (!text.trim() || !canSend) return;
    convaiClient.sendUserTextMessage(text);
    setText('');
  };

  return (
    <div>
      {!convaiClient.state.isConnected && (
        <button onClick={() => convaiClient.connect()}>Connect</button>
      )}

      <ul>
        {convaiClient.chatMessages
          .filter((m) => SHOWN.has(m.type) && m.content.trim())
          .map((m) => (
            <li key={m.id} className={m.type.startsWith('user') ? 'user' : 'character'}>
              {m.content}
            </li>
          ))}
      </ul>

      <p>{convaiClient.userTranscription}</p>

      <input value={text} onChange={(e) => setText(e.target.value)} disabled={!canSend} />
      <button onClick={send} disabled={!canSend}>Send</button>

      <Controls convaiClient={convaiClient} />
    </div>
  );
}
```
{% endcode %}

| Type | Contains |
|---|---|
| `user-llm-text` | Text you sent with `sendUserTextMessage`, added locally when you send it. |
| `user-transcription` | Final transcription of your speech. The live, partial transcription is in `userTranscription`. |
| `bot-llm-text` | The character's reply, streamed. `isStreaming` is `true` until the reply is complete. |
| `bot-output` | The character's spoken text, recorded when no `bot-llm-text` message carries the reply. |

The full list of message types is in the [Configuration and type reference](../vanilla-typescript/best-practices-and-type-definitions.md).

## Add media controls

The control objects are not React state, so their fields, such as `audioControls.isAudioMuted`, do not re-render your component when they change. Read the hook's reactive `isAudioMuted`, `isVideoEnabled`, and `isScreenShareActive` instead, and call the control methods to change them.

{% code title="src/Controls.tsx" %}
```tsx
import type { useConvaiClient } from '@convai/web-sdk/react';

type Client = ReturnType<typeof useConvaiClient>;

export function Controls({ convaiClient }: { convaiClient: Client }) {
  const { audioControls, videoControls, screenShareControls } = convaiClient;
  const hasVideo = convaiClient.connectionType === 'video';

  return (
    <>
      <button onClick={() => audioControls.toggleAudio()}>
        {convaiClient.isAudioMuted ? 'Unmute' : 'Mute'}
      </button>

      {hasVideo && (
        <button onClick={() => videoControls.toggleVideo()}>
          {convaiClient.isVideoEnabled ? 'Stop camera' : 'Start camera'}
        </button>
      )}

      {hasVideo && (
        <button onClick={() => screenShareControls.toggleScreenShare()}>
          {convaiClient.isScreenShareActive ? 'Stop sharing' : 'Share screen'}
        </button>
      )}
    </>
  );
}
```
{% endcode %}

The control methods return promises and can reject, for example when the browser denies microphone or camera access. Camera and screen share require a connection made with `enableVideo: true`.

## Verify the custom UI

Select **Connect**, wait for the input to enable, and send a message.

{% hint style="success" %}
Your message appears in the list, the character's reply streams in below it, and you hear the character's voice.
{% endhint %}

## Next steps

{% content-ref url="useconvaiclient-hook.md" %}
[useConvaiClient hook reference](useconvaiclient-hook.md)
{% endcontent-ref %}

{% content-ref url="../event-reference.md" %}
[Web SDK event reference](../event-reference.md)
{% endcontent-ref %}

{% content-ref url="../error-handling.md" %}
[Handle errors and disconnects](../error-handling.md)
{% endcontent-ref %}

{% content-ref url="audio-visualizer-optional.md" %}
[Add an audio visualizer in React](audio-visualizer-optional.md)
{% endcontent-ref %}
