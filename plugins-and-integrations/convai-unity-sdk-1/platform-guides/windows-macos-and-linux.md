---
title: Windows, macOS, and Linux
description: >-
  Windows, macOS, and Linux builds require no extra SDK configuration — all
  features including Vision, spatial audio, and screen share work after standard
  setup.
last_reviewed: "4.2.0"
---

Desktop builds have no platform-specific configuration requirements. All SDK features work without additional setup — no permission declarations, no manifest changes, no gesture handling. Microphone access, audio playback, spatial audio, Vision, and screen share all function immediately after the standard SDK setup.

## Feature support

| Feature                      | Windows | macOS  | Linux  |
| ---------------------------- | ------- | ------ | ------ |
| Voice conversation           | ✅ Full  | ✅ Full | ✅ Full |
| Lip sync                     | ✅ Full  | ✅ Full | ✅ Full |
| Actions                      | ✅ Full  | ✅ Full | ✅ Full |
| Emotion                      | ✅ Full  | ✅ Full | ✅ Full |
| Long-Term Memory             | ✅ Full  | ✅ Full | ✅ Full |
| Narrative Design             | ✅ Full  | ✅ Full | ✅ Full |
| Vision                       | ✅ Full  | ✅ Full | ✅ Full |
| Spatial audio                | ✅ Full  | ✅ Full | ✅ Full |
| Unity `AudioSource` playback | ✅ Full  | ✅ Full | ✅ Full |
| Microphone device selection  | ✅ Full  | ✅ Full | ✅ Full |
| Screen share                 | ✅ Full  | ✅ Full | ✅ Full |

Screen share is a desktop-exclusive capability — it is not available on WebGL, iOS, Android, or Android-based XR headsets.

## Platform and architecture support

The SDK ships pre-built native libraries for the following desktop configurations:

| Platform | Supported architectures                           |
| -------- | ------------------------------------------------- |
| Windows  | x86\_64, arm64                                    |
| macOS    | arm64 (Apple Silicon), x86\_64 (Intel), Universal |
| Linux    | x86\_64                                           |

{% hint style="warning" %}
**Linux arm64 is not supported.** If your deployment target includes Linux arm64 machines, the native transport library will fail to load and voice conversation will not work. Only x86\_64 is available on Linux.
{% endhint %}

## Microphone and audio

No permission declarations are required on desktop platforms. The operating system grants microphone access at the application level:

* **Windows:** Access is managed through Windows Privacy Settings. Unity builds are recognized as desktop applications and receive microphone access without any manifest changes.
* **macOS:** The OS presents a one-time system permission dialog when the application first accesses the microphone. Unity adds `NSMicrophoneUsageDescription` to the app's `Info.plist` automatically for macOS builds. No manual configuration is needed.
* **Linux:** Microphone access is handled by the system audio stack (PulseAudio, PipeWire, ALSA). No application-level permission handling is required.

## Vision on desktop

`CameraVisionFrameSource` works on all desktop platforms without additional configuration — add the component to a `Camera` GameObject, assign a `ConvaiVisionPublisher`, and Vision is active.

{% hint style="info" %}
Camera capture applies a vertical pixel flip internally to ensure correct frame orientation. This is handled automatically on all desktop platforms — no configuration is required.
{% endhint %}

## Usage examples

### Military mission rehearsal on Windows

A defense contractor runs mission rehearsal software on Windows workstations. Convai characters play opposing forces, local commanders, and civilian actors in a branching scenario. Trainees speak with characters using standard desktop microphones.

**Setup:** Standard SDK configuration — no platform-specific steps. Spatial audio places character voices in 3D space relative to the player's position.

**Outcome:** Trainees interact verbally with multiple characters across a mission simulation. The session records responses and branching decisions for after-action review.

### Medical consultation training on macOS

A medical school deploys a patient consultation trainer on faculty MacBook Pros. Residents practice taking patient histories with a Convai character that responds with realistic symptoms and adapts based on the resident's questions.

**Setup:** Standard SDK configuration. The character uses Vision via `CameraVisionFrameSource` pointed at a physical model the resident is examining. macOS prompts for microphone access on first launch — no additional setup is needed.

**Outcome:** The resident speaks with the character naturally. The macOS microphone permission dialog appears on first launch only. Vision enables the character to acknowledge and respond to what the resident is holding in-scene.

### Compliance training kiosk on Linux

A manufacturing company runs safety compliance training on Linux workstations in a secure facility. The same Unity build used on Windows deploys to Ubuntu x86\_64 machines with no modification.

**Setup:** Standard SDK configuration. Ensure the deployment machines run x86\_64 Linux — arm64 is not supported. No audio configuration changes are required; PulseAudio or PipeWire handles microphone access automatically.

**Outcome:** Operators complete verbal compliance assessments with Convai characters at the kiosk. The experience is identical to the Windows deployment.

## Next steps

Desktop builds need no platform-specific work. Once your scene is validated, your build is ready to ship. If you are also targeting WebGL, iOS, Android, or XR headsets, review the relevant platform guide before building.

{% content-ref url="webgl.md" %}
[WebGL](webgl.md)
{% endcontent-ref %}

{% content-ref url="ios-and-android.md" %}
[iOS and Android](ios-and-android.md)
{% endcontent-ref %}

{% content-ref url="xr-headsets.md" %}
[XR headsets](xr-headsets.md)
{% endcontent-ref %}
