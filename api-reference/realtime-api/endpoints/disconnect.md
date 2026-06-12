---
title: POST /disconnect
description: "Reference for POST /disconnect: query parameters, authentication requirements, response format, and the security risk of unauthenticated session teardown."
last_reviewed: "2026-06-11"
---

`POST /disconnect` ends an active realtime session. Convai invalidates the session cache and clears the active WebSocket marker for the given `session_id`. Call this endpoint after a conversation ends to release session resources promptly.

## Endpoint

**`POST`** <code class="expression">space.vars.live_server_url</code>`/disconnect`

## Authentication

No authentication header is required or accepted. The `session_id` query parameter is the only credential for this endpoint.

{% hint style="warning" %}
Any caller who knows a `session_id` can terminate that session. Treat session identifiers as secrets: do not log them, expose them in client-side code, or embed them in URLs accessible to untrusted parties.
{% endhint %}

## Request

**Query parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `session_id` | string (UUID) | Yes | The session identifier returned in the `session_id` field of the `/connect` response |

No request body is required.

## Response

A structurally valid request always returns `HTTP 200`, including when the session is not found. Convai treats a session that no longer exists as already disconnected.

```json
{
  "status": "success",
  "message": "Session disconnected successfully"
}
```

## Error codes

| HTTP status | Condition | Recovery |
|---|---|---|
| `400` | `session_id` is not a valid UUID string — `detail: "Invalid session ID format"` | Pass the exact UUID string returned by `/connect` |
| `500` | Unexpected server error | Retry with exponential backoff; open a support ticket if the error recurs |

## Usage example

A corporate onboarding application sends a disconnect request when an employee exits a training conversation.

{% tabs %}
{% tab title="curl" %}
```bash
curl -X POST $LIVE_SERVER_URL/disconnect?session_id=$SESSION_ID
```
{% endtab %}
{% tab title="Python" %}
```python
import requests

response = requests.post(
    f"{LIVE_SERVER_URL}/disconnect",
    params={"session_id": SESSION_ID},
)
print(response.json())
# {"status": "success", "message": "Session disconnected successfully"}
```
{% endtab %}
{% endtabs %}

A `200` response with `"status": "success"` confirms the session has been torn down.

## Next steps

{% content-ref url="connect.md" %}
[POST /connect](connect.md)
{% endcontent-ref %}

{% content-ref url="chat-websocket.md" %}
[WebSocket /chat](chat-websocket.md)
{% endcontent-ref %}
