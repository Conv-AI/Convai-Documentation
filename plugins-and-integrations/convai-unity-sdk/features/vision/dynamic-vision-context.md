---
title: Dynamic vision context
description: Reference for the dynamic vision context types that configure backend-driven camera frame sampling and per-lane respond-mode defaults.
last_reviewed: "5.0.0-preview"
---

Field-level reference for the three types that configure dynamic vision context: `ConvaiVisionContextMode` enables it per room, `ConvaiVisionInputSettings` tunes backend frame sampling, and `ConvaiVisionRespondModeSettings` sets per-lane respond-mode defaults. See [How vision works](how-vision-works.md#dynamic-vision-context) for what dynamic vision context is, why it exists, and how to enable it on a room.

{% hint style="info" %}
These settings request service behavior. Account availability, model compatibility, timing, and cost must be confirmed from actual responses and your service configuration.
{% endhint %}

## `ConvaiVisionContextMode`

Controls whether a room requests dynamic vision context. In the room manager's **Vision** card or profile, **Dynamic Vision** displays **Auto**, **On**, and **Off** for `Auto`, `Enabled`, and `Disabled`. Other sampling controls are shown when vision is on. Group rooms remain Audio.

| Value | Description |
|---|---|
| `Auto` | Follows the configured `Connection Type`: vision is enabled only when the room is already set to `Video`. Never upgrades an `Audio` room on its own. |
| `Enabled` | Always enables dynamic vision context; forces the room connection to `Video`. |
| `Disabled` | Never sends dynamic-vision config. The configured `Connection Type` is left untouched, so other video-dependent paths keep working. |

## `ConvaiVisionInputSettings`

Backend frame-sampling configuration for dynamic vision context, sent as `vision_input_config` on room connect. The client clamps values before serialization. This does not guarantee that the service accepts the configuration. These settings are read once at connect time — changing a sampling field requires a reconnect. Respond modes are the exception; see [`ConvaiVisionRespondModeSettings`](#convaivisionrespondmodesettings).

| Field | Wire field | Type | Default | Range |
|---|---|---|---|---|
| Frame Interval (s) | `sample_interval_secs` | `float` | `1` | 0.1–60 |
| Frames Per Reply | `frames_per_turn` | `int` | `5` | 1–20 |
| Frames Kept | `buffer_frames` | `int` | `0` (backend default = Frames Per Reply) | Frames Per Reply–120 when set |
| Custom Frame Spacing | `sampling_windows` | list | empty (uniform sampling at Frame Interval (s)) | see [Sampling windows](#sampling-windows) |
| Max Frame Age (s) | `staleness_seconds` | `float` | `10` | 0.1–120 |
| Max Image Size (px) | `max_resolution` | `int` | `0` (service-selected default) | 64–2048 when set |
| Replace Old Frames | `replace_previous_vision_context` | `bool` | `true` | — |

`Frame Interval (s)` is how often the backend grabs a frame into its buffer. `Frames Per Reply` is how many of those buffered frames get attached the next time the character produces a turn. `Frames Kept` is the size of the rolling buffer itself; leaving it at `0` sizes the buffer to `Frames Per Reply`. `Max Frame Age (s)` discards buffered frames older than this age at attach time. `Replace Old Frames` controls whether a new attach replaces the frames from the previous attach in context, instead of accumulating alongside them.

### Sampling windows

The Inspector shows **Custom Frame Spacing** rows as **N frames, M ms apart**, with **Add Window**. Its caption explains that zero-count or zero-spacing windows are skipped, and it warns when the total exceeds **Frames Per Reply**.

A sampling window picks a fixed count of frames spaced a fixed interval apart, so a project can combine dense recent motion with sparse older context — for example a `6`-frame window at `300` ms spacing plus a `6`-frame window at `1000` ms spacing (with `Frames Per Reply` set to at least `12`). When no window is configured, the backend samples uniformly at `Frame Interval (s)` instead.

Each window's `Count` and `Interval Ms` default to `0`, and a window is either fully configured or dropped entirely — there is no partial state. Setting only one of `Count` or `Interval Ms` leaves the window at `0` on the other field, and the SDK drops that window before sending `vision_input_config`; it never clamps a `0` ms interval up to the `1` ms floor. This matters because the request can ask for densely spaced frames, so a stray `1` ms window would request maximal capture load for the whole session. A window only reaches the backend when both `Count` (1–20) and `Interval Ms` (1–60000) are set.

If the total `Count` across configured windows exceeds `Frames Per Reply`, the SDK fills windows in order until the budget is used and trims the rest, logging a warning once, instead of sending a configuration the backend would reject.

## `ConvaiVisionRespondModeSettings`

The **When The Character Speaks Up** group contains per-lane respond-mode defaults sent as `respond_modes` on room connect. User text and voice always respond and cannot be lowered; only the four lanes below are configurable. Values use the same `ConvaiRespondMode` enum documented in [Dynamic context scripting API](../dynamic-context/dynamic-context-scripting-api.md#convairespondmode) — `Silent`, `Auto`, and `MustRespond` mean the same thing here as they do for dynamic context.

| Lane | Default | Governs |
|---|---|---|
| New Frames | `Silent` | How newly sampled vision frames affect speech |
| Context Updates | `Auto` | How a dynamic-context text update affects speech |
| Vision Triggers | `MustRespond` | The default behavior for an explicit vision trigger that doesn't set its own mode |
| Scene Metadata | `Silent` | How scene-metadata updates affect speech |

Use `UpdateRespondMode` to request a mid-session lane change. Check its boolean send result and the later acknowledgement; see [Vision scripting API](scripting-api.md).

## Next steps

{% content-ref url="how-vision-works.md" %}
[How vision works](how-vision-works.md)
{% endcontent-ref %}

{% content-ref url="../dynamic-context/dynamic-context-scripting-api.md" %}
[Dynamic context scripting API](../dynamic-context/dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Vision scripting API](scripting-api.md)
{% endcontent-ref %}
