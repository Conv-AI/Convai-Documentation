---
title: Meta Quest Vision setup
description: >-
  Explains how to stream the Meta Quest passthrough camera to a Convai
  character so it can see the player's real surroundings.
last_reviewed: "5.0.0-preview"
---

`QuestVisionFrameSource` streams the passthrough camera feed from a Meta Quest headset to Convai, enabling the AI character to see and respond to the real world the learner is looking at. This page covers the required Android manifest permissions, step-by-step component setup, Inspector field reference, and troubleshooting for Quest 3 and Quest 3S.

**Supported hardware:** Meta Quest 3 and Quest 3S running Horizon OS with the Passthrough Camera API available.

The component uses reflection to bind to the Meta XR SDK's `PassthroughCameraAccess` at runtime. The Convai SDK has no hard compile-time dependency on any Meta SDK package ; verify the reflected members remain compatible when updating the Meta SDK.

## Required permissions

{% hint style="danger" %}
Declare and grant both camera permissions before capture. A missing or unreadable `PassthroughCameraAccess` fails immediately with `InvalidConfiguration`. A bound component that never starts playing is retried three times at one-second intervals, then reports `DeviceUnavailable`.
{% endhint %}

{% code title="AndroidManifest.xml" %}
```xml
<uses-permission android:name="horizonos.permission.HEADSET_CAMERA" />
<uses-permission android:name="android.permission.CAMERA" />
```
{% endcode %}

Add both entries to `Assets/Plugins/Android/AndroidManifest.xml`. If this file does not exist, create it — Unity merges it with the generated manifest at build time. After building, verify that both permissions appear in the exported manifest inside the APK.

## Set up QuestVisionFrameSource

{% stepper %}
{% step %}
### Import the Meta XR SDK

Install the Meta XR SDK package from the Meta XR Developer Hub or the Unity Asset Store. Add a `PassthroughCameraAccess` component to a GameObject in your scene — this component is provided by the Meta SDK and handles the low-level passthrough camera API.
{% endstep %}

{% step %}
### Add QuestVisionFrameSource

Add the `QuestVisionFrameSource` component to a GameObject in your scene. This can be the same GameObject as `PassthroughCameraAccess` or a separate one.
{% endstep %}

{% step %}
### Assign the PassthroughCameraAccess reference

Drag the `PassthroughCameraAccess` component into the **Passthrough Camera Access** field on `QuestVisionFrameSource`. If left empty, the component searches the active scene automatically when `StartCapture()` is called. Assign explicitly when multiple `PassthroughCameraAccess` instances are present in the scene.
{% endstep %}

{% step %}
### Add a vision publisher

Add `ConvaiVisionPublisher` to the same GameObject. It auto-discovers `QuestVisionFrameSource` on its own GameObject or children, or you can assign the frame source reference in the publisher's Inspector field.
{% endstep %}

{% step %}
### Declare manifest permissions

Add both `horizonos.permission.HEADSET_CAMERA` and `android.permission.CAMERA` to your `AndroidManifest.xml` at `Assets/Plugins/Android/AndroidManifest.xml`. See the Required permissions section above.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Build and deploy to your Quest device. After capture starts, inspect the source's **Live > State** or a `VisionDebugPreview` overlay. Confirm Ready, advancing frames and the intended orientation. Then confirm publishing and a relevant character response; the runtime Settings Panel has no Vision status.
{% endhint %}

In the Unity Editor, `QuestVisionFrameSource` produces no frames. If `StartCapture()` is called, the source transitions to the `Failed` state with `InvalidConfiguration` — `PassthroughCameraAccess` is only available on Horizon OS. Test Vision on a physical Quest 3 or 3S device.

## Inspector reference

