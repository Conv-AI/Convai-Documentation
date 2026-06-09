---
title: Lip sync usage examples
description: "Configure lip sync for common scenarios: Add vs Override blending, tuning smoothing, mixing with body animation, and remapping blendshapes to a custom rig."
last_reviewed: 2026-06-05
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

A value of `0.4` produces smoother lip movement while remaining responsive. Decrease toward `0.1` for heavier smoothing with more lag; increase toward `1.0` for a faster response with less smoothing. The default of `1.0` is instant and applies no smoothing.

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

Some custom rigs split a single mouth movement into left and right target curves. For example, the MetaHuman source curve `CTRL_expressions_jawOpen` from Convai may need to drive two user-defined target curves on your custom rig.

In the `BlendshapeMapping` table on the AnimGraph node, add an entry:

| Key (`FName`) | `TargetNames` | `Multiplyer` | `Offset` |
|---|---|---|---|
| `CTRL_expressions_jawOpen` | `["InstructorJaw_L", "InstructorJaw_R"]` | `1.0` | `0.0` |

Both custom target curves receive the same value as the source `CTRL_expressions_jawOpen` curve.

### Scaling a curve down to prevent clipping

If a specific curve drives too much deformation on a particular mesh, add a mapping entry with a reduced `Multiplyer`:

| Key (`FName`) | `TargetNames` | `Multiplyer` | `Offset` |
|---|---|---|---|
| `CTRL_expressions_jawOpen` | `["CTRL_expressions_jawOpen"]` | `0.6` | `0.0` |

The target curve receives `60%` of the incoming value. The `GlobalMultiplier` still applies unless `IgnoreGlobalModifiers` is set to `true` on this entry.

### Pinning a curve to a fixed value

To prevent a specific curve from being driven by Convai at all — for example to keep the eyes fully open regardless of speech data — add a mapping entry with `UseOverrideValue = true`:

| Key (`FName`) | `TargetNames` | `UseOverrideValue` | `OverrideValue` |
|---|---|---|---|
| `CTRL_expressions_eyeBlinkL` | `["CTRL_expressions_eyeBlinkL"]` | `true` | `0.0` |

The curve is held at `0.0` regardless of incoming data.

## Recording and replaying a lip-sync sequence

### Capturing a response for cutscene playback

Use the recording API to capture a live lip-sync sequence during a conversation and replay it later — for example in a non-interactive cutscene or a pre-warmed response cache.

The recording API is C++ only. `StartRecordingLipSync`, `FinishRecordingLipSync`, `PlayRecordedLipSync`, `IsPlaying`, and `GetCurrentFrame` are plain C++ methods on `UConvaiFaceSyncComponent` with no `UFUNCTION` decoration.

```cpp
// pseudocode
UConvaiFaceSyncComponent* FaceSync = MyCharacter->FindComponentByClass<UConvaiFaceSyncComponent>();

// 1. Start recording before or at the start of the speech turn.
FaceSync->StartRecordingLipSync();

// 2. The character speaks — frames are captured automatically.

// 3. Stop recording when the turn ends and store the sequence.
FAnimationSequenceBP CachedSequence = FaceSync->FinishRecordingLipSync();

// 4. Replay the sequence when needed (e.g. on cutscene trigger).
//    Parameters: recorded sequence, start frame (0 = beginning),
//    end frame (-1 = end), overwrite duration (0.0 = use recorded duration).
FaceSync->PlayRecordedLipSync(CachedSequence, 0, -1, 0.0f);
```

{% hint style="info" %}
Use `IsPlaying()` to poll whether replay is active, and `GetCurrentFrame()` to read the live blendshape values for secondary systems such as audio-driven effects or lip sync debug overlays.
{% endhint %}

## Next steps

{% content-ref url="face-sync-anim-node-reference.md" %}
[Face Sync AnimGraph node reference](face-sync-anim-node-reference.md)
{% endcontent-ref %}

{% content-ref url="recording-lip-sync.md" %}
[Record and replay lip sync](recording-lip-sync.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot lip sync](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="how-lip-sync-works.md" %}
[How lip sync works](how-lip-sync-works.md)
{% endcontent-ref %}
