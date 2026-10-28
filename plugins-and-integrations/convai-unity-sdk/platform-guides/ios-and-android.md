---
title: iOS and Android
description: >-
  Configure iOS and Android permissions, native libraries, echo cancellation,
  and camera capture, then verify voice and recovery on physical devices.
last_reviewed: "5.0.0-preview"
---

iOS and Android builds use the native transport path. Voice, lip sync, actions, emotion, spatial audio and supported Vision sources have native implementations. Configure permissions and audio policy, then validate on each device; OS audio behavior and recovery are not identical.

## Feature support

| Feature                            | iOS             | Android         |
| ---------------------------------- | --------------- | --------------- |
| Voice conversation                 | ✅ Implemented          | ✅ Implemented          |
| Lip sync                           | ✅ Implemented          | ✅ Implemented          |
| Actions                            | ✅ Implemented          | ✅ Implemented          |
| Emotion                            | ✅ Implemented          | ✅ Implemented          |
| Long-Term Memory                   | ✅ Implemented          | ✅ Implemented          |
| Narrative Design                   | ✅ Implemented          | ✅ Implemented          |
| Vision (`WebcamVisionFrameSource`) | ✅ Implemented          | ✅ Implemented          |
| Spatial audio                      | ✅ Implemented          | ✅ Implemented          |
| Unity `AudioSource` playback       | ✅ Implemented          | ✅ Implemented          |
| Microphone device selection        | ✅ Implemented          | ✅ Implemented          |

| Platform | Supported architectures             |
| -------- | ----------------------------------- |
| iOS      | arm64 (device), arm64 (Simulator) |
| Android  | arm64-v8a, armeabi-v7a, x86\_64     |

## iOS setup

iOS requires usage description strings before your app can request microphone or camera access. Set these in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.

| Key                            | Required when                                | Recommended description                                                                                     |
| ------------------------------ | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `NSMicrophoneUsageDescription` | Always — required for all voice interactions | `This app uses your microphone to enable voice conversations with AI training characters.`                  |
| `NSCameraUsageDescription`     | When capturing a physical camera                  | `This app uses your camera so the AI character can see and respond to what you show during the simulation.` |

{% hint style="danger" %}
**Omitting `NSMicrophoneUsageDescription` crashes the app.** iOS raises `NSInvalidArgumentException` when an app attempts microphone access without this key. Set the description before any microphone access. `NSCameraUsageDescription` carries the same crash risk when a physical camera is used.
{% endhint %}

### Runtime permission handling

The 5.0 SDK requests microphone permission before opening capture. Handle denial in your UI and do not repeatedly start capture after access is refused. For an application-owned onboarding flow, you can request access before enabling the room. The permission service exposes `GetMicrophoneAccess()` and `RequestMicrophoneAccess`; states include Unknown, NotRequested, Granted, Denied, NoMicrophone and Unavailable.

Enable **Prepare iOS for Recording**. **Convai > Settings > Setup Health** checks this setting and the combined **macOS / iOS Microphone Usage Description**. Use its Setup action when the description is missing.

<figure><img src="../../../.gitbook/assets/unity-setup-health.png" alt="Setup Health checks for Apple microphone description, recording preparation and Android permission"><figcaption><p>Review these project checks before testing on a device.</p></figcaption></figure>

{% hint style="warning" %}
**iOS one-time prompts cannot be re-triggered.** If a user denies microphone permission, iOS will not show the prompt again. Your app must guide the user to **Settings → Privacy & Security → Microphone** to re-enable access manually. Add in-app messaging for this case — for example, detect denied permission via `Application.HasUserAuthorization(UserAuthorization.Microphone)` and display instructions before attempting to start a session.
{% endhint %}

Request permission and check the result before starting a session:

```csharp
using System.Collections;
using UnityEngine;

public class MicPermissionCheck : MonoBehaviour
{
    private IEnumerator Start()
    {
        if (!Application.HasUserAuthorization(UserAuthorization.Microphone))
        {
            yield return Application.RequestUserAuthorization(UserAuthorization.Microphone);
        }

        if (!Application.HasUserAuthorization(UserAuthorization.Microphone))
        {
            // User denied. Show guidance to re-enable in iOS Settings.
            ShowPermissionDeniedUI();
            yield break;
        }

        // Permission granted — proceed to start the session.
    }

    private void ShowPermissionDeniedUI()
    {
        // Display instructions directing the user to iOS Settings.
    }
}
```

### Example: Surgical consultation training on iOS with Vision

A medical school deploys a patient consultation training app on iPad Pros. Residents practice verbal interaction with a Convai patient character. Vision is enabled so the character can acknowledge physical props — anatomical models and procedure reference cards — held up by the resident.

**Setup:**

1. In **Project Settings → Player → iOS → Other Settings → Usage Descriptions**, set:
   * `NSMicrophoneUsageDescription`: `This app uses your microphone to enable voice conversations with AI training characters.`
   * `NSCameraUsageDescription`: `This app uses your camera so the AI character can see and respond to what you show during the simulation.`
