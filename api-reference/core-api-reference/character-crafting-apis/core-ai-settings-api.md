---
description: >-
  All the relevant APIs needed to modify Core AI setting of your Convai
  Character.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/api-reference/core-api-reference/character-crafting-apis/core-ai-settings-api
---

# Core AI Settings API

{% hint style="danger" %}
This API is available only on the Professional Plan and above.
{% endhint %}

## Character Model Selection

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/update`

Update API can be used to change the LLM to be used for Character. Currently following models are supported.

### **OpenAI**

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Uncensored</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>GPT-4.1</td><td>gpt-4.1</td><td>false</td><td>true</td></tr><tr><td>GPT-4.1-mini</td><td>gpt-4.1-mini</td><td>false</td><td>false</td></tr><tr><td>GPT-4.1-nano</td><td>gpt-4.1-nano</td><td>false</td><td>false</td></tr><tr><td>GPT-4o</td><td>gpt-4o</td><td>false</td><td>true</td></tr><tr><td>GPT-4o-mini</td><td>gpt-4o-mini</td><td>false</td><td>false</td></tr></tbody></table>

### Anthropic

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Uncensored</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Claude-Opus-4.1</td><td>claude-opus-4.1</td><td>false</td><td>true</td></tr><tr><td>Claude-Opus-4</td><td>claude-opus-4</td><td>false</td><td>true</td></tr><tr><td>Claude-4-Sonnet</td><td>claude-4-sonnet</td><td>false</td><td>false</td></tr><tr><td>Claude-3-7-Sonnet</td><td>claude-3-7-sonnet</td><td>false</td><td>false</td></tr></tbody></table>

### **Google**

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Uncensored</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Gemini-2.5-Flash</td><td>gemini-2.5-flash</td><td>false</td><td>false</td></tr><tr><td>Gemini-2.5-Flash-Lite</td><td>gemini-2.5-flash-lite</td><td>false</td><td>false</td></tr><tr><td>Gemini-2.0-Flash</td><td>gemini-2.0-flash</td><td>false</td><td>false</td></tr><tr><td>Gemma-3n-e4b</td><td>gemma-3n-e4b</td><td>false</td><td>false</td></tr><tr><td>Gemma-3n-e2b</td><td>gemma-3n-e2b</td><td>false</td><td>false</td></tr></tbody></table>

### **Llama**

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Uncensored</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>LLama-4-Maverick</td><td>llama-4-maverick</td><td>false</td><td>true</td></tr><tr><td>LLama-4-Scout</td><td>llama-4-scout</td><td>false</td><td>false</td></tr><tr><td>LLama-3.3-70B</td><td>llama-3-70B</td><td>true</td><td>false</td></tr></tbody></table>

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
{% tab title="200: OK The model has been sucessfuly updated." %}
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
