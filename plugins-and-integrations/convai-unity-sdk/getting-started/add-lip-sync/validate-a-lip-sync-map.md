---
title: Validate a lip-sync map
description: >-
  Check a lip-sync profile against a character's meshes, find missing or
  disabled mappings, and export a report before testing the talking avatar.
last_reviewed: "5.0.0-preview"
---

Use the **Lip Sync Mapping Validator** to check whether each source blendshape resolves to a target on the character's meshes. This validates the mapping structure; a live conversation is still needed to judge facial movement and audio timing.

## Check the mapping

{% stepper %}
{% step %}
### Open the validator from the character

Select a character with `ConvaiLipSyncComponent`. In its Inspector, choose **Validator**. The **Lip Sync Validator** window opens with that component selected.
{% endstep %}

{% step %}
### Confirm the configuration

Check **Lip Sync Component**, **Mapping Asset** and **Target Meshes**. When a component is assigned, **Profile** follows its selected profile. To inspect an unbound mapping, clear the component and choose the profile and meshes explicitly. Use **Add Mesh Slot** for additional renderers.
{% endstep %}

{% step %}
### Refresh and inspect results

Choose **Refresh Validation**. The validator rescans the component, meshes and mapping. Use **Search blendshapes** and the result filters to find missing targets or disabled mappings. The result table shows the source, target names, multiplier and status.

Correct target names in the [mapping asset](create-a-custom-blendshape-map.md), then refresh. A source may map to several targets; check that this is intentional. No meshes assigned or no analysis performed is an incomplete check, not a passing result.
{% endstep %}

{% step %}
### Verify motion and retain evidence

Choose **Export Report** to save the validation results. Enter Play Mode and test a short conversation with the character. Inspect mouth movement, settling and timing; a structurally valid map can still use unsuitable multipliers or the wrong facial mesh.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the reviewed 5.0 Lip Sync Mapping Validator with a real character component, selected Profile, Mapping Asset and Target Meshes, plus Validation Results showing recognizable mapped and missing-target rows. Use non-sensitive sample assets.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-lip-sync-validator.png" alt="Lip Sync Mapping Validator configuration and per-blendshape validation results"><figcaption><p>TODO: Profile-to-mesh mapping results with the controls needed to refresh and export.</p></figcaption></figure>

If the face stays still despite valid target names, confirm that the session supplies the profile's expected facial data, the component is enabled and the correct renderers are assigned. See [Add lip sync](README.md) for playback and latency controls.
