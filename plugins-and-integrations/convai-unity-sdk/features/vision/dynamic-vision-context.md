---
title: Dynamic vision context
description: Reference for the dynamic vision context types that configure backend-driven camera frame sampling and per-lane respond-mode defaults.
last_reviewed: "4.4.0"
---

Field-level reference for the three types that configure dynamic vision context: `ConvaiVisionContextMode` enables it per room, `ConvaiVisionInputSettings` tunes backend frame sampling, and `ConvaiVisionRespondModeSettings` sets per-lane respond-mode defaults. See [How vision works](how-vision-works.md#dynamic-vision-context) for what dynamic vision context is, why it exists, and how to enable it on a room.

{% hint style="info" %}
Dynamic vision context is an account-gated backend feature and requires a vision-capable non-realtime model (Gemini or GPT class). Confirm availability for the project before relying on it.
{% endhint %}

## `ConvaiVisionContextMode`

Controls whether a room opts into backend dynamic vision context.

| Value | Description |
|---|---|
| `Auto` | Follows the configured `Connection Type`: vision is enabled only when the room is already set to `Video`. Never upgrades an `Audio` room on its own. |
| `Enabled` | Always enables dynamic vision context; forces the room connection to `Video`. |
| `Disabled` | Never sends dynamic-vision config. The configured `Connection Type` is left untouched, so other video-dependent paths keep working. |

## `ConvaiVisionInputSettings`

Backend frame-sampling configuration for dynamic vision context, sent as `vision_input_config` on room connect. Every field is clamped into the backend's validated range, so an Inspector-authored configuration is never rejected at connect. These settings are read once at connect time — changing a sampling field requires a reconnect. Respond modes are the exception; see [`ConvaiVisionRespondModeSettings`](#convaivisionrespondmodesettings).

| Field | Wire field | Type | Default | Range |
|---|---|---|---|---|
| Sample Interval Seconds | `sample_interval_secs` | `float` | `1` | 0.1–60 |
| Frames Per Turn | `frames_per_turn` | `int` | `5` | 1–20 |
| Buffer Frames | `buffer_frames` | `int` | `0` (backend default = Frames Per Turn) | Frames Per Turn–120 when set |
| Sampling Windows | `sampling_windows` | list | empty (uniform sampling at Sample Interval Seconds) | see [Sampling windows](#sampling-windows) |
| Staleness Seconds | `staleness_seconds` | `float` | `10` | 0.1–120 |
| Max Resolution | `max_resolution` | `int` | `0` (provider default: Gemini 384 px, others 768 px) | 64–2048 when set |
| Replace Previous Vision Context | `replace_previous_vision_context` | `bool` | `true` | — |

`Sample Interval Seconds` is how often the backend grabs a frame into its buffer. `Frames Per Turn` is how many of those buffered frames get attached the next time the character produces a turn. `Buffer Frames` is the size of the rolling buffer itself; leaving it at `0` sizes the buffer to `Frames Per Turn`. `Staleness Seconds` discards buffered frames older than this age at attach time. `Replace Previous Vision Context` controls whether a new attach replaces the frames from the previous attach in context, instead of accumulating alongside them.

### Sampling windows

A sampling window picks a fixed count of frames spaced a fixed interval apart, so a project can combine dense recent motion with sparse older context — for example a `6`-frame window at `300` ms spacing plus a `6`-frame window at `1000` ms spacing (with `Frames Per Turn` set to at least `12`). When no window is configured, the backend samples uniformly at `Sample Interval Seconds` instead.

Each window's `Count` and `Interval Ms` default to `0`, and a window is either fully configured or dropped entirely — there is no partial state. Setting only one of `Count` or `Interval Ms` leaves the window at `0` on the other field, and the SDK drops that window before sending `vision_input_config`; it never clamps a `0` ms interval up to the `1` ms floor. This matters because the backend samples at the fastest configured window's interval, so a stray `1` ms window would request maximal capture load for the whole session. A window only reaches the backend when both `Count` (1–20) and `Interval Ms` (1–60000) are set.

If the total `Count` across configured windows exceeds `Frames Per Turn`, the SDK fills windows in order until the budget is used and trims the rest, logging a warning once, instead of sending a configuration the backend would reject.

## `ConvaiVisionRespondModeSettings`

Per-lane respond-mode defaults sent as `respond_modes` on room connect. User text and voice always respond and cannot be lowered; only the four lanes below are configurable. Values use the same `ConvaiRespondMode` enum documented in [Dynamic context scripting API](../dynamic-context/dynamic-context-scripting-api.md#convairespondmode) — `Silent`, `Auto`, and `MustRespond` mean the same thing here as they do for dynamic context.

| Lane | Default | Governs |
|---|---|---|
| Vision | `Silent` | How newly sampled vision frames affect speech |
| Context Update | `Auto` | How a dynamic-context text update affects speech |
| Trigger | `MustRespond` | The default behavior for an explicit vision trigger that doesn't set its own mode |
| Scene Metadata | `Silent` | How scene-metadata updates affect speech |

Respond modes can also be changed mid-session per lane without reconnecting; see [Dynamic context scripting API](../dynamic-context/dynamic-context-scripting-api.md) for the shared `ConvaiRespondMode` reference.

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
