---
description: >-
  All the relevant APIs needed to create your own intelligent AI characters with
  Convai.
---

# Character API

Access Convai endpoints for developing and interacting with an intelligent character, starting with some basic information like the character 's name, background information, and a voice selection.\
\
Unveil the character to the end-user through your custom UI or through other services where Convai provides custom plugins/libraries, for users to have engaging conversations with your new characters.

{% hint style="info" %}
**Missing Something?** In case you are missing something that is essential for your application, please reach out to us through the **support@convai.com** email and we'll get to your inquiry shortly!
{% endhint %}

## Create Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/create`

Users can either use the character creator tool to create their own characters on the platform or use this API endpoint to dynamically create characters, by providing some basic information as defined below.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name                                        | Type   | Description                                                                                                                                                                                          |
| ------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| charName<mark style="color:red;">\*</mark>  | String | Name of the new character being created.                                                                                                                                                             |
| voiceType<mark style="color:red;">\*</mark> | String | <p>The type of voice the character is expected to have.</p><p>[Please refer to the list of available voices in the <a href="../standalone-voice-api/text-to-speech-api/">Text to Speech API</a>]</p> |
| backstory<mark style="color:red;">\*</mark> | String | Basic background information of the character to start with.                                                                                                                                         |
| actions                                     | String | A list of actions for the character to choose from, to be performed by the character based on the interactions with the user.                                                                        |

{% tabs %}
{% tab title="201: Created A new character has bee created with the necessary details" %}
```json
{
    "charID": "<character id for new character>"
}
```
{% endtab %}

{% tab title="400: Bad Request The registration of the new character has failed" %}
```json
{
    "INTERNAL_ERROR": "Error in creating the character. Check if all the input data is valid. Contact support for more info."
}
```
{% endtab %}

{% tab title="401 API Key validation has failed" %}
```json
{
    "API_ERROR": "Invalid API key provided." / "api_key not found."
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

url = "https://api.convai.com/character/create"

payload = json.dumps({
  "charName": "Raymond",
  "voiceType": "MALE",
  "backstory": "Raymond Reddington is a main character in the NBC series The Blacklist. Reddington is a criminal mastermind, making it to #4 and later to #1 on the FBI's Ten Most Wanted Fugitives, who suddenly turns himself in after 20+ years of evading the FBI."
})
headers = {
  'CONVAI-API-KEY': '<your api key>',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl --location --request POST 'https://api.convai.com/character/create' \
--header 'CONVAI-API-KEY: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "charName": "Raymond",
    "voiceType": "MALE",
    "backstory": "Raymond Reddington is a main character in the NBC series The Blacklist. Reddington is a criminal mastermind, making it to #4 and later to #1 on the FBI'\''s Ten Most Wanted Fugitives, who suddenly turns himself in after 20+ years of evading the FBI."
}'
```
{% endtab %}
{% endtabs %}

## Update Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/update`

Users can update some of the existing details of a character that has been previously created. Users need to only pass any new character information that needs to be updated. The rest of the character information will not be changed.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name                                     | Type   | Description                                                                                                                                              |
| ---------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| charID<mark style="color:red;">\*</mark> | String | Character ID of the character to update for.                                                                                                             |
| charName                                 | String | New name of the character                                                                                                                                |
| backstory                                | String | Updated backstory                                                                                                                                        |
| voiceType                                | String | New voice type of the character \[Please refer to the list of available voices in the [Text to Speech API](../standalone-voice-api/text-to-speech-api/)] |
| action                                   | String | New list of actions for the character                                                                                                                    |

{% tabs %}
{% tab title="200: OK The details have been updated successfully" %}
```json
{
   "STATUS": "SUCCESS"
}
```
{% endtab %}

{% tab title="400: Bad Request The update might be unsuccessful due to various reason " %}
```json
{
    "ERROR": "Could not fetch character details from all_characters table." / 
             "Could not update character backstory." / 
             "Could not update all_characters table."
}
```
{% endtab %}

{% tab title="401 API Key validation has failed" %}
```json
{
    "API_ERROR": "Invalid API key provided." / "api_key not found."
}
```
{% endtab %}
{% endtabs %}

Here are some sample codes to demonstrate the request format for the endpoint -->

