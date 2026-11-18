---
title: Choose a built-in lip sync profile
description: Choose the facial data format for a character, replace an older custom profile selection, and verify the mapping against the character mesh.
last_reviewed: "5.0.0-pre.1"
---

Choose a built-in lip sync profile for the facial data Convai sends. To animate a mesh with different blendshape names, keep that profile and create a mapping asset for the mesh.

{% hint style="warning" %}
Older SDK versions supported custom profile assets and registries. The 5.0 profile catalog contains the built-in profiles. Replace a custom registry selection on each affected character before testing playback.
{% endhint %}

## Choose a profile for the character

{% stepper %}
{% step %}
### Select the incoming format

Select the character's `ConvaiLipSyncComponent` and choose the built-in **Profile** that matches the incoming stream. [Lip sync profiles and mappings](profiles-and-mappings.md) lists the formats.
{% endstep %}

{% step %}
### Map the channels to the face

Assign the facial renderers. If their blendshape names differ from the built-in map, [create a custom lip sync map](create-a-custom-blendshape-map.md) for the selected profile and assign it under **Mapping**.
{% endstep %}

{% step %}
### Verify the mouth moves

[Validate the map](validate-a-lip-sync-map.md) to find missing targets. Enter Play Mode and check that the mouth follows an audible reply and settles at the end.
{% endstep %}
{% endstepper %}
