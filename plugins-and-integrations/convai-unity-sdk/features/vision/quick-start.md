---
title: Vision quick start
description: Add a scene-camera feed to a working character, check the captured image and published track, and verify a vision response in the Unity Editor.
last_reviewed: "5.0.0-pre.1"
---

Add vision to an existing single-character scene that already supports conversation. This walkthrough uses a Unity camera and automatic publication. Group conversation rooms do not publish vision.

## Connect and capture

{% stepper %}
{% step %}
### Enable vision for the room

Select `ConvaiRoomManager`. Under **Connection**, set **Vision** to **On**. The setup dialog can offer **Add Components**, creating a `ConvaiVisionRoot` child with a publisher and camera source.

If components are still missing, the camera-feed warning offers **Add Missing Components**. That action adds the components to the room manager's own GameObject. Select the object actually created by your chosen path.

<figure><img src="../../../../.gitbook/assets/unity-room-vision-on.png" alt="Connection section of Convai Room Manager with Vision set to On."><figcaption><p>(1) Open <strong>Connection</strong> on the room manager. (2) Set <strong>Vision</strong> to <strong>On</strong>.</p></figcaption></figure>

<figure><img src="../../../../.gitbook/assets/unity-vision-setup-dialog.png" alt="Convai Vision Setup dialog offering to add the publisher and camera frame source."><figcaption><p>When setup prompts for the camera feed, choose <strong>Add Components</strong> (1).</p></figcaption></figure>

<figure><img src="../../../../.gitbook/assets/unity-vision-generated-hierarchy.png" alt="Hierarchy with ConvaiVisionRoot selected under the demo room."><figcaption><p>The dialog creates <strong>ConvaiVisionRoot</strong> (1) under the room. Its components are <strong>Convai Vision Publisher</strong> and <strong>Camera Vision Frame Source</strong>.</p></figcaption></figure>
{% endstep %}
{% step %}
### Assign the captured camera

On `CameraVisionFrameSource`, open **Camera Setup** and assign **Target Camera**. When blank, the source tries a Camera on the same object, then `Camera.main`. **Use Main Camera** is available with the missing-camera warning. Explicit assignment avoids ambiguity.

In **Capture Settings**, leave **Preset** at **Balanced** for `1280 × 720` capture at `15` fps. The publisher's policy separately controls the transmitted frame budget.

<figure><img src="../../../../.gitbook/assets/unity-vision-camera-source.png" alt="Camera Vision Frame Source Inspector with Balanced selected in Capture Settings and Convai Orbit Camera assigned under Camera Setup."><figcaption><p>(1) Open <strong>Camera Setup</strong>. (2) Assign the camera in <strong>Target Camera</strong>. (3) <strong>Balanced</strong> is selected in <strong>Capture Settings</strong>.</p></figcaption></figure>
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

## Manual placement

Add `ConvaiVisionPublisher` to the room manager or a child, then add a frame source on that object or beneath it. Assign **Source** explicitly when there are multiple candidates. Runtime discovery does not search the whole scene.

Set the track name on the publisher. The room uses the name reported by the registered publisher. For browser builds, choose the picture deliberately in [WebGL vision](webgl.md).

{% content-ref url="publishing-and-policies.md" %}
[Publish policies](publishing-and-policies.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot vision](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
