---
title: Web SDK event reference
description: Reference for every event the Convai Web SDK client and its media controls emit, with the payload each one carries and when it fires.
last_reviewed: "1.9.2"
icon: arrow-up-small-big
---

`ConvaiClient` emits the events on this page through `on(event, callback)`, which returns an unsubscribe function, and `off(event, callback)`. The `useConvaiClient` hook in `@convai/web-sdk/react` exposes the same `on` and `off`. Event names are plain strings and payloads are not typed by the emitter, so annotate callback parameters with the exported types.

```typescript
const unsubscribe = client.on('botReady', () => {
  client.sendUserTextMessage('Hello');
});

unsubscribe();
```

## Connection events

| Event | Payload | Fires when |
|---|---|---|
| `connect` | none | `connect()` or `connectWithPublicationGrant()` has opened the transport. The character can still be unready; wait for `botReady` before sending. |
| `botReady` | none | The character signals that it is ready for messages. Fires once per connection. |
| `disconnect` | `DisconnectReason` (`number`) | The session ends. The code is `0` when the transport gives no reason. See [Handle errors and disconnects](error-handling.md). |
| `error` | `unknown` | `connect()` or `connectWithPublicationGrant()` fails (the same error is rethrown), or, on the LiveKit transport, no ready signal arrives within 45 seconds (`bot-ready not received within 45000ms`). |
| `stateChange` | `ConvaiClientState` | Any field of `client.state` changes value. |
| `interactionCreated` | `InteractionCreated`: `{ interactionId: string; characterSessionId: string }` | Convai assigns an interaction ID to the session. |
| `botAudioTrack` | `MediaStreamTrack` | A WebSocket session exposes a character audio track. It does not fire with the current Pipecat WebSocket transport, which plays the voice itself and exposes no character track. See [Use the WebSocket transport](websocket-transport-layer.md). |

## Conversation events

| Event | Payload | Fires when |
|---|---|---|
| `conversationStart` | `{ sessionId: number; userMessage: string; timestamp: number }` | A new turn starts. `sessionId` increments per turn and matches `client.conversationSessionId`. `timestamp` is a `Date.now()` value. |
| `turnEnd` | `{ sessionId: number; duration: number; timestamp: number }` | The character stops speaking after at least one turn has started. `duration` is the seconds since the matching `conversationStart`. |
| `message` | `ChatMessage` | The message list changes. The payload is the last message in the list, so it fires again as a streaming message grows. |
| `messagesChange` | `ChatMessage[]` | The message list changes, including streaming updates and resets. |
| `userTranscriptionChange` | `string` | The live transcription of the end user's speech changes. An empty string clears it. |
| `llmNoResponse` | none | The character deliberately does not answer the turn. |
| `metrics` | `Record<string, unknown>` | Convai sends a metrics message. The raw data is also appended to `client.state.metrics`. |

`conversationStart.userMessage` identifies what started the turn:

| Value | Started by |
|---|---|
| The trimmed message text | `sendUserTextMessage()` |
| `[voice]` | The end user starting to speak |
| `[trigger:<name>]` | `sendTriggerMessage()`; `<name>` is empty when no trigger name was passed |
| `[context-update:<mode>]` | `updateContext()` with `run_llm: "true"`, or with `respond_mode: "must_respond"` and no `run_llm`; `<mode>` defaults to `append` |
| `[vision-trigger:must_respond]` | `visionTrigger()` with `respondMode: "must_respond"` |
| `[scene-metadata:must_respond]` | `updateSceneMetadata()` with `respondMode: "must_respond"` |

## Speech events