{% tabs %}
{% tab title="Python" %}
{% code overflow="wrap" %}
```python
import requests
import json

url = "https://api.convai.com/character/update"

payload = json.dumps({
  "charID": "<character ID>",
  "backstory": "Raymond Reddington is a highly intelligent, highly driven individual with developed sociopathic tendencies. This appears to be the product of PTSD (post-traumatic stress disorder) as there are no signs that he was born this way. Sly, manipulative, and charming, Red is always three steps ahead of everyone else, and is determined to keep himself a mystery. As he puts it, “I’m a criminal. Criminals are notorious liars. Everything about me is a lie.” That’s probably true, actually, but who knows for sure. He dislikes rude people, which is something that Agent Ressler pointed out after Red let a notorious drug dealer get away with false identification. Ressler mentioned that Red wouldn’t let the drug dealer get away because he was rude and Red doesn’t like rude people. Red responded with, “He is on my jet.”",
  "voiceType": "US MALE 1",
  "charName": "Raymond Reddington"
})
headers = {
  'CONVAI-API-KEY': '<your api key>',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl --location --request POST 'https://api.convai.com/character/update' \
--header 'CONVAI-API-KEY: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "charID": "<character ID>",
    "backstory": "Raymond Reddington is a highly intelligent, highly driven individual with developed sociopathic tendencies. This appears to be the product of PTSD (post traumatic stress disorder) as there are no signs that he was born this way. Sly, manipulative, and charming, Red is always three steps ahead of everyone else, and is determined to keep himself a mystery. As he puts it, “I’m a criminal. Criminals are notorious liars. Everything about me is a lie.” That’s probably true, actually, but who knows for sure. He dislikes rude people, which is something that Agent Ressler pointed out after Red let a notorious drug dealer get away with false identification. Ressler mentioned that Red wouldn’t let the drug dealer get away because he was rude and Red doesn’t like rude people. Red responded with, “He is on my jet.”",
    "voiceType": "US MALE 1",
    "charName": "Raymond Reddington"
}'\
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Get Details

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/get`

Users can retrieve all the information about a particular character that they have created or that has been listed as public.

#### Headers

| Name                                             | Type   | Description                                 |
| ------------------------------------------------ | ------ | ------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. |

#### Request Body

| Name                                     | Type   | Description                                                       |
| ---------------------------------------- | ------ | ----------------------------------------------------------------- |
| charID<mark style="color:red;">\*</mark> | String | Character ID of the character for which to fetch all the details. |

{% tabs %}
{% tab title="200: OK Returns all the information of the corresponding character" %}
```json
{
    "character_name": "<name of the character>",
    "user_id": "<the id of the user who created it>",
    "character_id": "<id of the character>",
    "voice_type": "<voice type set for the character>",
    "timestamp": "<when the character was created>",
    "backstory": "<backstory of the character>"
}
```
{% endtab %}

{% tab title="400: Bad Request Failed to fetch the information. Check if the character-id is valid" %}
```json
{
    "ERROR": "INTERNAL SERVER ERROR, one or more database calls failed!"
}
```
{% endtab %}
{% endtabs %}

Here are some sample codes to demonstrate the request format for the endpoint -->

Search by **charID:**

{% tabs %}
{% tab title="Python" %}
```python
import requests
import json

url = "https://api.convai.com/character/get"

payload = json.dumps({
  "charID": "<id of the character>"
})
headers = {
  'CONVAI-API-KEY': '<your api key>',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl --location --request POST 'https://api.convai.com/character/get' \
--header 'CONVAI-API-KEY: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "charID": "<the id of the character>"
}'
```
{% endtab %}
{% endtabs %}

Search by **charName:**

{% tabs %}
{% tab title="Python" %}
```python
import requests
import json

url = "https://api.convai.com/character/get"

payload = json.dumps({
  "charName": "name of the character"
})
headers = {
  'CONVAI-API-KEY': '<your api key>',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl --location --request POST 'https://api.convai.com/character/get' \
--header 'CONVAI-API-KEY: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "charName": "<the name of the character>"
}'
```
{% endtab %}
{% endtabs %}

## Clone Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/user/clone_character`

Users can clone their character using this API.

#### Headers

| Name                                             | Type   | Description                                 |
| ------------------------------------------------ | ------ | ------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. |

#### Request Body

| Name                                     | Type   | Description                                                         |
| ---------------------------------------- | ------ | ------------------------------------------------------------------- |
| charID<mark style="color:red;">\*</mark> | String | ID of the character to Clone.                                       |
| KB                                       | Bool   | True, if KB should be cloned as well. Else False. Default is False. |



{% tabs %}
{% tab title="200: OK Returns all the information of the corresponding character" %}
```json
{
    "charID": "<id of the newly created cloned character>"
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

url = "https://api.convai.com/user/clone_character"


headers = { 
  'CONVAI-API-KEY': '<Your-API-Key>',
  'Content-Type': 'application/json'
}

# Create a dictionary for the form data
payload = { 
    'charID': '<Your-Character-Id>'
}


# Convert the payload to JSON
json_payload = json.dumps(payload)

response = requests.post(url, headers=headers, data=json_payload)

print(response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl -X POST "https://api.convai.com/user/clone_character" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{"charID": "<Your-Character-Id>"}'
```
{% endtab %}
{% endtabs %}

