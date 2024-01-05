---
description: >-
  Follow these instructions to set up your imported character with Custom Model
  with Convai.
---

# Importing Custom Characters

To import your custom characters into your Convai-powered Unity project, you will first need to bring your model into your project. The model needs at least two animations: one for Talking and one for Idle.

## Part 1: Character

When you want to set up your custom character with Convai, you will need your character model and two animations: Idle and Talking.&#x20;

Create an animator controller with the two animations that looks like this. You should also add a 'Talk' boolean to ensure that you can trigger the animation. [Here is a YouTube tutorial on how to set up an animator controller](https://www.youtube.com/watch?v=JeZkctmoBPw\&t=53s). This is the bare minimum animator setup that you need to do.&#x20;

<figure><img src="../../.gitbook/assets/image (222).png" alt=""><figcaption><p>The animator controller should look like this. This is the the in-box NPC Animator. </p></figcaption></figure>

Add an animator component and the created animator controller to the component. NPC Animator is the name of the animator that ships out of the box with the plugin. You will want to replace this with your own animator.&#x20;

<figure><img src="../../.gitbook/assets/image (129).png" alt=""><figcaption><p>The animator component with the in-box "NPC Animator"</p></figcaption></figure>

Add a Capsule (or any other shape of choice) Collider and make it into a trigger by selecting the IsTrigger field.

<figure><img src="../../.gitbook/assets/image (152).png" alt=""><figcaption></figcaption></figure>

Add an Audio Source component to the character.

<figure><img src="../../.gitbook/assets/image (58).png" alt=""><figcaption></figcaption></figure>

The GameObject should look like this.

<figure><img src="../../.gitbook/assets/image (155).png" alt=""><figcaption></figcaption></figure>

Finally, change the Tag of the Convai-powered NPC to "Character" so that it can work with the in-box Convai Player Character.

<figure><img src="../../.gitbook/assets/image (182).png" alt=""><figcaption><p>Change the tag from "Untagged" to "Character"</p></figcaption></figure>

The next page gives a brief overview of the ConvaiNPC.cs script.

## Part 2: Transcriptions and Captions

{% hint style="info" %}
You will have to do this part of the setup for characters downloaded from the playground through the character downloader if you are using the Core version of the plugin.
{% endhint %}

Create a Canvas with two TextMeshPro GameObjects. One of these will be where the transcript appears as we speak and the other will be where the character's transcript appears.&#x20;

Drag the User Transcript TextMeshPro (named User Text here) to the User Text field in the Convai GRPCAPI script present in the Camera component in the Convai Player Character.

<figure><img src="../../.gitbook/assets/image (185).png" alt=""><figcaption><p>Go to the camera component of the Convai Player Character.</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (161).png" alt=""><figcaption><p>Add the User Text TextMeshPro GameObject to the User Text field.</p></figcaption></figure>

Drag the Character's Transcript TextMeshPro to the Character Text field in the Convai NPC script in the character that you added.

<figure><img src="../../.gitbook/assets/image (173).png" alt=""><figcaption><p>Add the Character Text TextMeshPro GameObject to the Character Text field.</p></figcaption></figure>

This will set up the new Character and you can talk to it.&#x20;
