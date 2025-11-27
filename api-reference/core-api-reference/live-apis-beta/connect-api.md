---
description: >-
  Establish a live chatbot session for your Convai character, enabling users to
  connect via audio or video and maintain conversational context.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/api-reference/core-api-reference/live-apis-beta/connect-api
---

# Connect API

## Overview

The **Connect API** establishes a live interactive session between an end-user and a Convai character.\
It allows developers to maintain conversational context using the `character_session_id` returned in each response and supports both **audio** and **video** connections.\
Optionally, scene descriptions or dynamic information can be included to tailor the interaction.

## Connecting to a Character

<mark style="color:green;">`POST`</mark> `https://live.convai.com/connect`

### Headers

<table><thead><tr><th width="199">Name</th><th width="108.9998779296875">Type</th><th>Description</th></tr></thead><tbody><tr><td>X-API-Key<mark style="color:red;">*</mark></td><td>String</td><td>Your Convai API key.</td></tr><tr><td>Content-Type</td><td>String</td><td>Must be set to <code>application/json</code>.</td></tr></tbody></table>

***

### Request Body

<table><thead><tr><th width="203.6666259765625">Name</th><th width="104">Type</th><th>Description</th></tr></thead><tbody><tr><td>character_id<mark style="color:red;">*</mark></td><td>String</td><td>Unique ID of the character to connect with.</td></tr><tr><td>connection_type</td><td>String</td><td><p>Connection mode for the session. </p><p>Supported values: <code>"audio"</code> (default) or <code>"video"</code>.</p></td></tr><tr><td>character_session_id</td><td>String</td><td>Existing session ID for maintaining conversation continuity. If omitted, a new one is generated.</td></tr><tr><td>dynamic_info</td><td><a href="connect-api.md#dynamic-info">JSON</a></td><td>Real-time contextual data to influence the conversation flow.</td></tr><tr><td>scene_description</td><td><a href="connect-api.md#scene_description">JSON</a></td><td>Descriptions of the current scene or environment context.</td></tr><tr><td>speaker_id</td><td>String</td><td>Speaker id of the user</td></tr></tbody></table>

{% tabs %}
{% tab title="dynamic info" %}
```json
{
    "text": "string"
}
```
{% endtab %}

{% tab title="scene_description" %}
```json
[
  {
    "name": "string",
    "description": "string"
  }
]
```
{% endtab %}
{% endtabs %}

***

### Response

{% tabs %}
{% tab title="200: OK The webrtc room with your character is created." %}
```json
{
  "session_id": "<your temporary session id for the live session>",
  "character_session_id": "<your session id. In case of a new session, it returns a newly generated value or returns the old one>",
  "room_url": "<url of the room your client needs to join>",
  "room_name": "<name of the room to join>",
  "token": "<token for the client to join the room>",
  "speaker_id": "<speaker id of the user in the session, null if not sent in request>"
}
```
{% endtab %}

{% tab title="404: Not Found Response generation failed for the request" %}
```json
{
    "detail": "Character not found or doesn't belong to user"
}
```
{% endtab %}

{% tab title="422: Incase of bad request" %}
```json
{
    "detail": [
        {
            "type": "<type_of_issue_with_the_request_body>",
            "loc": [],
            "msg": "<message>",
            "input": "<input value>",
            "ctx": {
                "error": "more details about the error"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}

***

## Important Notes

{% hint style="warning" %}
Convai strictly follows **OpenAI’s Content Policy** for API usage.\
Users must not generate or distribute toxic, harmful, or inappropriate content.\
Repeated violations will result in your API key being **blacklisted**.
{% endhint %}

{% hint style="info" %}
Always reuse the same **character\_session\_id** if you want to **maintain context** between interactions.
{% endhint %}

{% hint style="info" %}
A new **character\_session\_id** creates a **fresh session** without prior context.
{% endhint %}

***

## Example Requests

{% tabs %}
{% tab title="Python" %}
```python
import requests

url = "https://live.convai.com/connect"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "<your api key>"  # Replace with your actual Convai API key
}

data = {
    "character_id": "<your character id>",
    "connection_type": "audio",  # or "video"
    "character_session_id": "string"  # optional
## if need to specify scene description
##    "scene_description": [
##        {
##            "name": "string",
##            "description": "string"
##        }
##    ],
##if need to specify dynamic information
##    "dynamic_info": {
##        "text": "string"
##    },
}

response = requests.post(url, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response:", response.text)
```
{% endtab %}

{% tab title="cURL" %}
```shell
curl --location 'https://live.convai.com/connect' \
--header 'Content-Type: application/json' \
--header 'X-API-Key: <your api key>' \
--data '{
    "character_id": "<your character id>",
    "connection_type": "audio", // or "video" for video abilities
    "character_session_id": "string" // optional
    "dynamic_info": { // optional
        "text": "string"
    },
    "scene_description": [
        {
            "name": "string",
            "description": "string"
        }
    ], // optional
}'
```
{% endtab %}
{% endtabs %}

***

## Conclusion

The **Connect API** is a key component for integrating Convai’s real-time conversational capabilities into your applications.\
By maintaining session context and dynamically adapting scene or character information, developers can build seamless, context-aware voice or video interactions powered by Convai.
