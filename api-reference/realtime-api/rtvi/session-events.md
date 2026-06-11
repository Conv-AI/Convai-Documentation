---
title: Session events
description: Reference for interaction-created, usage-limit-reached, and user-idle-warning server events — payload fields, when each fires, and recommended client actions.
last_reviewed: "2026-06-11"
---

Session events fire at the session level rather than during a specific turn. They signal lifecycle milestones, quota conditions, and idle-timeout warnings.

## `interaction-created`

Sent early in the session lifecycle when an interaction ID is assigned. Store the `interaction_id` for analytics, logging, or support requests.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "interaction-created",
    "interaction_id": "int_abc123def456",
    "character_session_id": "cs_xyz789"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"interaction-created"`. |
| `interaction_id` | string | Unique identifier for this interaction. Use this in support tickets and analytics. |
| `character_session_id` | string | Character session identifier. Matches the `character_session_id` in the `/connect` response when the session was previously created. |

**Recommended action:** Store `interaction_id` for debugging and session tracking.

## `usage-limit-reached`

Sent when the account or session has exceeded a usage quota. The session cannot continue after this event.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "usage-limit-reached",
    "quota_type": "minutes",
    "message": "You have exceeded your monthly quota"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"usage-limit-reached"`. |
| `quota_type` | string | The type of quota that was exceeded. Values are set at runtime; examples include `"minutes"` and `"api_calls"`. |
| `message` | string | Human-readable explanation of the limit. Display this to the user or log it for support. |

**Recommended action:** Show the `message` to the user, end the session gracefully, and direct the user to upgrade their plan if appropriate.

{% hint style="info" %}
The `quota_type` values are set at runtime by the server. Contact Convai support if you need to handle specific quota types programmatically.
{% endhint %}

## `user-idle-warning`

Sent when the user has been idle in the session for a period. The event indicates how many seconds remain before the server disconnects the session. Sending any RTVI message — including `reset-idle-timer` — resets the idle counter.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "user-idle-warning",
    "remaining_seconds": 300,
    "message": "You've been idle. You will be disconnected in 5 minutes."
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"user-idle-warning"`. |
| `remaining_seconds` | integer | Seconds remaining before the server closes the session due to inactivity. |
| `message` | string \| null | Optional human-readable warning. May be shown directly to the user. |

**Recommended action:** Display the warning in the UI and prompt the user to interact. To reset the timer without triggering bot speech, send a `reset-idle-timer` client message.

## Related pages

{% content-ref url="server-events.md" %}
[Server events overview](server-events.md)
{% endcontent-ref %}

{% content-ref url="../core-concepts/session-lifecycle.md" %}
[Session lifecycle](../core-concepts/session-lifecycle.md)
{% endcontent-ref %}
