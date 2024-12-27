---
description: The page list all the APIs needed to interact Narrative Design
---

# Narrative Design API

{% hint style="danger" %}
This API is accessible with all plans.
{% endhint %}

## Toggle Narrative Design

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/toggle-is-narrative-driven`

Enable/Disable the Narrative Graph for your character.

#### Headers

<table><thead><tr><th width="211">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name                  | Type   | Description                                                 |
| --------------------- | ------ | ----------------------------------------------------------- |
| character\_id         | String | Id of your character.                                       |
| is\_narrative\_driven | Bool   | Set it to true or false, to enable disable Narrative Graph. |

{% tabs %}
{% tab title="200: OK " %}
```json
{"STATUS": "Successful"}
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

url = "https://api.convai.com/character/toggle-is-narrative-driven"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id": "<Your-Character-Id>",
    "is_narrative_driven": True
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
curl -X POST "https://api.convai.com/character/toggle-is-narrative-driven" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{"character_id": "<Your-Character-Id>", "is_narrative_driven": true}'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Create Section

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/create-section`

Create new section for your Character.

#### Headers

<table><thead><tr><th width="211">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name                     | Type   | Description                   |
| ------------------------ | ------ | ----------------------------- |
| character\_id            | String | Id of your character.         |
| objective                | String | Section Objective             |
| section\_name            | String | Name of the Section.          |
| updated\_character\_data | Json   | \*Ignore\* Field is not used. |
| behavior\_tree\_code     | String | \*Ignore\* Field is not used. |
| bt\_constants            | String | \*Ignore\* Field is not used. |

{% tabs %}
{% tab title="200: OK Section Created " %}
```json
{
    "section_id": "<New-Section-Id>"
}
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

url = "https://api.convai.com/character/narrative/create-section"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Your-Character-Id>",
    "objective":"Section Objective",
    "section_name":"SectionName",
    "updated_character_data":{},
    "behavior_tree_code":"",
    "bt_constants":""
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
curl -X POST "https://api.convai.com/character/narrative/create-section" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
         "character_id": "<Your-Character-Id>",
         "objective": "Section Objective",
         "section_name": "SectionName",
         "updated_character_data": {},
         "behavior_tree_code": "",
         "bt_constants": ""
     }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Edit Section

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/edit-section`

Edit section for your Character. You would send all the fields that you want to update for a section updated\_character\_data json. Following are the valid key.

* "section\_name"
* "objective"
*   "decisions": This is a list of json. Each entry in the list should have following format.

    ```
    {
        "criteria":"Decision Criteria",
        "next_section_id":"ID of the section to transition"
    }
    ```

#### Headers

<table><thead><tr><th width="226">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name                     | Type   | Description                       |
| ------------------------ | ------ | --------------------------------- |
| character\_id            | String | Id of your character.             |
| updated\_character\_data | Json   | Contains fields that are updated. |
| section\_id              | String | Id of the section to update.      |

{% tabs %}
{% tab title="200: OK Section Updated " %}
```json
{
    "status": "success",
    "section_id": "<Section-Id>",
    "updated_data": {
        "objective": "Some new objective."
    }
}
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

url = "https://api.convai.com/character/narrative/edit-section"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Your-Character-Id>",
    "section_id":"<Section-Id->",
    "updated_data":{
        "decisions":[
            {"criteria":"User agrees to take tour.", "next_section_id":"b9d7f568-7d06-11ef-be6a-42010a7be011"}
        ],  
        "objective":"Offer user tour of a Museum.",
        "section_name":"Welcome Section"
    }   
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
curl -X POST "https://api.convai.com/character/narrative/edit-section" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
         "character_id": "<Your-Character-Id>",
         "section_id": "<Section-Id->",
         "updated_data": {
             "decisions": [
                 {
                     "criteria": "User agrees to take tour.",
                     "next_section_id": "b9d7f568-7d06-11ef-be6a-42010a7be011"
                 }
             ],
             "objective": "Offer user tour of a Museum.",
             "section_name": "Welcome Section"
         }
     }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Get Section

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/get-section`

Get details for a particular narrative section of your Character.&#x20;

#### Headers

<table><thead><tr><th width="226">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name          | Type   | Description                 |
| ------------- | ------ | --------------------------- |
| character\_id | String | Id of your character.       |
| section\_id   | String | Id of the section to fetch. |

{% tabs %}
{% tab title="200: OK Section Details " %}
```json
{
   "character_id": "<Your-CharacterId>",
   "section_id": "<Your-SectionId>",
   "objective": "Offer user tour of History Museum.",
   "decisions": [{"criteria": "User agrees to take tour.", "next_section_id": "12345568-7890-1123-4456-424242424242"}],
   "parents": null,
   "updated_character_data": {},
   "bt_constants": "",
   "behavior_tree_code": "",
   "section_name": "Welcome Section",
   "triggers": null,
   "node_position": []
}
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

