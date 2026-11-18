---
title: Facial composition
description: Reference for the facial composition profile, including per-region blend configuration, blend modes, and layer priority.
last_reviewed: "4.5.0"
---

`ConvaiFacialCompositionProfile` is a `ScriptableObject` asset that configures how much of a character's face Emotion, LipSync, and a reserved Custom channel each control while idle and while speaking. Convai classifies every facial blendshape into one of six regions and composes each region's final weight from this profile before writing it to the character's face mesh.

## `ConvaiFacialCompositionProfile`

`ScriptableObject` — `Convai.Runtime.Animation`

Create menu: `Assets > Create > Convai > Embodiment > Facial Composition Profile`

### Properties

| Property | Type | Description |
|---|---|---|
| `SpeechRampUpDuration` | `float` | Seconds to ramp the speech blend factor from `0` to `1` when speech starts. Default `0.15`. Minimum `0.01`. |
| `SpeechRampDownDuration` | `float` | Seconds to ramp the speech blend factor from `1` to `0` when speech ends. Default `0.4`. Minimum `0.01`. |
| `EnableGlobalNormalization` | `bool` | When enabled, composed values exceeding 100 are clamped after all layers contribute. Default `false`. |
| `MouthConfig`, `BrowConfig`, `EyeConfig`, `CheekConfig`, `JawConfig`, `OtherConfig` | `RegionBlendConfig` | Read-only access to each region's blend configuration. |

### Methods

| Method | Signature | Description |
|---|---|---|
| `GetRegionConfig` | `RegionBlendConfig GetRegionConfig(FacialBlendshapeRegion region)` | Returns the blend configuration for a facial region. |
| `ClassifyBlendshape` | `FacialBlendshapeRegion ClassifyBlendshape(string blendshapeName)` | Classifies a blendshape name into a region using the profile's configured name patterns. Matching ignores case and separators, so `Jaw_Open` also matches `jawOpen`. |
| `CreateDefault` | `static ConvaiFacialCompositionProfile CreateDefault()` | Creates an instance with the shipped default values. Used internally when no profile is assigned; the caller owns and must destroy the returned instance. |

## Facial regions

Every blendshape is classified into exactly one of six regions. Classification checks Mouth, then Jaw, then Brow, then Eye, then Cheek, in that order; a blendshape that matches none of those patterns falls into Other.

| Region | Default name patterns | Typical content |
|---|---|---|
| `Mouth` | `Mouth`, `Lip`, `Tongue`, `Jaw_Open` | Lip, tongue, and mouth-corner shapes, driven primarily by lip sync during speech |
| `Jaw` | `Jaw_Forward`, `Jaw_Backward`, `Jaw_L`, `Jaw_R`, `Jaw_Up`, `Jaw_Down` | Directional jaw shapes, separate from Mouth |
| `Brow` | `Brow`, `Forehead` | Brow and forehead shapes |
| `Eye` | `Eye_Blink`, `Eye_Squint`, `Eye_Wide`, `Eye_Look`, `Eye_L_Look`, `Eye_R_Look`, `Eyelash` | Blink, squint, wide-eye, look, and eyelash shapes |
| `Cheek` | `Cheek`, `Nose`, `Sneer` | Cheek puff, cheek squint, and nose sneer shapes |
| `Other` | None (fallback) | Any blendshape that matches no configured pattern |

Each pattern list is a semicolon-separated string field on the profile (`Mouth Patterns`, `Jaw Patterns`, `Brow Patterns`, `Eye Patterns`, `Cheek Patterns`), editable per project. Mesh discovery uses a separate set of name patterns (`Head Mesh Patterns`, `Secondary Mesh Patterns`, `Tertiary Mesh Patterns`) to prioritize which `SkinnedMeshRenderer` blendshapes resolve from first.

## Per-region composition

`RegionBlendConfig` — `Convai.Runtime.Animation`, serializable struct

Each region has its own `RegionBlendConfig` with six weights (`0`–`1`) and a `FacialBlendMode`. Weights interpolate between `Idle*` and `Speaking*` values using the smoothed speech blend factor.

| Field | Type | Description |
|---|---|---|
| `IdleEmotionWeight` | `float` | Emotion layer weight while not speaking |
| `IdleLipSyncWeight` | `float` | LipSync layer weight while not speaking |
| `IdleCustomWeight` | `float` | Custom layer weight while not speaking |
| `SpeakingEmotionWeight` | `float` | Emotion layer weight while speaking |
| `SpeakingLipSyncWeight` | `float` | LipSync layer weight while speaking |
| `SpeakingCustomWeight` | `float` | Custom layer weight while speaking |
| `Mode` | `FacialBlendMode` | How the three layers combine within this region. Default `WeightedAdditive`. |
| `EnableNormalization` | `bool` | When enabled, this region's composed result is clamped to 100 and excess is proportionally reduced. |

### Default region weights

| Region | Idle Emotion | Idle LipSync | Speaking Emotion | Speaking LipSync |
|---|---|---|---|---|
| Mouth | `1.0` | `0.0` | `0.2` | `1.0` |
| Brow | `1.0` | `0.0` | `0.85` | `0.15` |
| Eye | `0.8` | `0.0` | `0.7` | `0.1` |
| Cheek | `1.0` | `0.0` | `0.7` | `0.25` |
| Jaw | `0.5` | `0.0` | `0.1` | `1.0` |
| Other | `1.0` | `0.0` | `0.8` | `0.3` |

`IdleCustomWeight` and `SpeakingCustomWeight` default to `0.0` for every region. `Mode` defaults to `WeightedAdditive` for every region.

## Blend modes

`FacialBlendMode` — `Convai.Runtime.Animation`

| Value | Integer | Description |
|---|---|---|
| `WeightedAdditive` | `0` | Each layer's value is multiplied by its interpolated weight and summed, then clamped to 0–100. Preserves subtle contributions from multiple sources. Default. |
| `Max` | `1` | Each layer's value is multiplied by its interpolated weight; the largest result wins. |
| `Override` | `2` | The highest-priority non-zero layer value, scaled by its weight, takes full control. Priority order: LipSync, then Emotion, then Custom. |

## Assign an override profile

Convai's auto-added character context resolves a built-in default profile with the values above when no profile is assigned. To rebalance composition or classify blendshapes with unusual names, assign a `ConvaiFacialCompositionProfile` asset to the **Face Blending Override** field under the **Advanced** section of that context's Inspector.

{% hint style="info" %}
If a profile is explicitly assigned as `null`, the compositing behavior degrades to a max-blend fallback across all active layers and logs a one-time warning. This only happens when a profile has been deliberately cleared — Convai supplies a built-in default otherwise.
{% endhint %}

## Related reference

{% content-ref url="character-rig-setup.md" %}
[Character rig setup](character-rig-setup.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Embodiment scripting reference](scripting-reference.md)
{% endcontent-ref %}
