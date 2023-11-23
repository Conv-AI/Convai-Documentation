# ConvaiLipSync.cs

{% content-ref url="../adding-lip-sync-to-your-character.md" %}
[adding-lip-sync-to-your-character.md](../adding-lip-sync-to-your-character.md)
{% endcontent-ref %}

{% hint style="info" %}
To understand the script in even more depth, please check out the comments in the script.
{% endhint %}

## Introduction

The `ConvaiLipSync` class is responsible for handling the lip sync based on the facial animation data received from the server based on the character's response.

#### Requirements

Before using the script, please ensure the following:

* The animations do not have any facial blendshapes.
* The animator avatar for the character had the Jaw bone mapping set to none.
* The character has blendshapes compatible with Oculus VR Visemes or Reallusion CC4 Extended Visemes.

***

### Properties

#### Public or Serialized Fields

**Skinned Mesh Renderers**

* **`HeadSkinnedMeshRenderer`**: Skinned Mesh Renderer Component for the head of the character. This field cannot be left empty.
* **`TeethSkinnedMeshRenderer`**: Skinned Mesh Renderer Component for the teeth of the character. Leave empty if not available.
* **`TongueSkinnedMeshRenderer`**: Skinned Mesh Renderer Component for the tongue of the character, if available. Leave empty if not.

**Bones**

* **`jawBone`**: Game object with the bone of the jaw for the character. Leave empty, if unavailable.
* **`tongueBone`**: Game object with the bone of the tongue for the character. Leave empty, if unavailable.

**Finetuning**

* **`tongueBoneOffset`**: Vector to control the position of the tongue. This can be used to make the look the tongue natural during lip-sync.
* **`firstIndex`**: The index of the first blendshape that will be manipulated. Use this if there are multiple sets of blendshapes in the character's model.

### Methods

#### `Start()`

* **Description**: This function will automatically set any of the unassigned skinned mesh renderers to appropriate values using regex based functions. It also invokes the `LipSyncCharacter()` function every one hundredth of a second.&#x20;

#### `Update()`

* **Description**: This function will adjust the position of the tongue according to the `tongueBoneOffset` value.

#### `GetHeadSkinnedMeshRendererWithRegex(Transform parentTransform)`, `GetTeethSkinnedMeshRendererWithRegex(Transform parentTransform)`, `GetTongueSkinnedMeshRendererWithRegex(Transform parentTransform)`

* **Description**: These functions find the Head, Teeth and Tongue skinned mesh renderers components if present in the children of the `parentTransform` using regex.

#### `LipSyncCharacter()`

* **Description**: This function will check if the list containing the facial animation data has any data. If it has any facial animation data, the function will adjust the face based on the data received.

***

### How to use

To use the `ConvaiLipSync` script, follow these steps:

1. Attach the `ConvaiLipSync` component to the character.
2. Select the type of blendshapes that you have from the BlendshapeType field: Oculus (`OVR`) or Reallusion CC4 Extended (`ReallusionPlus`).
3. Add the Skinned Mesh Renderer component containing the facial blendshapes to the `HeadSkinnedMeshRenderer` field. This is **mandatory**.&#x20;
4. If there are Skinned Mesh Renderers containing blendshapes pertaining to the teeth and tongue, add them to the `TeethSkinnedMeshRenderer` and the `TongueSkinnedMeshRenderer` fields respectively. Leave them blank if not.&#x20;
5. Similarly, if there are GameObjects for bones of the Jaw and the Tongue, add them to the `JawBone` and `TongueBone` fields respectively.
6. Adjust the Tongue Bone for a more natural look with the `TongueBoneOffset` field.
7. If your character model has more the one sets of blendshapes, use the `firstIndex` field to set the index of the first blendshape that we want to manipulate.

