---
title: Troubleshooting and diagnostics
description: Diagnose and fix lip sync issues in the Convai Unreal Engine plugin — no mouth movement, frame starvation, wrong blendshape map, and rig mismatch.
last_reviewed: 2026-06-03
---

Use this page to identify and fix the most common lip sync problems. Each entry describes what you observe, what causes it, and what to change.

## No mouth movement during speech

**Symptom:** The character speaks (audio plays) but the mouth and face do not move.

**Cause — missing Face Sync component:** The `Convai Face Sync` component is not present on the Actor, so no facial data is requested from Convai.

**Fix:** Open the character Blueprint, add a `Convai Face Sync` component, and set `LipSyncMode` to the mode that matches the rig (for example `MetaHuman Blendshapes` for a MetaHuman). Compile and save.

**Verify:** Enter Play mode and confirm that the **Convai Face Sync** component appears in the Actor's component list at runtime.

---

**Cause — AnimGraph node not connected:** The `Convai Face Sync` AnimGraph node is placed in the Animation Blueprint but is not wired into the active pose chain.

**Fix:** Open the face Animation Blueprint. Confirm that the `Convai Face Sync` node's **Source Pose** pin receives the preceding pose, and its **Output Pose** pin connects to the final output. Recompile the Animation Blueprint.

**Verify:** In the AnimGraph, the node should have no disconnected pins in the active path to the output.

---

**Cause — wrong chatbot component resolved:** The Actor has more than one `Convai Chatbot` component and the AnimGraph node auto-discovered the wrong one.

**Fix:** Explicitly connect the correct `Convai Chatbot` component reference to the **Convai Chatbot Component** pin on the `Convai Face Sync` node.

**Verify:** In PIE, the character's face should animate when that specific chatbot component is active in a conversation.

## Mouth moves but the wrong curves animate

**Symptom:** Something on the face moves, but it is not the mouth — for example the eyes blink rapidly, or unrelated shapes activate.

**Cause — LipSyncMode mismatch:** The `LipSyncMode` on the `Convai Face Sync` component does not match the curve names on the Skeletal Mesh. For example, the mode is set to `VisemeBased` but the mesh has MetaHuman CTRL curves, or vice versa.

**Fix:** Open the character Blueprint, select the `Convai Face Sync` component, and change `LipSyncMode` to the value that matches the rig:

| Rig type | Correct LipSyncMode |
|---|---|
| MetaHuman | `MetaHuman Blendshapes` |
| CC5 | `MetaHuman Blendshapes` |
| CC4 (standard export) | `ARKit Blendshapes` |
| CC4 (extended export) | `CC4 Extended Blendshapes` |
| Custom rig with OVR viseme curves | `Viseme Based` |

`LipSyncMode` can also be set globally in **Edit > Project Settings > Convai > LipSync Mode**. The per-component value overrides the global setting when both are set.

**Verify:** Reopen the Skeletal Mesh in the editor and check the **Curves** list. Confirm that the curve names match what the selected mode produces.

## Frame starvation — mouth animates then freezes mid-speech

**Symptom:** Lip sync starts correctly but the face freezes part-way through a speech turn, then resumes or snaps to neutral.

**Cause:** The AnimGraph node has consumed all buffered frames before new ones arrived from the network. This is a timing issue, often more visible on high-latency connections.

**Fix:** Increase `StarvationBlendOutDuration` on the AnimGraph node (for example to `1.2`) so the face blends out gradually rather than snapping. This makes brief starvation gaps less visible.

**Verify:** In PIE on a throttled network, the mouth should fade out smoothly during gaps rather than freezing at the last frame.

---

**Cause — interpolation disabled:** When `bEnableInterpolation` is `false` on the `Convai Face Sync` component, the component replays discrete frames without smoothing between them, which can make gaps more visible.

**Fix:** Enable `bEnableInterpolation` on the `Convai Face Sync` component in the character Blueprint **Details** panel under **Convai | LipSync**.

**Verify:** The transitions between frames should appear smoother in PIE.

## Custom blendshape remapping produces no output

**Symptom:** A `BlendshapeMapping` entry is configured but the target curve does not move.

**Cause — target curve name mismatch:** The `TargetNames` array in the `FConvaiBlendshapeParameters` entry does not match the exact curve name on the Skeletal Mesh.

**Fix:** Open the Skeletal Mesh asset in the editor, navigate to the **Curves** section, and copy the exact curve name. Paste it into the `TargetNames` entry. Curve names are case-sensitive.

**Verify:** Add a single test entry in the mapping, enter PIE, and confirm that the targeted curve responds.

---

**Cause — source name mismatch:** The key in the `BlendshapeMapping` table does not match the curve name that Convai delivers for the selected `LipSyncMode`.

**Fix:** Confirm the source curve name by checking the mode's expected curve set:

- `VisemeBased`: 15 OVR viseme names (`sil`, `PP`, `FF`, `TH`, `DD`, `kk`, `CH`, `SS`, `nn`, `RR`, `aa`, `E`, `ih`, `oh`, `ou`)
- `BS_ARKit`: 61 ARKit blendshape curve names (52 standard Apple ARKit + 9 head/eye rotation curves)
- `BS_MHA`: MetaHuman CTRL curve names

Use the exact source name as the map key.

**Verify:** Remove or temporarily clear the mapping. If the curve animates with 1:1 mapping, the source name is correct and the issue was in `TargetNames`.

## Face animates in editor but not in a packaged build

**Symptom:** Lip sync works in PIE but the face does not animate in a cooked build.

**Cause:** Curve assets or Animation Blueprint assets may not be included in the cook. Skeletal Mesh curves must be referenced by the Animation Blueprint or included in an asset list to survive cooking.

**Fix:** Confirm that the face Animation Blueprint is referenced by the character Blueprint or by a level that is included in the cook. If curves are stripped, add them to the asset's **Skeleton** and ensure the Skeleton asset is in a cooked package.

**Verify:** Run a Development cook and check the cook log for warnings about stripped curve tracks on the character's Skeleton.

{% hint style="info" %}
Command-line overrides (`-LipSyncAnim*` flags) set during PIE do not carry over to packaged builds unless passed explicitly at launch. See the [Face Sync AnimGraph node reference](face-sync-anim-node-reference.md) for the full list of overridable properties.
{% endhint %}

## Next steps

{% content-ref url="face-sync-component-reference.md" %}
[Face Sync component reference](face-sync-component-reference.md)
{% endcontent-ref %}

{% content-ref url="face-sync-anim-node-reference.md" %}
[Face Sync AnimGraph node reference](face-sync-anim-node-reference.md)
{% endcontent-ref %}

{% content-ref url="../../troubleshooting/lip-sync-and-animation-issues.md" %}
[Lip sync and animation issues](../../troubleshooting/lip-sync-and-animation-issues.md)
{% endcontent-ref %}
