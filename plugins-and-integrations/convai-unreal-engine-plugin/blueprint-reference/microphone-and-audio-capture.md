---
title: Microphone and audio capture
description: Reference for microphone device enumeration, selection, and volume on the Convai Player Component, the audio capture component, and Android permissions.
last_reviewed: "4.0.0-beta.21"
---

`UConvaiPlayerComponent` exposes all Blueprint-callable microphone functions under the `Convai|Microphone` category. Internally it drives a `UConvaiAudioCaptureComponent` instance that wraps the Unreal `AudioCapture` engine plugin. On Android, the `AndroidPermission` plugin handles the runtime microphone permission.

For the complete `UConvaiPlayerComponent` property set — identity, session, gaze attention, and audio processing — see [Convai Player Component](convai-player-component.md).

## FCaptureDeviceInfoBP

`FCaptureDeviceInfoBP` is a `BlueprintType` struct returned by the device-enumeration and selection functions. All fields are `EditAnywhere`, `BlueprintReadWrite`, `Category = "Convai|Microphone"`.

| Field | Type | Default | Description |
|---|---|---|---|
| `DeviceName` | `FString` | `""` | Human-readable name shown in device menus. |
| `DeviceIndex` | `int` | `0` | Zero-based index in the capture device list. Indices can change between sessions when devices are added or removed. |
| `LongDeviceId` | `FString` | `""` | Platform-specific device identifier. More stable than `DeviceIndex` across sessions on Windows. |
| `InputChannels` | `int` | `0` | Number of input channels reported by the device. |
| `PreferredSampleRate` | `int` | `0` | Device's preferred sample rate in Hz. |
| `bSupportsHardwareAEC` | `bool` | `false` | `true` when the device supports hardware acoustic echo cancellation. |

## Convai|Microphone functions

These `BlueprintCallable` functions are all on `UConvaiPlayerComponent` (Blueprint display name **Convai Player**).

### Device enumeration

| Function | Parameters | Returns | Description |
|---|---|---|---|
| `GetAvailableCaptureDeviceNames` | — | `TArray<FString>` | Names of all available input devices. Use these strings as display labels and as the `DeviceName` argument to `SetCaptureDeviceByName`. |
| `GetAvailableCaptureDeviceDetails` | — | `TArray<FCaptureDeviceInfoBP>` | Full `FCaptureDeviceInfoBP` structs for every available device. Includes index, long ID, channel count, sample rate, and AEC flag. |
| `GetDefaultCaptureDeviceInfo` | `OutInfo (FCaptureDeviceInfoBP)` out | `bool` | **Current source:** validates `AudioCaptureComponent`, then always returns `false` without populating `OutInfo`. Do not rely on `OutInfo` from this node. Use `GetAvailableCaptureDeviceDetails` or `GetActiveCaptureDevice` instead. |
| `GetCaptureDeviceInfo` | `OutInfo (FCaptureDeviceInfoBP)` out, `DeviceIndex (int)` | `bool` | Populates `OutInfo` for the device at `DeviceIndex`. Returns `false` when the index is out of range. |
| `GetActiveCaptureDevice` | `OutInfo (FCaptureDeviceInfoBP)` out | — | Populates `OutInfo` with the currently selected capture device. |

### Device selection

| Function | Parameters | Returns | Description |
|---|---|---|---|
| `SetCaptureDeviceByIndex` | `DeviceIndex (int)` | `bool` | Opens the capture device at `DeviceIndex`. Returns `false` when the index is out of range or the device cannot be opened. |
| `SetCaptureDeviceByName` | `DeviceName (FString)` | `bool` | Opens the last device in the enumerated list whose `DeviceName` matches the input. Returns `false` when no match is found. |

Both selection functions can be called before or during gameplay. After a successful call, `GetActiveCaptureDevice` reflects the new device.

### Volume

| Function | Parameters | Returns | Description |
|---|---|---|---|
| `SetMicrophoneVolumeMultiplier` | `InVolumeMultiplier (float)` | `Success (bool)` | Scales the captured audio signal. `Success` reflects whether a capture component is available, not whether microphone capture is currently streaming or recording. |
| `GetMicrophoneVolumeMultiplier` | — | `OutVolumeMultiplier (float)`, `Success (bool)` | Reads the current volume multiplier. `Success` reflects capture-component availability. |

`InVolumeMultiplier` has no enforced range in the API. A value of `1.0` applies no gain change. Values above `1.0` amplify the signal; values below `1.0` attenuate it. A value of `0.0` silences the captured audio while keeping the capture session active.

