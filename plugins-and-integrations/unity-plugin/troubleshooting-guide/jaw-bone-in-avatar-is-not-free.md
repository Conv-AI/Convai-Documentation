---
description: >-
  Fix jaw bone issues in Unity avatars with Convai. Ensure smooth lip sync and
  animations.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/troubleshooting-guide/jaw-bone-in-avatar-is-not-free
---

# Jaw Bone in Avatar is not Free

If the Lip Sync does not seem to cause any facial animations, even after removing all blendshapes from animations, then the following steps should help resolve the issue.

{% hint style="info" %}
This is a known issue in Reallusion CC4 characters.
{% endhint %}

Select the Character and head to the Animator component.

<figure><img src="../../../.gitbook/assets/image (361).png" alt=""><figcaption></figcaption></figure>

Click the Avatar Field once to select the character's avatar in the Project window.

<figure><img src="../../../.gitbook/assets/image (362).png" alt=""><figcaption></figcaption></figure>

Select the Avatar and click Configure Avatar.

<figure><img src="../../../.gitbook/assets/image (364).png" alt=""><figcaption></figcaption></figure>

Select the Head option in the Mapping tab.

<figure><img src="../../../.gitbook/assets/image (366).png" alt=""><figcaption></figcaption></figure>

Select the Jaw Mapping and set it to None.

<figure><img src="../../../.gitbook/assets/image (368).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (369).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (370).png" alt=""><figcaption></figcaption></figure>

Finally scroll down and click Apply.

<figure><img src="../../../.gitbook/assets/image (371).png" alt=""><figcaption></figcaption></figure>

This will free the avatar's jaw mapping and allow the script to manipulate the Jaw bones.
