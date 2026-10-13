---
title: Read raw transport messages
description: Observe every message a session receives, on any transport, with the typed rawMessage event, including MCP tool lifecycle frames and unknown types.
last_reviewed: "1.9.1"
icon: code
---

Observe the messages a Convai session receives, as decoded from the wire and before the SDK interprets them. Use the `rawMessage` event to log traffic, to read MCP tool lifecycle frames, or to handle message types the SDK does not turn into its own events. It works the same on LiveKit, WebSocket and SSE.

## Prerequisites

- The Convai Web SDK installed, with a client that connects. See [Web SDK quickstart](quickstart.md).

## Subscribe to raw messages

Call `client.on('rawMessage', listener)`. It returns an unsubscribe function. The React hook exposes the same listener through its `on` and `off` methods.

{% tabs %}
{% tab title="React" %}
{% code title="src/Chat.tsx" %}
```tsx
import { useEffect } from 'react';
import { useConvaiClient, ConvaiWidget } from '@convai/web-sdk/react';

const config = {
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  startWithAudioOn: false,
};

export default function Chat() {
  const client = useConvaiClient(config);

  useEffect(() => client.on('rawMessage', (event) => {
    console.log(event.transport, event.message);
    if (event.transport === 'sse') console.log(event.request.logicalTurnIds);
  }), [client.on]);

  return <ConvaiWidget convaiClient={client} />;
}
```
{% endcode %}

Return the unsubscribe function from the effect, as above, so unmounts and rerenders remove the listener.
{% endtab %}

{% tab title="TypeScript" %}
{% code title="src/main.ts" %}
```typescript
import { ConvaiClient } from '@convai/web-sdk/core';
import { createConvaiWidget } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  startWithAudioOn: false,
});

const unsubscribe = client.on('rawMessage', (event) => {
  console.log(event.transport, event.message);
});

createConvaiWidget(document.body, { convaiClient: client });

// When the host view is disposed:
// unsubscribe();
```
{% endcode %}

You can also remove the listener with `client.off('rawMessage', listener)`, passing the same function reference.
{% endtab %}
{% endtabs %}

Subscribing does not connect or send anything. The widget, or your own call to `connect()`, controls the connection. The listener covers inbound messages only; it does not publish events or observe outgoing traffic.

## Read the event payload

Every event carries `message`, `byteLength` and `transport`. The remaining field depends on the transport, so check `event.transport` first and TypeScript narrows the type for you.

| Transport | `message` | Extra field |
|---|---|---|
| `'livekit'` | The decoded JSON envelope, including nested `server-message` data. Non-JSON packets are not emitted. | `participant`: the sender supplied by the room. It can be absent. |
| `'websocket'` | The decoded JSON envelope, including nested `server-message` data. Non-JSON packets are not emitted. | None |
| `'sse'` | `{ type: eventName, data: decodedData }`. Data that is not JSON stays a string. | `request`: the originating request's `logicalTurnIds` and `messageTypes`. |

- `message` is `unknown`. Validate its shape before you use it.
- `message` and the SSE request metadata are detached from the SDK's own processing. Treat them as read-only.
- `byteLength` is the incoming payload size. For SSE it counts the joined data fields, without event framing.
- On SSE, session, done, error and unknown frames are included. SSE comments and frames without data are not.
- SSE reports individual text frames before the SDK batches them into chat messages.

### Check where a message came from

On LiveKit, validate the sender with `event.participant` against the current room. It is the original participant object, not a copy.

On SSE, use `event.request.logicalTurnIds` to match a frame to the user turn that caused it. Control-only requests can have an empty list. When a request is interrupted, its remaining frames are not emitted.

## Read MCP tool lifecycle frames

Messages about tool calls, including MCP tools, arrive on `rawMessage` like any other frame, along with event types the SDK does not interpret. Read the `type` field on `message` to pick out the ones you need, for example `llm-function-call-in-progress` and `llm-function-call-stopped`, or a `server-message` whose `data.type` is `mcp-tool-heartbeat`.

{% code title="src/tools.ts" %}
```typescript
client.on('rawMessage', ({ message }) => {
  const frame = message as { type?: string; data?: { type?: string; tool_call_id?: string } };
  if (frame.type === 'llm-function-call-in-progress') showToolSpinner(frame.data?.tool_call_id);
  if (frame.type === 'llm-function-call-stopped') hideToolSpinner(frame.data?.tool_call_id);
});
```
{% endcode %}

## When to use rawMessage

Use the SDK's normal events, listed in the [Web SDK event reference](event-reference.md), for anything they already cover. Use `rawMessage` for what they do not: debugging and logging traffic, tool and MCP lifecycle frames, server message types the SDK does not interpret, and per-request correlation on SSE.

{% hint style="warning" %}
A raw message is an observation, not proof that something succeeded. On SSE, the server can send a conflicting terminal frame that the SDK then rejects. Use the `botTurnCompleted` event to know that a turn completed.
{% endhint %}

An exception thrown in your listener does not stop the SDK from handling the message normally.

## API reference

| Property / Method | Type | Description |
|---|---|---|
| `client.on('rawMessage', listener)` | `(listener: (event: RawMessageEvent) => void) => () => void` | Subscribes to incoming messages. Returns an unsubscribe function. |
| `client.off('rawMessage', listener)` | `void` | Removes the same listener by reference. |
| `RawMessageEvent` | union type | The event payload. Narrow it by `transport`. |
| `event.message` | `unknown` | Decoded wire message, before SDK interpretation. Validate its shape before use. |
| `event.byteLength` | `number` | Incoming payload size. For SSE, the joined data fields without event framing. |
| `event.transport` | `'livekit' \| 'websocket' \| 'sse'` | Transport that delivered the message. |
| `event.participant` | `unknown` | LiveKit only. Sender supplied by the room; can be absent. |
| `event.request` | `SSERequestContext` | SSE only. The originating request's `logicalTurnIds` and `messageTypes`. |
| `SSERequestContext` | `{ transport: 'sse'; logicalTurnIds: string[]; messageTypes: string[] }` | Identity of the SSE request that produced the event. |
