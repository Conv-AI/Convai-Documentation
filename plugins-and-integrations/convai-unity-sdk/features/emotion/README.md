---
description: >-
  How the Emotion system works, what each component does, and where to go next —
  the starting point for adding facial emotion to any Convai character.
---

# Emotion

## Giving Convai Characters Emotionally Responsive Faces

The Emotion system translates the Convai AI's internal emotional state into live facial animation — driving blendshapes, Animator parameters, or both simultaneously. Every time the backend decides the character feels joy, anger, surprise, or any other state, the Emotion system receives that signal, smooths it into a natural arc, and writes the result to your character's face in real time. The result is a character that reads as emotionally present rather than expressionless.

## How It Works

```mermaid
flowchart TD
    A([Convai Backend]) -->|RTVI bot-emotion message\nemotion label + scale 1–3| B[RTVIBotEmotionMessage]
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

The backend sends a short emotion label (for example `"happy"`) and an intensity on a 1–3 scale. The **taxonomy** resolves that label to its canonical form (`"joy"`), normalises the intensity to a 0–1 score, and hands it to the **score accumulator**, which applies exponential smoothing and an optional micro-expression burst. The **neutral alternator** then periodically blends the expression back toward neutral to prevent a frozen face. Finally, the smoothed scores are written to blendshapes and Animator parameters through configurable **output bindings**.

## Prerequisites

{% hint style="info" %}
Before adding the Emotion system to a character, ensure:

* Your character mesh has facial blendshapes, or your Animator Controller has float parameters you want to drive from emotion. The pipeline runs without these, but no visual output occurs until at least one output binding is configured.
{% endhint %}

## What Goes Where

| Component                   | Where to place it                                                    | Notes                                                                                        |
| --------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `ConvaiEmotionController`   | On the **NPC's root GameObject**, alongside the Embodiment component | One per character                                                                            |
| `ConvaiEmotionProfile`      | Anywhere in your `Assets/` folder as a ScriptableObject asset        | Shared across multiple NPC prefabs if needed                                                 |
| `EmotionTaxonomyAsset`      | Anywhere in your `Assets/` folder                                    | Optional — omit to use the built-in Plutchik set                                             |
| `ConvaiCharacterEventRelay` | On any GameObject in the scene                                       | Auto-resolves `ConvaiCharacter` on the same GameObject; drag a different character if needed |

## Key Concepts

<table><thead><tr><th width="267.5">Concept</th><th>What It Is</th></tr></thead><tbody><tr><td><code>ConvaiEmotionController</code></td><td>The MonoBehaviour that owns the entire pipeline for one NPC. Add one per character.</td></tr><tr><td><code>ConvaiEmotionProfile</code></td><td>A ScriptableObject asset that holds every tunable parameter: smoothing, micro-burst, neutral alternation, and output slot definitions.</td></tr><tr><td><code>EmotionTaxonomyAsset</code></td><td>A ScriptableObject that defines the emotion vocabulary — canonical labels, server aliases, and mouth influence hints. The built-in default is Plutchik's eight primary emotions plus neutral.</td></tr><tr><td><code>Output bindings</code></td><td><code>BlendshapeEmotionBinding</code> and <code>AnimatorParameterEmotionBinding</code> map each canonical emotion label to mesh blendshape names or Animator float parameters.</td></tr><tr><td><code>EmotionReading</code></td><td>An immutable snapshot of the current emotional state: dominant label, dominant score, all scores, and mouth influence hint for LipSync. Available every frame via <code>ConvaiEmotionController.Current</code>.</td></tr><tr><td><code>Micro-burst</code></td><td>A short overshoot applied when a new emotion arrives, giving expressions a punchy entry before settling to their sustained level.</td></tr><tr><td><code>Neutral alternation</code></td><td>A timer that periodically fades the active expression toward neutral and back, preventing the character's face from locking into a single pose during long turns.</td></tr><tr><td><code>ConvaiCharacterEventRelay</code></td><td>An Inspector-friendly component that exposes emotion change callbacks as Unity Events — no code required.</td></tr></tbody></table>

## In This Section

<table data-view="cards"><thead><tr><th></th><th></th></tr></thead><tbody><tr><td><strong>Quick Start</strong></td><td>Attach the Emotion Controller, assign the bundled profile, and get your NPC reacting emotionally to conversation — no custom assets required.</td></tr><tr><td><strong>Emotion Profile</strong></td><td>Configure smoothing speed, micro-expression bursts, neutral alternation, and output bindings in one portable asset.</td></tr><tr><td><strong>Output Bindings</strong></td><td>Map smoothed emotion scores to facial blendshapes and Animator float parameters, with per-slot weight and LipSync control.</td></tr><tr><td><strong>Emotion Taxonomy</strong></td><td>Understand the built-in Plutchik vocabulary, how server aliases are resolved, and how to author a custom taxonomy.</td></tr><tr><td><strong>Scripting API</strong></td><td>Read live emotion state, inject overrides, lock expressions, and react to emotion events — from Inspector relays to typed C# subscriptions.</td></tr><tr><td><strong>Usage Examples</strong></td><td>Complete scenarios covering hazard triggers, locked greetings, distress branching, analytics logging, and Editor debugging.</td></tr><tr><td><strong>Troubleshooting &#x26; Diagnostics</strong></td><td>Step-by-step fixes for the most common problems — from expressions that will not move to LipSync conflicts and production build gotchas.</td></tr></tbody></table>

## Conclusion

The Emotion system gives Convai characters a believable emotional presence — server-driven, smoothed, and fully configurable without writing code for the common case. Start with Quick Start to get a character reacting live, then use the deeper configuration pages to tune the behaviour for your specific rig and scenario.