| Event | Payload | Fires when |
|---|---|---|
| `speakingChange` | `boolean` | The character starts (`true`) or stops (`false`) speaking. A reset or interruption also emits `false`. |
| `botOutput` | `{ text: string; spoken: boolean; aggregatedBy: string; segmentId?: number \| string; spokenStatus?: string }` | Convai sends an aggregated output segment. `aggregatedBy` is `"sentence"` when Convai does not specify it. The same `segmentId` can repeat as speech progresses. |
| `botTtsText` | `{ text: string }` | Convai sends text as it is spoken. |
| `botTtsStarted` | none | Speech synthesis for a response starts. |
| `botTtsStopped` | none | Speech synthesis for a response stops. |
| `userMuteStarted` | none | Convai reports that it stopped accepting the end user's audio. |
| `userMuteStopped` | none | Convai reports that it accepts the end user's audio again. |
| `emotionChange` | `{ emotion: string; scale?: number } \| null` | The character's emotion changes. `null` on reset and disconnect. Requires `enableEmotion: true`. See [Use character emotions](emotions.md). |

## Lip sync events

These require `enableLipsync: true`. Read frames from `client.blendshapeQueue` rather than from these payloads. See [Drive facial animation with blendshapes](lipsync-and-blendshape/README.md).

| Event | Payload | Fires when |
|---|---|---|
| `blendshapes` | Raw chunk object from Convai, with a `blendshapes` array of frames | A blendshape chunk is accepted for the current response. |
| `blendshapeStatsReceived` | Raw object from Convai, with turn statistics in `stats` | Convai sends end-of-turn blendshape statistics, meaning no more frames will come for that response. |
| `blendshapeCancel` | Raw cancel object from Convai | Convai cancels the blendshape stream of a response, for example after an interruption. |

## Action events

| Event | Payload | Fires when |
|---|---|---|
| `actionResponse` | `ActionResponseEvent`: `{ actions: Array<ConvaiAction \| ConvaiToolCall> }` | Convai sends actions for a turn. An empty array means no action. Not emitted when model output version 2 is selected. |
| `modelOutput` | `ModelOutputMessage` | A valid model output envelope arrives on a session that selected `capabilities.modelOutputVersion: 2`. A repeated `output_id` is dropped. |
| `modelOutputProtocolError` | `ModelOutputProtocolError`: `{ code: "invalid_model_output"; message: string }` | A model output envelope on a version 2 session is malformed or unsupported. |

See [Handle character actions](actions.md) for how to use these events.

## Acknowledgment and session events

| Event | Payload | Fires when |
|---|---|---|
| `serverResponse` | `ServerResponse`: `{ event_type: string; status: "success" \| "error" \| "processing" \| "pending"; message: string \| null; extras: ServerResponseExtras \| null }` | Convai acknowledges a message the client sent. `event_type` is the type of that message, such as `context-update` or `action-result`. |
| `idleWarning` | `{ remainingSeconds: number \| null }` | Convai warns that it will close the inactive session. Call `resetIdleTimer()` to keep it open. |

## Media control events

`client.audioControls`, `client.videoControls`, and `client.screenShareControls` each have their own `on` and `off` methods and emit one event.

| Emitter | Event | Payload fields |
|---|---|---|
| `audioControls` | `audioStateChange` | `isAudioMuted`, `isAudioEnabled`, and on most changes `audioLevel` |
| `videoControls` | `videoStateChange` | `isVideoEnabled`, `isVideoHidden`, `activeVisionSource`, `hasActiveVisionSource`, `visionSourceState` |
| `screenShareControls` | `screenShareStateChange` | `isScreenShareActive`, and on enable, disable, and reset `isScreenShareEnabled` |

```typescript
const off = client.audioControls.on('audioStateChange', (s: { isAudioMuted?: boolean }) => {
  micButton.textContent = s.isAudioMuted ? 'Unmute' : 'Mute';
});
```

## Related reference

{% content-ref url="vanilla-typescript/convaiclient-core-api.md" %}
[ConvaiClient reference](vanilla-typescript/convaiclient-core-api.md)
{% endcontent-ref %}

{% content-ref url="vanilla-typescript/best-practices-and-type-definitions.md" %}
[Configuration and type reference](vanilla-typescript/best-practices-and-type-definitions.md)
{% endcontent-ref %}

{% content-ref url="error-handling.md" %}
[Handle errors and disconnects](error-handling.md)
{% endcontent-ref %}
