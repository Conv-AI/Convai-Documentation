---
description: >-
  This page gives a small overview of the "ConvaiNPC.cs" script that controls
  the NPC.
---

# ConvaiNPC.cs

{% hint style="warning" %}
Only go through this if you want to customize the behavior of the NPC. Only proceed if you are familiar with gRPC and how to use it in Unity.
{% endhint %}

{% hint style="info" %}
To understand the script in even more depth, please check out the comments in the script.
{% endhint %}

## Class Overview

The ConvaiNPC.cs script is our first dive into the vast array of Convai's conversational agent creation tools. We attach this script to the NPC that we want to be our conversational agent. It contains only an instance of the Character Chatbot but is enough for us to get our hands dirty and learn how the Convai Pipeline works. We can also replicate the script to create our own conversation agent.

### Requirements

Before using the `ConvaiNPC` script, ensure you have the following:

* Integrated the Convai Unity plugin into your Unity project.
* Set up necessary UI elements and components (e.g., ConvaiChatUIHandler, ConvaiInteractablesData, ConvaiCrosshairHandler) correctly in your scene.
* Defined character settings including character ID, character name, and character activity status in the Inspector.

***

## Properties

### Character Information

* `characterName` (String): The NPC's display name.
* `characterID` (String): A unique identifier for the NPC.
* `sessionID` (String): The current session ID for the chat with the NPC.
* `isCharacterActive` (Boolean): Indicates if the NPC is currently active.

### Hidden Fields

* `actionsHandler` (ConvaiActionsHandler): Reference to the actions handler component.
* `lipSyncHandler` (ConvaiLipSync): Reference to the lip sync component.
* `_responseAudios` (List of ResponseAudio): Stores audio response data.
* `GetResponseResponses` (Queue of GetResponseResponse): Stores response data.

### Other References

* `_actionConfig` (ActionConfig): Reference to action configuration.
* `_isActionActive` (Boolean): Flag indicating if actions are active.
* `_isLipSyncActive` (Boolean): Flag indicating if lip syncing is active.
* `IncludeActionsHandler`, `LipSync`, `HeadEyeTracking`, `EyeBlinking` (Boolean): Flags for including various components.

## Functions

### Initialization

