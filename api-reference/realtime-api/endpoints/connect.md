---
title: POST /connect
description: Reference for the realtime connect endpoint: method, URL, authentication headers, request and response shapes, and all HTTP status codes.
last_reviewed: "2026-06-11"
---

`POST /connect` creates a new realtime session for a Convai character. Convai provisions a transport room, spawns a conversation agent, and returns the credentials the client uses to join. Call this endpoint once per conversation session before connecting a LiveKit, Daily, or WebSocket client.

## Endpoint

**`POST`** <code class="expression">space.vars.live_server_url</code>`/connect`

`Content-Type: application/json`

## Authentication

Every request must carry one of the following headers:

| Header | Value | Notes |
|---|---|---|
| `X-API-Key` | Your Convai API key | Preferred for server-to-server calls |
| `API-AUTH-TOKEN` | An active session token (UUID string) | Server resolves the token to its originating API key |

If neither header is present, the server returns `401 Unauthorized`. See [Authenticate to the Realtime API](../authentication.md) for full details.

## Request

Send a JSON body matching the [ConnectRequest](connect-request-reference.md) schema. Only `character_id` is required; all other fields use their defaults when omitted.

**Minimum request body:**

```json
{
  "character_id": "YOUR_CHARACTER_ID"
}
```

See [ConnectRequest field reference](connect-request-reference.md) for every field, its type, default, and constraints.

## Response

A `200 OK` response returns a JSON body matching the [ConnectResponse](connect-response-reference.md) schema.

**Example response (LiveKit transport):**

```json
{
  "session_id": "a1b2c3d4-e29b-41d4-a716-446655440000",
  "request_trace_id": "req_abc123def456",
  "character_session_id": "f7a8b9c0-e29b-41d4-a716-446655440001",
  "room_url": "https://live.convai.com",
  "room_name": "conversation-room-xyz",
  "token": "<livekit-participant-jwt>",
  "end_user_id": null,
  "end_user_metadata": null
}
```

Pass `room_name` and `token` to your LiveKit client SDK. For the WebSocket transport, connect directly to `room_url`. Save `character_session_id` if you intend to resume the conversation in a future session.

## Error codes

Each error response includes a `detail` field with a human-readable message. Use the HTTP status code for programmatic handling. The error category column is a stable documentation label for each condition.

| HTTP status | Error category | Condition | Recovery |
|---|---|---|---|
| `422` | `bad_request` | Request body failed schema validation | Correct the field identified in `detail` |
| `400` | `missing_end_user_id` | Character has Long Term Memory enabled and `end_user_id` was omitted | Include `end_user_id` in the request body |
| `401` | `invalid_api_key` | Authentication header is missing or rejected | Verify the `X-API-Key` or `API-AUTH-TOKEN` value |
| `403` | `realtime_access_denied` | Account plan does not include realtime access | Review your plan or contact support |
| `403` | `session_forbidden` | The supplied `character_session_id` belongs to a different account | Do not pass session IDs owned by other accounts |
| `404` | `character_not_found` | No character with the given `character_id` is visible to this API key | Confirm the character is owned by or publicly listed under this account |
| `404` | `session_not_found` | The supplied `character_session_id` does not exist | Omit `character_session_id` to start a fresh conversation |
| `409` | `shared_session_conflict` | Room state conflict when resolving a shared session | See [Shared sessions](shared-sessions.md) for conflict handling |
| `429` | `concurrency_limit` | Active session count exceeds the plan limit | Wait for sessions to close, then retry |
| `429` | `speaker_limit` | Plan end-user speaker count has been reached | Contact support to review limits |
| `500` | `internal_error` | Unhandled server error | Retry with exponential backoff; open a support ticket if the error recurs |
| `503` | `database_unavailable` | Convai cannot reach its database | Retry after a short delay |

## Usage example

A corporate onboarding application starts a new session for an employee interacting with a training character.

{% tabs %}
{% tab title="curl" %}
```bash
curl -X POST $LIVE_SERVER_URL/connect \
  -H 'X-API-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "character_id": "YOUR_CHARACTER_ID",
    "end_user_id": "employee-2947",
    "end_user_metadata": { "name": "Jordan" },
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
        "end_user_id": "employee-2947",
        "end_user_metadata": {"name": "Jordan"},
        "mode": "create",
    },
)
data = response.json()
room_name = data["room_name"]
token = data["token"]
character_session_id = data["character_session_id"]
```
{% endtab %}
{% endtabs %}

On success, use `room_name` and `token` to connect your LiveKit client.

## Next steps

{% content-ref url="connect-request-reference.md" %}
[ConnectRequest field reference](connect-request-reference.md)
{% endcontent-ref %}

{% content-ref url="connect-response-reference.md" %}
[ConnectResponse field reference](connect-response-reference.md)
{% endcontent-ref %}

{% content-ref url="shared-sessions.md" %}
[Shared sessions](shared-sessions.md)
{% endcontent-ref %}

{% content-ref url="resume-conversation.md" %}
[Resume a conversation](resume-conversation.md)
{% endcontent-ref %}