### Streaming and recording state

| Function | Category | Returns | Description |
|---|---|---|---|
| `GetIsStreaming` (display name **Is Streaming**) | `Convai|Microphone` | `bool` | `BlueprintPure`. `true` while microphone audio is being forwarded to the active session. |
| `GetIsRecording` (display name **Is Recording**) | `Convai|Microphone` | `bool` | `BlueprintPure`. `true` while a recording session started with `StartRecording` is in progress. |

`StartRecording`, `FinishRecording`, `UnmuteStreamingAudio`, and `MuteStreamingAudio` are documented under the **Audio streaming and recording** section of [Convai Player Component](convai-player-component.md).

## ConvaiAudioCaptureComponent

`UConvaiAudioCaptureComponent` (C++ class, `ClassGroup = Synth`) extends `USynthComponent` and wraps `FConvaiAudioCaptureSynth`, which in turn wraps the Unreal `FAudioCapture` object. `UConvaiPlayerComponent` creates and owns one instance automatically; you do not need to add `UConvaiAudioCaptureComponent` to your Actor manually.

{% hint style="info" %}
In most Blueprints, use the microphone functions on `UConvaiPlayerComponent` rather than interacting with `UConvaiAudioCaptureComponent` directly. The player component delegates internally and provides the higher-level streaming API documented in the sections above.
{% endhint %}

The component declares one Convai-specific Blueprint-configurable property; inherited `USynthComponent` properties also apply.

| Property | Type | Category | Constraints | Description |
|---|---|---|---|---|
| `JitterLatencyFrames` | `int32` | `Latency` | `ClampMin = 0`, `ClampMax = 1024` | Declared latency setting for induced jitter buffering. In current plugin source, this property is not read by the Convai capture implementation, so changing it has no verified runtime effect. |

Most device-enumeration and device-switching behavior is driven through `UConvaiPlayerComponent` — the Blueprint functions listed above delegate to the underlying `UConvaiAudioCaptureComponent` internally, except `GetDefaultCaptureDeviceInfo` on the player component, which does not currently forward to the capture component.

At the C++ layer, `UConvaiAudioCaptureComponent::GetDefaultCaptureDeviceInfo` does populate the system default device. That method is not exposed to Blueprint. The component's other device methods (`GetCaptureDevicesAvailable`, `GetCaptureDeviceInfo`, `GetActiveCaptureDevice`, `SetCaptureDevice`) are also C++ internal.

## Plugin dependencies

Both dependencies are declared in `ConvAI.uplugin` and are enabled automatically when the Convai plugin is installed. No manual plugin activation is required.

| Plugin | Enabled | Purpose |
|---|---|---|
| `AudioCapture` | `true` | Unreal Engine built-in plugin that provides `FAudioCapture` and `USynthComponent`-based capture. Required for all microphone input on Win64 and Android. |
| `AndroidPermission` | `true` | Unreal Engine built-in plugin that provides Blueprint nodes to check and request Android runtime permissions. Required for microphone access on Android. |

### Android microphone permission

On Android, the OS requires a runtime permission grant for audio capture. Without it, `UConvaiAudioCaptureComponent` initializes but captures no audio — the Convai character receives no speech input. The plugin does not log a permission-denied message, although stream-open failures can still produce capture warnings.

{% hint style="warning" %}
Request `android.permission.RECORD_AUDIO` before calling `StartSession` or `UnmuteStreamingAudio`. If the permission is denied, audio capture silently produces no data.
{% endhint %}

Use the `AndroidPermission` Blueprint nodes to request the permission:

1. Call `Check Android Permission` with the permission string `android.permission.RECORD_AUDIO`.
2. If the return value is `false`, call `Request Android Permission` for that same string.
3. Bind to the `On Permission Request Complete` delegate and start the conversation only after the permission is confirmed as granted.

The `AndroidPermission` plugin nodes are in the `Android Permission` Blueprint category. They are no-ops on Win64 — the same Blueprint graph works on both platforms without platform guards.

## Related reference

The player component page covers the full property surface; the how-to page walks through selecting and testing a device before shipping.

{% content-ref url="convai-player-component.md" %}
[Convai Player Component](convai-player-component.md)
{% endcontent-ref %}

{% content-ref url="../getting-started/configure-the-microphone.md" %}
[Configure the microphone](../getting-started/configure-the-microphone.md)
{% endcontent-ref %}
