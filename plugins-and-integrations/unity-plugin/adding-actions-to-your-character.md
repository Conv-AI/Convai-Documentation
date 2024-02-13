---
description: >-
  Follow these instructions to enable actions for your Convai-powered
  characters.
---

# Adding Actions to your Character

## Setting Up Action Configurations

1. Select the Convai NPC character from the hierarchy.
2. Scroll down to the ConvaiNPC script attached to your character.
3. Click the "Add Component" button.

<figure><img src="../../.gitbook/assets/image (1).png" alt="" width="438"><figcaption></figcaption></figure>

4. Use the checkbox to add the action script to the NPC Actions.
5. Click "Apply Changes" to confirm.

<figure><img src="../../.gitbook/assets/image (1) (2).png" alt="" width="563"><figcaption></figcaption></figure>

## Pre-defined Actions

Convai offers predefined actions for a quick start.

1. Click the "+" button to add a new action.
2. From the dropdown menu, select "Move To."

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

3. Enter the action name as "Move To" (the name doesn't have to match the action choice name).
4. Leave the Animation Name field empty for now.

Repeat these steps to add more actions like "Pickup" and "Drop" etc.

### Adding an Object in the Scene

1. Add any object into the scene—a sphere, a cube, a rock, etc.—that can be interacted with
2. Resize and place the object in your scene.

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

### Adding the Convai Interactables Data Script

1. Create an empty GameObject and name it "Convai Interactables."![](<../../.gitbook/assets/image (7).png>)
2. Attach the Convai Interactables Data script to this GameObject.
3. Add characters and objects to the script by clicking the "+" button and attaching the corresponding GameObjects.

<div align="left">

<figure><img src="../../.gitbook/assets/image (6).png" alt="" width="563"><figcaption></figcaption></figure>

</div>

### Test the Setup

1. Click "Play" to start the scene.
2. Ask the NPC, "Bring me the Box."&#x20;
3. If setup properly, the NPC should walk upto the box and bring it to you

{% hint style="warning" %}
This feature is currently experimental and can misbehave. Feel free to try it out and leave us any feedback.
{% endhint %}

## Adding Custom Actions to Your Unity NPC in Convai

### Introduction

Make your NPC perform custom actions like dancing.

### Action that Only Requires an Animation

1.  Locate the dance animation file within our plugin.

    <figure><img src="../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>
2. Incorporate this animation into your NPC's actions.

### Setting Up the Animator Controller

1. Open the Animator Controller from the Inspector window.
2.  Drag and drop the dance animation onto the controller, creating a new node named "Dancing."

    <figure><img src="../../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

### Adding custom Animation Action

1. Go to the Action Handler Script attached to your Convai NPC.
2. Add a new action named "Dancing."&#x20;
3. In the Animation Name field, enter "Dancing" (it must exactly match the Animator Controller node name).
4. Leave the enum as "None."

<figure><img src="../../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

### Testing the Custom Action

1. Click "Play" to start the scene.
2. Instruct the NPC, "Show me a dance move," and the NPC should start dancing.

## Creating Complex Custom Actions in Unity with Convai: Throwing a Rock

### Introduction

Adding advanced custom actions, such as a throw action, to your NPC.

### Animation Requirement

1. Grab a [throw animation from Mixamo](https://www.mixamo.com/#/?page=1\&query=throw) or anywhere you like.
2. Import it into Unity.

### Setting Up the Animator Controller

1. Drag and drop the throw animation onto the controller, creating a new node named "Throwing." (Follow steps in [#action-that-only-requires-an-animation](adding-actions-to-your-character.md#action-that-only-requires-an-animation "mention"))

### Action Handler Script Setup

1.  Add the "Throw" enum to the script.

    <figure><img src="../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>
2.  In the "Do Action" function, add a switch case for the throw action.&#x20;

    <figure><img src="../../.gitbook/assets/image (18).png" alt=""><figcaption></figcaption></figure>
3.  Define the "Throw()" function.&#x20;

    <figure><img src="../../.gitbook/assets/image (19).png" alt=""><figcaption></figcaption></figure>

### Adding the Throw Action

1. Add a new action named "Throw" and select the "Throw" enum.&#x20;
2.  Leave the animation name field empty.&#x20;

    <figure><img src="../../.gitbook/assets/image (21).png" alt=""><figcaption></figcaption></figure>

### Adding the Object (Rock) to the Convai Interactables Data script

1. Add any rock prefab into the scene.
2. Add the rock to the Convai Interactable Data script.

### Adding a location to Convai Interactables Data script

1. Add a stage/new location in the ground of the scene.
2.  Add that new location game object in the Convai Interactable Data.

    <figure><img src="../../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>

### Testing the Complex Action

1. Click "Play" to start the scene.
2. Instruct the NPC, "Pick up the rock and throw it from the stage."
3. If everything is set up properly, the NPC should pick up the rock and throw it from the stage.&#x20;

***
