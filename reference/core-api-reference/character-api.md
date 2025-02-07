---
description: >-
  All the relevant APIs needed to create your own intelligent AI characters with
  Convai.
---

# Character Base API

Access Convai endpoints for developing and interacting with an intelligent character, starting with some basic information like the character 's name, background information, and a voice selection.\
\
Unveil the character to the end-user through your custom UI or through other services where Convai provides custom plugins/libraries, for users to have engaging conversations with your new characters.

{% hint style="danger" %}
This API is accessible only with the Professional plan and higher plans.
{% endhint %}

## Create Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/create`

Users can either use the character creator tool to create their own characters on the platform or use this API endpoint to dynamically create characters, by providing some basic information as defined below.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name                                        | Type   | Description                                                                                                                                                              |
| ------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| charName<mark style="color:red;">\*</mark>  | String | Name of the new character being created.                                                                                                                                 |
| voiceType<mark style="color:red;">\*</mark> | String | <p>The type of voice the character is expected to have.</p><p>[For the list of supported voices, please refer to the <a href="voice-list-api.md">Voice List API</a>]</p> |
| backstory<mark style="color:red;">\*</mark> | String | Basic background information of the character to start with.                                                                                                             |
| actions                                     | String | A list of actions for the character to choose from, to be performed by the character based on the interactions with the user.                                            |

{% tabs %}
{% tab title="201:  A new character has been created with the necessary details" %}
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

| Name                                     | Type           | Description                                                                                                                                                    |
| ---------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| charID<mark style="color:red;">\*</mark> | String         | Character ID of the character to update for.                                                                                                                   |
| charName                                 | String         | New name of the character                                                                                                                                      |
| backstory                                | String         | Updated backstory                                                                                                                                              |
| voiceType                                | String         | New voice type of the character \[For the list of supported voices, please refer to the [Voice List API](voice-list-api.md).]                                  |
| action                                   | String         | New list of actions for the character                                                                                                                          |
| languageCodes                            | List \<String> | The list of language codes, the character needs to support \[Please refer to the list of available languages in the [Language List API](language-list-api.md)] |

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
{% tab title="200: OK Character is successfully Cloned." %}
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

## Delete Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/delete`

Delete an existing character using this command. Please be careful hat this action is irreversible and once deleted, the character cannot be recovered.

#### Headers

| Name                                             | Type   | Description                                 |
| ------------------------------------------------ | ------ | ------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. |

#### Request Body

| Name                                     | Type   | Description                    |
| ---------------------------------------- | ------ | ------------------------------ |
| charID<mark style="color:red;">\*</mark> | String | ID of the character to Delete. |



{% tabs %}
{% tab title="200: OK Character successfully deleted" %}
```json
{
    "STATUS": "SUCCESS"
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

url = "https://api.convai.com/character/delete"


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
curl -X POST "https://api.convai.com/character/delete" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{"charID": "<Your-Character-Id>"}'
```
{% endtab %}
{% endtabs %}
