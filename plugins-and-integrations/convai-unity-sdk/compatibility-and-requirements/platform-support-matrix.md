---
title: Platform support matrix
description: Reference for Convai Unity SDK platform support, including feature availability across Windows, macOS, Android, iOS, Meta Quest, and WebGL.
last_reviewed: "5.0.0-preview"
---

This matrix describes implemented platform paths in the reviewed 5.0 preview source. Feature availability depends on the device, browser, permissions and service configuration. Validate a built application on each target; this matrix is not a record of release qualification.

## Feature × platform matrix

| Feature                    | Windows / macOS / Linux | Android                        | iOS                                    | Meta Quest            | WebGL                                  |
| -------------------------- | ----------------------- | ------------------------------ | -------------------------------------- | --------------------- | -------------------------------------- |
| Voice conversation         | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Microphone capture         | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available — HTTPS + microphone permission required |
| Remote audio playback      | ✅ Unity `AudioSource`   | ✅ Unity `AudioSource`          | ✅ Unity `AudioSource`                  | ✅ Unity `AudioSource` | ⚠️ Browser-routed                      |
| Lip sync                   | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ⚠️ Browser playback clock                  |
| Spatial audio              | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ❌ Not supported                        |
| Actions                    | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Emotion                    | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Long-Term Memory           | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Narrative Design           | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Dynamic Context            | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Vision — Camera            | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Frame Source by default                      |
| Vision — Webcam            | ✅ Available                  | ⚠️ Runtime permission required | ⚠️ `NSCameraUsageDescription` required | ❌ Not applicable      | ❌ Not supported                        |
| Vision — Quest passthrough | ❌ Not supported         | ❌ Not supported                | ❌ Not supported                        | ✅ Available                | ❌ Not supported                        |
| Text-only ordinary rooms | ✅ Available | ✅ Available | ✅ Available | ✅ Available | ✅ Available |
| On-device Sentis/Silero voice detection | ✅ Native path | ✅ Native path | ✅ Native path | ✅ Native path | ❌ Excluded from build |
| Push-to-talk finalization | Capture drain when supported | Capture drain when supported | Capture drain when supported | Capture drain when supported | Legacy release |
| Group conversation | Correlated PTT required | Correlated PTT required | Correlated PTT required | Correlated PTT required | ❌ Legacy release cannot run group PTT |

The Scene Auto Tagger window and `ConvaiSceneTagger` are Editor authoring tools for Windows x64 and macOS, with separate native Core distribution gates. They are not player-platform features. See [Scene Auto Tagger](../features/scene-metadata/scene-auto-tagger.md).

