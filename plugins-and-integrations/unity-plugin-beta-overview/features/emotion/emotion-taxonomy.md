---
description: >-
  The emotion vocabulary that connects backend labels to your character's
  expressions — how it works, what the built-in set includes, and how to extend
  it.
---

# Emotion Taxonomy

## Defining the Emotion Vocabulary with EmotionTaxonomyAsset

The taxonomy is the dictionary that translates the Convai backend's raw emotion strings into the canonical labels the rest of the system uses. When the server sends `"happy"`, the taxonomy resolves that alias to `"joy"` so that the accumulator and output bindings — which are keyed on canonical labels — know exactly which score to update. The SDK ships with a nine-emotion Plutchik-inspired default; you can author a custom `EmotionTaxonomyAsset` whenever you need a different vocabulary or additional server labels.

## Built-in Plutchik Taxonomy

When the `taxonomy` field on a `ConvaiEmotionProfile` is left empty, the system synthesises the following set at runtime. This default covers all emotions the Convai backend currently produces and requires no asset to be created.

| Canonical Label | Server Aliases                                | Default Mouth Influence |
| --------------- | --------------------------------------------- | ----------------------- |
| `neutral`       | `calm`, `idle`                                | 0.0                     |
| `joy`           | `happy`, `happiness`, `ecstasy`, `serenity`   | 0.6                     |
| `trust`         | `acceptance`, `admiration`                    | 0.3                     |
| `fear`          | `afraid`, `apprehension`, `terror`, `fearful` | 0.4                     |
| `surprise`      | `amazement`, `distraction`, `surprised`       | 0.5                     |
| `sadness`       | `sad`, `pensiveness`, `grief`                 | 0.3                     |
| `disgust`       | `disgusted`, `loathing`, `boredom`, `bored`   | 0.4                     |
| `anger`         | `angry`, `annoyance`, `rage`                  | 0.55                    |
| `anticipation`  | `interest`, `vigilance`                       | 0.45                    |

**Default Mouth Influence** is a per-emotion hint (0–1) that tells the facial blendshape compositor how much an emotion-driven mouth shape should contribute when the character is not speaking. During active speech, LipSync overrides mouth blendshapes according to phoneme data; outside of speech, this value controls how strongly the emotional pose shapes the mouth region.

## How Alias Resolution Works

Every time the backend emits an emotion, the controller calls `IEmotionTaxonomy.TryResolve(serverLabel, out EmotionDescriptor descriptor)`. The resolver checks canonical labels first, then the full alias list across all entries.

* If the label resolves successfully, the corresponding canonical label and descriptor are used throughout the pipeline.
* If the label does **not** resolve, the emotion event is silently ignored and a warning is written to the Unity Console. This prevents unknown labels from disrupting the running state.

**Example:** The backend sends `"happy"` → `TryResolve` finds `"happy"` in the aliases list of the `joy` entry → the accumulator sets the target score for `"joy"`.

{% hint style="info" %}
If you see `[Taxonomy] Label not found` warnings in the Console, the backend is sending a label that is not present in the canonical list or any alias. Add the new label as an alias to the appropriate entry in a custom taxonomy asset, or create a new entry for it.
{% endhint %}

## Creating a Custom Taxonomy Asset

In the Project window, right-click inside your `Assets/` folder and choose:

**Create → Convai → Embodiment → Emotion Taxonomy**

A new asset named `EmotionTaxonomy` appears. Select it to edit the entries list in the Inspector.

### EmotionTaxonomyEntry Fields

<table><thead><tr><th width="228.49993896484375">Field</th><th width="163">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>label</code></td><td><code>string</code></td><td>The canonical, lowercase label used throughout the pipeline (e.g. <code>"joy"</code>). Must be unique within the taxonomy.</td></tr><tr><td><code>aliases</code></td><td><code>List&#x3C;string></code></td><td>All server-side strings that should resolve to this entry (e.g. <code>"happy"</code>, <code>"happiness"</code>).</td></tr><tr><td><code>complements</code></td><td><code>List&#x3C;string></code></td><td>Canonical labels of emotions that suppress neutral synthesis when active. If a complement emotion is currently scoring above zero, neutral alternation does not fade toward neutral for that cycle.</td></tr><tr><td><code>defaultMouthInfluence</code></td><td><code>float</code> (0–1)</td><td>Mouth influence hint for LipSync blending. See the built-in table above for reference values.</td></tr><tr><td><code>isNeutral</code></td><td><code>bool</code></td><td>Marks this entry as the taxonomy's neutral baseline — the decay target for the accumulator and the destination state during neutral alternation.</td></tr></tbody></table>

{% hint style="warning" %}
**Exactly one entry must have `isNeutral = true`.** The accumulator uses the neutral entry as its decay anchor. If no entry is marked neutral, or if more than one is marked neutral, the system's behaviour is undefined and expressions will not settle correctly at runtime.
{% endhint %}

### Assigning a Custom Taxonomy to a Profile

1. Open your `ConvaiEmotionProfile` asset.
2. Drag the custom `EmotionTaxonomyAsset` into the **Taxonomy** field.
3. The controller picks up the new taxonomy the next time the profile is applied — immediately in Play Mode, and immediately in Edit Mode because `ConvaiEmotionController` is `[ExecuteAlways]`.

## When to Create a Custom Taxonomy

The built-in Plutchik set covers all emotions the Convai backend currently sends. A custom taxonomy is worth creating when:

* Your Convai configuration uses custom emotion labels that differ from the built-in aliases.
* You want to use a different conceptual model — for example, Ekman's six basic emotions — and map multiple server aliases onto fewer canonical buckets.
* You want to adjust `defaultMouthInfluence` values for specific emotions to better suit your character's rig.
* You need to define `complements` relationships that prevent neutral alternation from interrupting specific emotion combinations in your application's flow.

## Conclusion

With the taxonomy in place, the pipeline has a complete, authoritative mapping from server labels to the canonical identifiers that drive your output bindings. Continue to [Scripting API](scripting-api-reference.md) to learn how to read and control emotion state from C# at runtime, or see [Troubleshooting](troubleshooting-and-diagnostics.md) if taxonomy warning messages are appearing in the Console.
