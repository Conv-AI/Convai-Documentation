---
description: >-
  API to retrieve the full list of voices, both public and private, available to
  a user.
---

# Voice List API

## Convai's Voice List API endpoint&#x20;

<mark style="color:green;">`GET`</mark> `https://api.convai.com/tts/get_available_voices`

This endpoint is called to get the list of available voices for a user. The voice list includes information regarding all the public as well as user's private voices.&#x20;

## Request

The request body only required the following header field :

### Headers

| Field Name                                       | Type   | Value / Description  |
| ------------------------------------------------ | ------ | -------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | Your Convai API Key. |

## Response

{% tabs %}
{% tab title="200 : OK" %}
On success, the API will return a nested JSON object in the following format :&#x20;

```
{
    "<Section Name#1>" : [
        {
            "<Voice Name #1>" : {
                "voice_value" : "voice_value_for_voice#1",
                "lang_codes"  : [<list of language codes, supported by the voice>],
                "gender"      : "<MALE/FEMALE>",
                "sample_link" : <link to the voice sample file>
            }
        },
        
        {
            "<Voice Name #2>" : {
                "voice_value" : "voice_value_for_voice#2",
                "lang_codes"  : [<list of language codes, supported by the voice>],
                "gender"      : "<MALE/FEMALE>",
                "sample_link" : <link to the voice sample file>
            }
        },
        ...
    ]
}
```
{% endtab %}

{% tab title="400 : API key not found" %}
No CONVAI-API-KEY provided by the user in the Request.
{% endtab %}

{% tab title="401 : Invalid API key provided" %}
Invalid CONVAI-API-KEY provided by the user in the Request.
{% endtab %}

{% tab title="500 : Internal Server Error" %}
Server Side Failure. Please reach out to support.
{% endtab %}
{% endtabs %}

### Response Field Descriptions&#x20;

* `Section Name` : The name of the section under which the voice is available (in the Convai Playground).
* `Voice Name` : The name of the voice that is visible to the user on the Convai Playground.
* `voice_value` : The unique id for the voice, uniquely identifying the voices. This is the value that needs to be sent to the backend while using the Convai's TTS endpoint or updating/setting the voice for the character.
* `lang_codes` : List of languages supported by the voice.
* `gender` : Gender of the voice (MALE/FEMALE).
* `sample_link` : The link to the voice sample file.



### Sample Code Snippet

```
import requests

# URL of the API endpoint
url = 'https://api.convai.com/tts/get_available_voices'

# creating the header
headers = {
     'CONVAI-API-KEY': '<your api key>',
}

# Make the request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    print(response.json())
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

```
