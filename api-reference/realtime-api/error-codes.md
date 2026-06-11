---
title: HTTP error codes
description: Reference for all error codes, their HTTP status mappings, WebSocket close codes, and the JSON error response shape returned by the Realtime API.
last_reviewed: "2026-06-11"
---

The Realtime API returns standard HTTP status codes on all REST endpoints. Most error responses carry a `detail` string that describes the problem; HTTP 422 validation errors carry a `detail` array of per-field error objects instead. Convai also assigns a stable `error_code` string to every response for use in logs and telemetry — the table below maps each code to its HTTP status and the conditions that produce it.

## ErrorCode values

| `error_code` | HTTP status | Description | When returned |
|---|---|---|---|
| `none` | 200 | No error; the request succeeded. | All successful responses. |
| `bad_request` | 400 | The request body contains a field with an invalid value or format. | Malformed `session_id` UUID on `POST /disconnect`, or other request-body validation failures. Note: field-level enum or type constraint violations (such as an unsupported `transport` value) return HTTP 422 instead. |
| `missing_end_user_id` | 400 | `end_user_id` is required but was not provided. | `POST /connect` when the character has Long Term Memory enabled and `end_user_id` is absent from the request body. |
| `invalid_api_key` | 401 | The API key could not be verified. | `X-API-Key` is invalid, `API-AUTH-TOKEN` refers to an expired or unknown session, or neither header is present. |
| `realtime_access_denied` | 403 | The account plan does not include realtime access. | `POST /connect` when the `realtime_access` flag is not enabled for the API key's plan. |
| `session_forbidden` | 403 | The `character_session_id` provided for conversation resumption belongs to a different user. | `POST /connect` when the supplied `character_session_id` is owned by a different account. |
| `character_not_found` | 404 | The character does not exist, is not owned by the user, or is not publicly accessible. | `POST /connect` with a `character_id` the authenticated user cannot access. |
| `session_not_found` | 404 | The `character_session_id` supplied for resumption was not found. | `POST /connect` when the specified `character_session_id` does not exist in the database. |
| `shared_session_conflict` | 409 | A conflict occurred during shared-session room resolution. | `POST /connect` with `shared_session_key` when a room-state conflict is detected. |
| `concurrency_limit` | 429 | The account has reached its concurrent session limit. | `POST /connect` when the number of active sessions equals the plan's concurrency limit. |
| `speaker_limit` | 429 | The unique end-user speaker limit for the account has been reached. | `POST /connect` when the plan's speaker count limit is exceeded. |
| `database_unavailable` | 503 | Convai cannot reach its database. The error is transient. | Any endpoint when the database is temporarily unreachable. Retry with exponential back-off. |
| `internal_error` | 500 | An unexpected server error occurred. | Any endpoint on an unhandled exception. |

## WebSocket close codes

The `/chat` WebSocket endpoint closes the connection with one of these codes when a non-recoverable error occurs.

| Code | Meaning | When used |
|---|---|---|
| `1008` | Policy violation | Session not found in the database or cache, session expired, session transport mismatch (non-WebSocket session connected to `/chat`), duplicate active WebSocket for the session, character no longer accessible, or user authentication failed during a database fallback. |
| `1011` | Internal error | Unhandled exception during session processing, or session cache data is incomplete after a cache miss and the database fallback cannot reconstruct it. |

## Validation errors (HTTP 422)

Field-level validation failures — such as submitting an unsupported `transport` value — return HTTP `422 Unprocessable Entity`. The response body is different from the `HTTPException` shape: `detail` is an array of per-field error objects rather than a plain string.

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "transport"],
      "msg": "Value error, Invalid transport: sse",
      "input": "sse"
    }
  ]
}
```

## Error response format

All Realtime API endpoints return errors in the following JSON format:

```json
{
  "detail": "<human-readable error description>"
}
```

For example, an invalid API key produces:

```json
{
  "detail": "Invalid API key"
}
```

A missing `end_user_id` on a character with Long Term Memory enabled produces:

```json
{
  "detail": "Missing end_user_id. end_user_id is required when the character has Long Term Memory enabled. Provide end_user_id or disable Long Term Memory."
}
```

{% hint style="info" %}
`POST /disconnect` never returns an error for an unknown `session_id`. When the session does not exist, the endpoint returns `{"status": "success", "message": "Session disconnected successfully"}` with HTTP `200`. This makes disconnect calls safely idempotent — you can call it multiple times without risk.
{% endhint %}

## Next steps

{% content-ref url="authentication.md" %}
[Authenticate to the Realtime API](authentication.md)
{% endcontent-ref %}

{% content-ref url="identifiers.md" %}
[Session and character identifiers](identifiers.md)
{% endcontent-ref %}
