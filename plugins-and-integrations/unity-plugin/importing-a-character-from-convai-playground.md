---
description: >-
  Follow these instructions to bring a character from the Convai Playground into
  your Unity Project.
---

# Importing Characters into a Scene

{% hint style="info" %}
You can import the character created in the Convai Playground **only** in the Core, Complete, and Actions versions of the plugin.
{% endhint %}

## Import RPM characters from the Convai Playground

This is how you can import characters from the Convai Playground into your Unity Project.

In the Menu Bar, go the Convai > Character Importer.

<figure><img src="../../.gitbook/assets/image (110).png" alt=""><figcaption></figcaption></figure>

Enter the Character ID and click Import.

<figure><img src="../../.gitbook/assets/image (90).png" alt=""><figcaption><p>Enter the character ID and click Import.</p></figcaption></figure>

If you are unsure how to get the character ID, click the "How do I create a character?".

You can get the character ID from the Character Description.

<figure><img src="../../.gitbook/assets/image (2) (4) (1).png" alt=""><figcaption></figcaption></figure>

The downloading will take a while. On successful download, you will see the character in the scene with the same GameObject as the character ID.&#x20;

<figure><img src="../../.gitbook/assets/image (361).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (1) (4) (1).png" alt=""><figcaption></figcaption></figure>

This character will automatically be set up with the basic Convai Setup including the ConvaiNPC Script and Out-Of-Box Animations.&#x20;

<figure><img src="../../.gitbook/assets/image (3) (4) (1).png" alt=""><figcaption></figcaption></figure>

If you are facing issues with the animations in your imported character, make sure to change the animation type of `Ellen@IdleNew` and `Ellen@TalkingNew` Animations in the `Assets/Convai/Animations` folder to `Humanoid`.

<figure><img src="../../.gitbook/assets/image (215).png" alt=""><figcaption><p>Change the animation type to 'Humanoid' and click 'Apply'.</p></figcaption></figure>

Now you are ready to set up the character with transcriptions.&#x20;
