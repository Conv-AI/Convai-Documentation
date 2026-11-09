---
title: Emotion profile
description: Every setting on a character emotion profile, covering resting mood, drift, contagion, blending, and the micro-expression life that keeps a face alive.
last_reviewed: "5.0.0-preview"
---

`ConvaiEmotionProfile` is the authoring asset for the Emotion module. It controls how quickly expressions transition, whether a character rests on a mood between server signals, how many emotions can show at once, and the optional shader output for effects such as blush or tears. Facial expression itself needs no per-rig authoring on this asset — the profile's expression recipes are resolved automatically against the character's rig. Start from a character type and adjust it. The defaults below describe a newly created blank asset; applying a character type replaces its personality values. With **Personality** empty, runtime uses a hidden Composed profile resting at `trust` with strength `0.45`.

## Create a profile asset

In the Project window, right-click inside your `Assets/` folder and choose:

**Create → Convai → Embodiment → Emotion Profile**

A new asset named `ConvaiEmotionProfile` appears. Rename it to something descriptive (for example, `NPC_Guard_EmotionProfile`) and assign it to the **Personality** field on the character's `ConvaiEmotionController` component.

## Character type presets

`ConvaiEmotionProfile.CreatePreset(CharacterDemeanor demeanor, EmotionTaxonomyAsset taxonomy)` builds a complete profile from one of four starting temperaments. The Inspector's **Character Type** row on a new profile writes the same table with one click.

| `CharacterDemeanor` | Rests at | Reads as |
| --- | --- | --- |
| `Reserved` | *(nothing)* | A guard or an officiant — shows as little as possible. |
| `Composed` | `trust` at `0.45` | A receptionist or clerk — civil, closed-lip. |
| `Warm` | `joy` at `0.55` | The default character type — visibly approachable. |
| `Energetic` | `joy` at `0.6` | A host or tour guide — openly cheerful. |

`CharacterDemeanor` is the same personality vocabulary shared by Gaze, Body Animation, and Body Language. When a scene needs one asset that carries a matching temperament across every module a character uses, bundle the per-module profiles into a single asset — see [Embodiment presets](../embodiment-presets.md).

Applying a character type does not touch the emotion vocabulary, the expression recipes, or the material output binding — those stay as authored. Changing a value the type owns after applying it does not clear the type label; the Inspector shows **Custom** instead and offers to reapply the type.

## Emotion vocabulary

| Serialized field | Inspector label | Default | Description |
| --- | --- | --- | --- |
| `taxonomy` | **Emotion Vocabulary** | _(none — built-in Plutchik set)_ | Optional `EmotionTaxonomyAsset` that defines which emotion labels this character recognizes and how server labels resolve to canonical names. Leave empty to use the built-in nine-emotion set. |

See [Emotion taxonomy](emotion-taxonomy.md) for the built-in set, alias resolution, and custom taxonomy authoring. The profile Inspector's **Unknown emotions** diagnostics identify unresolved authored labels and suggest known ones; fix the label or vocabulary before testing.

## Response speed and micro-burst

These controls appear under **Personality** and **Reactions** in the Inspector.

Emotion scores from Convai are not applied instantly. The accumulator smooths every frame so expressions blend naturally rather than snapping between values, and can apply a brief overshoot as a new emotion lands.

| Serialized field | Inspector label | Range | Default | Description |
| --- | --- | --- | --- | --- |
| `lerpSpeed` | **How Fast Emotions Appear** | 0.1 – 20 | **5** | How quickly a score rises toward its target. Higher values feel snappier; lower values feel more languid. |
| `decaySpeed` | **How Fast Emotions Fade** | 0.1 – 20 | **2** | How quickly a score falls back toward its resting value once the target is removed. |
| `intensityOffset` | **How Strongly It Shows** | -0.25 – 0.25 | **0** | A flat bias added to every normalized intensity value before it enters the accumulator. |
| `prosodyCoupling` | **Follow Voice Energy** | 0 – 1 | **0** | While the character speaks, expression intensity subtly follows the live speech-energy envelope — brighter on emphatic delivery, softer in lulls. `0` disables the effect; at `1` the effective intensity gain ranges `[0.85, 1.15]`. Only applies while speaking. |
| `microBurstEnabled` | **Extra Kick On New Emotion** | — | **true** | Whether a new emotion briefly overshoots before settling to its steady-state score. |
| `microBurstDuration` | **Kick Length** | 0.05 – 1.5 s | **0.25 s** | How long the overshoot lasts before the score decays to its sustained value. |
| `microBurstOvershoot` | **Kick Strength** | 1.0 – 3.0× | **1.4×** | Peak multiplier at the apex of the burst. |
| `microBurstThreshold` | **Minimum Change To Kick** | 0 – 1 | **0.15** | Minimum score delta required to trigger a burst. Smaller fluctuations settle without one. |

