---
title: Handle events and messages in TypeScript
description: Subscribe to connection, state, and message events from the Convai Web SDK client and render the conversation in a framework-free page.
last_reviewed: "1.9.2"
---

Subscribe to the client's events to keep a framework-free UI in step with the conversation. Use this page when you render state, messages, or live transcription yourself instead of using the chat widget.

## Prerequisites

- A `ConvaiClient` created as shown in [Get started with vanilla TypeScript](README.md).

## Subscribe and unsubscribe

`client.on(event, callback)` returns a function that removes the subscription. `client.off(event, callback)` removes it by reference.

```typescript
const unsubscribe = client.on('message', handleMessage);

// Later
unsubscribe();
// or
client.off('message', handleMessage);
```

Subscribe before you call `connect()` so you do not miss the first events of the session.

## Track connection state

`stateChange` fires whenever any field of `ConvaiClientState` changes. `state.agentState` combines the activity flags into one value: `'disconnected'`, `'connected'`, `'listening'`, `'thinking'`, or `'speaking'`.

```typescript
import type { ConvaiClientState } from '@convai/web-sdk/vanilla';

client.on('stateChange', (state: ConvaiClientState) => {
  statusEl.textContent = state.isConnected ? state.agentState : 'disconnected';
});
```

`client.state` returns the same state on demand.

## Wait for the character before sending

`connect` fires when the transport is up. The character can take a moment longer to be ready, and `sendUserTextMessage` does nothing while the transport is not ready. Send the first message on `botReady`, or check `client.isBotReady`.

```typescript
client.on('connect', () => console.log('Transport connected'));

client.on('botReady', () => {
  client.sendUserTextMessage('Hello!');
});

client.on('disconnect', (reason) => {
  console.log('Disconnected with reason', reason);
});
```

## Render the conversation

`message` fires with the newest `ChatMessage`. `messagesChange` fires with the whole array, including updates to a message that is still streaming. For a chat log, re-render from `messagesChange` and filter by `type`:

```typescript
import type { ChatMessage } from '@convai/web-sdk/vanilla';

const SHOWN = new Set(['user-llm-text', 'user-transcription', 'bot-llm-text', 'bot-output']);

client.on('messagesChange', (messages: ChatMessage[]) => {
  chatEl.replaceChildren(
    ...messages
      .filter((m) => SHOWN.has(m.type) && m.content.trim())
      .map((m) => {
        const div = document.createElement('div');
        div.className = m.type.startsWith('user') ? 'user' : 'bot';
        div.textContent = m.content;
        return div;
      }),
  );
});
```

The message types a chat UI usually shows:

| Type | Content |
|---|---|
| `user-llm-text` | A text message you sent with `sendUserTextMessage`. |
| `user-transcription` | What the user said, transcribed from speech. Final segments accumulate in one message until the character replies. |
| `bot-llm-text` | The character's reply, streamed as it is generated. `isStreaming` is `true` until it is final. |
| `bot-output` | The character's reply, aggregated as it is spoken. The SDK adds it to the log only when the reply did not already arrive as `bot-llm-text`. |

Other types carry emotions, actions, idle warnings, and no-response turns. See [Configuration and type reference](best-practices-and-type-definitions.md#chatmessage) for the full list.

## Show live transcription

`userTranscriptionChange` fires as the user speaks, with the transcription so far. It fires with an empty string when the utterance is final.

```typescript
client.on('userTranscriptionChange', (text: string) => {
  liveTranscriptEl.textContent = text;
});
```

## Handle errors

`error` fires for connection failures and when the character does not report ready in time. Its payload is whatever was thrown, so check the type before reading `message`.

```typescript
client.on('error', (error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
});
```

## Next steps

{% content-ref url="../event-reference.md" %}
[Web SDK event reference](../event-reference.md)
{% endcontent-ref %}

{% content-ref url="building-a-custom-ui-typescript.md" %}
[Build a custom UI in TypeScript](building-a-custom-ui-typescript.md)
{% endcontent-ref %}

{% content-ref url="../error-handling.md" %}
[Handle errors and disconnects](../error-handling.md)
{% endcontent-ref %}
