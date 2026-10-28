---
title: Audio and microphone issues
description: Diagnose microphone capture, permission, publication, and character playback failures, including native and browser audio differences.
last_reviewed: "5.0.0-preview"
---

Separate microphone input from character playback when diagnosing audio. A published microphone does not prove that playback is unlocked, and a connected room does not prove that either path is ready. Read `ConvaiSessionEventRelay.OnSessionError` and its message before changing audio settings.

## First-line check

{% stepper %}
{% step %}
### Check the session's microphone policy

A text-only session sets `LocalAudioPolicy.AllowMicrophone` to `false`. `SetMicrophoneAllowed(false)` can also turn off capture at runtime. A refused listening operation can report `audio.mic_not_allowed`; the capture path skips microphone creation and permission requests. If text-only behavior is intended, use typed input. Otherwise enable the policy before starting listening again.
{% endstep %}
{% step %}
### Read the audio error and platform detail

Filter the Console for `Audio` or `RoomAudioRuntimeAdapter`. `audio.mic_permission_denied` indicates refused access; `audio.mic_unavailable` indicates no usable device; `audio.mic_publish_failed` covers other publication failures. Browser error messages retain the rejection reason and can identify a host-page permission policy.
{% endstep %}
{% step %}
### Inspect the character's output component

Keep `ConvaiAudioOutput`, `ConvaiCharacter`, and `AudioSource` on the same `GameObject`. Unity's required-component attributes add the dependencies when you add the output component normally. On native platforms the voice plays through the `AudioSource`. On WebGL playback occurs in the browser, but `ConvaiAudioOutput` still exposes character gain, mute, and voice-level controls.

Set volume and spatial settings on `ConvaiAudioOutput`. It writes `AudioSource.volume`, `spatialBlend`, minimum and maximum distance, logarithmic rolloff, and `playOnAwake = false`. Manually changing those `AudioSource` values can be overwritten. Also inspect `AudioSource.mute`, the assigned mixer group, and the scene's audio listener on native platforms.
{% endstep %}
{% step %}
### Unlock browser playback when required

Microphone publication no longer aborts merely because browser playback requires a user gesture. Capture permission and playback autoplay are separate gates. If a WebGL conversation connects but the character is inaudible, use an explicit user interaction to call the scene room manager's `EnableAudioPlayback()` or `EnableAudioAndStartListening()`.

Check `CanEnableAudioPlayback`, `RequiresUserGestureForAudio`, and `IsAudioPlaybackActive` to drive that button. The SDK also handles the first qualifying interaction through its browser audio unlock path. Verify playback in the built page, not only in the Editor.
{% endstep %}
{% endstepper %}

## Audio error codes

| Code | Client interpretation | Fix and verification |
| --- | --- | --- |
| `audio.mic_not_allowed` | The session forbids microphone capture | Keep text input for text-only use, or enable microphone policy and retry listening |
| `audio.mic_permission_denied` | Platform or browser refused capture | Inspect system/site permission and the detailed message; retry after granting access |
| `audio.mic_unavailable` | No usable microphone or the platform-default fallback failed | Connect/select a microphone and retry listening |
| `audio.mic_publish_failed` | Source creation or track publication failed for another reason | Inspect the detailed exception and room state; retry after resolving it |

`Microphone publish aborted because the room audio path is not initialized.` means the audio path is not ready. `Microphone publish failed: IMicrophoneSourceFactory not registered.` means the required source factory is missing. These are separate from browser autoplay.

## Character output settings

| Field | Script default | Effect |
| --- | --- | --- |
| **Volume** | `1` | Replaces native source volume; it is not multiplied by a manually set source volume |
| **Is Muted** | `false` | Silences this character's output |
| **Use 3D Audio** | `true` | Uses native spatial attenuation |
| **Min Distance** | `5` | Native distance within which voice is at full volume |
| **Max Distance** | `50` | Native attenuation distance setting |

Browser voice playback does not apply Unity's distance rolloff or `AudioListener.volume`. Check the component's gain and mute controls there. [Connection and audio indicators](../ui-and-presentation/show-connection-and-audio-levels.md) explains the measurement availability properties.

## Platform permissions

{% tabs %}
{% tab title="Android" %}
The permission service uses Android's `RECORD_AUDIO` permission. Verify that the built manifest includes `android.permission.RECORD_AUDIO`. The SDK requests access through its permission service when capture is allowed. After a denial, inspect the device's application permissions before retrying listening.

If you maintain a custom manifest, the permission declaration is:

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

Verify on the device that granting permission allows capture. The local Settings Panel microphone test can help distinguish capture from a conversation-routing issue.
{% endtab %}
{% tab title="macOS and iOS" %}
Open **Convai → Settings → Setup Health** and inspect **macOS / iOS Microphone Usage Description**. Its **Setup** action fills the microphone usage description used by Apple builds. Review the text for your application before building. iOS also has **Prepare iOS for Recording** in Setup Health.

If access was denied, inspect the application's microphone permission in system settings. A successful Editor conversation does not verify the built application's permission configuration. Rebuild and test capture on the target platform.
{% endtab %}
{% tab title="WebGL" %}
The browser decides capture permission. The SDK classifies `NotAllowedError`, `SecurityError`, and `PermissionDeniedError` as `audio.mic_permission_denied`. `NotFoundError`, `OverconstrainedError`, and `DevicesNotFoundError` become `audio.mic_unavailable`; other capture rejections become `audio.mic_publish_failed`.

When the page's Permissions Policy blocks the microphone, the SDK message says the browser refused access without asking. An embedding host must grant microphone access, such as `allow="microphone"` on its iframe, in addition to any applicable host policy. A host that does not grant access cannot provide voice input; text input can still work.

Check the browser's site permission and secure deployment configuration. The SDK exposes a default microphone placeholder on WebGL; browser capture controls the actual device. The Settings Panel's local recording test is not supported in a WebGL player. Validate capture and playback separately in the deployed page.
{% endtab %}
{% endtabs %}

## Troubleshoot audio failures

| Symptom | Cause to check | Fix and verification |
| --- | --- | --- |
| No permission prompt in a text-only session | Microphone policy disables capture | Expected; verify typed input works |
| No prompt in an embedded browser build | Host Permissions Policy blocks capture | Ask the host to grant microphone access; retry and inspect the detailed error |
| Player transcript arrives but no character audio plays | Playback is locked, muted, or not routed | Unlock browser playback or inspect native output; verify a voice-level reading when available |
| Native voice becomes quiet with distance | Spatial attenuation is enabled | Adjust output distance settings or disable 3D audio, then test from the same position |
| Native source volume changes back | Output component owns its volume | Set **Volume** on `ConvaiAudioOutput`; verify the source reflects it |
| Microphone is available but the character does not hear speech | Input policy, mute, or targeting is incorrect | Inspect conversation availability and microphone policy; test a complete turn |
| Character output reports a missing character component | Components are on different objects | Place output and character together; re-enter Play Mode and check the error is gone |

## Next steps

{% content-ref url="debug-tools-reference.md" %}
[Debug tools reference](debug-tools-reference.md)
{% endcontent-ref %}
