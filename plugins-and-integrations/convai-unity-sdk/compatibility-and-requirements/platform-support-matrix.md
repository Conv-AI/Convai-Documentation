---
title: Platform support matrix
description: Reference for Convai Unity SDK platform support, including feature availability across Windows, macOS, Android, iOS, Meta Quest, and WebGL.
last_reviewed: "4.5.0"
---

SDK 4.5.0 contains integration paths for the targets below. This matrix is a source-level inventory, not proof that every feature passed on every device, browser, operating system, native architecture, or distributed package. Use it to choose the expected path, then run the linked platform validation before release.

## Feature × platform matrix

| Feature                    | Windows / macOS / Linux | Android                        | iOS                                    | Meta Quest            | WebGL                                  |
| -------------------------- | ----------------------- | ------------------------------ | -------------------------------------- | --------------------- | -------------------------------------- |
| Voice conversation         | Source path*             | Source path*                    | Source path*                            | Source path*           | Source path*                            |
| Microphone capture         | Source path*             | Runtime permission             | Usage description and OS permission     | Runtime permission    | HTTPS and user gesture                 |
| Remote audio playback      | Unity `AudioSource` path | Unity `AudioSource` path        | Unity `AudioSource` path                | Unity `AudioSource` path | Browser-routed path                  |
| Lip sync                   | Source path*             | Source path*                    | Source path*                            | Source path*           | Browser timing validation required     |
| Spatial audio              | `AudioSource` path       | `AudioSource` path              | `AudioSource` path                      | `AudioSource` path     | No Unity spatial-output path           |
| Actions                    | Shared runtime path      | Shared runtime path            | Shared runtime path                     | Shared runtime path    | Shared runtime path                    |
| Emotion                    | Shared runtime path      | Shared runtime path            | Shared runtime path                     | Shared runtime path    | Shared runtime path                    |
| Long-Term Memory           | REST/service path        | REST/service path              | REST/service path                       | REST/service path      | REST/service path                      |
| Narrative Design           | Shared runtime path      | Shared runtime path            | Shared runtime path                     | Shared runtime path    | Shared runtime path                    |
| Dynamic Context            | Shared runtime path      | Shared runtime path            | Shared runtime path                     | Shared runtime path    | Shared runtime path                    |
| Vision — Camera            | Camera frame source      | Camera frame source            | Camera frame source                     | Camera frame source    | Browser canvas capture                 |
| Vision — Webcam            | Webcam frame source      | Runtime camera permission      | `NSCameraUsageDescription`              | Not the Quest path     | Not exposed by the SDK                 |
| Vision — Quest passthrough | Not applicable           | Not applicable                 | Not applicable                          | Quest 3/3S source path | Not applicable                         |

`Source path*` means the SDK contains the relevant adapter or runtime surface. It still requires artifact and runtime validation on the target.

## Platform-specific requirements

{% tabs %}
{% tab title="WebGL" %}
WebGL uses dedicated browser transport paths with the following constraints:

* **Microphone capture** requires HTTPS or `localhost`. HTTP deployments cannot access the microphone. Call `ConvaiManager.EnableAudioAndStartListening()` from a user gesture (button click) — do not start audio automatically on scene load.
* **Remote audio playback** is routed through the browser's audio system, not Unity's `AudioSource`. Volume and spatialization controls on `AudioSource` components have no effect on WebGL.
* **Vision — Camera** uses browser canvas capture. `CameraVisionFrameSource` and other Unity `RenderTexture` sources are not used on WebGL.
* **Vision — Webcam** (`WebcamVisionFrameSource`) is not supported on WebGL — `AsyncGPUReadback` is unavailable in the browser runtime. Use `CameraVisionFrameSource` to stream the game canvas instead.
* **Spatial audio** is not supported on WebGL.

{% hint style="warning" %}
WebGL lip sync uses a browser-compatible realtime playback clock rather than the native hardware DSP clock. Validate timing across long utterances in every target browser and hosting environment.
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
* **Microphone:** The native audio path requests `Permission.Microphone` before recording when access is missing. Verify `RECORD_AUDIO` in the merged build manifest and handle both grant and denial cases in your app flow.
* **Vision — Webcam:** `android.permission.CAMERA` is requested at runtime by `WebcamVisionFrameSource`. Handle permission grant and denial in your app flow.

For Android build configuration, permission handling, and microphone setup, see the iOS and Android platform guide.

{% content-ref url="../platform-guides/ios-and-android.md" %}
[iOS and Android platform guide](../platform-guides/ios-and-android.md)
{% endcontent-ref %}
{% endtab %}

{% tab title="iOS" %}
* **Microphone:** `NSMicrophoneUsageDescription` must be set in **Player Settings → Other Settings → iOS → Microphone Usage Description**. Omitting this causes a crash on first microphone access.
* **Vision — Webcam:** `NSCameraUsageDescription` must be set in **Player Settings → Other Settings → iOS → Camera Usage Description** if you use `WebcamVisionFrameSource`. On iOS, `WebcamVisionFrameSource` accesses the device camera via Unity's `WebCamTexture` API.
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

Declare and verify `horizonos.permission.HEADSET_CAMERA` and `android.permission.CAMERA` in the merged application manifest.

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
