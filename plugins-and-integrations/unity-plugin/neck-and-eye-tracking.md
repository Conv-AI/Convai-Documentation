---
description: >-
  Follow these steps to enable your character's head and eyes to follow the
  player.
---

# Neck and Eye Tracking

While this is not an in-built Convai feature, you can easily allow your characters to follow the player with there head and eyes.

### Add Animation Rigging

You will need the Animation Rigging Package. To import it, go to Windows > Package Manager.

<figure><img src="../../.gitbook/assets/image (81).png" alt=""><figcaption></figcaption></figure>

Go to the Unity Registry.

<figure><img src="../../.gitbook/assets/image (168).png" alt=""><figcaption></figcaption></figure>

In the Packages Tab, Scroll down to find the package Animation Rigging and Click Install.

<figure><img src="../../.gitbook/assets/image (77).png" alt=""><figcaption></figcaption></figure>

### Add Rigs and Configure them

Go to your character's GameObject and add a Rig Builder Component.&#x20;

<figure><img src="../../.gitbook/assets/image (58).png" alt=""><figcaption></figcaption></figure>

Add an empty child GameObject. Name it Neck Rig.

<figure><img src="../../.gitbook/assets/image (83).png" alt=""><figcaption></figcaption></figure>

In the NeckRig, add a Rig Component and a Multi-Aim Constraint Component.

<figure><img src="../../.gitbook/assets/image (166).png" alt="" width="375"><figcaption></figcaption></figure>

Find the head or neck bone of the model. You will have to choose it carefully, since every model is different. Pick the one that seems to move the head around.

<figure><img src="../../.gitbook/assets/image (51).png" alt=""><figcaption></figcaption></figure>

In the Multi-Anim Constraint component, add the Neck/Head GameObject to the Constrained Object field and the in the Source Objects, add the Camera GameObject of the Player GameObject.

<figure><img src="../../.gitbook/assets/image (117).png" alt=""><figcaption></figcaption></figure>

Check the orientation of your model's neck GameObject (Toggle the Tool Handle Rotation to Local). Update the Aim Axis and the Up Axis based on that.

<figure><img src="../../.gitbook/assets/image (67).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (76).png" alt="" width="375"><figcaption></figcaption></figure>

Set the Min Limit and Max Limit fields to -45 and 45 respectively, so that the neck rotation is not uncanny.

<figure><img src="../../.gitbook/assets/image (187).png" alt="" width="375"><figcaption></figcaption></figure>

Back in the NPC GameObject, Set the Rig field in the Rig Builder as the NeckRig GameObject.

<figure><img src="../../.gitbook/assets/image (119).png" alt="" width="375"><figcaption></figcaption></figure>
