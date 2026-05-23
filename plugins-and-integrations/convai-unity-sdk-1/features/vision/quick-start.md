---
title: Vision quick start
description: Add Vision to an existing Convai scene so a character can see and respond to live camera input, using the SDK's automatic component setup.
---

Add Vision to an existing Convai scene in three steps. The SDK adds and wires the required components automatically when you set `ConvaiRoomManager` to Video mode.

## Prerequisites

- A Unity scene with a `ConvaiCharacter` component already set up and working (the character responds to speech).
- Your Convai API key configured in **Tools → Convai → Configuration**.

{% stepper %}
{% step %}
### Set Connection Type to Video

Select the `ConvaiRoomManager` GameObject in the Hierarchy. In the Inspector, set **Connection Type** to **Video**.

A dialog appears immediately:

> **Convai Vision Setup** — Connection Type is set to Video, but required vision components are missing. Add `ConvaiVisionPublisher` and `CameraVisionFrameSource` under this ConvaiRoomManager?

Click **Add Components**.

The SDK creates a child GameObject named **ConvaiVisionRoot** under `ConvaiRoomManager` and adds both `ConvaiVisionPublisher` and `CameraVisionFrameSource` to it.
{% endstep %}

{% step %}
### Assign a camera

Select the **ConvaiVisionRoot** GameObject (child of `ConvaiRoomManager`). On the `CameraVisionFrameSource` component, locate the **Target Camera** field.

- If your scene has a `Camera` tagged **MainCamera**, leave the field blank — the component resolves it automatically at runtime.
- To capture a specific camera (an overhead view, a security camera), drag that camera into the **Target Camera** field.

The default **Capture Preset** is **Balanced** (1280 × 720 at 15 fps), which suits most scenarios.

If **Target Camera** is blank and no camera in the scene is tagged **MainCamera**, the frame source enters `Failed` state at runtime. Always assign a camera explicitly or ensure one camera has the **MainCamera** tag.
{% endstep %}

{% step %}
### Verify with Debug Preview

On any scene GameObject, click **Add Component** → **Convai/Vision/Vision Debug Preview (Editor Only)**.

Press **Play**. An overlay appears in the Game view showing the live camera feed and a statistics panel. Once the room connects, the FPS counter increments and the frame count increases.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Success:** The Debug Preview overlay shows a live image and a non-zero FPS counter. Reading `ConvaiVisionPublisher.IsPublishing` from any script returns `true`. The character now receives the scene camera feed alongside the audio conversation.
{% endhint %}

{% hint style="warning" %}
If the overlay stays blank or the FPS counter reads zero, verify that `ConvaiRoomManager.Connection Type` is set to **Video** and that the room has fully connected. See [Vision troubleshooting](troubleshooting-and-diagnostics.md) for a step-by-step diagnosis.
{% endhint %}

## Manual component setup

If you clicked **Later** on the dialog, or want to place the components on a specific GameObject, add them manually:

1. Select the target GameObject (any persistent scene object — typically on or near your NPC).
2. **Add Component** → search for **Convai Vision Publisher**.
3. On the same GameObject (or a child), **Add Component** → **Convai/Vision/Camera Vision Frame Source**.
4. Assign the **Target Camera** if not using `Camera.main`.
5. Leave the **Source** field on `ConvaiVisionPublisher` blank — the publisher auto-discovers `CameraVisionFrameSource` on the same GameObject at runtime. Assign it explicitly only if you have multiple frame sources in the scene.

## Next steps

{% content-ref url="how-vision-works.md" %}
[How Vision works](how-vision-works.md)
{% endcontent-ref %}

{% content-ref url="frame-sources.md" %}
[Vision frame sources](frame-sources.md)
{% endcontent-ref %}

{% content-ref url="publishing-and-policies.md" %}
[Publish policies](publishing-and-policies.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Vision troubleshooting](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
