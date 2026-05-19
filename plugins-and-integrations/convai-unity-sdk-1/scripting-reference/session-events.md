---
description: >-
  Reference for session-level events — connection state, errors, idle warnings,
  and participant changes — via ConvaiSessionEventRelay or the typed
  ConvaiEvents C# hub.
---

# Session Events

## Subscribe to Session Events From C# and the Inspector

The SDK exposes session-level events through two wiring approaches that you can use independently or together. `ConvaiSessionEventRelay` is a MonoBehaviour that wires events to Inspector-assigned `UnityEvent` callbacks with no code required. `ConvaiEvents` is a C# typed event hub accessible from any script via `ConvaiManager.ActiveManager.Events`.

Both approaches fire on the same underlying SDK events — choose based on what your code needs. For a conceptual overview of relay components and when to choose each approach, see [Event System](/broken/pages/5ffdf62f8c66048a351a441887b656b3b3c4c917).

***

## Inspector Wiring — `ConvaiSessionEventRelay`

{% tabs %}
{% tab title="Inspector" %}
**Setup:**

1. Add `ConvaiSessionEventRelay` to any GameObject in your scene via **Add Component → Convai → Events → Convai Session Event Relay**.
2. Assign a `ConvaiManager` reference in the **Manager** field, or leave it empty and enable **Auto Resolve Manager** to use `ConvaiManager.ActiveManager` at runtime.
3. Wire your callbacks in the Inspector under each event.

{% hint style="warning" %}
**Auto Resolve Manager** is convenient but non-deterministic. For scenes with multiple `ConvaiManager` instances, assign the target manager explicitly.
{% endhint %}
{% endtab %}

{% tab title="Scripting" %}
```csharp
using Convai.Runtime.Facades;
using UnityEngine;

public class SessionStatusMonitor : MonoBehaviour
{
    private void OnEnable()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null) return;

        manager.Events.OnConnected    += HandleConnected;
        manager.Events.OnDisconnected += HandleDisconnected;
        manager.Events.OnSessionError += HandleError;
    }

    private void OnDisable()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null) return;

        manager.Events.OnConnected    -= HandleConnected;
        manager.Events.OnDisconnected -= HandleDisconnected;
        manager.Events.OnSessionError -= HandleError;
    }

    private void HandleConnected()             => Debug.Log("Session connected.");
    private void HandleDisconnected()          => Debug.Log("Session disconnected.");
    private void HandleError(SessionError err) => Debug.LogError($"[{err.ErrorCode}] {err.Message}");
}
```
{% endtab %}
{% endtabs %}

***

## `ConvaiSessionEventRelay` — All Events

| Event                   | Argument                       | Fires When                                                             |
| ----------------------- | ------------------------------ | ---------------------------------------------------------------------- |
| `OnConnected`           | —                              | Session transitions to `Connected`                                     |
| `OnDisconnected`        | —                              | Session transitions to `Disconnected`                                  |
| `OnReconnecting`        | —                              | Session transitions to `Reconnecting`                                  |
| `OnReconnected`         | —                              | Reconnection succeeds (transitions from `Reconnecting` to `Connected`) |
| `OnUsageLimitReached`   | —                              | Convai reports quota exhausted                                         |
| `OnSessionStateChanged` | `SessionStateChangedRelayData` | Any `SessionState` transition                                          |
| `OnSessionError`        | `SessionErrorRelayData`        | Session encounters an error                                            |

### `SessionStateChangedRelayData` Fields

| Field                      | Type           | Description                                                |
| -------------------------- | -------------- | ---------------------------------------------------------- |
| `OldState`                 | `SessionState` | State before the transition                                |
| `NewState`                 | `SessionState` | State after the transition                                 |
| `SessionId`                | `string`       | Current session identifier                                 |
| `ErrorCode`                | `string`       | Error code if new state is `Error`; empty otherwise        |
| `IsError`                  | `bool`         | True when `NewState == Error`                              |
| `IsReconnecting`           | `bool`         | True when transitioning from `Connected` to `Reconnecting` |
| `IsConnectionEstablished`  | `bool`         | True when transitioning from `Connecting` to `Connected`   |
| `IsReconnectionSuccessful` | `bool`         | True when transitioning from `Reconnecting` to `Connected` |
| `IsDisconnected`           | `bool`         | True when `NewState == Disconnected`                       |

