---
title: Platform support matrix
description: Reference for Convai Unity SDK platform support, including feature availability across Windows, macOS, Android, iOS, Meta Quest, and WebGL.
last_reviewed: "4.2.0"
---

The Convai Unity SDK runs on all major Unity deployment targets. Feature availability varies by platform — use the matrix below to confirm support before building for a specific target.

## Feature × platform matrix

| Feature                    | Windows / macOS / Linux | Android                        | iOS                                    | Meta Quest            | WebGL                                  |
| -------------------------- | ----------------------- | ------------------------------ | -------------------------------------- | --------------------- | -------------------------------------- |
| Voice conversation         | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ✅ Full                                 |
| Microphone capture         | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ✅ Full — HTTPS + user gesture required |
| Remote audio playback      | ✅ Unity `AudioSource`   | ✅ Unity `AudioSource`          | ✅ Unity `AudioSource`                  | ✅ Unity `AudioSource` | ⚠️ Browser-routed                      |
| Lip sync                   | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ⚠️ Known timing drift                  |
| Spatial audio              | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ❌ Not supported                        |
| Actions                    | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ✅ Full                                 |
| Emotion                    | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ✅ Full                                 |
| Long-Term Memory           | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ✅ Full                                 |
| Narrative Design           | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ✅ Full                                 |
| Dynamic Context            | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ✅ Full                                 |
| Vision — Camera            | ✅ Full                  | ✅ Full                         | ✅ Full                                 | ✅ Full                | ⚠️ Canvas capture                      |
| Vision — Webcam            | ✅ Full                  | ⚠️ Runtime permission required | ⚠️ `NSCameraUsageDescription` required | ❌ Not applicable      | ❌ Not supported                        |
| Vision — Quest passthrough | ❌ Not supported         | ❌ Not supported                | ❌ Not supported                        | ✅ Full                | ❌ Not supported                        |

## Platform-specific requirements

{% tabs %}
{% tab title="WebGL" %}
WebGL is fully supported with the following constraints imposed by browser security policies:

* **Microphone capture** requires HTTPS or `localhost`. HTTP deployments cannot access the microphone. Call `ConvaiManager.EnableAudioAndStartListening()` from a user gesture (button click) — do not start audio automatically on scene load.
* **Remote audio playback** is routed through the browser's audio system, not Unity's `AudioSource`. Volume and spatialization controls on `AudioSource` components have no effect on WebGL.
* **Vision — Camera** uses browser canvas capture (`CameraVisionFrameSource` is supported).
* **Vision — Webcam** (`WebcamVisionFrameSource`) is not supported on WebGL — `AsyncGPUReadback` is unavailable in the browser runtime. Use `CameraVisionFrameSource` to stream the game canvas instead.
* **Spatial audio** is not supported on WebGL.

{% hint style="warning" %}
WebGL has a known audio/lip-sync timing drift defect — audio and lip-sync data arrive correctly, but playback timing can drift in browser builds. This is a tracked defect, not a missing feature. Validate in your target browser before shipping.
{% endhint %}

{% hint style="info" %}
Always validate WebGL builds in the actual hosting environment, especially if the build is embedded in an iframe. Add `allow="microphone"` to the iframe tag if you embed the build in a page you control.
{% endhint %}
{% endtab %}

{% tab title="Android" %}
* **Microphone:** The SDK requests `RECORD_AUDIO` permission at runtime via `ConvaiPermissionService`. Declare the permission in your `AndroidManifest.xml` and handle both grant and denial cases in your app flow.
* **Vision — Webcam:** `android.permission.CAMERA` is requested at runtime by `WebcamVisionFrameSource`. Handle permission grant and denial in your app flow.
{% endtab %}

{% tab title="iOS" %}
* **Microphone:** `NSMicrophoneUsageDescription` must be set in **Player Settings → Other Settings → iOS → Microphone Usage Description**. Omitting this causes a crash on first microphone access.
* **Vision — Webcam:** `NSCameraUsageDescription` must be set in **Player Settings → Other Settings → iOS → Camera Usage Description** if you use `WebcamVisionFrameSource`. On iOS, `WebcamVisionFrameSource` accesses the device camera via Unity's `WebCamTexture` API.
* Define your app's behavior when the user denies microphone or camera permission, and when the app is interrupted or backgrounded during a conversation.
{% endtab %}

{% tab title="Meta Quest" %}
Quest passthrough vision (`QuestVisionFrameSource`) is supported on **Quest 3 and Quest 3S only**.

**Requirements:**

* Meta XR SDK imported into your project
* `PassthroughCameraAccess` component present in the scene

The required passthrough camera permissions are declared automatically when Meta XR SDK is imported.

On other Quest hardware or non-Quest platforms, `QuestVisionFrameSource` produces no frames. Use `CameraVisionFrameSource` or `WebcamVisionFrameSource` instead.

`WebcamVisionFrameSource` is not applicable on Meta Quest because Quest does not expose a standard `WebCamTexture` device.
{% endtab %}
{% endtabs %}

## Next steps

With platform constraints confirmed, review the network requirements for real-time SDK operation.

{% content-ref url="network-and-api-requirements.md" %}
[Network and API requirements](network-and-api-requirements.md)
{% endcontent-ref %}
