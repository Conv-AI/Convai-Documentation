# audio and microphone issues

Audio failures in the Convai Unity SDK fall into two categories: microphone input problems that prevent the SDK from capturing the player's voice, and audio output problems that prevent the character's voice from playing. Both categories produce specific error codes and console messages that point directly to the cause. This page covers both, with platform-specific guidance for Android, iOS, and WebGL.

***

## First-Line Check

{% stepper %}
{% step %}
**Check the Console for Audio Error Codes**

Open the Unity Console and filter for `audio`. Audio failures surface as session errors on `ConvaiSessionEventRelay.OnSessionError`. Look for these error codes:

* `audio.mic_unavailable` — no microphone device found
* `audio.mic_permission_denied` — user denied permission, or platform requires a user gesture
* `audio.mic_publish_failed` — microphone track could not be published to the room

Also look for console messages prefixed with `[RoomAudioRuntimeAdapter]` or `[AudioTrackManager]` — these give more detail than the error code alone.
{% endstep %}

{% step %}
**Verify ConvaiAudioOutput Is on the Correct GameObject**

`ConvaiAudioOutput` must be on the **same** GameObject as `ConvaiCharacter`. The component has `[RequireComponent(typeof(ConvaiCharacter))]` — Unity enforces this when you add it via Add Component, but it may be violated by manual prefab editing or copy-paste.

If `ConvaiAudioOutput` is on a different GameObject, you will see this error on Play: `[ConvaiAudioOutput] ConvaiCharacter component not found on {gameObjectName}`

That GameObject also needs an `AudioSource` component. Unity adds it automatically with the `[RequireComponent(typeof(AudioSource))]` constraint, but verify it is present and enabled.
{% endstep %}

{% step %}
**Check the AudioSource Settings**

Select the NPC GameObject and inspect the `AudioSource` component:

* **Volume** must be greater than 0
* **Mute** must be unchecked
* **AudioMixer** output group (if assigned) must not be at -80 dB
* **Spatial Blend** should be 0 (2D) for UI-style characters or 1 (3D) for in-scene positioned characters. A spatial blend of 1 with the camera far from the character will attenuate the audio.
{% endstep %}

{% step %}
**For WebGL — Confirm a User Gesture Triggers the Connection**

Browsers block microphone access until the user has interacted with the page. In WebGL builds, `ConvaiManager.ConnectAsync()` must be called from within a user gesture handler (e.g., a button `onClick` event), not automatically on scene load.

If the SDK connects before a gesture, mic publishing is aborted with: `[RoomAudioRuntimeAdapter] Microphone publish aborted because audio playback requires a user gesture.`
{% endstep %}
{% endstepper %}

***

## Audio Error Codes

| Error Code                    | Description                                                 | Common Cause                                                                 |
| ----------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `audio.mic_unavailable`       | No microphone device was found                              | No microphone connected; WebGL platform (always returns no devices)          |
| `audio.mic_permission_denied` | Permission to access the microphone was denied              | User rejected the system permission dialog; WebGL called before user gesture |
| `audio.mic_publish_failed`    | Microphone track could not be published to the LiveKit room | Room not connected; internal factory not registered                          |

***

## ConvaiAudioOutput Setup Errors

### Component on Wrong GameObject

**Console message:** `[ConvaiAudioOutput] ConvaiCharacter component not found on {gameObjectName}`

**Cause:** `ConvaiAudioOutput` is not on the same GameObject as `ConvaiCharacter`.

**Fix:** Select the NPC in the Hierarchy. Confirm `ConvaiAudioOutput`, `ConvaiCharacter`, and `AudioSource` are all on the same GameObject. Move `ConvaiAudioOutput` if needed.

***

## Platform Permissions

{% tabs %}
{% tab title="Android" %}
Android requires the `RECORD_AUDIO` permission. Without it, the microphone is unavailable and `audio.mic_permission_denied` fires.

