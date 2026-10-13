---
title: Configuration and type reference
description: Reference for the Convai Web SDK package entry points, every connection configuration field with its default, and the main exported types.
last_reviewed: "1.9.2"
---

This page lists the entry points of `@convai/web-sdk`, every field of `ConvaiConfig`, and the state, message, and acknowledgment types the client works with. The types are defined in the SDK's core and re-exported from `@convai/web-sdk/core`, `@convai/web-sdk/vanilla`, and `@convai/web-sdk/react`.

## Entry points

The package declares these import paths in its `exports` field. There is no other public entry point.

| Import path | Exports |
|---|---|
| `@convai/web-sdk` | Everything from `@convai/web-sdk/react` and `@convai/web-sdk/lipsync-helpers`. |
| `@convai/web-sdk/core` | `ConvaiClient`, `MemoryManager`, `BlendshapeQueue`, `EventEmitter`, `AudioManager`, `VideoManager`, `ScreenShareManager`, `MessageHandler`, the model output helpers `parseModelOutputMessage`, `ModelOutputExtensionRegistry`, `isJsonValue`, and `isJsonObject`, and every core type. |
| `@convai/web-sdk/vanilla` | `ConvaiClient`, the SDK's `AudioRenderer` class, `createConvaiWidget`, `destroyConvaiWidget`, the `VanillaWidget` and `VanillaWidgetOptions` types, and every core type. |
| `@convai/web-sdk/vanilla/websocket` | Registers the WebSocket transport when imported, and exports `WebSocketSession`. |
| `@convai/web-sdk/react` | `useConvaiClient`, `ConvaiWidget`, `useCharacterInfo`, `useLocalCameraTrack`, `ConvaiClient`, `AudioRenderer` and `AudioContext` (aliases of LiveKit's `RoomAudioRenderer` and `RoomContext`), and every core type. |
| `@convai/web-sdk/lipsync-helpers` | Channel order tables, mappers, queue factories, and the lip sync processor. See [Blendshape channel order reference](mappings-reference.md). |
| `@convai/web-sdk/embed` | Helpers for loading a published chat: `fetchPublishedChatDescriptor`, `requestPublishedChatGrant`, `loadPublishedChatSession`, and their types. |

`AudioRenderer` from `@convai/web-sdk/vanilla` and `AudioRenderer` from `@convai/web-sdk/react` are different objects with one name: the first is a class you construct with a room, the second is a React component.

## ConvaiConfig

Passed to `new ConvaiClient(config)`, `connect(config)`, or `useConvaiClient(config)`. Only `characterId` and one credential are required.

| Field | Type | Default | Description |
|---|---|---|---|
| `characterId` | `string` | required | Character to connect to. |
| `apiKey` | `string` | none | Convai API key. Either `apiKey` or `authToken` is required. |
| `authToken` | `string` | none | Short-lived auth token. Used instead of `apiKey` when both are set. See [Connect with an auth token](../auth-tokens.md). |
| `url` | `string` | `https://realtime-api.convai.com` | Base URL of the realtime API. The client posts to `{url}/connect`. |
| `transport` | `"livekit" \| "websocket"` | `"livekit"` | WebRTC through LiveKit, or the WebSocket transport. See [Use the WebSocket transport](../websocket-transport-layer.md). |
| `endUserId` | `string` | none | Stable ID of the end user, such as a UUID or an email address. Enables long-term memory and per-user analytics. Without it the session is anonymous. |
| `endUserMetadata` | `Record<string, unknown>` | none | Metadata about the end user, sent as `end_user_metadata`. |
| `characterSessionId` | `string` | none | Session to resume. `'-1'` is treated as no session. After a connection, the client stores the session ID Convai returns. |
| `enableVideo` | `boolean` | `false` | `true` opens a video connection with camera, screen share, and vision. `false` opens an audio connection. |
| `startWithVideoOn` | `boolean` | `false` | Turns the camera on at connect. Applies only when `enableVideo` is `true`. |
| `startWithAudioOn` | `boolean` | `false` on WebRTC | Turns the microphone on at connect. On the WebSocket transport the microphone starts on and is muted only when this is explicitly `false`. |
| `ttsEnabled` | `boolean` | `true` | Whether the character's replies are spoken. |
| `enableLipsync` | `boolean` | `false` | Requests blendshape frames for facial animation. |
| `blendshapeConfig` | `object` | see [blendshapeConfig](#blendshapeconfig) | Format and delivery of the blendshape frames. |
| `enableEmotion` | `boolean` | `false` | Requests the character's emotion with its replies. |
| `emotionConfig` | `object` | `{ provider: "llm" }` | How emotion is detected. Sent only when `enableEmotion` is `true`. See [emotionConfig](#emotionconfig). |
| `stateOfMind` | `string \| null` | none | Temporary state of mind sent at connect. The value is trimmed and lowercased; `"neutral"` or an empty string clears it. |
| `actionConfig` | `object` | none | Actions, scene objects, and characters the character can act on. See [actionConfig](#actionconfig). |
| `capabilities` | `ProtocolCapabilitiesConfig` | none | Opt-in protocol versions. See [capabilities](#capabilities). |
| `dynamicInfo` | `string` | none | Initial dynamic context text. |
| `keepInContext` | `boolean` | none | Sent with `dynamicInfo`. `true` keeps the dynamic information as a fixed prompt for the connection. |
| `narrativeTemplateKeys` | `Record<string, string>` | none | Narrative Design template key values, sent at connect when the map is not empty. |
| `visionInputConfig` | `VisionInputConfig` | enabled when `enableVideo` is `true` | Vision frame settings. See [visionInputConfig](#visioninputconfig). |
| `respondModes` | `RespondModesConfig` | none | Respond mode defaults per modality. See [respondModes](#respondmodes). |
| `invocationMetadata` | `object` | `source: "web_sdk"`, `clientVersion`: the SDK version | `source`, `clientVersion`, and `extraMetadata` sent for analytics. |
| `debug` | `boolean` | none | Sent to Convai as `debug` when set. |
| `logRtviMessages` | `boolean` | `true` | Logs decoded realtime messages to the browser console. Set `false` to silence them. |

### blendshapeConfig

| Field | Type | Default | Description |
|---|---|---|---|
| `format` | `"arkit" \| "mha"` | `"mha"` | `"mha"` sends 251 MetaHuman channels; `"arkit"` sends 61 values. |
| `customMapper` | `(input: number[] \| Float32Array) => Float32Array` | none | Applied to every frame as it enters `blendshapeQueue`. |
| `frames_buffer_duration` | `number` | `0.1` | Seconds of blendshapes Convai buffers before releasing them with the audio. |
| `deliver_chunks_ahead` | `boolean` | `true` when `enableLipsync` is `true` | Lets Convai send indexed frame chunks ahead of the audio. Set `false` for the paced delivery path. |
| `output_fps` | `number` | `60` | Frame rate of the ahead-delivered timeline. Ignored when `deliver_chunks_ahead` is `false`. |

### emotionConfig

| Field | Type | Default | Description |
|---|---|---|---|
| `provider` | `"llm" \| "nrclex"` | `"llm"` | `"llm"` infers emotion from the response; `"nrclex"` uses a word-level lexicon. |
| `min_word_threshold` | `number` | `3` | `"nrclex"` only. Minimum word count for detection. |
| `low_intensity_threshold` | `number` | `0.33` | `"nrclex"` only. Low intensity threshold, from 0 to 1. |
| `high_intensity_threshold` | `number` | `0.66` | `"nrclex"` only. High intensity threshold, from 0 to 1. |

### actionConfig

| Field | Type | Description |
|---|---|---|
| `actions` | `string[]` | Action names the character can perform. |
| `characters` | `Array<{ name: string; bio: string }>` | Other characters in the scene. |
| `objects` | `Array<{ name: string; description: string }>` | Objects in the scene. |
| `current_attention_object` | `string` | Optional. Object the character focuses on. Must match an `objects[].name`. |
| `tools` | `ClientToolDeclaration[]` | Optional. Client-executed tools, each with `name`, `description`, and `inputSchema`. Used only with action protocol version 2. |

See [Handle character actions](../actions.md).

### capabilities

| Field | Type | When omitted |
|---|---|---|
| `actionProtocolVersion` | `1 \| 2` | Action protocol version 1. |
| `modelOutputVersion` | `1 \| 2` | Legacy output messages. |
| `botLlmTextMode` | `"legacy" \| "raw"` | Filtered text on `bot-llm-text`. |

When a version 2 or `"raw"` selection is requested, `connect()` throws if Convai does not confirm it, and also throws if Convai selects it without the request.

### visionInputConfig

| Field | Type | Sent as |
|---|---|---|
| `enabled` | `boolean` | `enabled`. Defaults to `true` when `enableVideo` is `true`; set `false` to keep the video channel without vision context. |
| `sampleIntervalSecs` | `number` | `sample_interval_secs` |
| `framesPerTurn` | `number` | `frames_per_turn` |
| `bufferFrames` | `number` | `buffer_frames` |
| `samplingWindows` | `Array<{ count: number; intervalMs: number }>` | `sampling_windows` |
| `stalenessSeconds` | `number` | `staleness_seconds` |
| `maxResolution` | `number \| null` | `max_resolution` |
| `replacePreviousVisionContext` | `boolean` | `replace_previous_vision_context` |

### respondModes

`RespondMode` is `"must_respond"`, `"auto"`, or `"silent"`.

| Field | Type |
|---|---|
| `text` | `"must_respond"` |
| `audio` | `"must_respond"` |
| `vision` | `RespondMode` |
| `contextUpdate` | `RespondMode` |
| `trigger` | `RespondMode` |
| `sceneMetadata` | `RespondMode` |

## ConvaiClientState

Returned by `client.state` and carried by the `stateChange` event.

| Field | Type | Description |
|---|---|---|
| `isConnected` | `boolean` | Connected to Convai. |
| `isConnecting` | `boolean` | A connection attempt is in progress. |
| `isListening` | `boolean` | The user is speaking. |
| `isThinking` | `boolean` | The character is generating a reply. |
| `isSpeaking` | `boolean` | The character is speaking. |
| `agentState` | `'disconnected' \| 'connected' \| 'listening' \| 'thinking' \| 'speaking'` | Combined activity. `'disconnected'` when not connected; otherwise `'speaking'`, then `'listening'`, then `'thinking'`, then `'connected'`, in that priority. |
| `emotion` | `{ emotion: string; scale?: number } \| null` | Last emotion received. |
| `endUserId` | `string \| null` | End user ID returned by Convai on connect. |
| `endUserMetadata` | `Record<string, unknown> \| null` | End user metadata returned by Convai on connect. |
| `metrics` | `ConvaiMetrics[]` | Metrics events received this session, each with `id`, `data`, and `timestamp`. |
| `disconnectReason` | `DisconnectReason \| null` | Reason of the last disconnect, or `null`. |

## ChatMessage

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Message ID. |
| `type` | see below | Kind of message. |
| `content` | `string` | Message text. |
| `timestamp` | `string` | ISO 8601 creation time. |
| `isStreaming` | `boolean` | Optional. `true` while the message is still being appended to. |
| `logicalTurnId` | `string` | Optional. Turn ID of a correlated voice transcription under model output version 2. |

| `type` | Meaning |
|---|---|
| `user` | A message the user sent. |
| `user-llm-text` | A text message sent with `sendUserTextMessage`. |
| `user-transcription` | Transcribed user speech. |
| `convai` | A character response. |
| `bot-llm-text` | The character's reply, streamed as it is generated. |
| `bot-output` | The character's reply, aggregated as it is spoken. |
| `bot-emotion` | The character's emotion. |
| `emotion` | An emotional state. |
| `action` | Actions the character chose, as text. |
| `behavior-tree` | A behavior tree response. |
| `interrupt-bot` | An interruption of the character's response. |
| `idle-warning` | Idle timeout warning. `content` holds the remaining seconds as a numeric string. |
| `llm-no-response` | The character deliberately did not respond. `content` is empty. |

## DisconnectReason

`DisconnectReasonEnum` holds the numeric codes. `getDisconnectReasonMessage(reason)` returns the message below, `'Connected'` for `null`, and `'Disconnected'` for any other code.

| Code | Key | `getDisconnectReasonMessage` |
|---|---|---|
| `0` | `UNKNOWN_REASON` | `Network unavailable or unknown cause` |
| `1` | `CLIENT_INITIATED` | `User disconnected` |
| `2` | `DUPLICATE_IDENTITY` | `Another client with same identity joined` |
| `3` | `SERVER_SHUTDOWN` | `Server is shutting down` |
| `4` | `PARTICIPANT_REMOVED` | `Removed by RemoveParticipant API` |
| `5` | `ROOM_DELETED` | `Room ended via DeleteRoom API` |
| `6` | `STATE_MISMATCH` | `State mismatch` |
| `7` | `JOIN_FAILURE` | `Failed to join` |
| `8` | `MIGRATION` | `Participant moved to different room` |
| `9` | `SIGNAL_CLOSE` | `Signal connection closed` |

## ServerResponse

Carried by the `serverResponse` event, which acknowledges messages the client sends.

| Field | Type | Description |
|---|---|---|
| `event_type` | `string` | Type of the message being acknowledged, such as `context-update`. |
| `status` | `'success' \| 'error' \| 'processing' \| 'pending'` | Processing status. |
| `message` | `string \| null` | Human-readable result. |
| `extras` | `ServerResponseExtras \| null` | Event-specific data, such as `token_count`, `max_tokens`, and `remaining_tokens` for `context-update`. |

## Other exported types

| Area | Types |
|---|---|
| Client | `IConvaiClient`, `AudioControls`, `VideoControls`, `ScreenShareControls`, and `ConvaiClientType` from `@convai/web-sdk/core` |
| Messaging | `ContextUpdateOptions`, `SendUserTextMessageOptions`, `UpdateSceneMetadataOptions`, `UploadFileOptions`, `DynamicInfo`, `InteractionCreated`, `ServerResponseExtras` |
| Actions and model output | `ConvaiAction`, `ConvaiToolCall`, `ActionResponseEvent`, `ActionResult`, `ClientToolDeclaration`, `ModelOutputMessage`, `ModelOutputItem`, `ModelOutputProtocolError`, `ProtocolCapabilitiesConfig`, `JsonValue`, `JsonObject` |
| Vision | `VisionInputConfig`, `VisionStatusOptions`, `VisionTriggerOptions`, `VisionSourceState`, `VisionSourceHandle`, `PublishCanvasOptions`, `PublishVideoTrackOptions`, `RespondMode`, `RespondModality`, `RespondModesConfig`, `RespondModeUpdateOptions` |
| Memory | `Memory`, `MemoryAddResponse`, `MemoryListResponse`, `MemoryDeleteResponse`, `MemoryDeleteAllResponse` |
| Lip sync | `TurnStats` and `BlendshapeChunkMetadata` from `@convai/web-sdk/core`; `BlendshapeMapper`, `BlendshapeFormat`, `BlendshapeMappingConfig`, `BlendshapeNameMapping`, and `OptimizedBlendshapeOutput` from `@convai/web-sdk/lipsync-helpers` |
| Transport | `IWebSocketSession`, `WebSocketSessionFactory`, `PublishedChatConnectOptions` |

## Related reference

{% content-ref url="convaiclient-core-api.md" %}
[ConvaiClient reference](convaiclient-core-api.md)
{% endcontent-ref %}

{% content-ref url="../event-reference.md" %}
[Web SDK event reference](../event-reference.md)
{% endcontent-ref %}

{% content-ref url="mappings-reference.md" %}
[Blendshape channel order reference](mappings-reference.md)
{% endcontent-ref %}