* [`Awake()`](convainpc.cs.md#awake): Initializes component references and logs initialization.
* [`Start()`](convainpc.cs.md#start): Sets up gRPC communication, starts audio playback coroutine, and requests microphone permissions on Android.

### Runtime

* [`Update()`](convainpc.cs.md#update): Manages text input, character actions, scene management, and character animations.
* [`OnApplicationQuit()`](convainpc.cs.md#onapplicationquit): Stops the audio playback loop.

### Text Input Handling

* [`HandleTextInput`](convainpc.cs.md#handletextinput)`()`: Manages user text input and submission.
* [`WatchForInputSubmission`](convainpc.cs.md#watchforinputsubmission)`()`: Watches for input submission and updates the current input field.
* [`HandleInputSubmission`](convainpc.cs.md#handleinputsubmission-string-input)`(string input)`: Handles text input submission and sends data to the server.

### Character Actions

* [`HandleCharacterActions`](convainpc.cs.md#handlecharacteractions)`()`: Manages character-specific actions like audio recording.
* [`UpdateActionConfig`](convainpc.cs.md#updateactionconfig)`()`: Updates the action configuration with the current attention object.

### Scene Management

* [`HandleSceneManagement`](convainpc.cs.md#handlescenemanagement)`()`: Manages scene-related actions like reloading and quitting.

### Animation

* [`HandleCharacterTalkingAnimation`](convainpc.cs.md#handlecharactertalkinganimation)`()`: Manages the character's talking animation.

### Audio Recording

* [`StartListening`](convainpc.cs.md#startlistening)`()`: Initiates the audio recording process using gRPC.
* [`StopListening`](convainpc.cs.md#stoplistening)`()`: Stops the ongoing audio recording process.

### Response Processing

* [`ProcessResponse`](convainpc.cs.md#processresponse)`()`: Processes responses from the character, adding audio to the playlist and parsing actions.

### Audio Playback

* [`PlayAudioInOrder`](convainpc.cs.md#playaudioinorder)`()`: Plays audio clips in the order of responses, managing animations and lip syncing.

Let's go through the individual functions that are being called and understand the flow of control.

***

## ConvaiNPC Script Functions

This documentation provides detailed information about the important functions within the `ConvaiNPC` script. These functions are crucial for creating intelligent NPC behavior in Unity using the Convai conversational agent creation tools.

### `Awake()`

The `Awake()` function is integral to the initialization process of the `ConvaiNPC` component, setting up the necessary references for the NPC's conversational capabilities. This method is invoked automatically when the script instance is loaded. The following steps outline its key operations:

* Logs an informational message indicating the initialization of the `ConvaiNPC` component for the character specified by `characterName`.
* Locates and assigns the `ConvaiChatUIHandler` component within the scene, which is tasked with managing the display of chat transcripts.
* Searches for and assigns the `ConvaiCrosshairHandler` component, which is essential for identifying interactive objects or characters within the player's focus.
* Retrieves the `AudioSource` component attached to the same GameObject, a crucial element for handling audio playback.
* Acquires the `Animator` component from the same GameObject, enabling the control of character animations.
* Checks for the presence of a `ConvaiActionsHandler` component on the GameObject. If found, it:
  * Sets the `_isActionActive` flag to `true`, indicating that action handling is enabled.
  * Obtains the `ConvaiActionsHandler` component and extracts its action configuration stored in `_actionConfig`.

### `Start()`

Start() The `Start()` function is tasked with establishing the gRPC communication, initiating audio playback, and handling user permissions on Android devices. It is called before the first frame update after all `Awake()` functions have been executed. Here's a breakdown of its responsibilities:

* Assigns the `ConvaiGRPCAPI` component from the scene to the `_grpcAPI` variable, ensuring that the script has access to the necessary gRPC API methods.
* Begins the [`PlayAudioInOrder`](convainpc.cs.md#playaudioinorder)`()` coroutine, which is responsible for playing audio clips sequentially as they are received.
* Sets up a repeating invocation of the [`ProcessResponse`](convainpc.cs.md#processresponse)`()` method, which processes character responses at a specified interval (100 times per second in this case).
* Starts the [`WatchForInputSubmission`](convainpc.cs.md#watchforinputsubmission)`()` coroutine, which monitors for user input submissions.
* Checks if the application is running on an Android platform and, if so, verifies whether the user has granted microphone permissions. If not, it requests permission from the user to access the microphone.
* Establishes a secure gRPC communication channel with the server by creating SSL credentials and initializing a gRPC channel with the specified endpoint and credentials.
* Initializes the gRPC client for the `ConvaiService` using the channel created, allowing for communication with the Convai service.
* Calls the `ConvaiGRPCAPI.InitializeSessionIDAsync()` method to asynchronously initialize the session ID, passing in the character name, gRPC client, character ID, and current session ID. The session ID is then updated with the value returned from this call.

### `Update()`

The `Update()` method is called every frame and is responsible for handling various real-time interactions and updates within the scene. It performs the following actions:

* Checks if the character is active and handles text input focus and submission by calling [`HandleTextInput()`](convainpc.cs.md#handletextinput).
* If the character is active and the input field is not focused, it calls [`HandleCharacterActions`](convainpc.cs.md#handlecharacteractions)`()` to manage character-specific actions such as starting and stopping audio recording.
* Calls [`HandleSceneManagement`](convainpc.cs.md#handlescenemanagement)`()` to handle scene management actions, including scene reloading and application quitting.
* Manages the character's talking animation by invoking [`HandleCharacterTalkingAnimation`](convainpc.cs.md#handlecharactertalkinganimation)`()` based on whether the character is currently talking.

### `HandleSceneManagement()`

The `HandleSceneManagement()` method deals with scene management actions such as reloading the current scene or quitting the application. Here's how it functions:

* Listens for simultaneous presses of the 'R' key and '=' key. If detected, it reloads the current scene using `SceneManager.LoadScene(SceneManager.GetActiveScene().name)`.
* Checks for simultaneous presses of the 'Escape' key and '=' key. If this combination is pressed, it quits the application by calling `Application.Quit()`.

### `HandleCharacterTalkingAnimation()`

The `HandleCharacterTalkingAnimation()` method controls the character's talking animation, ensuring it reflects whether the character is currently engaged in conversation. The method works as follows:

* If `_isCharacterTalking` is true and the animation is not already playing, it sets `_animationPlaying` to true and triggers the talking animation by setting the `Talk` parameter in the `_characterAnimator` to true.
* Conversely, if `_isCharacterTalking` is false and the animation is playing, it sets `_animationPlaying` to false and stops the talking animation by setting the `Talk` parameter in the `_characterAnimator` to false.

### `WatchForInputSubmission()`

The `WatchForInputSubmission()` coroutine is dedicated to monitoring input submissions within the scene and updating the reference to the current input field. It is designed to run continuously throughout the game and should be initiated only once to avoid duplication. Here's an in-depth look at its functionality:

* Enters an infinite loop, allowing it to run indefinitely and check for input field changes each frame.
* Utilizes the [`FindActiveInputField`](convainpc.cs.md#findactiveinputfield)`()` method to locate an active `TMP_InputField` within the scene.
* If a new active input field is detected and it differs from the current one (`_currentInputField`), the following actions are taken:
  * Any existing listeners on the previous `_currentInputField` are removed to prevent multiple submissions (`_currentInputField.onSubmit.RemoveAllListeners()`).
  * The `_currentInputField` variable is updated to reference the newly active input field.
  * A new listener is added to the `_currentInputField`'s `onSubmit` event, which will trigger the `HandleInputSubmission()` method upon input submission.

### `HandleInputSubmission(string input)`

The `HandleInputSubmission()` method is responsible for processing the text input submitted by the user. It performs several key actions to ensure the input is handled correctly:

* Logs the action of sending user text to the server for debugging purposes using `Logger.DebugLog()`.
* Passes the player's text input to the server through `_chatUIHandler.SendPlayerText(input)`.
* Initiates an asynchronous operation `SendTextDataAsync(input)` to send the text data to the server without awaiting the result, preventing any blocking of the UI thread. It captures the context to return to the main thread after the server call is complete.
* Clears the text from the active input field by setting its `text` property to an empty string, ensuring the field is ready for new input.

### `FindActiveInputField()`

The `FindActiveInputField()` method searches the scene to find the currently active `TMP_InputField`. Here's how it operates:

* Retrieves all instances of `TMP_InputField` components present in the scene using `FindObjectsOfType<TMP_InputField>()`.
* Iterates through the array of input fields and returns the first one that is both active in the hierarchy and interactable, ensuring that only a usable input field is selected.
* If no active and interactable input field is found, the method returns `null`.

This method is crucial for identifying which input field the player is currently interacting with, allowing for accurate text submission handling.

### `OnApplicationQuit()`

The `OnApplicationQuit()` function is called when the application is quitting. It stops the loop that plays audio in order by setting the `_playingStopLoop` flag to true.

### `HandleTextInput()`

The `HandleTextInput()` function is tasked with managing the user's text input and its submission within the UI. This function is called within the [`Update()`](convainpc.cs.md#update) method to continuously check for user input. Here's a breakdown of its responsibilities:

* Monitors the current input field to determine if it is focused, allowing for user interaction.
* Detects when the user presses the Return key (Enter) or the KeypadEnter key, which triggers the submission of the text entered by the user.
* Upon submission, the function calls [`HandleInputSubmission()`](convainpc.cs.md#handleinputsubmission-string-input) with the text from the input field, processes the user's input, and then clears the input field for future use.
* Resets the input field text to an empty string and deactivates the input field if the Escape key is pressed, effectively canceling the input operation.
* Ensures that no further input handling occurs while the input field is active and focused, preventing unintended interactions with other UI elements or game controls.

### `HandleCharacterActions()`&#x20;

The `HandleCharacterActions()` method is integral to the `ConvaiNPC` script, providing the logic for initiating and terminating audio recording based on player input. Here's a detailed overview of its operation:

* Listens for the press of the 'T' key to begin audio recording. Upon detection, it performs the following:
  * Calls `UpdateActionConfig()` to ensure the action configuration is current, particularly updating the object of attention if the crosshair is pointing at a new object.
  * Invokes `StartListening()` to initiate the audio recording process, enabling the NPC to listen to player input.
* Detects when the 'T' key is released, signaling the end of audio input. It then calls `StopListening()` to terminate the recording process.

### `UpdateActionConfig()`&#x20;

The `UpdateActionConfig()` method updates the action configuration, specifically the attention object, which is the object currently being targeted by the player's crosshair. Here's what it does:

* Checks if the `_actionConfig` and `_convaiCrosshairHandler` are not null, ensuring that the necessary components are available for updating.
* Assigns the current attention object to `_actionConfig.CurrentAttentionObject` by calling `_convaiCrosshairHandler.FindPlayerReferenceObject()`, which identifies the object the crosshair is pointing at.

These methods collectively manage the audio interaction between the NPC and the player, allowing for a responsive and engaging conversational experience within the game.

### `StartListening()`

The `StartListening()` method is a public asynchronous function that handles the initialization of the audio recording session and manages communication with the server via gRPC. Here's the process it follows:

* Verifies that the character is active and ready to start listening.
* Begins the audio recording process by calling the `StartRecordAudio` method from the `ConvaiGRPCAPI`, passing in the necessary parameters such as the gRPC client, action activity status, lip sync status, recording frequency, recording length, character ID, action configuration, and face model.

### `StopListening()`

The `StopListening()` method is responsible for stopping the ongoing audio recording process. Here's its functionality:

* Calls the `StopRecordAudio` method from the `ConvaiGRPCAPI` to halt the audio recording, effectively ending the NPC's listening phase.

### `ProcessResponse()`

The `ProcessResponse()` method is tasked with handling the responses received from a character. It is a critical component of the NPC's conversational system, ensuring that the NPC can respond to the player with audio, text, and facial expressions. The method's operations are as follows:

* Begins by checking if the character is active and if there are any responses to process in the `GetResponseResponses` queue.
* If responses are available, it dequeues the next `GetResponseResponse` object for processing.
* Checks if the dequeued response contains an audio response. If it does, the following actions are taken:
  * Verifies that the audio data is not empty by checking the byte array length.
  * Extracts the text data from the response and initializes a string to hold it.
  * Converts the audio data from bytes to an `AudioClip` using the `_grpcAPI.ProcessByteAudioDataToAudioClip()` method, which also takes into account the sample rate.
  * Adds the processed audio and text data to the `_responseAudios` list, encapsulated in a new `ResponseAudio` object.
* If the response does not contain audio but includes a debug log, it adds a final `ResponseAudio` object to the list with null audio and transcript, indicating the end of the response sequence.
* If no responses are left to process, it sets `_isCharacterTalking` to false, indicating that the character has finished speaking.

### `PlayAudioInOrder()`

The `PlayAudioInOrder()` coroutine is responsible for playing audio clips that are attached to characters, following the sequence of responses. It ensures that the NPC's verbal responses are delivered in the correct order and are accompanied by appropriate actions and animations. Here's how it functions:

* Enters a loop that will continue to run until `_playingStopLoop` is set to true, typically when the application is about to quit.
* Within the loop, it first checks if there are any audio clips queued in the `_responseAudios` list.
* If there are clips to be played, it retrieves the first `ResponseAudio` object from the list.
* If the `ResponseAudio` object is not marked as final (`!currentResponseAudio.isFinal`), the following actions are performed:
  * The audio clip from the `ResponseAudio` object is set as the current clip for the `_audioSource` to play.
  * The audio source is instructed to play the clip, and `_isCharacterTalking` is set to true, indicating that the character is now talking.
  * If a `lipSyncHandler` is present, it is also notified that the character is talking (`lipSyncHandler.isCharacterTalking = true`).
  * The `ChatUIHandler` is updated to reflect that the character is talking (`_chatUIHandler.IsCharacterTalking = true`).
  * If the `ResponseAudio` object contains a non-empty transcript, it is sent to the `ChatUIHandler` to display the character's text alongside the audio.
  * The coroutine then waits for the duration of the audio clip (`yield return new WaitForSeconds(currentResponseAudio.AudioClip.length)`), allowing the clip to play in its entirety.
  * Once the clip has finished playing, the audio source is stopped, and the clip is cleared.
  * The `ChatUIHandler` is updated to indicate that the character has stopped talking (`_chatUIHandler.IsCharacterTalking = false`).
* After processing the current `ResponseAudio` object, it is removed from the list.
* If there are no audio clips to play, the coroutine yields until the next frame (`yield return null`) before checking again.
