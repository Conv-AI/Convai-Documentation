---
description: >-
  All the relevant APIs needed to modify Core AI setting of your Convai
  Character.
---

# Core AI Settings API

{% hint style="danger" %}
This API is available only on the Professional Plan and above.
{% endhint %}

## Character Model Selection

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/update`

Update API can be used to change the LLM to be used for Character. Currently following models are supported.

### Realtime / Live Models

#### OpenAI

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>GPT Realtime 1.5 (beta)</td><td>gpt-realtime-1.5</td><td>false</td></tr><tr><td>GPT Realtime Mini (beta)</td><td>gpt-realtime-mini</td><td>false</td></tr></tbody></table>

#### Google

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Gemini 2.5 Flash Live (beta)</td><td>gemini-2.5-flash-live</td><td>false</td></tr><tr><td>Gemma 4 34B Fast (beta)</td><td>gemma-4-34b-fast</td><td>false</td></tr><tr><td>Gemma 4 26B A4B Fast (beta)</td><td>gemma-4-26b-a4b-fast</td><td>false</td></tr></tbody></table>

### Standard Models

#### OpenAI

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>GPT-5.4</td><td>gpt-5.4</td><td>false</td></tr><tr><td>GPT-5.x (latest)</td><td>gpt-5.x</td><td>true</td></tr><tr><td>GPT-OSS-120B (beta)</td><td>gpt-oss-120b</td><td>false</td></tr><tr><td>GPT-5.1 (beta)</td><td>gpt-5.1</td><td>false</td></tr><tr><td>GPT-4.1</td><td>gpt-4.1</td><td>false</td></tr><tr><td>GPT-5.4-nano</td><td>gpt-5.4-nano</td><td>false</td></tr><tr><td>GPT-5.x-nano (latest)</td><td>gpt-5.x-nano</td><td>true</td></tr><tr><td>GPT-5.4-mini</td><td>gpt-5.4-mini</td><td>false</td></tr><tr><td>GPT-5.x-mini (latest)</td><td>gpt-5.x-mini</td><td>true</td></tr><tr><td>GPT-4.1-mini</td><td>gpt-4.1-mini</td><td>false</td></tr><tr><td>GPT-5.3 Instant</td><td>gpt-5.3-instant</td><td>false</td></tr><tr><td>GPT-4o</td><td>gpt-4o</td><td>false</td></tr><tr><td>GPT-4.1-nano</td><td>gpt-4.1-nano</td><td>false</td></tr><tr><td>GPT-4o-mini</td><td>gpt-4o-mini</td><td>false</td></tr></tbody></table>

#### Anthropic

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Claude 4.5 Sonnet (beta)</td><td>claude-4-5-sonnet</td><td>false</td></tr><tr><td>Claude 4.5 Haiku (beta)</td><td>claude-4-5-haiku</td><td>false</td></tr><tr><td>Claude Sonnet (latest)</td><td>claude-sonnet</td><td>true</td></tr><tr><td>Claude Haiku (latest)</td><td>claude-haiku</td><td>true</td></tr></tbody></table>

#### Google

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Gemini 3.5 Flash</td><td>gemini-3.5-flash</td><td>false</td></tr><tr><td>Gemini Flash (latest)</td><td>gemini-flash</td><td>true</td></tr><tr><td>Gemini 3.1 Flash Lite</td><td>gemini-3.1-flash-lite</td><td>false</td></tr><tr><td>Gemini Flash Lite (latest)</td><td>gemini-flash-lite</td><td>true</td></tr><tr><td>Gemini 2.5 Flash</td><td>gemini-2.5-flash</td><td>false</td></tr><tr><td>Gemini 2.5 Flash Lite</td><td>gemini-2.5-flash-lite</td><td>false</td></tr></tbody></table>

#### Qwen

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Qwen3.6 27B (beta)</td><td>qwen3.6-27b</td><td>false</td></tr><tr><td>Qwen3.6 35B A3B (beta)</td><td>qwen3.6-35b-a3b</td><td>false</td></tr></tbody></table>

#### Llama

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Llama 4 Maverick (beta)</td><td>llama-4-maverick</td><td>false</td></tr><tr><td>Llama 4 Scout (beta)</td><td>llama-4-scout</td><td>false</td></tr><tr><td>Llama3 70B</td><td>llama3-70b</td><td>false</td></tr></tbody></table>

#### xAI

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Grok 4.3</td><td>grok-4.3</td><td>false</td></tr></tbody></table>

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
