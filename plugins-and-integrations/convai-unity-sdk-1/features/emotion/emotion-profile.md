# Emotion Profile

### Tuning Emotional Behavior with ConvaiEmotionProfile

`ConvaiEmotionProfile` is the central configuration asset for the Emotion system. It controls how quickly expressions transition in and out, whether a short burst of intensity punctuates each new emotion, how the system prevents faces from freezing in a sustained pose, and which output bindings carry the scores to your character's mesh or Animator. Every parameter defaults to a value suitable for conversational NPC expression — start with the bundled sample and adjust from there.

### Creating a Profile Asset

In the Project window, right-click inside your `Assets/` folder and choose:

**Create → Convai → Embodiment → Emotion Profile**

A new asset named `ConvaiEmotionProfile` appears. Rename it to something descriptive (for example, `NPC_Guard_EmotionProfile`) and assign it to the **Profile** field on the character's `ConvaiEmotionController` component.

{% hint style="info" %}
To get started without creating an asset, assign the bundled `ConvaiSamplesShared_EmotionProfile` from `Packages / Convai SDK for Unity / SamplesShared / Resources / Embodiment / Modules / Emotion`. Duplicate it first if you want to edit any values — assets inside the package are read-only.
{% endhint %}

### Taxonomy Reference

| Field      | Default                      | Description                                                                                                                                                                                        |
| ---------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `taxonomy` | _(none — Plutchik built-in)_ | Optional `EmotionTaxonomyAsset` that defines which emotion labels are recognised and how server labels are resolved to canonical names. Leave empty to use the built-in nine-emotion Plutchik set. |

The taxonomy also provides per-emotion mouth influence hints used by the LipSync blending layer. See [Emotion Taxonomy](/broken/pages/d16937e3d6537821e2c4af08d397101d0111d1ee) for full details on the built-in set and how to create a custom one.

### Smoothing Parameters

Emotion scores from the server are not applied instantly. The accumulator applies exponential smoothing on every frame so that expressions blend naturally rather than snapping between values.

| Field             | Range        | Default | Description                                                                                                                                                                        |
| ----------------- | ------------ | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lerpSpeed`       | 0.1 – 20     | **5**   | How quickly a score rises toward its target. Higher values feel snappier; lower values feel more languid.                                                                          |
| `decaySpeed`      | 0.1 – 20     | **2**   | How quickly a score falls back toward zero once the target is removed. Decay is intentionally slower than rise by default, giving emotions time to linger naturally.               |
| `intensityOffset` | -0.25 – 0.25 | **0**   | A flat bias added to every normalised intensity value before it enters the accumulator. Positive values make all emotions appear stronger; negative values make them more subdued. |

**How exponential smoothing works:** Each frame, the current score moves a fraction of the remaining distance to the target. At `lerpSpeed = 5`, the score covers roughly 99% of that distance in about one second. Doubling the speed halves the time to reach full expression. Decay uses the same mechanism when the target drops to zero.

### Micro-Expression Burst

When a new emotion arrives, the accumulator can apply a brief overshoot — a short spike above the steady-state level — before settling. This gives expressions a punchy, naturalistic entry that reads much better on screen than a simple linear ramp.

| Field                 | Range        | Default    | Description                                                                                                                                                          |
| --------------------- | ------------ | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `microBurstEnabled`   | —            | **true**   | Enable or disable the burst effect entirely.                                                                                                                         |
| `microBurstDuration`  | 0.05 – 1.5 s | **0.25 s** | How long the overshoot envelope lasts before the score decays to its sustained value.                                                                                |
| `microBurstOvershoot` | 1.0 – 3.0×   | **1.4×**   | Peak multiplier applied to the score at the apex of the burst. A value of 1.4 means the expression briefly reaches 40% above its sustained level.                    |
| `microBurstThreshold` | 0 – 1        | **0.15**   | Minimum score delta required to trigger a burst. Small fluctuations below this threshold are smoothed without a burst, preventing jitter on subtle emotional shifts. |

{% hint style="info" %}
For calm, professional simulations, reduce `microBurstOvershoot` toward 1.1–1.2 or disable the burst entirely. For high-energy or dramatic characters, values up to 1.8 can be effective.
{% endhint %}

### Neutral Alternation

A character that receives a sustained emotion signal — for example, remaining "curious" throughout a long explanation — can end up with a frozen expression that breaks immersion. Neutral alternation solves this by periodically fading the active expression toward neutral and then returning it, creating subtle, lifelike variation even when the underlying emotion is constant.

| Field                       | Range      | Default   | Description                                                                                                                                                 |
| --------------------------- | ---------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `neutralAlternationEnabled` | —          | **true**  | Enable or disable the alternation system.                                                                                                                   |
| `alternationMinInterval`    | 0.5 – 30 s | **3 s**   | Minimum time the current expression is held before a neutral dip begins.                                                                                    |
| `alternationMaxInterval`    | 0.5 – 30 s | **7 s**   | Maximum hold time. The actual interval is chosen randomly between min and max each cycle.                                                                   |
| `alternationBlendDuration`  | 0.05 – 5 s | **1 s**   | How long the crossfade to neutral (and back) takes. Shorter values create clear, deliberate resets; longer values are almost imperceptible.                 |
| `alternateOnlyWhileTalking` | —          | **false** | When enabled, alternation only occurs while the character is actively speaking. Useful if you want pauses between turns to hold the expression more stably. |

{% hint style="warning" %}
Setting `alternationMinInterval` and `alternationMaxInterval` to the same low value (for example, both at 1 s) will make the face appear to flicker rather than alternate naturally. Keep at least a 2–3 second spread between the two values, and keep the minimum above 2 s for most characters.
{% endhint %}

### Output Bindings

The profile's **Blendshape Binding** and **Animator Binding** sections define which mesh blendshapes and Animator float parameters receive the smoothed emotion scores each frame. These are configured as lists of `EmotionSlotBinding` entries — one slot per emotion per output channel.

Full field definitions, rig-specific guidance, and the pre-built `RealisticEmotionSlots` factory are covered in [Output Bindings](/broken/pages/1e2b2eb9321a550a8ea8a49276a5aaad36013bb2).

### Conclusion

`ConvaiEmotionProfile` brings all smoothing, micro-burst, alternation, and output configuration into one portable asset that you can share across multiple NPC prefabs. Continue to [Output Bindings](/broken/pages/1e2b2eb9321a550a8ea8a49276a5aaad36013bb2) to wire the smoothed scores to your character's face, or see [Emotion Taxonomy](/broken/pages/d16937e3d6537821e2c4af08d397101d0111d1ee) to understand and customise the emotion vocabulary.

{% content-ref url="/broken/pages/1e2b2eb9321a550a8ea8a49276a5aaad36013bb2" %}
[Broken link](/broken/pages/1e2b2eb9321a550a8ea8a49276a5aaad36013bb2)
{% endcontent-ref %}

{% content-ref url="/broken/pages/d16937e3d6537821e2c4af08d397101d0111d1ee" %}
[Broken link](/broken/pages/d16937e3d6537821e2c4af08d397101d0111d1ee)
{% endcontent-ref %}
