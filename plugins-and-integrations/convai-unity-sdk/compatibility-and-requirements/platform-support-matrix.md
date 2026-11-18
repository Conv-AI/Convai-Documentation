---
title: Platform support matrix
description: Reference for Convai Unity SDK platform support, including feature availability across Windows, macOS, Android, iOS, Meta Quest, and WebGL.
last_reviewed: "5.0.0-pre.1"
---

This matrix describes the platform paths implemented in the SDK. Device permissions, browser settings, and service configuration affect feature availability. Verify the built application on each platform you distribute.

## Feature × platform matrix

| Feature                    | Windows / macOS / Linux | Android                        | iOS                                    | Meta Quest            | WebGL                                  |
| -------------------------- | ----------------------- | ------------------------------ | -------------------------------------- | --------------------- | -------------------------------------- |
| Voice conversation         | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Microphone capture         | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available — HTTPS + microphone permission required |
| Remote audio playback      | ✅ Unity `AudioSource`   | ✅ Unity `AudioSource`          | ✅ Unity `AudioSource`                  | ✅ Unity `AudioSource` | ⚠️ Browser-routed                      |
| Lip sync                   | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Browser media timing                  |
| Spatial audio              | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ❌ Not supported                        |
| Actions                    | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Emotion                    | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Long-Term Memory           | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Narrative Design           | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Dynamic Context            | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Available                                 |
| Vision — Camera            | ✅ Available                  | ✅ Available                         | ✅ Available                                 | ✅ Available                | ✅ Frame Source by default                      |
| Vision — Webcam            | ✅ Available                  | ⚠️ Runtime permission required | ⚠️ `NSCameraUsageDescription` required | ⚠️ Device-dependent | ⚠️ Browser camera permission and texture capture required |
| Vision — Quest passthrough | ❌ Not supported         | ❌ Not supported                | ❌ Not supported                        | ✅ Available                | ❌ Not supported                        |
| Text-only ordinary rooms | ✅ Available | ✅ Available | ✅ Available | ✅ Available | ✅ Available |
| On-device Sentis/Silero voice detection | ✅ Native path | ✅ Native path | ✅ Native path | ✅ Native path | ❌ Excluded from build |
| Push-to-talk finalization | Correlated release, native drain when available | Correlated release, native drain when available | Correlated release, native drain when available | Correlated release, native drain when available | Correlated release with a timed capture tail |
| Group conversation | Push-to-talk required | Push-to-talk required | Push-to-talk required | Push-to-talk required | Same input requirement. Validate in the hosted build. |

The Scene Auto Tagger window and `ConvaiSceneTagger` are Editor authoring tools for Windows x64 and macOS, with separate native Core distribution gates. They are not player-platform features. See [Scene Auto Tagger](../features/scene-metadata/scene-auto-tagger.md).

Use `ConvaiSceneTagger.TagAsync` or `DescribeViewAsync` for Unity Editor authoring in code. Player builds use the [Vision frame publishing workflow](../features/vision/README.md) for live visual input.

## Platform-specific requirements

{% tabs %}
{% tab title="WebGL" %}
WebGL uses browser media and permission APIs:

* **Microphone capture** requires HTTPS or `localhost`. HTTP deployments cannot access the microphone. When playback is blocked, the default manager retries audio unlock on eligible non-UI clicks after connection. A UI button can call `ConvaiManager.Audio.EnableAudioAndStartListening()` explicitly.
* **Remote audio playback** is routed through the browser's audio system, not Unity's `AudioSource`. Use `ConvaiAudioOutput.Volume` and `IsMuted` for browser playback control. Unity distance rolloff and listener volume do not apply; iOS Safari controls its own nonzero media volume.
* **Vision — Camera** publishes the configured frame source by default. **WebGL Publishes > Game View** explicitly captures the visible Unity canvas, including its UI. A custom `IVisionPageCanvasSource` can provide a page canvas.
* **Vision — Webcam** (`WebcamVisionFrameSource`) can publish a physical camera through **WebGL Publishes > Frame Source**. Request browser camera permission before starting the source. Texture publishing uses the WebGL 2 graphics path or requires support for asynchronous GPU readback on other graphics backends.
* **Spatial audio** is not supported on WebGL.

