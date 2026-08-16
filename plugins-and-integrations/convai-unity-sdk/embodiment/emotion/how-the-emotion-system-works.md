---
title: How the emotion system works
description: Understand how Emotion resolves the emotion signal in Convai's response, smooths it, and composes the character's face and mood.
last_reviewed: "4.5.0"
---

`ConvaiEmotionController` turns the emotion signal Convai sends with its response into a smoothed, composited facial expression, and separately tracks the character's longer-lived resting mood. This page explains where that input comes from, how the controller resolves and smooths it, and how the result reaches the character's face.

***

## Where emotion's input comes from

Unlike Gaze, Body Animation, and Body Language, which decide everything from state already local to the scene — the dialogue state, the rig, nearby targets — Emotion's decisions are only partly local. Two things arrive from outside the character on every turn:

- **The transient emotion itself.** Convai emits it as part of its response: an emotion label and an intensity, chosen by whichever detection provider `EmotionDetectionMode` on `ConvaiEmotionController` requests. **Responsive** (`EmotionDetectionMode.Nrclex`, the default) reads the reply as it streams, so the face can change more than once within one reply. **Accurate** (`EmotionDetectionMode.Llm`) reads the finished reply once, arriving later but weighing meaning rather than wording — the better choice for a character speaking any language other than English. **Off** requests no signal at all; a character with no `ConvaiEmotionController` is treated as `Off` by default. This setting lives on the character in Unity — it decides which provider Convai runs, not a Convai console setting.
- **Mood commands.** When Convai's response includes a set-mood or reaction instruction, it reaches this character through `MoodCommandHandlerAdapter` — infrastructure Convai adds alongside `ConvaiEmotionController` automatically, never a component you add or configure yourself. The adapter calls the same `SetMood` and `SetEmotionOverride` methods your own gameplay code can call — see [Moods](moods.md).

Everything downstream of these two entry points — resolution, smoothing, blending, micro-expression life, and output — runs locally, the same as every other embodiment module.

***

## How the controller resolves and smooths a signal

An incoming label is resolved through the character's `EmotionTaxonomyAsset` first — canonical labels such as `joy` plus whatever server aliases the vocabulary defines. A label the taxonomy cannot resolve logs one warning and falls back to neutral.

The resolved label and intensity then feed an internal score accumulator that owns two separate, independently-read channels:

| Channel | Public surface | What it represents |
| --- | --- | --- |
| Transient emotion | `CurrentResolvedEmotion`, `CurrentNormalizedIntensity` | The character's reaction to the most recent line. Rises and decays with each incoming signal, and settles back toward the mood below once a reaction fades. |
| Mood | `CurrentMoodLabel`, `CurrentMoodScore` | What the character rests at between reactions — set by its personality's baseline or by `SetMood`, and persistent until something changes it. |

An active reaction never overwrites the mood, and the mood never appears as the active transient emotion — a character can visibly react with `surprise` while resting on a `joy` mood underneath. See [Moods](moods.md) for controlling the second channel from your own code.

Two additional settings shape the transient channel before it reaches the face: an optional short overshoot on arrival (micro-burst) that gives an expression a punchier entry, and optional blending, which lets a primary emotion show alongside related taxonomy complements (`joy` and `trust`, for example) instead of one emotion replacing another outright. Both are authored on `ConvaiEmotionProfile` — see [Emotion profile](emotion-profile.md).

***

## How expression reaches the face

Expression recipes name *what should move* in semantic terms — `MouthSmileLeft`, `BrowOuterUpRight`, and the rest — rather than naming blendshapes on one particular mesh. At runtime those semantics resolve against whichever blendshapes the character's own face actually has, through a curated lookup covering ARKit, Reallusion CC3, Reallusion CC4 Extended, and MetaHuman. One profile therefore drives any supported rig with no per-character authoring; a rig matching none of those conventions needs a `CustomRigConventionMap`.

Emotion does not write blendshapes directly. It submits its composed expression, and — when enabled — a continuous micro-expression life layer (idle drift plus a speech-emphasis accent), to the character's shared facial compositor, the same single writer LipSync and every other facial contributor submit to. See [Facial composition](../facial-composition.md) for how the compositor resolves overlapping claims on the same region, such as the mouth during speech.

Emotion can also drive arbitrary shader float properties — blush, tear glisten, sweat sheen — from composed scores through an optional material property binding, entirely independent of the blendshape path. See [Emotion output bindings](output-bindings.md).

***

## EmotionDimensions: the cross-module signal

Alongside its categorical label, every resolved emotion also carries continuous `EmotionDimensions` — `Valence`, `Arousal`, `Agency`, and `Approach`, each clamped to `[-1, 1]`. Categorical labels stay authoritative for authored facial recipes; the dimensions give Gaze, Body Language, and Body Animation one coherent modulation signal to read, instead of each module needing to know Emotion's taxonomy.

***

## Key concepts

| Concept | What it is |
| --- | --- |
| `ConvaiEmotionController` | The `MonoBehaviour` that owns the entire pipeline for one character. Add one per character. |
| `ConvaiEmotionProfile` | The `ScriptableObject` asset holding every tunable parameter: smoothing, micro-burst, blending, mood, and micro-expression life. |
| `EmotionTaxonomyAsset` | The `ScriptableObject` defining the emotion vocabulary — canonical labels, server aliases, and complements. The built-in default is Plutchik's nine emotions including neutral. |
| `MoodCommandHandlerAdapter` | Hidden infrastructure Convai adds alongside `ConvaiEmotionController` so a mood or reaction instruction in Convai's response can reach this character. Never authored directly. |
| `EmotionReading` | An immutable snapshot of the current state: dominant label and score, all scores, mouth influence, and the mood label and score. Available every frame via `ConvaiEmotionController.Current`. |
| `ConvaiCharacterEventRelay` | An Inspector-friendly component that exposes emotion and mood change callbacks as Unity Events — no code required. |

***

## Component placement

| Component | Where to place it | Notes |
| --- | --- | --- |
| `ConvaiEmotionController` | On the character's root `GameObject`, alongside the character's other embodiment modules | One per character |
| `ConvaiEmotionProfile` | Anywhere in your `Assets/` folder as a `ScriptableObject` asset | Shared across multiple characters if needed; Convai copies a package-shipped profile for you the first time you edit it on a shared character |
| `EmotionTaxonomyAsset` | Anywhere in your `Assets/` folder | Optional — omit to use the built-in Plutchik set |
| `MoodCommandHandlerAdapter` | Added automatically alongside `ConvaiEmotionController` | Never add or remove this yourself |
| `ConvaiCharacterEventRelay` | On any `GameObject` in the scene | Auto-resolves `ConvaiCharacter` on the same `GameObject`; drag a different character if needed |

***

## Next steps

{% content-ref url="quick-start.md" %}
[Emotion quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="moods.md" %}
[Moods](moods.md)
{% endcontent-ref %}

{% content-ref url="emotion-profile.md" %}
[Emotion profile](emotion-profile.md)
{% endcontent-ref %}
