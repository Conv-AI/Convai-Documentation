---
title: Vision quick start
description: >-
  Add Vision to an existing Convai scene so a character can see and respond to
  live camera input, using the SDK's automatic component setup.
---

# Vision quick start

Add Vision to an existing Convai scene in three steps. The SDK adds and wires the required components automatically when you set `ConvaiRoomManager` to Video mode.

### Prerequisites

Before starting, verify:

* [ ] A `ConvaiCharacter` is in the scene and responds to speech in Play Mode

{% stepper %}
{% step %}
#### Set Connection Type to Video

Select the `ConvaiRoomManager` GameObject in the Hierarchy. In the Inspector, set **Connection Type** to **Video**.

<figure><img src="../../../../.gitbook/assets/Screenshot 2026-05-13 225029 (1).png" alt="Connection Type set to Video on ConvaiRoomManager in the Inspector"><figcaption><p>Connection Type set to Video on ConvaiRoomManager.</p></figcaption></figure>

A dialog appears immediately:

> **Convai Vision Setup** — Connection Type is set to Video, but required vision components are missing. Add `ConvaiVisionPublisher` and `CameraVisionFrameSource` under this ConvaiRoomManager?

Click **Add Components**.

<figure><img src="../../../../.gitbook/assets/Screenshot 2026-05-13 225326 (1).png" alt="Convai Vision Setup dialog prompt"><figcaption><p>Convai Vision Setup dialog prompt.</p></figcaption></figure>

The SDK creates a child GameObject named **ConvaiVisionRoot** under `ConvaiRoomManager` and adds both `ConvaiVisionPublisher` and `CameraVisionFrameSource` to it.
{% endstep %}

{% step %}
#### Assign a camera

Select the **ConvaiVisionRoot** GameObject (child of `ConvaiRoomManager`). On the `CameraVisionFrameSource` component, locate the **Target Camera** field.

* If your scene has a `Camera` tagged **MainCamera**, leave the field blank — the component resolves it automatically at runtime.
* To capture a specific camera (an overhead view, a security camera), drag that camera into the **Target Camera** field.

The default **Capture Preset** is **Balanced** (1280 × 720 at 15 fps), which suits most scenarios.

If **Target Camera** is blank and no camera in the scene is tagged **MainCamera**, the frame source enters `Failed` state at runtime. Always assign a camera explicitly or ensure one camera has the **MainCamera** tag.

<figure><img src="../../../../.gitbook/assets/Screenshot 2026-05-13 230410 (1).png" alt="Target Camera assigned on CameraVisionFrameSource in the Inspector"><figcaption><p>Target Camera assigned on CameraVisionFrameSource.</p></figcaption></figure>
{% endstep %}

{% step %}
#### Verify with Debug Preview

On any scene GameObject, click **Add Component** → **Convai/Vision/Vision Debug Preview (Editor Only)**.

Press **Play**. An overlay appears in the Game view showing the live camera feed and a statistics panel. Once the room connects, the FPS counter increments and the frame count increases.

<figure><img src="../../../../.gitbook/assets/Screenshot 2026-05-13 230509 (1).png" alt="Vision Debug Preview component added to a scene GameObject"><figcaption><p>Vision Debug Preview component added.</p></figcaption></figure>
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Success:** The Debug Preview overlay shows a live image and a non-zero FPS counter. Reading `ConvaiVisionPublisher.IsPublishing` from any script returns `true`. The character now receives the scene camera feed alongside the audio conversation.
{% endhint %}

{% hint style="warning" %}
If the overlay stays blank or the FPS counter reads zero, verify that `ConvaiRoomManager.Connection Type` is set to **Video** and that the room has fully connected. See [Troubleshoot vision](troubleshooting-and-diagnostics.md) for a step-by-step diagnosis.
{% endhint %}

### Manual component setup

If you clicked **Later** on the dialog, or want to place the components on a specific GameObject, add them manually:

1. Select the target GameObject (any persistent scene object — typically on or near your NPC).
2. **Add Component** → search for **Convai Vision Publisher**.
3. On the same GameObject (or a child), **Add Component** → **Convai/Vision/Camera Vision Frame Source**.
4. Assign the **Target Camera** if not using `Camera.main`.
5. Leave the **Source** field on `ConvaiVisionPublisher` blank — the publisher auto-discovers `CameraVisionFrameSource` on the same GameObject at runtime. Assign it explicitly only if you have multiple frame sources in the scene.

<figure><img src="../../../../.gitbook/assets/image (492).png" alt="Manual vision setup showing ConvaiVisionPublisher and CameraVisionFrameSource components"><figcaption><p>Manual vision setup — publisher and frame source components.</p></figcaption></figure>

### Next steps

{% content-ref url="how-vision-works.md" %}
[how-vision-works.md](how-vision-works.md)
{% endcontent-ref %}

{% content-ref url="frame-sources.md" %}
[frame-sources.md](frame-sources.md)
{% endcontent-ref %}

{% content-ref url="publishing-and-policies.md" %}
[publishing-and-policies.md](publishing-and-policies.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[troubleshooting-and-diagnostics.md](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
