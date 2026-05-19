# platform support matrix

The Convai Unity SDK runs on all major Unity deployment targets. Feature availability varies by platform. Use this matrix to confirm support before building for a specific target.

***

## Feature × Platform Matrix

| Feature                    | Windows / macOS / Linux | Android               | iOS                                  | Meta Quest            | WebGL                                  |
| -------------------------- | ----------------------- | --------------------- | ------------------------------------ | --------------------- | -------------------------------------- |
| Voice conversation         | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ✅ Full                                 |
| Microphone capture         | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ✅ Full — HTTPS + user gesture required |
| Remote audio playback      | ✅ Unity `AudioSource`   | ✅ Unity `AudioSource` | ✅ Unity `AudioSource`                | ✅ Unity `AudioSource` | ⚠️ Browser-routed                      |
| Lip sync                   | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ⚠️ Known timing drift                  |
| Spatial audio              | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ❌ Not supported                        |
| Actions                    | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ✅ Full                                 |
| Emotion                    | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ✅ Full                                 |
| Long-Term Memory           | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ✅ Full                                 |
| Narrative Design           | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ✅ Full                                 |
| Dynamic Context            | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ✅ Full                                 |
| Vision — Camera            | ✅ Full                  | ✅ Full                | ✅ Full                               | ✅ Full                | ⚠️ Canvas capture                      |
| Vision — Webcam            | ✅ Full                  | ⚠️ Runtime permission | ⚠️ NSCameraUsageDescription required | ❌ Not applicable      | ❌ Not supported                        |
| Vision — Quest passthrough | ❌ Not supported         | ❌ Not supported       | ❌ Not supported                      | ✅ Full                | ❌ Not supported                        |

***

## Platform Notes

{% tabs %}
{% tab title="WebGL" %}
WebGL is fully supported with the following constraints imposed by browser security policies:

* **Microphone capture** requires HTTPS or `localhost`. HTTP deployments cannot access the microphone. Use `ConvaiManager.EnableAudioAndStartListening()` from a user gesture (button click) — do not start audio automatically on scene load.
* **Remote audio playback** is routed through the browser's audio system, not Unity's `AudioSource`. Volume and spatialization controls on `AudioSource` components have no effect on WebGL.
* **Vision — Camera** uses browser canvas capture (`CameraVisionFrameSource` is supported).
* **Vision — Webcam** (`WebcamVisionFrameSource`) is not supported on WebGL — `AsyncGPUReadback` is unavailable in the browser. Use `CameraVisionFrameSource` to stream the game canvas instead.
* **Spatial audio** is not supported on WebGL.

{% hint style="warning" %}
WebGL has a known audio/lip-sync timing drift defect — audio and lip-sync data arrive correctly, but playback timing can drift in browser builds. This is a tracked defect, not a missing feature. Validate in your target browser before shipping.
{% endhint %}

{% hint style="info" %}
Always validate WebGL builds in the actual hosting environment, especially if the build is embedded in an iframe.
{% endhint %}
{% endtab %}

{% tab title="Android" %}
* **Microphone**: the SDK requests `RECORD_AUDIO` permission at runtime via `ConvaiPermissionService`. Your app flow must handle the grant and denial cases. The permission must also be declared in your `AndroidManifest.xml`.
* **Webcam / Vision**: `android.permission.CAMERA` is requested at runtime by `WebcamVisionFrameSource`. Your app flow must handle the permission grant and denial cases.
{% endtab %}

{% tab title="iOS" %}
* **Microphone**: `NSMicrophoneUsageDescription` must be set in **Player Settings → Other Settings → iOS → Microphone Usage Description**. Omitting this causes a crash on first mic access.
* **Webcam / Vision**: `NSCameraUsageDescription` must be set in **Player Settings → Other Settings → iOS → Camera Usage Description** if you use `WebcamVisionFrameSource`. On iOS, `WebcamVisionFrameSource` accesses the device camera via Unity's `WebCamTexture` API.
* Define what happens when the user denies microphone or camera permission and when the app is interrupted or backgrounded during a conversation.
{% endtab %}

{% tab title="Meta Quest" %}
Quest passthrough vision (`QuestVisionFrameSource`) is supported on **Quest 3 and Quest 3S only**.

Requirements:

* Meta XR SDK imported into your project
* `PassthroughCameraAccess` component present in the scene
* Two Android permissions declared: `horizonos.permission.HEADSET_CAMERA` and `android.permission.CAMERA`

On other Quest hardware or non-Quest platforms, `QuestVisionFrameSource` produces no frames. Use `CameraVisionFrameSource` or `WebcamVisionFrameSource` instead.

`WebcamVisionFrameSource` is listed as not applicable on Meta Quest because Quest does not expose a standard `WebCamTexture` device — use `QuestVisionFrameSource` for passthrough camera access instead.

See [Meta Quest and XR](/broken/pages/abc36347fdb7da79536cf6e2cecd800cac208c84) for the full setup guide.
{% endtab %}
{% endtabs %}

***

## Next Steps

{% content-ref url="/broken/pages/e7c4053fcd48f371ba53dedc370bae1887369155" %}
[Broken link](/broken/pages/e7c4053fcd48f371ba53dedc370bae1887369155)
{% endcontent-ref %}

{% content-ref url="/broken/pages/fbaedc8762e52778e0d684b9927484e7ef96fb8e" %}
[Broken link](/broken/pages/fbaedc8762e52778e0d684b9927484e7ef96fb8e)
{% endcontent-ref %}
