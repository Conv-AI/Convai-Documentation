# Adding Lip-Sync to your Character

To add Lip-Sync to your character, follow these steps.

{% hint style="info" %}
Convai's Lip-Sync uses [**OVR**](https://developer.oculus.com/documentation/unity/audio-ovrlipsync-viseme-reference/) or **Reallusion CC4 Extended** (Reallusion CC4+) Blendshapes. The lip-sync will work best with models that have **OVR** or **Reallusion CC4 Extended** (Reallusion CC4+) compatible Blendshapes.&#x20;
{% endhint %}

Select the character GameObject and click Add Component in the Inspector.&#x20;

<figure><img src="../../.gitbook/assets/image (228).png" alt=""><figcaption></figcaption></figure>

Select `Convai Lip Sync` to add the Lip Sync component.

<figure><img src="../../.gitbook/assets/image (227).png" alt=""><figcaption></figcaption></figure>



In the new component, select the type of lipsync, and assign the Skinned Mesh Renderer with the Facial Blendshapes (here for Reallusion Characters, `CC_Base_Body`, `CC_Base_Teeth` and `CC_Base_Tongue`)  and the game objects corresponding to the bones for Jaw and Tongue (here for Reallusion Characters, `CC_Base_JawRoot` and `CC_Base_Tongue01`). Feel free to adjust the position of the tongue with the Tongue Bone Offset field. &#x20;

{% hint style="warning" %}
Currently, only Reallusion Plus and OVR are supported as a type of lip sync.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (226).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
If your character's mouth seems to not be opening enough for a proper lip sync, this could indicate an issue with the animator or animations.
{% endhint %}

To resolve common issues caused by the animator and animations, follow the troubleshooting guides below.

[animations-have-facial-blendshapes.md](troubleshooting-guide/animations-have-facial-blendshapes.md "mention")
