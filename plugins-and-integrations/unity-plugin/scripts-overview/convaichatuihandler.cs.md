# ConvaiChatUIHandler.cs

{% hint style="info" %}
To understand the script in even more depth, please check out the comments in the script.
{% endhint %}

### Introduction

The `ConvaiChatUIHandler` class is a versatile component in Unity that facilitates the creation of various types of chat-based user interfaces (UIs). It enables characters and users to exchange messages, and it can be configured for different UI styles, such as subtitles, question-answer interfaces, and chat boxes.

#### Requirements

Before using `ConvaiChatUIHandler`, ensure that:

* The GameObject containing this script is set up with the necessary UI components (e.g., TextMeshProUGUI for displaying text).
* The character and user names are defined, and default texts are provided.
* The chat UI type (`UIType`) is selected according to the desired style (Subtitle, QuestionAnswer, or ChatBox).

### Properties

#### Serialized Fields

**Character Settings**

* **`characterName`**: Display name of the character.
* **`characterText`**: Default text of the character.
* **`characterTextColor`**: Color of the character's text.

**User Settings**

* **`userName`**: Display name of the user.
* **`userText`**: Default text of the user.
* **`userTextColor`**: Color of the user's text.

**UI Components**

* **`userTalkingMarker`**: GameObject active when the user is talking.
* **`userTextField`**: TextMeshProUGUI component for displaying the user's text.
* **`characterTextField`**: TextMeshProUGUI component for displaying the character's text.

**UI Settings**

* **`chatUIActive`**: Indicates whether the chat UI is currently visible.
* **`isCharacterTalking`**: Indicates whether the character is currently talking.
* **`isUserTalking`**: Indicates whether the user is currently talking.
* **`uIType`**: Specifies the type of UI to use (Subtitle, QuestionAnswer, or ChatBox).

### Methods

#### `Awake()`

* **Description:** This method finds the necessary game objects based on the selected `uIType` during Awake. It sets up references to UI elements.

#### `Start()`

* **Description:** On Start, this method sets default values for character and user names if not already provided.

#### `Update()`

* **Description:** In Update, this method refreshes the UI based on the current state. It updates the user's text, character's text, and user talking marker visibility according to the selected `uIType`.

#### `SendCharacterText(string charName, string text)`

* **Description:** This method processes text coming from the character based on the selected `uIType`. It updates the character's text with the provided text.

#### `SendUserText(string text)`

* **Description:** This method processes text coming from the user based on the selected `uIType`. It updates the user's text with the provided text.

### ChatBox-Specific Methods

#### `SendCharacterChatBoxMessage(string currentCharacterName, string text)`

* **Description:** This private method handles the display of the character's message in the chat box UI. It appends messages if they are from the same character or creates new messages if necessary.

#### `SendUserChatBoxMessage(string text)`

* **Description:** This private method handles the display of the user's message in the chat box UI. It activates the chat UI if the user is talking, appends messages if needed, and updates the last message if the user sends consecutive messages.

### How to Use

To utilize `ConvaiChatUIHandler` and create chat-based UIs:

1. Attach the `ConvaiChatUIHandler` script to the GameObject representing the chat UI.
2. Customize character and user names, default texts, and text colors in the Inspector.
3. Assign the necessary UI components (TextMeshProUGUI, GameObjects) to the corresponding fields in the Inspector.
4. Choose the appropriate UI type (`uIType`) based on your desired chat UI style (Subtitle, QuestionAnswer, or ChatBox).
5. Implement logic in your game scripts to call `SendCharacterText` and `SendUserText` methods to update the chat UI with character and user messages.

### Practical Use Case Scenario

#### Scenario 1: Subtitle-Style UI

In a story-driven game, use the `ConvaiChatUIHandler` with the `UIType.Subtitle` setting to display character dialogues as subtitles. As the character speaks, call `SendCharacterText` to update the UI with character lines, and similarly, use `SendUserText` to display user responses.

#### Scenario 2: Chat Box UI

For a chat-based interaction in a game, set up the chat UI using `UIType.ChatBox`. As characters and users send messages, call `SendCharacterText` and `SendUserText` to update the chat box with the conversation. The chat box will display messages from multiple characters and users.

#### Scenario 3: Question-Answer UI

In an interactive dialog system, configure the UI as `UIType.QuestionAnswer`. Use `SendCharacterText` to present character questions and `SendUserText` to display user-selected answers. This creates an engaging question-and-answer dialogue interface.





