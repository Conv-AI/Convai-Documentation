# GLB Characters for Convai

### RPM characters

Creating a Character on ReadyPlayer:

ReadyPlayer.me is a platform that allows you to create custom 3D avatars or characters. Here are the typical steps involved:

1. Go to the  [https://readyplayer.me/](https://readyplayer.me/) website.
2. Click on the "Create Avatar" or similar button to start the character creation process.
3. Customize your character's appearance by selecting different options for body type, clothing, hair, facial features, and other attributes.
4. Preview your character in 3D as you make changes.
5. Once you're satisfied with your character's look, you can save or download the character file (often in a format like .glb or .glTF).

<figure><img src="../../.gitbook/assets/Screenshot (23).png" alt=""><figcaption><p>RPM glb url</p></figcaption></figure>

Using Morphs with ReadyPlayer.me Characters:

Morphs, also known as blend shapes or morph targets, are a way to deform or animate a 3D model's mesh to create different expressions or appearances. ReadyPlayer.me characters can be animated using morphs.

> [https://models.readyplayer.me/661feb3563b4a87a148eb0df.glb](https://models.readyplayer.me/661feb3563b4a87a148eb0df.glb)[?morphTargets=ARKit,Oculus%20Visemes](https://models.readyplayer.me/65a8dba831b23abb4f401bae.glb?morphTargets=ARKit,Oculus%20Visemes)

<figure><img src="../../.gitbook/assets/Screenshot (24).png" alt=""><figcaption><p>RPM morphTargets api</p></figcaption></figure>

### Reallusion Characters : Actor core

Creating a Character on :

1. Go to the Reallusion website for actor core ([https://actorcore.reallusion.com/3d-character](https://actorcore.reallusion.com/3d-character)) and select the actor you like.
2. Add the "Actore Core" character to cart and also get the relevant animations for the same. For example ("Ideal", "Talking").&#x20;

<figure><img src="../../.gitbook/assets/Screenshot (25) (1).png" alt=""><figcaption><p>Select the character you preferred</p></figcaption></figure>

{% hint style="info" %}
Download animations with "Move in place" (Preferred Option).
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot (26).png" alt=""><figcaption><p>Move in place Animation</p></figcaption></figure>

### Checking Morph Targets with the glTF Viewer

To inspect and preview the available morph targets for your character, you can use the handy glTF viewer tool provided by Don McCurdy. This online viewer supports glTF files, which is a common format for 3D assets like characters and scenes.

Follow these steps:

1. Go to the glTF viewer website: [https://gltf-viewer.donmccurdy.com/](https://gltf-viewer.donmccurdy.com/)
2. In the glTF viewer interface, click the "Open File" button or drag and drop your character's glTF or GLB file onto the viewer window.
3. Once the file is loaded, you should see your character rendered in the 3D viewport.
4. On the right-hand side of the viewer, locate the "Morph Targets" section. This section will list all the available morph targets present in your character file.
5. Click on a morph target from the list to preview how it deforms the character's mesh. The viewer will show the character with the selected morph target applied.
6. Use the slider next to each morph target to adjust the intensity or weight of the deformation.
7. You can also enable multiple morph targets simultaneously by checking their respective boxes and adjusting their sliders.

This glTF viewer is an excellent tool for quickly inspecting and visualizing the morph targets of your character without needing to import it into a 3D software or game engine. It allows you to see how each morph target affects the character's appearance, which can be helpful for understanding the available facial expressions, body poses, or other deformations.

Additionally, the glTF viewer provides other useful features like viewing the character's node hierarchy, inspecting materials and textures, and more.

{% hint style="info" %}
If your character file is in a different format (e.g., FBX, OBJ), you may need to convert it to glTF or GLB first before being able to view it in this tool.
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot (27).png" alt=""><figcaption><p>Viseme_TH Morph</p></figcaption></figure>

glTF Viewer can also be used to find the skinnedMeshes which controlls the visme. In the above example its "Wolf3D\_Head".\
The "Wolf3D\_Head" controlls all morphs on Head object.

<figure><img src="../../.gitbook/assets/Screenshot (28).png" alt=""><figcaption><p>Jaw Open Morph</p></figcaption></figure>

In a similar way the "Wolf3d\_Teeth" in this case controls "Teeth" related morphs.
