---
title: How the emotion system works
description: >-
  Understand the emotion pipeline — how Convai sends emotion signals, how the
  SDK resolves and smooths them, and which components to place and where.
last_reviewed: 4.2.0
---

The Convai emotion system translates Convai emotion signals into live facial animation through a connect-time detection setting and a four-stage presentation pipeline. This page explains how each stage works, what the required components do, and where to place them in your scene.

## Detection source

`ConvaiCharacter` controls whether Unity asks Convai to stream emotion signals for a character session. The value is sent once when the room connection starts.

| `Detection Source` | Connect payload | Use when |
| ------------------ | --------------- | -------- |
| `Disabled`         | No `emotion_config` field is sent. | You do not need live emotion signals for this character. |
| `Llm`              | `emotion_config.provider = "llm"` | You want Convai to infer emotion from the AI response. This is the recommended first setup. |
| `Nrclex`           | `emotion_config.provider = "nrclex"` plus `min_word_threshold`, `low_intensity_threshold`, and `high_intensity_threshold` | You want NRCLex text analysis with tunable thresholds before the session connects. |

The `Nrclex` thresholds live on `ConvaiCharacter` under **EMOTION**. `Min Word Threshold` defaults to `3`, `Low Intensity Threshold` defaults to `0.33`, and `High Intensity Threshold` defaults to `0.66`.

## How the emotion pipeline works

After emotion detection is enabled, every emotion signal travels through four stages:

```mermaid
flowchart TD
    A([Convai]) -->|RTVI bot-emotion message\nemotion label + scale 1-3| B[RTVIBotEmotionMessage]
    B --> C[CharacterEmotionChanged\ndomain event]
    C --> D[ConvaiEmotionController]
    D --> E{Taxonomy\nresolution}
    E -->|alias → canonical label| F[EmotionScoreAccumulator\nsmoothing · micro-burst]
    F --> G[NeutralAlternator\nperiodic fade-to-neutral]
    G --> H{Output bindings}
    H --> I[BlendshapeEmotionBinding\nfacial blendshapes]
    H --> J[AnimatorParameterEmotionBinding\nAnimator float params]
    I & J --> K([EmotionReading\nread by your scripts])
```

Convai sends a short emotion label (for example `"happy"`) and an intensity on a `1`-`3` scale. `ConvaiCharacter` stores the raw label in `CurrentEmotion`, the raw scale in `CurrentEmotionIntensity`, and the normalized raw intensity in `CurrentEmotionNormalizedIntensity`. `ConvaiEmotionController` resolves the label to its canonical form (`"joy"`), normalizes the intensity, and hands it to the score accumulator, which applies exponential smoothing and an optional micro-expression burst. The neutral alternator periodically blends the expression back toward neutral to prevent a frozen face during long turns. The smoothed scores are then written to blendshapes and Animator parameters through configurable output bindings.

Use the raw `ConvaiCharacter` values for logging, UI, or tutorial overlays. Use `ConvaiEmotionController.Current`, `CurrentResolvedEmotion`, and `CurrentNormalizedIntensity` when you need the final value driving the face.

## Key concepts

| Concept                     | What it is                                                                                                                                                                                           |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ConvaiEmotionController`   | The MonoBehaviour that owns the entire pipeline for one NPC. Add one per character.                                                                                                                  |
| `ConvaiEmotionProfile`      | A ScriptableObject asset that holds every tunable parameter: smoothing, micro-burst, neutral alternation, and output slot definitions.                                                               |
| `EmotionTaxonomyAsset`      | A ScriptableObject that defines the emotion vocabulary — canonical labels, raw Convai aliases, and mouth influence hints. The built-in default is Plutchik's nine emotions including neutral.        |
| Output bindings             | `BlendshapeEmotionBinding` and `AnimatorParameterEmotionBinding` map each canonical emotion label to mesh blendshape names or Animator float parameters.                                             |
| `EmotionReading`            | An immutable snapshot of the current emotional state: dominant label, dominant score, all scores, and mouth influence hint for LipSync. Available every frame via `ConvaiEmotionController.Current`. |
| `RoomEmotionConfig`         | Connect request model serialized as `emotion_config`. `Llm` sends only `provider`; `Nrclex` sends `provider` and the three NRCLex thresholds.                                                        |
| Micro-burst                 | A short overshoot applied when a new emotion arrives, giving expressions a punchy entry before settling to their sustained level.                                                                    |
| Neutral alternation         | A timer that periodically fades the active expression toward neutral and back, preventing the character's face from locking into a single pose during long turns.                                    |
| `ConvaiCharacterEventRelay` | An Inspector-friendly component that exposes emotion change callbacks as Unity Events — no code required.                                                                                            |

## Component placement

| Component                   | Where to place it                                                | Notes                                                                                        |
| --------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `ConvaiEmotionController`   | On the NPC's root GameObject, alongside the Embodiment component | One per character                                                                            |
| `ConvaiEmotionProfile`      | Anywhere in your `Assets/` folder as a ScriptableObject asset    | Shared across multiple NPC prefabs if needed                                                 |
| `EmotionTaxonomyAsset`      | Anywhere in your `Assets/` folder                                | Optional — omit to use the built-in Plutchik set                                             |
| `ConvaiCharacterEventRelay` | On any GameObject in the scene                                   | Auto-resolves `ConvaiCharacter` on the same GameObject; drag a different character if needed |

## Next steps

{% content-ref url="quick-start.md" %}
[Emotion quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="emotion-profile.md" %}
[Emotion profile](emotion-profile.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}
