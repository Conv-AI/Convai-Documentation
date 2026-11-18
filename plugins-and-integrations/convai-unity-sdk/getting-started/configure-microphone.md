---
title: Configure microphone
description: >-
  Select an active microphone device at runtime, set a project-wide default, and
  configure platform permissions for Android, iOS, and WebGL builds.
last_reviewed: "5.0.0-pre.1"
---

The Convai SDK for Unity opens the microphone according to the room's input policy, when microphone capture is allowed. Select a device and configure platform permissions before testing voice. For a session that never requests microphone permission, turn off **Allow Microphone** before connecting.

## Microphone device selection

Choose a device from the list reported by the active transport. Apply its stable ID as a runtime preference before starting the next capture. If the transport reports no devices, use the system or browser default.

```csharp
using Convai.Domain.Types;
using Convai.Runtime.Components;
using UnityEngine;

public sealed class MicrophoneDevicePicker : MonoBehaviour
{
    public bool SelectForNextCapture(int index)
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.IsInitialized ||
            !manager.TryGetMicrophoneDeviceService(out var devices) ||
            !manager.TryGetRuntimeSettingsService(out var settings))
            return false;

        var available = devices.GetAvailableDevices();
        if (index < 0 || index >= available.Count) return false;

        return settings.Apply(new ConvaiRuntimeSettingsPatch
        {
            PreferredMicrophoneDeviceId = available[index].Id
        }).Success;
    }
}
```

## Set the project-wide default device

`ConvaiSettings.DefaultMicrophoneDeviceId` sets the microphone the SDK uses before a runtime settings override. An empty string resolves to the system default device.

{% stepper %}
{% step %}
### Open the Runtime Defaults section

Open **Edit > Project Settings > Convai SDK**, or select **Convai > Settings** in the Unity Editor menu bar. Scroll to the **Runtime Defaults** card.
{% endstep %}

{% step %}
### Pick a device

Use the **Microphone** dropdown to select a connected device by name, or leave it at **System Default** to follow the operating system's device order.
{% endstep %}

{% step %}
### Refresh the device list if needed

Select **Refresh** to re-enumerate connected microphones if you plugged in or removed a device after opening the window.
{% endstep %}
{% endstepper %}

## Platform-specific setup

### Android

The SDK requests permission when capture starts. Unity includes the microphone permission when it builds a project using the microphone APIs. If you supply a custom manifest, check that the merged manifest still contains:

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

You do not need to create a custom manifest solely for this permission.

When the SDK requests the permission, Android shows its standard permission dialog. If the player grants it, recording starts automatically. If denied, the SDK logs a warning and the microphone remains inactive.

### macOS and iOS

Add a microphone usage description to your `Info.plist`. In Unity, set this via **Player Settings > iOS > Other Settings > Microphone Usage Description**:

```text
"This app uses the microphone to support voice conversations with AI characters."
```

Open **Convai > Settings > Setup Health** and use **Setup** beside **macOS / iOS Microphone Usage Description**. For iOS, also enable **Prepare iOS for Recording**. The SDK requests microphone authorization on macOS and iOS when capture needs it.

<figure><img src="../../../.gitbook/assets/unity-setup-health.png" alt="Setup Health card showing Apple microphone usage, iOS recording, and Android permission checks"><figcaption><p>Project health checks for microphone permissions and recording configuration.</p></figcaption></figure>

{% hint style="danger" %}
Set a microphone usage description before building an app that records on macOS or iOS. If permission was denied, enable it in the operating system privacy settings before testing again.
{% endhint %}

### WebGL

A browser may require a gesture for blocked audio playback. Microphone capture separately requires HTTPS (or localhost) and permission. On each eligible scene click or tap after connection, the manager rechecks playback and calls `EnableAudioAndStartListening()` if needed; pointer events over UI are excluded. For a dedicated start button or when the automatic option is disabled, use one of these methods:

* **`Audio.EnableAudioPlayback()`** — unlocks browser audio output only. Use this when you want character voice to play but are not yet starting the microphone (for example, during a tutorial before the player speaks).
* **`manager.Audio.EnableAudioAndStartListening()`** — unlocks browser playback and requests capture if the room allows the microphone. Use this when the player is ready to begin a full conversation.

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class BrowserVoiceStartButton : MonoBehaviour
{
    // Assign this method to a UI Button's On Click event.
    public void StartVoice()
    {
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager != null && manager.IsInitialized) manager.Audio.EnableAudioAndStartListening();
    }
}
```

If browser playback remains blocked, click the scene or your start button and check `Audio.RequiresUserGesture`. When microphone capture is disabled, `EnableAudioAndStartListening()` enables playback without opening the microphone.

## Microphone processing and level

Under **Convai Room Manager > Listening > Microphone**, configure **Echo Cancellation**, **Noise Suppression**, and **Automatic Gain Control**. Native defaults are off, on, and off respectively. Processing changes apply on the next connection. WebGL uses browser processing.

Read `manager.Audio.MicrophoneLevel` for a continuous audio level, and check `IsMicrophoneLevelAvailable` before interpreting zero as silence. A level meter is separate from the speech-detection decision.

Turn off **Allow Microphone** before connecting for text input with voice replies. Use `SetMicrophoneAllowed(false)` to stop capture during an active session, or `SetMicrophoneAllowed(true)` to permit it again. See [Run a text-only session](run-a-text-only-session.md).

## Next steps

With audio configured, add a transcript UI to display conversation text.

{% content-ref url="add-chat-ui.md" %}
[Add chat UI](add-chat-ui.md)
{% endcontent-ref %}

<figure><img src="../../../.gitbook/assets/unity-room-listening.png" alt="Room Listening card with microphone policy and processing controls above Interruptions"><figcaption><p>This existing sample enables echo cancellation. Newly configured policies default to echo cancellation off; choose processing for your application.</p></figcaption></figure>
