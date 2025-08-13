---
description: >-
  Learn to integrate GLB and FBX animations into Convai's web plugin for dynamic
  character actions.
---

# GLB/FBX animations for Convai

### Mixamo

Mixamo is a free online service that provides a vast library of character animations that can be used in various 3D projects. Mixamo accepts only the .fbx file format for uploading animations. If you have an character in the .glb format, you'll need to convert it to .fbx first before uploading it to Mixamo.

#### GLB

1. Open Blender and navigate to `File > Import > GlTF 2.0 (.glb/.gltf)`.
2. Locate and select the .glb file you want to convert, then click `Import GlTF 2.0`.
3. Once the .glb file has been imported, navigate to `File > Export > FBX (.fbx)`.

<div>

<figure><img src="../../.gitbook/assets/Screenshot (32) (1).png" alt=""><figcaption><p>Imported GLB character</p></figcaption></figure>

 

<figure><img src="../../.gitbook/assets/Screenshot (33) (1).png" alt=""><figcaption><p>Export as FBX</p></figcaption></figure>

</div>

{% hint style="info" %}
Any animation that is compatible with the character works. It should be in glb. or fbx. format.
{% endhint %}
