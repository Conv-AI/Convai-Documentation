---
title: Emotion output bindings
description: Reference for the Emotion module's shader-property output binding, which drives effects such as blush, tear glisten, or sweat sheen.
last_reviewed: "4.6.0"
---

Output bindings are the optional extra stage of the Emotion pipeline, for effects beyond the face itself. Facial expression is not authored through a binding — it is written automatically through the shared facial compositor. This page covers `MaterialPropertyEmotionBinding`, the one output binding a profile authors, for shader effects such as blush, tear glisten, or sweat sheen.

## How facial expression reaches the face

Emotion writes facial output through the shared facial compositor rather than through a directly-authored binding. Expression recipes are compiled once, resolved against the character's rig, and submitted to the compositor's emotion layers alongside LipSync and the micro-expression life layer. See [Facial composition](../facial-composition.md) for the compositor's layer model, blend modes, and the LipSync-over-Emotion priority rule.

## MaterialPropertyEmotionBinding

`MaterialPropertyEmotionBinding` drives arbitrary shader float properties — blush, tear glisten, sweat sheen, or any other custom shader effect — from composed emotion scores, with no built-in shader knowledge in the SDK. It is authored in the **Material Effects** field on `ConvaiEmotionProfile`, as a list of `MaterialPropertyEmotionSlot` entries.

### MaterialPropertyEmotionSlot fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `emotionLabel` | `string` | — | The canonical taxonomy label that drives this effect (e.g. `"anger"`). |
| `propertyName` | `string` | — | The shader's exposed float property name (e.g. `"_EmotionBlush"`). Leave empty to skip this slot. |
| `minValue` | `float` | **0** | Property value written at zero composed intensity. |
| `maxValue` | `float` | **1** | Property value written at full (1.0) composed intensity. |

### How it resolves and writes

- Target renderers are resolved the same way the facial expression output is: the rig's facial meshes, falling back to a `SkinnedMeshRenderer` scan under the character root.
- Writes go through a per-renderer `MaterialPropertyBlock` (get-modify-set), so the shared material asset is never mutated and any other system's own property-block writes on the same renderer are preserved.
- **Max-combine rule.** When two or more slots target the same property on the same renderer — for example both `anger` and an `embarrassment`-labeled custom entry driving `_EmotionBlush` — their composed intensities are compared each frame and the strongest slot's `[minValue, maxValue]` range wins, independent of authoring order.
- **Rest on unbind.** Disabling the controller or swapping profiles writes each touched property back to its slot's `minValue` rather than leaving the last emotional value stuck.
- Whether a resolved facial mesh's material actually declares the authored property does not block the write — an unsupported `MaterialPropertyBlock` float write is inert, never an error, and shader variance across meshes on the same character is normal.
- A profile whose only authored output is material-property slots still counts as active output; it does not trigger the "no facial output resolved" diagnostic warning covered in [Troubleshoot emotion](troubleshooting-and-diagnostics.md).

{% hint style="warning" %}
If none of the authored property names are found on any target material, the binding logs one warning per bind: `[MaterialPropertyEmotionBinding] '<name>' has authored material-property slot(s) but none of the authored shader properties (<names>) were found on any target material. Verify the property name(s) (e.g. "_EmotionBlush") match a property exposed by the character's assigned material(s).` Per-slot misses on some meshes but not others stay silent, since shader variance across meshes is normal.
{% endhint %}

### Example

```csharp
// Material Binding slots authored on the profile:
// { emotionLabel: "anger", propertyName: "_EmotionBlush", minValue: 0, maxValue: 0.6 }
// { emotionLabel: "fear",  propertyName: "_EmotionSweat", minValue: 0, maxValue: 1 }
```

## Shared sample taxonomy and profile assets

The Emotion module ships shared sample assets under `SamplesShared/Profiles/Embodiment/Modules/Emotion/`: `ConvaiSamplesShared_EmotionTaxonomy.asset`, and four named personality profile assets — `Warm`, `Composed`, `Energetic`, `Reserved`.

1. Point a character's **Taxonomy** field at `SamplesShared/Profiles/Embodiment/Modules/Emotion/ConvaiSamplesShared_EmotionTaxonomy.asset`.
2. Point its **Profile** field at whichever of the four named personality assets fits the character, or build your own with [character type presets](emotion-profile.md#character-type-presets).
3. A character left with no taxonomy still runs, but every emotion dropdown that reads one comes up empty — this reads as a broken Inspector rather than as a missing reference, so check for it explicitly rather than waiting for a console warning.
4. These shared assets live inside the package. To edit either one directly, copy it into your own `Assets/` folder first — an edit made inside the package does not persist across a package update.

## Next steps

{% content-ref url="emotion-profile.md" %}
[Emotion profile](emotion-profile.md)
{% endcontent-ref %}

{% content-ref url="../facial-composition.md" %}
[Facial composition](../facial-composition.md)
{% endcontent-ref %}
