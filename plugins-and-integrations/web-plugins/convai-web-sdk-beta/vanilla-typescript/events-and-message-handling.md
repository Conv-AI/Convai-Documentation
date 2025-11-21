---
description: >-
  ConvaiClient provides a strongly typed event system. Use client.on(event,
  handler) to subscribe.
---

# Events & Message Handling

## Events

### State Changes

```ts
client.on('stateChange', (state) => {
  console.log(state.agentState, state.isConnected);
});
```

### New Messages

```ts
client.on('message', (message) => {
  console.log('Message:', message.type, message.content);
});
```

### Messages Updated

```ts
client.on('messagesChange', (messages) => {
  console.log('Total messages:', messages.length);
});
```

### Real-time Transcription

```ts
client.on('userTranscriptionChange', (text) => {
  console.log('You said:', text);
});
```

### Lifecycle Events

```ts
client.on('connect', () => console.log('Connected'));
client.on('disconnect', () => console.log('Disconnected'));
client.on('botReady', () => console.log('Bot is ready'));
```

### Errors

```ts
client.on('error', (err) => {
  console.error('Convai error:', err);
});
```

***

## Message Types

Convai messages include:

* `user-transcription`
* `bot-llm-text`
* `bot-emotion`
* `action`
* `behavior-tree`

Only some are shown in UIs (usually transcription + bot text).

***

## Removing Listeners

```ts
const unsub = client.on('message', handler);
unsub(); // Remove listener
```
