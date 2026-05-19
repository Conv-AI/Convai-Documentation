---
description: >-
  Declare microphone and camera permissions for iOS and Android builds —
  omitting them causes crashes on iOS and silent failures on Android.
---

# iOS and Android

### iOS and Android Deployment Guide

iOS and Android builds use the native transport path. All core SDK features — voice conversation, lip sync, actions, emotion, spatial audio, and Vision — work identically on both platforms. The only required implementation work is declaring OS-level permissions for microphone and camera access before your build goes to a device or an app store.

***

### What Works on iOS and Android

| Feature                            | iOS             | Android         |
| ---------------------------------- | --------------- | --------------- |
| Voice conversation                 | ✅ Full          | ✅ Full          |
| Lip sync                           | ✅ Full          | ✅ Full          |
| Actions                            | ✅ Full          | ✅ Full          |
| Emotion                            | ✅ Full          | ✅ Full          |
| Long-Term Memory                   | ✅ Full          | ✅ Full          |
| Narrative Design                   | ✅ Full          | ✅ Full          |
| Vision (`WebcamVisionFrameSource`) | ✅ Full          | ✅ Full          |
| Spatial audio                      | ✅ Full          | ✅ Full          |
| Unity `AudioSource` playback       | ✅ Full          | ✅ Full          |
| Microphone device selection        | ✅ Full          | ✅ Full          |
| Screen share                       | ❌ Not supported | ❌ Not supported |

***

### Platform and Architecture Support

| Platform | Supported Architectures             |
| -------- | ----------------------------------- |
| iOS      | arm64 (device), x86\_64 (Simulator) |
| Android  | arm64-v8a, armeabi-v7a, x86\_64     |

***

### iOS Setup

#### Permission Declarations

iOS requires usage description strings before your app can request microphone or camera access. Set these in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.

| Key                            | Required When                                | Recommended Description                                                                                     |
| ------------------------------ | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `NSMicrophoneUsageDescription` | Always — required for all voice interactions | `This app uses your microphone to enable voice conversations with AI training characters.`                  |
| `NSCameraUsageDescription`     | Only when Vision is enabled                  | `This app uses your camera so the AI character can see and respond to what you show during the simulation.` |

{% hint style="danger" %}
**Omitting `NSMicrophoneUsageDescription` crashes the app.** iOS raises `NSInvalidArgumentException` when an app attempts microphone access without this key. The crash occurs at runtime on the first conversation attempt and triggers Apple App Store rejection during review. `NSCameraUsageDescription` carries the same crash risk when Vision is enabled.
{% endhint %}

#### iOS Runtime Permission Handling

The SDK automatically calls `Application.RequestUserAuthorization(UserAuthorization.Microphone)` before the first conversation session. iOS displays the permission prompt once per permission type — subsequent launches skip the prompt if permission was already granted or denied.

{% hint style="warning" %}
**iOS one-time prompts cannot be re-triggered.** If a user denies microphone permission, iOS will not show the prompt again. Your app must guide the user to **Settings → Privacy & Security → Microphone** to re-enable access manually. Add in-app messaging for this case — for example, detect denied permission via `Application.HasUserAuthorization(UserAuthorization.Microphone)` and display instructions before attempting to start a session.
{% endhint %}

You can pre-check permission status before starting a session to provide contextual guidance:

```csharp
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

***

### Android Setup

#### Manifest Permissions

Declare required permissions in a custom `AndroidManifest.xml` at `Assets/Plugins/Android/AndroidManifest.xml`.

```xml
<!-- Required for all voice interactions -->
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<!-- Required only when Vision is enabled -->
<uses-permission android:name="android.permission.CAMERA" />
```

{% hint style="warning" %}
If `Assets/Plugins/Android/AndroidManifest.xml` does not exist in your project, create it. Unity merges it with the generated manifest at build time. After building, verify that the permissions appear in the exported `AndroidManifest.xml` inside the APK or AAB — Unity's manifest merge can sometimes omit entries if the file is malformed.
{% endhint %}

#### Android Runtime Permission Handling

The SDK automatically calls `Permission.RequestUserPermission(Permission.Microphone)` before the initial conversation. Unlike iOS, Android permits repeated permission requests — however, the SDK does not retry automatically if the user denies the request. After two denials, Android may present a "Don't ask again" option, after which `Permission.RequestUserPermission` has no effect. Handle this case with in-app guidance directing the user to device Settings.

***

### Vision on Mobile

`WebcamVisionFrameSource` functions on both iOS and Android. Add the component to a GameObject in your scene and assign a `ConvaiVisionPublisher`. The Unity Inspector displays platform-specific warnings if required permissions are absent — address these before building.

{% hint style="info" %}
On iOS, Vision requires both `NSCameraUsageDescription` in Player Settings and a granted runtime permission. On Android, Vision requires `android.permission.CAMERA` in the manifest. Both are covered in the setup sections above.
{% endhint %}

***

### Background Behavior

When the app moves to the background, the OS suspends microphone capture automatically. Upon returning to the foreground, the SDK resumes capture without developer intervention. Session state follows the reconnection rules defined in your lifecycle configuration.

***

### Usage Examples

#### Field Safety Compliance Drill on Android

A manufacturing company deploys a safety inspector training app on Android tablets issued to production floor staff. The Convai character plays a safety auditor who runs operators through equipment inspection protocols verbally.

**Setup:**

1. Add `<uses-permission android:name="android.permission.RECORD_AUDIO" />` to `Assets/Plugins/Android/AndroidManifest.xml`.
2. Standard SDK configuration — no Vision, no camera permission required.
3. After building, verify `RECORD_AUDIO` appears in the exported manifest.

**Outcome:** On first launch, Android displays the microphone permission prompt. After the user grants access, the Convai character begins the inspection dialogue. Subsequent launches skip the prompt. The app guides users to device Settings if permission was previously denied.

***

#### Surgical Consultation Training on iOS with Vision

A medical school deploys a patient consultation training app on iPad Pros. Residents practice verbal interaction with a Convai patient character. Vision is enabled so the character can acknowledge physical props — anatomical models and procedure reference cards — held up by the resident.

**Setup:**

1. In **Project Settings → Player → iOS → Other Settings → Usage Descriptions**, set:
   * `NSMicrophoneUsageDescription`: `This app uses your microphone to enable voice conversations with AI training characters.`
   * `NSCameraUsageDescription`: `This app uses your camera so the AI character can see and respond to what you show during the simulation.`
2. Add `WebcamVisionFrameSource` to a scene GameObject and assign a `ConvaiVisionPublisher`.
3. Standard SDK configuration for voice conversation.

**Outcome:** On first launch, iOS displays the microphone permission prompt followed by the camera permission prompt. After both are granted, the resident speaks with the character and holds up physical props in view of the iPad camera. The character acknowledges what it sees and responds with clinically appropriate dialogue.

***

### Troubleshooting

| Symptom                                                    | Likely Cause                                                | Fix                                                                                                                                                                                                      |
| ---------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| App crashes on first voice attempt (iOS)                   | `NSMicrophoneUsageDescription` missing from Player Settings | Add the key in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.                                                                                                                |
| App crashes when Vision starts (iOS)                       | `NSCameraUsageDescription` missing from Player Settings     | Add the key in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.                                                                                                                |
| Microphone permission prompt never appears (Android)       | `RECORD_AUDIO` missing from `AndroidManifest.xml`           | Add `<uses-permission android:name="android.permission.RECORD_AUDIO" />` to your manifest and verify it appears in the exported APK.                                                                     |
| Camera permission prompt never appears on Android (Vision) | `CAMERA` missing from `AndroidManifest.xml`                 | Add `<uses-permission android:name="android.permission.CAMERA" />` to your manifest.                                                                                                                     |
| Microphone stops working after app is backgrounded         | OS suspended capture — expected behavior                    | The SDK resumes capture automatically on foreground return. No action needed.                                                                                                                            |
| iOS prompt does not appear on second launch                | User denied on first launch — iOS does not re-prompt        | Add in-app messaging directing the user to **Settings → Privacy & Security → Microphone** to re-enable. Use `Application.HasUserAuthorization(UserAuthorization.Microphone)` to detect the denied state. |

***

### Next Steps

Once permissions are declared and tested on a physical device, your iOS and Android builds are ready for distribution. If you are deploying on XR headsets, those builds have additional Vision requirements.

{% content-ref url="/broken/pages/5a8d70bb1abe82b0a71b11c201ca0e03fe774511" %}
[Broken link](/broken/pages/5a8d70bb1abe82b0a71b11c201ca0e03fe774511)
{% endcontent-ref %}

{% content-ref url="/broken/pages/78fe0e353e3f4aef3b9b55038877dd98da20d25a" %}
[Broken link](/broken/pages/78fe0e353e3f4aef3b9b55038877dd98da20d25a)
{% endcontent-ref %}
