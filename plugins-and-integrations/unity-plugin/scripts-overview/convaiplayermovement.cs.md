# ConvaiPlayerMovement.cs

The `ConvaiPlayerMovement` script is designed for controlling the movement and camera rotation of a character in a Unity game using the CharacterController component. It provides a straightforward way to handle player input for walking, running, jumping, and looking around with the mouse. This script is essential for creating responsive and immersive player controls in your Unity projects.

### Properties

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

### Methods

#### `Start()`

* **Description:** This method is called on Start and performs initial setup for character movement and camera control. It locks the cursor to provide a more immersive experience.

#### `Update()`

* **Description:** This method is called on Update and handles player input for movement and camera rotation. It allows the player to switch between walking and running, jump, and look around with the mouse.

#### `SetupCharacter()`

* **Description:** Initializes the `_characterController` by getting the CharacterController component attached to the GameObject.

#### `LockCursor()`

* **Description:** Locks the cursor to the center of the screen and hides it. This function is used to provide a clean and immersive gameplay experience.

#### `Jump()`

* **Description:** Handles character jumping. If the jump button is pressed (`"Jump"`) and the character is grounded, it applies an upward force to make the character jump.

#### `ApplyGravity()`

* **Description:** Applies gravity to the character's vertical movement. If the character is not grounded, it simulates the effect of gravity.

#### `MovePlayer(bool isRunning)`

* **Description:** Moves the character based on user input. It calculates the movement direction based on the character's forward and right vectors, as well as the user's input for walking or running.

#### `RotatePlayerAndCamera()`

* **Description:** Rotates both the player and the camera based on mouse input. It allows the player to look around in a first-person perspective. The camera's vertical rotation is limited to prevent over-rotation.

### How to Use

To implement player movement and camera control in your Unity project using `ConvaiPlayerMovement`, follow these steps:

1. Attach the `ConvaiPlayerMovement` script to the GameObject representing the player character.
2. Customize the movement and camera control properties, such as walking speed, running speed, jump speed, gravity, look speed, and look limits, to match your game's requirements.
3. Assign the player's camera to the `playerCamera` field to enable camera rotation.
4. Optionally, set the `canMove` property to `false` to disable player movement temporarily, such as during cutscenes or menu screens.
5. Implement other game mechanics or interactions that depend on player movement and camera control.
