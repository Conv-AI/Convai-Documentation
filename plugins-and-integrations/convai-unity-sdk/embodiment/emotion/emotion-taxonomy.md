---
title: Emotion taxonomy
description: Reference for EmotionTaxonomyAsset, including the built-in emotion set, server alias resolution, and custom taxonomy authoring.
last_reviewed: "4.5.0"
---

The taxonomy translates Convai's raw emotion strings into the canonical labels the rest of the Emotion module uses. When Convai sends `"happy"`, the taxonomy resolves that alias to `"joy"` so that the accumulator and expression pipeline — which are keyed on canonical labels — know exactly which score to update. The SDK ships with a nine-emotion Plutchik-inspired default; author a custom `EmotionTaxonomyAsset` when you need a different vocabulary or additional server aliases.

## Built-in taxonomy

When the `taxonomy` field on a `ConvaiEmotionProfile` is left empty, the system synthesizes the following set at runtime. This default covers every emotion Convai currently produces and requires no asset to be created.

| Canonical label | Server aliases | Default mouth influence |
| --- | --- | --- |
| `neutral` | `calm`, `idle` | 0.0 |
| `joy` | `happy`, `happiness`, `ecstasy`, `serenity`, `excited`, `enthusiastic` | 0.6 |
| `trust` | `acceptance`, `admiration`, `confident`, `reassured` | 0.3 |
| `fear` | `afraid`, `apprehension`, `terror`, `fearful`, `worried`, `anxious`, `nervous` | 0.4 |
| `surprise` | `amazement`, `distraction`, `surprised` | 0.5 |
| `sadness` | `sad`, `pensiveness`, `grief` | 0.3 |
| `disgust` | `disgusted`, `loathing`, `boredom`, `bored` | 0.4 |
| `anger` | `angry`, `annoyance`, `rage` | 0.55 |
| `anticipation` | `interest`, `vigilance`, `curious`, `curiosity`, `eager`, `hopeful` | 0.45 |

**Default mouth influence** is a per-emotion hint (0–1) that tells the facial compositor how much an emotion-driven mouth shape should contribute when the character is not speaking. During active speech, LipSync owns the mouth blendshapes; outside of speech, this value controls how strongly the emotional pose shapes the mouth region.

Every non-neutral entry in the built-in set also carries a **complement** — a related emotion that comes along at reduced strength when [emotion blending](emotion-profile.md#emotion-blending) is on. `joy` and `trust` are mutual complements; `fear` and `surprise` are mutual; `sadness` complements `disgust`; `disgust` complements `anger`; `anger` complements `disgust`; `anticipation` complements `joy`.

## How alias resolution works

Every time Convai sends an emotion, the controller calls `IEmotionTaxonomy.TryResolve(serverLabel, out EmotionDescriptor descriptor)`. The resolver checks canonical labels first, then the full alias list across all entries.

- If the label resolves successfully, the corresponding canonical label and descriptor are used throughout the pipeline.
- If the label does **not** resolve, the controller falls back to the neutral descriptor. **No console warning is produced.** The pipeline continues running normally, writing neutral scores every frame.

**Example:** Convai sends `"happy"` → `TryResolve` finds `"happy"` in the aliases list of the `joy` entry → the accumulator sets the target score for `"joy"`.

{% hint style="warning" %}
When Convai sends a label that is not in the taxonomy, the failure is silent — no console warning appears and no error is logged. The character returns to neutral as if no emotion signal arrived. If a specific emotion never appears on your character, the server label is likely not covered by the active taxonomy. See [Troubleshoot emotion](troubleshooting-and-diagnostics.md#unknown-server-labels-silent-neutral-fallback) for how to detect and fix this.
{% endhint %}

## Creating a custom taxonomy asset

In the Project window, right-click inside your `Assets/` folder and choose:

**Create → Convai → Embodiment → Emotion Taxonomy**

A new asset named `EmotionTaxonomy` appears. Select it to edit the entries list in the Inspector.

### EmotionTaxonomyEntry fields

| Field | Type | Description |
| --- | --- | --- |
| `label` | `string` | The canonical, lowercase label used throughout the pipeline (e.g. `"joy"`). Must be unique within the taxonomy. |
| `aliases` | `List<string>` | All server-side strings that should resolve to this entry (e.g. `"happy"`, `"happiness"`). |
| `complements` | `List<string>` | Canonical labels of emotions that read naturally alongside this one and come along at reduced strength when [emotion blending](emotion-profile.md#emotion-blending) is on — for example `joy` with a trace of `trust`. Only consulted when the character's profile has blending enabled. |
| `defaultMouthInfluence` | `float` (0–1) | Mouth influence hint for LipSync blending. See the built-in table above for reference values. |
| `isNeutral` | `bool` | Marks this entry as the taxonomy's neutral baseline — what the face relaxes to between feelings, and the accumulator's decay anchor. |
| `useCustomDimensions` | `bool` | When enabled, this entry's `valence`/`arousal`/`agency`/`approach` fields override the built-in dimension defaults for the label. When disabled, the values are resolved from `EmotionDimensionDefaults` for known labels. |
| `valence`, `arousal`, `agency`, `approach` | `float` (-1 – 1) | The `EmotionDimensions` this emotion carries: how pleasant, how worked up, how in control, and whether it moves the character toward or away from what caused it. Consumed by Gaze, Body Language, and locomotion as one shared modulation signal alongside the categorical label. Only used when `useCustomDimensions` is `true`. |

{% hint style="warning" %}
**Exactly one entry must have `isNeutral = true`.** The accumulator uses the neutral entry as its decay anchor. If no entry is marked neutral, or if more than one is marked neutral, the system logs a warning and synthesizes a fallback — but expressions will not settle correctly at runtime. The console warning messages are:

- `[EmotionTaxonomyAsset] This emotion vocabulary marks no emotion as the neutral one, so a stand-in is being used. Tick 'Is Neutral' on exactly one emotion — it is what the face relaxes to between feelings.` — no neutral entry found
- `[EmotionTaxonomyAsset] N emotions in this vocabulary are ticked 'Is Neutral' and only the first is used. Untick the others, so it is clear which one the face relaxes to.` — multiple neutral entries found
{% endhint %}

### Assigning a custom taxonomy to a profile

1. Open your `ConvaiEmotionProfile` asset.
2. Drag the custom `EmotionTaxonomyAsset` into the **Taxonomy** field.
3. The controller picks up the new taxonomy the next time the profile is applied — immediately in Play Mode, and immediately in Edit Mode because `ConvaiEmotionController` carries `[ExecuteAlways]` from its base class.

## When to create a custom taxonomy

The built-in Plutchik set covers all emotions Convai currently sends. A custom taxonomy is worth creating when:

- Your Convai configuration uses custom emotion labels that differ from the built-in aliases.
- You want to use a different conceptual model — for example, Ekman's six basic emotions — and map multiple server aliases onto fewer canonical buckets.
- You want to adjust `defaultMouthInfluence` values for specific emotions to better suit your character's rig.
- You need to define `complements` relationships for emotion blending, or author `valence`/`arousal`/`agency`/`approach` dimensions that differ from the built-in defaults.

## Next steps

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot emotion](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
