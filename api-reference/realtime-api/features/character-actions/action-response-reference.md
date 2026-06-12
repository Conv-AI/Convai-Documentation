---
title: action-response reference
description: "Reference for the action-response server event: actions array fields, empty-array no-op behavior, multi-action sequencing, and the RTVI envelope."
last_reviewed: "2026-06-11"
---

`action-response` is a server event that Convai emits on conversation turns where the character should perform one or more physical actions. It carries a structured array of action objects that your client executes in order.

## Full RTVI envelope

`action-response` is delivered inside the standard RTVI server-message envelope.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "action-response",
    "actions": [
      {
        "name": "Move To",
        "target": "cube"
      },
      {
        "name": "Pick Up",
        "target": "cube"
      }
    ]
  }
}
```

## Inner data payload

```json
{
  "type": "action-response",
  "actions": [
    {
      "name": "Move To",
      "target": "cube"
    },
    {
      "name": "Pick Up",
      "target": "cube"
    }
  ]
}
```

## Fields

### action-response top-level fields

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"action-response"`. |
| `actions` | array of action objects | The ordered list of actions for the character to perform. Empty when no action is appropriate for the turn. |

### Action object fields

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | The action verb. Matches one of the strings declared in `action_config.actions` at connect time. |
| `target` | string | No | The name of the object or character the action applies to. Matches a `name` from `action_config.objects` or `action_config.characters`. Omitted when the action has no target. |

## No-action turns

When no action is appropriate — because the user's request is conversational, impossible, unsupported, non-physical, or the character verbally declines — Convai emits `action-response` with an empty `actions` array.

```json
{
  "type": "action-response",
  "actions": []
}
```

Your client must treat `[]` as a valid no-op. Do not check for the legacy string `"None"`; it is no longer emitted.

## Multi-action sequences

A single turn can produce multiple actions. Execute them in the order they appear in the array.

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

In this example, the character moves to the apple, picks it up, moves to the player, then drops the apple. Executing actions out of order produces undefined behavior in your scene.

## Dispatch guidance

When you receive an `action-response`:

1. Iterate the `actions` array in order.
2. For each action, look up `name` in your client's action dispatcher.
3. If `target` is present, resolve it against your local object or character map.
4. Execute the action. Wait for completion before starting the next one if your executor requires sequential dispatch.

Maintain a local map from each object `name` (as declared in `action_config.objects`) to your runtime entity so `target` values can be resolved without additional lookup at dispatch time.

{% content-ref url="action-config-reference.md" %}
[ActionConfig field reference](action-config-reference.md)
{% endcontent-ref %}

{% content-ref url="update-scene-and-attention.md" %}
[Update scene context and attention](update-scene-and-attention.md)
{% endcontent-ref %}
