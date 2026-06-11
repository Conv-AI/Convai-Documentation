---
title: Authenticate to the Realtime API
description: Authenticate Realtime API requests using an API key or session token, covering header names, resolution order, and unauthenticated endpoints.
last_reviewed: "2026-06-11"
---

The Realtime API authenticates every request using one of two HTTP request headers. Pass your Convai API key directly in `X-API-Key`, or pass an active session token in `API-AUTH-TOKEN` that Convai resolves to its associated API key. If neither header is present, the server returns `401`.

## Authentication headers

| Header | Value type | When to use | Description |
|---|---|---|---|
| `X-API-Key` | API key string | Primary method for server-side integrations | Your Convai API key. Obtain it from the Convai dashboard under **Account Settings**. |
| `API-AUTH-TOKEN` | Session UUID string | When the caller holds an active session token but not the raw API key | A `session_id` value returned by a previous `POST /connect` response. Convai looks up the active session and uses its associated API key. The session must still be active — that is, it must not have expired or been disconnected. |

## Precedence

The server evaluates headers in this order:

1. If `X-API-Key` is present, use it directly as the API key.
2. If `API-AUTH-TOKEN` is present, resolve it to an API key by looking up the active session record.
3. If neither header is present, return `401` with the message `Authentication required: provide X-API-Key or API-AUTH-TOKEN`.

When both headers are present, `X-API-Key` takes precedence and `API-AUTH-TOKEN` is ignored.

## Endpoints that do not require authentication

`POST /disconnect` and `GET /healthz` accept requests without any authentication header. The `/chat` WebSocket endpoint does not use authentication headers — it relies on the `session_id` query parameter that was issued by an authenticated `POST /connect` call.

{% hint style="danger" %}
Never expose your `X-API-Key` value in client-side JavaScript, public repositories, or any environment reachable by untrusted parties. An exposed API key grants access to your full Convai account. Treat it as a secret and rotate it immediately if it is compromised.
{% endhint %}

## Connect with an API key

The minimum authenticated request to `POST /connect` (base URL: <code class="expression">space.vars.live_server_url</code>):

```bash
curl -X POST https://live.convai.com/connect \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"character_id": "CHARACTER_ID"}'
```

## Next steps

{% content-ref url="quick-start.md" %}
[Connect your first character](quick-start.md)
{% endcontent-ref %}

{% content-ref url="error-codes.md" %}
[HTTP error codes](error-codes.md)
{% endcontent-ref %}
