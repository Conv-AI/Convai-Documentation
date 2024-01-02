---
description: >-
  This page gives a small overview of the "ConvaiGRPCAPI.cs" script that handles
  the inputs and outputs to the server.
---

# ConvaiGRPCAPI.cs

{% hint style="warning" %}
Only go through this if you want to customize the behavior of the NPC. Only proceed if you are familiar with gRPC and how to use it in Unity.
{% endhint %}

{% hint style="info" %}
To understand the script in even more depth, please check out the comments in the script.
{% endhint %}

The `ConvaiGRPCAPI` class is a critical component that manages all communications between the Convai server and the Unity plugin, as well as processing the data exchanged during these interactions. This class abstracts the underlying complexities of the Convai Unity plugin, providing a seamless interface for users. Modifying this class is discouraged as it may affect the stability and functionality of the system. The class is maintained by the development team to ensure compatibility and performance.

## Class Overview

The `ConvaiGRPCAPI` class serves as a central component for managing communications between the Convai server and your Unity project. It abstracts the complexities of communication, enabling seamless interactions with NPC characters. This class is crucial for creating immersive conversational experiences within your game.

### Requirements

To use the `ConvaiGRPCAPI` class effectively, you must ensure:

* The `ConvaiAPIKeySetup` ScriptableObject is set up correctly with your Convai API key.
* Your Unity project includes essential UI components like `ConvaiChatUIHandler` and `ConvaiGlobalActionSettings` to facilitate user interactions.
* NPC characters in your scene are configured with their character settings.

***

## Properties

The `ConvaiGRPCAPI` class features the following properties:

* `Instance`: A public static instance of the ConvaiGRPCAPI class. This singleton instance allows for easy access from other scripts within the project.
* `APIKey`: A hidden string field that stores the Convai API key.
* `_stringUserText`: A hidden list of strings to manage pending user text for display.
* `_activeConvaiNPC`: A hidden reference to the currently active Convai NPC character.
* `_chatUIHandler`: A reference to the `ConvaiChatUIHandler` component for user interface handling.
* `_cancellationTokenSource`: A private field that is used for potential task cancellation.

***

## Functions

Functions in the `ConvaiGRPCAPI` script:

