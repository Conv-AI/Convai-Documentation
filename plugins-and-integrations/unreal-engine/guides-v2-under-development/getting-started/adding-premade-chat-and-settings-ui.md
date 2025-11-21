---
description: >-
  Use a premade player blueprint that already contains a Chat and Settings
  widget.
---

# Adding Premade Chat and Settings UI

The goal of this guide is to easily show how to add a premade chat and settings widget to the UI by re-parenting the player blueprint, we will continue on the progress from the [Simple Talking Cube](simple-talking-cube.md) guide.

{% hint style="info" %}
It is recommended to remove the Convai Player component from the player blueprint that was created in the previous guide before proceeding with this guide.
{% endhint %}

1. (Optional) If you do not have a player blueprint already, then you can import a first person or third person content into your already existing project.
   1. From the Content Browser, click the Add button, then `Add feature or content pack to the project` then choose either `First Person` or `Third Person` then click `Add to Project`.\
      ![](<../../../../.gitbook/assets/pasted image 0.png>)\
      ![](<../../../../.gitbook/assets/pasted image 0 (1).png>)
   2. Click the Window menu and make sure `World Settings` is enabled.\
      ![](<../../../../.gitbook/assets/image (329).png>)
   3. On the `World Settings` tab, Find `GameMode Override` and set it to `BP_FirstPersonGameMode` for first person or `BP_thirdPersonGameMode` if you imported third person content.\
      ![](<../../../../.gitbook/assets/image (331).png>)<br>
2. In the content browser, navigate to your player blueprint, which is by default at `FirstPerson/Blueprint/BP_FirstPersonCharacter` for First Person or `ThirdPerson/Blueprint/BP_ThirdPersonCharacter` which is the default for Third Person.
3. Open the blueprint and click `Class Settings` then in the `Details` section Under `Class Options` change the parent class to `ConvaiBasePlayer`.

<img src="https://lh3.googleusercontent.com/yXsy1Zy7lfMCTEcj8wqpTZI44UbaDDYiasR9dWFnhzZmTvkV2cXy5-B0U9jNRI2U2lg9jBSkai57RIQ_InSSuaImlCuQIh9LNJaCrZ4Y3wTme_fj6gfMzsBf_HfWE9ICt7Tk_V4J5gs4JH6Ibvlq-Sc" alt="" data-size="line">

<figure><img src="https://lh4.googleusercontent.com/IIukEpo8niZHMAox4z4f-dkre2apO9DHZMKTGzCHfbYFSOZBSboGPnvhlKTDJdDvMTzuN7XND-3z52x42GlpiH1omXDrEeAq3crnK79_EFBobHAByuQtOP1QJbg04ZemJq0eojJb4DiRwyZoo4WNCuY" alt="" width="375"><figcaption><p>Set Parent Class</p></figcaption></figure>

4.  Hit save, compile and hit play to test - use the T key to talk and Enter to text chat.\
    <br>

    <figure><img src="../../../../.gitbook/assets/image (334).png" alt=""><figcaption></figcaption></figure>
5.  Hit F10 to open the settings menu where you have various options, like testing your microphone and changing the chat widget layout.



    <figure><img src="../../../../.gitbook/assets/image (335).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
For advanced use cases, you may not want to change the parent class of the player blueprint, in that case we encourage you to use the `Convai Base Player` Blueprint itself as reference to see how to add the Chat and Settings widget or even create your own widgets from scratch.\
\
We expect developers who are looking to implement everything from scratch or do customization to be advanced enough to navigate the blueprints on their own.
{% endhint %}
