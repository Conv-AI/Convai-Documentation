---
title: Convai Player Component
description: Reference for the player conversation component — every Blueprint-visible property, function, and event exposed by the Convai Player Component.
last_reviewed: "2026-06-05"
---

`UConvaiPlayerComponent` (Blueprint display name **Convai Player**) is added to the player's `Actor` to represent the human side of a conversation. It manages the player's session with Convai, captures microphone audio, streams it to the active chatbot session, and exposes gaze attention tracking.

Add it to the player pawn through the **Add Component** button in the **Details** panel.

## Identity

These properties identify the player to Convai and are used for long-term memory association.

| Property | Type | Access | Category | Description |
|---|---|---|---|---|
| `PlayerName` | `FString` | `EditAnywhere`, `Replicated` | `Convai` | Display name used by chatbots to address this player. Setting via the Blueprint setter calls `SetPlayerName`, which also calls the `Server Reliable` RPC `SetPlayerNameServer` so clients can update their own name. |
| `EndUserID` | `FString` | `EditAnywhere`, `Replicated` | `Convai` | End-user identity token for long-term memory. Sent to Convai at connect time. Use the Blueprint setter `SetEndUserID` to trigger replication. |
| `EndUserMetadata` | `FString` | `EditAnywhere`, `Replicated` | `Convai` | JSON string with additional user metadata for LTM. Use the Blueprint setter `SetEndUserMetadata` to trigger replication. |

{% hint style="info" %}
`SetPlayerName`, `SetEndUserID`, and `SetEndUserMetadata` each have a corresponding `Server Reliable` RPC (`SetPlayerNameServer`, `SetEndUserIDServer`, `SetEndUserMetadataServer`). These are called automatically by the Blueprint setter so that a locally owned client pawn can update its own identity and have the change propagate to the server.
{% endhint %}

## Session

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `bAutoInitializeSession` | `bool` | `true` | `Convai\|Session` | When `true`, calls `StartSession` automatically in `BeginPlay`. |

### Session functions

| Function | Inputs | Returns | Category | Description |
|---|---|---|---|---|
| `StartSession` | — | `bool` | `Convai\|Session` | Opens the WebRTC channel for this player. Returns `true` when the session initialized successfully. |
| `StopSession` | — | — | `Convai\|Session` | Closes the channel. Calling `StartSession` again reopens it. |
| `IsPlayerConnected` | — | `bool` | `Convai\|Session` | `BlueprintPure`. Returns `true` when the session is in the `EC_ConnectionState::Connected` state. |
| `SendText` | `ChatbotComponent (UConvaiConversationComponent*)`, `Text (FString)` | — | `Convai\|Session` | Sends a text message directly to a chatbot component, bypassing the microphone pipeline. |

See [Session lifecycle](../core-concepts/session-lifecycle.md) for connection states and multiplayer replication details.

## Microphone capture

The player component captures microphone audio through an attached `UConvaiAudioCaptureComponent` and feeds it to the active session.

### Device selection

| Function | Returns | Category | Description |
|---|---|---|---|
| `GetDefaultCaptureDeviceInfo` | `bool`, `OutInfo (FCaptureDeviceInfoBP)` | `Convai\|Microphone` | Populates `OutInfo` with the system default capture device details. Returns `false` when no device is available. |
| `GetCaptureDeviceInfo` | `bool`, `OutInfo (FCaptureDeviceInfoBP)` | `Convai\|Microphone` | Returns info for the capture device at the given `DeviceIndex`. |
| `GetAvailableCaptureDeviceDetails` | `TArray<FCaptureDeviceInfoBP>` | `Convai\|Microphone` | Returns details for all available capture devices. |
| `GetAvailableCaptureDeviceNames` | `TArray<FString>` | `Convai\|Microphone` | Returns the display names of all available capture devices. |
| `GetActiveCaptureDevice` | `OutInfo (FCaptureDeviceInfoBP)` | `Convai\|Microphone` | Populates `OutInfo` with the device currently in use. |
| `SetCaptureDeviceByIndex` | `bool` | `Convai\|Microphone` | Switches to the device at the given index. Returns `false` on failure. |
| `SetCaptureDeviceByName` | `bool` | `Convai\|Microphone` | Switches to the first device whose name matches `DeviceName`. Returns `false` when no match is found. |

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

