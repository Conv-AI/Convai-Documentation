---
description: >-
  Create, list, link, and delete External API functions so your characters can
  call custom Python code during conversations.
---

# External API

{% hint style="danger" %}
This API is available only on the Professional Plan and above.
{% endhint %}

External API functions are small Python handlers your character can call as tools during a conversation. Create a function once, link it to one or more characters, and the model decides when to run it based on the function name and description.

Typical flow:

1. Create a function with `/functions/create/`
2. Link it to a character with `/character/update` (`status: "active"`)
3. List functions (optionally filtered by character) with `/functions/list/`
4. Unlink it from a character with `/character/update` (`status: "inactive"`), or delete it entirely with `/functions/delete/`

For the Playground UI walkthrough and example handlers (weather, sports scores, Jira), see [External API](../../../convai-playground/character-customization/external-api.md).

Limits that apply here and in the Playground — supported models, Python 3.11 runtime, `requests`-only third-party packages, `handle_event`, input schema, and the 128-function cap — live on [External API limitations](../../../convai-playground/character-customization/external-api-limitations.md).

## Create a function

<mark style="color:green;">`POST`</mark> `https://api.convai.com/functions/create/`

Creates a new External API function on your account. The function is not attached to any character until you link it.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |
| Content-Type<mark style="color:red;">\*</mark>   | String | Must be `application/json`                                                                                 |

#### Request body

