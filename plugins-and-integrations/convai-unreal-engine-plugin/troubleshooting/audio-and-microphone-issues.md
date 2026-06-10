---
title: Audio and microphone issues
description: Fix audio capture failures, wrong microphone device, Android permission errors, and audio playback problems in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

Use this page to resolve problems where the plugin cannot capture microphone input, uses the wrong audio device, or fails to play character audio. Connection and API key problems are covered in [Connection and API key issues](connection-and-api-key-issues.md).

## First-line check

Run through these four checks before investigating specific symptoms.

{% stepper %}
{% step %}
### Open the Output Log and filter on ConvaiAudioLog

Open **Window > Output Log**, type `ConvaiAudioLog` in the search field, and look for error or warning entries. Most audio capture failures produce a message here immediately on Play.
{% endstep %}

{% step %}
### Confirm the AudioCapture plugin is enabled

Open **Edit > Plugins**, search for `Audio Capture`, and verify it is enabled. The `Convai Audio Capture` component depends on this engine plugin. If it is disabled, no capture device can be opened.
{% endstep %}

{% step %}
### Confirm a default microphone is set in the OS

On Windows, open **Sound Settings > Input** and confirm a default recording device is selected and not muted. Unreal Engine uses the OS default device when no explicit device index is set.
{% endstep %}

{% step %}
### On Android — confirm microphone permission is granted

Launch the app on the device, go to **Settings > Apps > [Your App] > Permissions**, and confirm microphone access is granted. The plugin declares `android.permission.RECORD_AUDIO` in `Convai_AndroidAPL.xml`, but the user still has to grant the runtime permission on the device.
{% endstep %}
{% endstepper %}

## Microphone input is not detected

**Symptom:** The character never responds to speech. The `ConvaiAudioLog` Output Log shows capture-device warnings, or no audio-forwarding activity appears after Play begins.

**Cause — `AudioCapture` plugin disabled:** The `Convai Audio Capture` component depends on the engine's `AudioCapture` plugin. If that plugin is disabled, no capture device can be opened.

**Fix:** Open **Edit > Plugins**, search for `Audio Capture`, enable it, and restart the editor.

**Verify:** Enter Play mode and speak. `ConvaiAudioLog` should show audio data being captured and forwarded.

---

**Cause — no microphone connected or no default device set:** The operating system reports no default capture device, so `ConvaiAudioCaptureComponent` cannot open a stream. In the Output Log you will see:

```text
ConvaiAudioLog: Warning: OpenStream returned false
```

**Fix:** Connect a microphone, set it as the default recording device in the OS sound settings, and restart the editor.

**Verify:** In the Output Log, `ConvaiAudioLog` should no longer show the `OpenStream returned false` warning after Play begins.

## Wrong microphone device is selected

**Symptom:** Audio is captured from the wrong input — for example, a built-in webcam microphone rather than a headset.

**Cause:** `ConvaiAudioCaptureComponent` opens the system default device unless an explicit device index is set. If the OS default is not the intended device, input comes from the wrong source.

**Fix:** Use `Get Available Capture Device Details` on the `Convai Player` component to enumerate available devices. The node returns an array of `FCaptureDeviceInfoBP` structs. Each struct exposes `DeviceName`, `DeviceIndex`, `LongDeviceId`, `InputChannels`, `PreferredSampleRate`, and `bSupportsHardwareAEC`. Pass the `DeviceIndex` of the correct device to `Set Capture Device By Index`, or use `Set Capture Device By Name` when you prefer to select by device name.

**Verify:** After selecting the device, speak and confirm in `ConvaiAudioLog` that the stream opened on the correct device name.

## Player component does not forward audio to the chatbot

**Symptom:** The microphone is detected and appears to be capturing, but the character still does not respond. No speech-related entries appear under `ConvaiPlayerLog`.

**Cause — `Convai Player` component not linked to the chatbot:** `UConvaiPlayerComponent` must be associated with the `UConvaiChatbotComponent` it is talking to. Without that link, captured audio is not forwarded to any character session.

**Fix:** In the Blueprint for the player pawn, select the `Convai Player` component and confirm that the chatbot component reference is set. If you are using Blueprint nodes, ensure the `Start Talking` node receives a valid reference to the `Convai Chatbot` component.

**Verify:** Enter Play mode and trigger the talking action. `ConvaiPlayerLog` should show audio being sent, and `ConvaiChatbotComponentLog` should show a response being received.

---

**Cause — push-to-talk key not held or talk trigger not firing:** The player component does not capture continuously by default; a trigger must be active.

**Fix:** Confirm that the Blueprint or input binding that calls `Start Talking` on the `Convai Player` component is firing correctly. Add a temporary Print String to the Blueprint event to verify execution.

**Verify:** While the trigger is held, `ConvaiPlayerLog` should show audio frames being enqueued.

## Audio channel mismatch warning

**Symptom:** Audio capture opens but voice quality is degraded, garbled, or silent. The Output Log shows:

```text
ConvaiAudioLog: Warning: Audio capture components only support mono and stereo mic input - Audio might be mangeled
```