2. Add `WebcamVisionFrameSource` to a scene GameObject and assign it to a `ConvaiVisionPublisher`.
3. Standard SDK configuration for voice conversation.

**Outcome:** On first launch, iOS displays the microphone permission prompt followed by the camera permission prompt. After both are granted, the resident speaks with the character and holds up physical props in view of the iPad camera. The character acknowledges what it sees and responds according to its authored character configuration. Treat this as a training scenario, not clinical validation.

## Android setup

Unity normally adds `RECORD_AUDIO` when microphone APIs are used. Do not create a custom manifest solely to duplicate it. If your project has a custom `AndroidManifest.xml`, verify the merged result retains microphone permission. Physical-camera Vision also needs `CAMERA`. The relevant merged entries are:

```xml
<!-- Required for all voice interactions -->
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<!-- Required when capturing a physical camera -->
<uses-permission android:name="android.permission.CAMERA" />
```

After building, verify that the permissions appear in the exported `AndroidManifest.xml` inside the APK or AAB — Unity's manifest merge can sometimes omit entries if the file is malformed.

### Runtime permission handling

The SDK requests microphone access before opening the Android input device. Handle grant, denial and unavailable-device states in your UI. If the OS no longer presents a prompt, guide the user to device settings instead of retrying indefinitely. The ordinary room can remain usable for [typed input](../getting-started/run-a-text-only-session.md).

### Example: Field safety compliance drill on Android

A manufacturing company deploys a safety inspector training app on Android tablets issued to production floor staff. The Convai character plays a safety auditor who runs operators through equipment inspection protocols verbally.

**Setup:**

1. Confirm the merged Android manifest contains `RECORD_AUDIO`; check any custom manifest if it is missing.
2. Standard SDK configuration — no Vision, no camera permission required.
3. After building, verify `RECORD_AUDIO` appears in the exported manifest.

**Outcome:** On first launch, Android displays the microphone permission prompt. After the user grants access, the Convai character begins the inspection dialogue. Subsequent launches skip the prompt. The app guides users to device Settings if permission was previously denied.

## Vision on mobile

`WebcamVisionFrameSource` functions on both iOS and Android. Add the component to a GameObject and assign it as the publisher's frame source. Its Inspector displays a fixed reminder for the active build target; it does not inspect the built application and prove a permission is present.

On iOS, Vision requires `NSCameraUsageDescription` in Player Settings — the component calls `Application.RequestUserAuthorization(UserAuthorization.WebCam)` automatically at runtime to request the permission. On Android, Vision requires `android.permission.CAMERA` in the manifest — the component calls `Permission.RequestUserPermission(Permission.Camera)` automatically at runtime. You do not need to request camera permission manually; declaring it in Player Settings (iOS) or the manifest (Android) is sufficient.

When audio plays through the phone speakers, enable **Room Manager > Listening > Microphone > Echo Cancellation**. The default is off. Hands Free on phone targets shows a warning when echo cancellation is disabled. Test interruption, background/foreground transitions and reconnect on physical devices; recovery depends on both the OS and your session policy.

## Troubleshooting

| Symptom                                                    | Likely cause                                                | Fix                                                                                                                                                                                                      |
| ---------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| App crashes on first voice attempt (iOS)                   | `NSMicrophoneUsageDescription` missing from Player Settings | Add the key in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.                                                                                                                |
| App crashes when Vision starts (iOS)                       | `NSCameraUsageDescription` missing from Player Settings     | Add the key in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.                                                                                                                |
| Microphone permission prompt never appears (Android)       | `RECORD_AUDIO` missing from `AndroidManifest.xml`           | Add `<uses-permission android:name="android.permission.RECORD_AUDIO" />` to your manifest and verify it appears in the exported APK.                                                                     |
| Camera permission prompt never appears on Android (Vision) | `CAMERA` missing from `AndroidManifest.xml`                 | Add `<uses-permission android:name="android.permission.CAMERA" />` to your manifest.                                                                                                                     |
| Microphone stops working after app is backgrounded         | OS suspended capture — expected behavior                    | Check permissions, device availability and the configured session recovery path; reproduce on the target device.                                                                                                                            |
| iOS prompt does not appear on second launch                | User denied on first launch — iOS does not re-prompt        | Add in-app messaging directing the user to **Settings → Privacy & Security → Microphone** to re-enable. Use `Application.HasUserAuthorization(UserAuthorization.Microphone)` to detect the denied state. |

## Next steps

Permission and media tests on a physical device are part of release validation, alongside your application's other distribution checks. If you are also deploying on XR headsets, those builds have additional Vision requirements.

{% content-ref url="xr-headsets.md" %}
[XR headsets](xr-headsets.md)
{% endcontent-ref %}

{% content-ref url="webgl.md" %}
[WebGL](webgl.md)
{% endcontent-ref %}
