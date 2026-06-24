---
description: >-
  Subscribe with `client.on(event, callback)`. The return value is an
  unsubscribe function.
icon: arrow-up-small-big
---

# Event Reference

```ts
const unsub = client.on('botReady', () => {
  console.log('Bot is ready');
});

// Later
unsub();
// or
client.off('botReady', handler);
```

***

### Connection events

#### `connect`

Fires when the WebRTC/WebSocket transport connects. The bot may not be ready yet — wait for `botReady` before sending messages.

```ts
client.on('connect', () => {
  console.log('Transport connected');
});
```

#### `botReady`

Fires when the character has confirmed it is ready to receive messages. This is the correct signal to start interacting.

```ts
client.on('botReady', () => {
  client.sendUserTextMessage('Hello!');
});
```

#### `disconnect`

Fires when the session ends. Receives a `DisconnectReason` code.

```ts
client.on('disconnect', (reason) => {
  // reason: number (see DisconnectReason)
  // 1 = CLIENT_INITIATED (intentional), others may warrant reconnection
  if (reason !== 1) {
    client.reconnect();
  }
});
```

#### `stateChange`

Fires whenever any part of `ConvaiClientState` changes. Use this for UI updates.

```ts
client.on('stateChange', (state) => {
  // state.isConnected, state.isConnecting, state.isListening,
  // state.isThinking, state.isSpeaking, state.agentState,
  // state.emotion, state.endUserId, state.metrics, state.disconnectReason
  updateUI(state);
});
```

#### `error`

Fires on connection errors or bot-ready timeout.

```ts
client.on('error', (error: Error) => {
  console.error(error.message);
});
```

***

### Conversation events

#### `conversationStart`

Fires when a new conversation turn begins — either when the user sends a text message or starts speaking.

```ts
client.on('conversationStart', ({ sessionId, userMessage, timestamp }) => {
  // sessionId: incrementing turn counter
  // userMessage: text sent, or "[voice]" for voice turns
  // timestamp: Date.now() value
  console.log(`Turn ${sessionId} started`);
});
```

#### `turnEnd`

Fires when the bot finishes speaking for a turn.

```ts
client.on('turnEnd', ({ sessionId, duration, timestamp }) => {
  // duration: seconds the bot spoke
  console.log(`Turn ${sessionId} lasted ${duration}s`);
});
```

#### `message`

Fires for each new `ChatMessage` added to the conversation. The full history is also available in `client.chatMessages`.

```ts
client.on('message', (msg) => {
  // msg.type, msg.content, msg.id, msg.timestamp, msg.isStreaming
  if (msg.type === 'bot-output') {
    display(msg.content);
  }
});
```

#### `messagesChange`

Fires whenever the message array changes (includes message updates mid-stream).

```ts
client.on('messagesChange', (messages) => {
  renderHistory(messages);
});
```

#### `userTranscriptionChange`

Fires repeatedly as the user speaks, providing live speech-to-text.

```ts
client.on('userTranscriptionChange', (text) => {
  showLiveTranscript(text);
});
```

***

### Speaking events

#### `speakingChange`

Fires when the bot starts or stops speaking.

```ts
client.on('speakingChange', (isSpeaking) => {
  if (isSpeaking) {
    startLipsyncAnimation();
  } else {
    stopLipsyncAnimation();
  }
});
```

#### `botOutput`

Fires for each aggregated output chunk from the bot. Includes both spoken and unspoken text.

```ts
client.on('botOutput', ({ text, spoken, aggregatedBy }) => {
  // spoken: true when the TTS engine will read this text aloud
  // aggregatedBy: "sentence" or "word" indicating chunk granularity
  if (spoken) {
    addToSubtitles(text);
  }
});
```

#### `botTtsStarted`

Fires when the TTS engine starts producing audio.

```ts
client.on('botTtsStarted', () => {
  showSpeakingIndicator();
});
```

#### `botTtsStopped`

Fires when the TTS engine finishes.

```ts
client.on('botTtsStopped', () => {
  hideSpeakingIndicator();
});
```

#### `botTtsText`

Fires word-by-word as the bot speaks, synchronized with TTS audio.

```ts
client.on('botTtsText', ({ text }) => {
  highlightWord(text); // karaoke-style word highlighting
});
```

***

### Microphone events

#### `userMuteStarted`

Fires when the server-side mutes the user's microphone (e.g., when the bot starts speaking to prevent echo).

```ts
client.on('userMuteStarted', () => {
  showMicMutedIndicator();
});
```

#### `userMuteStopped`

Fires when the server un-mutes the user's microphone.

```ts
client.on('userMuteStopped', () => {
  hideMicMutedIndicator();
});
```

***

### Blendshape / lipsync events

These require `enableLipsync: true` in config.

#### `blendshapes`

Fires for each incoming blendshape chunk (10 frames by default). Use `client.blendshapeQueue` instead of handling raw chunks directly.

```ts
client.on('blendshapes', (data) => {
  // Low-level: raw chunk data before queue processing
});
```

#### `blendshapeStatsReceived`

Fires when the server sends end-of-turn blendshape statistics. Signals that no more frames are coming for this turn.

```ts
client.on('blendshapeStatsReceived', (stats) => {
  // stats.total_blendshapes, stats.total_audio_duration_ms
});
```

