---
description: >-
  Map each emotion to the specific facial shapes or Animator parameters on your
  character's rig, with per-slot weight and LipSync coordination.
---

# Output Bindings

## Driving Faces and Animators from Emotion Scores

Output bindings are the bridge between the Emotion system's smoothed score table and your character's visual representation. The SDK provides two binding types — `BlendshapeEmotionBinding` for direct mesh control and `AnimatorParameterEmotionBinding` for Mecanim-based rigs — and both can be active at the same time. Each binding is a list of `EmotionSlotBinding` entries, one per emotion per output channel, all authored inside the `ConvaiEmotionProfile` asset.

## EmotionSlotBinding Fields

Every slot in both binding types shares the same set of fields:

<table><thead><tr><th width="208">Field</th><th width="86.49993896484375">Type</th><th width="148.5">Range / Format</th><th width="96.5">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>emotionLabel</code></td><td><code>string</code></td><td>Canonical taxonomy label</td><td>—</td><td>The emotion this slot drives. Must match a label defined in the active taxonomy (e.g. <code>"joy"</code>, <code>"anger"</code>, <code>"neutral"</code>).</td></tr><tr><td><code>blendshapeNames</code></td><td><code>string</code></td><td>Comma- or newline-separated</td><td>—</td><td>One or more blendshape names on the character's <code>SkinnedMeshRenderer</code>. All listed shapes receive the same computed weight simultaneously. Used by <code>BlendshapeEmotionBinding</code> only.</td></tr><tr><td><code>animatorParameterName</code></td><td><code>string</code></td><td>Animator float parameter name</td><td>—</td><td>The name of a <code>float</code> parameter in the Animator Controller. Leave empty to skip Animator output for this slot. Used by <code>AnimatorParameterEmotionBinding</code> only.</td></tr><tr><td><code>weightMultiplier</code></td><td><code>float</code></td><td>0 – 2</td><td><strong>1</strong></td><td>Per-slot scaling factor applied to the score before it is written to the output. Values above 1 amplify the emotion's visual impact; values below 1 reduce it.</td></tr><tr><td><code>fullBlendshapeWeight</code></td><td><code>float</code></td><td>0 – 100</td><td><strong>100</strong></td><td>The blendshape value written when the emotion score reaches 1.0. Maps the SDK's normalised 0–1 range to Unity's 0–100 mesh units.</td></tr><tr><td><code>isMouthShape</code></td><td><code>bool</code></td><td>—</td><td><code>false</code></td><td>When true, this blendshape is treated as a mouth-region shape and routed through a separate compositor layer that LipSync can modulate.</td></tr></tbody></table>

## Blendshape Binding

`BlendshapeEmotionBinding` writes directly to a `SkinnedMeshRenderer`'s blendshapes each frame. It is the most direct path and requires no Animator Controller.

### Blendshape Name Format

The `blendshapeNames` field accepts a comma-separated or newline-separated list. All names in the list receive the same weight simultaneously, which is useful when a single emotional pose requires more than one blendshape — for example, a smile that activates both a lip-corner raise and a cheek puff:

```
Facial_LipCornerPull_L, Facial_LipCornerPull_R, Facial_CheekPuff
```

To find the correct names for your character: select the character's mesh in the Hierarchy, look at the **Skinned Mesh Renderer** component in the Inspector, and expand the **BlendShapes** section at the bottom. The names listed there are exactly what you enter in the slot.

### Weight Calculation

At each frame, the final blendshape value is calculated as:

`finalWeight = score × weightMultiplier × fullBlendshapeWeight`

Where `score` is the smoothed, burst-adjusted value from the accumulator (0–1). At default settings, a fully active emotion drives the blendshape to 100 (Unity mesh units).

### The `isMouthShape` Flag

{% hint style="warning" %}
Only set `isMouthShape = true` for blendshapes that deform the lips, jaw, or immediate mouth area. The Emotion system routes mouth-flagged shapes through the facial blendshape compositor, where the LipSync system can blend over them during speech. Flagging non-mouth shapes (brow raises, eye squints) as mouth shapes will cause those shapes to be incorrectly suppressed or modulated during speech playback.
{% endhint %}

## Animator Parameter Binding

`AnimatorParameterEmotionBinding` writes smoothed emotion scores as `float` parameters into an `Animator` component on the same GameObject. This is the right choice when your character uses a Mecanim rig where emotion-driven poses are authored as animation states or blend trees.

### Requirements

* The parameter name in each slot must match a **Float** parameter defined in the Animator Controller exactly (case-sensitive).
* The Animator component must be on the same GameObject as the `ConvaiEmotionController`, or reachable via the rig binding.

### Recommended Naming Convention

Using a consistent prefix makes parameters easy to identify in the Animator window and avoids collisions with other systems:

```
Emotion_Joy
Emotion_Anger
Emotion_Sadness
Emotion_Fear
Emotion_Surprise
```

{% hint style="info" %}
Both `BlendshapeEmotionBinding` and `AnimatorParameterEmotionBinding` can be populated at the same time. The system writes to both channels every frame, which is useful for rigs that combine direct blendshape control with Animator-driven secondary motion (cloth, hair, body lean).
{% endhint %}

## Pre-built Slots via RealisticEmotionSlots

If your character uses a Reallusion CC3, CC4, or ARKit-compatible rig, the SDK includes a factory that generates FACS-inspired slot lists covering all eight non-neutral emotions. These slots use multi-shape combinations (Duchenne smile, oblique frown, brow raises, etc.) that produce more believable expressions than single-blendshape mappings.

The factory is invoked from code — for example, from an Editor utility or a setup script:

```csharp
using Convai.Modules.Emotion.Authoring;
using Convai.Modules.Emotion.Outputs;
using Convai.Domain.Embodiment;

// Build a slot list for a CC4 Extended rig
IReadOnlyList<EmotionSlotBinding> slots = RealisticEmotionSlots.Build(RigConvention.ReallusionCC4Extended);

// Assign to the profile's blendshape binding at authoring time
myProfile.BlendshapeBinding.SetSlots(slots);
```

Supported `RigConvention` values:

<table><thead><tr><th width="246.5">Value</th><th>Description</th></tr></thead><tbody><tr><td><code>ReallusionCC4Extended</code></td><td>Reallusion Character Creator 4 Extended facial profile</td></tr><tr><td><code>ReallusionCC3</code></td><td>Reallusion Character Creator 3 base profile</td></tr><tr><td><code>ARKit</code></td><td>Apple's 52-blendshape ARKit convention</td></tr></tbody></table>

For any other rig, author your slots manually using the field reference above as a guide, referring to your rig's blendshape documentation for the correct shape names.

## Conclusion

Configured bindings close the loop between the AI's emotional signal and your character's face. Continue to Emotion Taxonomy to understand how server emotion labels are resolved to the canonical labels used in your slots, or jump to Scripting API if you need to read or override the current emotion state from code.
