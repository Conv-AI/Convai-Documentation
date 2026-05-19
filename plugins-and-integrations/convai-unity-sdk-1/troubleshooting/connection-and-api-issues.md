---
description: >-
  Interpret Convai session error codes, read ConvaiRoomManager diagnostics, and
  resolve authentication, transport, and rate-limit failures.
---

# Connection and API Issues

### Understanding Convai Connection and API Errors

All session errors surface through `ConvaiSessionEventRelay.OnSessionError`. The event payload carries an `ErrorCode` string and a human-readable `Message`. Error codes follow a hierarchical dot-notation format: `{category}.{detail}`. The category prefix tells you which layer of the system failed.

| Category prefix | What failed                                             |
| --------------- | ------------------------------------------------------- |
| `config.*`      | SDK configuration — missing API key or Character ID     |
| `connection.*`  | Convai API or network — authentication, routing, limits |
| `transport.*`   | WebRTC / LiveKit layer — ICE, peer connection, signal   |
| `server.*`      | Convai backend pipeline — quota, fatal errors           |
| `session.*`     | Session lifecycle — token expiry, state conflicts       |

#### Subscribing to Errors

Add `ConvaiSessionEventRelay` to the same GameObject as `ConvaiManager` and wire it in the Inspector, or subscribe in code:

```csharp
using Convai.Runtime.Components;
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

#### Reading Error State Directly

`ConvaiRoomManager` stores the most recent error code and message as plain properties — no event subscription required. This is useful for logging diagnostic state on demand:

```csharp
var room = FindFirstObjectByType<ConvaiRoomManager>();
Debug.Log($"State:           {room.CurrentState}");
Debug.Log($"Connected:       {room.IsConnected}");
Debug.Log($"Last error code: {room.LastSessionErrorCode}");
Debug.Log($"Last error msg:  {room.LastSessionErrorMessage}");
Debug.Log($"Connect attempts:{room.ConnectAttemptCount}  Reconnects: {room.ReconnectCount}");
```

***

### Configuration Errors

Configuration errors fire immediately on connect — before any network traffic. Fix these first.

| Error Code                    | Description                                       | Fix                                                              |
| ----------------------------- | ------------------------------------------------- | ---------------------------------------------------------------- |
| `config.api_key_missing`      | API key field is empty in `ConvaiSettings`        | Open Edit → Project Settings → Convai SDK and paste your API key |
| `config.character_id_missing` | `CharacterId` field on `ConvaiCharacter` is empty | Set the Character ID in the `ConvaiCharacter` Inspector field    |

{% hint style="warning" %}
The SDK emits a warning before any connect attempt if the API key is empty: `Convai Bootstrapper: API key not configured. Please set your API key in Edit > Project Settings > Convai SDK.` This fires on Play — fix it before testing connections.
{% endhint %}

***

### Connection Errors

These codes appear when Convai rejects or cannot fulfill the connect request. Most have a clear cause and a direct fix.

| Error Code                                      | Description                                               | Retried Automatically | Fix                                                                                              |
| ----------------------------------------------- | --------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------ |
| `connection.connect_invalid_api_key`            | The API key was rejected by Convai                        | No                    | Copy a fresh key from the Convai dashboard; check for trailing spaces                            |
| `connection.auth_failed`                        | Authentication failed (revoked token or bad credentials)  | No                    | Re-enter your API key; check if the key has been revoked on the dashboard                        |
| `connection.invalid_token`                      | The connection token provided is invalid                  | No                    | Tokens are generated internally — if this appears, reconnect to generate a fresh token           |
| `connection.connect_invalid_session_id`         | Connect request used an invalid session identifier        | No                    | Session IDs are generated internally — reconnect to reset the session                            |
| `connection.connect_character_not_found`        | The Character ID does not exist on your account           | No                    | Verify the Character ID in the Convai dashboard matches exactly                                  |
| `connection.connect_realtime_not_allowed`       | Realtime access is not enabled for this account           | No                    | Upgrade your Convai plan or contact support                                                      |
| `connection.connect_concurrency_limit_reached`  | Your plan's simultaneous session limit is reached         | Yes                   | Disconnect idle characters; upgrade plan for higher limits                                       |
| `connection.connect_speaker_limit_reached`      | Backend speaker limit reached for this account            | Yes                   | Reduce concurrent active characters                                                              |
| `connection.connect_bot_start_failed`           | Convai pipeline failed to start (transient backend issue) | Yes                   | SDK retries automatically; if persistent, contact support                                        |
| `connection.connect_unhandled_server_exception` | Unhandled exception on Convai during connect              | Yes                   | SDK retries automatically; check Convai status page if persistent                                |
| `connection.timeout`                            | Connect did not complete within the timeout window        | Yes                   | Check internet connection; increase **Connection Timeout** in settings (default 30 s, max 120 s) |
| `connection.network_error`                      | DNS failure, socket error, or network unreachable         | Yes                   | Verify internet connectivity; check that Convai domains are not blocked by firewall              |
| `connection.rate_limited`                       | Too many connect requests in a short window               | Yes                   | Reduce frequency of reconnect attempts; add delay between retries in your code                   |
| `connection.service_unavailable`                | Convai temporarily unavailable (HTTP 503)                 | Yes                   | Wait and retry; SDK backs off automatically                                                      |
| `connection.server_error`                       | Convai returned a 5xx error                               | Yes                   | Transient — SDK retries; check Convai status page if persistent                                  |
| `connection.not_found`                          | Resource (character or room) not found (HTTP 404)         | No                    | Verify Character ID exists on your account                                                       |
| `connection.bad_request`                        | Invalid parameters in the connect request                 | No                    | Check that CharacterId and other connection parameters contain no invalid characters             |
| `connection.connect_validation_error`           | Connect request failed API validation (HTTP 422)          | No                    | Inspect error message for which field failed validation                                          |
| `connection.failed`                             | Generic connection failure not covered by a specific code | Depends               | Check `LastSessionErrorMessage` for details                                                      |

***

### Transport Errors

Transport errors occur at the WebRTC / LiveKit layer, after Convai has accepted the connect request. They are almost always transient and the SDK retries automatically.

| Error Code                         | Description                                            | What to Check                                                                 |
| ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------- |
| `transport.ice_failed`             | WebRTC ICE negotiation failed — peer cannot be reached | Verify the network allows UDP traffic; corporate firewalls often block WebRTC |
| `transport.peer_connection_failed` | WebRTC peer connection could not be established        | Same as ICE failed — check UDP ports and STUN/TURN accessibility              |
| `transport.livekit_error`          | LiveKit SDK reported an error                          | Usually transient; check internet stability                                   |
| `transport.signal_disconnected`    | LiveKit signal server connection dropped               | Usually auto-reconnects; persistent failures indicate network instability     |

{% hint style="info" %}
WebRTC requires UDP ports to be accessible. In corporate deployments, work with your network team to whitelist the Convai LiveKit endpoints. See the Network & API Requirements page for the full list of domains and ports.
{% endhint %}

***

### Server and Usage Errors

| Error Code                   | Description                                         | Fix                                                    |
| ---------------------------- | --------------------------------------------------- | ------------------------------------------------------ |
| `server.usage_limit_reached` | Daily or monthly usage quota exceeded               | Check usage in the Convai dashboard; upgrade your plan |
| `server.fatal_error`         | Fatal pipeline error — session terminated by Convai | Session cannot recover; initiate a new connect         |
| `server.error`               | Non-fatal pipeline error reported by Convai         | SDK retries; if persistent, report to Convai support   |

***

### Session and Protocol Errors

| Error Code                 | Description                                          | Fix                                                               |
| -------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------- |
| `session.token_expired`    | Session token has expired                            | Reconnect to obtain a fresh token                                 |
| `session.invalid_state`    | An operation was attempted in an invalid state       | Check your connect/disconnect call order                          |
| `session.cancelled`        | Session was cancelled by your code                   | Expected if you call `DisconnectAsync` manually                   |
| `protocol.message_invalid` | An invalid protocol message was received from Convai | Usually indicates an SDK/backend version mismatch; update the SDK |
| `protocol.parse_failed`    | SDK could not parse a message from Convai            | Usually indicates an SDK/backend version mismatch; update the SDK |

***

### Retry Behavior

The SDK uses an exponential backoff policy for transient errors. After a failed attempt, it waits before trying again:

| Attempt     | Delay Before This Attempt |
| ----------- | ------------------------- |
| 1 (initial) | None — immediate          |
| 2           | 1 second                  |
| 3           | 2 seconds                 |
| 4 (final)   | 4 seconds                 |

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

***

### Runtime Diagnostics

#### ConvaiRoomManager State Properties

These properties are readable at any time in Play Mode — from a script, an Editor tool, or the Inspector via a debug MonoBehaviour:

| Property                  | Type           | Description                                                                                                |
| ------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------- |
| `CurrentState`            | `SessionState` | Current session state: `Disconnected`, `Connecting`, `Connected`, `Disconnecting`, `Reconnecting`, `Error` |
| `IsConnected`             | `bool`         | `true` when the room is actively connected                                                                 |
| `ConnectAttemptCount`     | `int`          | Total connection attempts since scene load                                                                 |
| `ReconnectCount`          | `int`          | Total reconnection attempts                                                                                |
| `LastSessionErrorCode`    | `string`       | Error code from the most recent failure                                                                    |
| `LastSessionErrorMessage` | `string`       | Human-readable message for the last failure                                                                |

{% hint style="warning" %}
`SessionState.Error` indicates an unrecoverable session failure. The room does not reconnect automatically from this state. Your application must call `DisconnectAsync()` followed by `ConnectAsync()` to reset the session.
{% endhint %}

#### RoomDiagnosticsSnapshot

For more detail, read a full diagnostic snapshot. This is useful when building an in-game debug overlay or logging a support report:

```csharp
using Convai.Runtime.Adapters.Networking;
using Convai.Runtime.Core.Coordinators;
using UnityEngine;