**Step 1 — Add the permission to AndroidManifest.xml:**

If you do not have a custom `AndroidManifest.xml`, create one at `Assets/Plugins/Android/AndroidManifest.xml`. Add the following line inside the `<manifest>` tag:

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

**Step 2 — Set the Microphone Usage Description in Player Settings:**

Open **Edit → Project Settings → Player → Android → Other Settings**. Set **Microphone Usage Description** to a user-facing explanation, for example: `"Used for voice interaction with AI characters."`

**Runtime behavior:** Android shows a system permission dialog the first time the microphone is requested. If the user denies it, `audio.mic_permission_denied` fires. The SDK does not re-request the permission automatically — your application must guide the user to grant it in device Settings if they denied it initially.

{% hint style="warning" %}
If the permission dialog never appears, check that the `RECORD_AUDIO` permission is present in the manifest. A missing permission suppresses the dialog and silently denies access.
{% endhint %}
{% endtab %}

{% tab title="iOS" %}
iOS requires `NSMicrophoneUsageDescription` in `Info.plist`. Without it, the app crashes immediately when the microphone is first accessed.

**Set the description in Player Settings:**

Open **Edit → Project Settings → Player → iOS → Other Settings**. Set **Microphone Usage Description** to a user-facing explanation, for example: `"Used for voice interaction with AI characters."`

Unity writes this value to `Info.plist` during the build.

**Runtime behavior:** iOS shows a system permission dialog on first mic access. If the user denies it, `audio.mic_permission_denied` fires. The SDK does not re-request the permission — direct the user to iOS **Settings → Privacy & Security → Microphone** to re-enable it.

{% hint style="danger" %}
Submitting an iOS build to the App Store without `NSMicrophoneUsageDescription` causes an automatic rejection. Set this field even if microphone access is optional in your training simulation or experience.
{% endhint %}
{% endtab %}

{% tab title="WebGL" %}
WebGL has two constraints that affect microphone access:

**1. No device enumeration.** `MicrophoneDeviceService.GetAvailableDevices()` always returns an empty list on WebGL. The SDK uses the browser's default input device — device selection at the SDK level is not supported on this platform.

**2. User gesture required.** Browsers enforce a policy that microphone access can only be requested within a user gesture handler (a button click, key press, etc.). Calling connect automatically on scene load — without a prior user interaction — results in:

`[RoomAudioRuntimeAdapter] Microphone publish aborted because audio playback requires a user gesture.`

**Recommended pattern for WebGL:**

Add a **Start Conversation** button to your scene. Wire its `onClick` to call your connect logic. Do not connect on `Start()` or `Awake()`.

```csharp
// Called from a UI Button onClick event — this IS a user gesture
[SerializeField] private ConvaiManager _convaiManager;

public void OnStartButtonClicked()
{
    _ = _convaiManager.ConnectAsync();
}
```

**HTTPS required.** Browsers only grant microphone access on HTTPS pages. Local development on `localhost` is the only HTTP exception most browsers allow. Deploy to HTTPS for testing outside `localhost`.
{% endtab %}
{% endtabs %}

***

## Common Issues

