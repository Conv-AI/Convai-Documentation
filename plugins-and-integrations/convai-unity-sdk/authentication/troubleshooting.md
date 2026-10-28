---
title: Troubleshoot authentication
description: Diagnose failed token requests, missing credentials, and rejected connections using the messages returned by the Unity SDK.
last_reviewed: "5.0.0-preview"
---

Start with the failed operation's `Code` and `Message`. Token acquisition and the later room connection are separate operations: a token endpoint can succeed while Convai rejects the room connection.

## Match the failure

| Symptom or code | Action | Verify |
|---|---|---|
| Character never connects and the Console shows no error | Register a token provider before `ConvaiRoomManager` starts, or configure a valid endpoint. If registration happens later, call `ConnectAsync` explicitly. | The next connection attempt reaches your token source. |
| **Setup Health** reports an invalid or missing token endpoint | Correct **Credentials > Token Endpoint URL**, or use a runtime provider. Health checks configuration, not server acceptance. | The **Auth Token** row becomes **Healthy** for the configured endpoint. |
| `connection.auth_token_fetch_failed` | Read the accompanying provider or endpoint message in the table below. | Token resolution completes and the connect request begins. |
| `config.auth_token_mode_required` | Select **Auth Token** before calling `ConnectWithAuthTokenAsync`. | The call passes credential-mode validation. |
| `connection.invalid_token` | Supply a non-empty Convai `apiAuthToken` to the explicit connection method. | The call passes local argument validation. |
| `connection.bad_request` | Check required explicit identity arguments, the `512`-character ID limit, `255`-character name limit, and JSON-compatible metadata. | The call passes identity validation. |
| HTTP `401`, mapped to `connection.connect_invalid_api_key` | Read the response message. Confirm your provider returns a Convai auth token, not an account key or your game's login token. | A new connection succeeds with the correct credential. |
| `connection.connect_end_user_id_required` | Supply an appropriate stable end-user ID and reconnect. | Inspect `CurrentEndUserId` without logging it and `CurrentLongTermMemoryStatus`. |
| Works in the Editor but fails in a player | Supply a runtime provider, endpoint, or explicit token. The Editor's saved-key provider is not compiled into players. | Run the built player and connect. |
| An explicit-token call leaves the old session unchanged | Disable **Starts Connected** or disconnect the existing session first. | A new connection consumes the supplied token. |

## Diagnose a token request

| Message | Cause and correction |
|---|---|
| `Auth Token mode requires a registered IConvaiAuthTokenProvider or a configured endpoint URL.` | No source exists when a manual connection resolves credentials. Register your provider again each Play session, or configure the endpoint. |
| `Auth token endpoint must use HTTPS, except for HTTP loopback URLs used during local development.` | Use HTTPS. HTTP is accepted only for loopback development addresses. |
| `Auth token endpoint returned no response.` or a transport-failed message | Check host, network, endpoint availability, and the target device's access to it. |
| `Auth token endpoint request failed ({ExceptionType}).` | The request threw. Diagnose the exception type and endpoint transport. |
| `Auth token endpoint returned HTTP {code}.` | Check the endpoint's access logs and error response. |
| `Auth token endpoint returned malformed JSON.` | Return a JSON object with a string token field. |
| `Auth token response field '{field}' was not found.` | Match **Token Response Field** to the response, including a dotted path if nested. The default is `apiAuthToken`. |
| A token-field message ending in `was empty.` | Return a non-empty token string. |
| An invalid `expirationTime` message | Supply a parseable timestamp at the top level or omit that optional field. |
| `Auth token delegate returned no task.` | Return a task from the delegate. |
| `Auth token delegate returned an empty token.` | Resolve a non-empty token string. |
| `Auth token delegate failed ({ExceptionType}).` | Diagnose the exception in your delegate. Cancellation propagates separately. |
| A provider-failed or empty-token message | Inspect `GetTokenAsync`. A failed registered provider does not fall through to the configured endpoint. |

## Restore Editor-only token access

The Editor provider registers before scene load only when **Auth Token** is selected, a saved key exists, the endpoint is empty, and no other provider is registered. Any configured endpoint, including an invalid one, disables this fallback.

{% stepper %}
{% step %}
### Save the Editor key

Open **Convai > Settings**, scroll to **Credentials**, temporarily select **Api Key**, and use **Validate & Save** for your key. The key field is hidden in Auth Token mode.
{% endstep %}
{% step %}
### Select Auth Token again

For Editor-only testing, clear **Token Endpoint URL**, select **Auth Token**, and enter Play mode again. A custom provider registered later replaces the fallback.
{% endstep %}
{% step %}
### Verify the build separately

Configure a runtime source before distributing a player. Follow [Ship a secure build](ship-a-secure-build.md) and verify a connection in the built player.
{% endstep %}
{% endstepper %}

## Next steps

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Configure Auth Token mode</strong><br>Switch to Auth Token mode and configure the token endpoint in Project Settings.</td><td><a href="configure-auth-token-mode.md">configure-auth-token-mode.md</a></td></tr><tr><td><strong>Write a custom token provider</strong><br>Implement IConvaiAuthTokenProvider to fetch a token from your own login flow.</td><td><a href="custom-token-provider.md">custom-token-provider.md</a></td></tr><tr><td><strong>Ship a secure build</strong><br>What the build processor strips and the WebGL CORS requirements for a token endpoint.</td><td><a href="ship-a-secure-build.md">ship-a-secure-build.md</a></td></tr></tbody></table>
