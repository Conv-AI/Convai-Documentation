---
title: Vision in WebGL
description: Choose the image a browser build publishes, configure a scene or webcam source, and verify capture permissions and vision responses after deployment.
last_reviewed: "5.0.0-preview"
---

A WebGL build can publish a scene-camera texture, webcam texture, game view, or an application-owned page canvas. Choose the intended picture before building; Editor Play mode always previews the frame source and cannot prove the browser selected the same image.

## Choose the browser picture

{% stepper %}
{% step %}
### Configure a Video room

Use an effective Video connection and a `ConvaiVisionPublisher`. Group conversation rooms do not publish vision. Keep the publisher track name aligned with the room's **Video Track Name**.
{% endstep %}
{% step %}
### Select WebGL Publishes

In the publisher's **Frame Source** section, set **WebGL Publishes** to **Frame Source** or **Game View**. Frame Source is the default. With no source, the publisher falls back to the game view. Game View includes the game's rendered UI.

A source implementing `IVisionPageCanvasSource` always publishes its own `PageCanvasElementId`, even when Game View is selected. It is a source interface, not a third dropdown choice.
{% endstep %}
{% step %}
### Deploy and verify

Serve the build over HTTPS. For webcam capture, grant browser camera permission and wait for a usable frame. Check `IsPublishing`, then request vision status or a trigger and inspect the response. Confirm the content matches the intended source.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Screenshot required before publishing:** Capture Convai Vision Publisher with Frame Source, WebGL Publishes, Track Name, Publish Policy, Max Publish FPS, and Max Bitrate visible with the WebGL build target active.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-vision-publisher.png" alt="Convai Vision Publisher with Frame Source, WebGL Publishes, Track Name, Publish Policy, Max Publish FPS, and Max Bitrate visible with the WebGL build target active"><figcaption><p>TODO: Replace with screenshot showing Convai Vision Publisher with Frame Source, WebGL Publishes, Track Name, Publish Policy, Max Publish FPS, and Max Bitrate visible with the WebGL build target active.</p></figcaption></figure>

## Frame-source path

The SDK copies a texture source to a hidden page canvas for browser publication. `CameraVisionFrameSource` and `WebcamVisionFrameSource` are both usable on this path; a custom source must expose valid frames through the same contract. Output alpha is dropped.

`WebGLPublishSource` and `SetWebGLPublishSource(VisionWebGLPublishSource)` expose the selection in code. A live change replaces the published track. After a source stops or fails, restart it and call `EnablePublishing(true)` to resume publication, or reconnect. Switching a webcam is one case where this matters.

## Budget and custom canvases

Policy frame-rate defaults are capped at `15` fps in the browser path. A positive **Max Publish FPS** override is used as configured; the Inspector permits up to `30`. The policy bitrate budget still applies. These values request transport behavior and do not guarantee browser throughput.

For an application-owned canvas, implement `IVisionPageCanvasSource` and keep its element ID valid. Your page code creates the canvas, redraws it while capturing, and keeps it origin-clean. If it must update in background tabs, do not rely only on animation-frame callbacks. An invalid canvas retries; it does not silently switch to Game View. The publisher's readiness budget is `2` active seconds and pauses during permission waiting.

{% content-ref url="custom-frame-sources.md" %}
[Custom frame sources](custom-frame-sources.md)
{% endcontent-ref %}

{% content-ref url="debug-preview.md" %}
[Vision debug preview](debug-preview.md)
{% endcontent-ref %}