* [`Awake()`](convaigrpcapi.cs.md#awake): Initializes references to components and loads the API key.
* [`Start()`](convaigrpcapi.cs.md#awake): Initializes gRPC and event handlers for audio processing.
* [`FixedUpdate()`](convaigrpcapi.cs.md#fixedupdate): Sends user text to the chat UI for display.
* [`OnDestroy()`](convaigrpcapi.cs.md#ondestroy): Unsubscribes from event handlers.
* [`HandleActiveNPCChanged()`](convaigrpcapi.cs.md#handleactivenpcchanged): Called when the active NPC changes.
* [`ProcessRequestAudioToWav()`](convaigrpcapi.cs.md#processrequestaudiotowav): Converts an audio clip into WAV byte data.
* [`Convert16BitByteArrayToFloatAudioClipDat()`](convaigrpcapi.cs.md#convert16bitbytearraytofloataudioclipdata): Converts 16-bit audio byte array to a float array.
* [`ProcessStringAudioDataToAudioClip()`](convaigrpcapi.cs.md#processstringaudiodatatoaudioclip): Converts string-encoded audio data to an AudioClip.
* [`ProcessByteAudioDataToAudioClip()`](convaigrpcapi.cs.md#processbyteaudiodatatoaudioclip): Converts a byte array containing audio data into an AudioClip.
* [`StartRecordAudio()`](convaigrpcapi.cs.md#startrecordaudio): Initiates audio recording and sends it to the server for processing.
* [`StopRecordAudio()`](convaigrpcapi.cs.md#stoprecordaudio): Stops audio recording.
* [`ProcessAudioChunk()`](convaigrpcapi.cs.md#processaudiochunk): Processes and sends audio chunks to the server.
* [`ReceiveResultFromServer()`](convaigrpcapi.cs.md#receiveresultfromserver): Periodically receives responses from the server and adds them to an NPC's response list.
* [`AddByteToArray()`](convaigrpcapi.cs.md#addbytetoarray): Adds a WAV header to audio data for playback.

***

## Imports

We will import Service which is a script that has been created from a gRPC protocol buffer. This includes all the tools necessary for communicating with the server.&#x20;

{% code overflow="wrap" lineNumbers="true" %}
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Google.Protobuf;
using Grpc.Core;
using Service;
using UnityEngine;
using static Service.GetResponseRequest.Types;
```
{% endcode %}

***

## ConvaiGRPCAPI Script Functions

### `Awake()`

The awake function sets up the API key and initializes the script. It also gets the reference to the Chat UI Handler so that transcripts from users and the character can be handled.

### `Update()`

This method is responsible for managing the `ConvaiGRPCAPI` component during every frame update. It checks for pending user texts, updates the active NPC, and controls audio playback.&#x20;

* This method checks if there are pending user texts to be displayed. If so, it sends the first user text to the chat UI for presentation and removes it from the list.
* It also monitors the active NPC and keeps track of it to manage interactions.
* This function plays a role in controlling the playback of audio.

### **`FixedUpdate()`**

This method is called at fixed time intervals and is used to handle specific tasks within the `ConvaiGRPCAPI` script. In this context, it is responsible for processing and sending pending user text to the chat user interface (UI). It operates by checking if there is user text to display, and if so, it utilizes the chat UI handler to send the first user text in the list.

### **`OnDestroy()`**

The `OnDestroy()` function is a Unity callback method that is automatically called when the GameObject to which the script is attached is destroyed. In the `ConvaiGRPCAPI` script, this method is responsible for cleaning up resources and unsubscribing from event handlers to ensure proper memory management.

### **`HandleActiveNPCChanged()`**

This method is called whenever the active NPC changes. It updates the `_activeConvaiNPC` field with the new active NPC.

* **Parameters:**
  * `newActiveNPC` (ConvaiNPC): The new active NPC that has been selected.

### **`ProcessRequestAudioToWav()`**

```csharp
public byte[] ProcessRequestAudiotoWav(AudioClip requestAudioClip)
```

This method converts an audio clip into WAV byte data. It takes an `AudioClip` as input, retrieves audio data, and converts it into a byte array containing WAV audio data.

* **Parameters:**
  * `requestAudioClip` (AudioClip): The audio clip to be converted
* **Returns:**
  * Byte array containing WAV audio data

### **Convert16BitByteArrayToFloatAudioClipData()**

```csharp
float[] Convert16BitByteArrayToFloatAudioClipData(byte[] source)
```

This private method converts a byte array representing 16-bit audio samples to a float array. It is used to convert audio data from Convai server responses into a format suitable for Unity's `AudioClip`.

* **Parameters:**
  * `source` (byte\[]): Byte array containing 16-bit audio data
* **Returns:**
  * Float array containing audio samples in the range \[-1, 1

### ProcessStringAudioDataToAudioClip()

{% code overflow="wrap" %}
```csharp
public AudioClip ProcessStringAudioDataToAudioClip(string audioData, string stringSampleRate)
```
{% endcode %}

This method converts string-encoded audio data to an `AudioClip`. It takes a base64-encoded audio data string and the sample rate as input, decodes the audio data, and creates an `AudioClip` from it.

* **Parameters:**
  * `audioData` (string): String containing base64-encoded audio data
  * `stringSampleRate` (string): String representing the sample rate of the audio
* **Returns:**
  * AudioClip containing the decoded audio data

### ProcessByteAudioDataToAudioClip()

{% code overflow="wrap" %}
```csharp
public AudioClip ProcessByteAudioDataToAudioClip(byte[] byteAudio, string stringSampleRate)
```
{% endcode %}

This method converts a byte array containing audio data into an `AudioClip`. It is capable of processing audio data received from the Convai server, trimming the WAV header, and creating an `AudioClip`.

* **Parameters:**
  * `byteAudio` (byte\[]): Byte array containing the audio data
  * `stringSampleRate` (string): String containing the sample rate of the audio
* **Returns:**
  * AudioClip containing the decoded audio data

### StartRecordAudio()

{% code overflow="wrap" %}
```csharp
public async Task StartRecordAudio(ConvaiService.ConvaiServiceClient client, bool isActionActive, int recordingFrequency, int recordingLength, string characterID, ActionConfig actionConfig)
```
{% endcode %}

This method starts recording audio and sends it to the Convai server for processing. It is asynchronous and takes several parameters, including the gRPC client, recording configuration, character ID, and action configuration. It sends audio data in chunks to the server for real-time processing.

* **Parameters:**
  * `client` (ConvaiService.ConvaiServiceClient): gRPC service Client object
  * `isActionActive` (bool): Bool specifying whether we are expecting action responses
  * `isLipSyncActive` (bool): (Description of isLipSyncActive parameter)
  * `recordingFrequency` (int): Frequency of the audio being sent
  * `recordingLength` (int): Length of the recording from the microphone
  * `characterID` (string): Character ID obtained from the playground
  * `actionConfig` (ActionConfig): Object containing the action configuration

### StopRecordAudio()

This method stops recording and processing audio, effectively ending microphone recording. It logs information about the cessation of audio recording.

```csharp
 public void StopRecordAudio()
```

### **`ProcessAudioChunk()`**

{% code overflow="wrap" %}
```csharp
ProcessAudioChunk(AsyncDuplexStreamingCall<GetResponseRequest, GetResponseResponse> call, int diff, float[] audioData)
```
{% endcode %}

This private method processes each audio chunk and sends it to the server. It is used internally to send audio data in chunks to the server for real-time processing.

* **Parameters:**
  * `call` (AsyncDuplexStreamingCall\<GetResponseRequest, GetResponseResponse>): gRPC Streaming call connecting to the getResponse function
  * `diff` (int): Length of the audio data from the current position to the position of the last sent chunk
  * `audioData` (float\[]): Chunk of audio data that we want to be processed

### ReceiveResultFromServer()

{% code overflow="wrap" %}
```csharp
async Task ReceiveResultFromServer(AsyncDuplexStreamingCall<GetResponseRequest, GetResponseResponse> call)
```
{% endcode %}

This private method continuously receives responses from the Convai server and adds them to a static list in the active NPC. It processes different types of responses, including user queries, audio responses, and action responses. Additionally, it updates the session ID in the active NPC.

* **Parameters:**
  * `call` (AsyncDuplexStreamingCall\<GetResponseRequest, GetResponseResponse>): gRPC Streaming call connecting to the getResponse function

This function listens to the server for any results that it sends for the current query until the complete response is received from the server. This response is received in chunks. The chunks are classified into Audio Response or Action Response and then sent to the ConvaiNPC and ConvaiActionHandler respectively for processing.

### AddByteToArray()

{% code overflow="wrap" %}
```csharp
byte[] AddByteToArray(byte[] audioByteArray, string sampleRate)
```
{% endcode %}

A utility function that adds wav header to audioByteData to make it compatible with wav format. This private method adds a WAV header to the audio data, converting it into a byte array suitable for playback and storage. It takes an audio byte array and the sample rate as input and returns a new byte array with the WAV header added.

* **Parameters:**
  * `audioByteArray` (byte\[]): Byte array containing audio data
  * `sampleRate` (string): Sample rate of the audio that needs to be processed
* **Returns:**
  * Byte array with added WAV header
