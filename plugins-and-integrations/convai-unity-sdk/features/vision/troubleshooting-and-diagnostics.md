---
title: Troubleshoot vision
description: Separate capture, publication, and response failures to diagnose camera feeds, source restarts, browser selection, and dynamic vision requests.
last_reviewed: "5.0.0-preview"
---

Check capture, publication, and service responses separately. A moving Editor preview proves local frames exist; `IsPublishing` proves a track was opened; a vision acknowledgement reports what Convai did with the request.

## Check the pipeline

{% stepper %}
{% step %}
### Confirm the effective room mode

Use **Connection Type > Video**, or **Dynamic Vision > On** to resolve a configured Audio connection to Video. **Off** does not override an explicitly configured Video connection. Group conversation rooms remain Audio and do not publish vision.
{% endstep %}
{% step %}
### Confirm the room and source

Wait for room connection. On native platforms, assign a valid source or place it on the publisher object or beneath it. Runtime discovery does not search the whole scene. For WebGL, check **WebGL Publishes** and [browser source selection](webgl.md).
{% endstep %}
{% step %}
### Inspect frame readiness

Read the source's `State`, `ErrorKind`, `StatusMessage`, and usable-frame state. The publisher waits up to `2` active seconds for readiness, suspending that budget while permission is pending. A timeout can retry on a later frame event; a stopped or failed source needs explicit restart of publication.
{% endstep %}
{% step %}
### Verify publication and acknowledgement

Check `IsPublishing`, then request vision status. Inspect the boolean send result and the eventual response event. If a publisher uses a custom track name, align it with the room's resolved **Video Track Name**.
{% endstep %}
{% endstepper %}

## Match the failure

| Symptom | Action | Verify |
|---|---|---|
| `Target camera became unavailable or was destroyed` / `vision.camera_not_found` | Assign **Target Camera**. A blank reference tries a same-object Camera, then `Camera.main`. | The source produces a usable frame. |
| Black camera image | Confirm the intended camera, visible content, and render backend. Automatic SRP capture uses the explicit compatibility path; `SrpNative` is unavailable. | Preview the actual captured image. |
| Webcam permission denied | Check platform declarations and the user's current grant. On WebGL, test HTTPS and browser permission. | `Ready` and increasing frame count, not only permission success. |
| Webcam switched but publication stopped | After `SwitchWebcamAsync` succeeds, call `EnablePublishing(true)` or reconnect. | A new track publishes from the reopened source. |
| `Frame source did not become ready within 2s` | Check startup, permission state, texture/canvas output, and frame events. | A usable output causes publication. |
| `Frame source failed before publish. State=..., Error=...` | Fix the reported source failure, then explicitly enable publication again. | The source is usable and `IsPublishing` becomes true. |
| Quest source fails with `InvalidConfiguration` | Check that `PassthroughCameraAccess` exists and is readable on the target device, with the required platform integration. | The source binds and produces frames on device. |
| Browser shows the wrong picture | Choose Frame Source or Game View deliberately. An assigned page-canvas source uses its own canvas. | Inspect a browser vision response, not only the Editor preview. |
| Debug preview absent in a player | Expected: `VisionDebugPreview` disables itself in every player build. | Use publish state and response diagnostics in the player. |
| Sampling window omitted | Set both count and spacing above zero in **Custom Frame Spacing**. Keep totals within **Frames Per Reply**. | Inspect the requested settings and response. |
| Respond-mode update has no effect | Check the send boolean, target selection, group restrictions, and response `Status`/`Message`. | The acknowledgement reports the intended lane and mode. |

## Diagnose persistent black frames

For `CameraVisionFrameSource`, the optional health probe is available through the Inspector's Debug mode, not its normal custom Inspector. It reads a `4 × 4` pixel block at most every `0.75` seconds after a `1.5`-second grace period, when render hooks are unhealthy or the explicit path is active. It warns after `5` consecutive invalid samples; on the explicit path it escalates after `30`. It is a diagnostic readback, not a per-frame image logger. Disable it when the investigation is complete.

## Enable targeted logs

Open **Edit > Project Settings > Convai SDK > Diagnostics**. **Verbose** is a preset, not a log level. Set **Vision** under **Category Overrides** to Debug or Trace when needed, and reproduce once. Debug calls must also be present in the build: the Editor, a Development Build, or the Debug Logging feature flag provides them.

Capture domain events are emitted by the camera source only. For webcam and Quest health, subscribe to `IVisionFrameSourceStatusProvider.StatusChanged`. Track unpublish reasons are coarse: normal unpublish uses `UserRequested`, even on session end, so retain the surrounding source state when diagnosing.

{% content-ref url="scripting-api.md" %}
[Vision scripting API](scripting-api.md)
{% endcontent-ref %}
