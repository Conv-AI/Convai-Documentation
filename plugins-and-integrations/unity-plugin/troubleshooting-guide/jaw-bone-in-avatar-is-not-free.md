---
description: >-
  Fix jaw bone issues in Unity avatars with Convai. Ensure smooth lip sync and
  animations.
---

# Jaw Bone in Avatar is not Free

If the Lip Sync does not seem to cause any facial animations, even after removing all blendshapes from animations, then the following steps should help resolve the issue.

{% hint style="info" %}
This is a known issue in Reallusion CC4 characters.
{% endhint %}

Select the Character and head to the Animator component.

<figure><img src="../../../.gitbook/assets/image (260).png" alt=""><figcaption></figcaption></figure>

Click the Avatar Field once to select the character's avatar in the Project window.

<figure><img src="../../../.gitbook/assets/image (261).png" alt=""><figcaption></figcaption></figure>

Select the Avatar and click Configure Avatar.

<figure><img src="../../../.gitbook/assets/image (263).png" alt=""><figcaption></figcaption></figure>

Select the Head option in the Mapping tab.

<figure><img src="../../../.gitbook/assets/image (265).png" alt=""><figcaption></figcaption></figure>

Select the Jaw Mapping and set it to None.

<figure><img src="../../../.gitbook/assets/image (267).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (268).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (269).png" alt=""><figcaption></figcaption></figure>

Finally scroll down and click Apply.

<figure><img src="../../../.gitbook/assets/image (270).png" alt=""><figcaption></figcaption></figure>

This will free the avatar's jaw mapping and allow the script to manipulate the Jaw bones.
