---
title: Emotion output bindings
description: Reference for EmotionSlotBinding and the two binding types — field ranges, weight calculation, isMouthShape routing, and the pre-built slot factory.
---

Output bindings are the final stage of the Emotion pipeline. They receive the smoothed, burst-adjusted scores from the accumulator each frame and write them to your character's face. Two binding types are available: `BlendshapeEmotionBinding` for direct mesh deformation and `AnimatorParameterEmotionBinding` for Mecanim-driven rigs. Both can run simultaneously on the same character.

Both binding types are configured inside the `ConvaiEmotionProfile` asset — `BlendshapeEmotionBinding` in the **Blendshape Binding** section and `AnimatorParameterEmotionBinding` in the **Animator Binding** section. Each binding holds a list of `EmotionSlotBinding` entries, where each slot maps one canonical emotion label to one or more output targets.

## EmotionSlotBinding fields

Each slot in either binding type uses the same set of fields.

| Field | Type | Range | Default | Description |
| --- | --- | --- | --- | --- |
| `emotionLabel` | `string` | Canonical taxonomy label | — | The canonical label from the active taxonomy that this slot responds to (e.g. `"joy"`, `"anger"`). Must match a canonical label exactly — aliases do not resolve here. |
| `blendshapeNames` | `string` | Comma- or newline-separated | — | Names of blendshapes on the character's `SkinnedMeshRenderer` to drive. Leave empty to skip blendshape output for this slot. |
| `animatorParameterName` | `string` | Animator float parameter name | — | Name of a float parameter in the Animator Controller to write. Leave empty to skip Animator output for this slot. |
| `weightMultiplier` | `float` | 0 – 2 | **1** | Per-slot multiplier applied on top of the smoothed score. Use values above 1 to amplify subtle emotions, below 1 to restrain intense ones. |
| `fullBlendshapeWeight` | `float` | 0 – 100 | **100** | The blendshape value (in Unity's 0–100 mesh units) written when the smoothed score is exactly 1.0. |
| `isMouthShape` | `bool` | — | **false** | Routes this slot through the LipSync compositor's mouth layer. See [isMouthShape and LipSync routing](#ismouthshape-and-lipsync-routing) below. |

## Blendshape binding

`BlendshapeEmotionBinding` writes directly to one or more blendshapes on the character's `SkinnedMeshRenderer` each frame, without requiring an Animator Controller.

**Weight calculation:**

```text
finalBlendshapeWeight = score × weightMultiplier × fullBlendshapeWeight
```

Where `score` is the smoothed, burst-adjusted value in the range \[0, 1].

Multiple blendshape names can be listed in a single slot, separated by commas or newlines. All listed shapes receive the same computed weight:

```text
Brow_Raise_Inner_L, Brow_Raise_Inner_R
Eye_Wide_L, Eye_Wide_R
```

This is useful when an emotion symmetrically drives paired left/right shapes.

## Animator parameter binding

`AnimatorParameterEmotionBinding` writes the smoothed emotion score as a float parameter into the Animator Controller each frame. This is the right choice when your facial animation is driven by blend trees or state machines rather than direct blendshape control.

Requirements:

- The Animator Controller must define the parameter as a **Float** type.
- Parameter names are **case-sensitive**. The name in the slot must match the Animator Controller exactly.
- The Animator component must be on the **same GameObject** as `ConvaiEmotionController`.

The recommended naming convention for Animator parameters is `Emotion_<Label>` (e.g. `Emotion_Joy`, `Emotion_Anger`). This convention is used automatically by `RealisticEmotionSlots` when generating preset slot lists from code.

## isMouthShape and LipSync routing

The `isMouthShape` field controls whether a slot's output is routed through the mouth compositor layer — the same layer that LipSync writes phoneme shapes to during speech.

{% hint style="danger" %}
Set `isMouthShape = true` **only** for shapes that deform the lips, jaw, or chin. Brow raises, eye squints, cheek puffs, and all upper-face shapes must have `isMouthShape = false`.

Marking a non-mouth shape as `isMouthShape = true` routes it through the LipSync compositor, which suppresses or blends those shapes during speech. The result is upper-face animations (raised brows, wide eyes) that stop working while the character talks — a silent but clearly wrong visual that produces no console warning.
{% endhint %}

**When to use `isMouthShape = true`:**

| Shape category | `isMouthShape` |
| --- | --- |
| Lip corners, lip stretch, smile, frown | `true` |
| Jaw open, lip press, mouth dimple | `true` |
| Brow raise, brow drop, eye squint | `false` |
| Eye wide, eye blink | `false` |
| Cheek raise, cheek puff, nose sneer | `false` |

## Pre-built slot factory

For supported rigs, `RealisticEmotionSlots.Build(RigConvention rig)` generates a complete, FACS-inspired slot list covering all nine Plutchik emotions. This eliminates manual slot authoring for the supported character types.

**Supported rig conventions:**

| `RigConvention` | Description |
| --- | --- |
| `ReallusionCC4Extended` | Reallusion CC4 with the Extended facial profile. Richest slot set — uses per-side press, stretch, and upper-up shapes. |
| `ReallusionCC3` | Reallusion CC3 base profile. Same semantic coverage as CC4 Extended, using shapes available in the base profile. |
| `ARKit` | Apple's 52-blendshape convention. Uses camelCase naming (e.g. `mouthSmileLeft`, `browInnerUp`). |

Only `ReallusionCC4Extended`, `ReallusionCC3`, and `ARKit` are explicitly supported by the factory. For any other rig, author slots manually using the field table above.

{% hint style="info" %}
`RealisticEmotionSlots.Build()` is intended for programmatic profile creation and editor tooling. For Inspector-based authoring, fill slot entries directly in the profile asset. The bundled `ConvaiSamplesShared_EmotionProfile` was generated using the CC3 preset and can serve as a reference for custom slot configurations.
{% endhint %}

The factory is called on a profile in code as:

```csharp
using Convai.Modules.Emotion.Authoring;
using Convai.Domain.Embodiment.Semantics;

// Build an ARKit slot list
var slots = RealisticEmotionSlots.Build(RigConvention.ARKit);
blendshapeBinding.SetSlots(slots);
```

## Using both bindings together

Blendshape and Animator bindings can run simultaneously on the same character. A common pattern is to use blendshape binding for direct facial deformation and Animator binding to drive secondary motion (head tilt, shoulder shrug, body lean) via blend trees. Both bindings read from the same smoothed score table each frame, so they stay in sync.

Leave either binding's slot list empty to disable it — the controller skips any binding with no populated slots.

## Next steps

{% content-ref url="emotion-profile.md" %}
[Emotion profile](emotion-profile.md)
{% endcontent-ref %}

{% content-ref url="emotion-taxonomy.md" %}
[Emotion taxonomy](emotion-taxonomy.md)
{% endcontent-ref %}
