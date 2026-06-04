---
title: Usage examples
description: "Configure lip sync for common scenarios: Add vs Override blending, tuning smoothing, mixing with body animation, and remapping blendshapes to a custom rig."
last_reviewed: 2026-06-03
---

These examples cover the most common `FAnimNode_ConvaiFaceSync` configurations. Each example describes the scenario, the node or component settings to change, and the expected result.

## Add vs Override blending

### Layering lip sync on top of an idle animation

Use `ApplyMode = Add` when a body or idle animation already drives some facial curves — for example, a subtle breathing animation that moves the jaw slightly. Convai values are added to whatever the source pose already contains, so both animations coexist.

In the AnimGraph node **Details** panel:

| Property | Value |
|---|---|
| `ApplyMode` | `Add` |

The source pose animation retains its facial curves, and Convai values are added on top.

### Making Convai the sole driver

Use `ApplyMode = Override` when Convai should own all animated curves and any idle facial animation would conflict — for example, a character whose idle uses brow curves that would fight with emotion data from Convai.

In the AnimGraph node **Details** panel:

| Property | Value |
|---|---|
| `ApplyMode` | `Override` |

The source pose curves are replaced entirely by the Convai frame values.

## Tuning smoothing

### Smoothing lip movement to reduce jitter

Speech blendshape data can produce rapid frame-to-frame changes that read as jitter on screen, especially on the lower face. Enable lower-face smoothing and set a moderate speed to even out the motion without creating noticeable lag.

In the AnimGraph node **Details** panel:

| Property | Value |
|---|---|
| `bEnableLowerFaceSmoothing` | `true` |
| `LowerFaceSmoothingSpeed` | `0.4` |

A value of `0.4` produces visibly smoother movement. Increase toward `1.0` for a faster, more responsive but less smooth result.

### Suppressing brow and eye movement

Speech data sometimes includes brow and eyelid motion that does not match the character's emotion or looks unnatural. Reduce `UpperFaceAlpha` to lower the contribution of upper-face curves without disabling them entirely.

In the AnimGraph node **Details** panel:

| Property | Value |
|---|---|
| `UpperFaceAlpha` | `0.2` |

Set `UpperFaceAlpha` to `0.0` to suppress upper-face blendshapes entirely while keeping full lip animation.

## Mixing with body animation

### Preserving body animation curves

When the Animation Blueprint chains body and face layers together, ensure the `Convai Face Sync` node is placed after the body layer node and before the final output. Use `ApplyMode = Add` so that any body-layer facial curves (for example, a blink track) are preserved.

The AnimGraph order should be:

1. Body animation node (produces the source pose with body and idle facial curves)
2. `Convai Face Sync` node (reads the source pose, adds Convai curves)
3. Output Pose

This order guarantees that idle blinks and other body-layer facial animation survive alongside Convai lip sync.

## Custom blendshape remapping

### Mapping one Convai curve to two rig curves

Some rigs split a single blendshape into left and right variants. For example, `jawOpen` from Convai may need to drive both `Jaw_L` and `Jaw_R` on a custom rig.

In the `BlendshapeMapping` table on the AnimGraph node, add an entry:

| Key (`FName`) | `TargetNames` | `Multiplyer` | `Offset` |
|---|---|---|---|
| `jawOpen` | `["Jaw_L", "Jaw_R"]` | `1.0` | `0.0` |

Both `Jaw_L` and `Jaw_R` receive the same value as the source `jawOpen` curve.

### Scaling a curve down to prevent clipping

If a specific curve drives too much deformation on a particular mesh, add a mapping entry with a reduced `Multiplyer`:

| Key (`FName`) | `TargetNames` | `Multiplyer` | `Offset` |
|---|---|---|---|
| `mouthOpen` | `["mouthOpen"]` | `0.6` | `0.0` |

The target curve receives `60%` of the incoming value. The `GlobalMultiplier` still applies unless `IgnoreGlobalModifiers` is set to `true` on this entry.

### Pinning a curve to a fixed value

To prevent a specific curve from being driven by Convai at all — for example to keep the eyes fully open regardless of speech data — add a mapping entry with `UseOverrideValue = true`:

| Key (`FName`) | `TargetNames` | `UseOverrideValue` | `OverrideValue` |
|---|---|---|---|
| `eyeBlink_L` | `["eyeBlink_L"]` | `true` | `0.0` |

The curve is held at `0.0` regardless of incoming data.

## Next steps

{% content-ref url="face-sync-anim-node-reference.md" %}
[Face Sync AnimGraph node reference](face-sync-anim-node-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
