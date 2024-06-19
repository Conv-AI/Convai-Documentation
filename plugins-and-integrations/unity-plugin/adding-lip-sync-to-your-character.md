---
description: >-
  Learn to add lip sync to your Unity characters using Convai. Improve realism
  and interactivity.
---

# Adding Lip-Sync to your Character

## Step 1: Add Lip-Sync Component

To add Lip-Sync to your character, follow these steps.

{% hint style="info" %}
Convai's Lip-Sync uses [**OVR**](https://developer.oculus.com/documentation/unity/audio-ovrlipsync-viseme-reference/) or **Reallusion CC4 Extended** (Reallusion CC4+) Blendshapes. The lip-sync will work best with models that have **OVR** or **Reallusion CC4 Extended** (Reallusion CC4+) compatible Blendshapes.&#x20;
{% endhint %}

### Using Unity Inspector

Select the character GameObject and click Add Component in the Inspector.

<figure><img src="../../.gitbook/assets/image (259).png" alt=""><figcaption></figcaption></figure>

Select `Convai Lip Sync` to add the Lip Sync component.

<figure><img src="../../.gitbook/assets/image (258).png" alt=""><figcaption></figcaption></figure>

### Using Convai NPC Component

You can also select Add Components.

<figure><img src="../../.gitbook/assets/image (2) (1) (1).png" alt=""><figcaption></figcaption></figure>

Select the Lip-Sync checkmark and click Apply Changes.

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

## Step 2: Set up the Lip Sync Component

### For Reallusion Character Models

In the new component, select the type of lipsync, and assign the Skinned Mesh Renderer with the Facial Blendshapes (here for Reallusion Characters, `CC_Base_Body`, `CC_Base_Teeth` and `CC_Base_Tongue`)  and the game objects corresponding to the bones for Jaw and Tongue (here for Reallusion Characters, `CC_Base_JawRoot` and `CC_Base_Tongue01`). Feel free to adjust the position of the tongue with the Tongue Bone Offset field. &#x20;

{% hint style="danger" %}
The screenshot shows "Reallusion Plus" already selected. You must now manually change this **option from "OVR" to "Reallusion Plus"** for the lip sync to work. This was due to a recent Unity update that changed the default settings.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (257).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
If your character's mouth seems not to be opening enough for a proper lip sync, this could indicate an issue with the animator or animations.
{% endhint %}

### For Ready Player Me Character Models

**For Ready Player Me models**, the type of lipsync will be `OVR` and the appropriate facial skinned mesh renderers for the Head will be `Renderer_Head` and the appropriate facial skinned mesh renderer for the Teeth will be `Renderer_Teeth`. There is no need for adding any of the other mesh renderers or bones.&#x20;

<figure><img src="../../.gitbook/assets/image (277) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The above process of assigning the skinned mesh renderer is not necessary. The `ConvaiLipSync.cs` script is capable of assigning the necessary skinned mesh renderers by itself if you have left the fields empty.
{% endhint %}

To resolve common issues caused by the animator and animations, follow the troubleshooting guides below.

[animations-have-facial-blendshapes.md](troubleshooting-guide/animations-have-facial-blendshapes.md "mention")