url = "https://api.convai.com/character/narrative/get-section"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Your-Character-Id>",
    "section_id":"<Section-Id->", 
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
curl -X POST "https://api.convai.com/character/narrative/get-section" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
           "character_id": "<Your-Character-Id>",
           "section_id": "<Section-Id->"
         }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## List Sections

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/list-sections`

List details of all narrative sections for a given character.

#### Headers

<table><thead><tr><th width="226">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name          | Type   | Description           |
| ------------- | ------ | --------------------- |
| character\_id | String | Id of your character. |

{% tabs %}
{% tab title="200: OK List of Section Details " %}
```json
[
  {
    "character_id": "<Your-Character-Id>",
    "section_id": "123456789-7ddd-dddd-bbbb-424242424242",
    "objective": "",
    "decisions": null,
    "parents": null,
    "updated_character_data": {},
    "bt_constants": "",
    "behavior_tree_code": "",
    "section_name": "section 1",
    "triggers": null,
    "node_position": []
  },
  {
    "character_id": "<Your-Character-Id>",
    "section_id": "100000789-7ddd-dddd-bbbb-42424242424",
    "objective": "Offer user tour of History Museum.",
    "decisions": [
      {
        "criteria": "User agrees to take tour.",
        "next_section_id": "123456789-7ddd-dddd-bbbb-424242424242"
      }
    ],
    "parents": null,
    "updated_character_data": {},
    "bt_constants": "",
    "behavior_tree_code": "",
    "section_name": "Welcome Section",
    "triggers": null,
    "node_position": []
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

url = "https://api.convai.com/character/narrative/list-sections"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Your-Character-Id>",
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
curl -X POST "https://api.convai.com/character/narrative/list-sections" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
           "character_id": "<Your-Character-Id>"
         }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Delete Section

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/delete-section`

Delete a narrative section of your Character.&#x20;

#### Headers

<table><thead><tr><th width="226">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name          | Type   | Description                  |
| ------------- | ------ | ---------------------------- |
| character\_id | String | Id of your character.        |
| section\_id   | String | Id of the section to delete. |

{% tabs %}
{% tab title="200: OK Section Deleted " %}
```json
{"STATUS": "Successful"}
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

url = "https://api.convai.com/character/narrative/delete-section"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Your-Character-Id>",
    "section_id":"<Section-Id->", 
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
curl -X POST "https://api.convai.com/character/narrative/delete-section" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
         "character_id": "<Your-Character-Id>",
         "section_id": "<Section-Id->"
     }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Create Trigger

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/create-trigger`

Create a new Trigger for your Character.

#### Headers

<table><thead><tr><th width="226">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name                 | Type   | Description                                                                                                          |
| -------------------- | ------ | -------------------------------------------------------------------------------------------------------------------- |
| character\_id        | String | Id of your character.                                                                                                |
| trigger\_name        | String | Name of the trigger. Must be unique for a character.                                                                 |
| trigger\_message     | String | Message for the trigger. Commonly tell the event for which the Trigger is invoked. E.g. User entered the scene.      |
| desgination\_section | String | Destination section-id for this trigger. Do not pass this field if you don't want to connect Trigger to any section. |

{% tabs %}
{% tab title="200: OK Trigger Created " %}
```json
{
    "character_id": "<Your-Character-Id>,
    "trigger_id": "<ID-Of-The-Newly-Created-Trigger>",
    "trigger_name": "StartTrigger",
    "trigger_message": "User has entered the museum.",
    "destination_section": "<Destination-Section-ID>",
    "node_position": []
}
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

