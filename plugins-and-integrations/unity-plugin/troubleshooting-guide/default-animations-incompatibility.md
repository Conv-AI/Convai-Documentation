---
description: >-
  Fix default animation incompatibilities in Unity with Convai. Ensure smooth AI
  character animations.
---

# Default Animations Incompatibility

If the default animations that ship with the animator look bugged such that the hand seems to intersect with the body, it could indicate an issue with the wrong animation avatar being selected.&#x20;

<figure><img src="../../../.gitbook/assets/image (50).png" alt=""><figcaption></figcaption></figure>

You can easily fix that by heading to the character's animator component and assigning the correct animator to the Avatar field.

<div align="center">

<figure><img src="../../../.gitbook/assets/image (363).png" alt=""><figcaption><p>For male avatars</p></figcaption></figure>

</div>

<figure><img src="../../../.gitbook/assets/image (364).png" alt=""><figcaption><p>For female avatars</p></figcaption></figure>

The correct animation will look something like this. The hands should not intersect the body.

<figure><img src="../../../.gitbook/assets/image (51).png" alt=""><figcaption></figcaption></figure>
