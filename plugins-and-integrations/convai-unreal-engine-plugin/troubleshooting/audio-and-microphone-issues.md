---
title: Audio and microphone issues
description: Fix audio capture failures, wrong microphone device selection, and Android microphone permission errors in the Convai Unreal Engine plugin.
last_reviewed: 2026-06-04
---

Use this page to resolve problems where the plugin cannot capture microphone input or where the wrong audio device is used. Connection and API key problems are covered in [Connection and API key issues](connection-and-api-key-issues.md).

## Microphone input is not detected

**Symptom:** The character never responds to speech. The Output Log shows messages from `ConvaiAudioLog` indicating no audio data was received, or no capture device was found.

**Cause — `AudioCapture` plugin disabled:** The `Convai Audio Capture` component depends on the engine's `AudioCapture` plugin. If that plugin is disabled, no capture device can be opened.

**Fix:** Open **Edit > Plugins**, search for `Audio Capture`, enable it, and restart the editor.

**Verify:** Enter Play mode and speak. The Output Log under `ConvaiAudioLog` should show audio data being captured and forwarded.

---

**Cause — no microphone connected or no default device set:** The operating system reports no default capture device, so `ConvaiAudioCaptureComponent` cannot open a stream.

**Fix:** Connect a microphone, set it as the default recording device in the OS sound settings, and restart the editor.

**Verify:** In the Output Log, look for `ConvaiAudioLog` messages confirming that the default capture device was opened successfully.

## Wrong microphone device is selected

**Symptom:** Audio is captured from the wrong input — for example, a built-in webcam microphone rather than a headset.

**Cause:** `ConvaiAudioCaptureComponent` opens the system default device unless an explicit device index is set. If the OS default is not the intended device, input will come from the wrong source.

**Fix:** Use the `Get Capture Devices Available` Blueprint node (which returns an array of `FCaptureDeviceInfoBP` structs) to enumerate available devices. Each struct exposes `DeviceName`, `DeviceIndex`, `LongDeviceId`, `InputChannels`, `PreferredSampleRate`, and `bSupportsHardwareAEC`. Pass the `DeviceIndex` of the correct device to the `Set Capture Device` call on the audio component.

**Verify:** After selecting the device, speak and confirm in the Output Log (`ConvaiAudioLog`) that the stream opened on the correct device name.

## Player component does not forward audio to the chatbot

**Symptom:** The microphone is detected and appears to be capturing, but the character still does not respond. No speech-related log entries appear under `ConvaiPlayerLog`.

**Cause — `Convai Player` component not linked to the chatbot:** The `UConvaiPlayerComponent` must be associated with the `UConvaiChatbotComponent` it is talking to. Without that link, captured audio is not forwarded to any character session.

**Fix:** In the Blueprint for the player pawn, select the `Convai Player` component and confirm that the chatbot component reference is set. If you are using Blueprint nodes, ensure the `Start Talking` node receives a valid reference to the `Convai Chatbot` component.

**Verify:** Enter Play mode and trigger the talking action. `ConvaiPlayerLog` should show audio being sent, and `ConvaiChatbotComponentLog` should show a response being received.

---

**Cause — push-to-talk key not held or talk trigger not firing:** The player component does not capture continuously by default; a trigger must be active.

**Fix:** Confirm that the Blueprint or input binding that calls `Start Talking` on the `Convai Player` component is firing correctly. Add a temporary print string to the Blueprint event to verify execution.

**Verify:** While the trigger is held, `ConvaiPlayerLog` should show audio frames being enqueued.

## No audio on Android

**Symptom:** The plugin works correctly on Windows but no microphone input is received when the application runs on an Android device.

**Cause — microphone permission not granted:** Android requires the `android.permission.RECORD_AUDIO` permission to be declared in the manifest and granted at runtime. The plugin depends on the `AndroidPermission` engine plugin to handle this.

**Fix:**
1. Open **Edit > Plugins**, search for `Android Permission`, and confirm it is enabled.
2. In **Edit > Project Settings > Platforms > Android**, add `android.permission.RECORD_AUDIO` to the **Extra Permissions** list.
3. Rebuild and deploy. On first launch, the OS will prompt the user to grant the permission; ensure your Blueprint calls `Request Android Permissions` at startup and handles the result before starting audio capture.

**Verify:** On the Android device, grant the microphone permission when prompted. The character should respond to speech after permission is granted.

{% hint style="warning" %}
If the user denies the microphone permission and the app does not handle the denial gracefully, the audio capture stream will fail silently. Add a check in Blueprint: if permission is denied, show a message and disable the talking feature.
{% endhint %}

## Audio device hot-swap does not take effect

**Symptom:** Changing the active capture device while the application is running (for example, plugging in a headset) does not switch the input. The plugin continues using the previous device.

**Cause — stream was opened before the new device was connected:** In earlier plugin versions this required a stream restart. Starting with version 4.0.0-beta.20, microphone hot-swap is supported: switching the device mid-session no longer requires restarting the stream. However, the device switch must be triggered explicitly.

**Fix:** Call `Set Capture Device` on the `Convai Audio Capture` component with the new `DeviceIndex` after the new device is connected. Enumerate the current device list first using `Get Capture Devices Available` to obtain the correct index for the new device.

**Verify:** After calling `Set Capture Device`, speak into the new device and confirm that `ConvaiAudioLog` shows data from the updated device.

## Next steps

{% content-ref url="lip-sync-and-animation-issues.md" %}
[Lip sync and animation issues](lip-sync-and-animation-issues.md)
{% endcontent-ref %}

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
