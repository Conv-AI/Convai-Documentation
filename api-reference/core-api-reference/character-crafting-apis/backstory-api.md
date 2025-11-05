---
description: >-
  Learn how to use the Backstory API to create and manage character backstories,
  adding depth and personality to your NPCs.
---

# Backstory API

{% hint style="danger" %}
This API is available only on the Professional Plan and above.
{% endhint %}

## Generate Backstory for Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/generate-backstory`

Generate Backstory API is implemented as Server Sent Event (SSE). Given some initial description about the character and their name, this API can generate a description for the character.

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name      | Type   | Description                                              |
| --------- | ------ | -------------------------------------------------------- |
| inputText | String | High level character description.                        |
| charName  | String | Character name for which description is being generated. |



{% tabs %}
{% tab title="200: OK Returns multiple SSE events." %}
```json
# Output Format:
# The response will be streamed as Server-Sent Events (SSE).
# Each event will have a 'data' field containing a string with a part of the backstory.
# Example of a single event:

data: You step off the train, greeted by the bustling city sounds.

# Multiple events will be received, each containing a portion of the backstory.
# The full backstory can be assembled by concatenating the 'data' from all events.
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
import json
from sseclient import SSEClient
import requests

url = "https://api.convai.com/character/generate-backstory"

headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Accept': 'text/event-stream'
}

form_data = { 
    "inputText": "Lawyer in the New York City. Achiever. Stubborn.",
    "charName": "Mindy"
}

# Create a session to manage cookies and keep-alive
session = requests.Session()

# Send the POST request with form-data and stream the response
response = session.post(url, headers=headers, data=form_data, stream=True)

# Create an SSE client from the response
client = SSEClient(response)

# Process the events
full_response = ""
for event in client.events():
    if event.data:
        full_response += event.data

print(full_response)
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
{% code overflow="wrap" %}
```shell
curl -X POST 'https://api.convai.com/character/generate-backstory' \
-H 'CONVAI-API-KEY: <Your-API-Key>' \
-H 'Accept: text/event-stream' \
-d 'inputText=Lawyer in the New York City. Achiever. Stubborn.' \
-d 'charName=Mindy'
```
{% endcode %}
{% endtab %}
{% endtabs %}
