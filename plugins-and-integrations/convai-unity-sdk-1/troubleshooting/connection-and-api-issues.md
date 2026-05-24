---
title: Connection and API issues
description: Interpret Convai session error codes, read ConvaiRoomManager diagnostics, and resolve authentication, transport, and rate-limit failures.
last_reviewed: "4.2.0"
---

All session errors surface through `ConvaiSessionEventRelay.OnSessionError`. The event payload carries an `ErrorCode` string and a human-readable `Message`. Error codes follow a hierarchical dot-notation format: `{category}.{detail}`. The category prefix tells you which layer of the system failed.

| Category prefix | What failed |
| --- | --- |
| `config.*` | SDK configuration — missing API key or Character ID |
| `connection.*` | Convai API or network — authentication, routing, limits |
| `transport.*` | WebRTC / LiveKit layer — ICE, peer connection, signal |
| `server.*` | Convai backend pipeline — quota, fatal errors |
| `session.*` | Session lifecycle — token expiry, state conflicts |

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
        _sessionRelay.OnSessionError.AddListener(OnError);
    }

    private void OnDisable()
    {
        _sessionRelay.OnSessionError.RemoveListener(OnError);
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
var room = FindFirstObjectByType<ConvaiRoomManager>();
Debug.Log($"State:           {room.CurrentState}");
Debug.Log($"Connected:       {room.IsConnected}");
Debug.Log($"Last error code: {room.LastSessionErrorCode}");
Debug.Log($"Last error msg:  {room.LastSessionErrorMessage}");
Debug.Log($"Connect attempts:{room.ConnectAttemptCount}  Reconnects: {room.ReconnectCount}");
```

## Configuration errors

Configuration errors fire immediately on connect — before any network traffic. Fix these first.

| Error code | Description | Fix |
| --- | --- | --- |
| `config.api_key_missing` | API key field is empty in `ConvaiSettings` | Open Edit → Project Settings → Convai SDK and paste your API key |
| `config.character_id_missing` | `CharacterId` field on `ConvaiCharacter` is empty | Set the Character ID in the `ConvaiCharacter` Inspector field |

{% hint style="warning" %}
The SDK emits a warning before any connect attempt if the API key is empty: `Convai Bootstrapper: API key not configured. Please set your API key in Edit > Project Settings > Convai SDK.` This fires on Play — fix it before testing connections.
{% endhint %}

## Connection errors

These codes appear when Convai rejects or cannot fulfill the connect request. Most have a clear cause and a direct fix.

| Error code | Description | Retried automatically | Fix |
| --- | --- | --- | --- |
| `connection.connect_invalid_api_key` | The API key was rejected by Convai | No | Copy a fresh key from the Convai dashboard; check for trailing spaces |
| `connection.auth_failed` | Authentication failed (revoked token or bad credentials) | No | Re-enter your API key; check if the key has been revoked on the dashboard |
| `connection.invalid_token` | The connection token provided is invalid | No | Tokens are generated internally — if this appears, reconnect to generate a fresh token |
| `connection.connect_invalid_session_id` | Connect request used an invalid session identifier | No | Session IDs are generated internally — reconnect to reset the session |
| `connection.connect_character_not_found` | The Character ID does not exist on your account | No | Verify the Character ID in the Convai dashboard matches exactly |
| `connection.connect_realtime_not_allowed` | Realtime access is not enabled for this account | No | Upgrade your Convai plan or contact support |
| `connection.connect_concurrency_limit_reached` | Your plan's simultaneous session limit is reached | Yes | Disconnect idle characters; upgrade plan for higher limits |
| `connection.connect_speaker_limit_reached` | Backend speaker limit reached for this account | Yes | Reduce concurrent active characters |
| `connection.connect_bot_start_failed` | Convai pipeline failed to start (transient backend issue) | Yes | SDK retries automatically; if persistent, contact support |
| `connection.connect_unhandled_server_exception` | Unhandled exception on Convai during connect | Yes | SDK retries automatically; check Convai status page if persistent |
| `connection.timeout` | Connect did not complete within the timeout window | Yes | Check internet connection; increase **Connection Timeout** in settings (default 30 s, max 120 s) |
| `connection.network_error` | DNS failure, socket error, or network unreachable | Yes | Verify internet connectivity; check that Convai domains are not blocked by firewall |
| `connection.rate_limited` | Too many connect requests in a short window | Yes | Reduce frequency of reconnect attempts; add delay between retries in your code |
| `connection.service_unavailable` | Convai temporarily unavailable (HTTP 503) | Yes | Wait and retry; SDK backs off automatically |
| `connection.server_error` | Convai returned a 5xx error | Yes | Transient — SDK retries; check Convai status page if persistent |
| `connection.not_found` | Resource (character or room) not found (HTTP 404) | No | Verify Character ID exists on your account |
| `connection.bad_request` | Invalid parameters in the connect request | No | Check that CharacterId and other connection parameters contain no invalid characters |
| `connection.connect_validation_error` | Connect request failed API validation (HTTP 422) | No | Inspect error message for which field failed validation |
| `connection.failed` | Generic connection failure not covered by a specific code | Depends | Check `LastSessionErrorMessage` for details |

## Transport errors

Transport errors occur at the WebRTC / LiveKit layer, after Convai has accepted the connect request. They are almost always transient and the SDK retries automatically.

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
| `server.error` | Non-fatal pipeline error reported by Convai | SDK retries; if persistent, report to Convai support |

## Session and protocol errors

| Error code | Description | Fix |
| --- | --- | --- |
| `session.token_expired` | Session token has expired | Reconnect to obtain a fresh token |
| `session.invalid_state` | An operation was attempted in an invalid state | Check your connect/disconnect call order |
| `session.cancelled` | Session was cancelled by your code | Expected if you call `DisconnectAsync` manually |
| `protocol.message_invalid` | An invalid protocol message was received from Convai | Usually indicates an SDK/backend version mismatch; update the SDK |
| `protocol.parse_failed` | SDK could not parse a message from Convai | Usually indicates an SDK/backend version mismatch; update the SDK |

## Retry behavior

The SDK uses an exponential backoff policy for transient errors. After a failed attempt, it waits before trying again:

| Attempt | Delay before this attempt |
| --- | --- |
| 1 (initial) | None — immediate |
| 2 | 1 second |
| 3 | 2 seconds |
| 4 (final) | 4 seconds |

After four attempts, the SDK gives up and fires `OnSessionError` with the final error code. **Non-transient errors — such as invalid API key, character not found, or realtime not allowed — are not retried at all.** The SDK fires `OnSessionError` immediately.

The following error codes trigger automatic retries:

* `connection.timeout`
* `connection.network_error`
* `connection.server_error`
* `connection.service_unavailable`
* `connection.rate_limited`
* `connection.connect_concurrency_limit_reached`
* `connection.connect_bot_start_failed`
* `connection.connect_unhandled_server_exception`
* `transport.ice_failed`
* `transport.signal_disconnected`
* `server.error`

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
