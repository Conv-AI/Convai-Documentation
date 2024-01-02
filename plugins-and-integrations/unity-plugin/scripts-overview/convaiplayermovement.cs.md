---
description: >-
  The ConvaiPlayerMovement class provides essential functionality for
  first-person character control in a Unity scene.
---

# ConvaiPlayerMovement.cs

## Class Overview

The `ConvaiPlayerMovement` script is designed for controlling the movement and camera rotation of a character in a Unity game using the CharacterController component. It provides a straightforward way to handle player input for walking, running, jumping, and looking around with the mouse. This script is essential for creating responsive and immersive player controls in your Unity projects.

### **Requirements**

* This class requires the GameObject to which it is attached to have a `CharacterController` component.
* The script is designed for first-person player control.

## Properties

#### Movement Properties

**`walkingSpeed`:**

* **Type:** float (Range: 1 to 10)
* **Description:** The walking speed of the character.

**`runningSpeed`:**

* **Type:** float (Range: 1 to 10)
* **Description:** The running speed of the character.

**`jumpSpeed`:**

* **Type:** float (Range: 1 to 10)
* **Description:** The speed at which the character jumps.

**`gravity`:**

* **Type:** float (Range: 1 to 10)
* **Description:** The gravitational force applied to the character.

**`playerCamera`:**

* **Type:** Camera
* **Description:** The camera used to control the character's view.

#### Look Properties

**`lookSpeed`:**

* **Type:** float (Range: 1 to 10)
* **Description:** The speed at which the camera rotates when looking around.

**`lookXLimit`:**

* **Type:** float (Range: 1 to 90)
* **Description:** The limit on the camera's vertical rotation, preventing it from over-rotating.

#### Miscellaneous Property

**`canMove`:**

* **Type:** bool
* **Description:** Determines whether the character can move. When set to false, player input is ignored.

## Functions&#x20;

1. `Start()`: Initializes the character controller and locks the cursor for player control.
2. `Update()`: Main update function that handles cursor locking/unlocking, player movement, and player and camera rotation.
3. `HandleCursorLocking()`: Unlocks the cursor when the ESC key is pressed and re-locks it when the left mouse button is pressed. Prevents locking when the mouse is over a UI element.
4. `LockCursor()`: Locks the cursor for player control.
5. `MovePlayer()`: Moves the player based on input, including walking, running, and jumping. Handles gravity and character movement.
6. `RotatePlayerAndCamera()`: Rotates the player and camera based on mouse input. Handles both horizontal and vertical rotation.

## ConvaiPlayerMovement Script Functions:

### **`Start()`**

This method is called when the script instance is being loaded. It initializes the character controller and locks the cursor to enable player control

### **`Update()`**

The `Update()` method is executed every frame. It handles cursor locking/unlocking, player movement, and player and camera rotation.

### **`HandleCursorLocking()`**

This private method manages cursor locking and unlocking. It unlocks the cursor when the ESC key is pressed and re-locks it when the left mouse button is pressed. It also prevents cursor locking when the mouse is over a UI element.

### **`LockCursor()`**

This static method is used to lock the cursor, making it invisible and confined to the game window, ensuring a smooth player control experience.

### **`MovePlayer()`**

The `MovePlayer()` method handles player movement based on input, including walking, running, and jumping. It calculates the player's movement direction, handles jump, and applies gravity.

### **`RotatePlayerAndCamera()`**

This method is responsible for rotating the player and the camera based on mouse input. It handles both vertical and horizontal rotation, controlling the player's view direction

## How to Use

To implement player movement and camera control in your Unity project using `ConvaiPlayerMovement`, follow these steps:

1. Attach the `ConvaiPlayerMovement` script to the GameObject representing the player character.
2. Customize the movement and camera control properties, such as walking speed, running speed, jump speed, gravity, look speed, and look limits, to match your game's requirements.
3. Assign the player's camera to the `playerCamera` field to enable camera rotation.
4. Optionally, set the `canMove` property to `false` to disable player movement temporarily, such as during cutscenes or menu screens.
5. Implement other game mechanics or interactions that depend on player movement and camera control.
