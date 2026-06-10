---
title: Troubleshoot vision
description: Fix common Unreal vision problems including missing visual context, failed starts, blank render targets, and invalid source registration.
last_reviewed: "4.0.0-beta.21"
---

Use this page when scene vision does not work as expected. Each entry lists the symptom, probable cause, fix, and how to verify the fix.

## Diagnostic order

Check these signals before working through individual issues:

1. On the **Convai Chatbot** component, call **Supports Vision**.
2. On **Environment Webcam**, call **Get State**.
3. On **Environment Webcam**, call **Get Last Error Message** and **Get Last Error Code**.
4. Confirm **Convai Render Target** is assigned in the **Details** panel.
5. Open the render target asset in the **Content Browser** during Play In Editor and confirm the preview updates.
6. In the **Output Log**, filter by `ConvaiChatbotComponentLog` and look for `SendImage: Sending raw image` or `SendImage: Unable to capture Raw data`.

| Signal | Healthy value |
|---|---|
| **Supports Vision** | `true` |
| **Get State** | `Capturing` during an active capture session |
| **Get Last Error Message** | Empty string after a successful start |
| Render target preview | Shows scene content during Play In Editor |
| Output Log | `SendImage: Sending raw image` |

## The character does not respond to visual context

**Symptom:** The character responds to speech but ignores objects visible in the scene.

**Cause:** The frame source is not registered with the chatbot, capture is not in `Capturing` state, or the session was created before vision was available.

**Fix:**

1. Place **Environment Webcam** on the same `Actor` as the **Convai Chatbot** component, or call **Set Vision Component** with the webcam reference.
2. Call **Get State**. If it returns `Stopped`, call **Start** from `BeginPlay` or enable `bAutoStartVision`.
3. Assign a `UTextureRenderTarget2D` to **Convai Render Target**.
4. If the vision component is added after initial connection setup, enable **Always Allow Vision** in **Edit > Project Settings > Plugins > Convai** (advanced category), then reconnect the session.

**Verify:** **Supports Vision** returns `true`, **Get State** returns `Capturing`, and the character references visible scene content in its response.

## Start has no effect — the component stays in Stopped

**Symptom:** Calling **Start** does not move the component to `Capturing`. **Get State** still returns `Stopped`.

**Cause:** **Convai Render Target** is not assigned. `UEnvironmentWebcam` checks `CanStart()` before transitioning.

**Fix:** Assign a `UTextureRenderTarget2D` to **Convai Render Target**. Create the asset from **Convai > Vision  Render Target** in the **Content Browser** to use the plugin defaults (`512 x 512`, `RTF_RGBA8`, black clear color).

**Verify:** Call **Start** again. **Get State** should return `Capturing` within one tick.

**Diagnostic message:** **Get Last Error Message** returns `ConvaiRenderTarget is null. Cannot start capture.` when this failure occurs.

## Render target appears black or blank

**Symptom:** The render target preview in the **Content Browser** or a debug widget shows a completely black image.

**Cause:** **Environment Webcam** is not facing visible scene geometry, capture has not started, or the internal capture source was changed.

**Fix:**

1. Select **Environment Webcam** and confirm its `+X` axis faces the scene area you want the character to see.
2. Call **Get State**. If the state is `Stopped`, call **Start** or enable `bAutoStartVision`.
3. Select the nested `EnvironmentSceneCapture2D` sub-component (the `CaptureComponent` property) and confirm **Capture Source** is `SCS_FinalToneCurveHDR`.
4. If `bCopyPostProcessProperties` is `true`, verify that a post-process volume exists in the level. If not, disable the property.

**Verify:** With Play In Editor running, the render target preview should update with scene content.

## High latency in character responses when vision is on

**Symptom:** Character response time increases noticeably compared to conversations without vision.

**Cause:** Frames are being captured and sent at the default `15` FPS.

**Fix:** Lower the capture rate. Set **Maximum FPS** (`m_MaxFPS`) to `5` in the **Details** panel, or call **Set Max FPS** with value `5`.

**Verify:** Measure response time before and after the change. The **Output Log** should still show `SendImage: Sending raw image` at the reduced cadence.

## Supports Vision returns false after calling Set Vision Component

**Symptom:** **Set Vision Component** returns `false` and the chatbot still reports vision unsupported.

**Cause:** The passed component does not implement `UConvaiVisionInterface`.

**Fix:** Pass a `UConvaiWebcamBase` subclass such as `UEnvironmentWebcam`, or another class that implements `IConvaiVisionInterface`. A plain `USceneCaptureComponent2D` is not a valid frame source.

**Verify:** Cast the component to `UConvaiWebcamBase` in Blueprint. If the cast succeeds, pass it to **Set Vision Component** and confirm the return value is `true`.

## Console warns that raw data cannot be captured

**Symptom:** The **Output Log** shows `SendImage: Unable to capture Raw data`.

**Cause:** `UConvaiChatbotComponent::SendImage()` called `CaptureRaw()`, but the active frame source returned `false` or empty frame data.

**Fix:**

1. Confirm **Get State** returns `Capturing`.
2. Confirm **Convai Render Target** is assigned.
3. Open the render target preview and verify it contains scene content.
4. For a custom vision component, verify that `CaptureRaw()` fills `Width`, `Height`, and `Data`, and returns `true`.

**Verify:** The **Output Log** should switch to `SendImage: Sending raw image` after frame capture succeeds.

## Next steps

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Vision usage examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Vision quick start](quick-start.md)
{% endcontent-ref %}
