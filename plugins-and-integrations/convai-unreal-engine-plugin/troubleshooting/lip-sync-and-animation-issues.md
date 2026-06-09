---
title: Lip sync and animation issues
description: Fix missing mouth movement, wrong blendshape curves, frame starvation, and packaged build animation failures in the Convai Unreal Engine plugin.
last_reviewed: 2026-06-06
---

Use this page to resolve problems with facial animation during character speech. Issues where the character produces no audio at all are covered in [Audio and microphone issues](audio-and-microphone-issues.md). For a full reference of `Convai Face Sync` component properties, see [Face Sync component reference](../features/lip-sync/face-sync-component-reference.md).

{% hint style="info" %}
**Not sure which `LipSyncMode` to use?** Match your rig to the table below before investigating further — most mouth-movement problems are caused by a `LipSyncMode` mismatch.

| Rig type | Correct `LipSyncMode` |
| --- | --- |
| MetaHuman | `MetaHuman Blendshapes` |
| CC5 | `MetaHuman Blendshapes` |
| CC4 (standard export) | `ARKit Blendshapes` |
| CC4 (extended export) | `CC4 Extended Blendshapes` |
| Custom rig with OVR viseme curves | `Viseme Based` |
{% endhint %}

## Choose the right troubleshooting path

Start with the top-level checks on this page when you are not sure whether the issue is setup, audio, or rig selection. Move to the feature troubleshooting page when the `Convai Face Sync` component is present and you need to inspect AnimGraph node properties, blendshape remapping, smoothing, starvation, or command-line overrides.

| What you observe | Start here |
| --- | --- |
| Character produces no audio and no mouth movement | [Audio and microphone issues](audio-and-microphone-issues.md) |
| Character speaks but the face does not move | This page, then [Troubleshooting and diagnostics](../features/lip-sync/troubleshooting-and-diagnostics.md) |
| Mouth moves but the wrong facial curves animate | This page, then [Face Sync component reference](../features/lip-sync/face-sync-component-reference.md) |
| Lip sync starts, then freezes or fades during speech | [Troubleshooting and diagnostics](../features/lip-sync/troubleshooting-and-diagnostics.md) |
| Custom curve remapping does not work | [Troubleshooting and diagnostics](../features/lip-sync/troubleshooting-and-diagnostics.md) |

## No mouth movement during speech

**Symptom:** The character speaks, but the mouth and face do not move.

**Cause — missing Face Sync component:** The Actor does not have a `Convai Face Sync` component, so no facial animation data is requested.

**Fix:** Open the character Blueprint, add a `Convai Face Sync` component, and set `LipSyncMode` to the value that matches the rig. Compile and save.

**Verify:** Enter Play mode and confirm that the `Convai Face Sync` component is present on the character Actor.

---

**Cause — Face Sync AnimGraph node is not in the active pose path:** The node exists in the Animation Blueprint but its `Source Pose` and `Output Pose` pins are not connected to the pose chain that reaches the final animation output.

**Fix:** Open the face Animation Blueprint and connect the `Convai Face Sync` AnimGraph node into the active pose path.

**Verify:** Recompile the Animation Blueprint. The node should have no disconnected pins in the active path to the output.

## Mouth moves but the wrong curves animate

**Symptom:** The face moves, but the movement does not match speech. For example, unrelated facial controls activate instead of mouth shapes.

**Cause — `LipSyncMode` mismatch:** The selected `LipSyncMode` does not match the curve names on the Skeletal Mesh.

**Fix:** Select the `Convai Face Sync` component in the character Blueprint and set `LipSyncMode` to the rig-specific value in the table at the top of this page. For project-wide defaults, use **Edit > Project Settings > Plugins > Convai** and check `Lip Sync Mode`.

**Verify:** Open the Skeletal Mesh in the editor and inspect the **Curves** list. The selected mode should produce curve names that exist on the mesh.

{% hint style="warning" %}
Use per-component `LipSyncMode` values when one project contains multiple rig types. A project-wide value can make every character of a different rig type animate incorrectly.
{% endhint %}

## Lip sync freezes or drifts during speech

**Symptom:** Lip sync starts correctly, then freezes, fades out, or lags behind the audio.

**Cause:** This usually comes from timing settings rather than character setup. Source-backed controls include `OutputFPS`, `FramesBufferDuration`, `LipSyncTimeOffset`, `bEnableInterpolation`, and the AnimGraph node's `StarvationBlendOutDuration`.

**Fix:** Use the feature troubleshooting page to adjust the timing control that matches the symptom. Do not change several timing values at once; make one change, test in Play In Editor, then continue.

**Verify:** The mouth should remain synchronized with the spoken audio through the full response.

{% content-ref url="../features/lip-sync/troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](../features/lip-sync/troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

## Face animates in editor but not in a packaged build

**Symptom:** Lip sync works in PIE but the face does not animate in a cooked build.

**Cause:** Curve assets or Animation Blueprint assets may not be included in the cook. Skeletal Mesh curves must be referenced by the Animation Blueprint or included in an asset list to survive cooking.

**Fix:** Confirm that the face Animation Blueprint is referenced by the character Blueprint or by a level that is included in the cook. If curves are stripped, add them to the asset's **Skeleton** and ensure the Skeleton asset is in a cooked package.

**Verify:** Run a Development cook and check the cook log for warnings about stripped curve tracks on the character's Skeleton.

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
