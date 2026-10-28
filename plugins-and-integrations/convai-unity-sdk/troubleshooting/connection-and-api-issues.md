---
title: Connection and API issues
description: Interpret Convai session error codes, read the room manager diagnostics, and resolve authentication, transport, and rate-limit failures.
last_reviewed: "5.0.0-preview"
---

All session errors surface through `ConvaiSessionEventRelay.OnSessionError`. The event payload carries `ErrorCode`, `Message`, `SessionId`, `IsRecoverable`, `Stage`, `HttpStatusCode`, and `HasHttpStatusCode`. Check `HasHttpStatusCode` before using the status value. `IsRecoverable` is diagnostic information, not a promise of automatic retry. Error codes follow a hierarchical dot-notation format: `{category}.{detail}`. The category prefix tells you which layer of the system failed.

| Category prefix | What failed |
| --- | --- |
| `config.*` | SDK configuration — missing API key, Character ID, or Auth Token mode setup |
| `connection.*` | Convai API or network — authentication, routing, limits |
| `transport.*` | WebRTC / LiveKit layer — ICE, peer connection, signal |
| `server.*` | Convai's own pipeline — quota, fatal errors |
| `session.*` | Session lifecycle — token expiry, state conflicts |
| `audio.*` | Microphone capture, policy, or publication |
| `vision.*` | Vision capture or publication |
| `protocol.*` | Message validation or parsing |

## Subscribe to session errors

Add `ConvaiSessionEventRelay` to the same GameObject as `ConvaiManager` and wire it in the Inspector, or subscribe in code:

```csharp
using Convai.Runtime.Presentation.Events;
using UnityEngine;

public class ErrorListener : MonoBehaviour
{
    [SerializeField] private ConvaiSessionEventRelay _sessionRelay;

    private void OnEnable()
    {
        if (_sessionRelay != null) _sessionRelay.OnSessionError.AddListener(OnError);
    }

    private void OnDisable()
    {
        if (_sessionRelay != null) _sessionRelay.OnSessionError.RemoveListener(OnError);
    }

    private void OnError(SessionErrorRelayData data)
    {
        Debug.LogError($"[MyApp] Session error: {data.ErrorCode} — {data.Message}");
    }
}
```

### Read error state directly

`ConvaiRoomManager` stores the most recent error code and message as plain properties — no event subscription required. This is useful for logging diagnostic state on demand:

```csharp
// Inside a MonoBehaviour method; assign the scene's room component explicitly.
// using Convai.Runtime.Adapters.Networking;
// using UnityEngine;
// [SerializeField] private ConvaiRoomManager room;
// pseudocode: the field and using directives above belong in your component.
if (room != null)
{
    Debug.Log($"State: {room.CurrentState}; connected: {room.IsConnected}");
    Debug.Log($"Last error: {room.LastSessionErrorCode}");
    Debug.Log($"Attempts: {room.ConnectAttemptCount}; reconnects: {room.ReconnectCount}");
}
```

## Configuration errors

Configuration gates validate the required local settings before connection. Fix the reported configuration problem before retrying.

| Error code | Description | Fix |
| --- | --- | --- |
| `config.api_key_missing` | API key field is empty in `ConvaiSettings` | Open Edit → Project Settings → Convai SDK and paste your API key |
| `config.character_id_missing` | `CharacterId` field on `ConvaiCharacter` is empty | Set the Character ID in the `ConvaiCharacter` Inspector field |
| `config.auth_token_provider_missing` | Auth Mode is Auth Token, but no `IConvaiAuthTokenProvider` is registered and no Token Endpoint URL is configured | Register a provider or configure a Token Endpoint URL — see [Troubleshoot authentication](../authentication/troubleshooting.md) |
| `config.auth_token_endpoint_invalid` | The configured Token Endpoint URL is not HTTPS and is not a loopback development address | Use `https://`, or `http://localhost` / `http://127.0.0.1` for local development — see [Troubleshoot authentication](../authentication/troubleshooting.md) |
| `config.auth_token_mode_required` | `ConnectWithAuthTokenAsync` was called while Auth Mode is still API Key | Set Auth Mode to Auth Token in Convai Project Settings before calling `ConnectWithAuthTokenAsync` — see [Troubleshoot authentication](../authentication/troubleshooting.md) |

{% hint style="warning" %}
The SDK emits a warning before any connect attempt if the API key is empty: `Convai Bootstrapper: API key not configured. Please set your API key in Edit > Project Settings > Convai SDK.` This applies to API Key mode. Auth Token mode can instead report that it is awaiting a registered provider or valid endpoint before the first connection.
{% endhint %}

