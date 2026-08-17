---
title: Windows, macOS, and Linux
description: >-
  Review native transport, microphone, audio, Vision, and architecture checks
  for Convai Unity SDK builds on Windows, macOS, and Linux.
last_reviewed: "4.5.0"
---

SDK 4.5.0 contains native desktop transport, microphone, audio-output, and camera-Vision paths. That source inventory does not prove every feature on every desktop target or native architecture. Check operating-system privacy settings and native-library packaging, then run the distributed artifact on each desktop target you ship.

## Source-level feature inventory

| Surface | SDK 4.5.0 path | Release check |
| --- | --- | --- |
| Voice conversation and microphone | Native room transport and platform audio adapters | Connect, grant or deny microphone access, speak, reconnect, and change devices on each OS |
| Character playback and spatialization | Unity `AudioSource` output | Verify routing, mixers, attenuation, and the packaged native audio library |
| Lip sync, actions, emotion, LTM, and Narrative Design | Platform-independent runtime modules call the shared room and service layers | Run the feature's own integration scenario; source presence is not backend proof |
| Camera Vision | `CameraVisionFrameSource` and native video publishing | Verify rendered frames, orientation, publication, and backend response on the built player |
| Screen-share transport | Lower-level transport types contain a screen-share track source | Do not treat this as a documented public Unity workflow without a release-specific integration and runtime test |

## Platform and architecture support

The 4.5.0 package source contains import metadata for the following desktop configurations. Verify that the distributed Asset Store or UPM artifact actually includes and loads the matching native libraries:

| Platform | Supported architectures                           |
| -------- | ------------------------------------------------- |
| Windows  | x86\_64, arm64                                    |
| macOS    | arm64 (Apple Silicon), x86\_64 (Intel), Universal |
| Linux    | x86\_64                                           |

{% hint style="warning" %}
**Linux arm64 is not supported.** If your deployment target includes Linux arm64 machines, the native transport library will fail to load and voice conversation will not work. Only x86\_64 is available on Linux.
{% endhint %}

## Microphone and audio

Desktop microphone access is controlled by the operating system and the way the player is packaged:

* **Windows:** Check Windows microphone privacy settings for desktop applications and validate the packaged executable.
* **macOS:** Confirm the built app contains the required microphone usage description and signing entitlements for your distribution path, then test the one-time system prompt.
* **Linux:** Confirm the target machine's PulseAudio, PipeWire, or ALSA path exposes a usable input and that the packaged native library loads.

## Vision on desktop

`CameraVisionFrameSource` is the desktop scene-camera integration. Add it with `ConvaiVisionPublisher`, connect in Video mode, and verify both a healthy captured texture and a published track in the built player.

{% hint style="info" %}
Camera capture applies a vertical pixel flip internally to ensure correct frame orientation. This is handled automatically on all desktop platforms — no configuration is required.
{% endhint %}

## Usage examples

### Military mission rehearsal on Windows

A defense contractor runs mission rehearsal software on Windows workstations. Convai characters play opposing forces, local commanders, and civilian actors in a branching scenario. Trainees speak with characters using standard desktop microphones.

**Setup:** Standard SDK configuration — no platform-specific steps. Spatial audio places character voices in 3D space relative to the player's position.

**Validation target:** Confirm microphone capture, multi-character routing if used, spatialized output, and application-owned recording on the packaged Windows build.

### Medical consultation training on macOS

A medical school deploys a patient consultation trainer on faculty MacBook Pros. Residents practice taking patient histories with a Convai character that responds with realistic symptoms and adapts based on the resident's questions.

**Setup:** Standard SDK configuration. The character uses Vision via `CameraVisionFrameSource` pointed at a physical model the resident is examining. Configure the microphone usage description in Player Settings, then handle the macOS permission prompt and denial path in the application.

**Validation target:** Confirm the macOS permission prompt, native audio path, published Vision frames, and the deployed character's response to controlled visual prompts.

### Compliance training kiosk on Linux

A manufacturing company runs safety compliance training on Linux workstations in a secure facility. The same Unity build used on Windows deploys to Ubuntu x86\_64 machines with no modification.

**Setup:** Standard SDK configuration. Ensure the deployment machines run x86\_64 Linux — arm64 is not supported. Confirm that the target distribution's PulseAudio or PipeWire setup exposes the intended input and output devices to the packaged build.

**Validation target:** Confirm the native library loads on the target Linux distribution, the selected audio stack exposes the microphone, and behavior matches the separately tested Windows build where required.

## Next steps

A desktop build is ready for release review only after the packaged native libraries, microphone permission flow, room connection, audio playback, and any enabled feature scenarios pass on each target OS. If you also target WebGL, mobile, or XR, review the relevant platform guide before building.

{% content-ref url="webgl.md" %}
[WebGL](webgl.md)
{% endcontent-ref %}

{% content-ref url="ios-and-android.md" %}
[iOS and Android](ios-and-android.md)
{% endcontent-ref %}

{% content-ref url="xr-headsets.md" %}
[XR headsets](xr-headsets.md)
{% endcontent-ref %}
