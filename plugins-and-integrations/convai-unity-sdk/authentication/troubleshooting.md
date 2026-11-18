---
title: Troubleshoot authentication
description: Fix Convai Unity SDK authentication failures using exact console messages, error codes, and causes for API Key and Auth Token mode.
last_reviewed: "4.5.0"
---

Diagnose a failed connection in either authentication mode using the exact console message or `SessionErrorCodes` value the SDK returns. Use this page after a connection attempt fails, or when a token endpoint you configured is not being reached correctly.

## Symptom table

| Symptom | Likely cause | Fix | Verify |
|---|---|---|---|
| `Auth token endpoint must use HTTPS, except for HTTP loopback URLs used during local development.` | The configured **Token Endpoint URL** is plain HTTP and not a loopback address. | Change the endpoint to HTTPS, or use an `http://127.0.0.1` / `http://localhost` address for local development only. | Reconnect; the endpoint request now succeeds instead of failing validation. |
| `Auth token endpoint returned no response.` / `...transport failed.` | The endpoint is unreachable — wrong host, network failure, or the server is down. | Confirm the endpoint URL is correct and the server is running and reachable from the build target's network. | Reconnect and confirm the request reaches your server's access log. |
| `Auth token endpoint returned HTTP {code}.` | The endpoint responded with a non-2xx status. | Check your server logs for the returned status code and fix the underlying failure (auth, rate limit, server error). | Reconnect after the server returns `200`. |
| `Auth token endpoint returned malformed JSON.` | The endpoint's response body is not valid JSON. | Return a JSON object with the token field, for example `{"apiAuthToken": "..."}`. | Reconnect; the SDK parses the response without error. |
| `Auth token response field '{field}' was not found.` | The response JSON does not contain the field configured in **Token Response Field** (default `apiAuthToken`). | Match **Token Response Field** to the actual JSON key your endpoint returns, including the dotted path for a nested field such as `data.token`. | Reconnect; the SDK reads the token from the corrected field. |
| `...was empty.` (response field found but empty) | The response field exists but its value is an empty string. | Fix the server logic that mints the token — it returned successfully but with no token value. | Reconnect and confirm the field is populated. |
| `...contained an invalid expirationTime.` | The optional `expirationTime` field is not a parseable timestamp. | Return `expirationTime` as an ISO-8601 string, or omit the field entirely if you are not using it. | Reconnect; the SDK accepts the response. |
| `Auth token delegate returned no task.` / `...returned an empty token.` | A `DelegateAuthTokenProvider` lambda returned `null` or an empty string instead of a token. | Fix the delegate to always return a non-empty token string or throw/await a proper failure. | Reconnect; the delegate returns a valid token. |
| `Auth token delegate failed ({ExceptionType}).` | The `DelegateAuthTokenProvider` lambda threw an exception. | Check the exception type in the message and fix the underlying failure in your delegate. | Reconnect after the delegate stops throwing. |
| `Auth Token mode requires a registered IConvaiAuthTokenProvider or a configured endpoint URL.` (`ConfigAuthTokenProviderMissing`) | **Auth Mode** is **Auth Token**, but no provider is registered and no **Token Endpoint URL** is configured. | Register an `IConvaiAuthTokenProvider` before the first connection, or configure a **Token Endpoint URL** in **Convai > Settings > Credentials**. | Reconnect; the error no longer appears. |
| `Auth token provider failed ({ExceptionType}).` / `...failed to resolve a token.` / `...returned an empty token.` | Your registered `IConvaiAuthTokenProvider` implementation threw, failed, or returned an empty token. | Check the exception type or failure reason and fix `GetTokenAsync` in your provider. | Reconnect after the provider returns a valid, non-empty token. |
| `Explicit auth-token connections require Auth Token mode in Convai Project Settings.` (`ConfigAuthTokenModeRequired`) | `ConnectWithAuthTokenAsync` was called while **Auth Mode** is still **API Key**. | Set **Auth Mode** to **Auth Token** in **Convai > Settings > Credentials** before calling `ConnectWithAuthTokenAsync`. | Reconnect; the explicit token is accepted. |
| `A non-empty Convai auth token is required.` | `ConnectWithAuthTokenAsync` was called with an empty or whitespace `authToken` argument. | Confirm your login flow fetched a token before calling `ConnectWithAuthTokenAsync`; do not call it with a placeholder value. | Reconnect with a real token. |
| `A non-empty end-user ID is required.` / `A non-empty end-user name is required.` | `ConnectWithAuthTokenAsync` was called with an empty `endUserId` or `endUserName` argument. | Pass a non-empty, stable account ID and display name for every call. | Reconnect with both arguments populated. |
| Connection fails with `Connection token is invalid` (`ConnectionInvalidToken`) | Convai rejected the token — it is expired, malformed, or was not the token your endpoint most recently issued. | Confirm your endpoint returns a freshly minted token on every request and that no caching layer is serving a stale one. | Reconnect; a fresh token is accepted. |
| Connection fails with HTTP `401` | The room-connect request was rejected at the transport level, which the SDK maps to `ConnectionInvalidToken`. | Confirm the endpoint or provider is returning `apiAuthToken` — not the game-login token, a refresh token, or the Convai account API key — and that the token has not expired. | Reconnect; the connection succeeds. |
| `An API key must be saved in Convai Project Settings before the Editor can mint an auth token.` | The Editor-only fallback provider tried to run, but no API key is saved. | Save an API key in **Convai > Settings > Credentials**, even in Auth Token mode, so the Editor fallback can mint a token locally. | Enter Play mode again; the fallback provider succeeds. |
| Auth Token mode works in the Editor but fails immediately in a player build | The Editor-only fallback provider (`ConvaiEditorApiKeyAuthTokenProvider`) was silently covering for a missing provider or endpoint. It is compiled out of players. | Register a runtime `IConvaiAuthTokenProvider`, or configure a **Token Endpoint URL**, so the player build has a real credential source. | Run the build; the connection succeeds without the Editor fallback. |
| Endpoint configuration change during Play mode has no effect on an active session | Credentials resolve once per connection attempt, not continuously. | End the session and reconnect after changing the endpoint, headers, or provider. | The next connection attempt uses the updated configuration. |

