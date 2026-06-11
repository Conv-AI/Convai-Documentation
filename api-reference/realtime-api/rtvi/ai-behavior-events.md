---
title: AI behavior events
description: Reference for behavior-tree-response, moderation-response, and bot-emotion — payload fields, when each fires, and how to apply them in your avatar.
last_reviewed: "2026-06-11"
---

AI behavior events expose the bot's higher-level reasoning outputs. Use them to drive character behavior trees, apply content moderation policies, and animate emotional states on your avatar.

## `behavior-tree-response`

Sent when the bot returns a behavior tree response during a turn. The payload contains the behavior tree code, its constants, and the current narrative section identifier. Use these to drive programmatic character behavior in your application.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "behavior-tree-response",
    "bt_code": "...",
    "bt_constants": "...",
    "narrative_section_id": "section_1"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"behavior-tree-response"`. |
| `bt_code` | string | Behavior tree code for the bot's current action plan. |
| `bt_constants` | string | Constants used by the behavior tree. |
| `narrative_section_id` | string | Identifier for the current section in the narrative template. |

**Recommended action:** Parse `bt_code` and `bt_constants` with your behavior tree engine and execute the specified behavior. Use `narrative_section_id` to track narrative progression.

## `moderation-response`

Sent when the content moderation system has evaluated user input. This event fires regardless of whether the content passes or is blocked.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "moderation-response",
    "result": false,
    "user_input": "the flagged content",
    "reason": "Inappropriate language"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"moderation-response"`. |
| `result` | boolean | `true` if the content passed moderation and was forwarded to the bot; `false` if the content was blocked. |
| `user_input` | string | The user input that was evaluated. |
| `reason` | string \| null | Reason the content was blocked. `null` when `result` is `true`; a non-null string when `result` is `false`. Always present in the payload. |

**Recommended action:** When `result` is `false`, optionally show feedback to the user. Avoid exposing the raw `reason` string to end users in production — use it for logging and to build a user-friendly message instead.

## `bot-emotion`

Sent during a turn to indicate the bot's current emotional state. Use this to trigger the corresponding expression or animation on your avatar.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "bot-emotion",
    "emotion": "happy",
    "scale": 2
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"bot-emotion"`. |
| `emotion` | string | The emotion name, for example `"happy"`, `"sad"`, `"angry"`, `"excited"`, or `"neutral"`. The set of possible values depends on the character configuration. |
| `scale` | integer | Intensity of the emotion. `1` = subtle, `2` = moderate, `3` = intense. |

**Scale values:**

| Value | Meaning |
|---|---|
| `1` | Subtle — light emotional coloring. |
| `2` | Moderate — clearly expressed emotion. |
| `3` | Intense — strong emotional expression. |

**Recommended action:** Map `emotion` to the corresponding avatar expression or blend shape blend, then weight the expression by `scale` to produce proportional intensity.

## Related pages

{% content-ref url="server-events.md" %}
[Server events overview](server-events.md)
{% endcontent-ref %}

{% content-ref url="turn-events.md" %}
[Turn events](turn-events.md)
{% endcontent-ref %}