## Connection errors

These codes classify failures recognized by the client. Their messages guide the next check; account entitlement and service outcomes require confirmation from Convai. Retry selection depends on the thrown exception, not this code table.

| Error code | Description | Fix |
| --- | --- | --- |
| `connection.connect_invalid_api_key` | The API key was rejected by Convai | Copy a fresh key from the Convai dashboard; check for trailing spaces |
| `connection.auth_token_fetch_failed` | Auth Token mode failed to resolve a token before connecting (provider exception, empty token, or endpoint failure) | See [Troubleshoot authentication](../authentication/troubleshooting.md) for the exact console message and cause |
| `connection.auth_failed` | Authentication failed (revoked token or bad credentials) | Re-enter your API key; check if the key has been revoked on the dashboard |
| `connection.invalid_token` | The connection token provided is invalid | Tokens are generated internally — if this appears, reconnect to generate a fresh token |
| `connection.connect_invalid_session_id` | Connect request used an invalid session identifier | Session IDs are generated internally — reconnect to reset the session |
| `connection.connect_character_not_found` | The Character ID does not exist on your account | Verify the Character ID in the Convai dashboard matches exactly |
| `connection.connect_realtime_not_allowed` | Realtime access is not enabled for this account | Upgrade your Convai plan or contact support |
| `connection.connect_concurrency_limit_reached` | Your plan's simultaneous session limit is reached | Disconnect idle characters; upgrade plan for higher limits |
| `connection.connect_speaker_limit_reached` | Backend speaker limit reached for this account | Reduce the number of concurrently active characters, or raise the limit on your account. The reported limit must be resolved before another equivalent request can succeed. |
| `connection.connect_bot_start_failed` | Convai pipeline failed to start (transient backend issue) | Inspect the detailed error; if persistent, contact support |
| `connection.connect_unhandled_server_exception` | Unhandled exception on Convai during connect | Inspect the detailed error and service status if persistent |
| `connection.timeout` | Connect did not complete within the timeout window | Check internet connection; increase **Connection Timeout** in settings (default 30 s, max 120 s) |
| `connection.network_error` | DNS failure, socket error, or network unreachable | Verify internet connectivity; check that Convai domains are not blocked by firewall |
| `connection.rate_limited` | Too many connect requests in a short window | Reduce frequency of reconnect attempts; add delay between retries in your code |
| `connection.service_unavailable` | Convai temporarily unavailable (HTTP 503) | Wait before another attempt and inspect the error |
| `connection.server_error` | Convai returned a 5xx error | Inspect the error and service status if persistent |
| `connection.not_found` | Resource (character or room) not found (HTTP 404) | Verify Character ID exists on your account |
| `connection.bad_request` | Invalid parameters in the connect request | Check that CharacterId and other connection parameters contain no invalid characters |
| `connection.connect_validation_error` | Connect request failed API validation (HTTP 422) | Inspect error message for which field failed validation |
| `connection.failed` | Generic connection failure not covered by a specific code | Check `LastSessionErrorMessage` for details |

## Transport errors

Transport errors occur in the WebRTC / LiveKit layer. Inspect session state and transport diagnostics; a code alone does not establish whether a reconnect will run.

| Error code | Description | What to check |
| --- | --- | --- |
| `transport.ice_failed` | WebRTC ICE negotiation failed — peer cannot be reached | Verify the network allows UDP traffic; corporate firewalls often block WebRTC |
| `transport.peer_connection_failed` | WebRTC peer connection could not be established | Same as ICE failed — check UDP ports and STUN/TURN accessibility |
| `transport.livekit_error` | LiveKit SDK reported an error | Usually transient; check internet stability |
| `transport.signal_disconnected` | LiveKit signal server connection dropped | Usually auto-reconnects; persistent failures indicate network instability |

{% hint style="info" %}
WebRTC requires UDP ports to be accessible. In corporate deployments, work with your network team to whitelist the Convai LiveKit endpoints. See the Network & API Requirements page for the full list of domains and ports.
{% endhint %}

## Server and usage errors

| Error code | Description | Fix |
| --- | --- | --- |
| `server.usage_limit_reached` | Daily or monthly usage quota exceeded | Check usage in the Convai dashboard; upgrade your plan |
| `server.fatal_error` | Fatal pipeline error — session terminated by Convai | Session cannot recover; initiate a new connect |
| `server.error` | Non-fatal pipeline error reported by Convai | Inspect the detailed error; if persistent, report to Convai support |

## Session and protocol errors

