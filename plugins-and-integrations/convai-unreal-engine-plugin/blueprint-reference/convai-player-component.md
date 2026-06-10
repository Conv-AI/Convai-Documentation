---
title: Convai Player Component
description: Reference for the player conversation component — every Blueprint-visible property, function, and event exposed by the Convai Player Component.
last_reviewed: "4.0.0-beta.21"
---

`UConvaiPlayerComponent` (Blueprint display name **Convai Player**) is added to the player's `Actor` to represent the human side of a conversation. It manages the player's session with Convai, captures microphone audio, streams it to the active chatbot session, and exposes gaze attention tracking.

Add Component path: **Convai Player**.

## Identity

These properties identify the player to Convai and are used for long-term memory association.

| Property | Type | Access | Category | Description |
|---|---|---|---|---|
| `PlayerName` | `FString` | `EditAnywhere`, `Replicated` | `Convai` | Display name used by chatbots to address this player. Default: `"User"`. Setting via the Blueprint setter calls `SetPlayerName`, which also calls the `Server Reliable` RPC `SetPlayerNameServer` so clients can update their own name. |
| `EndUserID` | `FString` | `EditAnywhere`, server-updated by setter RPC | `Convai` | End-user identity token for long-term memory. Sent to Convai at connect time. The Blueprint setter calls `SetEndUserIDServer` when the component is replicated, updating the server copy. |
| `EndUserMetadata` | `FString` | `EditAnywhere`, server-updated by setter RPC | `Convai` | JSON string with additional user metadata for LTM. The Blueprint setter calls `SetEndUserMetadataServer` when the component is replicated, updating the server copy. |

{% hint style="info" %}
`SetPlayerName`, `SetEndUserID`, and `SetEndUserMetadata` each have a corresponding `Server Reliable` RPC (`SetPlayerNameServer`, `SetEndUserIDServer`, `SetEndUserMetadataServer`). In current source, only `PlayerName` is registered with `DOREPLIFETIME`; `EndUserID` and `EndUserMetadata` are updated on the server through their setter RPCs but are not property-replicated back to other clients.
{% endhint %}

## Session

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `bAutoInitializeSession` | `bool` | `true` | `Convai\|Session` | When `true`, calls `StartSession` automatically after the Convai connection state reaches `Connected`. |

### Session functions

| Function | Inputs | Returns | Category | Description |
|---|---|---|---|---|
| `StartSession` | — | `bool` | `Convai\|Session` | Opens the WebRTC channel for this player. Returns `true` when the session initialized successfully. |
| `StopSession` | — | — | `Convai\|Session` | Closes the channel. Calling `StartSession` again reopens it. |
| `IsPlayerConnected` | — | `bool` | `Convai\|Session` | `BlueprintPure`. Returns `true` when the session is in the `EC_ConnectionState::Connected` state. |
| `SendText` | `ChatbotComponent (UConvaiConversationComponent*)`, `Text (FString)` | — | `Convai\|Session` | Sends `Text` on the player's active session, bypassing the microphone pipeline. In current source, the `ChatbotComponent` pin is present in the signature but is not used by the implementation. |

See [Session lifecycle](../core-concepts/session-lifecycle.md) for connection states and session start/stop behavior.

## Microphone capture

The player component captures microphone audio through an attached `UConvaiAudioCaptureComponent` and feeds it to the active session.

### Device selection

