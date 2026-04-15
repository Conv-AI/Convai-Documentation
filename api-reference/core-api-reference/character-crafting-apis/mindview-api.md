---
description: >-
  Learn how to use the Backstory API to create and manage character backstories,
  adding depth and personality to your NPCs.
---

# Mindview API

{% hint style="danger" %}
This API is available only on the Professional Plan and above.
{% endhint %}

## Get Prompt For Mindview

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/generate-backstory`

Fetches prompt data for MindView in one of two ways:

1. **Session mode** (`session_id`): reads prompt data from stored interaction records.
2. **Character mode** (`character_id` only): generates static prompt data from current character configuration.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name          | Type    | Description                                                                       |
| ------------- | ------- | --------------------------------------------------------------------------------- |
| session\_id   | String  | Session identifier. If provided, API runs in session mode.                        |
| character\_id | String  | Character identifier. Used when `session_id` is not provided.                     |
| offset        | Integer | Optional. Used only with `session_id`. Default `-1` returns latest prompt record. |

> At least one of `session_id` or `character_id` is required.

{% tabs %}
{% tab title="200: OK (Session mode response)" %}
```json
{
  "prompt_id": "f2f8a75e-...",
  "prompt": "[{\"role\":\"system\",\"content\":\"...\"}]",
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "max_tokens": 512,
  "top_p": 1.0,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "stop": null,
  "session_id": "sess_123",
  "mindview": "{\"static_prompt\": {...}, \"dynamic_prompt\": {...}}"
}
```
{% endtab %}

{% tab title="200: OK (Character mode response)" %}
```json
{
  "mindview": "{\"static_prompt\": {...}, \"dynamic_prompt\": {...}}",
  "model": "gpt-4o-mini"
}
```
{% endtab %}

{% tab title="400: Bad Request" %}
```json
{
  "ERROR": "Either session_id or character_id is required",
  "Reference ID": "<transaction_id>"
}
```

```json
{
  "ERROR": "offset must be a valid integer",
  "Reference ID": "<transaction_id>"
}
```

```json
{
  "ERROR": "Offset is greater than the number of records",
  "Reference ID": "<transaction_id>"
}
```
{% endtab %}
{% endtabs %}

Here are some sample codes to demonstrate the request format for the endpoint -->

#### Session Mode (`session_id`)

{% tabs %}
{% tab title="Python" %}
```python
import json
import requests

url = "https://api.convai.com/character/chatHistory/get_prompt"

headers = {
    "CONVAI-API-KEY": "<Your-API-Key>",
    "Content-Type": "application/json"
}

payload = {
    "session_id": "<Your-Session-ID>",
    "offset": -1
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl -X POST "https://api.convai.com/character/chatHistory/get_prompt" \
  -H "CONVAI-API-KEY: <Your-API-Key>" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<Your-Session-ID>","offset":-1}'
```
{% endtab %}
{% endtabs %}

#### Character Mode (`character_id`)

{% tabs %}
{% tab title="Python" %}
```python
import json
import requests

url = "https://api.convai.com/character/chatHistory/get_prompt"

headers = {
    "CONVAI-API-KEY": "<Your-API-Key>",
    "Content-Type": "application/json"
}

payload = {
    "character_id": "<Your-Character-ID>"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl -X POST "https://api.convai.com/character/chatHistory/get_prompt" \
  -H "CONVAI-API-KEY: <Your-API-Key>" \
  -H "Content-Type: application/json" \
  -d '{"character_id":"<Your-Character-ID>"}'
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Implementation notes:

* If both `session_id` and `character_id` are provided, session mode is used.
* In current implementation, `mindview` and `prompt` fields are serialized JSON strings.
{% endhint %}
