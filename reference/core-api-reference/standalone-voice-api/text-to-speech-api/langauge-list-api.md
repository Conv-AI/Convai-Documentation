---
description: >-
  API to retrieve the full list of languages, both public and private, available
  to a user.
---

# Langauge List API

## Convai's Language List API endpoint&#x20;

<mark style="color:green;">`GET`</mark> `https://api.convai.com/tts/get_available_languages`

This endpoint is called to get the list of available languages for a user. The voice list includes information regarding all the public as well as user's private languages.&#x20;

## Request

The request body only required the following header field :

### Headers

| Field Name                                       | Type   | Value / Description  |
| ------------------------------------------------ | ------ | -------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | Your Convai API Key. |

## Response

On success, the API will return a nested JSON object in the following format :&#x20;

```
[
{
    "en-US": {
      "lang_code": "en-US",
      "lang_name": "English"
    }
  },
  {
    "es-ES": {
      "lang_code": "es-ES",
      "lang_name": "Spanish"
    }
  }, ...

]
```