| Function | Inputs | Returns / outputs | Category | Description |
|---|---|---|---|---|
| `GetDefaultCaptureDeviceInfo` | — | `bool` return, `OutInfo (FCaptureDeviceInfoBP)` out | `Convai\|Microphone` | **Current source:** validates `AudioCaptureComponent`, then always returns `false` without populating `OutInfo`. Do not rely on `OutInfo` from this node. Use `GetAvailableCaptureDeviceDetails` or `GetActiveCaptureDevice` instead. See [Microphone and audio capture](microphone-and-audio-capture.md). |
| `GetCaptureDeviceInfo` | `DeviceIndex (int)` | `bool` return, `OutInfo (FCaptureDeviceInfoBP)` out | `Convai\|Microphone` | Returns info for the capture device at the given `DeviceIndex`. |
| `GetAvailableCaptureDeviceDetails` | — | `TArray<FCaptureDeviceInfoBP>` return | `Convai\|Microphone` | Returns details for all available capture devices. |
| `GetAvailableCaptureDeviceNames` | — | `TArray<FString>` return | `Convai\|Microphone` | Returns the display names of all available capture devices. |
| `GetActiveCaptureDevice` | — | `OutInfo (FCaptureDeviceInfoBP)` out | `Convai\|Microphone` | Populates `OutInfo` with the currently selected capture device. |
| `SetCaptureDeviceByIndex` | `DeviceIndex (int)` | `bool` return | `Convai\|Microphone` | Switches to the device at the given index. Returns `false` on failure. |
| `SetCaptureDeviceByName` | `DeviceName (FString)` | `bool` return | `Convai\|Microphone` | Switches to the last device in the enumerated list whose name matches `DeviceName`. Returns `false` when no match is found. |

`FCaptureDeviceInfoBP` fields:

| Field | Type | Description |
|---|---|---|
| `DeviceName` | `FString` | Human-readable device name. |
| `DeviceIndex` | `int` | Index in the device list. |
| `LongDeviceId` | `FString` | Platform-specific device identifier. |
| `InputChannels` | `int` | Number of input channels. |
| `PreferredSampleRate` | `int` | Device's preferred sample rate. |
| `bSupportsHardwareAEC` | `bool` | `true` when the device supports hardware acoustic echo cancellation. |

`FCaptureDeviceInfoBP` is also documented alongside the audio capture component in [Microphone and audio capture](microphone-and-audio-capture.md).

### Volume

| Function | Inputs | Outputs | Category | Description |
|---|---|---|---|---|
| `SetMicrophoneVolumeMultiplier` | `InVolumeMultiplier (float)` | `Success (bool)` out | `Convai\|Microphone` | Adjusts the microphone input gain. `Success` reflects whether a capture component was available, not whether microphone capture is currently streaming or recording. |
| `GetMicrophoneVolumeMultiplier` | — | `OutVolumeMultiplier (float)` out, `Success (bool)` out | `Convai\|Microphone` | Reads the current microphone volume multiplier. `Success` reflects capture-component availability. |

## Audio streaming and recording

### Streaming

These functions control whether microphone audio is sent to the active session in real time.

| Function | Returns | Category | Description |
|---|---|---|---|
| `UnmuteStreamingAudio` | `bool` | `Convai\|Session` | Starts forwarding microphone audio to the session. Returns `true` on success. |
| `MuteStreamingAudio` | — | `Convai\|Session` | Stops forwarding microphone audio. |
| `GetIsStreaming` (display name **Is Streaming**) | `bool` | `Convai\|Microphone` | `BlueprintPure`. `true` while microphone audio is being streamed. |

### Recording

Use recording to capture a complete utterance and obtain a `USoundWave`.

| Function | Returns | Category | Description |
|---|---|---|---|
| `StartRecording` | — | `Convai\|Microphone` | Begins buffering microphone audio. Call `FinishRecording` to stop and retrieve the audio. |
| `FinishRecording` | `USoundWave*` | `Convai\|Microphone` | Stops recording and returns the captured audio as a `USoundWave`. Returns `null` when no audio was recorded. |
| `GetIsRecording` (display name **Is Recording**) | `bool` | `Convai\|Microphone` | `BlueprintPure`. `true` while recording is in progress. |

## Mute and voice activity detection

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `bMute` | `bool` | `false` | `Convai\|AudioProcessing` | When `true`, blocks the direct non-audio-processing streaming path. With an active `IConvaiAudioProcessingInterface`, processed audio can still be forwarded by the current implementation. |

| Function | Inputs | Returns | Category | Description |
|---|---|---|---|---|
| `UpdateVadBP` | `EnableVAD (bool)` | `bool` | `Convai\|AudioProcessing` | Enables or disables voice activity detection. Returns `false` when VAD is not supported by the active audio processing component. |

