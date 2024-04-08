---
description: All the available APIs needed to generate transcript from audio files.
---

# Speech To Text API

## Speech to Text

## This endpoint is called for transcribing an audio file.

<mark style="color:green;">`POST`</mark> `https://api.convai.com/stt/`

The user can send the audio file they want to transcribe to this endpoint and get the transcript in the response.

This endpoint also has an option for enabling time stamps, which will provide the timestamp along with the transcript.

#### Headers

| Name                                             | Type   | Description           |
| ------------------------------------------------ | ------ | --------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | User's Convai API Key |

#### Request Body

| Name                                   | Type        | Description                                                                                                                  |
| -------------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------- |
| file<mark style="color:red;">\*</mark> |  Audio File | <p>The audio file that the user wants to transcribe.</p><p><strong>Accepted Formats: wav / mp3</strong></p>                  |
| enableTimestamps                       | Boolean     | <p>Set to True if the user wants time stamps along with the transcript else False.</p><p><strong>Default: False</strong></p> |

{% tabs %}
{% tab title="200: OK Request processed successfully." %}
{% tabs %}
{% tab title="With Timestamps" %}
```javascript
{ 
	"result" : "<the complete transcription of the audio file>",
	"details": [
		{
			"id": "<sub-trsancript order number>",
			"start-time" : "<starting time, accurate up to milliseconds>",
			"end-time" : "<ending time, accurate up to milliseconds>",
			"text": "<sub-transcript for the time interval>"
		},
		.
		.

```
{% endtab %}

{% tab title="Untitled" %}
```javascript
{ 
	"result" : "<the complete transcription of the audio file>"
}
```
{% endtab %}
{% endtabs %}
{% endtab %}

{% tab title="401: Unauthorized Convai API Key is incorrect." %}
```json
{
    "ERROR": "<Error related to API key>"
}
```
{% endtab %}

{% tab title="400: Bad Request Incomplete / Invalid data sent through the request." %}
```json
{
    "ERROR": "<The corresponding error caused by incorrect request data>"
}
```
{% endtab %}
{% endtabs %}

Here some ample codeto demonstrate the request format for th endpoint -->

{% tabs %}
{% tab title="Python" %}
```python
import requests

url = "https://api.convai.com/stt/"

payload={
	"enableTimestamps": "<True or False>"	# Dont need to set if False (default).
}
files=[
  ('file',('audio.wav',open('<path to audio file>','rb'),'audio/wav'))
]
headers = {
  'CONVAI-API-KEY': '<your api key>'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl --location --request POST 'https://api.convai.com/stt/' \
--header 'CONVAI-API-KEY: <your api key>' \
--form 'file=@"<path to your audio file>"' \
--form 'enableTimestamps="<True or False>"'
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
Please note currently the API only supports and format for audio files. Sending audio files of other formats such as aac, flac, etc will result in a rror.
{% endhint %}

{% hint style="info" %}
Note: The audio should have a bit depth of at least 16 bits or higher.
{% endhint %}

## Add Words

## Adding specific words to be focused upon during the Speech-To-Text processing

<mark style="color:green;">`POST`</mark> `https://api.convai.com/stt/add-words`

This API is called to add new words that the user wants to focus on during the Speech to Text processing. Users can use this endpoint to add uncommon words, that they expect in their audio files and want the Speech-to-Text system to correctly recognize them.

#### Headers

| Name                                             | Type   | Description           |
| ------------------------------------------------ | ------ | --------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | User's Convai API Key |

#### Request Body

| Name                                   | Type   | Description                      |
| -------------------------------------- | ------ | -------------------------------- |
| word<mark style="color:red;">\*</mark> | String | The word, the user wants to add. |

{% tabs %}
{% tab title="401: Unauthorized Convai API Key is incorrect." %}
```json
{
    "ERROR": "<Error related to API key>"
}
```
{% endtab %}

{% tab title="400: Bad Request Invalid / Incomplete data sent through request." %}
```json
{
    "ERROR": "<The corresponding error caused by incorrect request data>"
}
```
{% endtab %}

{% tab title="200: OK Word successfully added to the records." %}
```json
{
    "STATUS" : 0
}
```
{% endtab %}
{% endtabs %}



Here are some sample codes to demonstrate the request format for the endpoint -->

{% tabs %}
{% tab title="Python" %}
```python
import requests
import json

url = "https://api.convai.com/stt/add-words"

payload = json.dumps({
  "word": "<new word>"
})
headers = {
  'CONVAI-API-KEY': '<your api key>',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl --location --request POST 'https://api.convai.com/stt/add-words' \
--header 'CONVAI-API-KEY: <your api key>' \
--data-raw '{
    "word": "<new word>"
}'
```
{% endtab %}
{% endtabs %}
