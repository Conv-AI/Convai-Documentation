---
description: >-
  A summary of recommended patterns and the main TypeScript types for quick
  reference.
---

# Best Practices & Type Definitions

## Best Practices

### 1. Check connection before sending messages

```ts
if (client.state.isConnected) {
  client.sendUserTextMessage('Hello');
}
```

### 2. Handle errors

```ts
try {
  await client.connect(config);
} catch (err) {
  console.error('Connection failed', err);
}
```

### 3. Unsubscribe from events when needed

```ts
const off = client.on('message', handler);
off();
```

### 4. Disconnect on cleanup

```ts
window.addEventListener('beforeunload', () => {
  client.disconnect();
});
```

### 5. Keep UI responsive with stateChange

```ts
client.on('stateChange', updateUI);
```

***

## **Core Types:**

```typescript
import type {
  ConvaiClient,
  ConvaiConfig,
  ConvaiClientState,
  ChatMessage,
  IConvaiClient,
} from '@convai/web-sdk';
```

**Control Interfaces:**

```typescript
import type {
  AudioControls,
  VideoControls,
  ScreenShareControls,
} from '@convai/web-sdk';
```

**Lipsync Types:**

```typescript
import type {
  BlendshapeQueue,
  BlendshapeMapper,
  BlendshapeFormat,
  BlendshapeMappingConfig,
  BlendshapeNameMapping,
  OptimizedBlendshapeOutput,
} from '@convai/web-sdk';
```

**Configuration Interface:**

```typescript
interface ConvaiConfig {
  apiKey: string;                    // Required: Your API key
  characterId: string;                // Required: Character ID
  endUserId?: string;                 // Optional: For memory & analytics
  url?: string;                       // Optional: Custom API endpoint
  enableVideo?: boolean;              // Enable video/screenshare (default: false)
  startWithVideoOn?: boolean;         // Start with camera on (default: false)
  startWithAudioOn?: boolean;         // Start with mic on (default: false)
  ttsEnabled?: boolean;               // Enable TTS (default: true)
  enableLipsync?: boolean;            // Enable blendshapes (default: false)
  blendshapeConfig?: {
    format?: 'arkit' | 'mha';         // Blendshape format (default: 'mha')
  };
  actionConfig?: {                    // Optional: Character actions
    actions: string[];
    characters: Array<{ name: string; bio: string }>;
    objects: Array<{ name: string; description: string }>;
    currentAttentionObject?: string;
  };
}
```

***

## Client State Management

The `ConvaiClientState` interface provides complete visibility into the conversation state:

```typescript
interface ConvaiClientState {
  isConnected: boolean;     // Connected to character
  isConnecting: boolean;    // Connection in progress
  isListening: boolean;     // Listening to user
  isThinking: boolean;      // Processing response
  isSpeaking: boolean;      // Character speaking
  agentState: string;       // Combined state
}
```

**Agent State Values:**

* `'disconnected'` - Not connected
* `'connected'` - Connected but idle
* `'listening'` - Actively listening to user
* `'thinking'` - Processing user input
* `'speaking'` - Character is responding

**Usage:**

```typescript
// React
const { state } = convaiClient;
if (state.isSpeaking) {
  console.log('Character is speaking');
}

// Vanilla
client.on('stateChange', (state) => {
  console.log('State:', state.agentState);
});
```

***

## Event System

The SDK uses an event-driven architecture for state changes and messages:

**Available Events:**

| Event                     | Parameters                   | Description                       |
| ------------------------- | ---------------------------- | --------------------------------- |
| `stateChange`             | `(state: ConvaiClientState)` | Connection/activity state changed |
| `message`                 | `(message: ChatMessage)`     | New message received              |
| `messagesChange`          | `(messages: ChatMessage[])`  | Message history updated           |
| `connect`                 | `()`                         | Successfully connected            |
| `disconnect`              | `()`                         | Disconnected from character       |
| `error`                   | `(error: Error)`             | Error occurred                    |
| `botReady`                | `()`                         | Bot is ready to receive messages  |
| `userTranscriptionChange` | `(transcription: string)`    | User speech transcription updated |

**Usage:**

```typescript
// Subscribe to events
const unsubscribe = client.on('stateChange', (state) => {
  console.log('State changed:', state);
});

// Unsubscribe
unsubscribe();

// Or manually
client.off('stateChange', callback);
```
