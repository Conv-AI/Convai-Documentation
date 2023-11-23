---
description: Advanced Character Head Tracking
---

# ConvaiHeadTracking

{% hint style="info" %}
To understand the script in even more depth, please check out the comments in the script.
{% endhint %}

#### Description

The `ConvaiHeadTracking` class is designed to provide head tracking functionalities for a GameObject (like a character) equipped with an `Animator`. The primary use-case for this utility is to facilitate characters that can rotate their heads and eyes to look at a specific target in the scene, creating a more immersive and interactive experience.

#### Requirements

* An `Animator` component should be attached to the same GameObject.
* Only one instance of `ConvaiHeadTracking` is allowed per GameObject.

***

#### Properties

**`Tracking Properties`**

* **targetObject**:
  * **Type**: `Transform`
  * **Description**: The object in the scene that the character's head should track.
  * **Default**: If not set, it will default to the main camera.
* **trackingDistanceThreshold**:
  * **Type**: `float`
  * **Description**: Defines the maximum distance at which the head must still track the target.

**`Look At Weights`**

* **bodyLookAtWeight**:
  * **Type**: `float`
  * **Description**: Controls the amount of rotation applied to the body to align with the target. A value closer to `1` will cause the body to rotate more towards the target.
* **headLookAtWeight**:
  * **Type**: `float`
  * **Description**: Controls the amount of rotation applied to the head to look at the target. A value closer to `1` will cause the head to rotate more towards the target.
* **eyesLookAtWeight**:
  * **Type**: `float`
  * **Description**: Controls the amount of rotation applied to the eyes to fixate on the target. A value of `1` makes the eyes fully track the target.
* **lookAway**:
  * **Type**: `bool`
  * **Description**: Determines whether the character occasionally looks away from the target. If set as`true`, the character will look away randomly, mimicking real-life interactions
  * **Default**: true

***

#### Methods

**Public Methods:**

* **OnAnimatorIK(int layerIndex)**:
  * **Description**: A Unity built-in method triggered during the IK pass to handle the head tracking.

**Private Methods:**

* **InitializeTargetObject()**: Sets the target to the main camera if no target is set.
* **CreateHeadPivot()**: Creates a pivot point for the head's rotation.
* **UpdateTarget()**: Adjusts the look-at weight based on the `lookAway` property.
* **PerformHeadTracking()**: Manages the actual head tracking based on the distance and angle from the target.
* **SetCurrentLookAtWeight()**: Modifies the current look-at weight based on the head's pivot angle.
* **AdjustAnimatorLookAt()**: Updates the Animator's look-at position and weight.
* **DrawRayToTarget()**: Draws a ray from the GameObject to the target for debugging purposes.

***

#### How to Use

1. Attach this script to a GameObject that has an Animator component.
2. In the Inspector, assign a target for the head to track or leave it blank to default to the main camera.
3. Adjust the look-at weights and the tracking distance threshold as per your requirement.
4. Enable the `lookAway` option if you want the character to occasionally look away from the target.

***

#### Detailed Method Explanations

**`InitializeTargetObject()`**

```csharp
private void InitializeTargetObject()
{
    if (targetObject != null) return;

    Debug.LogWarning("No target object set for head tracking. Setting default target as main camera");
    if (Camera.main != null) targetObject = Camera.main.transform;
}
```

This method ensures that there is always a target for the head tracking to focus on. If the user hasn't specified a `targetObject`, it defaults to the main camera. This is particularly useful for scenarios where you'd like characters to look at the player (often represented by the main camera) by default. The user can set the targetObject from the inspector itself if the target-object is desired to be something else

**`CreateHeadPivot()`**

```csharp
private void CreateHeadPivot()
{
    _headPivot = new GameObject("HeadPivot").transform;
    _headPivot.transform.parent = transform;
    _headPivot.localPosition = new Vector3(0, 1.6f, 0);
}
```

This method creates a virtual pivot point, `_headPivot`, around which the head will rotate. This pivot is positioned slightly above the base transform, typically around the neck region of humanoid characters, allowing for more natural head movements.

**`UpdateTarget()`**

```csharp
private void UpdateTarget()
{
    _desiredLookAtWeight = lookAway ? Random.Range(0.2f, 1.0f) : 1f;
}
```

This method determines how intently the character should be looking at the target. If `lookAway` is set to `true`, the `_desiredLookAtWeight` can vary between `0.2` (almost looking away) to `1` (directly at the target). If `lookAway` is `false`, the character will always try to look directly at the target.

**`PerformHeadTracking()`**

```csharp
private void PerformHeadTracking()
{
    ...
}
```

The core of the head tracking behavior. This method:

1. Checks the distance between the character and the target. If it's within half the `trackingDistanceThreshold`, tracking is enabled.
2. Adjusts the rotation of the `_headPivot` to face the target.
3. Modulates the amount of body rotation based on the head's angle. For larger angles (when the target is almost beside the character), the body also rotates slightly.
4. Restricts extreme head rotations, ensuring a more natural look.
5. Adjusts the final look-at weights for the body, head, and eyes based on the current situation.

**`SetCurrentLookAtWeight()`**

```csharp
private void SetCurrentLookAtWeight()
{
    ...
}
```

Modulates the `_currentLookAtWeight` based on the difference in angle from the head pivot's current rotation. The goal is to smoothly interpolate between the current look-at weight and the desired one. If the character is looking almost sideways (`angleDifference > 0.65`), the weight is reduced to zero, making the character look forward instead of at the target.

**`AdjustAnimatorLookAt()`**

```csharp
private void AdjustAnimatorLookAt()
{
    ...
}
```

This method uses the `SetLookAtWeight` and `SetLookAtPosition` functions of the Unity's `Animator` component to control how the character looks at the target. The various look-at weights (for body, head, and eyes) are adjusted and clamped within allowed limits, and the character's gaze direction is set towards the target.

***

#### Practical Usecase Scenario:

For a practical application of this script, imagine a museum scene in a game where several NPC (Non-Playable Character) guides are standing around. Using `ConvaiHeadTracking`, each guide can turn their head towards the player as they walk by, making the environment feel more interactive and alive. If `lookAway` is enabled, the NPCs won't constantly stare, but occasionally look around, mimicking real-life behavior.

***

#### Notes

* The script utilizes Unity's IK system to achieve a smooth look-at functionality.
* Care has been taken to ensure the head does not over-rotate, providing a natural appearance.

***
