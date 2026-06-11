---
title: Scene messages
description: Reference for update-scene-metadata and update-template-keys client messages that update descriptive scene context and bot prompt template variables.
last_reviewed: "2026-06-11"
---

`update-scene-metadata` and `update-template-keys` are client messages that update scene-level data during an active session. `update-scene-metadata` refreshes the descriptive object list used for action grounding. `update-template-keys` updates string variables that the bot's prompt template uses to personalize responses.

## update-scene-metadata

`update-scene-metadata` sends a new list of scene objects, each with a name and description. Convai uses these descriptions to understand the current state of the environment when grounding character actions and responses.

{% hint style="warning" %}
`update-scene-metadata` updates descriptive context only. It does not modify the authoritative `action_config.objects` list supplied at connect time. The bot cannot perform actions on objects that were not declared in `action_config` on `/connect`.
{% endhint %}

### Message format

```json
{
  "type": "update-scene-metadata",
  "data": {
    "scene_metadata": [
      {
        "name": "fire_extinguisher",
        "description": "A red CO2 extinguisher mounted on the east wall, fully charged."
      },
      {
        "name": "emergency_exit",
        "description": "The emergency exit door on the north wall, currently unlocked."
      }
    ]
  }
}
```

### Data fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `scene_metadata` | array of objects | Yes | — | List of scene objects. Replaces the previous `scene_metadata` entirely on each update. |
| `scene_metadata[].name` | string | Yes | — | The object name. Should match a name declared in `action_config.objects` at connect time for action grounding to apply. |
| `scene_metadata[].description` | string | Yes | — | A description of the object's current state or position. |

### Server response

```json
{
  "type": "server-response",
  "event_type": "update-scene-metadata",
  "status": "success",
  "message": "Scene metadata updated successfully"
}
```

## update-template-keys

`update-template-keys` sets string key-value pairs that the bot's configured prompt template can reference. Use it to inject runtime values — such as player name, current location, or mission status — into the character's system prompt without reconnecting.

### Message format

```json
{
  "type": "update-template-keys",
  "data": {
    "template_keys": {
      "player_name": "Sergeant Torres",
      "current_location": "sector-7",
      "alert_level": "red"
    }
  }
}
```

### Data fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `template_keys` | object (string → string) | Yes | — | Key-value pairs to update in the template context. Keys correspond to placeholder names in the bot's configured prompt template. |

### Server response

```json
{
  "type": "server-response",
  "event_type": "update-template-keys",
  "status": "success",
  "message": "Template keys updated successfully"
}
```

{% content-ref url="client-messages.md" %}
[Client messages overview](client-messages.md)
{% endcontent-ref %}

{% content-ref url="client-message-errors.md" %}
[Client message errors](client-message-errors.md)
{% endcontent-ref %}