## Gaze attention

Gaze attention lets the player component automatically promote in-scene objects to the chatbot's "object in attention" based on where the player is looking. Enable the system with `bEnableGazeAttention`. For the full cross-component API, defaults, events, and version-specific highlight behavior, see [Gaze attention reference](../features/gaze-attention/gaze-attention-reference.md).

### Core settings

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `bEnableGazeAttention` | `bool` | `false` | `Convai\|Gaze Attention` | Master switch. All gaze attention properties below are inactive when this is `false`. |
| `GazeShouldRespond` | `EC_RunLLMOption` | `Never` | `Convai\|Gaze Attention` | Controls whether the chatbot replies when an object is promoted to attention: `Never` (silent update), `Auto` (LLM decides), or `Always` (forced reply). |
| `GazeAttentionText` | `FString` | `""` | `Convai\|Gaze Attention` | Narrative event text sent alongside the attention promotion. Has no effect when `GazeShouldRespond` is `Never`. |
| `GazeAttentionDelay` | `float` | `1.0` | `Convai\|Gaze Attention` | Sustained gaze duration in seconds before an object is promoted to "in attention". |
| `GazeAttentionLossDelay` | `float` | `5.0` | `Convai\|Gaze Attention` | Look-away duration in seconds before the current attention slot is released. |
| `GazeMaxDistance` | `float` | `5000.0` | `Convai\|Gaze Attention` (Advanced) | Maximum line-trace distance from the camera in world units (cm). |
| `GazeAngleTolerance` | `float` | `5.0` | `Convai\|Gaze Attention` | Half-angle of a dot-product fallback cone (degrees) used when the strict line trace does not engage a valid gaze target and is not blocked by non-Convai geometry. `0` disables the fallback. |
| `GazeTraceChannel` | `ECollisionChannel` | `ECC_Visibility` | `Convai\|Gaze Attention` (Advanced) | Collision channel used by the gaze line trace. |

`GazeShouldRespond` accepts `EC_RunLLMOption` values (`Auto`, `Always`, `Never`). For value descriptions, see [Data types and enums](data-types-and-enums.md).

### Highlight settings

These settings control the silhouette overlay drawn over the gazed-at object.

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `GazeHighlightActorClass` | `TSubclassOf<AConvaiGazeHighlightActor>` | Plugin default | `Convai\|Gaze Attention\|Highlight` | The actor class spawned to show the highlight. Subclass `AConvaiGazeHighlightActor` for a custom visual. |
| `GazeHighlightColor` | `FLinearColor` | `(1.0, 0.9, 0.2, 1.0)` | `Convai\|Gaze Attention\|Highlight` | Tint applied to the silhouette or wireframe. |
| `GazeOverlayMaterial` | `TSoftObjectPtr<UMaterialInterface>` | Unset | `Convai\|Gaze Attention\|Highlight` | Overlay material applied via `UMeshComponent::SetOverlayMaterial`. Leave unset to use the plugin's built-in Fresnel-rim material (`/ConvAI/Highlights/M_ConvaiGazeOverlay`). The material must expose an `EmissiveColor` vector parameter. |
| `GazeHighlightEmissiveIntensity` | `float` | `2.5` | `Convai\|Gaze Attention\|Highlight` (Advanced) | Forwarded to the highlight actor's `EmissiveIntensity` scalar parameter. The plugin overlay material multiplies `EmissiveColor` by this value internally. |