public class DiagnosticsLogger : MonoBehaviour
{
    [ContextMenu("Dump Diagnostics")]
    private void DumpDiagnostics()
    {
        var room = FindFirstObjectByType<ConvaiRoomManager>();
        if (room == null)
        {
            Debug.LogWarning("ConvaiRoomManager not found in scene.");
            return;
        }

        // Quick state
        Debug.Log($"State:            {room.CurrentState}");
        Debug.Log($"Connected:        {room.IsConnected}");
        Debug.Log($"Connect attempts: {room.ConnectAttemptCount}");
        Debug.Log($"Reconnects:       {room.ReconnectCount}");
        Debug.Log($"Last error code:  {room.LastSessionErrorCode}");
        Debug.Log($"Last error msg:   {room.LastSessionErrorMessage}");

        // Full snapshot
        if (room.DiagnosticsCoordinator == null)
        {
            Debug.Log("DiagnosticsCoordinator not yet initialized (room has not connected).");
            return;
        }

        RoomDiagnosticsSnapshot snap = room.DiagnosticsCoordinator.GetDiagnostics();
        Debug.Log($"--- Room Diagnostics Snapshot ---");
        Debug.Log($"Current state:        {snap.CurrentState}");
        Debug.Log($"Total attempts:       {snap.TotalConnectionAttempts}");
        Debug.Log($"Successful:           {snap.SuccessfulConnections}");
        Debug.Log($"Failed:               {snap.FailedConnections}");
        Debug.Log($"Total errors:         {snap.TotalErrors}");
        Debug.Log($"Last connected at:    {snap.LastConnectedAt}");
        Debug.Log($"Last error at:        {snap.LastErrorAt}");
        Debug.Log($"Last error code:      {snap.LastErrorCode}");
        Debug.Log($"Last error message:   {snap.LastErrorMessage}");
        Debug.Log($"Session uptime:       {snap.SessionUptime}");
        Debug.Log($"Characters:           {snap.RegisteredCharacterCount}");
        Debug.Log($"Players:              {snap.RegisteredPlayerCount}");
    }
}
```

#### RoomDiagnosticsSnapshot Field Reference

| Field                      | Type        | Description                                                              |
| -------------------------- | ----------- | ------------------------------------------------------------------------ |
| `CurrentState`             | `string`    | State name at the time of the snapshot                                   |
| `TotalConnectionAttempts`  | `int`       | All connection attempts since the diagnostics instance was created       |
| `SuccessfulConnections`    | `int`       | Attempts that reached the Connected state                                |
| `FailedConnections`        | `int`       | Attempts that ended in failure                                           |
| `TotalErrors`              | `int`       | Errors recorded since diagnostics reset                                  |
| `LastConnectedAt`          | `DateTime?` | UTC timestamp of the last successful connection                          |
| `LastErrorAt`              | `DateTime?` | UTC timestamp of the last recorded error                                 |
| `LastErrorCode`            | `string`    | Error code from the last recorded error                                  |
| `LastErrorMessage`         | `string`    | Human-readable message from the last error                               |
| `SessionUptime`            | `TimeSpan?` | Elapsed time since the current session connected; `null` if disconnected |
| `RegisteredCharacterCount` | `int`       | Number of `ConvaiCharacter` instances currently registered               |
| `RegisteredPlayerCount`    | `int`       | Number of `ConvaiPlayer` instances currently registered                  |

{% hint style="info" %}
`DiagnosticsCoordinator` is `null` until the room has initialized its internal assembly — typically after the first connect attempt. Always null-check before calling `GetDiagnostics()`.
{% endhint %}

***

### Quick Reference: Common Failure Patterns

| Symptom                                       | Likely Cause                       | Fix                                                                                                    |
| --------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `config.api_key_missing` on every connect     | API key never entered              | Edit → Project Settings → Convai SDK → paste key                                                       |
| `connection.connect_invalid_api_key`          | Wrong or revoked API key           | Copy a fresh key from the Convai dashboard                                                             |
| `connection.connect_character_not_found`      | Character ID typo or wrong account | Verify in Convai dashboard; check for copy-paste whitespace                                            |
| `connection.connect_realtime_not_allowed`     | Realtime not enabled on account    | Upgrade plan                                                                                           |
| `connection.timeout` every time               | Firewall blocking connections      | Whitelist Convai domains; try on a different network                                                   |
| `transport.ice_failed` repeatedly             | Strict firewall blocking UDP       | Allow UDP; request TURN relay from network admin                                                       |
| `server.usage_limit_reached`                  | Quota exceeded                     | Check Convai dashboard usage page                                                                      |
| Character connects once then never reconnects | `ReconnectPolicy` maxed out        | SDK stops after 4 failed reconnects; application must call `ConnectAsync` again if user wants to retry |
| `connection.rate_limited`                     | Too many connects in short time    | Add a minimum delay between connect calls in your application logic                                    |
| `CurrentState` stuck at `Error`               | Unrecoverable session failure      | Call `DisconnectAsync()` then `ConnectAsync()` to reset                                                |

***

### Next Steps

For a full reference to the SDK's logging system, built-in diagnostic tools, and session metrics, see the Debug Tools Reference.

{% content-ref url="/broken/pages/173d13efab3adc52c44a199c0a38344e54eb2dfd" %}
[Broken link](/broken/pages/173d13efab3adc52c44a199c0a38344e54eb2dfd)
{% endcontent-ref %}
