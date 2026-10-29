---
title: Windows, macOS, and Linux
description: >-
  Prepare Windows, macOS, and Linux builds with the right native transport
  libraries, microphone permissions, voice output, and camera configuration.
last_reviewed: "5.0.0-preview"
---

Desktop players use native transport libraries and Unity audio output. Install the library for the target architecture, configure microphone access and verify the built application. macOS also needs a microphone usage description before requesting access.

## Feature support

| Feature                      | Windows | macOS  | Linux  |
| ---------------------------- | ------- | ------ | ------ |
| Voice conversation           | ✅ Implemented  | ✅ Implemented | ✅ Implemented |
| Lip sync                     | ✅ Implemented  | ✅ Implemented | ✅ Implemented |
| Actions                      | ✅ Implemented  | ✅ Implemented | ✅ Implemented |
| Emotion                      | ✅ Implemented  | ✅ Implemented | ✅ Implemented |
| Long-Term Memory             | ✅ Implemented  | ✅ Implemented | ✅ Implemented |
| Narrative Design             | ✅ Implemented  | ✅ Implemented | ✅ Implemented |
| Vision                       | ✅ Implemented  | ✅ Implemented | ✅ Implemented |
| Spatial audio                | ✅ Implemented  | ✅ Implemented | ✅ Implemented |
| Unity `AudioSource` playback | ✅ Implemented  | ✅ Implemented | ✅ Implemented |
| Microphone device selection  | ✅ Implemented  | ✅ Implemented | ✅ Implemented |


## Platform and architecture support

The Editor downloads prebuilt native libraries for these target architectures; they are not bundled in the package:

| Platform | Supported architectures                           |
| -------- | ------------------------------------------------- |
| Windows  | x86\_64, arm64                                    |
| macOS    | arm64 (Apple Silicon), x86\_64 (Intel), Universal |
| Linux    | x86\_64                                           |

{% hint style="warning" %}
**Linux arm64 is not supported.** If your deployment target includes Linux arm64 machines, the native transport library will fail to load and voice conversation will not work. Only x86\_64 is available on Linux.
{% endhint %}

The downloader installs libraries for the Editor and active build target under `Assets/Convai/Plugins/client-sdk-unity-livekit/Runtime/Plugins`. Windows defaults to x86_64; use **Convai > Platform Support > Download FFI Libraries (All Platforms)** when another listed architecture is needed. See [Native transport libraries](native-transport-libraries.md).

The 5.0 macOS build processor combines arm64 and x86_64 slices for Universal players. Confirm the built app contains the resulting native plugin and test both target architectures; Editor playback does not prove the Universal build.

## Microphone and audio

Operating-system privacy settings and device availability still apply:

* **Windows:** Check microphone privacy settings for desktop applications and select an available input device.
* **macOS:** Set **Microphone Usage Description** and use **Convai > Settings > Setup Health** to verify it. The 5.0 SDK requests microphone authorization before opening capture; handle denial by directing the player to system settings.
* **Linux:** Verify that the target machine's audio stack exposes a working microphone and playback device to Unity.

<figure><img src="../../../.gitbook/assets/unity-setup-health.png" alt="Setup Health showing the macOS and iOS microphone usage-description check"><figcaption><p>The Apple usage-description check applies before building the application.</p></figcaption></figure>

Use `ConvaiAudioOutput` for per-character volume and spatial audio. The 5.0 native playback path uses a carrier clip so Unity can apply direction and distance. Reserve that AudioSource for the voice; place other sounds on another source. Test microphone capture with and without echo cancellation on the actual device.

## Vision on desktop

Configure `CameraVisionFrameSource` with the scene camera and assign it to `ConvaiVisionPublisher`, or place it on the publisher's GameObject or a child for discovery. Configure the room for Vision and verify the preview and publishing status. Use `WebcamVisionFrameSource` for a physical camera; a Unity scene camera does not see the room around the computer.

{% hint style="info" %}
Camera capture applies a vertical pixel flip internally to ensure correct frame orientation. This is handled automatically on all desktop platforms — no configuration is required.
{% endhint %}

## Verify a desktop build

* [ ] The native library matches the built player's architecture.
* [ ] A fresh installation can request microphone access and handles denial.
* [ ] A voice or text turn receives a response after the character becomes ready.
* [ ] Moving the listener changes native spatial playback as expected.
* [ ] The configured Vision source shows the intended image and orientation.
* [ ] Suspend/resume and reconnect recover in the built application.

These checks should run on each desktop platform you distribute, including both architectures for a Universal macOS build.

## Next steps

A scene validation pass checks local setup. Native library loading, permissions and actual media behavior need a built-player check before distribution. If you are also targeting WebGL, iOS, Android, or XR headsets, review the relevant platform guide before building.

{% content-ref url="webgl.md" %}
[WebGL](webgl.md)
{% endcontent-ref %}

{% content-ref url="ios-and-android.md" %}
[iOS and Android](ios-and-android.md)
{% endcontent-ref %}

{% content-ref url="xr-headsets.md" %}
[XR headsets](xr-headsets.md)
{% endcontent-ref %}