### `SessionErrorRelayData` Fields

| Field               | Type                | Description                                                           |
| ------------------- | ------------------- | --------------------------------------------------------------------- |
| `ErrorCode`         | `string`            | Hierarchical error code, e.g. `"connection.timeout"`                  |
| `Message`           | `string`            | Human-readable error description                                      |
| `SessionId`         | `string`            | Session identifier at the time of the error                           |
| `IsRecoverable`     | `bool`              | True if the SDK can attempt reconnection automatically                |
| `Stage`             | `SessionErrorStage` | Broad lifecycle stage where the error originated                      |
| `HttpStatusCode`    | `int`               | HTTP status code if the error came from an HTTP response; 0 otherwise |
| `HasHttpStatusCode` | `bool`              | True when `HttpStatusCode > 0`                                        |

***

## C# Event Hub — `ConvaiEvents`

Access via `ConvaiManager.ActiveManager.Events`. Subscribe in `OnEnable`, unsubscribe in `OnDisable`.

### Session-Scoped Events

| Event                               | Argument Type                     | Fires When                                                                   |
| ----------------------------------- | --------------------------------- | ---------------------------------------------------------------------------- |
| `OnConnected`                       | —                                 | Session reaches `Connected`                                                  |
| `OnDisconnected`                    | —                                 | Session reaches `Disconnected`                                               |
| `OnSessionStateChanged`             | `SessionStateChanged`             | Any `SessionState` transition                                                |
| `OnSessionError`                    | `SessionError`                    | Session encounters an error                                                  |
| `OnPipelineError`                   | `SessionError`                    | Processing pipeline encounters an error (distinct from session-level errors) |
| `OnUsageLimitReached`               | `UsageLimitReached`               | Convai reports quota exhausted                                               |
| `OnUserIdleWarningReceived`         | `UserIdleWarningReceived`         | Convai warns the session will close due to inactivity                        |
| `OnParticipantJoined`               | `ParticipantInfo`                 | A participant joins the room                                                 |
| `OnParticipantLeft`                 | `ParticipantInfo`                 | A participant leaves the room                                                |
| `OnRoomOwnershipRebindStateChanged` | `RoomOwnershipRebindStateChanged` | Active character ownership rebinding changes state                           |

### Domain Event Payload Types

#### `SessionStateChanged`

| Field       | Type            | Description                                         |
| ----------- | --------------- | --------------------------------------------------- |
| `OldState`  | `SessionState`  | State before the transition                         |
| `NewState`  | `SessionState`  | State after the transition                          |
| `SessionId` | `string`        | Session identifier                                  |
| `Timestamp` | `DateTime`      | UTC time of the transition                          |
| `Error`     | `SessionError?` | Present when `NewState == Error`                    |
| `ErrorCode` | `string`        | Shortcut to `Error?.ErrorCode`; empty when no error |

#### `UsageLimitReached`

| Field       | Type       | Description                                          |
| ----------- | ---------- | ---------------------------------------------------- |
| `QuotaType` | `string`   | Which quota was exhausted (e.g. `"monthly_minutes"`) |
| `Message`   | `string`   | Human-readable description from Convai               |
| `Timestamp` | `DateTime` | UTC time of the event                                |

#### `UserIdleWarningReceived`

| Field              | Type       | Description                                               |
| ------------------ | ---------- | --------------------------------------------------------- |
| `RemainingSeconds` | `int`      | Seconds until Convai closes the session due to inactivity |
| `Message`          | `string`   | Human-readable warning message                            |
| `Timestamp`        | `DateTime` | UTC time of the event                                     |

#### `ParticipantInfo`

