---
title: Emotion taxonomy
description: Reference for EmotionTaxonomyAsset, including built-in labels, Convai label resolution, aliases, and custom taxonomy authoring.
---

The taxonomy translates raw Convai emotion strings into the canonical labels used by the Unity presentation pipeline. The SDK ships with a nine-emotion Plutchik-inspired default. Author a custom `EmotionTaxonomyAsset` when Convai, a custom provider, or your own tooling intentionally emits labels outside the default vocabulary.

## Built-in Plutchik taxonomy

When the `taxonomy` field on a `ConvaiEmotionProfile` is left empty, the system synthesizes the following set at runtime. This default covers the Convai emotion contract and requires no asset to be created.

| Canonical label | Aliases | Default mouth influence |
| --- | --- | --- |
| `neutral` | None | 0.0 |
| `joy` | `serenity`, `ecstasy` | 0.6 |
| `trust` | `acceptance`, `admiration` | 0.3 |
| `fear` | `apprehension`, `terror` | 0.4 |
| `surprise` | `distraction`, `amazement` | 0.5 |
| `sadness` | `pensiveness`, `grief` | 0.3 |
| `disgust` | `boredom`, `loathing` | 0.4 |
| `anger` | `annoyance`, `rage` | 0.55 |
| `anticipation` | `interest`, `vigilance` | 0.45 |

**Default mouth influence** is a per-emotion hint (0–1) that tells the facial blendshape compositor how much an emotion-driven mouth shape should contribute when the character is not speaking. During active speech, LipSync overrides mouth blendshapes according to phoneme data; outside of speech, this value controls how strongly the emotional pose shapes the mouth region.

## How alias resolution works

Every time Convai emits an emotion, the controller calls `IEmotionTaxonomy.TryResolve(serverLabel, out EmotionDescriptor descriptor)`. The resolver checks canonical labels first, then the full alias list across all entries.

- If the label resolves successfully, the corresponding canonical label and descriptor are used throughout the pipeline.
- If the label does **not** resolve, `ConvaiEmotionController` logs a warning and falls back to the neutral descriptor. The pipeline continues running normally, writing neutral scores every frame.

**Example:** Convai sends `"Ecstasy"` -> `TryResolve` finds `ecstasy` in the aliases list of the `joy` entry -> the accumulator sets the target score for `joy`.

{% hint style="warning" %}
When Convai sends a label that is not in the taxonomy, the character returns to neutral and the Console shows `[ConvaiEmotionController] Unknown backend emotion label ...`. If the label is expected, add it as an alias in a custom taxonomy. See [Troubleshoot emotion](troubleshooting-and-diagnostics.md#unknown-labels-fall-back-to-neutral) for how to detect and fix this.
{% endhint %}

## Creating a custom taxonomy asset

In the Project window, right-click inside your `Assets/` folder and choose:

**Create → Convai → Embodiment → Emotion Taxonomy**

A new asset named `EmotionTaxonomy` appears. Select it to edit the entries list in the Inspector.

### EmotionTaxonomyEntry fields

| Field | Type | Description |
| --- | --- | --- |
| `label` | `string` | The canonical, lowercase label used throughout the pipeline (e.g. `"joy"`). Must be unique within the taxonomy. |
| `aliases` | `List<string>` | Additional strings that should resolve to this entry, such as high- or low-intensity Convai labels. |
| `complements` | `List<string>` | Canonical labels of emotions that suppress neutral alternation when active. If a complement emotion is currently scoring above zero, the neutral alternator skips its fade cycle for that entry. In the built-in taxonomy, `joy` and `trust` are mutual complements. |
| `defaultMouthInfluence` | `float` (0–1) | Mouth influence hint for LipSync blending. See the built-in table above for reference values. |
| `isNeutral` | `bool` | Marks this entry as the taxonomy's neutral baseline — the decay target for the accumulator and the destination state during neutral alternation. |

{% hint style="warning" %}
**Exactly one entry must have `isNeutral = true`.** The accumulator uses the neutral entry as its decay anchor. If no entry is marked neutral, or if more than one is marked neutral, the system logs a warning and synthesises a fallback — but expressions will not settle correctly at runtime. The console warning messages are:

- `[EmotionTaxonomyAsset] No entry marked neutral; synthesized 'neutral' fallback.` — no neutral entry found
- `[EmotionTaxonomyAsset] N entries are marked IsNeutral; only the first will be used.` — multiple neutral entries found
{% endhint %}

### Assigning a custom taxonomy to a profile

1. Open your `ConvaiEmotionProfile` asset.
2. Drag the custom `EmotionTaxonomyAsset` into the **Taxonomy** field.
3. The controller picks up the new taxonomy the next time the profile is applied — immediately in Play Mode, and immediately in Edit Mode because `ConvaiEmotionController` carries `[ExecuteAlways]` from its base class.

## When to create a custom taxonomy

The built-in Plutchik set covers the current Convai emotion labels. A custom taxonomy is worth creating when:

- Convai or a custom provider sends project-specific emotion labels that differ from the built-in aliases.
- You want to use a different conceptual model, such as Ekman's six basic emotions, and map multiple incoming aliases onto fewer canonical buckets.
- You want to adjust `defaultMouthInfluence` values for specific emotions to better suit your character's rig.
- You need to define `complements` relationships that prevent neutral alternation from interrupting specific emotion combinations in your application's flow.

## Next steps

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot emotion](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
