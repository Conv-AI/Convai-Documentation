---
title: Configure the microphone
description: Select a capture device, adjust volume, and handle Android microphone permissions so player speech reaches the Convai character correctly.
last_reviewed: "4.0.0-beta.21"
---

The `UConvaiPlayerComponent` captures microphone audio through `UConvaiAudioCaptureComponent`. By default it uses the system's default capture device. Use the Blueprint functions on `UConvaiPlayerComponent` to enumerate, select, and adjust the capture device at runtime.

## Default behavior

When `UConvaiPlayerComponent` initializes, it opens the system's default microphone. No configuration is required for this path. If the default device works for your project, no additional steps are needed.

## Enumerate available devices

Call these Blueprint functions on a `UConvaiPlayerComponent` reference to list what is available:

| Function | Returns | Notes |
|---|---|---|
| `GetAvailableCaptureDeviceNames()` | `TArray<FString>` | Names of all available input devices |
| `GetAvailableCaptureDeviceDetails()` | `TArray<FCaptureDeviceInfoBP>` | Full details: name, device index, long ID, channel count, sample rate, AEC support |
| `GetDefaultCaptureDeviceInfo(OutInfo)` | `bool` | Fills `OutInfo` with the default device details |
| `GetCaptureDeviceInfo(OutInfo, DeviceIndex)` | `bool` | Fills `OutInfo` for the device at `DeviceIndex` |
| `GetActiveCaptureDevice(OutInfo)` | void | Fills `OutInfo` with the currently active device |

The `FCaptureDeviceInfoBP` struct exposes these fields:

| Field | Type | Description |
|---|---|---|
| `DeviceName` | `FString` | Human-readable device name |
| `DeviceIndex` | `int` | Index used for selection |
| `LongDeviceId` | `FString` | Platform-specific device identifier |
| `InputChannels` | `int` | Number of input channels |
| `PreferredSampleRate` | `int` | Device's preferred sample rate |
| `bSupportsHardwareAEC` | `bool` | Whether the device supports hardware echo cancellation |

## Select a capture device

To switch from the default device, call one of these functions on `UConvaiPlayerComponent`:

| Function | Selects by |
|---|---|
| `SetCaptureDeviceByIndex(DeviceIndex)` | Device index from the enumeration list |
| `SetCaptureDeviceByName(DeviceName)` | Device name string |

Both functions return `bool` — `true` if the switch succeeded. Call them before or during gameplay. A common pattern is to build a settings menu that lists `GetAvailableCaptureDeviceNames()` and calls `SetCaptureDeviceByIndex()` when the player picks a device.

## Adjust the microphone volume

```text
SetMicrophoneVolumeMultiplier(InVolumeMultiplier, Success)
GetMicrophoneVolumeMultiplier(OutVolumeMultiplier, Success)
```

`InVolumeMultiplier` scales the captured audio signal. A value of `1.0` is the default (no change). Values above `1.0` amplify the input; values below `1.0` attenuate it. Use this if the character consistently mishears quiet speakers or if your microphone has low gain.

## Android microphone permission

On Android, the operating system requires an explicit runtime permission grant before audio capture can start. The Convai plugin depends on the `AndroidPermission` engine plugin (bundled and enabled automatically) to request this permission.

{% hint style="warning" %}
Without the microphone permission on Android, `UConvaiPlayerComponent` will initialize but audio capture will silently fail — the character will not receive any speech input.
{% endhint %}

To request the permission at runtime from Blueprint, use the **Android Permission** nodes provided by the engine's `AndroidPermission` plugin. Request `android.permission.RECORD_AUDIO` at the point in your application flow where the player is about to start a conversation (for example, when the player character enters a conversation zone).

The standard pattern:

1. Call **Check Android Permission** with `android.permission.RECORD_AUDIO`.
2. If the result is `false`, call **Request Android Permission** for that permission.
3. Bind to the **On Permission Request Complete** delegate and proceed to start the conversation only when the grant is confirmed.

## Troubleshooting

### No microphone input on Android

**Symptom:** The character never receives speech; conversation does not start after the player speaks.

**Cause:** The `android.permission.RECORD_AUDIO` runtime permission was not granted before audio capture was initialized. Without it, `UConvaiAudioCaptureComponent` initializes silently but captures nothing.

**Fix:** Request the permission at runtime using the `AndroidPermission` engine plugin nodes (see [Android microphone permission](#android-microphone-permission) above). Call **Check Android Permission** → if `false`, call **Request Android Permission** → bind **On Permission Request Complete** and start the conversation only on a granted result.

**Verify:** After granting the permission, enter Play mode and speak. The character should receive and respond to voice input.

### Device selection returns false

**Symptom:** `SetCaptureDeviceByIndex()` or `SetCaptureDeviceByName()` returns `false`.

**Cause:** The requested device index is out of range, or the device name does not match any entry in `GetAvailableCaptureDeviceNames()`.

**Fix:** Call `GetAvailableCaptureDeviceNames()` first and use only the names and indices from that list. Indices can change between sessions if devices are added or removed.

**Verify:** Call `GetActiveCaptureDevice(OutInfo)` after selection and confirm `OutInfo.DeviceName` matches the intended device.

## Next steps

- [Configure conversation input](configure-conversation-input.md) — set push-to-talk or hands-free mode.
- [Validate your setup](validate-your-setup.md) — verify the full pipeline is working.
