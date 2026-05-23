---
title: Create a lip sync profile
description: >-
  Create a ConvaiLipSyncProfile asset to define a custom transport format
  identifier when your rig uses a blendshape format not covered by the bundled
  ARKit, MetaHuman, or CC4 Extended profiles.
last_reviewed: "4.2.0"
---

A lip sync profile defines the transport format identifier — it tells the SDK which blendshape channel names to expect from Convai. Create a custom profile only when your character uses a blendshape format that Convai streams under a custom ID not covered by the three bundled profiles (`arkit`, `metahuman`, `cc4extended`).

{% hint style="info" %}
If your character uses standard ARKit, MetaHuman, or CC4 Extended naming, use the bundled profiles. A custom profile is only needed for proprietary or non-standard transport formats.
{% endhint %}

{% stepper %}
{% step %}
### Create the asset

In the Project window, navigate to the folder where you want to store the profile. Right-click and select **Create > Convai > Lip Sync Profile**. Name the asset descriptively — for example, `ConvaiLipSyncProfile_MyRig`.
{% endstep %}

{% step %}
### Configure the fields

Select the new asset to open it in the Inspector.

| Field                | Description                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------- |
| **Profile ID**       | Transport format identifier. Must match the format ID Convai streams for this character. |
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

You will also need a matching map asset that routes the custom channels to your rig's blendshape names.

## Usage example

**Scenario:** A military training simulation uses a proprietary soldier character rigged with a custom set of 30 facial blendshapes. Convai streams these under the format ID `"militaryrig-v1"`.

**Setup:**

* Create `ConvaiLipSyncProfile_MilitaryRig.asset`
* Profile ID: `militaryrig-v1`
* Display Name: `Military Rig V1`
* Transport Format: `militaryrig-v1`
* Set `_lockedProfileId` on the character's `ConvaiLipSyncComponent` to `militaryrig-v1`

**Expected outcome:** The SDK streams and buffers the correct blendshape channels for this character. Pair with a custom map that routes those channels to the rig's blendshape names.

## Next steps

After creating the profile, create a map to route its channels to your rig's blendshape names.

{% content-ref url="create-a-custom-blendshape-map.md" %}
[Create a custom blendshape map](create-a-custom-blendshape-map.md)
{% endcontent-ref %}