| Field                         | Default             | Description                                                                                                                                                                 |
| ----------------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Passthrough Camera Access** | None                | Optional reference to the `PassthroughCameraAccess` component. Auto-discovered from the active scene if left empty. If no readable component exists when capture starts, it fails immediately. Create or bind the component before starting capture; retries apply only after it has bound a component that is not yet playing. |
| **Source Id**                 | `quest-passthrough` | Identifier used by `ConvaiVisionPublisher` to select this frame source.                                                                                                     |
| **Max Output Width**          | 1280                | Maximum pixel width of frames sent to Convai. Reduce to lower bandwidth usage.                                                                                              |
| **Max Output Height**         | 720                 | Maximum pixel height of frames sent to Convai.                                                                                                                              |
| **Target Frame Rate**         | 15                  | Frames per second cap for the passthrough capture loop. Lower values reduce bandwidth and processing load.                                                                  |
| **Flip Y**                    | true                | Flips the passthrough texture vertically so the published frame is top-down. Disable only if your Meta SDK version handles orientation before handing the texture to Unity. |

## Usage examples

### Surgical resident training with passthrough scene awareness

A surgical resident training application on Quest 3 places learners in a simulated operating environment. The Convai character plays a surgical team member who can see and comment on physical props the resident holds up — anatomical models, instruments, and procedure reference cards.

**Setup:** `QuestVisionFrameSource` on a scene GameObject with **Passthrough Camera Access** auto-discovered. `ConvaiVisionPublisher` on the same object. Both permissions declared in the manifest. The character's Convai configuration includes a vision-aware system prompt instructing it to acknowledge and respond to what it sees in the passthrough feed.

**Verification:** Use non-sensitive props and confirm the preview shows them clearly. Test whether the authored character uses the visual context as intended; a working video stream does not establish recognition accuracy or suitability for clinical decisions.

### Industrial safety inspection with environmental object recognition

A factory safety training application on Quest 3S guides equipment operators through machinery inspection. The AI character identifies physical components visible in the passthrough feed and adapts its safety guidance based on what the operator is looking at.

**Setup:** Same configuration as the medical training example. **Target Frame Rate** is set to 10 (reduced from 15) to accommodate an industrial network environment with limited bandwidth. **Max Output Width** is set to 960 to reduce per-frame payload size and then evaluated for the visual details the training task requires.

**Outcome:** Verify the character's responses against the authored training scenario; frame delivery alone does not establish reliable identification or safety advice. The SDK streams passthrough frames to Convai, which handles scene understanding and generates contextually appropriate guidance.

## Troubleshooting

| Symptom                                                                           | Likely cause                                                                                                                                                               | Fix                                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source transitions to `Failed / DeviceUnavailable` a few seconds after scene load | A bound `PassthroughCameraAccess` did not start playing, possibly because camera permissions are not granted | (1) Add `PassthroughCameraAccess` to the scene or assign it explicitly in the **Passthrough Camera Access** Inspector field. (2) Verify both permissions are declared in `AndroidManifest.xml` and appear in the exported APK manifest. |
| Immediate `Failed / InvalidConfiguration` | No readable passthrough component was bound. | Add or assign a compatible `PassthroughCameraAccess` before starting capture. |
| `QuestVisionFrameSource` produces no output in the Editor                         | Expected — `PassthroughCameraAccess` only runs on Horizon OS                                                                                                               | Test on a physical Quest 3 or 3S device.                                                                                                                                                                                                |
| Character does not respond to visual context                                      | Vision publisher not connected, or Vision not enabled in character config                                                                                                  | Verify `ConvaiVisionPublisher` is in the scene and Vision is enabled in the character's Convai dashboard configuration.                                                                                                                 |
| Passthrough feed correct but image appears upside down                            | **Flip Y** was disabled                                                                                                                                                    | Re-enable **Flip Y** in the `QuestVisionFrameSource` Inspector.                                                                                                                                                                         |

## Next steps

With `QuestVisionFrameSource` configured and manifest permissions declared, your Quest build is ready for on-device testing. Review the Vision feature documentation to configure publishing policies, set frame rate and resolution for your bandwidth target, and enable the debug preview overlay during development.

{% content-ref url="../features/vision/README.md" %}
[Vision](../features/vision/README.md)
{% endcontent-ref %}

{% content-ref url="ios-and-android.md" %}
[iOS and Android](ios-and-android.md)
{% endcontent-ref %}
