---
title: Emotion output bindings
description: Reference for the Emotion module's remaining output binding, now that the slot-list facial output path has been removed as a breaking change.
last_reviewed: "4.5.0"
---

Output bindings are the optional extra stage of the Emotion pipeline, for effects beyond the face itself. Facial expression is not authored through a binding — it is written automatically through the shared facial compositor. This page covers `MaterialPropertyEmotionBinding`, the one output binding a profile can still author, and the migration for profiles that used the removed slot-list path.

{% hint style="danger" %}
**Breaking change in SDK <code class="expression">space.vars.unity_sdk_version</code>.** The slot-list facial output path is removed from the Emotion module: `EmotionSlotBinding`, `BlendshapeEmotionBinding`, `AnimatorParameterEmotionBinding`, `RealisticEmotionSlots`, `NeutralAlternator`, and the profile's `SemanticExpressionsEnabled`/`NeutralAlternationEnabled` switches and `CreateBlendshapeRuntimeBinding`/`CreateAnimatorRuntimeBinding` factories are all gone. See [Migrate from the slot-list facial path](#migrate-from-the-slot-list-facial-path) below.
{% endhint %}

## Why the slot-list path was removed

The slot-list path was a second facial output system whose data the runtime discarded whenever semantic expressions were active — which was every shipped profile. Its authored slots, the per-rig tooling that built them, and the neutral alternator they fed were dead weight presented as live configuration. [Expression recipes](emotion-profile.md#expression-recipes-and-output) replace it and need no per-rig authoring at all: a recipe names what should move in semantic terms, and the runtime resolves that against whichever blendshapes the character's mesh actually has. A profile that carried authored slots loses only data that was never read — nothing needs porting.

Shader-property output is unaffected and is now the one remaining output binding a profile authors directly.

## How facial expression reaches the face now

Emotion writes facial output through the shared facial compositor rather than through a directly-authored binding. Expression recipes are compiled once, resolved against the character's rig, and submitted to the compositor's emotion layers alongside LipSync and the micro-expression life layer. See [Facial composition](../facial-composition.md) for the compositor's layer model, blend modes, and the LipSync-over-Emotion priority rule.

## MaterialPropertyEmotionBinding

`MaterialPropertyEmotionBinding` drives arbitrary shader float properties — blush, tear glisten, sweat sheen, or any other custom shader effect — from composed emotion scores, with no built-in shader knowledge in the SDK. It is authored in the **Material Binding** field on `ConvaiEmotionProfile`, as a list of `MaterialPropertyEmotionSlot` entries.

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
If none of the authored property names are found on any target material, the binding logs one warning per bind: `[MaterialPropertyEmotionBinding] '<name>' has authored material-property slot(s) but none of the authored shader properties (<names>) were found on any target material.` Per-slot misses on some meshes but not others stay silent, since shader variance across meshes is normal.
{% endhint %}

### Example

```csharp
// Material Binding slots authored on the profile:
// { emotionLabel: "anger", propertyName: "_EmotionBlush", minValue: 0, maxValue: 0.6 }
// { emotionLabel: "fear",  propertyName: "_EmotionSweat", minValue: 0, maxValue: 1 }
```

## Migrate from the slot-list facial path

If your profile authored `BlendshapeEmotionBinding` or `AnimatorParameterEmotionBinding` slots for facial expression, that authored data is not read in SDK <code class="expression">space.vars.unity_sdk_version</code> and does not need to be re-entered:

1. Open the affected `ConvaiEmotionProfile` asset. Any slot lists from the removed bindings are gone from the Inspector — there is nothing to delete by hand.
2. Confirm the character still expresses correctly: expression recipes drive the face automatically, with no per-rig authoring. Leave the profile's **Expression Recipes** field empty to use Convai's production-safe defaults, or author your own recipes for character-specific art direction.
3. If you used `RealisticEmotionSlots.Build(RigConvention)` from code to generate slots, remove that call — the type no longer exists, and its job is done automatically by expression recipe resolution.
4. If you relied on **Neutral Alternation** to keep a sustained expression from reading as frozen, enable **Micro Expressions Enabled** on the profile instead. It produces idle drift and speech-coupled accents procedurally and composes additively, so it can never suppress the expression underneath. See [Micro-expression life](emotion-profile.md#micro-expression-life).
5. If you authored `isMouthShape` routing on a slot to keep an emotion-driven mouth shape from fighting LipSync, no action is needed — the shared facial compositor now owns that priority (LipSync over Emotion) for every character automatically.
6. Any `materialBinding` slots you authored for shader effects are unaffected and require no changes.

## Re-point the shared sample taxonomy and profile

The shared sample assets also changed in this release, separately from the slot-list removal: `ConvaiSamplesShared_EmotionTaxonomy.asset` was rebuilt with a new asset identifier, and `ConvaiSamplesShared_EmotionProfile.asset` was removed entirely, replaced by four named personality assets (`Warm`, `Composed`, `Energetic`, `Reserved`). Unity cannot carry a reference across an asset identifier change, so a character or profile that pointed at either shared asset reports a missing reference after upgrading.

1. Open each affected character and re-point its **Taxonomy** field at `SamplesShared/Profiles/Embodiment/Modules/Emotion/ConvaiSamplesShared_EmotionTaxonomy.asset`.
2. Re-point its **Profile** field at whichever of the four named personality assets fits the character, or build your own with [character type presets](emotion-profile.md#character-type-presets).
3. A character left with no taxonomy still runs, but every emotion dropdown that reads one comes up empty — this reads as a broken Inspector rather than as a missing reference, so check for it explicitly rather than waiting for a console warning.
4. If you had edited either shared asset from inside the package, copy your version into your own `Assets/` folder before upgrading; anything left inside the package is replaced by the SDK update.

## Next steps

{% content-ref url="emotion-profile.md" %}
[Emotion profile](emotion-profile.md)
{% endcontent-ref %}

{% content-ref url="../facial-composition.md" %}
[Facial composition](../facial-composition.md)
{% endcontent-ref %}
