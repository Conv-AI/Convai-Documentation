# mobile ios and android

Mobile builds use the native transport path — full feature parity with desktop. Voice conversation, lip sync, actions, emotion, spatial audio, and Vision all work on iOS and Android without behavioral differences. The only platform-specific work is declaring permissions so the OS knows your app needs microphone (and optionally camera) access. The SDK requests those permissions automatically at runtime; you provide the declarations.

***

## What Works on Mobile

| Feature                      | iOS    | Android |
| ---------------------------- | ------ | ------- |
| Voice conversation           | ✅ Full | ✅ Full  |
| Lip sync                     | ✅ Full | ✅ Full  |
| Actions                      | ✅ Full | ✅ Full  |
| Emotion                      | ✅ Full | ✅ Full  |
| Long-Term Memory             | ✅ Full | ✅ Full  |
| Narrative Design             | ✅ Full | ✅ Full  |
| Vision (webcam)              | ✅ Full | ✅ Full  |
| Spatial audio                | ✅ Full | ✅ Full  |
| Microphone device selection  | ✅ Full | ✅ Full  |
| Unity `AudioSource` playback | ✅ Full | ✅ Full  |

***

## iOS Setup

### Required Privacy Descriptions

iOS requires usage description strings for any hardware the app accesses. These are set in **Project Settings → Player → iOS → Other Settings → Usage Descriptions**.

| Description Key                | When Required                                      |
| ------------------------------ | -------------------------------------------------- |
| `NSMicrophoneUsageDescription` | Always — required for voice conversation           |
| `NSCameraUsageDescription`     | Only when Vision (webcam) is enabled in your scene |

{% hint style="danger" %}
If `NSMicrophoneUsageDescription` is missing, iOS throws `NSInvalidArgumentException` and crashes the app the moment the SDK requests microphone access. Apple also rejects builds that access hardware without the corresponding usage description.
{% endhint %}

Write descriptions that explain the feature to the user — Apple's review guidelines require meaningful text:

* `NSMicrophoneUsageDescription`: "This app uses your microphone to enable voice conversations with AI training characters."
* `NSCameraUsageDescription`: "This app uses your camera so the AI character can see and respond to what you show during the simulation."

### Permission Flow

The SDK calls `Application.RequestUserAuthorization(UserAuthorization.Microphone)` automatically before the first conversation session starts. When Vision is enabled, it calls `RequestUserAuthorization(UserAuthorization.WebCam)` before first capture. You do not need to trigger these requests manually.

{% hint style="info" %}
**iOS only prompts once per permission type.** If the user denies microphone access, iOS will not show the prompt again — the user must re-enable it in **Settings → Privacy & Security → Microphone**. Consider showing an in-app explanation if permission is denied, guiding the user to re-enable it.
{% endhint %}

If you want to check permission state before the SDK connects — for example, to show an explanation screen — you can query it early:

{% code title="PermissionCheck.cs" %}
```csharp
using System.Collections;
using UnityEngine;

public class PermissionCheck : MonoBehaviour
{
    private IEnumerator Start()
    {
        if (!Application.HasUserAuthorization(UserAuthorization.Microphone))
        {
            // Optionally show explanation UI here before the system dialog appears
            yield return Application.RequestUserAuthorization(UserAuthorization.Microphone);
        }

        // Proceed with scene initialization
    }
}
```
{% endcode %}

***

## Android Setup

### Required Manifest Permissions

Android requires explicit permission declarations in `AndroidManifest.xml`. Place your custom manifest at `Assets/Plugins/Android/AndroidManifest.xml`.

{% code title="AndroidManifest.xml" %}
```xml
<!-- Required for voice conversation -->
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<!-- Required only if Vision (webcam) is enabled -->
<uses-permission android:name="android.permission.CAMERA" />
```
{% endcode %}

{% hint style="info" %}
Unity automatically adds `RECORD_AUDIO` to the manifest when it detects microphone API usage in the build. Verify that it appears in the exported manifest at `<YourProject>/Temp/StagingArea/AndroidManifest.xml` before submitting to Google Play — especially in projects with custom manifest merging.
{% endhint %}

### Permission Flow

The SDK calls `Permission.RequestUserPermission(Permission.Microphone)` automatically before the first conversation session. Vision calls `Permission.RequestUserPermission(Permission.Camera)` before first capture. Both use Android's standard runtime permission callback system with grant and deny handlers.

