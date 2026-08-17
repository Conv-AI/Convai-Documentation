---
title: iOS and Android
description: >-
  Declare microphone and camera permissions for iOS and Android builds —
  omitting them causes crashes on iOS and silent failures on Android.
last_reviewed: "4.5.0"
---

iOS and Android builds use the native transport path. SDK 4.5.0 contains mobile paths for conversation, embodiment, audio, and Vision, but source support is not device proof. Configure the required usage descriptions and permissions, then validate the distributed package on every OS version and device class you ship.

## Feature support

| Feature                            | iOS             | Android         |
| ---------------------------------- | --------------- | --------------- |
| Voice conversation                 | SDK path*        | SDK path*        |
| Lip sync                           | SDK path*        | SDK path*        |
| Actions                            | SDK path*        | SDK path*        |
| Emotion                            | SDK path*        | SDK path*        |
| Long-Term Memory                   | SDK path*        | SDK path*        |
| Narrative Design                   | SDK path*        | SDK path*        |
| Vision (`WebcamVisionFrameSource`) | SDK path*        | SDK path*        |
| Spatial audio                      | SDK path*        | SDK path*        |
| Unity `AudioSource` playback       | SDK path*        | SDK path*        |
| Microphone device selection        | SDK path*        | SDK path*        |
| Screen share                       | ❌ Not supported | ❌ Not supported |

`SDK path*` means the 4.5.0 source and platform adapters contain the integration path. It does not replace physical-device or distributed-package validation.

| Platform | Supported architectures             |
| -------- | ----------------------------------- |
| iOS      | arm64 (device), x86\_64 (Simulator) |
| Android  | arm64-v8a, armeabi-v7a, x86\_64     |

## iOS setup

iOS requires usage description strings before your app can request microphone or camera access. Set these in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.

| Key                            | Required when                                | Recommended description                                                                                     |
| ------------------------------ | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `NSMicrophoneUsageDescription` | Always — required for all voice interactions | `This app uses your microphone to enable voice conversations with AI training characters.`                  |
| `NSCameraUsageDescription`     | Only when Vision is enabled                  | `This app uses your camera so the AI character can see and respond to what you show during the simulation.` |

{% hint style="danger" %}
**Omitting `NSMicrophoneUsageDescription` crashes the app.** iOS raises `NSInvalidArgumentException` when an app attempts microphone access without this key. The crash occurs at runtime on the first conversation attempt and triggers Apple App Store rejection during review. `NSCameraUsageDescription` carries the same crash risk when Vision is enabled.
{% endhint %}

### Runtime permission handling

The iOS native audio path accesses the microphone when recording starts, which causes the operating system permission flow. You can request `UserAuthorization.Microphone` earlier to control when the prompt appears and to present denial guidance before connecting. iOS displays the system prompt once per permission type; later launches retain the user's decision.

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
2. Add `WebcamVisionFrameSource` to a scene GameObject and assign a `ConvaiVisionPublisher`.
3. Standard SDK configuration for voice conversation.

**Validate on device:** Confirm the expected microphone and camera prompts, successful capture after both grants, and your denial/recovery UI. Character interpretation and dialogue are backend outcomes and must be tested with the deployed character configuration.

## Android setup

Build once and inspect the merged Android manifest in the exported APK or AAB. Unity's normal microphone and camera packaging should supply the permissions used by those APIs. If your build pipeline omits either required entry, add it in `Assets/Plugins/Android/AndroidManifest.xml` so Unity merges it into the final manifest.

```xml
<!-- Required for all voice interactions -->
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<!-- Required only when Vision is enabled -->
<uses-permission android:name="android.permission.CAMERA" />
```

After building, verify that the permissions appear in the exported `AndroidManifest.xml` inside the APK or AAB — Unity's manifest merge can sometimes omit entries if the file is malformed.

### Runtime permission handling

The SDK's native audio path checks `Permission.Microphone` and requests it before recording when access is missing. An application can still preflight the same permission to control onboarding and denial UI. If Android reports a permanent denial, direct the user to device Settings rather than repeatedly requesting it.

### Example: Field safety compliance drill on Android

A manufacturing company deploys a safety inspector training app on Android tablets issued to production floor staff. The Convai character plays a safety auditor who runs operators through equipment inspection protocols verbally.

**Setup:**

1. Verify `<uses-permission android:name="android.permission.RECORD_AUDIO" />` exists in the merged manifest; add a custom manifest entry only if it is absent.
2. Standard SDK configuration — no Vision, no camera permission required.
3. After building, verify `RECORD_AUDIO` appears in the exported manifest.

**Validate on device:** Confirm the runtime prompt, successful recording after a grant, retained permission behavior on relaunch, and your permanent-denial path.

## Vision on mobile

`WebcamVisionFrameSource` functions on both iOS and Android. Add the component to a GameObject in your scene and assign a `ConvaiVisionPublisher`. The Unity Inspector displays platform-specific warnings if required permissions are absent — address these before building.

On iOS, Vision requires `NSCameraUsageDescription` in Player Settings — the component calls `Application.RequestUserAuthorization(UserAuthorization.WebCam)` automatically at runtime to request the permission. On Android, Vision requires `android.permission.CAMERA` in the manifest — the component calls `Permission.RequestUserPermission(Permission.Camera)` automatically at runtime. You do not need to request camera permission manually; declaring it in Player Settings (iOS) or the manifest (Android) is sufficient.

Mobile operating systems can suspend capture or networking while an app is backgrounded. Observe the SDK runtime-background and session events, then verify foreground recovery on each target device. If the room reconnects, reacquire connection-scoped state and subscriptions rather than assuming capture resumed in place.

## Troubleshooting

| Symptom                                                    | Likely cause                                                | Fix                                                                                                                                                                                                      |
| ---------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| App crashes on first voice attempt (iOS)                   | `NSMicrophoneUsageDescription` missing from Player Settings | Add the key in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.                                                                                                                |
| App crashes when Vision starts (iOS)                       | `NSCameraUsageDescription` missing from Player Settings     | Add the key in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.                                                                                                                |
| Microphone permission prompt never appears (Android)       | `RECORD_AUDIO` missing from `AndroidManifest.xml`           | Add `<uses-permission android:name="android.permission.RECORD_AUDIO" />` to your manifest and verify it appears in the exported APK.                                                                     |
| Camera permission prompt never appears on Android (Vision) | `CAMERA` missing from `AndroidManifest.xml`                 | Add `<uses-permission android:name="android.permission.CAMERA" />` to your manifest.                                                                                                                     |
| Microphone stops working after app is backgrounded         | OS suspended capture or the room reconnected                | Observe runtime-background/session events; restore the intended input mode after connection recovery and test on the target device.                                                                       |
| iOS prompt does not appear on second launch                | User denied on first launch — iOS does not re-prompt        | Add in-app messaging directing the user to **Settings → Privacy & Security → Microphone** to re-enable. Use `Application.HasUserAuthorization(UserAuthorization.Microphone)` to detect the denied state. |

## Next steps

Once permissions are declared and tested on a physical device, your iOS and Android builds are ready for distribution. If you are also deploying on XR headsets, those builds have additional Vision requirements.

{% content-ref url="xr-headsets.md" %}
[XR headsets](xr-headsets.md)
{% endcontent-ref %}

{% content-ref url="webgl.md" %}
[WebGL](webgl.md)
{% endcontent-ref %}
