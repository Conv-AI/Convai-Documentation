---
title: Configure actions on connect
description: Set up action configuration on connect so a character knows which actions, objects, and characters are available in the current session.
last_reviewed: "2026-06-11"
---

To enable character actions, include an `action_config` object in the body of your `POST /connect` request. Without it, Convai behaves as a conversational-only character and does not emit `action-response` events.

## Prerequisites

- An active Convai API key. See [Authenticate to the Realtime API](../../authentication.md).
- A `POST /connect` call in your client. See [POST /connect](../../endpoints/connect.md).
- A list of the action verbs, objects, and characters your scene supports.

## Define the allowed actions

List the action verbs the character may use. Each item in the `actions` array is a plain string.

```json
"actions": ["Move To", "Pick Up", "Drop", "Follow"]
```

Use human-readable verb phrases that match the commands your client executor understands. The server passes these strings back verbatim in `action-response` events.

## Define the scene objects

List the objects the character is allowed to act on. Each object requires a `name` and a `description`.

```json
"objects": [
  {
    "name": "cube",
    "description": "A red cube on the table"
  },
  {
    "name": "lever",
    "description": "A metal lever on the wall"
  }
]
```

Object names must be unique within the list. Use stable, human-readable names because `action-response` events reference objects by name and your client must resolve them to scene entities.

## Define the scene characters

List the characters the model may target. Each entry requires a `name` and a `bio`.

```json
"characters": [
  {
    "name": "Player",
    "bio": "The current user"
  },
  {
    "name": "Guard",
    "bio": "A nearby guard NPC"
  }
]
```

## Set the initial attention object

`current_attention_object` tells the server which object the user is currently focused on. It must match one of the `name` values in `objects`. You can also pass the full object payload instead of a name string; the server resolves both forms against the `objects` list.

```json
"current_attention_object": "cube"
```

## Complete example

The following payload includes all four fields and is ready to submit as part of your `/connect` body.

```json
{
  "character_id": "00000000-0000-0000-0000-000000000000",
  "invocation_source": "web_sdk",
  "action_config": {
    "actions": ["Move To", "Pick Up", "Drop", "Follow"],
    "objects": [
      {
        "name": "cube",
        "description": "A red cube on the table"
      },
      {
        "name": "lever",
        "description": "A metal lever on the wall"
      }
    ],
    "characters": [
      {
        "name": "Player",
        "bio": "The current user"
      },
      {
        "name": "Guard",
        "bio": "A nearby guard NPC"
      }
    ],
    "current_attention_object": "cube"
  }
}
```

## Verify the setup

After connecting, speak or send a message that requests a physical action on one of the configured objects. Convai should respond with both spoken output and an `action-response` event containing a non-empty `actions` array.

If no `action-response` event arrives, confirm that `action_config` was included in the `/connect` body. A session established without `action_config` will not emit action events. See [Troubleshoot character actions](troubleshooting.md) for additional diagnostics.

## What to do when affordances change

If your scene changes so that different objects or actions should be available, you must reconnect with an updated `action_config`. Sending `update-scene-metadata` after connect does not modify the authoritative affordance set.

{% content-ref url="update-scene-and-attention.md" %}
[Update scene context and attention](update-scene-and-attention.md)
{% endcontent-ref %}

{% content-ref url="action-config-reference.md" %}
[ActionConfig field reference](action-config-reference.md)
{% endcontent-ref %}
