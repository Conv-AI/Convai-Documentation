---
description: API to retrieve the list of characters, created by a user.
---

# Character List API

## Convai's Character List API endpoint

<mark style="color:green;">`POST`</mark> [`https://api.convai.com/character/list`](https://api.convai.com/character/list)

This endpoint is called to get the list of characters for a user account. The character list includes information regarding all the characters.

## Request

The request body only requires the following header field:

## Headers

| Field Name       | Type   | Value / Description   |
| ---------------- | ------ | --------------------- |
| CONVAI-API-KEY\* | String | User's Convai API Key |

## Response

{% tabs %}
{% tab title="200 : OK" %}
On success, the API will return a nested JSON object in the following format :&#x20;

```
{
  "characters": [
    {
      "character_name": "Rafael",
      "collection_name": "convai_default_collection",
      "user_id": "SOME_USER_ID",
      "character_id": "SOME_CHAR_ID",
      "model_type": "RPM-3D",
      "state_names": [],
      "state_links": [],
      "listing": "unlisted",
      "voice_type": "SOME_VOICE",
      "voice_pitch": 0.0,
      "blockchain": "NULL",
      "contract_address": "NULL",
      "mint_address": "NULL",
      "owner_address": "NULL",
      "timestamp": "2023-11-07T02:57:59",
      "character_actions": [
        "laugh",
        "walk",
        "run",
        "giggle"
      ],
      "character_emotions": [],
      "model_details": {
        "modelType": "RPM-3D",
        "modelLink": "https://models.readyplayer.me/63f8983f9dc8b8dcb3aff14a.glb",
        "modelPlaceholder": "https://models.readyplayer.me/63f8983f9dc8b8dcb3aff14a.png?pose=relaxed&background=0,0,60",
        "METAHUMAN": {
          "avatar_id": "4d923463-f1c8-4169-95f4-d6d19f6ad49a",
          "avatar_image": "https://storage.googleapis.com/experience-asset-storage/user-uploaded-avatar-image/4d923463-f1c8-4169-95f4-d6d19f6ad49a_avatar_image.png?img_last_modified=1737042662?img_last_modified=1737113901",
          "avatar_image_square": "https://storage.googleapis.com/experience-asset-storage/user-uploaded-avatar-image/4d923463-f1c8-4169-95f4-d6d19f6ad49a_avatar_image_square?img_last_modified=1737042662?img_last_modified=1737113901",
          "experience_id": "faa18c71-fc1d-4282-b616-f88a79cd9d62",
          "bg_image": ""
        }
      },
      "language_code": "en-US",
      "guard_rails": {
        "type1": "3"
      },
      "metadata_filter": {},
      "personalised_prompt_config": {
        "MODEL": "gpt-4o",
        "PROMPT": "",
        "VERBOSITY": 2,
        "TEMPERATURE": 0.07,
        "MODERATION_ENABLED": true,
        "USE_COMBINED_PROMPT": "true",
        "ALLOWED_MODERATION_FILTERS": [
          "violence",
          "violence/graphic"
        ],
        "USE_ACTION_OPTMIZED_PROMPT": true
      },
      "boosted_words": {
        "words": []
      },
      "guardrail_meta": {
        "limitResponseLevel": 4,
        "blockedWords": []
      },
      "start_narrative_section_id": null,
      "is_narrative_driven": false,
      "character_traits": {
        "catch_phrases": [],
        "speaking_style": "None",
        "personality_traits": {
          "openness": 2,
          "sensitivity": 2,
          "extraversion": 2,
          "agreeableness": 2,
          "meticulousness": 2
        }
      },
      "language_codes": [
        "en-US"
      ],
      "memory_settings": {
        "enabled": false
      },
      "last_interacted_with": "2025-02-20T07:20:13",
      "pronunciation_metadata": {
        "pronunciations": [
          {
            "word": "OCMO",
            "ipaPronunciation": "ɔkmow",
            "customPronunciation": "aukmo"
          }
        ]
      },
      "description": "",
      "speaking_style": {
        "description": "",
        "sample_dialogues": ""
      },
      "embodiment": null,
      "embodiment_data": {}
    },
    {
      "character_name": "Steven",
      "collection_name": "convai_default_collection",
      "user_id": "SOME_USER_ID",
      "character_id": "SOME_CHAR_ID",
      "model_type": "RPM-3D",
      "state_names": [],
      "state_links": [],
      "listing": "unlisted",
      "voice_type": "SOME_VOICE",
      "voice_pitch": 0.0,
      "blockchain": "NULL",
      "contract_address": "NULL",
      "mint_address": "NULL",
      "owner_address": "NULL",
      "timestamp": "2024-12-19T10:30:42",
      "character_actions": [],
      "character_emotions": [],
      "model_details": {
        "modelType": "RPM-3D",
        "modelLink": "https://models.readyplayer.me/673282ecef64719015ef8068.glb",
        "modelPlaceholder": "https://models.readyplayer.me/673282ecef64719015ef8068.png?pose=relaxed&background=0,0,60&size=512",
        "METAHUMAN": {
          "avatar_id": "c63e322d-c2cb-46f0-a466-9fd7c8073f9b",
          "avatar_image": "https://storage.googleapis.com/experience-asset-storage/user-uploaded-avatar-image/c63e322d-c2cb-46f0-a466-9fd7c8073f9b_avatar_image.png?img_last_modified=1737042663",
          "avatar_image_square": "https://storage.googleapis.com/experience-asset-storage/user-uploaded-avatar-image/c63e322d-c2cb-46f0-a466-9fd7c8073f9b_avatar_image_square?img_last_modified=1737042663",
          "experience_id": "7eb6e6eb-158d-44b1-8ecf-1657205f7765",
          "bg_image": ""
        }
      },
      "language_code": "en-US",
      "guard_rails": {
        "type1": "3"
      },
      "metadata_filter": {},
      "personalised_prompt_config": {
        "PROMPT": "",
        "MODEL": "gpt-4o-mini",
        "VERBOSITY": 2,
        "SPEAKER": "User",
        "MODERATION_ENABLED": true,
        "ALLOWED_MODERATION_FILTERS": [
          "violence",
          "violence/graphic"
        ],
        "USE_COMBINED_PROMPT": true,
        "TEMPERATURE": 0.7
      },
      "boosted_words": {
        "words": []
      },
      "guardrail_meta": {
        "limitResponseLevel": 4,
        "blockedWords": []
      },
      "start_narrative_section_id": "d20e62cc-bdf5-11ef-a5c2-42010a7be016",
      "is_narrative_driven": true,
      "character_traits": {
        "catch_phrases": [],
        "speaking_style": "None",
        "personality_traits": {
          "openness": 2,
          "sensitivity": 2,
          "extraversion": 2,
          "agreeableness": 2,
          "meticulousness": 2
        }
      },
      "language_codes": [
        "en-US"
      ],
      "memory_settings": {
        "enabled": true
      },
      "last_interacted_with": "2025-02-12T08:23:05",
      "pronunciation_metadata": {
        "pronunciations": []
      },
      "description": "",
      "speaking_style": {
        "description": "",
        "sample_dialogues": ""
      },
      "embodiment": null,
      "embodiment_data": {
        "looks_description": "",
        "clothes_description": ""
          }
        }, .... 
    ]
    }
```


{% endtab %}

{% tab title="400 : API Key not found" %}
No CONVAI-API-KEY provided by the user in the Request.
{% endtab %}

{% tab title="401 : Invalid API Key provided" %}
Invalid CONVAI-API-KEY provided by the user in the Request.
{% endtab %}

{% tab title="500 : Internal Server Error" %}
Server Side Failure. Please reach out to support.
{% endtab %}
{% endtabs %}

### Response Field Descriptions&#x20;

* `character_name`: Name of the character.
* `user_id`: User ID of the user / character owner.
* `character_id`: Unique ID of the character.
* `voice_type`: Voice set for the character.
* `model_type`: Model (Avatar) used by the character.
* `timestamp`: Timestamp when the character was created.
* `character_actions`: Set of actions described by the user for the character.
* `character_emotions`: Set of emotions described by the user for the character.
* `personalised_prompt_config`: Information regarding the model and prompt used by the character at the backend.
* `language_codes`: List of languages supported by the character.
* `pronunciation_metadata`: Information related to the custom pronunciations set for the character.

## Sample Code Snippet

```python
import requests

# URL of the API endpoint
url = 'https://api.convai.com/character/list'

# creating the header
headers = {
     'CONVAI-API-KEY': '<your api key>',
}

# Make the request
response = requests.post(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    print(response.json())
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

```
