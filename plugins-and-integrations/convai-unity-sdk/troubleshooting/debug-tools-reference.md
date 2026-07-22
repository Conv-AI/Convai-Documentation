---
title: Debug tools reference
description: Reference for Convai SDK debug tools, including logging configuration, ConvaiActionDebugProbe, session diagnostics, and client latency metrics.
last_reviewed: "4.4.0"
---

The Convai Unity SDK ships with a layered set of diagnostic tools: a configurable logging system with per-subsystem verbosity control, a live Inspector probe for action debugging, real-time session diagnostics on `ConvaiRoomManager`, session metrics emitted to the Console, and client-side latency measurements for conversation pipeline profiling. This page is the complete reference for all of them.

## Diagnostics

{% hint style="warning" %}
SDK `4.4.0` removed the `Convai → Logger Settings` menu and window. Logging configuration now lives in the Diagnostics section, reachable from `Convai → Settings` and from `Edit → Project Settings → Convai SDK`.
{% endhint %}

### Where to configure

Open `Convai → Settings` or `Edit → Project Settings → Convai SDK` and scroll to the **Diagnostics** section. Both entry points render the same `DiagnosticsSectionView`, so a change made in one place shows up in the other. The settings that control what appears in the Unity Console are:

* **Presets** — one-click buttons that set Global Log Level, Include Stack Traces, and Colored Console Output together; see [Logging presets](#logging-presets)
* **Global Log Level** — minimum verbosity that applies to all log categories
* **Include Stack Traces** — whether Warning and Error entries include a stack trace
* **Colored Console Output** — whether log entries are color-coded in the Unity Console
* **Category Overrides** — per-subsystem overrides that supersede the global level

The Diagnostics section header also has its own **Reset** button, which applies the same configuration as the `Default` preset below.

### Logging presets

Three preset buttons sit above the Global Log Level field. Each preset sets the global level and both output flags together, then clears every category override.

| Preset | Global Log Level | Include Stack Traces | Colored Console Output | Category Overrides |
| --- | --- | --- | --- | --- |
| `Verbose` | `Trace` | On | On | Cleared |
| `Default` | `Info` | On | On | Cleared |
| `Errors Only` | `Error` | On | On | Cleared |

`Default` matches the SDK's default logging configuration. Applying any preset overwrites Global Log Level, Include Stack Traces, and Colored Console Output, and removes existing Category Overrides — reapply project-specific overrides after clicking a preset.

### Log levels

The SDK uses five log levels. Higher numeric value means more verbose.

| Level | Value | What appears in the Console |
| --- | --- | --- |
| **Error** | 1 | Errors only |
| **Warning** | 2 | Errors and Warnings |
| **Info** | 3 | Errors, Warnings, and Info messages _(default)_ |
| **Debug** | 4 | All of the above plus Debug messages |
| **Trace** | 5 | Everything, including fine-grained internal traces |

The default is **Info**. Switching to **Debug** during an investigation produces significantly more output — disable it before releasing to production.

{% hint style="warning" %}
`Debug`-level calls in the SDK source are decorated with `[Conditional("UNITY_EDITOR")]`, `[Conditional("DEVELOPMENT_BUILD")]`, and `[Conditional("CONVAI_DEBUG_LOGGING")]`. This means **Debug log calls are compiled out of non-development builds** unless you add `CONVAI_DEBUG_LOGGING` to your scripting define symbols. Setting `GlobalLogLevel` to `Debug` in a release build will not produce Debug messages because the call sites do not exist in the compiled code. Debug messages remain active in the Unity Editor and in Development Builds without any additional defines.
{% endhint %}

To enable Debug messages in a production build, add `CONVAI_DEBUG_LOGGING` to **Edit → Project Settings → Player → Scripting Define Symbols**.

### Log category overrides

Category overrides let you increase verbosity for one subsystem without flooding the Console with output from others. For example, to diagnose a transport issue without seeing audio, UI, and character logs:

1. Open **Diagnostics** and expand the **Category Overrides** foldout — it lists every log category with a dropdown that defaults to `Inherit`
2. Set the `Transport` dropdown to `Debug`

All other categories remain at the global level. The foldout title shows the active override count, for example **Category Overrides (1)**. Set a category's dropdown back to `Inherit` to remove that override.

### Log category reference

| Category | Subsystem it covers |
| --- | --- |
| `SDK` | General SDK operations and initialization |
| `Character` | Character and NPC lifecycle |
| `Audio` | Audio output and microphone input |
| `UI` | Transcript UI and notification components |
| `REST` | REST API calls to Convai |
| `Transport` | LiveKit and WebRTC transport layer |
| `Events` | Event relay system (session, character, transcript events) |
| `Player` | Player identity and input |
| `Editor` | Editor-only tools and validators |
| `Vision` | Camera capture and video publishing |
| `Bootstrap` | SDK initialization and ConvaiSettings loading |
| `Transcript` | Transcript processing and routing |
| `Narrative` | Narrative design and story trigger system |
| `LipSync` | Lip sync processing and blendshape playback |

### Custom log sinks

Forward SDK log entries to a custom destination — a file, telemetry service, or in-game debug overlay — by implementing `ILogSink` and registering it with `ConvaiLogger`.

`ILogSink` requires these members:

| Member | Description |
| --- | --- |
| `string Name { get; }` | Sink identifier shown in diagnostics |
| `bool IsEnabled { get; }` | Returns `false` to pause the sink without unregistering it |
| `void SetEnabled(bool enabled)` | Toggle the sink at runtime |
| `void Write(LogEntry entry)` | Called for each log entry that passes the level filter |
| `void Flush()` | Flush any buffered entries — call before application shutdown |
| `void Dispose()` | Clean up resources when the sink is removed |

{% code title="FileLogSink.cs" %}
```csharp
using System.IO;
using Convai.Domain.Logging;

public class FileLogSink : ILogSink
{
    private readonly string _path;
    private bool _enabled = true;

    public FileLogSink(string path) => _path = path;

    public string Name => "FileLogSink";
    public bool IsEnabled => _enabled;
    public void SetEnabled(bool enabled) => _enabled = enabled;

    public void Write(LogEntry entry)
    {
        string line = $"[{entry.Level}][{entry.Category}] {entry.Message}";
        File.AppendAllText(_path, line + "\n");
    }

    public void Flush() { }
    public void Dispose() { }
}
```
{% endcode %}

Register the sink early — in `Awake()` or a `[RuntimeInitializeOnLoadMethod]` callback — before any Convai component activates. `ConvaiLogger` auto-initializes on first use; sinks registered after initialization only receive subsequent messages.

```csharp
// Register once before any Convai component activates
private void Awake()
{
    ConvaiLogger.RegisterSink(new FileLogSink(Application.persistentDataPath + "/sdk.log"));
}
```

Remove a sink when it is no longer needed:

```csharp
ConvaiLogger.UnregisterSink(mySink);
```

`ConvaiLogger.SinkCount` returns the number of currently registered sinks. The default Unity Console sink (`UnityConsoleSink`) is always registered and cannot be removed through the public API.

## ConvaiActionDebugProbe

`ConvaiActionDebugProbe` is the primary diagnostic tool for the Actions feature. It subscribes to every dispatcher event and surfaces live counters and the last-seen action data directly in the Inspector — no custom logging required.

**Add via:** Add Component → **Convai/Debug/Convai Action Debug Probe**

The component requires `ConvaiCharacter` on the same GameObject and auto-resolves `ConvaiActionDispatcher`. If `ConvaiActionDispatcher` is absent, the probe still records received action batches via `ConvaiCharacter.OnActionsReceived`, but dispatcher lifecycle events (step started, succeeded, failed) will not be tracked.

### Inspector fields

| Field | Description |
| --- | --- |
| **Log To Console** | When enabled, every action event is printed to the Console with full details. Disable in production to avoid log spam. |
| **Received Batch Count** | Total action batches received since Play started |
| **Started Step Count** | Total steps the dispatcher has begun executing |
| **Succeeded Step Count** | Total steps that completed with `Succeeded` |
| **Failed Step Count** | Total steps that returned `Failed`, `TimedOut`, or had a missing definition or target |
| **Unhandled Step Count** | Total steps where the executor returned `Unhandled` |
| **Aborted Batch Count** | Total batches stopped early (Stop Batch failure policy) |
| **Last Received Batch** | JSON of the most recent batch as received from Convai |
| **Last Step Started** | Details of the most recently started step |
| **Last Step Succeeded** | Details of the most recently succeeded step |
| **Last Unhandled Step** | Details of the most recently unhandled step |

### Context menu actions

Right-click the `ConvaiActionDebugProbe` component header in the Inspector to access:

| Item | What it does |
| --- | --- |
| **Inject Test Batch** | Sends a `Move To` action targeting the first registered object — verifies executor wiring without a live conversation |
| **Reset Probe State** | Resets all counters and clears the last-seen text fields |

{% hint style="info" %}
**Inject Test Batch** is the fastest way to verify executor wiring. If it succeeds, your action definition, object target, and executor are all configured correctly. If `Unhandled Step Count` increments instead of `Succeeded Step Count`, an executor for `Move To` is not registered on this GameObject.
{% endhint %}

## ConvaiRoomManager runtime state

`ConvaiRoomManager` exposes diagnostic state as plain properties — no event subscription required. Read them from any script, from a `[ContextMenu]` method in the Editor, or from an in-scene debug panel.

### Public state properties

| Property | Type | Description |
| --- | --- | --- |
| `CurrentState` | `SessionState` | Active session state: `Disconnected`, `Connecting`, `Connected`, `Disconnecting`, `Reconnecting`, `Error` |
| `IsConnected` | `bool` | `true` when the room is actively connected |
| `ConnectAttemptCount` | `int` | Total connection attempts since scene load |
| `ReconnectCount` | `int` | Total reconnection attempts since scene load |
| `LastSessionErrorCode` | `string` | Error code from the most recent error event |
| `LastSessionErrorMessage` | `string` | Human-readable message from the most recent error |

{% hint style="warning" %}
`SessionState.Error` indicates an unrecoverable session failure. The room will not reconnect automatically from this state. Call `DisconnectAsync()` followed by `ConnectAsync()` to reset the session.
{% endhint %}

### IRoomDiagnostics full snapshot

For a richer snapshot, call `GetDiagnostics()` on `ConvaiRoomManager.DiagnosticsCoordinator`. This returns a `RoomDiagnosticsSnapshot` with connection statistics accumulated since the diagnostics instance was created.

```csharp
var room = FindFirstObjectByType<ConvaiRoomManager>();
if (room?.DiagnosticsCoordinator != null)
{
    RoomDiagnosticsSnapshot snap = room.DiagnosticsCoordinator.GetDiagnostics();
    Debug.Log($"State:          {snap.CurrentState}");
    Debug.Log($"Connections:    {snap.SuccessfulConnections} / {snap.TotalConnectionAttempts} succeeded");
    Debug.Log($"Failed:         {snap.FailedConnections}");
    Debug.Log($"Total errors:   {snap.TotalErrors}");
    Debug.Log($"Last connected: {snap.LastConnectedAt}");
    Debug.Log($"Last error:     {snap.LastErrorCode} at {snap.LastErrorAt}");
    Debug.Log($"Uptime:         {snap.SessionUptime}");
    Debug.Log($"Characters:     {snap.RegisteredCharacterCount}");
    Debug.Log($"Players:        {snap.RegisteredPlayerCount}");
}
```

### RoomDiagnosticsSnapshot field reference

| Field | Type | Description |
| --- | --- | --- |
| `CurrentState` | `string` | State name at the moment the snapshot was taken |
| `TotalConnectionAttempts` | `int` | All connect attempts since startup or last reset |
| `SuccessfulConnections` | `int` | Attempts that reached the Connected state |
| `FailedConnections` | `int` | Attempts that ended in failure |
| `TotalErrors` | `int` | Total errors recorded |
| `LastConnectedAt` | `DateTime?` | UTC timestamp of the last successful connection; `null` if never connected |
| `LastErrorAt` | `DateTime?` | UTC timestamp of the last recorded error; `null` if no errors |
| `LastErrorCode` | `string` | Error code from the last error |
| `LastErrorMessage` | `string` | Human-readable message from the last error |
| `SessionUptime` | `TimeSpan?` | Time elapsed since the current session connected; `null` when disconnected |
| `RegisteredCharacterCount` | `int` | `ConvaiCharacter` instances currently registered in the agent registry |
| `RegisteredPlayerCount` | `int` | `ConvaiPlayer` instances currently registered |

{% hint style="info" %}
`DiagnosticsCoordinator` is `null` until the room's internal assembly has been created, which happens on the first connection attempt. Null-check before calling `GetDiagnostics()`.
{% endhint %}

## Session metrics console messages

`SessionMetrics` logs session lifecycle events to the Console. Some messages appear at **Info** level (visible by default); others require the global log level to be set to **Debug**.

| Message | Level | When it appears |
| --- | --- | --- |
| `[SessionMetrics] Metrics reset` | Debug | Metrics were reset programmatically |
| `[SessionMetrics] Session started` | Debug | Initial connection attempt begins (room transitions from Disconnected to Connecting) |
| `[SessionMetrics] Connected - starting duration timer` | Debug | Initial connection reaches Connected state; starts the session uptime timer (reconnects fire "Reconnection successful" instead) |
| `[SessionMetrics] Reconnection attempt #N` | Debug | Each reconnection attempt begins |
| `[SessionMetrics] Reconnection successful (attempt #N, success rate: P%)` | Info | A reconnection attempt succeeded |
| `[SessionMetrics] Reconnection failed (error: X)` | Warning | A reconnection attempt failed |
| `[SessionMetrics] Session error: X` | Warning | A non-reconnect session error was recorded |
| `[SessionMetrics] Session ended (reason): {snapshot}` | Info | Session terminated for any reason; snapshot includes full metrics |

{% hint style="info" %}
`[SessionMetrics]` messages tagged Debug only appear in the Unity Editor, Development Builds, or builds with the `CONVAI_DEBUG_LOGGING` scripting define. See [Log levels](#log-levels) above.
{% endhint %}

## Client latency metrics

`ClientLatencyMetricsCollector` measures the end-to-end latency of the conversation pipeline from the moment the player stops speaking to the moment the character's audio starts playing. It is active in the Unity Editor and Development Builds.

Latency entries appear automatically in the Console after each completed turn:

```text
[ClientLatency] Player: stop→finalTranscript=120ms | Character: stop→firstTranscript=450ms stop→ttsStarted=520ms stop→firstLipSync=600ms stop→audioPlaying=650ms (audioHoldForLipSync=130ms)
```

### Latency segment reference

| Segment | What it measures |
| --- | --- |
| `stop→finalTranscript` | From the player stopping speech to the final player transcript arriving at the client |
| `stop→firstTranscript` | From the player stopping to the first character transcript token arriving |
| `stop→ttsStarted` | From the player stopping to Convai beginning text-to-speech synthesis |
| `stop→firstLipSync` | From the player stopping to the first lip sync data frame arriving |
| `stop→audioPlaying` | From the player stopping to the character's audio actually playing through `AudioSource` |
| `audioHoldForLipSync` | Delta between TTS start and audio playback — the audio buffer fill duration before playback begins |

### Interpreting the numbers

| High segment value | Likely cause |
| --- | --- |
| `stop→firstTranscript` > 500 ms | Network latency to Convai; check connection quality |
| `stop→ttsStarted` much higher than `stop→firstTranscript` | Convai processing time; expected for complex responses |
| `audioHoldForLipSync` > 200 ms | Audio buffer is large; acceptable but reduces perceived responsiveness |
| `stop→audioPlaying` > 1000 ms | Combined network + processing + buffering; investigate each segment |

{% hint style="info" %}
Latency measurements appear only in Editor and Development Builds — the `[ClientLatency]` log calls are conditionally compiled. They are not available in release builds unless `CONVAI_DEBUG_LOGGING` is defined.
{% endhint %}

## Quick reference

| Tool | What it diagnoses | How to access |
| --- | --- | --- |
| **Diagnostics** | All SDK subsystems — verbosity and filtering | `Convai → Settings` or `Edit → Project Settings → Convai SDK` (Diagnostics section) |
| **ConvaiActionDebugProbe** | Action dispatch, executor wiring, batch failures | Add Component → Convai/Debug/Convai Action Debug Probe |
| **ConvaiRoomManager properties** | Session state, error codes, connect/reconnect counts | `FindFirstObjectByType<ConvaiRoomManager>()` — read properties directly |
| **IRoomDiagnostics snapshot** | Connection attempt counts, uptime, last error, agent counts | `room.DiagnosticsCoordinator.GetDiagnostics()` |
| **Session Metrics messages** | Reconnection success rate, session lifecycle, error timeline | Console filter `[SessionMetrics]`; requires Info or Debug level |
| **Client Latency metrics** | End-to-end conversation pipeline latency | Console filter `[ClientLatency]`; Editor and Development Builds only |
| **Custom log sinks** | Route logs to files, telemetry, or overlays | `ConvaiLogger.RegisterSink(new YourSink())` |

## Next steps

For platform-specific issues — WebGL AudioContext unlock, Android microphone handling, or platform build settings — see the Platform Guides section.

{% content-ref url="../platform-guides/README.md" %}
[Platform guides](../platform-guides/README.md)
{% endcontent-ref %}

For feature-specific diagnostic tools, see the troubleshooting page inside each feature's section. The Actions, Emotion, Vision, and Narrative Design features each have detailed decision trees and console log references beyond what is covered here.