`ConvaiObjectAutotagClient` is separate. It sends your own images to Convai Vision from the Editor and from player builds, WebGL included, and needs no native libraries. See [Call Convai Vision directly](../features/scene-metadata/scene-auto-tagger-scripting-api.md#call-convai-vision-directly).

## Platform-specific requirements

{% tabs %}
{% tab title="WebGL" %}
WebGL uses browser media and permission APIs:

* **Microphone capture** requires HTTPS or `localhost`. HTTP deployments cannot access the microphone. When playback is blocked, the default manager retries audio unlock on eligible non-UI clicks after connection. A UI button can call `ConvaiManager.EnableAudioAndStartListening()` explicitly.
* **Remote audio playback** is routed through the browser's audio system, not Unity's `AudioSource`. Use `ConvaiAudioOutput.Volume` and `IsMuted` for browser playback control. Unity distance rolloff and listener volume do not apply; iOS Safari controls its own nonzero media volume.
* **Vision — Camera** publishes the configured frame source by default. **WebGL Publishes > Game View** explicitly captures the visible Unity canvas, including its UI. A custom `IVisionPageCanvasSource` can provide a page canvas.
* **Vision — Webcam** (`WebcamVisionFrameSource`) is not supported on WebGL — `AsyncGPUReadback` is unavailable in the browser runtime. Use the supported camera frame-source path instead.
* **Spatial audio** is not supported on WebGL.

{% hint style="warning" %}
WebGL aligns lip sync to measured browser voice onset, waiting up to two seconds through initial silence, and uses a realtime playback clock. Verify timing in the target browser and hosting environment.
{% endhint %}

{% hint style="info" %}
Always validate WebGL builds in the actual hosting environment, especially if the build is embedded in an iframe. Add `allow="microphone"` to the iframe tag if you embed the build in a page you control.
{% endhint %}

For detailed WebGL setup, browser compatibility, and deployment steps, see the WebGL platform guide.

{% content-ref url="../platform-guides/webgl.md" %}
[WebGL deployment guide](../platform-guides/webgl.md)
{% endcontent-ref %}
{% endtab %}

{% tab title="Android" %}
* **Microphone:** The SDK requests `RECORD_AUDIO` permission at runtime via `ConvaiPermissionService`. Unity normally adds that manifest permission when microphone APIs are used. Verify a custom manifest does not remove it, and handle denial in your app flow.
* **Vision — Webcam:** `android.permission.CAMERA` is requested at runtime by `WebcamVisionFrameSource`. Handle permission grant and denial in your app flow.

For Android build configuration, permission handling, and microphone setup, see the iOS and Android platform guide.

{% content-ref url="../platform-guides/ios-and-android.md" %}
[iOS and Android platform guide](../platform-guides/ios-and-android.md)
{% endcontent-ref %}
{% endtab %}

{% tab title="iOS" %}
* **Microphone:** The SDK requests access before opening capture. `NSMicrophoneUsageDescription` must be set in **Player Settings → Other Settings → iOS → Microphone Usage Description**. Omitting this causes a crash on first microphone access.
* **Vision — Webcam:** `NSCameraUsageDescription` must be set in **Player Settings → Other Settings → iOS → Camera Usage Description** if you use `WebcamVisionFrameSource`. On iOS, `WebcamVisionFrameSource` accesses the device camera via Unity's `WebCamTexture` API.
* Enable **Prepare iOS for Recording** and use **Setup Health** to check the microphone description.
* Define your app's behavior when the user denies microphone or camera permission, and when the app is interrupted or backgrounded during a conversation.

For iOS build configuration, permission setup, and Info.plist requirements, see the iOS and Android platform guide.

{% content-ref url="../platform-guides/ios-and-android.md" %}
[iOS and Android platform guide](../platform-guides/ios-and-android.md)
{% endcontent-ref %}
{% endtab %}

{% tab title="Meta Quest" %}
Quest passthrough vision (`QuestVisionFrameSource`) is supported on **Quest 3 and Quest 3S only**.

**Requirements:**

* Meta XR SDK imported into your project
* `PassthroughCameraAccess` component present in the scene
* The `horizonos.permission.HEADSET_CAMERA` and `android.permission.CAMERA` permissions granted to the app

The Convai Unity SDK does not ship an `AndroidManifest.xml` and does not declare or request these permissions itself — `QuestVisionFrameSource` requires both to already be granted. Declare them in your project's manifest and confirm they are granted before relying on passthrough capture.

On other Quest hardware or non-Quest platforms, `QuestVisionFrameSource` produces no frames. Use `CameraVisionFrameSource` or `WebcamVisionFrameSource` instead.

`WebcamVisionFrameSource` is not applicable on Meta Quest because Quest does not expose a standard `WebCamTexture` device.

For Meta Quest project setup, XR SDK configuration, and passthrough Vision integration, see the XR headsets platform guide.

{% content-ref url="../platform-guides/xr-headsets.md" %}
[XR headsets platform guide](../platform-guides/xr-headsets.md)
{% endcontent-ref %}
{% endtab %}
{% endtabs %}

## Next steps

With platform constraints confirmed, review the network requirements for real-time SDK operation.

{% content-ref url="network-and-api-requirements.md" %}
[Network and API requirements](network-and-api-requirements.md)
{% endcontent-ref %}