If the user denies a permission, conversation or Vision cannot start. Design your UX to handle the denied state — the SDK does not retry permission requests automatically.

***

## Vision on Mobile

`WebcamVisionFrameSource` works on both iOS and Android. Camera permission is requested automatically on the first `StartCapture()` call.

The Inspector shows platform-specific warnings when `WebcamVisionFrameSource` is in your scene:

* **Android:** "Android: the CAMERA permission will be requested at runtime. Ensure it is declared in your AndroidManifest.xml."
* **iOS:** "iOS: NSCameraUsageDescription must be set in Player Settings → Other Settings."

These warnings appear in the Unity Editor Inspector — address them before building.

***

## App Backgrounding

When your app moves to the background, the OS suspends microphone capture. When the app returns to the foreground, the SDK restarts capture automatically. No code is required to handle this.

The Convai session state follows the reconnect rules defined in the session lifecycle. If the connection drops while backgrounded, the SDK reconnects when the app resumes. See **Core Concepts → Session Lifecycle and State Management** for reconnect configuration options.

***

## Usage Examples

### Field Safety Inspection on Android

A manufacturing company deploys a safety drill application to Android tablets. Field inspectors speak with a Convai character that guides them through compliance check procedures and records their responses.

**Setup:** Add `android.permission.RECORD_AUDIO` to `AndroidManifest.xml`. Vision is not required for this scenario — omit `CAMERA`. The SDK requests microphone permission on the first session start. No additional configuration needed.

**Outcome:** On first launch, the Android permission dialog appears for microphone access. The inspector speaks; the character responds in real time. Spatial audio routes through the tablet speaker. The session records completion via an Action trigger that fires when all checklist items are addressed.

***

### Medical Training Simulation on iOS

A surgical training application on iPad places learners in mock patient consultations. A Convai character plays the patient role. Vision is enabled so the character can see and respond to physical props — models, instruments, reference cards — the trainee holds up.

**Setup:** In Player Settings → iOS → Other Settings:

* `NSMicrophoneUsageDescription`: "This app uses your microphone for training conversations with the patient character."
* `NSCameraUsageDescription`: "This app uses your camera so the patient character can see and respond to what you show during the consultation."

Vision is enabled via `WebcamVisionFrameSource` on the scene's Vision Publisher GameObject.

**Outcome:** On first launch, iOS shows the microphone permission dialog. When the trainee first shows something to the camera, the camera permission dialog appears. The character responds to both voice and visual context. The app passes Apple's App Store review because both usage descriptions are present and meaningful.

***

## Troubleshooting

| Symptom                                                   | Likely Cause                            | Fix                                                                                         |
| --------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------- |
| App crashes on iOS when conversation starts               | `NSMicrophoneUsageDescription` missing  | Add the key in Player Settings → iOS → Other Settings → Usage Descriptions                  |
| App crashes on iOS when Vision starts                     | `NSCameraUsageDescription` missing      | Add the key in Player Settings → iOS → Other Settings → Usage Descriptions                  |
| App rejected by Apple App Store review                    | Usage description missing or empty      | Write meaningful usage description strings — Apple requires user-readable text              |
| Microphone permission dialog never appears on Android     | `RECORD_AUDIO` not declared in manifest | Add to `AndroidManifest.xml`; verify it appears in the exported manifest                    |
| Camera permission dialog never appears on Android         | `CAMERA` not declared in manifest       | Add `android.permission.CAMERA` to `AndroidManifest.xml`                                    |
| User denied microphone on iOS; dialog never appears again | iOS one-time prompt behavior            | Show an in-app message directing the user to **Settings → Privacy & Security → Microphone** |
| Microphone stops when app goes to background              | Expected mobile OS behavior             | Capture restarts automatically when the app returns to foreground                           |
| Vision camera feed goes black on iOS after backgrounding  | iOS suspends camera in background       | Vision restarts automatically on foreground; no action needed                               |

***

## Next Steps

{% content-ref url="/broken/pages/ff400377bdbe8a12298f59c05337311a5c570cc2" %}
[Broken link](/broken/pages/ff400377bdbe8a12298f59c05337311a5c570cc2)
{% endcontent-ref %}

{% content-ref url="/broken/pages/f796a49a82f4b79cf42397dc35d3add7a3f73bdd" %}
[Broken link](/broken/pages/f796a49a82f4b79cf42397dc35d3add7a3f73bdd)
{% endcontent-ref %}
