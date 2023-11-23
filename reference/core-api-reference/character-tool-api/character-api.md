---
description: >-
  All the available APIs needed to create your own intelligent character with
  Convai.
---

# Character API

Access Convai endpoints for developing and interacting with an intelligent character, starting with some information like the character name, some background information, and a voice. Unveil the character to the end-user through your custom UI or through other services where Convai provides custom plugins/libraries, for them to have engaging conversations with your creation.

{% hint style="info" %}
**Missing Something?** In case you are missing something that is essential for your innovative application, please reach out to us through the Contact Page form on our page and we will positively get back to you for more discussion on the requirement.
{% endhint %}

## Create / Update Character

{% swagger method="post" summary="This endpoint is called to create a new character." baseUrl="https://api.convai.com/character" path="/create" %}
{% swagger-description %}
Users can either use the character creator tool to create their own characters or directly use this endpoint to dynamically create characters, by providing some basic information
{% endswagger-description %}

{% swagger-parameter in="header" name="CONVAI-API-KEY" required="true" %}
The unique api-key provided for every user.
{% endswagger-parameter %}

{% swagger-parameter in="body" name="charName" required="true" %}
Name of the new character being created.
{% endswagger-parameter %}

{% swagger-parameter in="body" name="voiceType" required="true" %}
The type of voice the character is expected to have.

\[Please refer to the list of available voices mentioned below]
{% endswagger-parameter %}

{% swagger-parameter in="body" name="backstory" required="true" %}
Basic background information of the character to start with.
{% endswagger-parameter %}

{% swagger-parameter in="body" name="actions" %}
A list of actions for the character to choose from, to be performed by the character based on the interactions with the user.
{% endswagger-parameter %}

{% swagger-response status="201: Created" description="A new character has bee created with the necessary details" %}
```json
{
    "charID": "<character id for new character>"
}
```
{% endswagger-response %}

{% swagger-response status="400: Bad Request" description="The registration of the new character has failed" %}
```json
{
    "INTERNAL_ERROR": "Error in creating the character. Check if all the input data is valid. Contact support for more info."
}
```
{% endswagger-response %}

