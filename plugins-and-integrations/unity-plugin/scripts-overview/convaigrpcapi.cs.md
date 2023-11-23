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

ConvaiGRPCAPI is responsible for all server-client communications and other data processing. This function effectively handles the nitty-gritty side of our plugin and is **not meant to be edited**.&#x20;

This script is usually added as part of the Camera GameObject in the player controller. This is so that the attached trigger collider can be used to determine which is the active character currently being spoken to.

Let's go through the individual functions that are being called and understand the flow of control:

#### Imports

We will import Service which is a script that has been created from a gRPC protocol buffer. This includes all the tools necessary for communicating with the server.&#x20;

{% code overflow="wrap" lineNumbers="true" %}
```csharp
using System;
using System.Threading.Tasks;

using UnityEngine;

using Grpc.Core;
using Service;
using static Service.GetResponseRequest.Types;
using Google.Protobuf;

using Convai.NPC;
using Convai.APIKeySetup;
using Convai.UIHandler;

using System.Collections.Generic;
```
{% endcode %}

#### Awake()

The awake function sets up the API key and initializes the script. It also gets the reference to the Chat UI Handler so that transcripts from users and the character can be handled.

```csharp
private void Awake()
```

#### Update()

The update function primarily handles the Chat UI and sends the user's transcript to the chat handler.

```csharp
private void Update()
```

#### OnTriggerEnter()

This function listens to any trigger collisions. Here it is looking for trigger collision with the collider attached to the camera, that we use to identify which character is currently being spoken to.

We check if the object that triggered the collider has the tag character and has the ConvaiNPC component attached to it. If there is, the current character is set as active and the previous character is set as inactive.

{% code overflow="wrap" %}
```csharp
/// <summary>
/// This function is called when a collider enters the trigger zone of the GameObject.
/// It sets the active character based on the character the player is facing.
/// </summary>
/// <param name="other">The collider of the object that entered the trigger zone</param>
private void OnTriggerEnter(Collider other)
```
{% endcode %}

#### ProcessRequestAudiotoWav()

This function converts the audio recorded an as Unity audioClip and converts it to byte data in the wav format.

```csharp
/// <summary>
/// Converts an audio clip into WAV byte data.
/// </summary>
/// <param name="requestAudioClip">The audio clip to be converted</param>
/// <returns>Byte array containing WAV audio data</returns>
public byte[] ProcessRequestAudiotoWav(AudioClip requestAudioClip)
```

#### Convert16BitByteArrayToFloatAudioClipData()

This function converts 16-bit byte audio data into to an array of float data that can be used to create a Unity audioClip.

```csharp
/// <summary>
/// Converts a byte array representing 16-bit audio samples to a float array.
/// </summary>
/// <param name="source">Byte array containing 16-bit audio data</param>
/// <returns>Float array containing audio samples in the range [-1, 1]</returns>
float[] Convert16BitByteArrayToFloatAudioClipData(byte[] source)
```

#### ProcessStringAudioDataToAudioClip()

This function converts string audio data into to a Unity audioClip.

{% code overflow="wrap" %}
```csharp
/// <summary>
/// Converts string-encoded audio data to an AudioClip.
/// </summary>
/// <param name="audioData">String containing base64-encoded audio data</param>
/// <param name="stringSampleRate">String representing the sample rate of the audio</param>
/// <returns>AudioClip containing the decoded audio data</returns>
public AudioClip ProcessStringAudioDataToAudioClip(string audioData, string stringSampleRate)
```
{% endcode %}

#### ProcessByteAudioDataToAudioClip()

This function converts byte audio data into to a Unity audioClip.

{% code overflow="wrap" %}
```csharp
/// <summary>
/// Converts a byte array containing audio data into an AudioClip.
/// </summary>
/// <param name="byteAudio">Byte array containing the audio data</param>
/// <param name="stringSampleRate">String containing the sample rate of the audio</param>
/// <returns>AudioClip containing the decoded audio data</returns>
public AudioClip ProcessByteAudioDataToAudioClip(byte[] byteAudio, string stringSampleRate)
```
{% endcode %}

#### StartRecordAudio()

The function initializes the connection to the server and the stream with the configuration of the data and some headers to be sent the server. The script starts recording the audio using the default microphone. It then starts a coroutine that will listen to any responses from the server (`ReceiveResultFromServer()`). &#x20;

While the mic is recording, we get the data from the audioclip to which the Unity microphone class is writing and then asynchronously calls a function that will process the audio and send it to the server as a stream of audio data (`ProcessAudioChunk()`).&#x20;

Once the microphone stops recording (handled by the `StopRecordAudio()` function). The final audio data is sent for processing. After this we close the request stream to the server.&#x20;

{% code overflow="wrap" %}
```csharp
/// <summary>
/// Starts recording audio and sends it to the server for processing.
/// </summary>
/// <param name="client">gRPC service Client object</param>
/// <param name="isActionActive">Bool specifying whether we are expecting action responses</param>
/// <param name="recordingFrequency">Frequency of the audio being sent</param>
/// <param name="recordingLength">Length of the recording from the microphone</param>
/// <param name="characterID">Character ID obtained from the playground</param>
/// <param name="actionConfig">Object containing the action configuration</param>
public async Task StartRecordAudio(ConvaiService.ConvaiServiceClient client, bool isActionActive, int recordingFrequency, int recordingLength, string characterID, ActionConfig actionConfig)
```
{% endcode %}

#### StopRecordAudio()

Stops the microphone from recording audio.

```csharp
 /// <summary>
 /// Stops recording and processing the audio.
 /// </summary>
 public void StopRecordAudio()
```

#### ReceiveResultFromServer()

This function listens to the server for any results that it sends for the current query until the complete response is received from the server. This response is received in chunks. The chunks are classified into Audio Response or Action Response and then sent to the ConvaiNPC and ConvaiActionHandler respectively for processing.&#x20;

{% code overflow="wrap" %}
```csharp
/// <summary>
/// Periodically receives responses from the server and adds it to a static list in streaming NPC
/// </summary>
/// <param name="call">gRPC Streaming call connecting to the getResponse function</param>
async Task ReceiveResultFromServer(AsyncDuplexStreamingCall<GetResponseRequest, GetResponseResponse> call)
```
{% endcode %}

#### AddByteToArray()

A utility function that adds wav header to audioByteData to make it compatible with wav format.

{% code overflow="wrap" %}
```csharp
/// <summary>
/// Adds WAV header to the audio data
/// </summary>
/// <param name="audioByteArray">Byte array containing audio data</param>
/// <param name="sampleRate">Sample rate of the audio that needs to be processed</param>
/// <returns>Byte array with added WAV header</returns>
byte[] AddByteToArray(byte[] audioByteArray, string sampleRate)
```
{% endcode %}
