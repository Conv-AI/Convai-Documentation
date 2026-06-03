---
title: Face Sync component reference
description: Property reference for the Convai Face Sync component and all six lip-sync mode values with rig compatibility guidance for MetaHuman, CC4, CC5, and custom rigs.
last_reviewed: 2026-06-03
---

`UConvaiFaceSyncComponent` is a Scene Component (Blueprint display name **"Convai Face Sync"**) that receives server-precomputed facial animation data from Convai, buffers it, and exposes the current blendshape frame each tick. It implements `IConvaiLipSyncInterface` and sets `RequiresPrecomputedFaceData()` to `true`, which instructs the audio streamer to request facial data from the server.

Add it to the same Actor as `UConvaiChatbotComponent`. The `FAnimNode_ConvaiFaceSync` AnimGraph node reads from it automatically when both components are on the same Actor.

## Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `LipSyncMode` | `EC_LipSyncMode` | `BS_MHA` | Selects the blendshape set the server produces and the curve names the AnimGraph node expects. Must match the curves available on the character's Skeletal Mesh. |
| `bEnableInterpolation` | `bool` | `false` | When `true`, the component interpolates between consecutive blendshape frames to smooth playback. Exposed in the **Details** panel under **Convai\|LipSync**; not exposed as a Blueprint read/write pin. |

## EC_LipSyncMode values

`EC_LipSyncMode` is a Blueprint-exposed enum (`UENUM(BlueprintType)`) defined in `ConvaiDefinitions.h`.

| Value | Display name | Compatible rigs | Notes |
|---|---|---|---|
| `Off` | `Off` | — | Disables lip sync. No facial data is requested from Convai. |
| `Auto` | `Auto` | Determined at runtime | Delegates to the attached `UConvaiFaceSyncComponent`'s own `GetLipSyncMode()` result to select the blendshape format. The selection is made client-side, not by the server. |
| `VisemeBased` | `Viseme Based` | Custom rigs with OVR viseme curves | Produces 15 OVR viseme curve names: `sil`, `PP`, `FF`, `TH`, `DD`, `kk`, `CH`, `SS`, `nn`, `RR`, `aa`, `E`, `ih`, `oh`, `ou`. |
| `BS_MHA` | `MetaHuman Blendshapes` | MetaHuman, CC5 | Produces MetaHuman CTRL curve names. This is the default mode. |
| `BS_ARKit` | `ARKit Blendshapes` | CC4 | Produces 61 ARKit blendshape curve names (52 standard Apple ARKit + 9 head/eye rotation curves). |
| `BS_CC4_Extended` | `CC4 Extended Blendshapes` | CC4 with extended blendshape sets | Produces CC4 Extended curve names. Use when the CC4 character was exported with the extended blendshape option enabled in Character Creator 4. |

### Choosing the right mode

The `LipSyncMode` value must correspond to the curve names present on the character's Skeletal Mesh asset. If the mode does not match the rig, the AnimGraph node receives data but finds no matching curves to write, and the face does not animate.

- **MetaHuman characters:** use `BS_MHA`.
- **CC5 characters:** use `BS_MHA`.
- **CC4 characters (standard export):** use `BS_ARKit`.
- **CC4 characters (extended blendshape export):** use `BS_CC4_Extended`.
- **Custom rigs with OVR viseme targets:** use `VisemeBased`.

## Related reference

{% content-ref url="face-sync-anim-node-reference.md" %}
[Face Sync AnimGraph node reference](face-sync-anim-node-reference.md)
{% endcontent-ref %}

{% content-ref url="how-lip-sync-works.md" %}
[How lip sync works](how-lip-sync-works.md)
{% endcontent-ref %}
