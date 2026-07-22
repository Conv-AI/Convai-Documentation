---
title: Profiles and mappings
description: >-
  Reference for the profile and map assets that control how Convai blendshape
  data reaches your character's face mesh, and when to create custom ones.
last_reviewed: "4.4.0"
---

The lip sync system uses two `ScriptableObject` types to describe how blendshape data flows from Convai to your character's mesh: **profiles** and **maps**. Most setups work with the bundled assets — create custom ones only when your rig uses non-standard blendshape names or a transport format not covered by the built-in profiles.

## What is a profile?

A **profile** defines the transport format — it tells the SDK which blendshape channel names to expect in the data stream from Convai. The profile's ID (e.g., `arkit`, `metahuman`, `cc4_extended`) is what you enter in `ConvaiLipSyncComponent._lockedProfileId`.

**Three profiles are bundled:**

| Profile asset                      | ID              | Format                            |
| ----------------------------------- | --------------- | --------------------------------- |
| `ConvaiLipSyncProfile_ARKit`       | `arkit`         | 61 standard ARKit channels        |
| `ConvaiLipSyncProfile_MetaHuman`   | `metahuman`     | 251 MetaHuman CTRL expressions    |
| `ConvaiLipSyncProfile_CC4Extended` | `cc4_extended`  | 170 Character Creator 4 channels  |

Create a custom profile only if your character uses a proprietary blendshape format that Convai streams under a custom ID. In practice, this is rare — most pipelines use one of the three bundled formats.

## What is a map?

A **map** routes the source blendshape channels (from the profile) to the actual blendshape names on your character's `SkinnedMeshRenderer`. It also lets you apply per-channel multipliers, offsets, and clamps.

**Four maps are bundled:**

| Map asset                                    | Routes                                  |
| -------------------------------------------- | --------------------------------------- |
| `ConvaiLipSyncDefaultMap_ARKit`              | ARKit → ARKit (passthrough)             |
| `ConvaiLipSyncDefaultMap_MetaHuman`          | MetaHuman → MetaHuman (passthrough)     |
| `ConvaiLipSyncDefaultMap_CC4Extended`        | CC4Extended → CC4Extended (passthrough) |
| `ConvaiLipSyncDefaultMap_ARKitToCC4Extended` | ARKit → CC4Extended (conversion)        |

When `ConvaiLipSyncComponent._mapping` is left empty, the SDK selects the matching passthrough map automatically based on the locked profile ID.

`ConvaiLipSyncMapAsset.Mappings` exposes its entries as `IReadOnlyList<BlendshapeMappingEntry>` — code that reads a map at runtime cannot add, remove, or reorder entries. Author mappings in the Editor; see [Create a custom lip sync map](create-a-custom-blendshape-map.md).

Create a custom map when your character's blendshape names differ from the expected names, or when you need to adjust weight multipliers to match your rig's calibration.

## When to create custom assets

| Situation                                               | Create                                                 |
| ------------------------------------------------------- | ------------------------------------------------------ |
| Your rig uses ARKit/MetaHuman/CC4 names exactly         | Nothing — use the bundled map (leave `_mapping` empty) |
| Your rig uses different names for standard blendshapes  | Custom **map** only                                    |
| You receive an ARKit stream but your rig uses CC4 names | Use the bundled `ARKitToCC4Extended` map               |
| Your character uses a completely custom blendshape set  | Custom **profile** + custom **map**                    |

## Next steps

{% content-ref url="create-a-lip-sync-profile.md" %}
[Create a lip sync profile](create-a-lip-sync-profile.md)
{% endcontent-ref %}

{% content-ref url="create-a-custom-blendshape-map.md" %}
[Create a custom lip sync map](create-a-custom-blendshape-map.md)
{% endcontent-ref %}
