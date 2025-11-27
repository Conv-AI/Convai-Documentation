---
description: >-
  This page explains how to interact with the standalone Text-to-Speech (TTS)
  API to generate audio from a given transcript, using a selected voice from the
  available voice list.
hidden: true
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/api-reference/core-api-reference/character-crafting-apis/text-to-speech-api
---

# Text to Speech API

{% hint style="danger" %}
This API is available only on the Enterprise Plan.
{% endhint %}

## Generate Audio from Text

<mark style="color:green;">`POST`</mark>  `https://api.convai.com/tts/`&#x20;

***

## **Headers**

| **CONVAI-API\_KEY**<mark style="color:red;">**\***</mark> | String | Your Convai API Key. |
| --------------------------------------------------------- | ------ | -------------------- |
| **Content-Type**<mark style="color:red;">**\***</mark>    | String | application/json     |

***

## Request Body

| Name                                             | Type   | Description                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **transcript**<mark style="color:red;">\*</mark> | String | The text to be converted into audio.                                                                                                                                                                                                                                                                                   |
| **voice**<mark style="color:red;">\*</mark>      | String | <p>Specifies the type of voice used for the audio response. This can be retrieved using the <a href="voice-list-api.md">Voice List API</a>, from the <code>voice_value</code> attribute of the desired voice.<br><br><strong>NOTE :</strong> Realtime voices are not supported in the standalone TTS API endpoint.</p> |
| filename                                         | String | The name of the audio file.                                                                                                                                                                                                                                                                                            |
| encoding                                         | String | <p>This is the format of the audio file. We currently support WAV and MP3 formats for STT (speech-to-text) audio. By default, it is set to WAV.<br><br><strong>NOTE :</strong> MP3 is not supported by all voices.</p>                                                                                                 |

***

## Response&#x20;

If the API call is successful, it returns the generated audio file as the response.

***

## Sample Code Snippet

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}
```python
import requests
import json

url = "https://api.convai.com/tts/"

payload = json.dumps({
  "transcript": "In the quiet of the morning, as the sky turned shades of pink and orange, she walked along the path lined with blooming flowers, feeling the cool breeze on her face. It was finally time for dinner.",
  "voice": "fable_OpenAi_c4d30a32-bcaf-4048-b7b0-0f2bb293205a",
  "encoding": "wav"
})

headers = {
  'CONVAI-API-KEY': '<Your Convai API Key>',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    with open('audio.wav','wb') as f:
      f.write(response.content)
else:
    print(response.text)
```
{% endcode %}
{% endtab %}
{% endtabs %}
