---
title: Lip sync and animation issues
description: Fix missing mouth movement, wrong blendshape curves, and rig mismatch problems in the Convai Unreal Engine plugin lip sync system.
last_reviewed: 2026-06-04
---

Use this page to resolve problems with facial animation during character speech. Issues where the character produces no audio at all are covered in [Audio and microphone issues](audio-and-microphone-issues.md). For a full reference of `Convai Face Sync` component properties, see [Face Sync component reference](../features/lip-sync/face-sync-component-reference.md).

## No mouth movement during speech

**Symptom:** The character speaks (audio plays) but the mouth and face do not move.

**Cause — missing Face Sync component:** The `Convai Face Sync` component is not present on the Actor, so no facial data is requested from Convai.

**Fix:** Open the character Blueprint, add a `Convai Face Sync` component, and set `LipSyncMode` to the value that matches the rig. Compile and save.

**Verify:** Enter Play mode and confirm that the `Convai Face Sync` component appears in the Actor's component list at runtime.

---

**Cause — AnimGraph node not connected:** The `Convai Face Sync` AnimGraph node is placed in the Animation Blueprint but is not wired into the active pose chain.

**Fix:** Open the face Animation Blueprint. Confirm that the `Convai Face Sync` node's **Source Pose** pin receives the preceding pose and its **Output Pose** pin connects to the final output. Recompile the Animation Blueprint.

**Verify:** In the AnimGraph, the node should have no disconnected pins in the active path to the output.

---

**Cause — wrong chatbot component resolved:** The Actor has more than one `Convai Chatbot` component and the AnimGraph node auto-discovered the wrong one.

**Fix:** Explicitly connect the correct `Convai Chatbot` component reference to the **Convai Chatbot Component** pin on the `Convai Face Sync` AnimGraph node.

**Verify:** In Play-in-Editor (PIE), the character's face should animate when that specific chatbot component is active in a conversation.

## Mouth moves but the wrong curves animate

**Symptom:** Something on the face moves, but it is not the mouth — for example the eyes blink rapidly or unrelated shapes activate.

**Cause — `LipSyncMode` mismatch:** The `LipSyncMode` on the `Convai Face Sync` component does not match the curve names on the Skeletal Mesh. For example, the mode is set to `Viseme Based` but the mesh has MetaHuman CTRL curves.

**Fix:** Open the character Blueprint, select the `Convai Face Sync` component, and change `LipSyncMode` to the value that matches the rig:

| Rig type | Correct `LipSyncMode` |
|---|---|
| MetaHuman | `MetaHuman Blendshapes` |
| CC5 | `MetaHuman Blendshapes` |
| CC4 (standard export) | `ARKit Blendshapes` |
| CC4 (extended export) | `CC4 Extended Blendshapes` |
| Custom rig with OVR viseme curves | `Viseme Based` |

`LipSyncMode` can be set per-component in the **Details** panel or globally in **Edit > Project Settings > Convai** via the `LipSyncMode` property on `UConvaiSettings`.

**Verify:** Open the Skeletal Mesh in the editor and inspect the **Curves** list. Confirm that the curve names match what the selected mode produces.

## Frame starvation — mouth animates then freezes mid-speech

**Symptom:** Lip sync starts correctly but the face freezes part-way through a speech turn, then resumes or snaps to neutral.

**Cause:** The AnimGraph node has consumed all buffered frames before new ones arrived from the network. This is a timing issue, often more visible on high-latency connections.

**Fix:** Increase `StarvationBlendOutDuration` on the AnimGraph node (for example to `1.2`) so the face blends out gradually rather than snapping.

**Verify:** In PIE on a high-latency connection, the mouth should fade out smoothly during gaps rather than freezing at the last frame.

---

**Cause — interpolation disabled:** When `bEnableInterpolation` is `false` on the `Convai Face Sync` component, the component replays discrete frames without smoothing, which makes starvation gaps more visible.

**Fix:** Enable `bEnableInterpolation` on the `Convai Face Sync` component in the character Blueprint **Details** panel.

**Verify:** The transitions between frames should appear smoother in PIE.

## Custom blendshape remapping produces no output

**Symptom:** A `BlendshapeMapping` entry is configured but the target curve does not move.

**Cause — target curve name mismatch:** The `TargetNames` array in the `FConvaiBlendshapeParameters` entry does not match the exact curve name on the Skeletal Mesh. Curve names are case-sensitive.

**Fix:** Open the Skeletal Mesh asset in the editor, navigate to the **Curves** section, and copy the exact curve name. Paste it into the `TargetNames` entry.

**Verify:** Add a single test mapping entry, enter PIE, and confirm that the targeted curve responds.

---

**Cause — source name mismatch:** The key in the `BlendshapeMapping` table does not match the curve name that Convai delivers for the selected `LipSyncMode`.

**Fix:** Confirm the expected source curve names for the selected mode:

- `Viseme Based`: 15 OVR viseme names — `sil`, `PP`, `FF`, `TH`, `DD`, `kk`, `CH`, `SS`, `nn`, `RR`, `aa`, `E`, `ih`, `oh`, `ou`
- `ARKit Blendshapes`: 52 standard Apple ARKit curves plus 9 head and eye rotation curves
- `MetaHuman Blendshapes`: MetaHuman CTRL curve names

**Verify:** Temporarily clear the mapping. If the curve animates with 1:1 mapping, the source name is correct and the issue was in `TargetNames`.

## Face animates in editor but not in a packaged build

**Symptom:** Lip sync works in PIE but the face does not animate in a cooked build.

**Cause:** Curve assets or Animation Blueprint assets may not be included in the cook. Skeletal Mesh curves must be referenced by the Animation Blueprint or included in an asset list to survive cooking.

**Fix:** Confirm that the face Animation Blueprint is referenced by the character Blueprint or by a level that is included in the cook. If curves are stripped, add them to the asset's **Skeleton** and ensure the Skeleton asset is in a cooked package.

**Verify:** Run a Development cook and check the cook log for warnings about stripped curve tracks on the character's Skeleton.

{% hint style="info" %}
The global `LipSyncMode` in **Edit > Project Settings > Convai** applies to all `Convai Face Sync` components that do not override the mode locally. Set a per-component override when different characters in the same project use different rig types.
{% endhint %}

## Next steps

{% content-ref url="../features/lip-sync/face-sync-component-reference.md" %}
[Face Sync component reference](../features/lip-sync/face-sync-component-reference.md)
{% endcontent-ref %}

{% content-ref url="../features/lip-sync/troubleshooting-and-diagnostics.md" %}
[Lip sync troubleshooting and diagnostics](../features/lip-sync/troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