## Interacting with a Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/getResponse`

Users can implement a chatbot session for the end-users to converse with their character. The users can maintain the context of a conversation by maintaining the session-id in the API requests made.

Please remember to go through the list of "Important Points to Remember" mentioned at the end. They contain key information on the constraints and requirements to execute a successful API call to this endpoint.

#### Headers

| Name                                             | Type   | Description                                 |
| ------------------------------------------------ | ------ | ------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. |

#### Request Body

| Name                                            | Type    | Description                                                               |
| ----------------------------------------------- | ------- | ------------------------------------------------------------------------- |
| userText<mark style="color:red;">\*</mark>      | String  | The query or input of the user interacting with the charater.             |
| charID<mark style="color:red;">\*</mark>        | String  | The ID of the character that the user is interacting with.                |
| sessionID<mark style="color:red;">\*</mark>     | String  | Used to identify a session of conversation to maintain the context.       |
| voiceResponse<mark style="color:red;">\*</mark> | Boolean | To generate an audio file for the response in the voice of the character. |
| audio<mark style="color:red;">\*</mark>         | File    | The audio file containing the query of the user, in base64 format.        |
| sample\_rate                                    | String  | Sample rate of the audio file being sent.                                 |

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

## Update Character Details

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/update`

Users can different properties of a Character like Backstory, Voice and Actions using an Update API.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name                                     | Type   | Description                                                                                                                                              |
| ---------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| charID<mark style="color:red;">\*</mark> | String | Character ID of the character to update for.                                                                                                             |
| charName                                 | String | New name of the character                                                                                                                                |
| backstory                                | String | Updated backstory                                                                                                                                        |
| voiceType                                | String | New voice type of the character \[Please refer to the list of available voices in the [Text to Speech API](../standalone-voice-api/text-to-speech-api/)] |
| action                                   | String | New list of actions for the character                                                                                                                    |

{% tabs %}
{% tab title="200: OK The details have been updated successfully" %}
```json
{
   "STATUS": "SUCCESS"
}
```
{% endtab %}

{% tab title="400: Bad Request The update might be unsuccessful due to various reason " %}
```json
{
    "ERROR": "Could not fetch character details from all_characters table." / 
             "Could not update character backstory." / 
             "Could not update all_characters table."
}
```
{% endtab %}

{% tab title="401 API Key validation has failed" %}
```json
{
    "API_ERROR": "Invalid API key provided." / "api_key not found."
}
```
{% endtab %}
{% endtabs %}

Here are some sample codes to demonstrate the request format for the endpoint -->

{% tabs %}
{% tab title="Python" %}
{% code overflow="wrap" %}
```python
import requests
import json

url = "https://api.convai.com/character/update"

payload = json.dumps({
  "charID": "<character ID>",
  "backstory": "Raymond Reddington is a highly intelligent, highly driven individual with developed sociopathic tendencies. This appears to be the product of PTSD (post-traumatic stress disorder) as there are no signs that he was born this way. Sly, manipulative, and charming, Red is always three steps ahead of everyone else, and is determined to keep himself a mystery. As he puts it, “I’m a criminal. Criminals are notorious liars. Everything about me is a lie.” That’s probably true, actually, but who knows for sure. He dislikes rude people, which is something that Agent Ressler pointed out after Red let a notorious drug dealer get away with false identification. Ressler mentioned that Red wouldn’t let the drug dealer get away because he was rude and Red doesn’t like rude people. Red responded with, “He is on my jet.”",
  "voiceType": "US MALE 1",
  "charName": "Raymond Reddington"
})
headers = {
  'CONVAI-API-KEY': '<your api key>',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl --location --request POST 'https://api.convai.com/character/update' \
--header 'CONVAI-API-KEY: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "charID": "<character ID>",
    "backstory": "Raymond Reddington is a highly intelligent, highly driven individual with developed sociopathic tendencies. This appears to be the product of PTSD (post traumatic stress disorder) as there are no signs that he was born this way. Sly, manipulative, and charming, Red is always three steps ahead of everyone else, and is determined to keep himself a mystery. As he puts it, “I’m a criminal. Criminals are notorious liars. Everything about me is a lie.” That’s probably true, actually, but who knows for sure. He dislikes rude people, which is something that Agent Ressler pointed out after Red let a notorious drug dealer get away with false identification. Ressler mentioned that Red wouldn’t let the drug dealer get away because he was rude and Red doesn’t like rude people. Red responded with, “He is on my jet.”",
    "voiceType": "US MALE 1",
    "charName": "Raymond Reddington"
}'\
```
{% endcode %}
{% endtab %}
{% endtabs %}
