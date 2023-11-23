---
description: Advanced Character Head Tracking
---

# ConvaiBlinkingHandler

{% hint style="info" %}
To understand the script in even more depth, please check out the comments in the script.
{% endhint %}

#### Description

The `ConvaiBlinkingHandler` class manages a character's blinking behavior in Unity. It is designed to work with a character's face, adjusting the blend shapes of the eyelids to simulate blinking. This script adds a dynamic and lifelike aspect to character animations.

#### Requirements

Before using `ConvaiBlinkingHandler`, ensure the following requirements are met:

* **SkinnedMeshRenderer:** Attach a SkinnedMeshRenderer component to the character's face for manipulating blend shapes.
* **Character Name:** This script relies on the character's name obtained from a `ConvaiNPC` script. Ensure that the character's name is set correctly in `ConvaiNPC`.

***

### Properties

#### Serialized Fields

**`faceSkinnedMeshRenderer`:**

* **Type:** SkinnedMeshRenderer
* **Description:** The SkinnedMeshRenderer for the character's face. This renderer allows for the manipulation of blend shapes to control blinking.

**`indexOfLeftEyelid`:**

* **Type:** int
* **Description:** The index of the left eyelid blend shape in the SkinnedMeshRenderer.

**`indexOfRightEyelid`:**

* **Type:** int
* **Description:** The index of the right eyelid blend shape in the SkinnedMeshRenderer.

**`minBlinkDuration`:**

* **Type:** float
* **Description:** The minimum amount of time, in seconds, for a single blink.

**`maxBlinkDuration`:**

* **Type:** float
* **Description:** The maximum amount of time, in seconds, for a single blink.

**`minBlinkInterval`:**

* **Type:** float
* **Description:** The minimum amount of time, in seconds, between blinks.

**`maxBlinkInterval`:**

* **Type:** float
* **Description:** The maximum amount of time, in seconds, between blinks.

### Methods

#### `Start()`

* **Description:** This method is called when the script starts. It initializes the eyelid blend shape indices based on the character's name and player preferences. If the indices are not found in preferences, it searches for appropriate blend shape names in the character's face mesh. If the indices are still not found, an error is logged. After initialization, it starts the blinking coroutine.

```csharp
csharpCopy codestring npcName = GetComponent<ConvaiNPC>().characterName;
...
indexOfLeftEyelid = PlayerPrefs.GetInt(leftBlinkKey, -1);
...
StartCoroutine(BlinkCoroutine());
```

#### `BlinkCoroutine()`

* **Description:** This coroutine handles the blinking mechanism of the character. It generates random blink durations and intervals within the specified minimum and maximum values. During a blink, it gradually adjusts the blend shape weights to simulate eyelid movement. After each blink, there's a pause before the next blink occurs.

#### `SetEyelidsBlendShapeWeight(float weight)`

* **Description:** This method sets the same weight to both eyelids' blend shapes in the SkinnedMeshRenderer. It's used to smoothly adjust the eyelid positions during blinking.

### How to Use

To implement blinking behavior for a character using the `ConvaiBlinkingHandler` script, follow these steps:

1. Attach the `ConvaiBlinkingHandler` script to the GameObject representing the character.
2. Attach a SkinnedMeshRenderer component to the character's face and assign it to the `faceSkinnedMeshRenderer` field in the Inspector.
3. Set the character's name correctly in the associated `ConvaiNPC` script.
4. Adjust the `minBlinkDuration`, `maxBlinkDuration`, `minBlinkInterval`, and `maxBlinkInterval` properties in the Inspector to control the blinking frequency and duration.
5. Ensure that the character's face mesh has appropriate blend shapes for the left and right eyelids.

### Practical Use Case Scenario

The `ConvaiBlinkingHandler` script is particularly useful for creating more realistic and expressive character animations. It can be applied to various character types, such as NPCs in a game, to make them blink at random intervals, adding a touch of realism to their appearance.

By following this documentation, you can seamlessly integrate blinking behavior into your character animations in Unity.

***
