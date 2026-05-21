# Quick Start

### Your First Vision Setup

This guide walks you through the minimum steps needed to get a Convai character receiving a live camera feed from your Unity scene. The SDK can add the required components automatically — follow the primary path below, or use the manual path if you dismissed the prompt or need custom component placement.

{% hint style="info" %}
**Prerequisites**

* A Unity scene with a `ConvaiCharacter` component already set up and working (the character responds to speech).
* Your Convai API key is configured in **Tools → Convai → Configuration**.
{% endhint %}

{% stepper %}
{% step %}
**Set the Connection Type to Video**

Select the `ConvaiRoomManager` GameObject in the Hierarchy. In the Inspector, set **Connection Type** to **Video**.

A dialog appears immediately:

> **Convai Vision Setup** — Connection Type is set to Video, but required vision components are missing. Add `ConvaiVisionPublisher` and `CameraVisionFrameSource` under this ConvaiRoomManager?

Click **Add Components**.

The SDK creates a child GameObject named **ConvaiVisionRoot** under `ConvaiRoomManager` and adds both `ConvaiVisionPublisher` and `CameraVisionFrameSource` to it.

{% hint style="info" %}
If you clicked **Later** and need to add the components manually, see [Manual Component Setup](quick-start.md#manual-component-setup) below.
{% endhint %}
{% endstep %}

{% step %}
**Assign a Camera (If Not Using Camera.main)**

Select the **ConvaiVisionRoot** GameObject (child of `ConvaiRoomManager`). On the `CameraVisionFrameSource` component, locate the **Target Camera** field.

* If your scene has a `Camera` tagged **MainCamera**, leave the field blank — the component resolves it automatically at runtime.
* To capture a specific camera (an overhead view, a security camera), drag that camera into the **Target Camera** field.

The default **Capture Preset** is **Balanced** (1280 × 720 at 15 fps), which suits most scenarios.

{% hint style="warning" %}
If **Target Camera** is blank and no camera in the scene is tagged **MainCamera**, the frame source enters `Failed` state at runtime. Always assign a camera explicitly or ensure one camera has the **MainCamera** tag.
{% endhint %}
{% endstep %}

{% step %}
**Add Vision Debug Preview and Verify**

On any scene GameObject, click **Add Component** → **Convai/Vision/Vision Debug Preview (Editor Only)**.

Press **Play**. An overlay appears in the Game view showing the live camera feed and a statistics panel. Once the room connects, the FPS counter increments and the frame count increases.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Success:** The Debug Preview overlay shows a live image and a non-zero FPS counter. Reading `ConvaiVisionPublisher.IsPublishing` from any script returns `true`. The character now receives the scene camera feed alongside the audio conversation.
{% endhint %}

{% hint style="warning" %}
If the overlay stays blank or the FPS counter reads zero, verify that `ConvaiRoomManager.Connection Type` is set to **Video** and that the room has fully connected. See [Troubleshooting & Diagnostics](/broken/pages/ce72ed1f95d78e73f4af5a61fbeaeb221e86e25d) for a step-by-step diagnosis.
{% endhint %}

***

### Manual Component Setup

If you clicked **Later** on the dialog, or want to place the components on a specific GameObject, add them manually:

1. Select the target GameObject (any persistent scene object — typically on or near your NPC).
2. **Add Component** → search for **Convai Vision Publisher**.
3. On the same GameObject (or a child), **Add Component** → **Convai/Vision/Camera Vision Frame Source**.
4. Assign the **Target Camera** if not using `Camera.main`.
5. Leave the **Frame Source Component** field on `ConvaiVisionPublisher` blank — the publisher auto-discovers `CameraVisionFrameSource` on the same GameObject at runtime. Assign it explicitly only if you have multiple frame sources in the scene.

***

### What Just Happened

When you clicked **Add Components** and pressed Play, the following occurred:

1. The SDK created a **ConvaiVisionRoot** child GameObject under `ConvaiRoomManager` and added `ConvaiVisionPublisher` and `CameraVisionFrameSource` to it.
2. `ConvaiRoomManager` established a **Video** connection to Convai.
3. `ConvaiVisionPublisher` detected the active room and waited for the frame source to become ready.
4. `CameraVisionFrameSource` rendered the assigned camera (or `Camera.main`) into a `RenderTexture` and signalled that frames were available.
5. `VisionPublishCoordinator` applied the `AutoCompatible` publish policy (10 fps, 750 kbps) and passed the texture to the video pipeline.
6. A video track named `"unity-scene"` was published to Convai. `IsPublishing` became `true`.

From this point the character receives the live scene camera feed alongside the audio conversation, processed together.

***

### Next Steps

You now have a working Vision setup. The SDK handles component placement and runtime wiring automatically. Continue to [Frame Sources](/broken/pages/44c584bfd55c71a11de36936d6fd56b8168e8858) to configure the right capture method for your platform, or jump to [Publishing & Policies](/broken/pages/1538f07b55ab5c719a79be190e1c775c62b5bd3c) to control frame rate and bandwidth. If anything is not working, start with [Troubleshooting & Diagnostics](/broken/pages/ce72ed1f95d78e73f4af5a61fbeaeb221e86e25d).