{% hint style="warning" %}
WebGL uses the browser media clock for lip sync. When the browser audio analyser detects silence, the SDK waits up to two seconds for audible speech before starting from a fallback time. Verify timing in the target browser and hosting environment.
{% endhint %}

{% hint style="info" %}
Always validate WebGL builds in the actual hosting environment, especially if the build is embedded in an iframe. For cross-origin embeds, delegate microphone access to the iframe and check the parent page’s Permissions Policy.
{% endhint %}

For detailed WebGL setup, browser compatibility, and deployment steps, see the WebGL platform guide.

{% content-ref url="../platform-guides/webgl.md" %}
[WebGL deployment guide](../platform-guides/webgl.md)
{% endcontent-ref %}
{% endtab %}

{% tab title="Android" %}
* **Microphone:** The SDK requests `RECORD_AUDIO` at runtime before opening microphone capture. Unity normally adds that manifest permission when microphone APIs are used. Verify a custom manifest does not remove it, and handle denial in your app flow.
* **Vision — Webcam:** `android.permission.CAMERA` is requested at runtime by `WebcamVisionFrameSource`. Handle permission grant and denial in your app flow.

For Android build configuration, permission handling, and microphone setup, see the iOS and Android platform guide.

{% content-ref url="../platform-guides/ios-and-android.md" %}
[iOS and Android platform guide](../platform-guides/ios-and-android.md)
{% endcontent-ref %}
{% endtab %}

{% tab title="iOS" %}
* **Microphone:** The SDK requests access before opening capture. `NSMicrophoneUsageDescription` must be set in **Player Settings → Other Settings → iOS → Microphone Usage Description**. Check this string in the built app before requesting access.
* **Vision — Webcam:** `NSCameraUsageDescription` must be set in **Player Settings → Other Settings → iOS → Camera Usage Description** if you use `WebcamVisionFrameSource`. On iOS, `WebcamVisionFrameSource` accesses the device camera via Unity's `WebCamTexture` API.
* Enable **Prepare iOS for Recording** and use **Convai > Home > Welcome > Setup Health** to check the microphone description.
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
* The `horizonos.permission.HEADSET_CAMERA` permission declared and granted for Meta's `PassthroughCameraAccess` component

Your project or Meta integration must handle permissions before starting `QuestVisionFrameSource`. See [Meta’s Unity camera setup](https://developers.meta.com/vr/documentation/unity/unity-pca-documentation/).

On other Quest hardware or non-Quest platforms, use `CameraVisionFrameSource` for Unity scene cameras or `WebcamVisionFrameSource` where Unity exposes a physical camera. Use `QuestVisionFrameSource` with Meta's `PassthroughCameraAccess` for supported headset cameras.

For Meta Quest project setup, XR SDK configuration, and passthrough Vision integration, see the XR headsets platform guide.

{% content-ref url="../platform-guides/xr-headsets.md" %}
[XR headsets platform guide](../platform-guides/xr-headsets.md)
{% endcontent-ref %}
{% endtab %}
{% endtabs %}

## IL2CPP stripping and validation

The SDK preserves platform transport types reached by reflection, reflected JSON models, and the LiveKit browser bridge in `SDK/link.xml`. Startup assemblies for native and WebGL transport, client voice activity, Conversation Flow, Gaze, and LipSync also use `AlwaysLinkAssembly` so Unity processes their startup registration in a player.

If your project passes its own types through reflection or JSON, preserve the members your code uses. Applying `[Preserve]` to a type keeps its default constructor. List reflective members in your own `link.xml` when they also need to survive stripping. For Quest projects that use Convai's reflection path, this includes `PassthroughCameraAccess.GetTexture()` and the `IsPlaying` getter if no other code keeps them.

Build the actual target with your production scripting backend and stripping level. Check its transport startup and run a conversation in the player. If a stripped build fails while the Editor works, look under `Library/Bee/artifacts/<target>/ManagedStripped` for the target’s managed assemblies. Check for `NativeTransportProvider` or `WebGLTransportProvider` and its compiled `get_Instance` method, then inspect the component or data type involved in the failing path.

## Next steps

With platform constraints confirmed, review the network requirements for real-time SDK operation.

{% content-ref url="network-and-api-requirements.md" %}
[Network and API requirements](network-and-api-requirements.md)
{% endcontent-ref %}
