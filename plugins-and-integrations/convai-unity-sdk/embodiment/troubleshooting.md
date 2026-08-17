---
title: Troubleshoot embodiment
description: Diagnose rig detection, preset slot, module tick, and facial compositing problems in the Convai embodiment system, with fixes and verification steps.
last_reviewed: "4.5.0"
---

Use this page when a character's rig is not detected correctly, an embodiment preset is not applying the way you expect, a module never seems to update, or two modules appear to fight over the same facial expression. Start with the [Embodiment Editor window](embodiment-editor.md) — its `Setup` tab and `Presets` tab surface most of these problems directly, with a one-click fix where one exists.

## Troubleshooting table

| Symptom | Likely cause | Fix | Verify |
|---|---|---|---|
| Rig section in the Embodiment Editor reads `Not Set Up` | No character is selected, or the selected `GameObject` has no `ConvaiCharacter` component | Select the character in the Hierarchy, or add `ConvaiCharacter` to its `GameObject` | The `Setup` tab's `Rig` section header changes to `Ready` or `Needs Attention` |
| Rig section reads `Needs Attention`: "No Animator (Optional)" or "Rig is not Humanoid" | The character has no `Animator`, or its rig is not set to `Humanoid` | Skip this if the character does not need skeletal body movement; otherwise set the model's Rig type to `Humanoid` in its import settings | The finding is replaced by an `Ok` finding, or a bone-resolution finding for `Head`/`LeftEye`/`RightEye` |
| Rig section reads `Needs Attention`: "Face rig not recognized" | `StandardRigBinding.DetectedConvention` resolved to `Unknown` — the face mesh does not match a known blendshape naming convention | Set `Convention Override` on the `StandardRigBinding` component manually, or assign a `CustomRigConventionMap` | The finding is replaced by an `Ok` finding naming the convention |
| Rig section reads `Needs Attention`: "…but only just" | `DetectionConfidence` is below `50%` | Check that expression and lip sync look correct; if not, set the convention manually instead of trusting auto-detection | `DetectionConfidence` reported by `StandardRigBinding` rises above `50%`, or the convention is set manually |
| "Head", "Left eye", or "Right eye" bone finding shows a warning | The rig's humanoid avatar has no bone mapped for that semantic, or the rig is not Humanoid | Set the model's Rig type to `Humanoid` in its import settings, or assign an explicit bone override on `StandardRigBinding` | `StandardRigBinding.TryGetBone` for that bone returns `true`, and the corresponding warning stops appearing in the Console |
| Console repeats a rig bone or blendshape warning every time you touch the character | Normal for the first miss — this is a rig gap, not a bug | Fill the gap (see the two rows above), or ignore it if the feature that needs it is not in use | The warning is logged once per component lifetime, not once per frame, so it should not recur without a state change |
| A `ConvaiEmbodimentPreset` shows `Not Set Up` in the Embodiment Editor's `Presets` tab | The preset has duplicate module IDs, a slot with no module chosen, or a slot pointing at the wrong profile type | Open the preset and use the finding's fix button, such as `Remove Duplicate` or `Clear Settings` | The preset's status in the `Presets` tab changes to `Ready` or `Needs Attention` |
| A module's settings do not match what the assigned preset says they should be | `Preserve Missing Slots` is enabled and the preset has no slot for that module, so the module kept its own inspector-assigned profile | Add a slot for the module in the preset, or disable `Preserve Missing Slots` if you want every unlisted module to fall back to its default profile instead | The Console's preset diagnostics message for that character no longer lists the module under "Active receivers without a preset slot" |
| A module never seems to update — its state never changes at runtime | The component is not on the same `GameObject` hierarchy as `ConvaiCharacter`, so it disabled itself | Move the component onto the character's `GameObject` or one of its children | The Console error naming the component and "is not on a Convai character" stops appearing, and the component stays enabled after entering Play mode |
| A module updates correctly for a while, then silently stops | The module's tick threw an exception, which is reported once and then the module is skipped | Check the Console for the "threw during its embodiment tick" message and fix the underlying exception in that module | The module resumes updating once code that raised the exception is corrected and the scene is re-entered |
| Two modules appear to fight over the same facial expression | Two modules are driving blendshapes in the same facial region with conflicting weights | Check the per-region weights on the character's `ConvaiFacialCompositionProfile` rather than disabling either module — facial output is a weighted blend of Emotion, LipSync, and Custom layers per region, not an exclusive lock | The region's blendshapes settle into one consistent expression instead of visibly oscillating |

## Rig not detected or low confidence

The Embodiment Editor's `Setup` tab reports the state of a character's `StandardRigBinding` under the `Rig` section. If the character has no `StandardRigBinding` component yet, the tab reports "Rig will be worked out automatically" — Convai resolves it the moment the character starts, so this by itself is not a problem.

Once a `StandardRigBinding` exists (either added manually or by the **Set Up This Character** button), its `DetectedConvention` and `DetectionConfidence` come from inspecting the character's facial meshes. Detection confidence below `50%` is treated as a guess worth checking:

```text
Face rig detected as <convention>, but only just
```

If no known convention matches at all, `DetectedConvention` stays `Unknown` and the tab reports:

```text
Face rig not recognized
```

In both cases, set `Convention Override` on the `StandardRigBinding` component directly, or supply a `CustomRigConventionMap` for a rig that does not match any built-in convention. See [Character rig setup](character-rig-setup.md) for the full detection model.

A missing bone or blendshape logs a warning through the Console once per component lifetime:

```text
[<character name>] This rig has no '<bone>' bone, so anything that needs it stays inactive. Assign it under Custom Rig Setup on the Character Rig component, or use a rig whose humanoid avatar maps that bone.
```

```text
[<character name>] No mesh on this character has a '<blendshape>' blendshape, so anything that drives it stays inactive. Add the blendshape to the face mesh, or map its actual name under Custom Convention Map.
```

Both messages come from `StandardRigBinding.TryGetBone` and `TryGetBlendshape`. They stop repeating once the corresponding bone or blendshape resolves, or once you assign an explicit override.

## Preset slot mismatches

A `ConvaiEmbodimentPreset` maps module IDs to profile assets. Two problems come from the preset asset itself:

- **Duplicate module IDs.** If a preset lists the same module twice, only the first matching slot is used. The Console logs:

  ```text
  Duplicate module profile slots: <ids>. First matching slot is used.
  ```

  Open the preset in the Embodiment Editor's `Presets` tab and remove the duplicate entry.

- **A slot naming a module the project does not have installed**, a slot with no module chosen, or a slot whose assigned profile is the wrong type for the module. Each of these appears as its own finding in the `Presets` tab, with a fix button that removes or clears the offending slot.

Separately, `ConvaiEmbodimentPresetBinding` compares the preset against the modules actually present on the character and logs a combined diagnostics message when anything is off:

```text
[ConvaiEmbodimentPresetBinding] Preset '<preset name>' diagnostics on '<character name>': <report>
```

The `<report>` portion can include any of:

- `Profile slots without an active receiver: <ids>.` — the preset configures a module the character does not have.
- `Profile slots with null profiles: <ids>.` — a slot exists but has no profile asset assigned.
- `Active receivers without a preset slot; inspector profiles will be preserved: <ids>.` — shown when `Preserve Missing Slots` is enabled: modules with no matching slot keep whatever profile is assigned on their own component.
- `Active receivers without a preset slot; null profiles will be applied: <ids>.` — shown when `Preserve Missing Slots` is disabled: modules with no matching slot fall back to `null`, which resolves to their built-in default profile.
- `Blank profile slot indices: <indices>.` — a slot entry has no module ID at all.

If a module's behavior does not match what you expect from the preset, check `Preserve Missing Slots` on `ConvaiEmbodimentPresetBinding` first — it decides whether an unlisted module keeps its own settings or is reset to defaults.

## A module is not ticking

Every embodiment module registers with the character's tick scheduler in `OnEnable` through `EmbodimentContext.RegisterTickable`. Two distinct failures look similar but have different causes.

**The component never registered at all.** This happens when the component is not on the same `GameObject` hierarchy as `ConvaiCharacter`. The component disables itself and the Console logs:

```text
[<ComponentType>] '<GameObject name>' is not on a Convai character, so it has nothing to drive. Move this component onto the object with the Convai Character component (or one of its children).
```

Move the component onto the character's `GameObject` or a child of it, then re-enable it.

**The component registered but its tick throws.** The scheduler catches an exception from any single module's tick, reports it once, and keeps ticking every other module normally:

```text
[EmbodimentTickScheduler] <ComponentType> on '<GameObject name>' threw during its embodiment tick and will be reported only once. Other modules on this character are unaffected.
```

Because this is reported only once per module per session, a module that appears to have "stopped working" without any further Console output is the usual sign of this case. Fix the exception at its source and re-enter Play mode — the module resumes on the fix.

If neither message appears and the module still seems inert, confirm the scene is in Play mode: the tick scheduler is created only at runtime, so nothing ticks in Edit mode outside the Embodiment Editor's `Live` tab.

## Facial output fighting between modules

Facial blendshapes are not owned exclusively by one module. Instead, each blendshape region (mouth, brow, eye, cheek/nose, jaw, and everything else) blends Emotion, LipSync, and Custom layers together according to per-region weights on the character's `ConvaiFacialCompositionProfile`, separately for idle and speaking states.

Visible fighting — an expression that flickers or overshoots instead of settling — usually means two layers are contributing conflicting values to the same region at comparable weight, not that one module is broken. Check the region's weights on `ConvaiFacialCompositionProfile` rather than disabling one of the modules: lowering one layer's weight in that region, or moving a blendshape into a different region by adjusting its name pattern, resolves the conflict without losing the module's other output. See [Facial composition](facial-composition.md) for the full per-region weighting model.

## Next steps

{% content-ref url="embodiment-editor.md" %}
[Embodiment Editor window](embodiment-editor.md)
{% endcontent-ref %}

{% content-ref url="character-rig-setup.md" %}
[Character rig setup](character-rig-setup.md)
{% endcontent-ref %}

{% content-ref url="embodiment-presets.md" %}
[Embodiment presets](embodiment-presets.md)
{% endcontent-ref %}
