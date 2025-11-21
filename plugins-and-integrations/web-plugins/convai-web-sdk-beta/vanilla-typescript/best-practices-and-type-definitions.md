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

## Key Types

```ts
interface ConvaiConfig {
  apiKey: string;
  characterId: string;
  endUserId?: string;
  enableVideo?: boolean;
  startWithVideoOn?: boolean;
  ttsEnabled?: boolean;
  actionConfig?: ActionConfig;
}
```

```ts
interface ConvaiClientState {
  isConnected: boolean;
  isConnecting: boolean;
  isListening: boolean;
  isThinking: boolean;
  isSpeaking: boolean;
  agentState: 'disconnected' | 'listening' | 'thinking' | 'speaking';
}
```

```ts
interface ChatMessage {
  id: string;
  type:
    | 'user-transcription'
    | 'bot-llm-text'
    | 'bot-emotion'
    | 'action'
    | 'behavior-tree';
  content: string;
  timestamp: number;
}
```
