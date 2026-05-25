---
title: Vision debug preview
description: >-
  Reference for VisionDebugPreview, including Inspector fields, statistics
  overlay output, and script access for verifying the live feed in the Editor.
---

# Vision debug preview

`VisionDebugPreview` is an Editor-only component that renders the live camera feed as a screen overlay and displays a capture statistics panel. Use it to answer "What does the AI actually see?" during development before shipping.

### Add the component

On any scene GameObject, click **Add Component** → **Convai/Vision/Vision Debug Preview (Editor Only)**.

The component auto-discovers the active frame source in the scene. No explicit assignment is required unless multiple frame sources are present.

{% hint style="info" %}
`VisionDebugPreview` discovers frame sources in priority order: same GameObject, children, parents, then scene-wide search. Assign the **Frame Source Component** field explicitly when multiple frame sources are present to avoid ambiguity.
{% endhint %}

### Inspector reference

**Preview Settings**

| Field            | Type   | Default | Description                           |
| ---------------- | ------ | ------- | ------------------------------------- |
| **Show Preview** | `bool` | `true`  | Enables the camera feed overlay.      |
| **Show Stats**   | `bool` | `true`  | Enables the capture statistics panel. |

**Source**

| Field                               | Type            | Default             | Description                                                                                                                                   |
| ----------------------------------- | --------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frame Source Component**          | `MonoBehaviour` | _(auto-discovered)_ | The frame source to preview. Leave blank to auto-discover.                                                                                    |
| **Fallback To Active Frame Source** | `bool`          | `true`              | When the assigned source has no texture, searches the scene for another active frame source. Useful when the source starts after the preview. |

**Overlay Layout**

| Field                | Type              | Default       | Description                                                                                                         |
| -------------------- | ----------------- | ------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Overlay Position** | `PreviewPosition` | `BottomRight` | Corner of the Game view where the preview is anchored. Options: `TopLeft`, `TopRight`, `BottomLeft`, `BottomRight`. |
| **Overlay Width**    | `int` (160–640)   | `320`         | Preview width in pixels. Height is calculated automatically from the aspect ratio.                                  |
| **Offset X**         | `int` (0–200)     | `10`          | Horizontal inset from the selected corner in pixels.                                                                |
| **Offset Y**         | `int` (0–200)     | `10`          | Vertical inset from the selected corner in pixels.                                                                  |

<figure><img src="../../../../.gitbook/assets/image (503).png" alt="Debug preview overlay positioning controls in the Inspector"><figcaption><p>Debug preview overlay positioning controls.</p></figcaption></figure>

**Aspect Ratio**

| Field                       | Type          | Default        | Description                                                                                                                |
| --------------------------- | ------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Use Source Aspect Ratio** | `bool`        | `true`         | When enabled, derives aspect ratio from the frame source's `FrameDimensions`. When disabled, uses **Custom Aspect Ratio**. |
| **Custom Aspect Ratio**     | `float` (1–3) | `1.778` (16:9) | Aspect ratio used when **Use Source Aspect Ratio** is disabled.                                                            |

### Statistics overlay

When **Show Stats** is enabled, a text box is drawn adjacent to the preview. The exact output:

```
Vision Capture Debug
Status: Capturing
Source: ConvaiVisionRoot/ConvaiVisionRoot [camera] (CameraVisionFrameSource)
Resolution: 1280x720
FPS: 14.9 (target: 15)
Frames: 447
```

| Line                          | Source                                            | Notes                                              |
| ----------------------------- | ------------------------------------------------- | -------------------------------------------------- |
| `Status: Capturing / Stopped` | `IsCapturing` on the frame source                 | Boolean string — not the `VisionSourceState` enum. |
| `Source: ...`                 | Hierarchy path + SourceId + type name             | Full path from scene root for disambiguation.      |
| `Resolution: WxH`             | `FrameDimensions`                                 | `(0, 0)` before capture starts.                    |
| `FPS: X.X (target: Y)`        | Measured over 0.5 s intervals + `TargetFrameRate` | Measured FPS updates every 0.5 seconds.            |
| `Frames: N`                   | `FrameCount`                                      | Cumulative total since capture started.            |

<figure><img src="../../../../.gitbook/assets/image (491).png" alt="Statistics panel showing FPS and frame metrics in the Vision Debug Preview overlay"><figcaption><p>Statistics panel showing FPS and frame metrics.</p></figcaption></figure>

{% hint style="warning" %}
**`IsCapturing` vs `IsPublishing`:** The statistics panel shows `IsCapturing` — whether the frame source is producing frames. This is distinct from `ConvaiVisionPublisher.IsPublishing`, which indicates whether a WebRTC video track is actively being sent to Convai. Both can be checked independently; a source may be capturing while publishing is paused or not yet started.
{% endhint %}

### Script access

These properties can be read from other scripts:

| Property      | Type    | Description                                           |
| ------------- | ------- | ----------------------------------------------------- |
| `ShowPreview` | `bool`  | Gets or sets whether the preview overlay is visible.  |
| `ShowStats`   | `bool`  | Gets or sets whether the statistics panel is visible. |
| `CurrentFps`  | `float` | Measured capture FPS, updated every 0.5 seconds.      |
| `FrameCount`  | `long`  | Cumulative frames from the current frame source.      |
| `IsCapturing` | `bool`  | Whether the current frame source is capturing.        |

### Known limitations

* Editor only. `VisionDebugPreview` calls `enabled = false` in `Awake()` on non-Editor builds. No runtime overhead in shipped builds.
* On WebGL the overlay is blank because `ConvaiVisionPublisher` bypasses frame sources and uses `canvas.captureStream()` directly. There is no `RenderTexture` to display. Verify the stream via `IsPublishing` instead.
* The overlay is rendered via `OnGUI` (IMGUI). It cannot be positioned with UGUI or rendered in world space.
* Only one statistics panel is drawn per `VisionDebugPreview` component. Add multiple components if you need to compare two frame sources side by side.

### Next steps

{% content-ref url="publishing-and-policies.md" %}
[publishing-and-policies.md](publishing-and-policies.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[troubleshooting-and-diagnostics.md](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
