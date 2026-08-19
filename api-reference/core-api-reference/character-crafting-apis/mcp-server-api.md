---
description: >-
  Register MCP servers, connect them with static headers or OAuth, and attach
  them to characters programmatically.
---

# MCP Server API

Manage MCP servers programmatically. Everything available in the Playground's MCP tab is also available over HTTP: registering servers, testing connections, connecting OAuth accounts, and attaching servers to characters.

For what MCP servers are and how characters use them, see MCP Servers.

Typical flow:

1. Probe the endpoint with `/mcp/servers/test`
2. Register it with `/mcp/servers/create`
3. For OAuth servers: `/mcp/oauth/start`, open the returned URL in a browser, then poll `/mcp/oauth/status`
4. Attach it to a character with `/mcp/characters/attach`

## Conventions

* **Base URL:** `https://api.convai.com/mcp`
* All endpoints use **POST** with a JSON body (`Content-Type: application/json`), including reads. The only exception is the OAuth browser callback, which you never call directly.
* **Auth:** pass your API key in the `CONVAI-API-KEY` header. Every request is scoped to your account: you can only see and modify your own servers and characters.
* **Errors** return a JSON envelope with an appropriate status code:

```json
{ "ERROR": "name: Field required" }
```

| Status | Meaning                                                            |
| ------ | ------------------------------------------------------------------ |
| 400    | Invalid request body. The message names the failing field.         |
| 401    | Missing or invalid API key.                                        |
| 404    | The referenced server or character doesn't exist (or isn't yours). |
| 429    | Rate limit exceeded (100 requests/minute per endpoint).            |
| 500    | Internal error. Safe to retry.                                     |

## The server object

```json
{
  "server_id": "15e08050-2952-4380-8dfa-41242edbbcfe",
  "name": "order-lookup",
  "description": "Order status tools for support characters",
  "url": "https://mcp.example.com/mcp",
  "transport": "streamable_http",
  "auth_type": "headers",
  "auth_headers": { "Authorization": "Bearer sk-..." },
  "header_names": ["Authorization"],
  "tools_allowlist": ["lookup_order", "cancel_order"],
  "timeout_s": 30,
  "result_max_chars": null,
  "enabled": true,
  "created_at": "2026-08-19T09:18:44.783437"
}
```

