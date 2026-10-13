---
title: ConvaiClient reference
description: Reference for the framework-free Convai Web SDK client, including its properties, methods, media controls, lip sync queue, and errors.
last_reviewed: "1.9.2"
---

`ConvaiClient` is the framework-free client of the Convai Web SDK. It is exported from `@convai/web-sdk/core` and `@convai/web-sdk/vanilla`, implements the `IConvaiClient` interface, and extends the SDK's `EventEmitter`. The React hook `useConvaiClient` wraps the same class.

## Constructor

```typescript
new ConvaiClient(config?: ConvaiConfig)
```

| Parameter | Type | Description |
|---|---|---|
| `config` | `ConvaiConfig` | Optional. Stored and used by `connect()` and `reconnect()` when they are called without a config. |

The constructor creates the WebRTC room and does not connect. For every `ConvaiConfig` field, see [Configuration and type reference](best-practices-and-type-definitions.md).

## Static methods

### `registerWebSocketTransport(factory)`

```typescript
static registerWebSocketTransport(factory: WebSocketSessionFactory): void
```

Registers the implementation used when `transport` is `"websocket"`. Importing `@convai/web-sdk/vanilla/websocket` calls it for you with the SDK's own WebSocket session. Call it directly only to supply a custom implementation of `IWebSocketSession`.

`WebSocketSessionFactory` is `(onMessage: (payload: Uint8Array) => void, enableMic: boolean) => IWebSocketSession`.

## Properties

All properties are read-only.

