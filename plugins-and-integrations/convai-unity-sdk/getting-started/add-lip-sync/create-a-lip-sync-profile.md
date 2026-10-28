---
title: Create a lip sync profile
description: >-
  Explains how to create a custom lip sync profile asset for a blendshape
  format beyond the three profiles the SDK bundles by default.
last_reviewed: "5.0.0-preview"
---

A lip sync profile defines the transport format identifier — it tells the SDK which blendshape channel names to expect from Convai.

{% hint style="warning" %}
The bundled profiles request transport tokens `arkit`, `mha`, and `cc4_extended`. A custom profile is useful only when Convai supports its transport format for your deployment. Creating a local asset does not add a server-side format.
{% endhint %}

For all standard setups, use one of the three bundled profiles and leave this page for advanced or future use.

{% stepper %}
{% step %}
### Create the asset

In the Project window, navigate to the folder where you want to store the profile. Right-click and select **Create > Convai > Lip Sync > Profile**. Name the asset descriptively — for example, `ConvaiLipSyncProfile_MyRig`.
{% endstep %}

{% step %}
### Configure the fields

Select the new asset to open it in the Inspector.

| Field                | Description                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------- |
| **Profile ID**       | Canonical local profile identifier, used to select the profile and its map. |
| **Display Name**     | Human-readable name shown in the Inspector. Does not affect runtime behavior.            |
| **Transport Token** | Token sent to Convai and expected on incoming data. It defaults to Profile ID; enable **Override default token** if it differs.                      |

{% hint style="danger" %}
**Transport Token** must match the format Convai sends. The bundled MetaHuman profile demonstrates the distinction: its Profile ID is `metahuman`, while its Transport Token is `mha`.
{% endhint %}
{% endstep %}

{% step %}
### Register and select the profile

Create a **Convai > Lip Sync > Profile Registry** asset from the Project window's **Create** menu under `Assets/Resources/LipSync/ProfileRegistries/`. Add your profile to its **Profiles** list. The catalog loads registry assets from that Resources path; an unregistered profile asset is not enough.

Return to the character's Convai Lip Sync component and select your profile in **Profile**. Assign a compatible map, then verify it with **Validator**. Higher-priority registries are applied after lower-priority registries.
{% endstep %}
{% endstepper %}

## Next steps

After creating the profile, create a map to route its channels to your rig's blendshape names.

{% content-ref url="create-a-custom-blendshape-map.md" %}
[Create a custom lip sync map](create-a-custom-blendshape-map.md)
{% endcontent-ref %}
