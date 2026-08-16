---
title: Migrate from Dialogue Animation
description: Replace the retired Dialogue Animation components with Convai Body Animation and delete the Animator Controller assets it replaces.
last_reviewed: "4.5.0"
---

SDK 4.5.0 retired the Dialogue Animation module and deleted the nine documentation pages that covered it, with no redirects. If a bookmark or a search result brought you here instead, this page is the replacement: it maps every removed component and asset to its Convai Body Animation equivalent, and it says plainly that the Animator Controller workflow those pages taught has no successor — it is deleted, not migrated.

## Component and asset replacements

| Removed in 4.5.0 | Replaced by | Add through |
|---|---|---|
| `ConvaiDialogueAnimationController` | `ConvaiBodyAnimationController` | **Add Component > Convai > Embodiment > Body Animation** |
| `DialogueAnimationLibrary` | `ConvaiBodyAnimationSet` | **Create > Convai > Embodiment > Body Animation Set** |
| `DialogueAnimationRuntimeConfig` | `ConvaiBodyAnimationConfig` | **Create > Convai > Embodiment > Body Animation Config** |
| `ConvaiDialogueAnimationProfile` | `ConvaiBodyAnimationProfile` | Bundles a Set and a Config for the controller to read together |
| `DialogueAnimatorContract`, its four Animator Controller layers, the ping-pong states, and every `ConvaiDialogueSlot_*` placeholder clip | Nothing — `ConvaiBodyAnimationController` builds its own layered `PlayableGraph` in code | Delete the contract asset and its layers; see the next section |
| `AnimationRiggingGazeBridge` | Nothing — Convai Gaze writes bone rotations procedurally | Remove the component and its constraints |

`DialogueClipEntry`, `IAnimationClipLibrary`, `IDialogueVariantSelector`, `VariantSelectionContext`, `EmotionWeightedRandomSelector`, `DialogueAnimationClipPicker`, `AnimatorLayerBlender`, `AnimatorSlotOverrider`, and `AnimatorStatePingPong` are also gone with the module. If your project implemented `IDialogueVariantSelector` to control which clip variant played, that seam does not exist on Body Animation — open an issue with Convai describing what your selector decided, so the replacement covers it.

## Delete the Animator Controller workflow entirely

{% hint style="warning" %}
Dialogue Animation played idle and talk clips by driving a four-layer Animator Controller you authored yourself. `ConvaiBodyAnimationController` replaces the Animator's output with its own `PlayableGraph` while active, but it does not remove a leftover controller for you — an Animator Controller left assigned fights the graph for the same bones.
{% endhint %}

Delete the `DialogueAnimatorContract` asset, its four layers (base idle, idle overlay, body talk, head talk), the ping-pong states inside them, and every `ConvaiDialogueSlot_*` placeholder clip the layers referenced. Nothing in Body Animation reads any of them. This is the important part of the migration: you are not porting the animator contract to a new format, you are deleting it, because content now lives in a `ConvaiBodyAnimationSet` and behavior tuning lives in a `ConvaiBodyAnimationConfig` instead of Animator Controller states.

If the character's Animator still has a Runtime Animator Controller assigned after you add `ConvaiBodyAnimationController`, the component's own inspector reports it as a finding and offers a one-click fix to clear the reference.

## What carries over automatically

Idle and talk variants, emotion-weighted selection between them, and upper-body talk coverage all carry over conceptually from Dialogue Animation to Body Animation — the ideas are the same, only the authoring surface changed. Move your idle and talk clips into a `ConvaiBodyAnimationSet`'s Idle and Talk pools; the set reuses the same weighted, emotion-aware selection Dialogue Animation used, and the talk layer still restricts itself to the upper body when a mask is assigned.

## Gender filtering and emotion affinity tags have no migration path

Two authoring concepts from Dialogue Animation have no field-level replacement, and their data does not migrate:

- **Per-clip gender filtering.** `CharacterGender`, authored on the character and on each clip entry, is gone. Author one `ConvaiBodyAnimationSet` per character type — one set for your female characters, a separate set for your male or creature characters — instead of authoring a single mixed set and filtering it at runtime.
- **Per-clip emotion affinity tags.** `DialogueEmotionAffinity` and the `EmotionBiasStrength` that weighted it are gone as an authoring surface. Body Animation and the Emotion module coordinate through the embodiment context instead of through tags on individual clip entries — there is no equivalent field to fill in on a `ConvaiBodyAnimationSet` entry.

Neither concept was dropped silently: both are named in the `4.5.0` migration notes as having no field-level equivalent, so treat their absence as a deliberate design change, not a gap to work around.

## Convai Gaze needs no rigging package

If a character used `AnimationRiggingGazeBridge` to drive Unity Animation Rigging `MultiAimConstraint` weights from gaze, remove the bridge component and its constraints. Convai Gaze writes bone rotations procedurally and needs no rigging package at all — delete the `com.unity.animation.rigging` package reference too, if nothing else in your project depends on it.

## Verify the migration

- Enter Play mode. The character idles and plays talk gestures while `DialogueState` is `Speaking`, with no Animator Controller assigned.
- Open the character's Animator component and confirm **Controller** is empty — a leftover controller is the most common cause of legs or arms twitching against the `PlayableGraph`'s output.
- Confirm the project has no remaining reference to `ConvaiDialogueAnimationController`, `DialogueAnimationLibrary`, `DialogueAnimatorContract`, or `AnimationRiggingGazeBridge` — Unity reports a missing script or a missing reference on any `GameObject` or asset that still points at one.
- Open **Convai > Body Animation Editor**, the **Setup** mode, and confirm the character shows no error-severity finding.

## Next steps

{% content-ref url="quick-start.md" %}
[quick-start.md](quick-start.md)
{% endcontent-ref %}

{% content-ref url="build-an-animation-set.md" %}
[build-an-animation-set.md](build-an-animation-set.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[troubleshooting.md](troubleshooting.md)
{% endcontent-ref %}