| Function | Inputs | Category | Description |
|---|---|---|---|
| `SetMicrophoneVolumeMultiplier` | `InVolumeMultiplier (float)`, `Success (bool)` out | `Convai\|Microphone` | Adjusts the microphone input gain. `Success` is `false` when no capture device is active. |
| `GetMicrophoneVolumeMultiplier` | — | `Convai\|Microphone` | Returns `OutVolumeMultiplier (float)` and `Success (bool)`. |

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
| `bMute` | `bool` | `false` | `Convai\|AudioProcessing` | When `true`, the player's microphone audio is silenced before it reaches the session. |

| Function | Inputs | Returns | Category | Description |
|---|---|---|---|---|
| `UpdateVadBP` | `EnableVAD (bool)` | `bool` | `Convai\|AudioProcessing` | Enables or disables voice activity detection. Returns `false` when VAD is not supported by the active audio processing component. |

## Gaze attention

Gaze attention lets the player component automatically promote in-scene objects to the chatbot's "object in attention" based on where the player is looking. Enable the system with `bEnableGazeAttention`.

### Core settings

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `bEnableGazeAttention` | `bool` | `false` | `Convai\|Gaze Attention` | Master switch. All gaze attention properties below are inactive when this is `false`. |
| `GazeShouldRespond` | `EC_RunLLMOption` | `Never` | `Convai\|Gaze Attention` | Controls whether the chatbot replies when an object is promoted to attention: `Never` (silent update), `Auto` (LLM decides), or `Always` (forced reply). |
| `GazeAttentionText` | `FString` | `""` | `Convai\|Gaze Attention` | Narrative event text sent alongside the attention promotion. Has no effect when `GazeShouldRespond` is `Never`. |
| `GazeAttentionDelay` | `float` | `1.0` | `Convai\|Gaze Attention` | Sustained gaze duration in seconds before an object is promoted to "in attention". |
| `GazeAttentionLossDelay` | `float` | `5.0` | `Convai\|Gaze Attention` | Look-away duration in seconds before the current attention slot is released. |
| `GazeMaxDistance` | `float` | `5000.0` | `Convai\|Gaze Attention` (Advanced) | Maximum line-trace distance from the camera in world units (cm). |
| `GazeAngleTolerance` | `float` | `5.0` | `Convai\|Gaze Attention` | Half-angle of a dot-product fallback cone (degrees) used when the strict line trace does not hit anything. `0` disables the fallback. |
| `GazeTraceChannel` | `ECollisionChannel` | `ECC_Visibility` | `Convai\|Gaze Attention` (Advanced) | Collision channel used by the gaze line trace. |

`GazeShouldRespond` accepts `EC_RunLLMOption` values (`Auto`, `Always`, `Never`). For value descriptions, see [Data types and enums](data-types-and-enums.md).

### Highlight settings

These settings control the silhouette overlay drawn over the gazed-at object.

| Property | Type | Default | Category | Description |
|---|---|---|---|---|
| `GazeHighlightActorClass` | `TSubclassOf<AConvaiGazeHighlightActor>` | Plugin default | `Convai\|Gaze Attention\|Highlight` | The actor class spawned to show the highlight. Subclass `AConvaiGazeHighlightActor` for a custom visual. |
| `GazeHighlightColor` | `FLinearColor` | `(1.0, 0.9, 0.2, 1.0)` | `Convai\|Gaze Attention\|Highlight` | Tint applied to the silhouette or wireframe. |
| `GazeOverlayMaterial` | `TSoftObjectPtr<UMaterialInterface>` | Plugin default | `Convai\|Gaze Attention\|Highlight` | Overlay material applied via `UMeshComponent::SetOverlayMaterial`. Leave unset to use the plugin's built-in Fresnel-rim material (`/ConvAI/Highlights/M_ConvaiGazeOverlay`). The material must expose an `EmissiveColor` vector parameter. |
| `GazeHighlightEmissiveIntensity` | `float` | `2.5` | `Convai\|Gaze Attention\|Highlight` (Advanced) | Multiplier on `GazeHighlightColor` before it is passed to the `EmissiveColor` parameter. |

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

Gaze events only fire when `bEnableGazeAttention` is `true`.

