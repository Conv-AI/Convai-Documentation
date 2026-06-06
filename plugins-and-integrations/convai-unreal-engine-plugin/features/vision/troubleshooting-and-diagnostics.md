---
title: Troubleshoot vision
description: Fix common vision problems including blank feeds, incorrect vision states, and frame-rate issues, and read diagnostic state at runtime.
last_reviewed: "4.0.0-beta.21"
---

Use this page to diagnose and fix problems with the vision feature. Each entry states the symptom, probable cause, fix, and how to verify the fix worked.

## Diagnostic state at runtime

Before working through specific issues, read the component's diagnostic state.

Call **Get State** on the **Environment Webcam** component. Compare the returned `EVisionState` against what you expect:

- `Stopped` — the component has not been started.
- `Starting` — the component is initializing; wait one or two ticks.
- `Capturing` — the component is running normally.
- `Stopping` — the component is shutting down.
- `Paused` — the component was running but has been suspended.

Call **Get Last Error Message** and **Get Last Error Code** on the component to retrieve the most recent error. An empty message means no error has been recorded since the component was created.

## The character does not respond to visual context

**Symptom:** The character responds normally to speech but ignores objects visible in the scene.

**Cause:** The vision component is not registered with the chatbot, the component is in the `Stopped` state, or no render target is assigned.

**Fix:**
1. Call **Supports Vision** on the `UConvaiChatbotComponent`. If it returns `false`, the chatbot has no vision component registered. Verify that the **Environment Webcam** component is on the same Actor as the chatbot and that `Start` has been called.
2. Call **Get State** on the webcam. If it returns `Stopped`, call `Start` from `BeginPlay` or set `bAutoStartVision = true`.
3. In the **Details** panel for the webcam, confirm that a `UTextureRenderTarget2D` is assigned to **Convai Render Target**.

**Verify:** Call **Supports Vision** again. It should return `true`. Ask the character about something visible in front of it; the response should reference scene content.

## Start has no effect — the component stays in Stopped

**Symptom:** Calling `Start` does not move the component to `Capturing`. `Get State` still returns `Stopped`.

**Cause:** The `ConvaiRenderTarget` property is `null`. `UEnvironmentWebcam` checks `CanStart()` before transitioning, and `CanStart` requires a valid render target.

**Fix:** Assign a `UTextureRenderTarget2D` to **Convai Render Target** in the **Details** panel. Create the asset using **Right-click → Convai Vision Render Target** in the Content Browser to get the correct format automatically.

**Verify:** Call `Start` again. `Get State` should return `Capturing` within one tick.

## Render target appears black or blank

**Symptom:** The render target in the Content Browser or a debug widget shows a completely black image.

**Cause:** The `CaptureComponent` inside `UEnvironmentWebcam` is not positioned in front of any scene geometry, or its capture source is misconfigured.

**Fix:**
1. Select the **Environment Webcam** component and check its position in the Viewport. The component must face the scene; the `+X` axis is the viewing direction.
2. Select the nested **Environment Scene Capture 2D** sub-component and confirm its **Capture Source** has not been changed from the default (`SCS_FinalToneCurveHDR`). Changing it to an incompatible mode can produce a black or empty image.
3. If `bCopyPostProcessProperties` is `true`, verify that a post-process volume is present and configured in the level.

**Verify:** Open the render target asset in the Content Browser. With the level running, the preview should update with scene content.

## High latency in character responses when vision is on

**Symptom:** Character response time increases noticeably compared to conversations without vision.

**Cause:** Frames are being sent at the default 15 FPS. Each frame adds data to the WebRTC stream.

**Fix:** Reduce the capture rate. Call **Set Max FPS** on the webcam with a lower value such as `5`. For most conversational contexts, 5 FPS provides sufficient visual continuity.

**Verify:** Measure response time before and after the FPS change. A lower FPS reduces per-turn data volume.

## Supports Vision returns false after calling Set Vision Component

**Symptom:** Calling **Set Vision Component** returns `false` and the chatbot still reports vision unsupported.

**Cause:** The component passed to `Set Vision Component` does not implement `IConvaiVisionInterface`.

**Fix:** Confirm that the component you are passing is a `UConvaiWebcamBase` subclass (such as `UEnvironmentWebcam`) or another class that explicitly implements `IConvaiVisionInterface`. Passing a plain `USceneCaptureComponent2D` or other non-vision component will fail silently.

**Verify:** Cast the component to `UConvaiWebcamBase` in Blueprint. If the cast succeeds, the component is a valid vision source. Pass it to `Set Vision Component` and check the return value.

## Frames stop after a few seconds

**Symptom:** Vision appears to work initially, then stops sending frames. `Get State` returns `Stopped` or `Paused`.

**Cause:** An error in the capture pipeline (for example a render target format mismatch or a GPU flush failure) caused the component to call `SetState(Stopped)` internally.

**Fix:** Call **Get Last Error Message** on the webcam immediately after the symptom is observed. Check the render target format; it must be `RTF RGBA8`. If `bCopyPostProcessProperties` is `true` and no post-process volume is present, disable that property.

**Verify:** Restart vision by calling `Stop` followed by `Start`. Monitor `Get State` for several seconds; it should remain `Capturing`.

## Next steps

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Vision usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="frame-sources.md" %}
[Vision frame sources](frame-sources.md)
{% endcontent-ref %}
