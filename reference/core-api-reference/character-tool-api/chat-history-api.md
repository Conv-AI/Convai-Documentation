---
description: >-
  All the relevant APIs needed to interact with Chat History of a session or
  character.
---

# Chat History API

## List Sessions for a Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/chatHistory/list`

List all the sessions for the Character. The API accepts a limit parameter which can be used to limit the number of sessions to fetch. If the value is set to "-1", then all sessions are returned.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name   | Type   | Description                  |
| ------ | ------ | ---------------------------- |
| charID | String | Id of your character.        |
| limit  | String | Number of sessions to return |

{% tabs %}
{% tab title="200: OK Returns List of sessions" %}
```json
[
    {
        "sessionID": "c1234567890aba1111222233334447862",
        "date": "25-09-2024",
        "time": "20:52:57",
        "is_added_to_memory": false
    },
    {
        "sessionID": "8c123456789011111222223333344455",
        "date": "25-09-2024",
        "time": "19:54:56",
        "is_added_to_memory": false
    }
]

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
import requests
import json

url = "https://api.convai.com/character/chatHistory/list"

headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "charID": "<Your-Character-Id>",
    "limit": "-1"
}

# Convert the payload to JSON
json_payload = json.dumps(payload)

response = requests.post(url, headers=headers, data=json_payload)

print(response.text)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl -X POST "https://api.convai.com/character/chatHistory/list" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{"charID": "<Your-Character-Id>", "limit": "-1"}'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## ChatHistory for a Session

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/chatHistory/details`

List all interactions for a given session-id. The output also contain a bool parameter which tell if the user input is a trigger or not. This will be set to true, if you have ever send a trigger while interacting with your character.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name      | Type   | Description                                                              |
| --------- | ------ | ------------------------------------------------------------------------ |
| charID    | String | Id of your character.                                                    |
| sessionID | String | SessionId of the character for which you want to fetch the interactions. |

{% tabs %}
{% tab title="200: OK Returns Session Interactions" %}
```json
[
    {
        "timestamp": "2024-09-25 19:54:59.124733",
        "interaction": [
            {
                "speaker": "User",
                "message": "Hi there"
            },
            {
                "speaker": "Character",
                "message": "Hi there, Welcome to the History Museum. We have the most ancient fossil ever discovered. Would be interesting in taking a tour?"
            }
         ],
        "is_trigger_input": false
    }
]
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
import requests
import json

url = "https://api.convai.com/character/chatHistory/details"

headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "charID": "<Your-Character-Id>",
    "sessionID": "<Your-Session-ID>"
}

# Convert the payload to JSON
json_payload = json.dumps(payload)

response = requests.post(url, headers=headers, data=json_payload)

print(response.text)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl -X POST "https://api.convai.com/character/chatHistory/list" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{"charID": "<Your-Character-Id>", "sessionID": "<Your-Session-ID>"}'
```
{% endcode %}
{% endtab %}
{% endtabs %}