| Field             | Type              | Description                                                            |
| ----------------- | ----------------- | ---------------------------------------------------------------------- |
| `ParticipantId`   | `string`          | Unique participant identifier                                          |
| `Identity`        | `string`          | Identity string associated with this participant                       |
| `DisplayName`     | `string`          | Human-readable display name                                            |
| `ParticipantType` | `ParticipantType` | Whether the participant is a local player, remote player, or character |
| `IsLocal`         | `bool`            | True for the local player participant                                  |
| `IsMuted`         | `bool`            | True when this participant's audio is muted                            |

#### `RoomOwnershipRebindStateChanged`

| Field                  | Type                        | Description                                              |
| ---------------------- | --------------------------- | -------------------------------------------------------- |
| `Outcome`              | `RoomOwnershipRebindStatus` | Result of the rebind attempt                             |
| `HasPendingReconnect`  | `bool`                      | True when a reconnect is required to complete the rebind |
| `SessionState`         | `SessionState`              | Session state at the time of the event                   |
| `ActiveCharacterId`    | `string`                    | Character ID currently bound for conversation            |
| `RequestedCharacterId` | `string`                    | Character ID that was requested for rebind               |
| `Timestamp`            | `DateTime`                  | UTC time of the event                                    |
| `ReconnectRequired`    | `bool`                      | True when ownership change requires session reconnection |

***

## Supporting Types

### `SessionState` Enum

| Value               | Description                                                                |
| ------------------- | -------------------------------------------------------------------------- |
| `Disconnected` (0)  | No active session. Initial state and final state after a clean disconnect. |
| `Connecting` (1)    | Attempting to establish a new session.                                     |
| `Connected` (2)     | Session is active and accepting input.                                     |
| `Reconnecting` (3)  | Connection was lost; the SDK is attempting to restore it automatically.    |
| `Disconnecting` (4) | Gracefully closing the session.                                            |
| `Error` (5)         | Unrecoverable error. Session cannot continue without explicit reset.       |

**Extension Methods** (on `SessionState`):

| Method              | Returns `true` When                                       |
| ------------------- | --------------------------------------------------------- |
| `IsConnected()`     | State is `Connected` or `Reconnecting`                    |
| `IsTransitioning()` | State is `Connecting`, `Reconnecting`, or `Disconnecting` |
| `IsStable()`        | State is `Disconnected`, `Connected`, or `Error`          |
| `CanAcceptInput()`  | State is `Connected` only                                 |

### `SessionErrorStage` Enum

| Value                 | Description                                                |
| --------------------- | ---------------------------------------------------------- |
| `Unknown` (0)         | Error stage could not be determined                        |
| `Configuration` (1)   | Error occurred while reading or applying SDK configuration |
| `ConnectApi` (2)      | Error during API connection setup                          |
| `Transport` (3)       | Error in the transport layer (WebSocket, gRPC)             |
| `SessionRecovery` (4) | Error during reconnection attempt                          |
| `Runtime` (5)         | Error during an active session                             |

### `ParticipantType` Enum

| Value              | Description                              |
| ------------------ | ---------------------------------------- |
| `Unknown` (0)      | Participant type not determined          |
| `LocalPlayer` (1)  | The local player on this client          |
| `RemotePlayer` (2) | A remote player in a multiplayer session |
| `Character` (3)    | An AI character                          |

### `RoomOwnershipRebindStatus` Enum

| Value                          | Description                                                   |
| ------------------------------ | ------------------------------------------------------------- |
| `DeferredUntilStartup` (0)     | Rebind queued; will apply once the runtime starts             |
| `AppliedImmediately` (1)       | Rebind applied without requiring reconnection                 |
| `PendingReconnect` (2)         | Rebind staged; requires reconnection to take effect           |
| `RejectedTransitionState` (3)  | Rejected because the session is currently transitioning       |
| `RejectedInvalidOwnership` (4) | Rejected because the requested character is not a valid owner |

### `SessionError` Struct

The full error detail type, used as the argument to `OnSessionError` and `OnPipelineError` in the C# hub, and exposed via `SessionErrorRelayData` in the relay.