{% swagger-response status="401" description="API Key validation has failed" %}
```json
{
    "API_ERROR": "Invalid API key provided." / "api_key not found."
}
```
{% endswagger-response %}
{% endswagger %}

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
}'e
```
{% endtab %}
{% endtabs %}

{% swagger method="post" path="/update" baseUrl="https://api.convai.com/character" summary="This endpoint is called to update the details of an existing character" %}
{% swagger-description %}
Users can update some of the existing information of a character that the user has created. They can pass only the new character information that needs to be updated, through the request. The rest of the information remains the same.
{% endswagger-description %}

{% swagger-parameter in="header" name="CONVAI-API-KEY" required="true" %}
The unique api-key provided for every user.
{% endswagger-parameter %}

{% swagger-parameter in="body" name="charID" required="true" %}
Character ID of the character to update for.
{% endswagger-parameter %}

{% swagger-parameter in="body" name="charName" required="false" %}
New name of the character
{% endswagger-parameter %}

{% swagger-parameter in="body" name="backstory" %}
Updated backstory
{% endswagger-parameter %}

{% swagger-parameter in="body" name="voiceType" %}
New voice name
{% endswagger-parameter %}

{% swagger-parameter in="body" name="action" %}
New list of actions for the character
{% endswagger-parameter %}

{% swagger-response status="200: OK" description="The details have been updated successfully" %}
```json
{
   "STATUS": "SUCCESS"
}
```
{% endswagger-response %}

{% swagger-response status="400: Bad Request" description="The update might be unsuccessful due to various reason " %}
```json
{
    "ERROR": "Could not fetch character details from all_characters table." / 
             "Could not update character backstory." / 
             "Could not update all_characters table."
}
```
{% endswagger-response %}

{% swagger-response status="401" description="API Key validation has failed" %}
```json
{
    "API_ERROR": "Invalid API key provided." / "api_key not found."
}
```
{% endswagger-response %}
{% endswagger %}

{% hint style="info" %}
For the list of supported voices please refer to the table in Text To Speech API
{% endhint %}

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

Get Details of Characters

{% swagger method="post" path="/get" baseUrl="https://api.convai.com/character" summary="This endpoint is called to fetch all the necessary details of a particular character." %}
{% swagger-description %}
Users can retrieve all the information about a particular character that they have created or that has been listed public.
{% endswagger-description %}

{% swagger-parameter in="header" name="CONVAI-API-KEY" required="true" %}
The unique api-key provided for every user.
{% endswagger-parameter %}

{% swagger-parameter in="body" name="charID" required="true" %}
Character ID of the character for which to fetch all the details.
{% endswagger-parameter %}

{% swagger-response status="200: OK" description="Returns all the information of the corresponding character" %}
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
{% endswagger-response %}

{% swagger-response status="400: Bad Request" description="Failed to fetch the information. Check if the character-id is valid" %}
```json
{
    "ERROR": "INTERNAL SERVER ERROR, one or more database calls failed!"
}
```
{% endswagger-response %}
{% endswagger %}

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

## Interact with a Character

{% swagger method="post" path="/getResponse" baseUrl="https://api.convai.com/character" summary="This endpoint is called to converse with the character" %}
{% swagger-description %}
Users can implement a chatbot session for the end-users to converse with their character. The users can maintain the context of a conversation by maintaining the session-id in the API requests made.

Please remember to go through the list of "Important Points to Remember" mentioned at the end. They contain some information on the constraints and requirements to execute a successful API call to this endpoint
{% endswagger-description %}

{% swagger-parameter in="header" name="CONVAI-API-KEY" required="true" %}
The unique api-key provided for every user.
{% endswagger-parameter %}

{% swagger-parameter in="body" name="userText" required="true" %}
The query of the user interacting with the charater
{% endswagger-parameter %}

{% swagger-parameter in="body" name="file" type="File" required="true" %}
The audio file containing the query of the user
{% endswagger-parameter %}

{% swagger-parameter in="body" name="charID" required="true" %}
The ID of the character, the user is interacting with
{% endswagger-parameter %}

{% swagger-parameter in="body" name="sessionID" required="true" %}
Used to identify a session of conversation to maintain the context.
{% endswagger-parameter %}

{% swagger-parameter in="body" name="voiceResponse" type="Boolean" required="true" %}
To generate an audio file for the response in the voice of the character
{% endswagger-parameter %}

{% swagger-parameter in="body" %}

{% endswagger-parameter %}

{% swagger-response status="200: OK" description="The character is able to generate a response to the user's query" %}
```json
{
    "charID": "<character id sent in the request body>",
    "text": "<response generated by the language model to the query>",
    "audio": null / "<base64 encoded audio>"
    "sample_rate": null / "<sample rate of the audio in Hz>"
    "sessionID": "<your session id. In case of a new session, it returns a newly generated value or returns the old one>"
}
```
{% endswagger-response %}

{% swagger-response status="404: Not Found" description="Response generation failed for the request" %}
```json
{
    "charID": "<character id sent in the request body>",
    "text": "process_failure, error: <error representation>"
}
```
{% endswagger-response %}

{% swagger-response status="400: Bad Request" description="In case of bad input" %}
```json
{
    "ERROR": "Expecting only one; either an audio file or user's query as a string"
}
```
{% endswagger-response %}
{% endswagger %}

{% hint style="warning" %}
Important Points to Remember:

* The API endpoint expects the request body to contain only one type of input (either text input, via **userText**, or audio input via file). Including both types of input or none will result in an error.
* We strictly adhere to OpenAI’s Content Policy for API usage and expect the user to respect the rules as well, to prevent the generation of toxic and inappropriate content.
* Please note that the body of the request should be **form-data**. This is to maintain consistency of format while uploading audio files.
* Sending -1 as the session ID value starts a new chat session. Use the returned session ID in subsequent getResponse requests to ensure conversation context is maintained.
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