## Endpoint not HTTPS

**Symptom:** The Console logs `Auth token endpoint must use HTTPS, except for HTTP loopback URLs used during local development.`

**Cause:** `EndpointAuthTokenProvider` validates the **Token Endpoint URL** before every request and rejects any scheme other than `https://`, unless the host is a loopback address (`127.0.0.1` or `localhost`) used for local development.

**Fix:** Change the endpoint to `https://`. If you are testing against a local server, use a loopback address instead of a LAN IP or a public HTTP tunnel.

**Verify:** Reconnect. The request reaches your server instead of failing validation before the request is sent.

## Endpoint response is missing the token field

**Symptom:** The Console logs `Auth token response field 'apiAuthToken' was not found.` (or whatever field name is configured).

**Cause:** `EndpointAuthTokenProvider` parses the JSON response and looks up **Token Response Field**, which defaults to `apiAuthToken` and supports dotted paths such as `data.token`. If your server's response uses a different key, or nests the token under a path the configured field does not match, resolution fails.

**Fix:** Either change your server to return the token under `apiAuthToken` at the top level, or update **Token Response Field** in **Convai > Settings > Credentials** to match your server's actual response shape.

**Verify:** Reconnect. The SDK reads the token from the response instead of reporting a missing field.

## Provider registered too late

**Symptom:** The first connection attempt after entering Play mode or after a build starts fails with `Auth Token mode requires a registered IConvaiAuthTokenProvider or a configured endpoint URL.`, even though your code registers a provider.