## Resting mood (persona baseline)

Inspector section: **Resting Mood**.

A blank asset has no resting mood. Character types and the hidden Composed runtime default set their own baseline. These fields optionally give it a resting mood it settles toward instead.

| Serialized field | Inspector label | Range | Default | Description |
| --- | --- | --- | --- | --- |
| `baselineEmotionLabel` | **Resting Mood** | Canonical taxonomy label | _(empty — no baseline)_ | The resting mood's canonical label (for example `joy`). Empty or `neutral` means no baseline. |
| `baselineIntensity` | **Resting Mood Strength** | 0 – 1 | **0** | Resting strength of the mood. `0` disables the resting mood entirely. |

Baseline intensity drives the smile blendshapes directly, so calibrate by eye: `0.2` is measurable but nearly invisible, `0.45`–`0.6` reads as friendly, and above `0.7` starts to read as a fixed grin. `ConvaiEmotionController.CurrentMoodLabel`/`CurrentMoodScore` report the resolved resting mood; an active baseline never appears as the character's dominant (transient) emotion. `ConvaiEmotionController` also exposes a **This character rests at** per-character override on the component itself, and `SetMood`/`ClearMood` change the resting mood at runtime — see [Emotion scripting API](scripting-api.md).

### Per-emotion overrides

Inspector section: **Per-Emotion Tuning**.

| Serialized field | Inspector label | Range | Default | Description |
| --- | --- | --- | --- | --- |
| `expressiveness` | **Per-Emotion Strength** | Gain 0 – 2 per label | _(empty)_ | `EmotionExpressivenessEntry` list. Applies a per-label score gain to incoming server intensities, before smoothing — for example `joy` gain `> 1` to make a character smile easily. Labels not listed default to gain `1`. Never applied to the resting baseline. |
| `emotionDynamics` | **Per-Emotion Timing** | Attack/decay 0.1 – 20 per label | _(empty)_ | `EmotionDynamicsEntry` list. Overrides `lerpSpeed`/`decaySpeed` for a single label — for example anger that snaps on and sadness that creeps in and lingers. Labels not listed use the profile's global speeds. |

## Mood drift

These fields are also under **Resting Mood**.

An optional, fully automatic channel: sustained conversational emotions slowly tint the resting mood on their own, so mood feels earned by the conversation rather than only ever set through code.

| Serialized field | Inspector label | Range | Default | Description |
| --- | --- | --- | --- | --- |
| `moodDriftEnabled` | **Mood Follows Conversation** | — | **false** | Whether the resting mood follows the conversation. Off means the drift channel never advances. |
| `moodDriftRate` | **How Quickly Mood Shifts** | 0.001 – 0.5 | **0.02** | Exponential rate/s the drift intensity approaches its target while a dominant transient sustains it. |
| `moodRecoveryRate` | **How Long Mood Lingers** | 0.001 – 1 | **0.05** | Exponential rate/s drift decays back toward `0` once the sustaining transient fades or changes label. |
| `moodDriftMaxIntensity` | **How Far Mood Can Shift** | 0 – 1 | **0.25** | Hard cap on drift intensity, regardless of how strong or long the sustaining transient runs. |

Drift never appears via `CurrentResolvedEmotion`/`DominantLabel`. It contributes to `CurrentMoodLabel`/`CurrentMoodScore` alongside the persona baseline and any runtime `SetMood` override; ties favor the explicit anchor over drift. A session reset always clears drift.

## Emotional contagion

Inspector section: **Other Characters**.

An optional low-intensity, capped facial echo of a nearby other Convai character's strong dominant emotion.

| Serialized field | Inspector label | Range | Default | Description |
| --- | --- | --- | --- | --- |
| `contagionEnabled` | **Picks Up Others' Moods** | — | **false** | Whether this character picks up nearby emotions at all. Every character with a `ConvaiEmotionController` is witnessable regardless of this setting; only the receiving character's own setting decides whether it reacts. |
| `contagionStrength` | **How Strongly** | 0 – 1 | **0.3** | How much of a witnessed emotion carries over, before distance falloff and the intensity cap. |
| `contagionRadius` | **Within This Distance** | 0.5 – 20 m | **4 m** | Maximum distance at which another character's emotion can be witnessed. Falls off linearly to `0` at this radius. |
| `contagionMaxIntensity` | **Never Stronger Than** | 0 – 1 | **0.2** | Hard cap on the echoed intensity. |

The echo folds into the rendered face only. It never appears via `CurrentResolvedEmotion`/`DominantLabel` or `CurrentMoodLabel`/`CurrentMoodScore`, and it is cleared on a session reset.

## Emotion blending

Inspector section: **Mixing Emotions**.

