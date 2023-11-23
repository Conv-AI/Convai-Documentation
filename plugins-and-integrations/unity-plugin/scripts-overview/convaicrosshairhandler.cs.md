# ConvaiCrosshairHandler.cs

{% hint style="info" %}
To understand the script in even more depth, please check out the comments in the script.
{% endhint %}

The `ConvaiCrosshairHandler` script is responsible for managing the crosshair behavior in the Convai application. It allows detection of the Convai game object currently under the player's crosshair, enabling interactions with the focused object or character. This script is crucial for providing a user-friendly and interactive experience within the Convai application.

### Properties

#### Cached References

* **`_camera`** (Type: `Camera`): A reference to the player's camera, obtained from the GameObject tagged as "Player." This camera is used to determine what the player's crosshair is looking at.
* **`_globalActionSettings`** (Type: `ConvaiGlobalActionSettings`): A reference to the `ConvaiGlobalActionSettings` component, which stores information about interactable objects and characters within the Convai application.

### Methods

#### `Awake()`

* **Description:** Initializes the script by finding necessary components in the scene. It locates the `ConvaiGlobalActionSettings` component and retrieves the player's camera.

#### `FindPlayerReferenceObject()`

* **Description:** Finds the reference object currently under the player's crosshair. It uses raycasting from the center of the screen to detect what the crosshair is looking at.
* **Returns:** A reference string for the interactable object or character under the crosshair. Returns "None" if no valid hit is detected.

#### `FindInteractableReference(Object lookingAtGameObject)`

* **Description:** A helper method to find the reference of an interactable object or character based on the GameObject that the crosshair is looking at.
* **Parameters:**
  * `lookingAtGameObject` (Type: `Object`): The GameObject being looked at by the crosshair.
* **Returns:** A reference string for the interactable object or character. Returns "None" if no matching reference is found.

### How to Use

To implement crosshair functionality in your Convai application using the `ConvaiCrosshairHandler` script, follow these steps:

1. Attach the `ConvaiCrosshairHandler` script to an appropriate GameObject in your scene, such as the player's character or a dedicated crosshair object.
2. Create and configure a `ConvaiGlobalActionSettings` component in your scene. This component should contain information about the interactable objects and characters within your Convai application.
3. In the Inspector, assign the `ConvaiGlobalActionSettings` component to the `_globalActionSettings` field of the `ConvaiCrosshairHandler` script.
4. Ensure that the player's camera is correctly tagged as "Player" in your scene hierarchy. The script relies on this tag to locate the camera.
5. Use the `FindPlayerReferenceObject()` method to determine the reference of the interactable object or character currently under the player's crosshair. You can call this method when the player interacts with the environment to identify the target of their interaction.
