---
description: >-
  useConvaiClient manages all Convai connection logic, audio/video pipelines,
  and message flows.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/web-plugins/convai-web-sdk-beta/react/useconvaiclient-hook
---

# useConvaiClient Hook

## Configuration

```tsx
interface ConvaiConfig {
  apiKey: string;
  characterId: string;
  endUserId?: string;
  url?: string;
  enableVideo?: boolean;
  startWithVideoOn?: boolean;
  ttsEnabled?: boolean;
  actionConfig?: {
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
