---
title: Configure the microphone
description: Select a capture device, adjust volume, and handle Android microphone permissions so player speech reaches the Convai character correctly.
last_reviewed: "4.0.0-beta.21"
---

`UConvaiPlayerComponent` captures microphone audio through `UConvaiAudioCaptureComponent`. By default it opens the system's default capture device at initialization. Use the Blueprint functions on `UConvaiPlayerComponent` to enumerate, select, and adjust the capture device at runtime.

## Default behavior

When `UConvaiPlayerComponent` initializes, it opens the system's default microphone automatically. No additional configuration is required for this path. If the default device works for your project, skip to [Configure character audio](configure-character-audio.md).

## Enumerate available devices

Call these Blueprint functions on a `UConvaiPlayerComponent` reference to list available input devices:

| Function | Returns | Notes |
|---|---|---|
| `GetAvailableCaptureDeviceNames()` | `TArray<FString>` | Names of all available input devices. |
| `GetAvailableCaptureDeviceDetails()` | `TArray<FCaptureDeviceInfoBP>` | Full details: name, index, long ID, channel count, sample rate, AEC support. |
| `GetCaptureDeviceInfo(OutInfo, DeviceIndex)` | `bool` | Fills `OutInfo` for the device at `DeviceIndex`. |
| `GetActiveCaptureDevice(OutInfo)` | `void` | Fills `OutInfo` with the currently active device. |

The `FCaptureDeviceInfoBP` struct exposes these fields:

| Field | Type | Description |
|---|---|---|
| `DeviceName` | `FString` | Human-readable device name. |
| `DeviceIndex` | `int` | Index used for selection. |
| `LongDeviceId` | `FString` | Platform-specific device identifier. |
| `InputChannels` | `int` | Number of input channels. |
| `PreferredSampleRate` | `int` | Device's preferred sample rate. |
| `bSupportsHardwareAEC` | `bool` | Whether the device supports hardware echo cancellation. |

## Select a capture device

To switch from the default device, call one of these functions on `UConvaiPlayerComponent`:

| Function | Selects by | Returns |
|---|---|---|
| `SetCaptureDeviceByIndex(DeviceIndex)` | Device index from the enumeration list. | `bool` — `true` if the switch succeeded. |
| `SetCaptureDeviceByName(DeviceName)` | Device name string. | `bool` — `true` if the switch succeeded. |

Call either function while audio capture is active (for example, during an active push-to-talk or VAD session). A common pattern is to build a settings menu that lists `GetAvailableCaptureDeviceNames()` and calls `SetCaptureDeviceByIndex()` when the player picks a device. Device selection before capture starts may not take effect until the next capture session.

## Adjust the microphone volume

| Function | Parameters | Returns | Description |
|---|---|---|---|
| `SetMicrophoneVolumeMultiplier` | `InVolumeMultiplier` (`float`), `Success` (`bool&`) | `void` | Scales the captured audio signal. `1.0` is the default (no change); values above `1.0` amplify, values below attenuate. |
| `GetMicrophoneVolumeMultiplier` | `OutVolumeMultiplier` (`float&`), `Success` (`bool&`) | `void` | Returns the current volume multiplier. |

Use `SetMicrophoneVolumeMultiplier` if the character consistently mishears quiet speakers or if your microphone has low gain.

## Android microphone permission

On Android and standalone VR builds (such as Meta Quest), the operating system requires an explicit runtime permission grant before audio capture can start. The Convai plugin depends on the `AndroidPermission` engine plugin — bundled and enabled automatically — to request this permission.

{% hint style="warning" %}
Without the microphone permission on Android, `UConvaiPlayerComponent` will initialize but audio capture will silently fail. The character will not receive any speech input.
{% endhint %}

### Prepare the Android build

{% stepper %}
{% step %}
### Enable the Android Permission plugin

In the Unreal Editor, open **Edit > Plugins**, search for `Android Permission`, and confirm it is enabled. Restart the editor if prompted.
{% endstep %}

{% step %}
### Declare the permission in Project Settings

Open **Edit > Project Settings > Platforms > Android > Advanced APK Packaging**. Under **Extra Permissions**, click **+** and add:

```text
android.permission.RECORD_AUDIO
```

Save Project Settings.
{% endstep %}
{% endstepper %}

### Request permission at runtime

Request `android.permission.RECORD_AUDIO` at the point in your application where the player is about to start a conversation — for example, in your Game Mode or Player Controller **BeginPlay** event, or when the player enters a conversation zone.

Use the **Android Permission** nodes from the `AndroidPermission` engine plugin:

1. Call **Check Android Permission** with `android.permission.RECORD_AUDIO`.
2. If the result is `false`, call **Request Android Permission** for that permission (or **Request Android Permissions** with a string array containing `android.permission.RECORD_AUDIO`).
3. Bind to **On Permission Request Complete** (or **On Permissions Granted**) and start the conversation only when the grant is confirmed.

Simplified Blueprint flow:

```text
Event BeginPlay → Delay (0.5s) → Check Android Permission (RECORD_AUDIO) → Branch
  → True: start conversation / enable voice input
  → False: Request Android Permission → On grant confirmed: start conversation
```

If the player previously denied the permission, enable **Microphone** manually under the device's app settings before testing again.

On Quest devices: **Settings > Apps > [Your App] > Permissions > Microphone > Allow**.

After permission is granted, rebuild and redeploy the Android or Quest package before testing voice input on device.

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

{% content-ref url="configure-character-audio.md" %}
[Configure character audio](configure-character-audio.md)
{% endcontent-ref %}

{% content-ref url="configure-conversation-input.md" %}
[Configure conversation input](configure-conversation-input.md)
{% endcontent-ref %}
