---
title: ActionConfig field reference
description: Reference for every field in the action configuration model and its nested character and object configuration types, including types and constraints.
last_reviewed: "2026-06-11"
---

`ActionConfig` is the payload object you include as `action_config` in `POST /connect` to declare the physical affordances for the session.

## ActionConfig

| Field | Type | Required | Description |
|---|---|---|---|
| `actions` | array of strings | No | The action verbs the character is allowed to perform. Each item is a plain string in the request JSON; the server normalizes them internally. Absent or empty means no actions are enabled. |
| `objects` | array of `ActionObjectConfig` | No | The scene objects the character can target with actions. |
| `characters` | array of `ActionCharacterConfig` | No | The characters the bot can target with actions such as `"Follow"`. |
| `current_attention_object` | string or `ActionObjectConfig` | No | The object currently in focus. Accepts an object name string (resolved against the `objects` list) or a full object payload. Must match a `name` in `objects` when set. Send an empty string in a `context-update` message to clear it. |

### ActionConfig behavior notes

- The server normalizes `actions` entries: you submit plain strings in the request body and they are stored internally as `Action` objects with a `value` field. The original strings are returned verbatim in `action-response` events.
- `current_attention_object` set at connect time initializes the pronoun-resolution context for the first turn.
- All fields are optional. A session with no `actions` and no `objects` will not produce useful action output.

## ActionObjectConfig

`ActionObjectConfig` is used in the `objects` array and is also accepted as the full-payload form of `current_attention_object`.

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | A unique, human-readable identifier for the object. Referenced by `action-response.actions[].target` and by `current_attention_object`. |
| `description` | string | Yes | A short description of the object's current state or position. Used by the language model when generating action output and spoken responses. |

### Constraints

- `name` values must be unique within the `objects` list.
- `current_attention_object` must resolve to one of the declared `name` values.
- If a target object is removed from the scene, stop sending it as `current_attention_object` or reconnect with an updated `action_config` if its removal changes the allowed action target set.

## ActionCharacterConfig

`ActionCharacterConfig` is used in the `characters` array.

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | A unique identifier for the character. Referenced by `action-response.actions[].target` when an action targets a person rather than an object. |
| `bio` | string | Yes | A short description of the character's role or relationship to the scene. |

## Request JSON shape

In the `/connect` request body, `action_config` is serialized as shown below. The `actions` array contains plain strings.

```json
{
  "action_config": {
    "actions": ["Move To", "Pick Up", "Drop", "Follow"],
    "objects": [
      { "name": "cube",  "description": "A red cube on the table" },
      { "name": "lever", "description": "A metal lever on the wall" }
    ],
    "characters": [
      { "name": "Player", "bio": "The current user" }
    ],
    "current_attention_object": "cube"
  }
}
```

{% content-ref url="configure-actions.md" %}
[Configure actions on connect](configure-actions.md)
{% endcontent-ref %}

{% content-ref url="action-response-reference.md" %}
[action-response reference](action-response-reference.md)
{% endcontent-ref %}