| Symptom                                                                                                | Likely Cause                                                | Fix                                                                           |
| ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `audio.mic_permission_denied` on Android                                                               | `RECORD_AUDIO` missing in `AndroidManifest.xml`             | Add the permission; rebuild                                                   |
| `audio.mic_permission_denied` on iOS                                                                   | `NSMicrophoneUsageDescription` missing in Player Settings   | Set the description; rebuild                                                  |
| `audio.mic_permission_denied` on WebGL                                                                 | No user gesture before connect                              | Trigger connect from a UI button click                                        |
| `audio.mic_unavailable`                                                                                | No microphone connected to the machine                      | Connect a microphone; check OS audio devices                                  |
| `audio.mic_unavailable` on WebGL                                                                       | Platform always returns empty device list                   | Expected — SDK uses browser default device                                    |
| `[ConvaiAudioOutput] ConvaiCharacter component not found on X`                                         | `ConvaiAudioOutput` on wrong GameObject                     | Move it to the same GameObject as `ConvaiCharacter`                           |
| Character transcript appears but no audio plays                                                        | `AudioSource` muted, volume 0, or mixer at -80 dB           | Inspect the `AudioSource` component on the NPC                                |
| Character audio plays on one ear only in 3D                                                            | `AudioSource.spatialBlend` set to 1 with camera too far     | Reduce Max Distance on AudioSource or bring camera closer                     |
| `[RoomAudioRuntimeAdapter] Microphone publish aborted because the room audio path is not initialized.` | `ConnectAsync` not yet complete when mic publish was called | Wait for `OnSessionStateChanged` event with `Connected` before publishing mic |
| `[AudioTrackManager] PublishMicrophoneAsync aborted: LocalParticipant is null`                         | Room not connected when publish was attempted               | Ensure full Connected state before any audio publish                          |
| `[AudioTrackManager] PublishMicrophoneAsync failed: track is null`                                     | Track creation failed internally                            | Check SDK version; reinstall package                                          |
| `[RoomAudioRuntimeAdapter] Microphone publish failed: IMicrophoneSourceFactory not registered.`        | Internal SDK wiring failure                                 | Reinstall the SDK; verify package version is 4.2.0                            |
| Microphone works in Editor but not in a build                                                          | `CONVAI_DEBUG_LOGGING` define present in Editor only        | This is not an audio issue — check for missing build permissions              |

***

## Console Log Reference

These are the exact messages from the audio subsystem. Filtering the Console for `RoomAudioRuntimeAdapter` or `AudioTrackManager` shows them directly.

| Message                                                                                                | Level   | What It Means                                                                     |
| ------------------------------------------------------------------------------------------------------ | ------- | --------------------------------------------------------------------------------- |
| `[RoomAudioRuntimeAdapter] Microphone publish aborted because audio playback requires a user gesture.` | Warning | WebGL: connect triggered before a user gesture                                    |
| `[RoomAudioRuntimeAdapter] Microphone publish aborted because the room audio path is not initialized.` | Warning | Mic publish was called before the room audio path was ready                       |
| `[RoomAudioRuntimeAdapter] Microphone publish failed: IMicrophoneSourceFactory not registered.`        | Error   | Internal factory missing — SDK installation issue                                 |
| `[RoomAudioRuntimeAdapter] Microphone publish failed while creating microphone source: {exception}`    | Error   | Exception during mic source creation — check exception message                    |
| `[AudioTrackManager] PublishMicrophoneAsync aborted: LocalParticipant is null`                         | Error   | Room not connected; no local participant                                          |
| `[AudioTrackManager] PublishMicrophoneAsync failed: track is null`                                     | Error   | Mic track creation returned null                                                  |
| `[AudioTrackManager] Exception in PublishMicrophoneAsync: {exception}`                                 | Error   | Unexpected exception — check the exception details                                |
| `[AudioTrackManager] SetMicMuted failed to set mute on MicrophoneSource: {exception}`                  | Error   | Mute operation failed — usually a timing issue                                    |
| `[ConvaiAudioOutput] Registered AudioSource for character '{characterId}'`                             | Debug   | AudioSource successfully registered (visible only in Editor or Development Build) |
| `[ConvaiAudioOutput] ConvaiCharacter component not found on {name}`                                    | Error   | `ConvaiAudioOutput` is on the wrong GameObject                                    |

***

## Next Steps

For how to enable verbose audio logging and use the `Audio` log category override to see all SDK audio messages, see the Debug Tools Reference.

{% content-ref url="/broken/pages/36bfe9c33ac1dc1d9279735540880afca0b017c3" %}
[Broken link](/broken/pages/36bfe9c33ac1dc1d9279735540880afca0b017c3)
{% endcontent-ref %}