| Property | Type | Description |
|---|---|---|
| `state` | `ConvaiClientState` | A copy of the current connection and activity state. |
| `connectionType` | `'audio' \| 'video' \| 'text' \| null` | `'video'` when connected with `enableVideo: true`, `'audio'` otherwise, `'text'` for a published-chat session, and `null` when disconnected. |
| `apiKey` | `string \| null` | API key of the current connection, or `null`. |
| `authToken` | `string \| null` | Auth token of the current connection, or `null`. |
| `characterId` | `string \| null` | Character ID of the current connection, or `null`. |
| `characterSessionId` | `string \| null` | Session ID returned by Convai on connect. `'-1'` before the first connection and after `resetSession()`. |
| `requestTraceId` | `string \| null` | Trace ID of the most recent connection request, when Convai returns one. |
| `isBotReady` | `boolean` | `true` after the character signals that it is ready for messages. |
| `isPublishedChatSession` | `boolean` | `true` when the last connection used `connectWithPublicationGrant()`. |
| `chatMessages` | `ChatMessage[]` | Every message in the current conversation. |
| `userTranscription` | `string` | Live speech-to-text of the current user utterance. |
| `conversationSessionId` | `number` | Turn counter, incremented each time a turn starts. Carried by `conversationStart` and `turnEnd`. |
| `room` | `Room` | The underlying LiveKit `Room`, for advanced use. |
| `audioControls` | `AudioControls` | Microphone controls. See [Audio controls](#audio-controls). |
| `videoControls` | `VideoControls` | Camera and vision-source controls. See [Video controls](#video-controls). |
| `screenShareControls` | `ScreenShareControls` | Screen-share controls. See [Screen share controls](#screen-share-controls). |
| `blendshapeQueue` | `BlendshapeQueue` | Buffer of lip sync frames. See [BlendshapeQueue](#blendshapequeue). |
| `memoryManager` | `MemoryManager \| null` | Long-term memory API. `null` unless the connection returned an end user ID. See [Use long-term memory](../long-term-memory.md). |

## Connection methods

### `connect(config?)`

```typescript
connect(config?: ConvaiConfig): Promise<void>
```

Connects to the character. Uses `config` when given, otherwise the config passed to the constructor, and stores the result for `reconnect()`.

The client sends `POST {url}/connect`, where `url` defaults to `https://realtime-api.convai.com`. It authenticates with the `API-AUTH-TOKEN` header when `authToken` is set, and otherwise with the `X-API-Key` header. When both are set, `authToken` is used. It then joins the WebRTC room, or opens the WebSocket session when `transport` is `"websocket"`, and emits `connect`.

After `connect` the client waits for the character to report that it is ready, and emits `botReady`. On the WebRTC transport, if that does not happen within 45 seconds, the client emits `error` with `bot-ready not received within 45000ms`.

| Condition | Result |
|---|---|
| No config passed and none stored | Throws `No configuration provided. Pass config to connect() or store it in the client` |
| Neither `apiKey` nor `authToken`, or no `characterId` | Throws `Either apiKey or authToken is required, and characterId is required` |
| Convai rejects the request | Throws an `Error` whose message is the reason Convai returned, or `HTTP <status>` |
| `transport: "websocket"` without registering the transport | Throws ``[ConvaiClient] WebSocket transport is not registered. Add `import '@convai/web-sdk/vanilla/websocket'` before calling connect().`` |
| WebSocket closes before the connection completes | Throws `WebSocket disconnected before connect completed` |

Except for the two configuration checks, every failure also emits `error` with the same error before the promise rejects.

### `reconnect()`

```typescript
reconnect(): Promise<void>
```

Calls `connect()` with the stored config. The stored config carries the `characterSessionId` from the previous connection, so the session resumes. Throws `No stored config available for reconnection` when nothing is stored.

### `disconnect()`

```typescript
disconnect(): Promise<void>
```

Leaves the room or closes the WebSocket session, and clears the connection's credentials, controls, and memory manager. The client does not reconnect automatically after any disconnect.

### `resetSession()`

```typescript
resetSession(): void
```

Sets `characterSessionId` back to `'-1'` so the next connection starts a new session, clears the chat history and lip sync queue, and clears `metrics` and `disconnectReason` in `state`.

### `connectWithPublicationGrant(launchToken, options?)`

```typescript
connectWithPublicationGrant(launchToken: string, options?: PublishedChatConnectOptions): Promise<void>
```

Connects to a published text chat with a single-use launch token instead of an API key or auth token. The session is text only: no microphone, camera, speech, or lip sync. `options` accepts `url`, `signal` (an `AbortSignal`), and `connectAttemptId`. Throws `A valid publication launch token is required` for a token shorter than 32 or longer than 512 characters, and `Disconnect the current session before connecting again` when a session is open.

## Messaging methods

Unless a row says otherwise, these methods return `void` and do nothing when the transport is not ready.

| Method | Description |
|---|---|
| `sendUserTextMessage(text: string, options?: SendUserTextMessageOptions)` | Sends a text message and starts a new turn. Ignores empty text. `options.logicalTurnId` correlates model output version 2 envelopes; it must be non-empty and at most 128 UTF-8 bytes, or the method throws `logicalTurnId must be non-empty and at most 128 UTF-8 bytes`. |
| `sendTriggerMessage(triggerName?: string, triggerMessage?: string)` | Fires a named trigger, optionally with a message, and starts a new turn. |
| `sendInterruptMessage()` | Asks Convai to stop the current response and stops local lip sync playback. |
| `sendActionResult(result: ActionResult)` | Returns the result of a client tool call. Throws instead of doing nothing: `Cannot send an action result before the session is ready` when the transport is not ready, and a validation error for an empty `id`, an unknown `status`, `error` on a `completed` result, or non-JSON values. See [Handle character actions](../actions.md). |
| `updateContext(options: ContextUpdateOptions)` | Appends, replaces, or resets the runtime context, or sets `current_attention_object`. Logs a warning and sends nothing when there is no text and no attention object and `mode` is not `"reset"`. |
| `updateDynamicInfo(dynamicInfo: string)` | Sends dynamic information text. Ignores empty text. |
| `updateTemplateKeys(templateKeys: Record<string, string>)` | Replaces the Narrative Design template keys of the live session. Ignores an empty object. |
| `updateEmotion(stateOfMind: string \| null)` | Sets the character's temporary state of mind without triggering a response. `null`, an empty string, or `"neutral"` clears it. The value is also stored for the next `connect()`, even when no session is open. |
| `updateSceneMetadata(items: Array<{ name: string; description: string }>, options?: UpdateSceneMetadataOptions)` | Describes what is visible or nearby. Does not change `actionConfig`. `options.respondMode` sets whether the update may trigger a response. |
| `toggleTts(enabled: boolean)` | Turns the character's speech on or off. |
| `toggleStt(enabled: boolean)` | Turns speech-to-text on or off. Sent to Convai as `muted: !enabled`. |
| `resetIdleTimer()` | Resets Convai's idle timer for the session. |

See [Update character context at runtime](../dynamic-context.md) for how these fit together.

## Vision and respond-mode methods

Each returns the update ID it sent, or `null` when the transport is not ready. When `updateId` is omitted, the client generates one.

| Method | Description |
|---|---|
| `visionStatus(options?: VisionStatusOptions): string \| null` | Requests a server acknowledgment that reports the vision frame buffer. `options.updateId` is optional. |
| `visionTrigger(options?: VisionTriggerOptions): string \| null` | Attaches buffered frames to the conversation and optionally triggers a response. `options` accepts `updateId`, `text`, `respondMode`, `frameIndices` (`[start, end]`), and `frameIds`. |
| `respondModeUpdate(options: RespondModeUpdateOptions): string \| null` | Changes the session's respond mode for one modality. `options` takes `modality` (`"text"`, `"audio"`, `"vision"`, `"context_update"`, `"trigger"`, or `"scene_metadata"`), `mode` (`"must_respond"`, `"auto"`, or `"silent"`), and an optional `updateId`. |

Convai acknowledges each of these on the `serverResponse` event.

## File upload

### `uploadFile(file, options?)`

```typescript
uploadFile(file: File, options?: UploadFileOptions): Promise<void>
```

Sends a file to the character over the WebRTC transport. Resolves when the upload completes.

| Option | Type | Default | Description |
|---|---|---|---|
| `topic` | `string` | `"file-upload"` | Routing topic for the upload. |
| `onProgress` | `(progressPercent: number) => void` | none | Called with an integer percentage from 0 to 100. |

Throws `[ConvaiClient] uploadFile: not connected to a LiveKit room` when there is no WebRTC room participant.

## Events

### `on(event, callback)`

```typescript
on(event: string, callback: (...args: any[]) => void): () => void
```

Subscribes to an event and returns a function that unsubscribes.

### `off(event, callback)`

```typescript
off(event: string, callback: (...args: any[]) => void): void
```

Removes a subscription. For every event name and payload, see [Web SDK event reference](../event-reference.md).

## Audio controls

`client.audioControls` implements `AudioControls`. The methods throw `Room not initialized` when no room is available.

| Member | Type | Description |
|---|---|---|
| `isAudioEnabled` | `boolean` | Whether the microphone is enabled. |
| `isAudioMuted` | `boolean` | Whether the microphone is muted. |
| `audioLevel` | `number` | Microphone level. Level monitoring is not implemented in this release, so the value stays `0`. |
| `enableAudio()` | `Promise<void>` | Enables the microphone. |
| `disableAudio()` | `Promise<void>` | Disables the microphone and stops the track, releasing the device. |
| `muteAudio()` | `Promise<void>` | Same as `disableAudio()`. |
| `unmuteAudio()` | `Promise<void>` | Same as `enableAudio()`. |
| `toggleAudio()` | `Promise<void>` | Unmutes when muted, otherwise mutes. |
| `setAudioDevice(deviceId: string)` | `Promise<void>` | Enables the microphone on the given input device. |
| `getAudioDevices()` | `Promise<MediaDeviceInfo[]>` | Lists audio input devices. |
| `startAudioLevelMonitoring()` | `void` | Reserved for level monitoring. Has no effect in this release. |
| `stopAudioLevelMonitoring()` | `void` | Stops level monitoring and sets `audioLevel` to `0`. |
| `on(event, callback)`, `off(event, callback)` | | Subscribe to `audioStateChange`, whose payload carries `isAudioMuted`, `isAudioEnabled`, and `audioLevel`. |

## Video controls

`client.videoControls` implements `VideoControls`. Camera, screen share, and vision sources are part of a video connection, which you open with `enableVideo: true`.

| Member | Type | Description |
|---|---|---|
| `isVideoEnabled` | `boolean` | Whether the camera is enabled. |
| `isVideoHidden` | `boolean` | Whether the local video is hidden. |
| `activeVisionSource` | `VisionSourceHandle \| null` | The source that frames are taken from. |
| `hasActiveVisionSource` | `boolean` | Whether a vision source is active. |
| `visionSourceState` | `VisionSourceState` | `active`, `source`, `sourceName`, `trackState`, and optionally `transport` and `reason`. |
| `enableVideo()`, `disableVideo()`, `toggleVideo()` | `Promise<void>` | Turn the camera on, off, or over. |
| `hideVideo()`, `showVideo()` | `Promise<void>` | Hide or show the local video. |
| `setVideoDevice(deviceId: string)` | `Promise<void>` | Switches the camera. |
| `getVideoDevices()` | `Promise<MediaDeviceInfo[]>` | Lists video input devices. |
| `setVideoQuality(quality: 'low' \| 'medium' \| 'high')` | `Promise<void>` | Accepts a quality level. It does not change the published video in this release. |
| `publishCanvas(canvas: HTMLCanvasElement, options?: PublishCanvasOptions)` | `Promise<VisionSourceHandle>` | Publishes a canvas as the vision source. `options` accepts `fps`, `name`, `source`, and `stopTrackOnUnpublish`. Throws `Canvas captureStream() is not supported in this browser` when the canvas cannot be captured. |
| `publishVideoTrack(track: MediaStreamTrack, options?: PublishVideoTrackOptions)` | `Promise<VisionSourceHandle>` | Publishes any video track as the vision source. |
| `unpublishVisionSource(source?: VisionSourceHandle \| MediaStreamTrack)` | `Promise<void>` | Stops publishing a vision source. |
| `on(event, callback)`, `off(event, callback)` | | Subscribe to `videoStateChange`. |

## Screen share controls

`client.screenShareControls` implements `ScreenShareControls`. The methods throw `Room not initialized` when no room is available.

| Member | Type | Description |
|---|---|---|
| `isScreenShareEnabled` | `boolean` | Whether screen share is enabled. |
| `isScreenShareActive` | `boolean` | Whether a screen is being shared. |
| `enableScreenShare()`, `disableScreenShare()`, `toggleScreenShare()` | `Promise<void>` | Start, stop, or toggle screen share. |
| `enableScreenShareWithAudio()` | `Promise<void>` | Starts screen share with audio. |
| `getScreenShareTracks()` | `Promise<any[]>` | Returns the screen-share tracks. |
| `on(event, callback)`, `off(event, callback)` | | Subscribe to `screenShareStateChange`. |

## BlendshapeQueue

`client.blendshapeQueue` buffers lip sync frames when `enableLipsync` is `true`. The class is exported from `@convai/web-sdk/core`. Frames arrive in chunks of 10 and are played on a timeline whose rate is `getPlaybackFps()`, which falls back to 60.

| Method | Returns | Description |
|---|---|---|
| `isBotSpeaking()` | `boolean` | `true` while the character's audio is playing. |
| `isConversationActive()` | `boolean` | `true` from the start of a turn until Convai sends the turn's end statistics. |
| `hasReceivedEndSignal()` | `boolean` | `true` once the turn's end statistics have arrived and audio playback has started. |
| `isConversationEnded()` | `boolean` | `true` once the end signal has arrived, the character has stopped speaking, and the frames are played or gone. |
| `hasFrames()` | `boolean` | Whether playable frames are buffered. |
| `hasBufferedFrames()` | `boolean` | Whether any frames are buffered, including ones not yet in playback order. |
| `length` | `number` | Number of playable frames in the queue. |
| `getFrame(index)` | `Float32Array \| null` | Frame at `index`, or `null` when out of range. |
| `getFrameWithAlpha(index)` | `Float32Array \| null` | Same frame, faded in over the first 10 frames of the turn and out over the last 10. |
| `getFrameAtTime(elapsedSeconds)` | `{ frame, frameIndex } \| null` | Frame at `elapsedSeconds` multiplied by the playback rate, clamped to the last frame. Does not consume. |
| `getFrames()` | `Float32Array[]` | All playable frames. |
| `consumeFrames(count)` | `void` | Removes `count` frames from the front and adds them to the consumed total. |
| `getFramesConsumed()` | `number` | Frames consumed this turn. |
| `getPlaybackFps()` | `number` | Playback rate of the current turn. |
| `getTurnStats()` | `TurnStats \| null` | `fps`, `total_audio_bytes`, `total_audio_duration_ms`, `total_blendshapes`, and `total_turn_duration_ms`. |
| `getTimeLeftMs()` | `number \| null` | Estimated remaining playback time, or `null` before the statistics arrive. |
| `isAllFramesConsumed()` | `boolean` | Whether the consumed total reached `total_blendshapes`. |
| `consumeNormalizationSignal()` | `boolean` | Returns `true` once after an interruption or a cancelled response, as the signal to ease the face back to neutral. |
| `setMapper(mapper)`, `clearMapper()`, `hasMapper()` | | Set, remove, or check the function applied to each frame as it enters the queue. |
| `reset()` | `void` | Empties the queue and clears the turn state. |
| `getDebugInfo()` | `object` | Snapshot of the queue state for logging. |

The client starts, interrupts, and ends turns on the queue itself. See [Add lip sync in vanilla TypeScript](real-time-lipsync.md) for a playback loop.

## Related reference

{% content-ref url="best-practices-and-type-definitions.md" %}
[Configuration and type reference](best-practices-and-type-definitions.md)
{% endcontent-ref %}

{% content-ref url="../event-reference.md" %}
[Web SDK event reference](../event-reference.md)
{% endcontent-ref %}

{% content-ref url="../error-handling.md" %}
[Handle errors and disconnects](../error-handling.md)
{% endcontent-ref %}