***

### Action events

Requires `actionConfig` in config.

#### `actionResponse`

Fires after each bot turn with the actions the bot decided to perform.

```ts
client.on('actionResponse', ({ actions }) => {
  for (const { name, target } of actions) {
    executeAction(name, target);
  }
});
```

See Actions for the complete guide.

***

### Server response events

#### `serverResponse`

Fires as an acknowledgment for every message you send to the server.

```ts
client.on('serverResponse', (response) => {
  // response.event_type: the message type you sent
  // response.status: "success" | "error" | "processing" | "pending"
  // response.message: human-readable result
  // response.extras: event-specific data (e.g., token counts for context-update)
  if (response.status === 'error') {
    console.error(`Server error on ${response.event_type}:`, response.message);
  }
});
```

#### `interactionCreated`

Fires early in the session lifecycle — before `botReady` — when the server assigns a unique interaction ID. This is the first message that carries both `interactionId` and `characterSessionId`, making it the right place to capture identifiers for analytics, logging, or session resumption.

```ts
client.on('interactionCreated', ({ interactionId, characterSessionId }) => {
  console.log('Interaction ID:', interactionId);       // e.g. "int_abc123def456"
  console.log('Character session:', characterSessionId); // e.g. "cs_xyz789"

  // Store for analytics / logging
  analytics.track('conversation_started', {
    interactionId,
    characterSessionId,
    timestamp: Date.now(),
  });
});
```

| Field                | Type     | Description                                                                            |
| -------------------- | -------- | -------------------------------------------------------------------------------------- |
| `interactionId`      | `string` | Unique identifier for this interaction. Use for analytics or log correlation.          |
| `characterSessionId` | `string` | Character session identifier. Same value as `client.characterSessionId` after connect. |

`interactionCreated` fires once per `connect()` call. If you reconnect, a new `interactionId` is issued.

***

### Session events

#### `idleWarning`

Fires before the server disconnects an idle session.

```ts
client.on('idleWarning', ({ remainingSeconds }) => {
  if (remainingSeconds !== null) {
    showWarning(`Session will close in ${remainingSeconds}s`);
  }
  // Reset the timer on any user activity
  client.resetIdleTimer();
});
```

#### `llmNoResponse`

Fires when the LLM deliberately chose not to respond (e.g., because the input didn't warrant a reply).

```ts
client.on('llmNoResponse', () => {
  // No response will arrive for this turn — update UI accordingly
  hideThinkingIndicator();
});
```

***

#### `metrics`

Fires with performance data after each turn.

```ts
client.on('metrics', (data) => {
  // Raw metrics from the server (latency, token counts, etc.)
  console.log('Turn metrics:', data);
});
```

***

### Audio track (WebSocket transport)

#### `botAudioTrack`

Fires when a new audio track is available from the bot (WebSocket transport only). Attach to an `<audio>` element to play.

```ts
client.on('botAudioTrack', (track: MediaStreamTrack) => {
  const audio = document.querySelector<HTMLAudioElement>('#bot-audio')!;
  audio.srcObject = new MediaStream([track]);
});
```

***

### Event quick-reference

| Event                     | Payload                                 | When                           |
| ------------------------- | --------------------------------------- | ------------------------------ |
| `connect`                 | —                                       | Transport connected            |
| `botReady`                | —                                       | Bot confirmed ready            |
| `disconnect`              | `DisconnectReason`                      | Session ended                  |
| `stateChange`             | `ConvaiClientState`                     | Any state change               |
| `error`                   | `Error`                                 | Connection or timeout error    |
| `conversationStart`       | `{ sessionId, userMessage, timestamp }` | New turn begins                |
| `turnEnd`                 | `{ sessionId, duration, timestamp }`    | Bot finishes speaking          |
| `message`                 | `ChatMessage`                           | New message                    |
| `messagesChange`          | `ChatMessage[]`                         | History updated                |
| `userTranscriptionChange` | `string`                                | Live STT update                |
| `speakingChange`          | `boolean`                               | Bot speaking state             |
| `botOutput`               | `{ text, spoken, aggregatedBy }`        | Aggregated bot chunk           |
| `botTtsStarted`           | —                                       | TTS begins                     |
| `botTtsStopped`           | —                                       | TTS ends                       |
| `botTtsText`              | `{ text }`                              | Word-by-word TTS               |
| `userMuteStarted`         | —                                       | Server muted user mic          |
| `userMuteStopped`         | —                                       | Server un-muted user mic       |
| `blendshapes`             | raw data                                | Blendshape chunk               |
| `blendshapeStatsReceived` | stats                                   | Turn end stats                 |
| `actionResponse`          | `{ actions }`                           | Bot action decisions           |
| `serverResponse`          | `ServerResponse`                        | Server acknowledgment          |
| `interactionCreated`      | `{ interactionId, characterSessionId }` | Session ID assigned            |
| `idleWarning`             | `{ remainingSeconds }`                  | Idle timeout warning           |
| `llmNoResponse`           | —                                       | LLM chose not to respond       |
| `metrics`                 | data                                    | Turn performance data          |
| `botAudioTrack`           | `MediaStreamTrack`                      | New audio track (WS transport) |
