---
title: Vision
description: Find guides for adding real-time scene vision to Convai characters in Unity, including frame sources, publish policies, scripting, and troubleshooting.
last_reviewed: "4.4.0"
---

Vision gives Convai characters the ability to see what is happening inside your Unity scene. A frame source captures images from a Unity camera, physical webcam, or Meta Quest passthrough feed, and the SDK streams them to Convai over WebRTC alongside the audio conversation.

## Platform support

| Platform | Supported frame sources | Notes |
| --- | --- | --- |
| PC / Mac / Console | `CameraVisionFrameSource`, `WebcamVisionFrameSource` | Full RenderTexture pipeline; max 30 fps |
| Android / iOS | `CameraVisionFrameSource`, `WebcamVisionFrameSource` | Webcam source requests camera permission at startup |
| WebGL | _(Canvas, automatic)_ | `canvas.captureStream()` path — no frame source component needed; frame rate capped at 15 fps; **HTTPS required** |
| Meta Quest 3 / 3S | `QuestVisionFrameSource` | Requires Meta XR SDK and `horizonos.permission.HEADSET_CAMERA` |

{% hint style="info" %}
Vision requires `ConvaiRoomManager.Connection Type` set to **Video**. If it is set to `Audio`, `ConvaiVisionPublisher` remains idle regardless of how other components are configured.
{% endhint %}

{% hint style="danger" %}
**WebGL: HTTPS required.** The `canvas.captureStream()` API is blocked by browsers on non-HTTPS origins. `http://localhost` is the only exception. Deploy your WebGL build to an HTTPS host before testing Vision in production.
{% endhint %}

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>How vision works</strong><br>Understand the pipeline architecture, key concepts, component placement, and the startup sequence.</td><td><a href="how-vision-works.md">how-vision-works.md</a></td></tr>
<tr><td><strong>Dynamic vision context</strong><br>Turn on frame sampling so a character reasons over buffered frames instead of every incoming one, using the same respond-mode vocabulary as dynamic context.</td><td><a href="dynamic-vision-context.md">dynamic-vision-context.md</a></td></tr>
<tr><td><strong>Vision quick start</strong><br>Get a character receiving a live camera feed with a step-by-step Inspector walkthrough — no code required.</td><td><a href="quick-start.md">quick-start.md</a></td></tr>
<tr><td><strong>Vision frame sources</strong><br>Configure CameraVisionFrameSource, WebcamVisionFrameSource, and QuestVisionFrameSource for every platform and use case.</td><td><a href="frame-sources.md">frame-sources.md</a></td></tr>
<tr><td><strong>Publish policies</strong><br>Choose a publish policy, tune frame rate and bitrate, and understand platform-specific behavior including WebGL.</td><td><a href="publishing-and-policies.md">publishing-and-policies.md</a></td></tr>
<tr><td><strong>Vision debug preview</strong><br>Visualize the active frame source as an on-screen overlay and monitor capture health in the Editor.</td><td><a href="debug-preview.md">debug-preview.md</a></td></tr>
<tr><td><strong>Custom frame sources</strong><br>Implement IVisionFrameSource to publish any custom video pipeline — interface contract, Y-flip requirement, and minimal implementation.</td><td><a href="custom-frame-sources.md">custom-frame-sources.md</a></td></tr>
<tr><td><strong>Vision scripting API</strong><br>ConvaiVisionPublisher properties and methods, runtime state monitoring, and domain events for analytics integration.</td><td><a href="scripting-api.md">scripting-api.md</a></td></tr>
<tr><td><strong>Vision usage examples</strong><br>End-to-end examples for safety training, equipment onboarding, VR walkthroughs, and manual-trigger sessions.</td><td><a href="usage-examples.md">usage-examples.md</a></td></tr>
<tr><td><strong>Troubleshoot vision</strong><br>Diagnose publishing failures, blank feeds, permission errors, and platform-specific issues with a structured checklist and decision tree.</td><td><a href="troubleshooting-and-diagnostics.md">troubleshooting-and-diagnostics.md</a></td></tr>
</tbody></table>

## Dynamic vision context

Dynamic vision context lets Convai continuously sample the published video track into a rolling frame buffer and attach the freshest frames to a character's turns, instead of reacting to every frame as it arrives. It shares its respond-mode vocabulary with [dynamic context](../dynamic-context/README.md): `ConvaiRespondMode` values `Silent`, `Auto`, and `MustRespond` decide whether new input speaks, whether the model decides, or whether it stays silent. See [Dynamic context scripting API](../dynamic-context/dynamic-context-scripting-api.md) for the full `ConvaiRespondMode` reference.

## Next steps

Start with [Vision quick start](quick-start.md) to get a working stream from a scene camera, then use [Vision frame sources](frame-sources.md) to select the right capture method for your platform. For pipeline details, see [How vision works](how-vision-works.md).
