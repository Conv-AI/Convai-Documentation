---
title: Create a lip sync profile
description: >-
  Create a ConvaiLipSyncProfile asset to define a custom transport format
  identifier for blendshape formats beyond the three bundled profiles.
last_reviewed: "4.4.0"
---

A lip sync profile defines the transport format identifier — it tells the SDK which blendshape channel names to expect from Convai.

{% hint style="warning" %}
Convai currently streams blendshape data in three formats only: `arkit`, `metahuman`, and `cc4_extended`. A custom profile is only useful if Convai explicitly supports a custom format for your deployment. Creating a profile with an unsupported format ID will result in no blendshape data being received.
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
| **Profile ID**       | Transport format identifier. Must exactly match the format ID Convai streams for this character. |
| **Display Name**     | Human-readable name shown in the Inspector. Does not affect runtime behavior.            |
| **Transport Format** | Network transport format string — typically the same as Profile ID.                      |

{% hint style="danger" %}
**Profile ID** must exactly match the identifier Convai uses when streaming blendshape data. A mismatch causes the SDK to fall back to a no-op map — no blendshapes animate.
{% endhint %}
{% endstep %}

{% step %}
### Assign the profile ID to the component

Set `ConvaiLipSyncComponent._lockedProfileId` to the **Profile ID** string you defined. The SDK looks up this profile from the registry at runtime.
{% endstep %}
{% endstepper %}

## Next steps

After creating the profile, create a map to route its channels to your rig's blendshape names.

{% content-ref url="create-a-custom-blendshape-map.md" %}
[Create a custom lip sync map](create-a-custom-blendshape-map.md)
{% endcontent-ref %}