* `auth_type`: `headers` (static headers, the default) or `oauth` (see [OAuth connections](mcp-server-api.md#oauth-connections)).
* `auth_headers` contains the stored header values, returned only to the owning account. `header_names` is the same set as names only, kept for compatibility. OAuth tokens are **never** returned by any endpoint.
* `tools_allowlist`: `null` = all tools the server exposes; a list = only those tools; `[]` = no tools.
* `timeout_s` / `result_max_chars`: `null` = platform default (30 s / 4,000 characters).

## Server endpoints

### List servers

<mark style="color:green;">`POST`</mark> `https://api.convai.com/mcp/servers/list` with body `{}`. Returns all servers on your account, newest first.

```json
{ "servers": [ { ...server object... } ] }
```

### Create a server

<mark style="color:green;">`POST`</mark> `https://api.convai.com/mcp/servers/create`

| Field              | Required | Constraints                                                                         |
| ------------------ | -------- | ----------------------------------------------------------------------------------- |
| `name`             | yes      | 1–120 characters                                                                    |
| `url`              | yes      | HTTPS, ≤ 2048 characters, full MCP endpoint path (typically ending in `/mcp`)       |
| `description`      | no       | ≤ 2000 characters                                                                   |
| `transport`        | no       | `streamable_http` (default) or `sse`                                                |
| `auth_type`        | no       | `headers` (default) or `oauth`                                                      |
| `auth_headers`     | no       | object of header name → value; ≤ 20 headers, names ≤ 120 chars, values ≤ 8192 chars |
| `tools_allowlist`  | no       | array of tool names; ≤ 200 entries, names ≤ 128 chars; omit for all tools           |
| `timeout_s`        | no       | integer 1–300                                                                       |
| `result_max_chars` | no       | integer 100–100000                                                                  |

Returns `{ "server": { ... } }`. Header values are encrypted at rest.

### Update a server

<mark style="color:green;">`POST`</mark> `https://api.convai.com/mcp/servers/update` with body `{ "server_id": "...", ...fields to change }`.

Partial update: omitted fields are unchanged. `enabled: false` disables the server everywhere without detaching it. Returns the updated `{ "server": { ... } }`.

**Header keep-marker:** inside `auth_headers`, an empty-string value means "keep the stored value for this header". To remove a header, send `auth_headers` without it; to clear all headers, send `auth_headers: null`.

Setting `auth_type` to `headers` on an OAuth-connected server disconnects it: the stored tokens are revoked with the provider and deleted.

### Delete a server

<mark style="color:green;">`POST`</mark> `https://api.convai.com/mcp/servers/delete` with body `{ "server_id": "..." }`. Removes the server and all of its character attachments. For OAuth servers, the stored tokens are revoked with the provider and deleted. Returns `{ "status": "success" }`.

### Test a connection

<mark style="color:green;">`POST`</mark> `https://api.convai.com/mcp/servers/test` has two modes, mutually exclusive:

* **Pre-create probe:** `{ "url": "...", "transport"?, "auth_headers"? }`
* **Saved server:** `{ "server_id": "..." }`. Uses the stored URL, transport, and credentials. OAuth servers are probed with the connected account's live token.

Returns the discovered tools, or a diagnostic:

```json
{ "ok": true, "tools": [ { "name": "lookup_order", "description": "..." } ] }
{ "ok": false, "error": "HTTP 401 on initialize (check URL and auth)" }
```

Connection failures are reported in the `ok: false` body with HTTP 200; non-200 statuses mean the request itself failed, not the probed server.

## OAuth connections

Servers with `auth_type: "oauth"` authenticate by connecting an account instead of storing header values. The flow has one browser step, where the account owner signs in at the provider; everything else is API calls:

1. Create the server with `auth_type: "oauth"` and no `auth_headers`.
2. Call `/mcp/oauth/start`. It returns an `authorize_url`.
3. Open `authorize_url` in a browser, sign in, and approve the requested access. The provider redirects back to Convai and the connection completes server-side.
4. Poll `/mcp/oauth/status` until `status` is `connected`.

Convai registers itself with most providers automatically. Tokens are stored encrypted and refreshed automatically; no endpoint ever returns them.

### Start a connection

<mark style="color:green;">`POST`</mark> `https://api.convai.com/mcp/oauth/start`

| Field           | Required | Notes                                                                  |
| --------------- | -------- | ---------------------------------------------------------------------- |
| `server_id`     | yes      | Must be a `streamable_http` server.                                    |
| `client_id`     | no       | Only for providers that don't allow automatic registration; see below. |
| `client_secret` | no       | Ditto; omit for public clients.                                        |
| `scopes`        | no       | Space-delimited scope string. Omit to use the provider's defaults.     |

```json
{ "ok": true, "authorize_url": "https://mcp.notion.com/authorize?client_id=..." }
```

The URL is single-use and expires in a few minutes; call `/mcp/oauth/start` again for a fresh one. Flow failures (like a provider that refuses automatic registration) come back as `{ "ok": false, "error": "..." }` with HTTP 200.

**Providers that require a registered app** (Google, most enterprise identity systems) refuse automatic registration; `start` returns an error saying so. Create an OAuth app in the provider's console, register `https://api.convai.com/mcp/oauth/callback` as its redirect URL, and call `start` again with the app's `client_id` (and `client_secret`, if issued).

### Check connection status

<mark style="color:green;">`POST`</mark> `https://api.convai.com/mcp/oauth/status` with body `{ "server_id": "..." }`.

```json
{ "status": "connected", "scope": "default" }
```

| `status`       | Meaning                                                                         |
| -------------- | ------------------------------------------------------------------------------- |
| `disconnected` | No connection. Start one with `/mcp/oauth/start`.                               |
| `pending`      | A connection was started but the browser step hasn't completed.                 |
| `connected`    | Connected; the server's tools are usable. `scope` is what the provider granted. |
| `needs_reauth` | The provider invalidated the grant. Run `/mcp/oauth/start` again.               |

### Disconnect

<mark style="color:green;">`POST`</mark> `https://api.convai.com/mcp/oauth/disconnect` with body `{ "server_id": "..." }`. Revokes the grant with the provider (best-effort) and deletes the stored tokens. The server configuration stays, so you can reconnect later. Returns `{ "status": "success" }`.

## Character attachments

* <mark style="color:green;">`POST`</mark> `/mcp/characters/list` with body `{ "character_id": "..." }` returns `{ "server_ids": ["..."] }`
* <mark style="color:green;">`POST`</mark> `/mcp/characters/attach` with body `{ "character_id": "...", "server_id": "..." }` returns `{ "status": "success" }`. Both must belong to your account. Idempotent.
* <mark style="color:green;">`POST`</mark> `/mcp/characters/detach` with body `{ "character_id": "...", "server_id": "..." }` returns `{ "status": "success" }`. Idempotent.

Attached tools are picked up at the character's next conversation session.

## Example: header-auth server

```bash
# Probe first, then register and attach
curl -s https://api.convai.com/mcp/servers/test \
  -H "CONVAI-API-KEY: $CONVAI_API_KEY" -H "Content-Type: application/json" \
  -d '{"url": "https://mcp.example.com/mcp"}'

curl -s https://api.convai.com/mcp/servers/create \
  -H "CONVAI-API-KEY: $CONVAI_API_KEY" -H "Content-Type: application/json" \
  -d '{"name": "order-lookup", "url": "https://mcp.example.com/mcp",
       "auth_headers": {"Authorization": "Bearer sk-..."}}'

curl -s https://api.convai.com/mcp/characters/attach \
  -H "CONVAI-API-KEY: $CONVAI_API_KEY" -H "Content-Type: application/json" \
  -d '{"character_id": "<character_id>", "server_id": "<server_id from create>"}'
```

## Example: OAuth server

```bash
# Register, start the connection, open the URL, poll until connected
curl -s https://api.convai.com/mcp/servers/create \
  -H "CONVAI-API-KEY: $CONVAI_API_KEY" -H "Content-Type: application/json" \
  -d '{"name": "notion", "url": "https://mcp.notion.com/mcp", "auth_type": "oauth"}'

curl -s https://api.convai.com/mcp/oauth/start \
  -H "CONVAI-API-KEY: $CONVAI_API_KEY" -H "Content-Type: application/json" \
  -d '{"server_id": "<server_id>"}'
# -> { "ok": true, "authorize_url": "https://..." }   open this in a browser

curl -s https://api.convai.com/mcp/oauth/status \
  -H "CONVAI-API-KEY: $CONVAI_API_KEY" -H "Content-Type: application/json" \
  -d '{"server_id": "<server_id>"}'
# -> { "status": "connected", "scope": "default" }
```
