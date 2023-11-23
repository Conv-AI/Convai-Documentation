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

### Introduction

The ConvaiNPC.cs script is our first dive into the vast array of Convai's conversational agent creation tools. We attach this script to the NPC that we want to be our conversational agent. It contains only an instance of the Character Chatbot but is enough for us to get our hands dirty and learn how the Convai Pipeline works. We can also replicate the script to create our own conversation agent.

#### Requirements

Before using `ConvaiNPC`, ensure that:

* You have integrated the Convai Unity plugin into your Unity project.
* You have the necessary UI elements and components (e.g., `ConvaiChatUIHandler`, `ConvaiGlobalActionSettings`, `ConvaiCrosshairHandler`) correctly set up in your scene.
* You have defined character names, IDs, and other settings in the Inspector.

### Properties

#### Serialized Fields

**Character Settings**

* **`characterID`**: A unique identifier for the character.
* **`characterName`**: The display name of the character.
* **`isCharacterActive`**: Indicates whether the character is currently active.

**Include Components**

These properties determine whether specific components should be included for the character:

* **`includeActionsHandler`**: Include the `ConvaiActionsHandler` component.
* **`includeLipSync`**: Include the `ConvaiLipSync` component.
* **`includeHeadEyeTracking`**: (Not used in this script)
* **`includeBlinking`**: (Not used in this script)

#### Do Not Edit

These properties and fields are not meant for direct editing and are used for internal functionality:

* **`stringCharacterText`**: Internal field for character text processing.
* **`_responseAudios`**: Internal list to store response audio data.
* **`_actionConfig`**: Internal reference to action configuration.
* **`_actionsHandler`**: Internal reference to `ConvaiActionsHandler` component.
* **`_isActionActive`**: Internal flag to determine if actions are active.
* **`_isLipSyncActive`**: Internal flag to determine if lip syncing is active.
* **`_lipSyncHandler`**: Internal reference to `ConvaiLipSync` component.
* **`_playingStopLoop`**: Internal flag to control audio playback loop termination.
* **`GetResponseResponses`**: Internal list to store response data.

Let's go through the individual functions that are being called and understand the flow of control:

#### Imports

We will include a bunch of Utility Scripts in our Convai NPC Script. These contain a gRPC API script that contains a bunch of utility methods used to connect to the servers and send and receive data from the servers. We also have scripts to handle the actions, UI, LipSync, and Crosshairs (player look at pointer).

{% code lineNumbers="true" %}
```csharp
using System.Collections;

using UnityEngine;
using UnityEngine.SceneManagement;

using Grpc.Core;
using Service;

using System.Collections.Generic;

using Convai.gRPCAPI;
using Convai.ActionHandler;
using Convai.UIHandler;
using static Convai.LipSync.ConvaiLipSync;
using Convai.LipSync;
using Convai.CrosshairHandler;
```
{% endcode %}

#### Awake()

In the awake function, we initialize various game objects references present in the scene that we will need to connect with the various components of the Convai Pipeline.&#x20;

We find game objects for the following:

* **gRPC API**: Responsible for communicating with the Convai servers.
* **Chat UI**: Responsible for displaying the transcripts from users and the characters.
* **Global Actions Settings**: Responsible for setting up the global actions related settings like the interactable characters and interactable objects.&#x20;
* **Crosshair Handler**: Responsible for identifying the object or character being pointed at.

We also initialize the components that are part of the character gameObject. These help us figure out which features need to be initialized.&#x20;

* **Action Handler**: Script responsible for setting up the action following by the character.
* **Lip Sync**: Script responsible for handling the lipsync.

```csharp
private void Awake()
```

#### Start()

In the Start function, we will start one coroutine that is responsible for capturing responses from the server and playing them. We will also initialize the gRPC connection.

```csharp
private void Start()
```

#### Update()

In the update function, we do the following:

We start recording when the space bar is pressed, we start sending chunks of audio to the server.

When the left control is released, we stop recording and let the server know that we are ready for a response, and the server sends a response (which is updated in the `getResponseResponses` array).

The Update function also monitors the `getResponseResponses` array and when the array is not empty, i.e. we have a response from the server that needs to be spoken out loud, it processes the response received from the server (in the `ProcessResponse()`).

```csharp
private void Update()
```

#### ProcessResponse()

`ProcessResponse()`decides whether the response is audio data or action data. Based on that the script either creates and adds AudioClips to a playlist (`ResponseAudios`) or sends the response to the action handler for further processing.

```csharp
/// <summary>
///     When the response list has more than one element, 
///     then the audio or the actions will be added to a playlist. 
///     This function adds individual responses to the list.
/// </summary>
/// <param name="getResponseResponse">
///     The getResponseResponse object that will be processed 
///     to add the audio or action and transcript to the playlist
/// </param>
void ProcessResponse(GetResponseResponse getResponseResponse)
```

#### playAudioInOrder()

The script also plays a talking animation when the playlist is not empty (through the `playAudioInOrder()` function).

```csharp
/// <summary>
///     This function plays the streamed audio clips 
///     received from the server in the order they are received.
/// </summary>
private IEnumerator playAudioInOrder() 

```

### How to Use

To use the `ConvaiNPC` script to create intelligent NPC behavior:

1. Attach the `ConvaiNPC` script to the GameObject representing your NPC character.
2. Configure the character settings, including `characterID`, `characterName`, and `isCharacterActive`.
3. Choose which components to include for the character behavior using the `includeActionsHandler` and `includeLipSync` properties.
4. Ensure that you have the necessary UI elements and components (e.g., `ConvaiChatUIHandler`, `ConvaiGlobalActionSettings`, `ConvaiCrosshairHandler`) correctly set up in your scene.
5. Implement logic in your game scripts to call methods like `StartListening` and `StopListening` to control when the character starts and stops talking.
6. Process responses received from characters using the `ProcessResponse` method.
7. Customize character animations and actions based on your game's requirements.