With blending off, the transient (server-driven) state is winner-takes-all: one non-neutral emotion at a time. With blending on, a character can express a primary emotion plus related taxonomy complements at once, with hysteresis so noisy or rapidly alternating server labels do not make the face flicker.

| Serialized field | Inspector label | Range | Default | Description |
| --- | --- | --- | --- | --- |
| `enableEmotionBlending` | **Show Mixed Emotions** | — | **true** | Whether more than one emotion can show at once. |
| `emotionSwitchDwell` | **Hold Before Switching** | 0 – 2 s | **0.35 s** | Minimum time the current primary emotion is protected before a weaker new label may replace it. |
| `emotionSwitchMargin` | **Cut In If Stronger By** | 0 – 1 | **0.15** | A new label bypasses the dwell if its score exceeds the current primary's by at least this margin. |
| `complementBlendScale` | **Secondary Emotion Strength** | 0 – 1 | **0.35** | Weight of a co-occurring taxonomy complement relative to the primary emotion's score. |
| `maxSimultaneousEmotions` | **Most Emotions At Once** | 1 – 4 | **2** | Hard cap on how many transient emotions, primary plus complements, can be non-zero at once. |

Complements are authored per label on the taxonomy (`EmotionTaxonomyEntry.Complements`); the built-in taxonomy pairs `joy` and `trust`.

## Micro-expression life

Inspector section: **Small Movements**.

A perfectly still expression reads as frozen even with smoothing and a resting mood active. This optional low-amplitude layer adds idle brow/cheek/eye drift plus a brow-raise accent on speech emphasis, so the face keeps a trace of movement.

| Serialized field | Inspector label | Range | Default | Description |
| --- | --- | --- | --- | --- |
| `microExpressionsEnabled` | **Never Sits Perfectly Still** | — | **true** | Whether the layer runs at all. Off means the director and its compositor submission are never created. |
| `microExpressionAmplitude` | **How Much Movement** | 0 – 1 | **0.15** | Idle-drift amplitude. |
| `speechAccentStrength` | **Brow Accent While Speaking** | 0 – 1 | **0.3** | Strength of the brow-raise accent triggered by rising speech energy. |
| `microExpressionStillness` | **How Settled** | 0 – 1 | **0.5** | In this preview's runtime, `0` removes idle drift and `1` uses the full authored amplitude. This runs opposite to the **How Settled** tooltip; tune while watching the face in Play mode. |
| `listeningReactionStrength` | **Attentive While Listening** | 0 – 1 | **0** | Sustained attentive brow/squint lift while the player is speaking. `0` disables it. Needs the Conversation Flow module. |
| `thinkingReactionStrength` | **Concentrating While Thinking** | 0 – 1 | **0** | Sustained concentration look during the pause before the character replies. `0` disables it. Needs the Conversation Flow module. |
| `reactingAccentStrength` | **Reaction Flash** | 0 – 1 | **0** | One-shot brow flash on entering the `Reacting` dialogue state. `0` disables it. |
| `interruptedFlinchStrength` | **Flinch When Interrupted** | 0 – 1 | **0** | One-shot flinch on entering the `Interrupted` dialogue state. `0` disables it. |

Idle drift is deterministic per character and biased by the current dominant emotion or, when stronger, the current resting mood.

All four character types set these reaction strengths above zero; the blank asset defaults in the table do not describe those presets. The reactions need **Never Sits Perfectly Still** enabled, as well as Conversation Flow. If disabled, use **Keep The Face Alive** on the **Conversation reactions will never show** finding.

Raising any of the four dialogue-reaction strengths above `0` asks Convai to add a Conversation Flow controller automatically if the character has none — see [Conversation Flow is added automatically when needed](how-the-emotion-system-works.md#conversation-flow-is-added-automatically-when-needed).

## Expression recipes and output

Inspector section: **Expressions**.

| Serialized field | Inspector label | Default | Description |
| --- | --- | --- | --- |
| `expressionRecipes` | **Expression Recipes** | _(empty — built-in library)_ | `EmotionExpressionRecipe` list. Names what should move in semantic terms rather than by blendshape name, so one profile drives any supported rig. An empty list uses Convai's production-safe defaults for all nine built-in emotions. |
| `materialBinding` | **Material Effects** | _(empty)_ | A `MaterialPropertyEmotionBinding` for shader effects such as blush, tears, or sweat sheen. Empty drives no shader properties. |

Facial expression itself is written through the shared facial compositor rather than through an authored slot list — see [Facial composition](../facial-composition.md). Full field definitions for the material output and how it composes with other shader writers are in [Emotion output bindings](output-bindings.md).

## Next steps

{% content-ref url="output-bindings.md" %}
[Emotion output bindings](output-bindings.md)
{% endcontent-ref %}

{% content-ref url="emotion-taxonomy.md" %}
[Emotion taxonomy](emotion-taxonomy.md)
{% endcontent-ref %}
