---
description: >-
  All the relevant APIs needed to interact with Knowledge Bank for you AI
  characters with Convai.
---

# Knowledge Bank API

{% hint style="danger" %}
This API is available only with the Enterprise Plan.
{% endhint %}

## Upload a new KB File

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/knowledge-bank/upload`

Users can upload a new KB file. Once the file is successfully uploaded, they can connect it to a character. Upon calling the API, the file will only be uploaded for processing and will not be available for use until the processing is complete. The upload API will return a unique ID assigned to the uploaded file, which must be used for all future interactions with the file.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name       | Type   | Description      |
| ---------- | ------ | ---------------- |
| file\_name | String | Name of the file |
| file       | Bytes  | Raw file bytes   |

{% tabs %}
{% tab title="200: OK The file is successfully uploaded" %}
```json
{
   "id": "<uuid of the uploaded file>",
   "file_name": "<file_name>",
   "is_available": false,
   "status": "inactive",
   "timestamp": "2024-09-17 20:51:09.216522",
   "file_size": "72374"
}

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

url = "https://api.convai.com/character/knowledge-bank/upload"


headers = { 
  'CONVAI-API-KEY': '<Your-API-Key>',
}

# Path to the file you want to upload
file_path = "photosynthesis.txt"

# Open the file in binary mode
with open(file_path, "rb") as file:
    # Create a dictionary for the form data
    form_data = { 
        "file_name": file.name,
        "file": file
    }   

    # Send the POST request with multipart/form-data
    response = requests.post(url, headers=headers, files=form_data)


print(response.text)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl -X POST \
  https://api.convai.com/character/knowledge-bank/upload \
  -H 'CONVAI-API-KEY: <Your-API-Key>' \
  -F 'file_name=photosynthesis.txt' \
  -F 'file=@photosynthesis.txt'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Update Existing KB File

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/knowledge-bank/update`

Users can update an existing KB file by uploading a new version. Once the file is successfully uploaded, they can connect it to a character. Upon calling the API, the file will only be uploaded for processing and will not be available for use until the processing is complete.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name         | Type   | Description                                         |
| ------------ | ------ | --------------------------------------------------- |
| document\_id | String | ID of the existing document that needs to be upated |
| file         | Bytes  | Raw file bytes                                      |

{% tabs %}
{% tab title="200: OK The file is successfully uploaded" %}
```json
{
   "id": "<uuid of the uploaded file>",
   "file_name": "<file_name>",
   "is_available": false,
   "status": "inactive",
   "timestamp": "2024-09-17 20:51:09.216522",
   "file_size": "72374"
}

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

url = "https://api.convai.com/character/knowledge-bank/update"


headers = { 
  'CONVAI-API-KEY': '<Your-API-Key>',
}

# Path to the file you want to upload
file_path = "photosynthesis.txt"

# Open the file in binary mode
with open(file_path, "rb") as file:
    # Create a dictionary for the form data
    files = {"file": ("photosynthesis-filename.txt", file, "text/plain")}
    form_data = {"document_id": "<document_id"}

    # Send the POST request with multipart/form-data
    response = requests.post(url, headers=headers, files=files, data=form_data)


print(response.text)
```
{% endcode %}
{% endtab %}
{% endtabs %}

## List KB File Status

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/knowledge-bank/list`

List the status of KB files. Use this API to check the status of previously uploaded KB files. Once this API returns "_is\_available_" as _true_ for your UUID, you can confidently assume that the previously uploaded file is processed and ready to be connected to your character.

Please note that the list API requires the character\_id as input. Accordingly, it returns a "_status_" field, which can either be "_active_" or "_inactive_." This field indicates whether a particular file is connected to a character. A file is considered connected if its "_status_" is "_active_" in the output.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name          | Type   | Description           |
| ------------- | ------ | --------------------- |
| character\_id | String | Id of your character. |

{% tabs %}
{% tab title="200: OK The file is successfully uploaded" %}
```json
{
  'docs': [
    '{
        "id": "<File UUID>",
        "file_name": "photosynthesis.txt",
        "is_available": true,
        "status": "inactive",
        "timestamp": "2024-09-17 21:44:53.201385",
        "file_size": "1404"
    }',
    '{
        "id": "<File UUID>",
        "file_name": "FAQ.txt",
        "is_available": true,
        "status": "inactive",
        "timestamp": "2024-09-17 21:21:35.566677",
        "file_size": "736"
    }']
}

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

url = "https://api.convai.com/character/knowledge-bank/list"


headers = { 
  'CONVAI-API-KEY': '<Your-API-Key>',
}

# Create a dictionary for the form data
form_data = { 
    'character_id': '<Your-CharacterId>',
}

# Send the POST request with multipart/form-data
response = requests.post(url, headers=headers, data=form_data)

print(response.text)

```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl -X POST 'https://api.convai.com/character/knowledge-bank/list' \
  -H 'CONVAI-API-KEY: <Your-API-Key>' \
  -F 'character_id=<Your-CharacterId>'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Connect (or Disconnect) a KB file to a Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/update`

Update API can be used to attach (or remove) a KB file to your character. Once the file is successfully connected, all future interactions with the character will fetch knowledge from the attached KB as needed.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name   | Type   | Description                                                              |
| ------ | ------ | ------------------------------------------------------------------------ |
| charID | String | Id of your character.                                                    |
| docs   | List   | List of JSON. Each entry correspond to a file. Fields "id" and "status". |

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
    "docs": [
        {   
            "id": "<File-UUID>",
            "status": "active"  # or "inactive" depending on what you want to set
        }   
    ]   
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
curl -X POST 'https://api.convai.com/character/update' \
-H 'CONVAI-API-KEY: <Your-API-Key>' \
-H 'Content-Type: application/json' \
-d '{
  "charID": "<Your-Character-Id>",
  "docs": [
    {
      "id": "<File-UUID>",
      "status": "active"
    }
  ]
}'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Delete a KB file

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/knowledge-bank/delete`

The knowledge bank delete API can be used to permanently remove documents from the user's account. Note that deleting a document will remove it from all characters it is associated with.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name         | Type   | Description                                |
| ------------ | ------ | ------------------------------------------ |
| document\_id | String | Id of the document that should be deleted. |

{% tabs %}
{% tab title="200: OK The file is successfully deleted" %}
```json
{"Successfully deleted document"}
```
{% endtab %}

{% tab title="401 API Key validation has failed" %}
```
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

url = "https://api.convai.com/character/knowledge-bank/delete"

headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
}

# Create a dictionary for the JSON payload
form_data = { 
    "document_id": "<File-UUID>"   
}

response = requests.post(url, headers=headers, data=form_data)

print(response.text)

```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
```bash
curl -X POST "https://api.convai.com/character/knowledge-bank/delete" \
-H "CONVAI-API-KEY: <Your-API-Key>" \
-d "document_id=<File-UUID>"
```
{% endtab %}
{% endtabs %}
