---
description: ConvaiClient is the main class for managing Convai in vanilla TypeScript.
---

# ConvaiClient (Core API)

## Creating a Client

```ts
const client = new ConvaiClient();
```

You configure it when calling `connect()`.

***

## Connecting

```ts
await client.connect({
  apiKey: string,
  characterId: string,
  endUserId?: string,
  url?: string,
  enableVideo?: boolean,
  startWithVideoOn?: boolean,
  ttsEnabled?: boolean,
  actionConfig?: {
    actions: string[];
    characters: Array<{ name: string; bio: string }>;
    objects: Array<{ name: string; description: string }>;
    currentAttentionObject?: string;
  }
});
```

***

## Connection Methods

```ts
await client.disconnect();
await client.reconnect(); // Uses last provided config
client.resetSession();    // Clears history
```

***

## Messaging

```ts
client.sendUserTextMessage('Hello');
client.sendTriggerMessage('greet_user', 'Optional payload');

client.updateTemplateKeys({ user: 'Alex' });
client.updateDynamicInfo({ text: 'User is on the blog page' });

client.toggleTts(true);  // Enable/disable TTS
```

***

## Media Controls

All controls are async.

```ts
// Audio
await client.audioControls.toggleAudio();
await client.audioControls.muteAudio();
await client.audioControls.unmuteAudio();
await client.audioControls.setAudioDevice('device-id');

// Video
await client.videoControls.toggleVideo();
await client.videoControls.enableVideo();
await client.videoControls.disableVideo();

// Screen share
await client.screenShareControls.toggleScreenShare();
```

***

## Core Properties

```ts
client.state                 // Connection + activity state
client.connectionType        // 'audio' | 'video' | null
client.isBotReady            // Bot ready for messages

client.chatMessages          // Array of ChatMessage
client.userTranscription     // Live speech-to-text
client.characterSessionId    // Session ID

client.room       
```