| Name                                                      | Type   | Description                                                                                          |
| --------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------- |
| name<mark style="color:red;">\*</mark>                    | String | Display name of the function. Prefer a clear verb phrase the model can match (for example `Get Weather`). |
| description<mark style="color:red;">\*</mark>             | String | When the character should call this function. Used by the model for tool selection.                  |
| language<mark style="color:red;">\*</mark>                | String | Implementation language. Only `python` is supported.                                                 |
| source\_code<mark style="color:red;">\*</mark>            | String | Full Python 3.11 source, including `handle_event`. Max 400 lines. Stdlib + `requests` only. See [External API limitations](../../../convai-playground/character-customization/external-api-limitations.md#runtime). |
| input\_description<mark style="color:red;">\*</mark>      | String | JSON **string** describing parameters. Must match the schema in [External API limitations](../../../convai-playground/character-customization/external-api-limitations.md#input-description). |

#### Example payload

```json
{
  "name": "Get Weather",
  "description": "Fetches current weather for a given city",
  "language": "python",
  "input_description": "{\"parameters\":{\"city\":{\"type\":\"string\",\"description\":\"Name of the city to get weather for\"}},\"required\":[\"city\"]}",
  "source_code": "import requests\n\nAPI_KEY = \"<openweather-api-key>\"\n\ndef handle_event(data):\n    city = data.get(\"city\")\n    url = f\"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}\"\n    response = requests.get(url)\n    weather_data = response.json()\n    return {\"weather\": weather_data[\"weather\"][0][\"description\"]}\n"
}
```

{% tabs %}
{% tab title="201: Created" %}
```json
{
  "transactionID": "<uuid>",
  "function": {
    "function_id": "<function uuid>",
    "name": "Get Weather",
    "description": "Fetches current weather for a given city",
    "language": "python",
    "source_code": "import requests\n...",
    "base64_source_code": "<base64 encoded source>",
    "input_description": "{\"parameters\":{...},\"required\":[\"city\"]}",
    "created_at": "2026-03-18T12:34:56"
  }
}
```
{% endtab %}

{% tab title="400: Bad Request" %}
```json
{
  "ERROR": "Missing required field: name",
  "Reference ID": "<uuid>"
}
```

Other common 400 messages:

* `Field input_description must be a valid json string`
* `Language pythonx not supported`
* Schema errors from an invalid `input_description`
* Source code validation failures (empty, over 400 lines, or blocked as malicious)
{% endtab %}

{% tab title="401 Unauthorized" %}
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

url = "https://api.convai.com/functions/create/"

input_description = {
    "parameters": {
        "city": {
            "type": "string",
            "description": "Name of the city to get weather for"
        }
    },
    "required": ["city"]
}

source_code = """
import requests

API_KEY = "<openweather-api-key>"

def handle_event(data):
    city = data.get("city")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    weather_data = response.json()
    return {"weather": weather_data["weather"][0]["description"]}
""".strip()

payload = json.dumps({
    "name": "Get Weather",
    "description": "Fetches current weather for a given city",
    "language": "python",
    "input_description": json.dumps(input_description),
    "source_code": source_code
})

headers = {
    "CONVAI-API-KEY": "<your api key>",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl --location --request POST 'https://api.convai.com/functions/create/' \
--header 'CONVAI-API-KEY: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "Get Weather",
  "description": "Fetches current weather for a given city",
  "language": "python",
  "input_description": "{\"parameters\":{\"city\":{\"type\":\"string\",\"description\":\"Name of the city to get weather for\"}},\"required\":[\"city\"]}",
  "source_code": "import requests\n\nAPI_KEY = \"<openweather-api-key>\"\n\ndef handle_event(data):\n    city = data.get(\"city\")\n    url = f\"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}\"\n    response = requests.get(url)\n    weather_data = response.json()\n    return {\"weather\": weather_data[\"weather\"][0][\"description\"]}\n"
}'
```
{% endcode %}
{% endtab %}
{% endtabs %}

***

## List functions

<mark style="color:green;">`POST`</mark> `https://api.convai.com/functions/list/`

Returns the External API functions on your account. Pass `character_id` to include each function's link status for that character (`active` or `inactive`).

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request body

All fields are optional. An empty body lists every function on the account.

| Name          | Type    | Description                                                                                         |
| ------------- | ------- | --------------------------------------------------------------------------------------------------- |
| character\_id | String  | If set, each function includes `status` relative to this character (`active` / `inactive`).         |
| per\_page     | Integer | Page size. Defaults to `-1` (return all). When set to a positive value, pagination fields are added. |
| page          | Integer | Page number, starting at `1`. Used only when `per_page` is not `-1`. Default `1`.                   |

#### Example payload

```json
{
  "character_id": "<character uuid>",
  "per_page": 20,
  "page": 1
}
```

{% tabs %}
{% tab title="200: OK" %}
```json
{
  "transactionID": "<uuid>",
  "functions": [
    {
      "function_id": "<function uuid>",
      "name": "Get Weather",
      "description": "Fetches current weather for a given city",
      "language": "python",
      "created_at": "2026-03-18T12:34:56",
      "status": "active"
    }
  ],
  "total_pages": 1,
  "per_page": 20,
  "page": 1,
  "total": 1
}
```

`total_pages`, `per_page`, `page`, and `total` are only present when `per_page` is a positive integer.
{% endtab %}

{% tab title="400: Bad Request" %}
```json
{
  "ERROR": "Failed to get functions with response: ...",
  "Reference ID": "<uuid>"
}
```
{% endtab %}

{% tab title="401 Unauthorized" %}
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

url = "https://api.convai.com/functions/list/"

payload = json.dumps({
    "character_id": "<character uuid>",
    "per_page": 20,
    "page": 1
})
headers = {
    "CONVAI-API-KEY": "<your api key>",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl --location --request POST 'https://api.convai.com/functions/list/' \
--header 'CONVAI-API-KEY: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "character_id": "<character uuid>",
  "per_page": 20,
  "page": 1
}'
```
{% endcode %}
{% endtab %}
{% endtabs %}

***

## Link functions to a character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/update`

Attach one or more External API functions to a character through the existing [Character Base API](character-api.md) update endpoint. Once linked (`status: "active"`), the model can call those functions during conversation.

A character can have at most **128** active functions. You can link several functions in one request, and you can mix link and [unlink](#unlink-functions-from-a-character) entries together.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |
| Content-Type                                     | String | `application/json`                                                                                         |

#### Request body

| Name                                     | Type   | Description                                                                                          |
| ---------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------- |
| charID<mark style="color:red;">\*</mark> | String | Character to update.                                                                                 |
| functions                                | Array  | List of function configs. Each item needs `id` (function UUID) and `status` set to `"active"`.      |

#### Example payload

```json
{
  "charID": "<character uuid>",
  "functions": [
    {
      "id": "<function uuid>",
      "status": "active"
    }
  ]
}
```

{% tabs %}
{% tab title="200: OK" %}
```json
{
  "STATUS": "SUCCESS"
}
```
{% endtab %}

{% tab title="400: Bad Request" %}
```json
{
  "ERROR": "Function limit exceeded. A maximum of 128 functions can be connected to a character.",
  "Reference ID": "<uuid>"
}
```

Also returned for invalid configs, for example:

* `Functions must be a list of configurations`
* `Missing required fields in function configuration: id`
* `Function status must be one of: active, inactive`
* `Duplicate function ID found: <id>`
{% endtab %}

{% tab title="401 Unauthorized" %}
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

url = "https://api.convai.com/character/update"

payload = json.dumps({
    "charID": "<character uuid>",
    "functions": [
        {"id": "<function uuid>", "status": "active"}
    ]
})
headers = {
    "CONVAI-API-KEY": "<your api key>",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=payload)
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
  "charID": "<character uuid>",
  "functions": [
    {"id": "<function uuid>", "status": "active"}
  ]
}'
```
{% endcode %}
{% endtab %}
{% endtabs %}

After linking, confirm with `/functions/list/` and `character_id` set — linked functions show `"status": "active"`.

***

## Unlink functions from a character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/update`

Disconnect a function from a character without deleting it from your account. Same endpoint as linking; set `status` to `"inactive"`.

After unlinking, the character can no longer call that function. The function stays available to re-link later, or to attach to other characters.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |
| Content-Type                                     | String | `application/json`                                                                                         |

#### Request body

| Name                                     | Type   | Description                                                                                            |
| ---------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------ |
| charID<mark style="color:red;">\*</mark> | String | Character to update.                                                                                   |
| functions                                | Array  | List of function configs. Each item needs `id` (function UUID) and `status` set to `"inactive"`.      |

#### Example payload

```json
{
  "charID": "<character uuid>",
  "functions": [
    {
      "id": "<function uuid>",
      "status": "inactive"
    }
  ]
}
```

{% tabs %}
{% tab title="200: OK" %}
```json
{
  "STATUS": "SUCCESS"
}
```
{% endtab %}

{% tab title="400: Bad Request" %}
```json
{
  "ERROR": "Missing required fields in function configuration: status",
  "Reference ID": "<uuid>"
}
```
{% endtab %}

{% tab title="401 Unauthorized" %}
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

url = "https://api.convai.com/character/update"

payload = json.dumps({
    "charID": "<character uuid>",
    "functions": [
        {"id": "<function uuid>", "status": "inactive"}
    ]
})
headers = {
    "CONVAI-API-KEY": "<your api key>",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=payload)
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
  "charID": "<character uuid>",
  "functions": [
    {"id": "<function uuid>", "status": "inactive"}
  ]
}'
```
{% endcode %}
{% endtab %}
{% endtabs %}

Confirm with `/functions/list/` and `character_id` set — unlinked functions show `"status": "inactive"`.

{% hint style="info" %}
Unlinking only removes the character association. To remove the function from your account entirely (and every character it is linked to), use [Delete a function](#delete-a-function).
{% endhint %}

***

## Delete a function

<mark style="color:green;">`POST`</mark> `https://api.convai.com/functions/delete/`

Deletes a function you own and removes every character association for it. This cannot be undone.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |
| Content-Type<mark style="color:red;">\*</mark>   | String | Must be `application/json`                                                                                 |

#### Request body

| Name                                              | Type   | Description                    |
| ------------------------------------------------- | ------ | ------------------------------ |
| function\_id<mark style="color:red;">\*</mark>    | String | UUID of the function to delete |

#### Example payload

```json
{
  "function_id": "<function uuid>"
}
```

{% tabs %}
{% tab title="200: OK" %}
```json
{
  "transactionID": "<uuid>",
  "status": "success"
}
```
{% endtab %}

{% tab title="403 Forbidden" %}
```json
{
  "ERROR": "You don't have permission to delete this function",
  "Reference ID": "<uuid>"
}
```
{% endtab %}

{% tab title="404 Not Found" %}
```json
{
  "ERROR": "Function with id <function uuid> not found",
  "Reference ID": "<uuid>"
}
```
{% endtab %}

{% tab title="401 Unauthorized" %}
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

url = "https://api.convai.com/functions/delete/"

payload = json.dumps({
    "function_id": "<function uuid>"
})
headers = {
    "CONVAI-API-KEY": "<your api key>",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl --location --request POST 'https://api.convai.com/functions/delete/' \
--header 'CONVAI-API-KEY: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "function_id": "<function uuid>"
}'
```
{% endcode %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
To disconnect a function from a character without deleting it, use [Unlink functions from a character](#unlink-functions-from-a-character).
{% endhint %}