| Member              | Type                | Description                                                                    |
| ------------------- | ------------------- | ------------------------------------------------------------------------------ |
| `ErrorCode`         | `string`            | Hierarchical code, e.g. `"connection.timeout"`, `"transport.closed"`           |
| `Message`           | `string`            | Human-readable description                                                     |
| `SessionId`         | `string`            | Session identifier at time of error                                            |
| `Timestamp`         | `DateTime`          | UTC time the error occurred                                                    |
| `IsRecoverable`     | `bool`              | True when the SDK will attempt automatic recovery                              |
| `Exception`         | `Exception`         | Underlying exception, if any                                                   |
| `Stage`             | `SessionErrorStage` | Lifecycle stage where the error originated                                     |
| `HttpStatusCode`    | `int?`              | HTTP status code for API-layer errors                                          |
| `Category`          | `string`            | First segment of `ErrorCode` (e.g. `"connection"` from `"connection.timeout"`) |
| `IsConnectionError` | `bool`              | True when `ErrorCode` starts with `"connection."`                              |
| `IsSessionError`    | `bool`              | True when `ErrorCode` starts with `"session."`                                 |
| `IsTransportError`  | `bool`              | True when `ErrorCode` starts with `"transport."`                               |
| `IsProtocolError`   | `bool`              | True when `ErrorCode` starts with `"protocol."`                                |
| `IsServerError`     | `bool`              | True when `ErrorCode` starts with `"server."`                                  |

***

## Advanced — `ConvaiEvents.Raw` Event Hub

{% hint style="warning" %}
This is an advanced pattern. Use the typed properties on `ConvaiEvents` for all common scenarios.
{% endhint %}

`ConvaiEvents.Raw` exposes the underlying `IEventHub`, which lets you subscribe to any domain event type that has no corresponding typed property on `ConvaiEvents`.

The raw hub uses a token-based subscription model. **Losing the token causes a memory leak** — the hub holds a reference to the adapter until explicitly unsubscribed.

```csharp
using Convai.Domain.DomainEvents.Session;
using Convai.Domain.EventSystem;
using UnityEngine;

public class RawHubExample : MonoBehaviour
{
    private SubscriptionToken _token;

    private void OnEnable()
    {
        var hub = ConvaiManager.ActiveManager?.Events?.Raw;
        if (hub == null) return;

        _token = hub.Subscribe<SessionStateChanged>(
            e => Debug.Log($"Raw hub: {e.OldState} → {e.NewState}"),
            EventDeliveryPolicy.MainThread);
    }

    private void OnDisable()
    {
        ConvaiManager.ActiveManager?.Events?.Raw?.Unsubscribe(_token);
        _token = default;
    }
}
```

**`EventDeliveryPolicy` Options:**

| Value                  | When to Use                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| `MainThread` (default) | All Unity API access — delivered on the next Unity `Update` tick |
| `Background`           | Non-Unity thread-safe logging or metrics                         |
| `Immediate`            | Synchronous delivery on the publishing thread (use with caution) |

***

## Usage Examples

### Example 1 — Proctor HUD That Dims On Disconnect

A training simulation shows a proctor overlay that dims when the session drops, giving learners a clear visual signal that the AI character is unavailable.

```csharp
using Convai.Domain.DomainEvents.Session;
using Convai.Runtime.Facades;
using UnityEngine;

public class ProctorHUD : MonoBehaviour
{
    [SerializeField] private CanvasGroup _overlay;

    private void OnEnable()
    {
        var mgr = ConvaiManager.ActiveManager;
        if (mgr == null) return;
        mgr.Events.OnConnected           += OnConnected;
        mgr.Events.OnDisconnected        += OnDisconnected;
        mgr.Events.OnSessionStateChanged += OnSessionStateChanged;
    }

    private void OnDisable()
    {
        var mgr = ConvaiManager.ActiveManager;
        if (mgr == null) return;
        mgr.Events.OnConnected           -= OnConnected;
        mgr.Events.OnDisconnected        -= OnDisconnected;
        mgr.Events.OnSessionStateChanged -= OnSessionStateChanged;
    }

    private void OnConnected()    => SetAlpha(1f);
    private void OnDisconnected() => SetAlpha(0.3f);

    private void OnSessionStateChanged(SessionStateChanged e)
    {
        if (e.NewState == SessionState.Reconnecting)
            SetAlpha(0.6f);
    }

    private void SetAlpha(float a) => _overlay.alpha = a;
}
```

