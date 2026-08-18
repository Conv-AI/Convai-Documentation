---
title: Microphone and audio capture
description: Reference for microphone device enumeration, selection, volume, and persisted settings on the Convai Player Component and the microphone subsystem.
last_reviewed: "4.0.0-beta.27"
---

`UConvaiPlayerComponent` exposes all Blueprint-callable microphone functions under the `Convai|Microphone` category. Internally it drives a `UConvaiAudioCaptureComponent` instance that wraps the Unreal `AudioCapture` engine plugin, and persists the player's chosen device and gain across sessions through `UConvaiMicrophoneSubsystem`. On Android, the `AndroidPermission` plugin handles the runtime microphone permission.

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

### Persisted settings

| Function | Parameters | Returns | Description |
|---|---|---|---|
| `SaveMicrophoneSettings` | — | `bool` | Snapshots the player component's current capture device and gain, then persists them through `UConvaiMicrophoneSubsystem`. Call this after the player commits a device choice — selecting a device only applies it for the current session until this is called. Returns `false` when the subsystem is not available. |
| `ApplySavedMicrophoneSettings` | — | `bool` | Re-applies the persisted device (skipping it if no longer plugged in) and gain to the player component. Called automatically during `BeginPlay`; call it again from a UI that needs to revert unsaved changes. Returns `false` when the subsystem is not available. |

Both functions delegate to `UConvaiMicrophoneSubsystem`, documented below.

## UConvaiMicrophoneSubsystem

`UConvaiMicrophoneSubsystem` (Blueprint display name **Convai Microphone Subsystem**) is a `UGameInstanceSubsystem` that owns the player's microphone device and gain preference across sessions, so the selection no longer resets to the system default at every launch. Every Blueprint-exposed member on it uses `Category = "Convai|Microphone"`.

| Node | Kind | Parameters | Returns | Description |
|---|---|---|---|---|
| `Get` (display name **Get**, derived — no explicit `DisplayName` meta) | `BlueprintPure`, static | `WorldContextObject` | `UConvaiMicrophoneSubsystem*` | Returns the subsystem instance for the current game instance. |
| `GetMicrophoneSettings` (display name **Get Microphone Settings**) | `BlueprintPure` | — | `FConvaiMicrophoneSettings` | Returns the settings currently held by the subsystem. |
| `HasSavedMicrophoneSettings` (display name **Has Saved Microphone Settings**) | `BlueprintPure` | — | `bool` | `true` when a saved record was found on disk this session, as opposed to falling back to defaults. |
| `SaveMicrophoneSettings` (display name **Save Microphone Settings**) | `BlueprintCallable` | `InSettings (FConvaiMicrophoneSettings)` | — | Replaces the held settings and writes them to the shared record. Broadcasts `OnMicrophoneSettingsChanged`. Takes an explicit settings value — distinct from the identically named node on `UConvaiPlayerComponent`, which reads the component's live device and gain instead. |
| `SaveMicrophoneSettingsFromPlayerComponent` (display name **Save Microphone Settings From Player Component**) | `BlueprintCallable` | `PlayerComponent (UConvaiPlayerComponent)` | `bool` | Snapshots `PlayerComponent`'s live capture device and gain, then persists them. This is what `UConvaiPlayerComponent::SaveMicrophoneSettings` calls internally. |
| `ResetMicrophoneSettingsToDefaults` (display name **Reset Microphone Settings To Defaults**) | `BlueprintCallable` | — | — | Forgets the saved choice and deletes the shared record. |
| `GetAvailableMicrophoneNames` (display name **Get Available Microphone Names**) | `BlueprintCallable` | — | `TArray<FString>` | Device names present right now, with the same naming as `UConvaiPlayerComponent::GetAvailableCaptureDeviceNames`. |
| `IsSavedMicrophoneAvailable` (display name **Is Saved Microphone Available**) | `BlueprintCallable` | — | `bool` | `true` when a device is saved and it is plugged in right now. `false` with nothing saved is the normal "follow the system default" case, not an error. |
| `ApplySavedSettingsToPlayerComponent` (display name **Apply Saved Settings To Player Component**) | `BlueprintCallable` | `PlayerComponent (UConvaiPlayerComponent)` | `bool` | Applies the saved gain, plus the saved device if it is still available, to `PlayerComponent`. Returns `true` only when a saved device was resolved and selected. |
| `OnMicrophoneSettingsChanged` (display name **On Microphone Settings Changed**) | `BlueprintAssignable` event | `NewSettings (FConvaiMicrophoneSettings)` | — | Broadcast whenever `SaveMicrophoneSettings` runs on the subsystem. |

## FConvaiMicrophoneSettings

`FConvaiMicrophoneSettings` (`BlueprintType`, `Category = "Convai|Microphone"`) is the struct `UConvaiMicrophoneSubsystem` persists.

| Field | Type | Default | Description |
|---|---|---|---|
| `InputDeviceName` | `FString` | `""` | Empty means the system default device. Otherwise a `DeviceName` value from `UConvaiPlayerComponent::GetAvailableCaptureDeviceNames`. |
| `InputGain` | `float` | `1.0` | Multiplier applied to microphone input gain. `1.0` is unchanged; the editor UI clamps the field to the `0.0`–`2.0` range. |

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
