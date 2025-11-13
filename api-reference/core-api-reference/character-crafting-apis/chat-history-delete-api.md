---
description: API endpoint for deleting character sessions.
hidden: true
---

# Chat History Delete API

{% hint style="danger" %}
This API is available only to select customers.
{% endhint %}

## Delete Sessions for a Character

<mark style="color:green;">`POST`</mark> `https://api.convai.com/character/chatHistory/delete`

#### Headers

| Name                                             | Type   | Description                                                                                                |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every user. Found under the Key icon when logged into your Convai account. |

#### Request Body

| Name                                         | Type   | Description                        |
| -------------------------------------------- | ------ | ---------------------------------- |
| charID<mark style="color:red;">\*</mark>     | String | Id of your character.              |
| sessionIDs<mark style="color:red;">\*</mark> | list   | list of session ids to be deleted. |

{% tabs %}
{% tab title="200: OK" %}
```json
{
  "status": "SUCCESSFULLY DELETED"
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

url = "https://api.convai.com/character/chatHistory/delete"

headers = { 
    'CONVAI-API-KEY': '<Your-API-Key>',
    'Content-Type': 'application/json'
}

# Create a dictionary for the JSON payload
payload = { 
    "charID": "<Your-Character-Id>",
    "sessionIDs": ["<your-session-id-1>",] 
}

# Convert the payload to JSON
json_payload = json.dumps(payload)

response = requests.post(url, headers=headers, data=json_payload)

print(response.json())
```
{% endcode %}
{% endtab %}

{% tab title="cURL" %}
```sh
curl -X POST "https://api.convai.com/character/chatHistory/delete" \
     -H "CONVAI-API-KEY: <Your-API-Key>" \
     -H "Content-Type: application/json" \
     -d '{"charID": "<Your-Character-Id>", "sessionIDs": ["<your-session-id-1>"]}'
```
{% endtab %}
{% endtabs %}
