---
description: Build your own UI while using Convai’s audio pipelines and message system.
---

# Custom UI & Advanced Usage

## Required for Custom UIs: AudioRenderer

If you don’t use the widget, include `AudioRenderer` so bot audio works.

```tsx
import { useConvaiClient, AudioRenderer, AudioContext } from '@convai/web-sdk';

function CustomApp() {
  const convaiClient = useConvaiClient({
    apiKey: 'your-api-key',
    characterId: 'your-character-id'
  });

  return (
    <AudioContext.Provider value={convaiClient.room}>
      <AudioRenderer />       {/* Required for audio playback */}
      <YourCustomUI />
    </AudioContext.Provider>
  );
}
```

***

## Custom Message List

```tsx
function Messages({ convaiClient }) {
  return convaiClient.chatMessages.map(msg => (
    <div key={msg.id} className={msg.type}>
      {msg.content}
    </div>
  ));
}
```

***

## Custom Controls

```tsx
function Controls({ convaiClient }) {
  const { audioControls, videoControls, screenShareControls } = convaiClient;

  return (
    <>
      <button onClick={audioControls.toggleAudio}>
        {audioControls.isAudioMuted ? 'Unmute' : 'Mute'}
      </button>

      <button onClick={videoControls.toggleVideo}>
        {videoControls.isVideoEnabled ? 'Stop Camera' : 'Start Camera'}
      </button>

      <button onClick={screenShareControls.toggleScreenShare}>
        {screenShareControls.isScreenShareActive ? 'Stop Sharing' : 'Share Screen'}
      </button>
    </>
  );
}
```

***

## Message Types

The SDK produces:

* `user` — User messages
* `user-transcription` — Live ASR
* `bot-llm-text` — Character text
* `bot-emotion` — Emotion signals
* `action` — Action triggers
* `behavior-tree` — Behavior responses

***

## Best Practices

1. Use a **single** `useConvaiClient()` per application.
2. Always check `state.isConnected` before sending messages.
3. Call `resetSession()` when switching scenes or flows.
4. Use `<AudioRenderer />` for custom UIs.
5. Provide `endUserId` in production for memory and analytics.
6. Wrap connect/disconnect in `try/catch`.
