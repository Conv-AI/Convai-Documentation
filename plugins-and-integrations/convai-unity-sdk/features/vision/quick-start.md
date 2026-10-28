---
title: Vision quick start
description: Add a scene-camera feed to a working character, check the captured image and published track, and verify a vision response in the Unity Editor.
last_reviewed: "5.0.0-preview"
---

Add vision to an existing single-character scene that already supports conversation. This walkthrough uses a Unity camera and automatic publication. Group conversation rooms do not publish vision.

## Connect and capture

{% stepper %}
{% step %}
### Enable a Video connection

Select `ConvaiRoomManager`. In **Connection**, choose **Video**. With **Dynamic Vision** set to Auto or On, the setup dialog can offer **Add Components**, creating a `ConvaiVisionRoot` child with a publisher and camera source.

If components are still missing, the **Video needs a camera feed** warning offers **Add Missing Components**. That action adds the components to the room manager's own GameObject. Select the object actually created by your chosen path.
{% endstep %}
{% step %}
### Assign the captured camera

On `CameraVisionFrameSource`, open **Camera Setup** and assign **Target Camera**. When blank, the source tries a Camera on the same object, then `Camera.main`. **Use Main Camera** is available with the missing-camera warning. Explicit assignment avoids ambiguity.

In **Capture Settings**, leave **Preset** at **Balanced** for `1280 × 720` capture at `15` fps. The publisher's policy separately controls the transmitted frame budget.
{% endstep %}
{% step %}
### Verify capture and publication

Add **Convai > Vision > Vision Debug Preview (Editor Only)**, assign the intended source if there are several, and enter Play mode. Confirm the preview shows the intended image and increasing frame count. Separately check `ConvaiVisionPublisher.IsPublishing` after the room connects. Capture alone does not confirm publication.
{% endstep %}
{% step %}
### Verify the response

Request vision status or a vision trigger through the [sample debug tool](debug-preview.md). Inspect the returned outcome. A published track does not prove that frames were attached to a response.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Screenshot required before publishing:** Capture Camera Vision Frame Source with Capture Settings showing Balanced Preset and Camera Setup showing an assigned Target Camera and Identifier.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-vision-camera.png" alt="Camera Vision Frame Source with Capture Settings showing Balanced Preset and Camera Setup showing an assigned Target Camera and Identifier"><figcaption><p>TODO: Replace with screenshot showing Camera Vision Frame Source with Capture Settings showing Balanced Preset and Camera Setup showing an assigned Target Camera and Identifier.</p></figcaption></figure>

## Manual placement

Add `ConvaiVisionPublisher` to the room manager or a child, then add a frame source on that object or beneath it. Assign **Source** explicitly when there are multiple candidates. Runtime discovery does not search the whole scene.

Keep the publisher's **Track Name** aligned with the room's **Video Track Name**. A room-level name overrides the discovered publisher name. For browser builds, choose the picture deliberately in [WebGL vision](webgl.md).

{% content-ref url="publishing-and-policies.md" %}
[Publish policies](publishing-and-policies.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot vision](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
