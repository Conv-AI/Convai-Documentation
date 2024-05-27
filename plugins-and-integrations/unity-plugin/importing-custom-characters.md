---
description: >-
  Follow these instructions to set up your imported character with Custom Model
  with Convai.
---

# Importing Custom Characters

To import your custom characters into your Convai-powered Unity project, you will first need to bring your model into your project. The model needs at least two animations: one for talking and one for Idle.

## Prerequisites

When you want to set up your custom character with Convai, you will need your character model and two animations: Idle and Talking.&#x20;

Create an animator controller with the two animations that looks like this. You should also add a 'Talk' Boolean to ensure that you can trigger the animation. [Here is a YouTube tutorial on how to set up an animator controller](https://www.youtube.com/watch?v=JeZkctmoBPw\&t=53s). This is the bare minimum animator setup that you need to do.&#x20;

<figure><img src="../../.gitbook/assets/image (222).png" alt=""><figcaption><p>The animator controller should look like this. This is the in-box NPC Animator. </p></figcaption></figure>

### Step 1: Add Animator to your custom character

Select your character from the Hierarchy and Add Animator Component

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 195315.png" alt=""><figcaption><p>Screenshot showing newly added Animator Component</p></figcaption></figure>

Convai Plugin ships with two pre-made animation controller, you can choose these controllers or can assign your custom controller, whatever fits your need. For this demo we are going with `Feminine NPC Animator`

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 195607.png" alt=""><figcaption><p>Screenshot showing selection of Animation Controller</p></figcaption></figure>

### Step 2: Adding a Trigger Volume

With your custom character selected, add a Collision shape of your choice, for this demo we are going with a `Capsule Collider`

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 200002.png" alt=""><figcaption><p>Screenshot showing newly added Capsule Collider</p></figcaption></figure>

We will make this Collider a trigger, for this we will enable the `Is Trigger` option in the inspector panel



<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 200219.png" alt=""><figcaption><p>Screenshot showing enable of Is Trigger option</p></figcaption></figure>

We will adjust the Center, Radius and Height of the collider such that it fits our character

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 203103 (1).png" alt=""><figcaption></figcaption></figure>

### Step 3: Add [ConvaiNPC](scripts-overview/convainpc.cs.md) Component

With your Custom Character Selection add ConvaiNPC component. By doing so, your Game objectgame should look like this:

{% hint style="info" %}
We assume that nothing other than pre-instructed components were added by you; your Game Object component list may be different
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 201324.png" alt=""><figcaption><p>Screenshot showing newly added ConvaiNPC Component</p></figcaption></figure>

Copy your character's ID and name from [Convai Playground](broken-reference) and paste them here.

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 201727.png" alt=""><figcaption><p>Screenshot showing filled-in character information.</p></figcaption></figure>

### Step 4: Setup a: game object for Convai Character

We will assign `Convai Character` layer to your Custom Character Game Object&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 202613.png" alt=""><figcaption><p>Screenshot showing selection of Convai Character</p></figcaption></figure>

Now your Custom Character is all set to work with Convai Plugin
