---
description: >-
  Resolve facial blendshape issues in Unity animations with Convai. Improve
  character realism.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/troubleshooting-guide/animations-have-facial-blendshapes
---

# Animations have Facial Blendshapes

If the Lip-sync from characters are either not visible or are very faint, if could be a result of character's animations overriding the blendshape changes made by the script. We recommend deleting the relevant components in the animation dopesheet.

<figure><img src="../../../.gitbook/assets/image (156).png" alt=""><figcaption><p>The blendshapes in the CC_Base_Body's Skinned Mesh Renderer. We shall delete these.</p></figcaption></figure>
