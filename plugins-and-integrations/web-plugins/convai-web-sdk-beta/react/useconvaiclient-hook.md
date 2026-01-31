---
description: >-
  useConvaiClient manages all Convai connection logic, audio/video pipelines,
  and message flows.
---

# useConvaiClient Hook

## Configuration

```tsx
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

### Return Value

```tsx
const convaiClient = useConvaiClient(config);
```

### State

```tsx
convaiClient.state              // Connection + activity state
convaiClient.connectionType     // 'audio' | 'video' | null
convaiClient.isBotReady         // Bot ready for messages
convaiClient.chatMessages       // All conversation messages
convaiClient.userTranscription  // Live speech-to-text
```

### Connection Methods

```tsx
convaiClient.connect(config?)   
convaiClient.disconnect()
convaiClient.reconnect()
convaiClient.resetSession()
```

### Messaging

```tsx
convaiClient.sendUserTextMessage(text)
convaiClient.sendTriggerMessage(triggerName, message?)
convaiClient.updateTemplateKeys({ key: 'value' })
convaiClient.updateDynamicInfo({ text: 'context' })
```

### Controls

```tsx
convaiClient.audioControls
convaiClient.videoControls
convaiClient.screenShareControls
convaiClient.toggleTts(enabled)
```

### Example: Manual Connect

```tsx
function App() {
  const convaiClient = useConvaiClient(); // No initial config

  const connect = () => convaiClient.connect({
    apiKey: 'your-api-key',
    characterId: 'your-character-id'
  });

  return <button onClick={connect}>Connect</button>;
}
```
