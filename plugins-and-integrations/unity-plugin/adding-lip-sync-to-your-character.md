# Adding Lip-Sync to your Character

## Step 1: Add Lip-Sync Component

To add Lip-Sync to your character, follow these steps.

{% hint style="info" %}
Convai's Lip-Sync uses [**OVR**](https://developer.oculus.com/documentation/unity/audio-ovrlipsync-viseme-reference/) or **Reallusion CC4 Extended** (Reallusion CC4+) Blendshapes. The lip-sync will work best with models that have **OVR** or **Reallusion CC4 Extended** (Reallusion CC4+) compatible Blendshapes.&#x20;
{% endhint %}

### Using Unity Inspector

Select the character GameObject and click Add Component in the Inspector.

<figure><img src="../../.gitbook/assets/image (228).png" alt=""><figcaption></figcaption></figure>

Select `Convai Lip Sync` to add the Lip Sync component.

<figure><img src="../../.gitbook/assets/image (227).png" alt=""><figcaption></figcaption></figure>

### Using Convai NPC Component

You can also select Add Components.

<figure><img src="../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

Select the Lip-Sync checkmark and click Apply Changes.

<figure><img src="../../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

## Step 2: Set up the Lip Sync Component

### For Reallusion Character Models

In the new component, select the type of lipsync, and assign the Skinned Mesh Renderer with the Facial Blendshapes (here for Reallusion Characters, `CC_Base_Body`, `CC_Base_Teeth` and `CC_Base_Tongue`)  and the game objects corresponding to the bones for Jaw and Tongue (here for Reallusion Characters, `CC_Base_JawRoot` and `CC_Base_Tongue01`). Feel free to adjust the position of the tongue with the Tongue Bone Offset field. &#x20;

{% hint style="warning" %}
Currently, only Reallusion Plus and OVR are supported as a type of lip sync.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (226).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
If your character's mouth seems not to be opening enough for a proper lip sync, this could indicate an issue with the animator or animations.
{% endhint %}

### For Ready Player Me Character Models

**For Ready Player Me models**, the type of lipsync will be `OVR` and the appropriate facial skinned mesh renderers for the Head will be `Renderer_Head` and the appropriate facial skinned mesh renderer for the Teeth will be `Renderer_Teeth`. There is no need for adding any of the other mesh renderers or bones.&#x20;

<figure><img src="../../.gitbook/assets/image (271).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The above process of assigning the skinned mesh renderer is not necessary. The `ConvaiLipSync.cs` script is capable of assigning the necessary skinned mesh renderers by itself if you have left the fields empty.
{% endhint %}

To resolve common issues caused by the animator and animations, follow the troubleshooting guides below.

[animations-have-facial-blendshapes.md](troubleshooting-guide/animations-have-facial-blendshapes.md "mention")
