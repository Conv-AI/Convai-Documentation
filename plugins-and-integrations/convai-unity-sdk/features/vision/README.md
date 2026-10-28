---
title: Vision
description: Find guides for adding real-time scene vision to Convai characters in Unity, including frame sources, publish policies, scripting, and troubleshooting.
last_reviewed: "5.0.0-preview"
---

Vision gives Convai characters the ability to see what is happening inside your Unity scene. A frame source captures images from a Unity camera, physical webcam, or Meta Quest passthrough feed, and the SDK streams them to Convai over WebRTC alongside the audio conversation.

## Platform support

| Platform | Supported frame sources | Notes |
| --- | --- | --- |
| PC / Mac / Console | `CameraVisionFrameSource`, `WebcamVisionFrameSource` | Full RenderTexture pipeline; max 30 fps |
| Android / iOS | `CameraVisionFrameSource`, `WebcamVisionFrameSource` | Webcam source requests camera permission at startup |
| WebGL | Camera, webcam, custom texture, or page canvas | Defaults to the frame source; **Game View** publishes the game canvas. An explicit FPS override can exceed the policy's `15` fps default cap. See [WebGL vision](webgl.md). |
| Meta Quest 3 / 3S | `QuestVisionFrameSource` | Requires Meta XR SDK and `horizonos.permission.HEADSET_CAMERA` |

{% hint style="info" %}
Vision needs an effective Video connection. **Dynamic Vision > On** resolves Audio to Video; **Off** preserves the configured connection type. Group conversation rooms resolve to Audio and do not publish vision.
{% endhint %}

{% hint style="danger" %}
Deploy WebGL over HTTPS and verify browser camera permission for webcam capture. Use loopback only for local development; test the selected source in an actual browser build.
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

Dynamic vision context lets Convai continuously sample the published video track into a rolling frame buffer and attach the freshest frames to a character's turns, instead of reacting to every frame as it arrives. It shares its respond-mode vocabulary with [dynamic context](../dynamic-context/README.md): `ConvaiRespondMode` values `Silent`, `Auto`, and `MustRespond` request silent input, let the character decide, or request a reply, respectively. See [Dynamic context scripting API](../dynamic-context/dynamic-context-scripting-api.md) for the full `ConvaiRespondMode` reference.

## Next steps

Start with [Vision quick start](quick-start.md) to get a working stream from a scene camera, then use [Vision frame sources](frame-sources.md) to select the right capture method for your platform. For pipeline details, see [How vision works](how-vision-works.md).
