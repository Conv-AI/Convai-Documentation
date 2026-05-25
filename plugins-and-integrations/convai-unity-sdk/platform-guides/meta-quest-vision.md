---
title: Meta Quest Vision setup
description: >-
  Configure QuestVisionFrameSource to stream the Meta Quest passthrough camera
  to a Convai character on Quest 3 and 3S builds.
last_reviewed: "4.2.0"
---

`QuestVisionFrameSource` streams the passthrough camera feed from a Meta Quest headset to Convai, enabling the AI character to see and respond to the real world the learner is looking at. This page covers the required Android manifest permissions, step-by-step component setup, Inspector field reference, and troubleshooting for Quest 3 and Quest 3S.

**Supported hardware:** Meta Quest 3 and Quest 3S running Horizon OS with the Passthrough Camera API available.

The component uses reflection to bind to the Meta XR SDK's `PassthroughCameraAccess` at runtime. The Convai SDK has no hard compile-time dependency on any Meta SDK package — you can update or swap the Meta XR SDK version without changes to the Convai SDK.

## Required permissions

{% hint style="danger" %}
Both permissions must be declared in your `AndroidManifest.xml`. The passthrough camera will not start without them, and `QuestVisionFrameSource` will enter the `Failed` state after three retry attempts.
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

Add `ConvaiVisionPublisher` to the same GameObject. It auto-discovers `QuestVisionFrameSource` in the scene, or you can assign the frame source reference in the publisher's Inspector field.
{% endstep %}

{% step %}
### Declare manifest permissions

Add both `horizonos.permission.HEADSET_CAMERA` and `android.permission.CAMERA` to your `AndroidManifest.xml` at `Assets/Plugins/Android/AndroidManifest.xml`. See the Required permissions section above.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Build and deploy to your Quest device. After the scene loads, the Vision status in the Convai Settings Panel should show **Ready**. The character will begin receiving passthrough frames and can respond to what it sees.
{% endhint %}

In the Unity Editor, `QuestVisionFrameSource` produces no frames. If `StartCapture()` is called, the source transitions to the `Failed` state with `InvalidConfiguration` — `PassthroughCameraAccess` is only available on Horizon OS. Test Vision on a physical Quest 3 or 3S device.

## Inspector reference

| Field                         | Default             | Description                                                                                                                                                                 |
| ----------------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Passthrough Camera Access** | None                | Optional reference to the `PassthroughCameraAccess` component. Auto-discovered from the active scene if left empty. The component retries up to three times with one-second intervals before entering the `Failed` state — assign explicitly when `PassthroughCameraAccess` initializes asynchronously or after a delay. |
| **Source Id**                 | `quest-passthrough` | Identifier used by `ConvaiVisionPublisher` to select this frame source.                                                                                                     |
| **Max Output Width**          | 1280                | Maximum pixel width of frames sent to Convai. Reduce to lower bandwidth usage.                                                                                              |
| **Max Output Height**         | 720                 | Maximum pixel height of frames sent to Convai.                                                                                                                              |
| **Target Frame Rate**         | 15                  | Frames per second cap for the passthrough capture loop. Lower values reduce bandwidth and processing load.                                                                  |
| **Flip Y**                    | true                | Flips the passthrough texture vertically so the published frame is top-down. Disable only if your Meta SDK version handles orientation before handing the texture to Unity. |

## Usage examples

### Surgical resident training with passthrough scene awareness

A surgical resident training application on Quest 3 places learners in a simulated operating environment. The Convai character plays a surgical team member who can see and comment on physical props the resident holds up — anatomical models, instruments, and procedure reference cards.

**Setup:** `QuestVisionFrameSource` on a scene GameObject with **Passthrough Camera Access** auto-discovered. `ConvaiVisionPublisher` on the same object. Both permissions declared in the manifest. The character's Convai configuration includes a vision-aware system prompt instructing it to acknowledge and respond to what it sees in the passthrough feed.

**Outcome:** The character responds to visual context alongside conversation — "I can see you are preparing the scalpel — let's review the incision depth for this procedure." The resident practices both verbal interaction and physical task execution without any object detection code in the Unity project.

### Industrial safety inspection with environmental object recognition

A factory safety training application on Quest 3S guides equipment operators through machinery inspection. The AI character identifies physical components visible in the passthrough feed and adapts its safety guidance based on what the operator is looking at.

**Setup:** Same configuration as the medical training example. **Target Frame Rate** is set to 10 (reduced from 15) to accommodate an industrial network environment with limited bandwidth. **Max Output Width** is set to 960 to reduce per-frame payload size without meaningful quality loss for object recognition tasks.

**Outcome:** The character identifies machinery in the passthrough view and provides component-specific safety instructions — no hardcoded object detection, no custom computer vision pipeline. The SDK streams passthrough frames to Convai, which handles scene understanding and generates contextually appropriate guidance.

## Troubleshooting

| Symptom                                                                           | Likely cause                                                                                                                                                               | Fix                                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source transitions to `Failed / DeviceUnavailable` a few seconds after scene load | `PassthroughCameraAccess` not found after three retry attempts — OR — missing `horizonos.permission.HEADSET_CAMERA` / `android.permission.CAMERA` in `AndroidManifest.xml` | (1) Add `PassthroughCameraAccess` to the scene or assign it explicitly in the **Passthrough Camera Access** Inspector field. (2) Verify both permissions are declared in `AndroidManifest.xml` and appear in the exported APK manifest. |
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