| Error code | Description | Fix |
| --- | --- | --- |
| `session.token_expired` | Session token has expired | Reconnect to obtain a fresh token |
| `session.invalid_state` | An operation was attempted in an invalid state | Check your connect/disconnect call order |
| `session.cancelled` | Session was cancelled by your code | Expected if you call `DisconnectAsync` manually |
| `protocol.message_invalid` | An invalid protocol message was received from Convai | Usually indicates an SDK/backend version mismatch; update the SDK |
| `protocol.parse_failed` | SDK could not parse a message from Convai | Usually indicates an SDK/backend version mismatch; update the SDK |

## Multi-character and memory rejections

| Code | Client interpretation | Next check |
| --- | --- | --- |
| `connection.connect_multi_character_not_allowed` | The requested multi-character room is not permitted | Confirm account access and use a supported roster |
| `connection.connect_multi_character_roster_limit` | Roster size exceeds the reported allowance | Reduce the roster or confirm the account allowance |
| `connection.connect_end_user_id_required` | Memory configuration requires an end-user ID | Supply a stable application-owned end-user ID |
| `connection.connect_ltm_end_user_limit_reached` | The long-term memory end-user allowance is exhausted | Inspect usage and account configuration |
| `connection.connect_ltm_not_configured` | No long-term memory allowance is configured | Confirm the account's memory configuration |

See [Multi-character sessions](../features/multi-character-sessions/) and [Long-term memory troubleshooting](../features/long-term-memory/troubleshooting-and-diagnostics.md). These mappings describe the client's handling of reported errors; they do not independently verify an account's limits.

## Retry behavior

The generic `RetryExecutor` uses exception-based `ExponentialBackoffPolicy`. Its default schedule is four attempts: immediately, then after delays of `1`, `2`, and `4` seconds. `TimeoutException` and `HttpRequestException`, including supported wrapped or aggregate cases, can qualify while attempts remain.

The policy also recognizes `OperationCanceledException` as transient, but `RetryExecutor` explicitly excludes a directly thrown cancellation from its catch-and-retry loop. Cancellation is not a reason to promise another attempt. A `ConvaiOperationException` carrying a recoverable-looking code is not automatically retried solely because of that code.

`SessionErrorCodes.IsRecoverable` supplies diagnostic classification. It is separate from exception retry and from transport reconnection. Check `ConnectAttemptCount`, `ReconnectCount`, and state changes to establish what actually happened.

## Runtime diagnostics

Read `ConvaiRoomManager` state properties to narrow down a connection failure. The properties update in real time — no event subscription required. For the full property reference, diagnostic snapshot API, and code samples, see the Debug Tools Reference.

{% content-ref url="debug-tools-reference.md" %}
[Debug tools reference](debug-tools-reference.md)
{% endcontent-ref %}

## Quick reference: common failure patterns

| Symptom | Likely cause | Fix | Verify |
| --- | --- | --- | --- |
| `config.api_key_missing` on every connect | API key never entered | Edit → Project Settings → Convai SDK → paste key | Re-enter Play Mode — error no longer fires |
| `connection.connect_invalid_api_key` | Wrong or revoked API key | Copy a fresh key from the Convai dashboard | Session reaches `Connected` state |
| `connection.connect_character_not_found` | Character ID typo or wrong account | Verify in Convai dashboard; check for copy-paste whitespace | Session reaches `Connected` state |
| `connection.connect_realtime_not_allowed` | Realtime not enabled on account | Upgrade plan | Session reaches `Connected` state |
| `connection.timeout` every time | Firewall blocking connections | Whitelist Convai domains; try on a different network | Session connects within the timeout window |
| `transport.ice_failed` repeatedly | Strict firewall blocking UDP | Allow UDP; request TURN relay from network admin | Session connects; WebRTC negotiation completes |
| `server.usage_limit_reached` | Quota exceeded | Check Convai dashboard usage page | Session connects after usage resets or plan upgrades |
| Character connects once then never reconnects | `ReconnectPolicy` maxed out | SDK stops after 3 reconnect attempts (default `MaxReconnectAttempts`); call `ConnectAsync` again to retry | `ConnectAsync` call succeeds; character connects |
| `connection.rate_limited` | Too many connects in short time | Add a minimum delay between connect calls in your application logic | `connection.rate_limited` no longer fires |
| `CurrentState` stuck at `Error` | Unrecoverable session failure | Call `DisconnectAsync()` then `ConnectAsync()` to reset | Session transitions to `Connected` |

## Next steps

For a full reference to the SDK's logging system, built-in diagnostic tools, and session metrics, see the Debug Tools Reference.

{% content-ref url="debug-tools-reference.md" %}
[Debug tools reference](debug-tools-reference.md)
{% endcontent-ref %}
