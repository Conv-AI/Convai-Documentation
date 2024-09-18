---
description: >-
  All the relevant APIs needed to modify Core AI setting of your Convai
  Character.
---

# Core AI Setting API

## Character Model Selection

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/update`

Update API can be used to change the LLM to be used for Character. Currently following models are supported.

| Model                     | Model Code        | Uncensored |
| ------------------------- | ----------------- | ---------- |
| Claude-3-5-Sonnet         | claude-3-5-sonnet | No         |
| Gemini-1.5-pro            | gemini-1.5-pro    | No         |
| LLama3-70B                | llama-2-13b       | Yes        |
| LLama2-13B                | llama3-70b        | Yes        |
| GPT-4o                    | gpt-4o            | No         |
| GPT-4o-mini               | gpt-4o-mini       | No         |
| Fine Tuned - Mistral - 7B | uncensored-small  | Yes        |

When calling update API to update Model for your Character, please ensure to pass the `Model Code` corresponding to the `Model` from the table above.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name               | Type   | Description                                                               |
| ------------------ | ------ | ------------------------------------------------------------------------- |
| charID             | String | Id of your character.                                                     |
| model\_group\_name | String | Model Code of the Model to which you want to update. See the table above. |

{% tabs %}
{% tab title="200: OK The file is successfully uploaded" %}
```json
{"STATUS": "SUCCESS"}
```
{% endtab %}

{% tab title="401 API Key validation has failed" %}
```json
{
    "API_ERROR": "Invalid API key provided.
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

headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "charID": "<Your-Character-Id>",
    "model_group_name": "claude-3-5-sonnet"
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
curl -X POST "https://api.convai.com/character/update" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
           "charID": "<Your-Character-Id>",
           "model_group_name": "claude-3-5-sonnet"
         }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Temperature Setting

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/update`

When chatting with AI, the temperature setting is like adjusting how creative or predictable the responses will be. A lower temperature makes the AI stick closer to what it knows for sure (Less Hallucinations), while a higher temperature lets it get more imaginative and potentially surprising (better Role Play).

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name        | Type   | Description                                 |
| ----------- | ------ | ------------------------------------------- |
| charID      | String | Id of your character.                       |
| temperature | Float  | Temperature value. Must be between 0 and 1. |

{% tabs %}
{% tab title="200: OK Temperature Successfully Updated" %}
```json
{"STATUS": "SUCCESS"}
```
{% endtab %}

{% tab title="401 API Key validation has failed" %}
```json
{
    "API_ERROR": "Invalid API key provided.
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

headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "charID": "<Your-Character-Id>",
    "temperature": 0.42
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
curl -X POST "https://api.convai.com/character/update" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
           "charID": "<Your-Character-Id>",
           "temperature": 0.42
         }'
```
{% endcode %}
{% endtab %}
{% endtabs %}