**Cause:** The capture device is reporting more than two input channels (for example, a multi-channel audio interface). The plugin processes only mono or stereo streams; multichannel input is accepted but may produce incorrect output.

**Fix:** In the OS audio settings, configure the capture device to use a mono or stereo format before opening the stream. Alternatively, select a different device that natively presents as mono or stereo.

**Verify:** The warning no longer appears in `ConvaiAudioLog` after restarting the capture stream.

## No audio on Android

**Symptom:** The plugin works correctly on Windows but no microphone input is received when the application runs on an Android device.

{% tabs %}
{% tab title="Permission not granted" %}
**Cause:** Android requires the `android.permission.RECORD_AUDIO` permission to be declared in the manifest and granted at runtime.

**Fix:**
1. Open **Edit > Plugins**, search for `Android Permission`, and confirm it is enabled.
2. Rebuild and deploy. The plugin adds `android.permission.RECORD_AUDIO` through `Convai_AndroidAPL.xml`.
3. On first launch, grant the microphone permission when Android prompts for it. If the permission was denied earlier, enable it manually in Android app settings.

**Verify:** On the Android device, grant the microphone permission when prompted. The character should respond to speech after permission is granted.

If your project needs to check permission before starting a scene, use the plugin's Android permission helpers or Unreal's Android permission nodes and show a user-facing message when permission is denied.
{% endtab %}

{% tab title="Native libraries missing" %}
**Cause:** The plugin bundles native audio libraries (`libconvai_client.so`, `libconvai_http_helper.so`) that must be present in the APK. If ProGuard or a custom packaging step removed them, audio initialization fails on-device with no clear log message in the game output.

**Fix:** Use `adb logcat` to read system logs from the device — game Output Log is not written on a deployed APK without extra steps. Filter for Convai-related entries:

```text
adb logcat -s ConvaiAudioLog:V LogConvai:V
```

If you see `UnsatisfiedLinkError` or `dlopen failed` referencing `libconvai_client.so`, confirm that `Convai_AndroidAPL.xml` was not removed or overridden and that your Android build still packages the plugin's native libraries.

**Verify:** After a clean package rebuild, run `adb shell ls /data/app/<your.package>/lib/arm64/` to confirm `libconvai_client.so` is present in the installed APK.
{% endtab %}
{% endtabs %}

## Character audio does not play — mouth moves but no sound

**Symptom:** The `Convai Face Sync` component animates (mouth moves), confirming that responses are arriving, but no audio plays from the character. The Output Log may contain:

```text
ConvaiAudioStreamerLog: Warning: PlayVoiceData: Failed to parse wav header, reason: <detail>
```

**Cause:** The audio data received from Convai could not be decoded. This is usually a transient network issue — a partial or corrupted packet — rather than a configuration problem.

**Fix:** This error is typically self-resolving on the next turn. If it persists across multiple turns:
1. Check network quality and packet loss on the connection to `realtime-api.convai.com`.
2. Confirm the API key is valid — authentication failures can cause malformed response data.
3. Re-enter Play mode to establish a fresh session.

**Verify:** On the next successful turn, audio should play normally and the warning should not recur.

## Audio device hot-swap does not take effect

**Symptom:** Changing the active capture device while the application is running — for example, plugging in a headset — does not switch the input. The plugin continues using the previous device.

**Cause — device switch not triggered explicitly:** Microphone hot-swap is supported in recent plugin versions. However, the device switch must be triggered explicitly via Blueprint; the plugin does not detect hardware changes automatically.

**Fix:** Call `Set Capture Device By Index` on the `Convai Player` component with the new `DeviceIndex` after the new device is connected. Enumerate the current device list first using `Get Available Capture Device Details` to obtain the correct index for the new device.

**Verify:** After calling `Set Capture Device By Index`, speak into the new device and confirm that `ConvaiAudioLog` shows data from the updated device.

## UE version note — audio capture API differences

{% hint style="info" %}
On Unreal Engine 5.3 and later, the plugin uses `OpenAudioCaptureStream()`. On UE 5.2 and earlier, it uses `OpenCaptureStream()`. On UE 5.2 and earlier, occasional device hiccups can produce degenerate (zero-length) audio buffers; the plugin drops these buffers silently. If you see intermittent audio gaps on an older engine version, upgrading to UE 5.3 or later resolves this class of issue.
{% endhint %}

## Output Log reference — `ConvaiAudioLog` messages

| Log message | Level | Meaning | Action |
| --- | --- | --- | --- |
| `OpenStream returned false` | Warning | OS reported no capture device available | Connect a microphone; check OS audio settings |
| `Audio capture components only support mono and stereo mic input - Audio might be mangeled` | Warning | Device has > 2 channels | Set device to mono/stereo in OS settings |
| `SetCaptureDevice: OpenStream failed for device index %d` | Warning | Requested device index could not be opened | Enumerate devices again; index may have changed |
| `PlayVoiceData: Failed to parse wav header, reason: %s` | Warning | Received audio data is malformed | Usually transient; check network quality |

## Next steps

{% content-ref url="lip-sync-and-animation-issues.md" %}
[Lip sync and animation issues](lip-sync-and-animation-issues.md)
{% endcontent-ref %}

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
