---
title: Profiles and mappings
description: >-
  Reference for the two ScriptableObject types — profiles and maps — that
  control how Convai blendshape data reaches your character's
  SkinnedMeshRenderer.
last_reviewed: "4.2.0"
---

The lip sync system uses two ScriptableObject types to describe how blendshape data flows from Convai to your character's mesh: **profiles** and **maps**. Most setups work with the bundled assets — create custom ones only when your rig uses non-standard blendshape names or a transport format not covered by the built-in profiles.

## What is a profile?

A **profile** defines the transport format — it tells the SDK which blendshape channel names to expect in the data stream from Convai. The profile's ID (e.g., `arkit`, `metahuman`, `cc4extended`) is what you enter in `ConvaiLipSyncComponent._lockedProfileId`.

**Three profiles are bundled:**

| Profile asset                      | ID            | Format                            |
| ---------------------------------- | ------------- | --------------------------------- |
| `ConvaiLipSyncProfile_ARKit`       | `arkit`       | 61 standard ARKit channels        |
| `ConvaiLipSyncProfile_MetaHuman`   | `metahuman`   | 275+ MetaHuman CTRL expressions   |
| `ConvaiLipSyncProfile_CC4Extended` | `cc4extended` | 240+ Character Creator 4 channels |

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

Create a custom map when your character's blendshape names differ from the expected names, or when you need to adjust weight multipliers to match your rig's calibration.

## When to create custom assets

| Situation                                               | Create                                                 |
| ------------------------------------------------------- | ------------------------------------------------------ |
| Your rig uses ARKit/MetaHuman/CC4 names exactly         | Nothing — use the bundled map (leave `_mapping` empty) |
| Your rig uses different names for standard blendshapes  | Custom **map** only                                    |
| You receive an ARKit stream but your rig uses CC4 names | Use the bundled `ARKitToCC4Extended` map               |
| Your character uses a completely custom blendshape set  | Custom **profile** + custom **map**                    |

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Create a lip sync profile</strong><br>Define a new transport format identifier for proprietary blendshape sets.</td><td><a href="create-a-lip-sync-profile.md">create-a-lip-sync-profile.md</a></td></tr><tr><td><strong>Create a custom blendshape map</strong><br>Route stream channels to your rig's actual blendshape names with per-channel tuning.</td><td><a href="create-a-custom-blendshape-map.md">create-a-custom-blendshape-map.md</a></td></tr></tbody></table>
