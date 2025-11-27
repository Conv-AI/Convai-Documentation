---
description: >-
  Fix default animation incompatibilities in Unity with Convai. Ensure smooth AI
  character animations.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/troubleshooting-guide/default-animations-incompatibility
---

# Default Animations Incompatibility

If the default animations that ship with the animator look bugged such that the hand seems to intersect with the body, it could indicate an issue with the wrong animation avatar being selected.&#x20;

<figure><img src="../../../.gitbook/assets/image (151).png" alt=""><figcaption></figcaption></figure>

You can easily fix that by heading to the character's animator component and assigning the correct animator to the Avatar field.

<div align="center"><figure><img src="../../../.gitbook/assets/image (477).png" alt=""><figcaption><p>For male avatars</p></figcaption></figure></div>

<figure><img src="../../../.gitbook/assets/image (478).png" alt=""><figcaption><p>For female avatars</p></figcaption></figure>

The correct animation will look something like this. The hands should not intersect the body.

<figure><img src="../../../.gitbook/assets/image (152).png" alt=""><figcaption></figcaption></figure>