| Event | Category | Fires when |
|---|---|---|
| `OnGazeBegin` | `Convai\|Gaze Attention\|Events` | The player's gaze first enters the bounds of a `UConvaiObjectComponent`. Fires before any attention threshold. |
| `OnGazeEnd` | `Convai\|Gaze Attention\|Events` | The player's gaze leaves a `UConvaiObjectComponent`, regardless of whether it had been promoted to attention. |
| `OnAttentionGained` | `Convai\|Gaze Attention\|Events` | A gazed-at object is promoted to "in attention" after the sustained-gaze period (`GazeAttentionDelay`). |
| `OnAttentionLost` | `Convai\|Gaze Attention\|Events` | The attention slot is released: the player looked away for longer than `GazeAttentionLossDelay`, another object took the slot, or the attention target was destroyed. |

See [Event system](../core-concepts/event-system.md) for binding patterns and full parameter details.

## Blueprint usage patterns

### Push-to-talk recording

On an **Input Action Pressed** event for your push-to-talk key, call `StartRecording` on the player component. On the corresponding **Input Action Released** event, call `FinishRecording` — it returns a `USoundWave`. To send the captured utterance as a text message to a chatbot, pass the `USoundWave` through a speech-to-text node, then feed the transcription string to `SendText`. Alternatively, unmute streaming audio (`UnmuteStreamingAudio`) on press and mute it on release (`MuteStreamingAudio`) to stream live microphone audio to the active session instead.

### Populating a microphone device picker

Call `GetAvailableCaptureDeviceNames` on `BeginPlay` and wire the returned `TArray<FString>` into a **Create Widget** flow that feeds a **ComboBox (String)**. Bind the **On Selection Changed** event of the combo box to a custom event that calls `SetCaptureDeviceByName` with the selected string. To pre-select the active device, call `GetActiveCaptureDevice` and match `DeviceName` against the list.

### Enabling gaze attention and reacting to object focus

Set `bEnableGazeAttention = true` on the player component. Configure `GazeAttentionDelay` (default `1.0` s) for how long the player must look before attention is promoted, and `GazeAttentionLossDelay` (default `5.0` s) for how long they can look away before it is released. Bind the **On Attention Gained** event on the player component — it fires with `PlayerComponent` and `ObjectComponent` pins. From `ObjectComponent`, get the object's name or tag to determine which object gained focus and drive UI highlights, dialogue triggers, or state changes.

## Troubleshooting

### Player not connecting

**Cause:** `StartSession` was never called, or `bAutoInitializeSession` was set to `false` without a manual `StartSession` call in `BeginPlay`.

**Fix:** Confirm `bAutoInitializeSession` is `true`, or add a `StartSession` call in `BeginPlay`. Check the Output Log for `Convai:` errors — a missing API key in **Project Settings → Plugins → Convai** also prevents connection.

**Verify:** Call `IsPlayerConnected` after a short delay — it should return `true` once the WebRTC channel is open.

### Microphone not capturing audio

**Cause:** The device index passed to `SetCaptureDeviceByIndex` is out of range, or on Android the microphone permission has not been granted.

**Fix:** Call `GetAvailableCaptureDeviceDetails` and inspect the returned array to confirm the intended device index is valid. On Android, call `AndroidRequestMicrophonePermission` before starting the session and verify the permission is granted before capturing.

**Verify:** Call `GetIsStreaming` after `UnmuteStreamingAudio` — it should return `true`. If it returns `false`, no capture device is active.

### Gaze highlight does not appear

**Cause:** Either `bEnableGazeAttention` is `false` (the master switch is off) or `GazeHighlightActorClass` is unset, so no highlight actor is spawned when gaze hits an object.

**Fix:** Confirm `bEnableGazeAttention` is `true` on the player component. If `GazeHighlightActorClass` is empty, the plugin uses its built-in default — verify the plugin content is present under `/ConvAI/Highlights/`. For a custom visual, set `GazeHighlightActorClass` to a subclass of `AConvaiGazeHighlightActor`.

**Verify:** Enable `bShowGazeCursor` and confirm the cursor appears at screen center — if the cursor shows but no highlight, the issue is in `GazeHighlightActorClass`. If neither appears, `bEnableGazeAttention` is likely `false`.

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
