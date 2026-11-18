---
title: Character rig setup
description: Configure a character's rig so Convai automatically detects its facial blendshape convention and bones, and resolve low-confidence detection.
last_reviewed: "4.5.0"
---

Every embodied character needs a mapping from its skeleton and face mesh to the semantic bones and blendshapes the embodiment modules read. Use this page to check what Convai detected on a character's rig, fix a low-confidence result, or map a rig that uses a naming convention Convai does not recognize.

## Prerequisites

- A character `GameObject` with a `SkinnedMeshRenderer` face mesh that has blendshapes
- An `Animator` on the character (humanoid or generic)
- At least one embodiment module (Gaze, Body Animation, Body Language, Conversation Flow, or Emotion) added to the character, since that is what triggers Convai to resolve a rig binding

## Let Convai detect the rig automatically

Convai adds the `Character Rig` component (`Convai/Embodiment/Character Rig` in the Add Component menu) to a character's root the first time an embodiment module needs a rig binding. You do not add it yourself in the common case.

When the component is added, it scans the character hierarchy for `SkinnedMeshRenderer` components with blendshapes and matches their names against four built-in conventions: **Apple ARKit**, **Reallusion Character Creator 3**, **Epic MetaHuman**, and **Reallusion Character Creator 4 (Extended)**. It also resolves the semantic bones (`Hips`, `Spine`, `Head`, and 15 others) from the character's humanoid avatar when one is present, falling back to name matching otherwise.

Open the **Character Rig** component in the Inspector to see the result:

- **Character Type** reports the detected **Rig type** and a **Match** strength — `Strong`, `Partial`, or `Weak` — or `Set by you` if you picked a type manually
- **Bones Convai Found** lists all 18 semantic bones and what each resolved to
- **Face Shapes Convai Found** lists every semantic blendshape and the mesh and index it resolved to, or `not found on this rig`

{% hint style="success" %}
Detection succeeded when **Character Type** shows a recognized rig type and neither the Hips, Spine, nor Head bone is reported missing. The Inspector header reads **Ready** in that state.
{% endhint %}

## Fix a low-confidence detection

If the Inspector warns that face shapes were only partially recognized, or that no convention matched at all, you have two options before falling back to a custom map:

1. **Pick the rig type yourself.** Open the **Rig Type** field under **Character Type** and select the correct convention (**Apple ARKit**, **Reallusion Character Creator 3**, **Epic MetaHuman**, or **Reallusion Character Creator 4 (Extended)**) instead of leaving it on **Detect automatically**. This skips detection and applies that convention's name table directly.
2. **Assign missing bones manually.** If **Bones Convai Found** reports a missing `Hips`, `Spine`, or `Head` bone, expand **Custom Rig Setup** and assign the correct `Transform` to the matching override field. The transform must belong to the character's own hierarchy. Click **Lock In What Convai Found** to copy every bone Convai already resolved into these override fields, so they stay fixed even if the model is re-imported or renamed.

After any change, click **Re-scan This Character** to rebuild the resolution tables, or call `Rebuild()` from a script.

## Map a custom rig convention

Use a custom convention map when a character's face mesh uses blendshape names that do not match any of the four built-in conventions.

1. Create a `CustomRigConventionMap` asset: **Assets > Create > Convai > Embodiment > Custom Rig Convention Map**.
2. Add one entry per semantic blendshape from the `StandardBlendshape` enum you want to drive, and set each entry's blendshape name to the name on your mesh. Leave an entry's name empty to skip that semantic blendshape on this rig.
3. On the **Character Rig** component, set **Rig Type** to **Custom — I will map the names myself**, then assign the asset to the **Custom Convention Map** field.
4. Click **Re-scan This Character**.

{% hint style="warning" %}
Bone resolution still runs through the humanoid avatar or name matching when **Rig Type** is `Custom` — only blendshape resolution reads the custom map. Assign bone overrides under **Custom Rig Setup** separately if the avatar does not resolve them.
{% endhint %}

## Verify the rig setup

Check **Bones Found** and **Face Shapes Found** in the Inspector header: a healthy rig shows all critical bones resolved and a recognized rig type with no warning box. From a script, read `DetectedConvention` and `DetectionConfidence` on the `Character Rig` component, or call `TryGetBone(StandardBone, out Transform)` and `TryGetBlendshape(StandardBlendshape, out SkinnedMeshRenderer, out int)` to confirm a specific semantic identifier resolves.

Not every rig provides every bone or blendshape. `UpperChest` and the eye bones are optional — Gaze supports head-only aiming when eye bones are absent — so their absence alone does not indicate a setup problem.

## Next steps

{% content-ref url="how-embodiment-works.md" %}
[How embodiment works](how-embodiment-works.md)
{% endcontent-ref %}

{% content-ref url="facial-composition.md" %}
[Facial composition](facial-composition.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot embodiment](troubleshooting.md)
{% endcontent-ref %}