### Example 2 — Session Error Banner With Recoverability Branch

A corporate onboarding simulation displays a dismissible error banner. Recoverable errors show a "reconnecting…" message; unrecoverable errors prompt the trainee to reload the module.

```csharp
using Convai.Domain.DomainEvents.Session;
using Convai.Runtime.Facades;
using TMPro;
using UnityEngine;

public class ErrorBanner : MonoBehaviour
{
    [SerializeField] private GameObject _bannerRoot;
    [SerializeField] private TMP_Text   _messageLabel;
    [SerializeField] private GameObject _reloadButton;

    private void OnEnable()  => ConvaiManager.ActiveManager?.Events.OnSessionError += ShowError;
    private void OnDisable() => ConvaiManager.ActiveManager?.Events.OnSessionError -= ShowError;

    private void ShowError(SessionError err)
    {
        _bannerRoot.SetActive(true);
        _messageLabel.text = err.IsRecoverable
            ? "Connection interrupted. Reconnecting…"
            : $"Session error: {err.Message}. Please reload the module.";
        _reloadButton.SetActive(!err.IsRecoverable);
    }
}
```

### Example 3 — Idle Warning Countdown Timer

A medical training simulation shows a countdown when Convai warns the session will close, giving learners time to resume before the AI character disconnects.

```csharp
using Convai.Domain.DomainEvents.Session;
using Convai.Runtime.Facades;
using System.Collections;
using TMPro;
using UnityEngine;

public class IdleCountdown : MonoBehaviour
{
    [SerializeField] private TMP_Text _countdownLabel;

    private Coroutine _countdown;

    private void OnEnable()  => ConvaiManager.ActiveManager?.Events.OnUserIdleWarningReceived += StartCountdown;
    private void OnDisable() => ConvaiManager.ActiveManager?.Events.OnUserIdleWarningReceived -= StartCountdown;

    private void StartCountdown(UserIdleWarningReceived e)
    {
        if (_countdown != null) StopCoroutine(_countdown);
        _countdown = StartCoroutine(CountdownRoutine(e.RemainingSeconds));
    }

    private IEnumerator CountdownRoutine(int seconds)
    {
        while (seconds > 0)
        {
            _countdownLabel.text = $"Session closes in {seconds}s";
            yield return new WaitForSeconds(1f);
            seconds--;
        }
        _countdownLabel.text = string.Empty;
    }
}
```

***

## Troubleshooting

| Symptom                                                    | Likely Cause                                         | Fix                                                                                                |
| ---------------------------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `OnSessionError` never fires                               | Subscribed after connect attempt; missed the event   | Subscribe in `OnEnable`, ensure `OnEnable` runs before `ConnectAsync`                              |
| `ConvaiSessionEventRelay` callbacks not invoked            | Manager not assigned and `AutoResolveManager` is off | Enable **Auto Resolve Manager** or assign the `ConvaiManager` field                                |
| Session stuck in `Reconnecting` indefinitely               | Server unreachable or retry limit hit                | Check network; listen to `OnSessionError` with `IsRecoverable == false` to detect terminal failure |
| `OnConnected` fires but `CanAcceptInput()` returns `false` | State check called during a transition               | Evaluate `CanAcceptInput()` inside the `OnConnected` handler, not in `Update`                      |

***

## Next Steps

With session events wired, move to [Character Events](/broken/pages/441e0a9c27e1e102f3b91a7c1a16c119a5e26148) to respond to speech, emotion, and turn lifecycle. For connection control from script, see [ConvaiManager API](/broken/pages/564f314eec17c428b3dab299640bba82bd89e9e7).