url = "https://api.convai.com/character/narrative/create-trigger"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Your-Character-Id>",
    "trigger_message":"User has entered the museum.",
    "trigger_name":"StartTrigger",
    "destination_section": "<Destination-Section-ID-to-connect-to>"
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
curl -X POST "https://api.convai.com/character/narrative/create-trigger" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
         "character_id": "<Your-Character-Id>",
         "trigger_message": "User has entered the museum.",
         "trigger_name": "StartTrigger",
         "destination_section": "<Destination-Section-ID-to-connect-to>"
     }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Update Trigger

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/update-trigger`

Edit a Trigger. You would send all the fields that you want to update for a trigger via updated\_data json. Following are the valid key.

* "trigger\_name": New trigger name. Must be unique.
* "trigger\_message": New trigger message.
* "destination\_section": New destination section-id for the trigger.

#### Headers

<table><thead><tr><th width="226">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name          | Type   | Description                       |
| ------------- | ------ | --------------------------------- |
| character\_id | String | Id of your character.             |
| updated\_data | Json   | Contains fields that are updated. |
| trigger\_id   | String | Id of the trigger to update.      |

{% tabs %}
{% tab title="200: OK Trigger Updated " %}
```json
{
    "STATUS": "Successful",
    "message": "Trigger updated successfully"
}
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

url = "https://api.convai.com/character/narrative/update-trigger"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Character-Id>",
    "trigger_id": "<Trigger-Id>",
    "updated_data": {
        "destination_section":"<New-Destination-Section-Id>",
        "trigger_message":"User has entered the Computer history museum"
    }   
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
curl -X POST "https://api.convai.com/character/narrative/update-trigger" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
         "character_id": "<Character-Id>",
         "trigger_id": "<Section-Id>",
         "updated_data": {
             "destination_section": "<New-Destination-Section-Id>",
             "trigger_message": "User has entered the Computer history museum"
         }
     }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Delete Trigger

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/delete-trigger`

Delete an existing Trigger.&#x20;

#### Headers

<table><thead><tr><th width="226">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name          | Type   | Description                  |
| ------------- | ------ | ---------------------------- |
| character\_id | String | Id of your character.        |
| trigger\_id   | String | Id of the trigger to delete. |

{% tabs %}
{% tab title="200: OK Trigger Deleted " %}
```json
{
    "STATUS": "Successful",
    "message": "Trigger deleted successfully"
}
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

url = "https://api.convai.com/character/narrative/delete-trigger"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Character-Id>",
    "trigger_id": "<Trigger-Id>",  
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
curl -X POST "https://api.convai.com/character/narrative/delete-trigger" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
         "character_id": "<Character-Id>",
         "trigger_id": "<Trigger-Id>"
     }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Get Trigger

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/get-trigger`

Fetch details of an existing Trigger.&#x20;

#### Headers

<table><thead><tr><th width="226">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name          | Type   | Description                 |
| ------------- | ------ | --------------------------- |
| character\_id | String | Id of your character.       |
| trigger\_id   | String | Id of the trigger to fetch. |

{% tabs %}
{% tab title="200: OK Trigger Details " %}
```json
{
    "character_id": "<Character-Id>",
    "trigger_id": "<Trigger-Id>",
    "trigger_name": "UserEntry",
    "trigger_message": "User has entered the museum.",
    "destination_section": null,
    "node_position": []
}
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

url = "https://api.convai.com/character/narrative/get-trigger"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Character-Id>",
    "trigger_id": "<Trigger-Id>",  
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
curl -X POST "https://api.convai.com/character/narrative/get-trigger" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{
           "character_id": "<Character-Id>",
           "trigger_id": "<Trigger-Id>"
         }'
```
{% endcode %}
{% endtab %}
{% endtabs %}

## List Triggers

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/narrative/list-triggers`

List all the triggers for a Character.&#x20;

#### Headers

<table><thead><tr><th width="226">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>CONVAI-API-KEY<mark style="color:red;">*</mark></td><td>String</td><td>The unique api-key provided for every user. Found under the Key icon when logged into your Convai account.</td></tr></tbody></table>

#### Request Body

| Name          | Type   | Description           |
| ------------- | ------ | --------------------- |
| character\_id | String | Id of your character. |

{% tabs %}
{% tab title="200: OK List of Trigger Details " %}
```json
[
  {
    "character_id": "<Character-Id>",
    "trigger_id": "<Trigger-ID1>",
    "trigger_name": "trigger 1",
    "trigger_message": "",
    "destination_section": null,
    "node_position": []
  },
  {
    "character_id": "<Character-Id>",
    "trigger_id": "<Trigger-ID2>",
    "trigger_name": "UserEntry",
    "trigger_message": "User has entered the museum.",
    "destination_section": null,
    "node_position": [ ]
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

url = "https://api.convai.com/character/narrative/list-triggers"
headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "character_id":"<Character-Id>", 
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
curl -X POST "https://api.convai.com/character/narrative/list-triggers" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{"character_id":"<Character-Id>"}'
```
{% endcode %}
{% endtab %}
{% endtabs %}
