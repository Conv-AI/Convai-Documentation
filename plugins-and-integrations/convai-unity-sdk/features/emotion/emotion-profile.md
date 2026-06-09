---
title: Emotion profile
description: Reference for ConvaiEmotionProfile, including smoothing speed, micro-burst settings, neutral alternation, and output binding configuration.
---

`ConvaiEmotionProfile` is the central configuration asset for the Emotion system. It controls how quickly expressions transition in and out, whether micro-expression bursts punctuate each new emotion, how neutral alternation prevents frozen faces during long turns, and which output bindings carry the scores to your character's mesh or Animator. Every parameter defaults to a value suitable for conversational NPC expression — start with the bundled sample and adjust from there.

## Create a profile asset

In the Project window, right-click inside your `Assets/` folder and choose:

**Create → Convai → Embodiment → Emotion Profile**

A new asset named `ConvaiEmotionProfile` appears. Rename it to something descriptive (for example, `NPC_Guard_EmotionProfile`) and assign it to the **Profile** field on the character's `ConvaiEmotionController` component.

{% hint style="info" %}
To get started without creating an asset, assign the bundled `ConvaiSamplesShared_EmotionProfile` from `Packages / Convai SDK for Unity / SamplesShared / Resources / Embodiment / Modules / Emotion`. Duplicate it first if you want to edit any values — assets inside the package are read-only.
{% endhint %}

## Taxonomy reference

| Field | Default | Description |
| --- | --- | --- |
| `taxonomy` | _(none — Plutchik built-in)_ | Optional `EmotionTaxonomyAsset` that defines which emotion labels are recognized and how Convai labels are resolved to canonical names. Leave empty to use the built-in nine-emotion Plutchik set. |

The taxonomy also provides per-emotion mouth influence hints used by the LipSync blending layer. See [Emotion taxonomy](emotion-taxonomy.md) for full details on the built-in set and how to create a custom one.

## Smoothing parameters

Emotion scores from the server are not applied instantly. The accumulator applies exponential smoothing on every frame so that expressions blend naturally rather than snapping between values.

| Field | Range | Default | Description |
| --- | --- | --- | --- |
| `lerpSpeed` | 0.1 – 20 | **5** | How quickly a score rises toward its target. Higher values feel snappier; lower values feel more languid. |
| `decaySpeed` | 0.1 – 20 | **2** | How quickly a score falls back toward zero once the target is removed. Decay is intentionally slower than rise by default, giving emotions time to linger naturally. |
| `intensityOffset` | -0.25 – 0.25 | **0** | A flat bias added to every normalised intensity value before it enters the accumulator. Positive values make all emotions appear stronger; negative values make them more subdued. |

**How exponential smoothing works:** Each frame, the current score moves a fraction of the remaining distance to the target. At `lerpSpeed = 5`, the score covers roughly 99% of that distance in about one second. Doubling the speed halves the time to reach full expression. Decay uses the same mechanism when the target drops to zero.

## Micro-expression burst

When a new emotion arrives, the accumulator can apply a brief overshoot — a short spike above the steady-state level — before settling. This gives expressions a punchy, naturalistic entry that reads much better on screen than a simple linear ramp.

| Field | Range | Default | Description |
| --- | --- | --- | --- |
| `microBurstEnabled` | — | **true** | Enable or disable the burst effect entirely. |
| `microBurstDuration` | 0.05 – 1.5 s | **0.25 s** | How long the overshoot envelope lasts before the score decays to its sustained value. |
| `microBurstOvershoot` | 1.0 – 3.0× | **1.4×** | Peak multiplier applied to the score at the apex of the burst. A value of 1.4 means the expression briefly reaches 40% above its sustained level. |
| `microBurstThreshold` | 0 – 1 | **0.15** | Minimum score delta required to trigger a burst. Small fluctuations below this threshold are smoothed without a burst, preventing jitter on subtle emotional shifts. |

{% hint style="info" %}
For calm, professional simulations, reduce `microBurstOvershoot` toward 1.1–1.2 or disable the burst entirely. For high-energy or dramatic characters, values up to 1.8 can be effective.
{% endhint %}

## Neutral alternation

A character that receives a sustained emotion signal, such as `interest` throughout a long explanation, can end up with a frozen expression that breaks immersion. Neutral alternation solves this by periodically fading the active expression toward neutral and then returning it, creating subtle variation even when the underlying emotion is constant.

| Field | Range | Default | Description |
| --- | --- | --- | --- |
| `neutralAlternationEnabled` | — | **true** | Enable or disable the alternation system. |
| `alternationMinInterval` | 0.5 – 30 s | **3 s** | Minimum time the current expression is held before a neutral dip begins. |
| `alternationMaxInterval` | 0.5 – 30 s | **7 s** | Maximum hold time. The actual interval is chosen randomly between min and max each cycle. |
| `alternationBlendDuration` | 0.05 – 5 s | **1 s** | How long the crossfade to neutral (and back) takes. Shorter values create clear, deliberate resets; longer values are almost imperceptible. |
| `alternateOnlyWhileTalking` | — | **false** | When enabled, alternation only occurs while the character is actively speaking. Useful if you want pauses between turns to hold the expression more stably. |

{% hint style="warning" %}
Setting `alternationMinInterval` and `alternationMaxInterval` to the same low value (for example, both at 1 s) will make the face appear to flicker rather than alternate naturally. Keep at least a 2–3 second spread between the two values, and keep the minimum above 2 s for most characters.
{% endhint %}

## Output bindings

The profile's **Blendshape Binding** and **Animator Binding** sections define which mesh blendshapes and Animator float parameters receive the smoothed emotion scores each frame. These are configured as lists of `EmotionSlotBinding` entries — one slot per emotion per output channel.

Full field definitions, rig-specific guidance, and the pre-built `RealisticEmotionSlots` factory are covered in [Emotion output bindings](output-bindings.md).

## Next steps

{% content-ref url="output-bindings.md" %}
[Emotion output bindings](output-bindings.md)
{% endcontent-ref %}

{% content-ref url="emotion-taxonomy.md" %}
[Emotion taxonomy](emotion-taxonomy.md)
{% endcontent-ref %}
