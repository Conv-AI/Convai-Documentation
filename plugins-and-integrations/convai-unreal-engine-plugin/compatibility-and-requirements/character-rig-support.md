---
title: Character rig support
description: Which character rigs work with the Convai Unreal Engine plugin, what setup each requires, and where to find the rig-specific setup guides.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin drives facial animation through the `UConvaiFaceSyncComponent`, which outputs facial animation data controlled by the `EC_LipSyncMode` enum. Blendshape modes output blendshape channels; `VisemeBased` mode outputs viseme values. The lip sync mode you select determines which rig types are compatible.

## Supported rigs

| Rig type | Lip sync mode | Out-of-the-box | Additional setup |
|---|---|---|---|
| [MetaHuman](../getting-started/set-up-a-metahuman-character.md) | `MetaHuman Blendshapes` (`BS_MHA`) | Yes; this is the default mode | Bundled `Convai_MetaHuman_BodyAnim` and `Convai_MetaHuman_FaceAnim` animation Blueprints included |
| [Reallusion Character Creator (CC4 and CC5)](https://www.reallusion.com/auto-setup/unreal-engine/default.html) | CC5: `MetaHuman Blendshapes` (`BS_MHA`); CC4: `ARKit Blendshapes` (`BS_ARKit`) or `CC4 Extended Blendshapes` (`BS_CC4_Extended`) | No | Follow the [Reallusion setup guide](../getting-started/set-up-a-reallusion-cc-character.md) for animation Blueprint setup |
| ARKit-compatible rigs | `ARKit Blendshapes` (`BS_ARKit`) | No | Configure `LipSyncMode` to `BS_ARKit`; wire 61 blendshape channels to your rig |
| Viseme-based rigs | `Viseme Based` (`VisemeBased`) | No | Configure `LipSyncMode` to `VisemeBased`; map 15 OVR visemes to your rig |
| Single-mesh generic rigs | `Auto` or `Off` | Partial | No facial animation without a compatible mode configured |

## MetaHuman characters

MetaHuman is the default rig target. The plugin ships with `Convai_MetaHuman_BodyAnim` and `Convai_MetaHuman_FaceAnim` under `Content/MetaHumans/Animations/`, and sets `LipSyncMode` to `BS_MHA` by default on `UConvaiFaceSyncComponent`. No separate animation Blueprint download is required for MetaHuman setup.

The `GetBodyAndFaceSkeletalMeshComponents` utility function (Blueprint-callable, category `Convai|Utilities`) resolves the body and face `Skeletal Mesh Component` references on a MetaHuman-style `Actor` automatically using bone-name heuristics. MetaHuman rigs that separate the face mesh from the body mesh are handled correctly.

Use the MetaHuman setup guide for the rig-specific setup flow.

{% content-ref url="../getting-started/set-up-a-metahuman-character.md" %}
[Set up a MetaHuman character](../getting-started/set-up-a-metahuman-character.md)
{% endcontent-ref %}

{% embed url="https://youtu.be/4fMCKkrfyaA" %}
MetaHuman character setup walkthrough
{% endembed %}

## Reallusion Character Creator (CC4 and CC5)

[Reallusion Character Creator](https://www.reallusion.com/auto-setup/unreal-engine/default.html) CC4 and CC5 characters use a separate animation Blueprint workflow from the MetaHuman setup. The plugin includes `FixCC5LipsyncPostProcessBlendshapes` (Blueprint-callable, category `Convai|LipSync`) to apply a post-process fix for CC5 rigs that use `ExpBoneData` in their post-process animation instance.

{% hint style="info" %}
Reallusion setup uses a separate Convai animation Blueprint. Follow the Reallusion setup guide before assigning a CC4 or CC5 character to your scene.
{% endhint %}

After the Reallusion animation Blueprint is assigned, set `LipSyncMode` on the `UConvaiFaceSyncComponent` attached to your CC character based on the rig generation: use `MetaHuman Blendshapes` (`BS_MHA`) for CC5, and `ARKit Blendshapes` (`BS_ARKit`) for CC4. For CC4 rigs that drive the extended Reallusion blendshape set, use `CC4 Extended Blendshapes` (`BS_CC4_Extended`) instead.

Use the Reallusion setup guide for the download and animation Blueprint assignment steps.

{% content-ref url="../getting-started/set-up-a-reallusion-cc-character.md" %}
[Set up a Reallusion character](../getting-started/set-up-a-reallusion-cc-character.md)
{% endcontent-ref %}

{% embed url="https://www.youtube.com/watch?v=nyPNP-S92QI" %}
Reallusion CC character setup walkthrough
{% endembed %}

## ARKit-compatible rigs

Any rig that exposes ARKit-style blendshape targets can use `BS_ARKit` mode. The plugin drives 61 blendshape channels in this mode: the 52 standard ARKit face targets plus 9 head and eye rotation channels (`HeadYaw`, `HeadPitch`, `HeadRoll`, `LeftEyeYaw`, `LeftEyePitch`, `LeftEyeRoll`, `RightEyeYaw`, `RightEyePitch`, `RightEyeRoll`). Set `LipSyncMode` to `ARKit Blendshapes` on the `UConvaiFaceSyncComponent` and wire the blendshape output to your rig's animation Blueprint.

## Viseme-based rigs

`VisemeBased` mode outputs 15 OVR viseme values (named `sil`, `PP`, `FF`, `TH`, `DD`, `kk`, `CH`, `SS`, `nn`, `RR`, `aa`, `E`, `ih`, `oh`, `ou`). Any rig that maps those 15 viseme names to morph targets or bone poses can use this mode.

## Rig detection utility

`GetBodyAndFaceSkeletalMeshComponents` inspects an `Actor`'s `Skeletal Mesh Component` references and resolves the body and face meshes using bone-name heuristics. It handles:

- Actors with a single skeletal mesh — the mesh becomes the body, face output is `null`.
- Actors with two or more skeletal meshes — each mesh is scored against body token bones (`pelvis`, `hand`, `neck`, and others) and face token bones (`eye`, `jaw`, `brow`, and others); the highest-scoring mesh wins each role.
- Actors with no skeletal mesh components — both outputs are `null`.

This function is intended for MetaHuman-style rigs but also handles single-mesh and unrecognized rigs without crashing.

## Next steps

After confirming rig support, check the network requirements before installing or validating the plugin.

{% content-ref url="network-and-api-requirements.md" %}
[Network and API requirements](network-and-api-requirements.md)
{% endcontent-ref %}
