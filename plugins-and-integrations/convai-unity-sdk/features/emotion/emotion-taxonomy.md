---
title: Emotion taxonomy
description: Understand how emotion labels resolve from Convai signals to canonical presentation labels, including the built-in set and custom taxonomy authoring.
last_reviewed: "4.2.0"
---

The taxonomy translates Convai's raw emotion strings into the canonical labels the rest of the system uses. When Convai sends `"serenity"`, the taxonomy resolves that alias to `"joy"` so that the accumulator and output bindings — which are keyed on canonical labels — know exactly which score to update. The SDK ships with a nine-emotion Plutchik-inspired default; author a custom `EmotionTaxonomyAsset` when you need a different vocabulary or additional Convai aliases.

## Built-in Plutchik taxonomy

When the `taxonomy` field on a `ConvaiEmotionProfile` is left empty, the system synthesises the following set at runtime. This default covers all emotions Convai currently produces and requires no asset to be created.

| Canonical label | Convai aliases | Default mouth influence |
| --- | --- | --- |
| `neutral` | _(none)_ | 0.0 |
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

Every time Convai emits an emotion, the controller calls `IEmotionTaxonomy.TryResolve(convaiLabel, out EmotionDescriptor descriptor)`. The resolver checks canonical labels first, then the full alias list across all entries.

- If the label resolves successfully, the corresponding canonical label and descriptor are used throughout the pipeline.
- If the label does **not** resolve, the controller logs a warning and falls back to the neutral descriptor. The pipeline continues running normally, writing neutral scores every frame.

**Example:** Convai sends `"serenity"` → `TryResolve` finds `"serenity"` in the aliases list of the `joy` entry → the accumulator sets the target score for `"joy"`.

{% hint style="warning" %}
When Convai sends a label that is not in the taxonomy, `ConvaiEmotionController` logs a warning before falling back to neutral. If a specific emotion never appears on your character, the Convai label may not be covered by the active taxonomy. See [Troubleshoot emotion](troubleshooting-and-diagnostics.md#unknown-convai-labels-fall-back-to-neutral) for how to detect and fix this.
{% endhint %}

## Creating a custom taxonomy asset

In the Project window, right-click inside your `Assets/` folder and choose:

**Create → Convai → Embodiment → Emotion Taxonomy**

A new asset named `EmotionTaxonomy` appears. Select it to edit the entries list in the Inspector.

### EmotionTaxonomyEntry fields

| Field | Type | Description |
| --- | --- | --- |
| `label` | `string` | The canonical, lowercase label used throughout the pipeline (e.g. `"joy"`). Must be unique within the taxonomy. |
| `aliases` | `List<string>` | All Convai-side strings that should resolve to this entry (e.g. `"serenity"`, `"ecstasy"`). |
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

The built-in Plutchik set covers all emotions Convai currently sends. A custom taxonomy is worth creating when:

- Your Convai configuration uses custom emotion labels that differ from the built-in aliases.
- You want to use a different conceptual model — for example, Ekman's six basic emotions — and map multiple Convai aliases onto fewer canonical buckets.
- You want to adjust `defaultMouthInfluence` values for specific emotions to better suit your character's rig.
- You need to define `complements` relationships that prevent neutral alternation from interrupting specific emotion combinations in your application's flow.

## Next steps

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot emotion](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
