---
title: Resume a conversation
description: Resume a previous character conversation by passing a prior session identifier, restoring chat history and conversation state for the new session.
last_reviewed: "2026-06-11"
---

Passing a `character_session_id` from a previous session to `POST /connect` tells Convai to load the prior conversation history and inject it into the new session's context. The character remembers what was said in the original session and continues from that point.

## Prerequisites

- A `character_session_id` value from a previous successful `/connect` call.
- The API key used for the new call must be the same account that owned the original session.

## Save the session identifier after connect

Every `/connect` response includes a `character_session_id`. Store this value in your application if you plan to resume the conversation.

```json
{
  "character_session_id": "f7a8b9c0-e29b-41d4-a716-446655440001"
}
```

Save it against the end user or context in your own data store. The identifier is a UUID string.

## Pass the identifier on the next connect call

Include `character_session_id` in the request body of the new `/connect` call.

```json
{
  "character_id": "YOUR_CHARACTER_ID",
  "character_session_id": "f7a8b9c0-e29b-41d4-a716-446655440001",
  "end_user_id": "trainee-42"
}
```

The server fetches the conversation history associated with `character_session_id`, validates ownership, and injects the messages into the new session.

## Understand mode behavior

The `mode` field controls room creation, not conversation history. Set `mode` to `"create"` (the default) for most resume scenarios — this starts a new room while restoring the conversation thread.

| `mode` | Effect |
|---|---|
| `"create"` | Creates a new room. Conversation history is loaded from `character_session_id`. |
| `"join"` | Joins an existing room identified by `shared_session_key` or `room_name`. |

Resuming history does not require `mode="join"`. Use `mode="join"` only when you want to join a specific shared room.

## Handle errors during resume

| Error | Cause | Fix |
|---|---|---|
| `404 session_not_found` | The `character_session_id` does not exist in Convai's records | Verify the value was saved correctly; omit it to start a fresh session |
| `403 session_forbidden` | The session belongs to a different account | Use the API key that created the original session |

## Full example

An industrial safety training application resumes a conversation from a previous shift so the character recalls the earlier assessment.

{% tabs %}
{% tab title="curl" %}
```bash
curl -X POST $LIVE_SERVER_URL/connect \
  -H 'X-API-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "character_id": "YOUR_CHARACTER_ID",
    "character_session_id": "f7a8b9c0-e29b-41d4-a716-446655440001",
    "end_user_id": "technician-88",
    "mode": "create"
  }'
```
{% endtab %}
{% tab title="Python" %}
```python
import requests

response = requests.post(
    "$LIVE_SERVER_URL/connect",
    headers={
        "X-API-Key": "YOUR_API_KEY",
        "Content-Type": "application/json",
    },
    json={
        "character_id": "YOUR_CHARACTER_ID",
        "character_session_id": "f7a8b9c0-e29b-41d4-a716-446655440001",
        "end_user_id": "technician-88",
        "mode": "create",
    },
)
data = response.json()
# New session, same conversation thread
new_session_id = data["session_id"]
```
{% endtab %}
{% endtabs %}

## Next steps

{% content-ref url="connect-request-reference.md" %}
[ConnectRequest field reference](connect-request-reference.md)
{% endcontent-ref %}

{% content-ref url="connect-response-reference.md" %}
[ConnectResponse field reference](connect-response-reference.md)
{% endcontent-ref %}

{% content-ref url="../identifiers.md" %}
[Session and character identifiers](../identifiers.md)
{% endcontent-ref %}
