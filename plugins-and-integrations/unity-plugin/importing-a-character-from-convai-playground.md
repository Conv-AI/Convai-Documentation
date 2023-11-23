---
description: >-
  Follow these instructions to bring a character from the Convai Playground into
  your Unity Project.
---

# Importing a character from Convai Playground

{% hint style="info" %}
You can import the character created in the Convai Playground **only** in the Core, Complete, and Actions versions of the plugin.
{% endhint %}

### Core Plugin

This is how you can import characters from the Convai Playground into your Unity Project.

In the Menu Bar, go the Convai > Character Importer.

<figure><img src="../../.gitbook/assets/image (79).png" alt=""><figcaption></figcaption></figure>

Enter the Character ID and click Import.

<figure><img src="../../.gitbook/assets/image (59).png" alt=""><figcaption><p>Enter the character ID and click Import.</p></figcaption></figure>

If you are unsure how to get the character ID, click the "How do I create a character?".

You can get the character ID from the Character Description.

<figure><img src="../../.gitbook/assets/image (88).png" alt=""><figcaption></figcaption></figure>

The downloading will take a while. On successful download, you will see the character in the scene with the same GameObject as the character ID.&#x20;

<figure><img src="../../.gitbook/assets/image (33).png" alt=""><figcaption></figcaption></figure>

This character will automatically be set up with the basic Convai Setup including the ConvaiNPC Script and Out-Of-Box Animations.&#x20;

<figure><img src="../../.gitbook/assets/image (149).png" alt=""><figcaption></figcaption></figure>

If you are facing issues with the animations in your imported character, make sure to change the animation type of `Ellen@IdleNew` and `Ellen@TalkingNew` Animations in the `Assets/Convai/Animations` folder to `Humanoid`.

<figure><img src="../../.gitbook/assets/image (184).png" alt=""><figcaption><p>Change the animation type to 'Humanoid' and click 'Apply'.</p></figcaption></figure>

Now you are ready to set up the character with transcriptions.&#x20;

Follow the tutorial on importing custom characters below to see how you can set up the character with Transcriptions and Custom Animations.

{% content-ref url="importing-custom-characters.md" %}
[importing-custom-characters.md](importing-custom-characters.md)
{% endcontent-ref %}

### Complete Plugin

For the Complete Plugin, the process of importing the character is different. First, we will want to create a scene that is compatible with the Convai. This scene needs to have the Convai Player Character and the Convai Transcript Canvas prefabs (or similar prefabs). For the Core Plugin, we do this manually, but for the Complete Plugin, the setup process is automated.&#x20;

First, we will click on File > New Scene.

<figure><img src="../../.gitbook/assets/image (29).png" alt=""><figcaption><p>Click on New Scene in the File Menu</p></figcaption></figure>

In the Dialogue that opens, select Convai Scene and click Create.

<figure><img src="../../.gitbook/assets/image (94).png" alt=""><figcaption><p>Click on Convai Scene and click create.</p></figcaption></figure>

Then go the Convai > Character Importer.

<figure><img src="../../.gitbook/assets/image (79).png" alt=""><figcaption></figcaption></figure>

Enter the Character ID and click Import.

<figure><img src="../../.gitbook/assets/image (92).png" alt=""><figcaption><p>Enter the character ID and click Import.</p></figcaption></figure>

This will import your character completely set up with Lip Sync and basic animations.

<figure><img src="../../.gitbook/assets/image (45).png" alt=""><figcaption><p>The character is in the scene.</p></figcaption></figure>

You can also see the prefab for the character in the Assets/Convai/Prefabs folder.

<figure><img src="../../.gitbook/assets/image (146).png" alt=""><figcaption><p>Character Prefab is in the Assets/Convai/Prefabs folder.</p></figcaption></figure>

With this, you can use the Convai-powered RPM character in any scene in the project if you want.