**Cause:** `ConvaiAuthTokenProviderRegistry` is a process-local static registry that resets automatically on `RuntimeInitializeLoadType.SubsystemRegistration` — every domain reload and every Play mode entry clears it. A provider registered in a component that initializes after the SDK's first connection attempt, or a provider that was never re-registered after a reload, leaves the registry empty when the SDK needs it.

**Fix:** Register the provider as early as possible, for example in a scene bootstrap component's `Awake` method, and register it again after any domain reload or scene reload that could have cleared it. If your login SDK initializes asynchronously, register the provider immediately and let your provider's own token-fetch logic await login initialization internally — do not delay registration itself.

**Verify:** Reconnect after the fix. `IsRegistered` reflects the provider immediately after registration, and the connection resolves a token instead of reporting a missing provider.

## Auth Token mode not selected for an explicit-token connect

**Symptom:** `ConnectWithAuthTokenAsync` fails immediately with `Explicit auth-token connections require Auth Token mode in Convai Project Settings.`

**Cause:** `RoomConnectionRuntimeAdapter` checks that the active credential provider implements the explicit-token contract, which only happens when **Auth Mode** is **Auth Token**. Calling `ConnectWithAuthTokenAsync` while the project is still in **API Key** mode fails this check before any network request is made.

**Fix:** Set **Auth Mode** to **Auth Token** in **Convai > Settings > Credentials**. You do not need to configure a **Token Endpoint URL** or register a provider for this path — the caller supplies the token directly.

**Verify:** Reconnect using `ConnectWithAuthTokenAsync`. The call proceeds past credential validation instead of failing immediately.

## HTTP 401 on connect

**Symptom:** The room-connect request returns HTTP `401`, which the SDK reports as `Connection token is invalid` (`ConnectionInvalidToken`).

**Cause:** Convai rejected the token sent in the `API-AUTH-TOKEN` header. This happens when the token is expired, was already consumed, or is not actually a Convai `apiAuthToken` — for example if the endpoint or provider accidentally returned the game-login token or the Convai account API key instead.

**Fix:** Confirm your endpoint or provider returns the value of the `apiAuthToken` field from Convai's own token-minting response, not any other credential, and that it is minted fresh for each connection rather than served from a cache that can go stale.

**Verify:** Reconnect. A freshly minted, correctly sourced token connects successfully.

## Editor-only fallback provider does not kick in

**Symptom:** In the Unity Editor, Auth Token mode still fails with `Auth Token mode requires a registered IConvaiAuthTokenProvider or a configured endpoint URL.`, even though an API key is saved.

**Cause:** `ConvaiEditorApiKeyAuthTokenProvider` only auto-registers when all three conditions hold: **Auth Mode** is **Auth Token**, an API key is saved, and no **Token Endpoint URL** is configured. If a **Token Endpoint URL** is set — even an invalid one — the fallback does not activate, because an explicit endpoint takes precedence.

**Fix:** For local Editor testing without a real backend, clear **Token Endpoint URL** and confirm an API key is saved in **Convai > Settings > Credentials**. Do not rely on this fallback for anything other than Editor testing — it is compiled out of players entirely, so a build will fail this same way unless a runtime provider or endpoint is configured. See [Ship a secure build](ship-a-secure-build.md).

**Verify:** Enter Play mode. The Editor mints a token from the saved API key and the connection succeeds.

## Next steps

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Configure Auth Token mode</strong><br>Switch to Auth Token mode and configure the token endpoint in Project Settings.</td><td><a href="configure-auth-token-mode.md">configure-auth-token-mode.md</a></td></tr><tr><td><strong>Write a custom token provider</strong><br>Implement IConvaiAuthTokenProvider to fetch a token from your own login flow.</td><td><a href="custom-token-provider.md">custom-token-provider.md</a></td></tr><tr><td><strong>Ship a secure build</strong><br>What the build processor strips and the WebGL CORS requirements for a token endpoint.</td><td><a href="ship-a-secure-build.md">ship-a-secure-build.md</a></td></tr></tbody></table>
