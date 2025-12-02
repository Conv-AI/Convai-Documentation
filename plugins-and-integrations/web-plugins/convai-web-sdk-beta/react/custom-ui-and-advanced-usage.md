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

### Message Types

Common message types in `convaiClient.chatMessages`:

```ts
type ChatMessageType =
  | "user"               // User's sent message (raw)
  | "user-transcription" // Real-time speech-to-text from user
  | "user-llm-text"      // Final user text processed by LLM
  | "convai"             // Raw character message
  | "bot-llm-text"       // Character’s LLM-generated text
  | "bot-emotion"        // Character’s emotion state
  | "emotion"            // Generic emotion message
  | "behavior-tree"      // Behavior tree / decision output
  | "action"             // Action execution
  | "interrupt-bot";     // Interrupt message
```

For chat UIs, you usually show only:

```ts
const displayMessages = chatMessages.filter(
  (msg) => msg.type === "user-llm-text" || msg.type === "bot-llm-text"
);
```

***

## Best Practices

1. Use a **single** `useConvaiClient()` per application.
2. Always check `state.isConnected` before sending messages.
3. Call `resetSession()` when switching scenes or flows.
4. Use `<AudioRenderer />` for custom UIs.
5. Provide `endUserId` in production for memory and analytics.
6. Wrap connect/disconnect in `try/catch`.