### Cursor settings

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `bShowGazeCursor` | `bool` | `true` | `Convai\|Gaze Attention\|Cursor` | Shows a small reticle at screen center while gaze tracking is active. |
| `bAlwaysShowGazeCursor` | `bool` | `false` | `Convai\|Gaze Attention\|Cursor` | When `true`, the cursor stays in its Active color even when no Convai object is under the gaze. |
| `GazeCursorWidgetClass` | `TSubclassOf<UConvaiGazeCursorWidget>` | Plugin default | `Convai\|Gaze Attention\|Cursor` | Widget class used to draw the cursor. |
| `GazeCursorActiveColor` | `FLinearColor` | White | `Convai\|Gaze Attention\|Cursor` | Cursor color while the gaze is on a `UConvaiObjectComponent`. |
| `GazeCursorIdleColor` | `FLinearColor` | `(1.0, 1.0, 1.0, 0.0)` | `Convai\|Gaze Attention\|Cursor` (Advanced) | Cursor color while the gaze is on nothing. Default alpha `0.0` makes the cursor fully transparent when idle. |
| `GazeCursorDotSize` | `float` | `6.0` | `Convai\|Gaze Attention\|Cursor` (Advanced) | Edge length of the cursor square in Slate units. |
| `GazeCursorFadeInTime` | `float` | `0.1` | `Convai\|Gaze Attention\|Cursor` (Advanced) | Seconds to fade the cursor from idle to active when gaze first hits a Convai object. |
| `GazeCursorFadeOutTime` | `float` | `0.25` | `Convai\|Gaze Attention\|Cursor` (Advanced) | Seconds to fade the cursor from active to idle when gaze leaves a Convai object. |

## Events (Blueprint-assignable delegates)

Bind these in the player Blueprint using the **Assign** node on the `Convai Player` component reference.

### Inherited from `UConvaiConversationComponent`

| Event | Category | Fires when |
|---|---|---|
| `OnTranscriptionReceivedDelegate` | `Convai\|Transcription` | A speech-to-text update arrives for this player's utterance. Parameters: `Speaker`, `Listener`, `Transcription (FString)`, `IsTranscriptionReady (bool)`, `IsFinal (bool)`. |
| `OnAttendeeConnectionStateChangedEvent` | `Convai\|Connection` | An attendee's connection state changes. Parameters: `ConvaiConversationComponent`, `AttendeeID (FString)`, `ConnectionState (EC_ConnectionState)`. |

### Gaze events

All four gaze delegates carry the same signature: `PlayerComponent (UConvaiPlayerComponent*)` and `ObjectComponent (UConvaiObjectComponent*)`.

Most gaze events fire while `bEnableGazeAttention` is `true`; `OnAttentionLost` can also fire during teardown when gaze attention is disabled.

| Event | Category | Fires when |
|---|---|---|
| `OnGazeBegin` | `Convai\|Gaze Attention\|Events` | The player's gaze first enters the bounds of a `UConvaiObjectComponent`. Fires before any attention threshold. |
| `OnGazeEnd` | `Convai\|Gaze Attention\|Events` | The player's gaze leaves a `UConvaiObjectComponent`, regardless of whether it had been promoted to attention. |
| `OnAttentionGained` | `Convai\|Gaze Attention\|Events` | The sustained-gaze dwell threshold (`GazeAttentionDelay`) was reached and gaze promotion was attempted. Fires even when every chatbot rejects the update. |
| `OnAttentionLost` | `Convai\|Gaze Attention\|Events` | The attention slot is released: the player looked away for longer than `GazeAttentionLossDelay`, another object took the slot, or the attention target was destroyed. |

See [Event system](../core-concepts/event-system.md) for binding patterns and full parameter details. For microphone setup and gaze task flows, see [Configure the microphone](../getting-started/configure-microphone.md) and [Gaze attention reference](../features/gaze-attention/gaze-attention-reference.md).

## Related reference

{% content-ref url="convai-chatbot-component.md" %}
[Convai Chatbot Component](convai-chatbot-component.md)
{% endcontent-ref %}

{% content-ref url="microphone-and-audio-capture.md" %}
[Microphone and audio capture](microphone-and-audio-capture.md)
{% endcontent-ref %}

{% content-ref url="../core-concepts/session-lifecycle.md" %}
[Session lifecycle](../core-concepts/session-lifecycle.md)
{% endcontent-ref %}

{% content-ref url="../core-concepts/event-system.md" %}
[Event system](../core-concepts/event-system.md)
{% endcontent-ref %}
