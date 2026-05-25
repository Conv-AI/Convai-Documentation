---
title: Configure microphone
description: >-
  Select the active microphone device and configure platform-specific
  permissions for Android, iOS, and WebGL builds.
last_reviewed: "4.2.0"
---

The Convai SDK for Unity opens the system microphone automatically when a session starts. This page covers how to enumerate and select a specific device at runtime, and how to satisfy the platform-specific requirements for Android, iOS, and WebGL.

## Microphone device selection

To list available microphone devices and let the player choose one:

```csharp
using Convai.Runtime.Settings;

// Get the microphone device service from the SDK
if (ConvaiManager.ActiveManager.TryGetMicrophoneDeviceService(out IMicrophoneDeviceService micService))
{
    // List all available devices
    IReadOnlyList<ConvaiMicrophoneDevice> devices = micService.GetAvailableDevices();

    foreach (var device in devices)
    {
        Debug.Log($"{device.Name} (ID: {device.Id}, Index: {device.Index})");
    }

    // Start listening with a specific device index
    await ConvaiManager.ActiveManager.Audio.StartListeningAsync(microphoneIndex: device.Index);
}
```

{% hint style="warning" %}
On WebGL, `GetAvailableDevices()` returns an empty list outside the Editor. Microphone access on WebGL goes through the browser's Web Audio API and does not support Unity's native device enumeration.
{% endhint %}

## Platform-specific setup

### Android

The SDK requests microphone permission at runtime automatically when a recording starts. You must declare the permission in your `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

If your project does not have a custom manifest, create one or enable **Override Default Manifest** in **Player Settings > Publishing Settings**.

When the SDK requests the permission, Android shows its standard permission dialog. If the player grants it, recording starts automatically. If denied, the SDK logs a warning and the microphone remains inactive.

### iOS

Add a microphone usage description to your `Info.plist`. In Unity, set this via **Player Settings > iOS > Other Settings > Microphone Usage Description**:

```
"This app uses the microphone to support voice conversations with AI characters."
```

The SDK requests authorization automatically using Unity's `Application.RequestUserAuthorization`. The app does not need to call any permission API directly.

{% hint style="danger" %}
Submitting to the App Store without a microphone usage description will cause App Store review rejection. Set this value before building for iOS distribution.
{% endhint %}

### WebGL

Browsers block audio playback and microphone access until the user has interacted with the page. The SDK provides two methods depending on your use case:

* **`Audio.EnableAudioPlayback()`** — unlocks browser audio output only. Use this when you want character voice to play but are not yet starting the microphone (for example, during a tutorial before the player speaks).
* **`ConvaiManager.EnableAudioAndStartListening()`** — unlocks browser audio output **and** opens the microphone. Use this when the player is ready to begin a full conversation.

```csharp
// Call from a UI button's onClick event
public void OnStartButtonClicked()
{
    // Option A: unlock audio only (no microphone yet)
    if (ConvaiManager.ActiveManager.Audio.RequiresUserGesture)
    {
        ConvaiManager.ActiveManager.Audio.EnableAudioPlayback();
    }

    // Option B: unlock audio and open microphone in one step
    // ConvaiManager.ActiveManager.EnableAudioAndStartListening();
}
```

If you skip this step on WebGL, the character's voice will not play even though Convai sends audio data. `RequiresUserGesture` returns `true` only on WebGL.

## Next steps

With audio configured, add a transcript UI to display conversation text.

{% content-ref url="add-chat-ui.md" %}
[Add chat UI](add-chat-ui.md)
{% endcontent-ref %}
