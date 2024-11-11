---
description: >-
  API to retrieve the full list of languages, both public and private, available
  to a user.
---

# Language List API

## Convai's Language List API endpoint

```markup
GET https://api.convai.com/tts/get_available_languages
```

This endpoint is called to get the list of available languages for a user. The voice list includes information regarding all the public as well as user's private languages.

## Request

The request body only require the following header field :&#x20;

### Headers

| Field Name       | Type   | Value / Description  |
| ---------------- | ------ | -------------------- |
| CONVAI-API-KEY\* | String | Your Convai API Key. |

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



## Current List of supported languages :&#x20;

| Language                | Language Code |
| ----------------------- | ------------- |
| English                 | en-US         |
| Spanish                 | es-ES         |
| French                  | fr-FR         |
| Arabic                  | ar            |
| Hindi                   | hi-IN         |
| Japanese                | ja-JP         |
| Korean                  | ko-KR         |
| Russian                 | ru-RU         |
| Dutch                   | nl-NL         |
| Dutch (Belgium)         | nl-BE         |
| Chinese (Mainland)      | cmn-CN        |
| German                  | de-DE         |
| Vietnamese              | vi-VN         |
| Italian                 | it-IT         |
| Turkish                 | tr-TR         |
| Portuguese (Brazil)     | pt-BR         |
| Mexican Spanish         | es-MX         |
| Cantonese               | zh-HK         |
| Polish (Poland)         | pl-PL         |
| Portuguese (Portugal)   | pt-PT         |
| Spanish (United States) | es-US         |
| Swedish                 | sv-SE         |
| Kazakh (Kazakhstan)     | kk-KZ         |
| Finnish                 | fi-FI         |







