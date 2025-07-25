---
description: This page details on how you can interact with Character.
---

# Interaction API

{% hint style="danger" %}
This API is available only with the Professional Plan and above.
{% endhint %}

## Interacting with a Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/getResponse`

Users can implement a chatbot session for the end-users to converse with their character. The users can maintain the context of a conversation by maintaining the session-id in the API requests made.

Please remember to go through the list of "Important Points to Remember" mentioned at the end. They contain key information on the constraints and requirements to execute a successful API call to this endpoint.

#### Headers

| Name                                             | Type   | Description                                 |
| ------------------------------------------------ | ------ | ------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. |

#### Request Body

<table><thead><tr><th width="166">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>userText<mark style="color:red;">*</mark></td><td>String</td><td>The query or input of the user interacting with the charater.</td></tr><tr><td>charID<mark style="color:red;">*</mark></td><td>String</td><td>The ID of the character that the user is interacting with.</td></tr><tr><td>sessionID<mark style="color:red;">*</mark></td><td>String</td><td>Used to identify a session of conversation to maintain the context.</td></tr><tr><td>voiceResponse<mark style="color:red;">*</mark></td><td>Boolean</td><td>To generate an audio file for the response in the voice of the character.</td></tr><tr><td>file<mark style="color:red;">*</mark></td><td>File</td><td>The audio file containing the user's query. Must be in WAV format and mono channel.</td></tr><tr><td>sample_rate</td><td>String</td><td>Sample rate of the audio file being sent.</td></tr></tbody></table>

{% tabs %}
{% tab title="200: OK The character is able to generate a response to the user's query" %}
```json
{
    "charID": "<character id sent in the request body>",
    "text": "<response generated by the language model to the query>",
    "audio": null / "<base64 encoded audio>"
    "sample_rate": null / "<sample rate of the audio in Hz>"
    "sessionID": "<your session id. In case of a new session, it returns a newly generated value or returns the old one>"
}
```
{% endtab %}

{% tab title="404: Not Found Response generation failed for the request" %}
```json
{
    "charID": "<character id sent in the request body>",
    "text": "process_failure, error: <error representation>"
}
```
{% endtab %}

{% tab title="400: Bad Request In case of bad input" %}
```json
{
    "ERROR": "Expecting only one; either an audio file or user's query as a string"
}
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
Important Points to Remember:

* The API endpoint expects the request body to contain only one type of input (either text input, via **userText**, or audio input via file). Including **both types of input or none will result in an error.**
* We strictly adhere to OpenAI’s Content Policy for API usage and expect the user to respect the rules as well, to prevent the generation of toxic and inappropriate content. Repeated violations will result in the API key being blacklisted.
* Please note that the body of the request should be **form-data**. This is to maintain consistency of format while uploading audio files.
* Sending -1 as the session ID value **starts a new chat session**. Use the returned session ID in subsequent getResponse requests to ensure conversation context is maintained.
* While sending an audio file, make sure that it should have a **bit depth** of at least **16 bits or higher**.
{% endhint %}

Here are some sample codes to demonstrate the request format for the endpoint -->

Request with **text only:**

{% tabs %}
{% tab title="Python" %}
```python
import requests
import json
import base64

url = "https://api.convai.com/character/getResponse"

payload={
    'userText': 'What is your name ?',
    'charID': '<your character id>',
    'sessionID': '-1',
    'voiceResponse': 'True'
}

headers = {
  'CONVAI-API-KEY': '<your api key>'
}

response = requests.request("POST", url, headers=headers, data=payload)

data = response.json()

character_response = data["text"]

decode_string = base64.b64decode(data["audio"])

with open('audioResponse.wav','wb') as f:
  f.write(decode_string)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl --location --request POST 'https://api.convai.com/character/getResponse' \
--header 'CONVAI-API-KEY: <your api key>' \
--form 'userText="What is your name ?"' \
--form 'charID="<your character id>"' \
--form 'sessionID="-1"' \
--form 'voiceResponse="True"'
```
{% endtab %}
{% endtabs %}

Request with **audio only:**

{% tabs %}
{% tab title="Python" %}
```python
import requests
import json
import base64

url = "https://api.convai.com/character/getResponse"

payload={
		'charID': '<your character id>',
		'sessionID': '-1',
		'responseLevel': '5',
		'voiceResponse': 'True'}
files=[
  ('file',('audio.wav',open('<path to the audio file audio.wav>','rb'),'audio/wav'))
]
headers = {
  'CONVAI-API-KEY': '<your api key>'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)
data = response.json()

character_response = data["text"]
sessionID = data["sessionID"]

print("Session ID: ", sessionID)
print("Response: ", character_response)

decode_string = base64.b64decode(data["audio"])

with open('audioResponse.wav','wb') as f:
  f.write(decode_string)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl --location --request POST 'https://api.convai.com/character/getResponse' \
--header 'CONVAI-API-KEY: <your api key>' \
--form 'charID="<your character id>"' \
--form 'sessionID="-1"' \
--form 'voiceResponse="True"' \
--form 'file=@"<path to the audio file audio.wav>"'
```
{% endtab %}
{% endtabs %}

## Generate Conversation Options

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/generate-starter-conversation`

Generate Starter Conversation API is implemented as Server Sent Event (SSE).  It uses Character backstory and current chat history to generate next set of possible follow-ups with Character.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name      | Type   | Description                                                                                                           |
| --------- | ------ | --------------------------------------------------------------------------------------------------------------------- |
| charId    | String | Id of the character for which to generate the conversation options.                                                   |
| sessionId | String | Session Id for which to generate next round of conversation. Set it to "-1" to generate opening conversation options. |



{% tabs %}
{% tab title="200: OK Returns multiple SSE events." %}
```json
# Output Format:
# The response will be streamed as Server-Sent Events (SSE).
# Each event will have a 'data' field containing a string which is a single chat suggestion.
# Example of a single event:

data: I'm curious about your most challenging match ever.

# Multiple events will be received, each containing a single chat suggestion.
```
{% endtab %}

{% tab title="401 API Key validation has failed" %}
```json
{
    "ERROR": "Invalid API key provided."
}
```
{% endtab %}
{% endtabs %}

Here are some sample codes to demonstrate the request format for the endpoint -->

{% tabs %}
{% tab title="Python" %}
{% code overflow="wrap" %}
```python
import json
import requests

url = "https://api.convai.com/character/generate-starter-conversation"

headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
}

form_data = { 
    'charId': '<Your-Character-ID>',
    'sessionId': '<Your-Session-ID>'
}

response = requests.post(url, headers=headers, data=form_data)

print(response.text)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl -X POST "https://api.convai.com/character/generate-starter-conversation" \
-H "CONVAI-API-KEY: <Your-API-Key>" \
-d "charId=<Your-Character-ID>" \
-d "sessionId=<Your-Session-ID>"
```
{% endcode %}
{% endtab %}
{% endtabs %}
