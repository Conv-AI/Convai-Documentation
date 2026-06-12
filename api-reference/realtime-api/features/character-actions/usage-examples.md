---
title: Character actions usage examples
description: "Two complete integration scenarios for character actions: an object-interaction training simulation and a session with attention tracking updates."
last_reviewed: "2026-06-11"
---

The examples below show end-to-end character action flows for two scenarios. Each scenario covers the `/connect` payload, runtime updates, and the resulting `action-response` events your client receives.

## Scenario 1: Training simulation with object interaction

A safety-training application has a character that can move to, pick up, and drop objects in a warehouse scene. The user gives verbal instructions and the character performs an ordered sequence of physical actions.

### Connect with action_config

```json
{
  "character_id": "00000000-0000-0000-0000-000000000000",
  "invocation_source": "unity_sdk",
  "action_config": {
    "actions": ["Move To", "Pick Up", "Drop", "Follow"],
    "objects": [
      {
        "name": "apple",
        "description": "A green apple on the crate"
      },
      {
        "name": "basket",
        "description": "A wicker basket near the player"
      }
    ],
    "characters": [
      {
        "name": "Player",
        "bio": "The current user"
      }
    ],
    "current_attention_object": "apple"
  }
}
```

### User sends a request

The user says: "Pick that up and bring it to me."

Because `current_attention_object` is `"apple"`, the server resolves `"that"` and `"it"` to `"apple"`, and `"me"` to `"Player"`.

### Server emits action-response

```json
{
  "type": "action-response",
  "actions": [
    { "name": "Move To",  "target": "apple"  },
    { "name": "Pick Up",  "target": "apple"  },
    { "name": "Move To",  "target": "Player" },
    { "name": "Drop",     "target": "apple"  }
  ]
}
```

Your client dispatches these four actions in order: move to the apple, pick it up, move to the player, then drop the apple.

### Update attention when focus changes

When the user looks at the basket, send a `context-update` to shift the attention object:

```json
{
  "type": "context-update",
  "data": {
    "mode": "append",
    "run_llm": "false",
    "current_attention_object": "basket"
  }
}
```

Subsequent pronoun references now resolve to `"basket"` instead of `"apple"`.

## Scenario 2: Onboarding assistant with attention tracking

A corporate onboarding experience has an assistant character that guides a new employee through a virtual office. The environment changes as the user moves between areas, and the assistant tracks which item the user is currently looking at.

### Connect with initial configuration

No initial `current_attention_object` is set because the user has not focused on a specific object yet.

```json
{
  "character_id": "00000000-0000-0000-0000-000000000000",
  "invocation_source": "web_sdk",
  "action_config": {
    "actions": ["Move To", "Point At", "Open"],
    "objects": [
      {
        "name": "reception_desk",
        "description": "The main reception desk at the building entrance"
      },
      {
        "name": "badge_printer",
        "description": "The badge printer on the reception desk"
      },
      {
        "name": "elevator",
        "description": "The elevator on the right side of the lobby"
      }
    ],
    "characters": [
      {
        "name": "Employee",
        "bio": "The new employee being onboarded"
      }
    ]
  }
}
```

### Send descriptive context as the user moves

As the user walks to the badge printer area, send a scene update describing its current state. This lets the character speak about the printer accurately, without granting any new action affordances.

```json
{
  "type": "update-scene-metadata",
  "data": {
    "scene_metadata": [
      {
        "name": "badge_printer",
        "description": "The badge printer is showing a ready light. The paper tray is loaded."
      }
    ]
  }
}
```

### Update attention when the user focuses on the printer

```json
{
  "type": "context-update",
  "data": {
    "text": "The employee is now standing in front of the badge printer.",
    "mode": "append",
    "run_llm": "auto",
    "current_attention_object": "badge_printer"
  }
}
```

### User asks a question and requests an action

The user says: "How do I use this? Can you show me?"

With `current_attention_object` set to `"badge_printer"`, the server resolves `"this"` to the printer and may emit:

```json
{
  "type": "action-response",
  "actions": [
    { "name": "Move To",  "target": "badge_printer" },
    { "name": "Point At", "target": "badge_printer" }
  ]
}
```

Your client moves the character to the printer and plays a pointing animation targeting the badge printer entity.

{% content-ref url="how-character-actions-work.md" %}
[How character actions work](how-character-actions-work.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot character actions](troubleshooting.md)
{% endcontent-ref %}
