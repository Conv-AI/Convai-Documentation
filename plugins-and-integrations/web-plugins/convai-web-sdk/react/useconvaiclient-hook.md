---
title: useConvaiClient hook reference
description: Reference for the React hook that owns a Convai client, including its parameter, every returned field, and the state it keeps for rendering.
last_reviewed: "1.9.2"
---

`useConvaiClient` is the React hook exported from `@convai/web-sdk/react`. It creates one `ConvaiClient` for the lifetime of the component, subscribes to its events, and returns the client's API together with React state that re-renders the component when the conversation changes.

## Signature

```ts
function useConvaiClient(config?: ConvaiConfig): IConvaiClient & {
  connectWithPublicationGrant: (
    launchToken: string,
    options?: PublishedChatConnectOptions,
  ) => Promise<void>;
  activity: string;
  chatMessages: ChatMessage[];
  isAudioMuted: boolean;
  isVideoEnabled: boolean;
  isScreenShareActive: boolean;
};
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `config` | `ConvaiConfig` | none | Connection config stored on first render and used by `connect()` when it is called with no argument. Later changes to this argument are ignored. Every field is listed in the [Configuration and type reference](../vanilla-typescript/best-practices-and-type-definitions.md). |

The hook creates its client once, with `useState`. Listeners are removed and the hidden WebSocket audio element is removed when the component unmounts. The hook does not disconnect on unmount; call `disconnect()` yourself when the session should end.

## React state

These fields are React state. Reading them in render keeps the component in step with the conversation.

| Field | Type | Updated when |
|---|---|---|
| `state` | `ConvaiClientState` | The client emits `stateChange`, `connect`, or `disconnect`. |
| `activity` | `string` | The client emits `stateChange`, `botReady`, or `disconnect`. See [Activity values](#activity-values). |
| `chatMessages` | `ChatMessage[]` | The client emits `messagesChange`. Cleared to `[]` on `disconnect`. |
| `userTranscription` | `string` | The client emits `userTranscriptionChange`. Holds the live, non-final transcription of your speech. |
| `isBotReady` | `boolean` | Set to `true` on `botReady` and to `false` on `disconnect`. |
| `isAudioMuted` | `boolean` | `audioControls` emits `audioStateChange`. Set to `true` on `disconnect`. |
| `isVideoEnabled` | `boolean` | `videoControls` emits `videoStateChange`. Set to `false` on `disconnect`. |
| `isScreenShareActive` | `boolean` | `screenShareControls` emits `screenShareStateChange`. Set to `false` on `disconnect`. |

`activity`, `isAudioMuted`, `isVideoEnabled`, and `isScreenShareActive` exist only on the hook's return value. A `ConvaiClient` created directly does not have them.

## Activity values

`activity` starts as `"Idle"`. After that the hook sets it from the client state in this order of priority:

| Value | Set when |
|---|---|
| `"Connecting..."` | `state.isConnecting` is `true`. |
| `"Disconnected"` | Not connected and not connecting, or the client emits `disconnect`. |
| `"Speaking"` | The character is speaking. |
| `"Listening"` | You are speaking. |
| `"Thinking"` | The character is preparing a response. |
| `"Connected"` | Connected with none of the above, or when `botReady` fires. |

## Client values

These fields are read from the client each time the component renders. They do not trigger a render on their own.

| Field | Type | Description |
|---|---|---|
| `connectionType` | `'audio' \| 'video' \| 'text' \| null` | Connection type of the current session. `null` when not connected. |
| `isPublishedChatSession` | `boolean` | `true` when the client was last connected with `connectWithPublicationGrant`. |
| `apiKey` | `string` | API key of the current connection. Present only when one was used. |
| `authToken` | `string` | Auth token of the current connection. Present only when one was used. |
| `characterId` | `string \| null` | Character ID of the current connection. |
| `characterSessionId` | `string \| null` | Session ID returned by Convai for the current conversation. |
| `requestTraceId` | `string \| null` | Trace ID for the most recent connection request, when Convai provided one. |
| `conversationSessionId` | `number` | Turn counter used by the `conversationStart` and `turnEnd` events. |
| `room` | `Room` | The LiveKit room. Pass it to `AudioContext.Provider` in a custom UI. |
| `audioControls` | `AudioControls` | Microphone controls. |
| `videoControls` | `VideoControls` | Camera and vision source controls. |
| `screenShareControls` | `ScreenShareControls` | Screen share controls. |
| `blendshapeQueue` | `BlendshapeQueue` | Buffered lip sync frames. |
| `memoryManager` | `MemoryManager \| null` | Long-term memory API. `null` until connected with an `endUserId`. |

## Methods

Every method is bound to the hook's client, so you can pass it directly as an event handler. Behavior, parameters, and errors are documented in the [ConvaiClient reference](../vanilla-typescript/convaiclient-core-api.md).

| Method | Notes |
|---|---|
| `connect(config?)` | Connects with `config`, or with the config passed to the hook. Throws `No configuration provided. Pass config to useConvaiClient() or to connect()` when neither exists. |
| `connectWithPublicationGrant(launchToken, options?)` | Connects to a published text chat with a single-use launch token. |
| `disconnect()` | Ends the session. |
| `reconnect()` | Connects again with the last stored config. |
| `resetSession()` | Clears the conversation and starts a new session on the next connect. On a live connection, call `disconnect()` first, then `connect()` again. |
| `sendUserTextMessage(text, options?)` | Sends a text message. |
| `sendTriggerMessage(triggerName?, triggerMessage?)` | Fires a trigger. |
| `sendInterruptMessage()` | Interrupts the character's current response. |
| `sendActionResult(result)` | Returns the result of a client tool call. |
| `resetIdleTimer()` | Resets the idle timer for the session. |
| `updateTemplateKeys(templateKeys)` | Replaces the Narrative Design template keys. |
| `updateDynamicInfo(dynamicInfo)` | Sends dynamic context text. |
| `updateContext(options)` | Appends, replaces, or resets runtime context. |
| `updateEmotion(stateOfMind)` | Sets or clears the character's state of mind. |
| `updateSceneMetadata(items, options?)` | Sends descriptive scene items. |
| `visionStatus(options?)` | Requests the vision buffer status. |
| `visionTrigger(options?)` | Attaches buffered vision frames and optionally requests a response. |
| `respondModeUpdate(options)` | Changes a respond mode for the session. |
| `toggleTts(enabled)` | Turns speech output on or off. |
| `toggleStt(enabled)` | Turns speech-to-text on or off. |
| `uploadFile(file, options?)` | Sends a file over the LiveKit transport. |
| `on(event, callback)` | Subscribes to a client event and returns an unsubscribe function. |
| `off(event, callback)` | Removes a listener. |

## WebSocket audio playback

When the session uses `transport: "websocket"`, the Pipecat transport plays the character's voice itself through Web Audio, so no extra code is needed. The hook also appends a hidden `<audio data-convai-ws>` element to `document.body` for the `botAudioTrack` event, but that event does not fire with the current WebSocket transport, so the element stays silent. With the default LiveKit transport, render `AudioRenderer` or `ConvaiWidget` to hear the character. See [Build a custom UI in React](custom-ui-and-advanced-usage.md).

## Example

```tsx
import { useConvaiClient } from '@convai/web-sdk/react';

export function ConnectButton() {
  const client = useConvaiClient();

  const connect = () =>
    client.connect({
      apiKey: 'YOUR_API_KEY',
      characterId: 'YOUR_CHARACTER_ID',
    });

  return (
    <button onClick={connect} disabled={client.state.isConnected}>
      {client.activity}
    </button>
  );
}
```

## Related reference

{% content-ref url="../vanilla-typescript/convaiclient-core-api.md" %}
[ConvaiClient reference](../vanilla-typescript/convaiclient-core-api.md)
{% endcontent-ref %}

{% content-ref url="../vanilla-typescript/best-practices-and-type-definitions.md" %}
[Configuration and type reference](../vanilla-typescript/best-practices-and-type-definitions.md)
{% endcontent-ref %}

{% content-ref url="../event-reference.md" %}
[Web SDK event reference](../event-reference.md)
{% endcontent-ref %}

{% content-ref url="convaiwidget.md" %}
[ConvaiWidget component reference](convaiwidget.md)
{% endcontent-ref %}
