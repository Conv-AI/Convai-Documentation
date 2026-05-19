# debug tools reference

The Convai Unity SDK ships with a layered set of diagnostic tools: a configurable logging system with per-subsystem verbosity control, a live Inspector probe for action debugging, real-time session diagnostics on `ConvaiRoomManager`, session metrics emitted to the Console, and client-side latency measurements for conversation pipeline profiling. This page is the complete reference for all of them.

***

## Logging Configuration

### Where to Configure

Open **Edit → Project Settings → Convai SDK → Logging**. The three settings that control what appears in the Unity Console are:

* **Global Log Level** — minimum verbosity that applies to all log categories
* **Category Overrides** — per-subsystem overrides that supersede the global level
* **Include Stack Traces** — whether Warning and Error entries include a stack trace
* **Colored Output** — whether log entries are color-coded in the Unity Console

### Log Levels

The SDK uses five log levels. Higher numeric value means more verbose.

| Level       | Value | What Appears in the Console                        |
| ----------- | ----- | -------------------------------------------------- |
| **Error**   | 1     | Errors only                                        |
| **Warning** | 2     | Errors and Warnings                                |
| **Info**    | 3     | Errors, Warnings, and Info messages _(default)_    |
| **Debug**   | 4     | All of the above plus Debug messages               |
| **Trace**   | 5     | Everything, including fine-grained internal traces |

The default is **Info**. Switching to **Debug** during an investigation produces significantly more output — disable it before releasing to production.

{% hint style="warning" %}
`Debug`-level calls in the SDK source are decorated with `[Conditional("UNITY_EDITOR")]`, `[Conditional("DEVELOPMENT_BUILD")]`, and `[Conditional("CONVAI_DEBUG_LOGGING")]`. This means **Debug log calls are compiled out of non-development builds** unless you add `CONVAI_DEBUG_LOGGING` to your scripting define symbols. Setting `GlobalLogLevel` to `Debug` in a release build will not produce Debug messages because the call sites do not exist in the compiled code.
{% endhint %}

To enable Debug messages in a release build, add `CONVAI_DEBUG_LOGGING` to **Edit → Project Settings → Player → Scripting Define Symbols**.

### Log Category Overrides

Category overrides let you increase verbosity for one subsystem without flooding the Console with output from others. For example, to diagnose a transport issue without seeing audio, UI, and character logs:

1. Go to **Edit → Project Settings → Convai SDK → Logging → Category Overrides**
2. Click **+** to add an override
3. Set **Category** to `Transport` and **Level** to `Debug`

All other categories remain at the global level.

### Log Category Reference

| Category     | Subsystem It Covers                                        |
| ------------ | ---------------------------------------------------------- |
| `SDK`        | General SDK operations and initialization                  |
| `Character`  | Character and NPC lifecycle                                |
| `Audio`      | Audio output and microphone input                          |
| `UI`         | Transcript UI and notification components                  |
| `REST`       | REST API calls to Convai                                   |
| `Transport`  | LiveKit and WebRTC transport layer                         |
| `Events`     | Event relay system (session, character, transcript events) |
| `Player`     | Player identity and input                                  |
| `Editor`     | Editor-only tools and validators                           |
| `Vision`     | Camera capture and video publishing                        |
| `Bootstrap`  | SDK initialization and ConvaiSettings loading              |
| `Transcript` | Transcript processing and routing                          |
| `Narrative`  | Narrative design and story trigger system                  |
| `LipSync`    | Lip sync processing and blendshape playback                |

### Custom Log Sinks

Forward SDK log entries to a custom destination — a file, telemetry service, or in-game debug overlay — by implementing `ILogSink` and registering it with `ConvaiLogger`:

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

```csharp
// Register once, e.g., in a bootstrap MonoBehaviour Awake()
ConvaiLogger.RegisterSink(new FileLogSink(Application.persistentDataPath + "/sdk.log"));
```

Remove a sink when it is no longer needed:

```csharp
ConvaiLogger.UnregisterSink(mySink);
```

`ConvaiLogger.SinkCount` returns the number of currently registered sinks. The default Unity Console sink (`UnityConsoleSink`) is always registered and cannot be removed through the public API.

***

## ConvaiActionDebugProbe

`ConvaiActionDebugProbe` is the primary diagnostic tool for the Actions feature. It subscribes to every dispatcher event and surfaces live counters and the last-seen action data directly in the Inspector — no custom logging required.

**Add via:** Add Component → **Convai/Debug/Convai Action Debug Probe**

The component requires `ConvaiCharacter` on the same GameObject and auto-resolves `ConvaiActionDispatcher`.

### Inspector Fields

| Field                    | Description                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------- |
| **Log To Console**       | When enabled, every action event is printed to the Console with full details. Disable in production. |
| **Received Batch Count** | Total action batches received since Play started                                                     |
| **Started Step Count**   | Total steps the dispatcher has begun executing                                                       |
| **Succeeded Step Count** | Total steps that completed with `Succeeded`                                                          |
| **Failed Step Count**    | Total steps that returned `Failed`, `TimedOut`, or had a missing definition or target                |
| **Unhandled Step Count** | Total steps where the executor returned `Unhandled`                                                  |
| **Aborted Batch Count**  | Total batches stopped early (Stop Batch failure policy)                                              |
| **Last Received Batch**  | JSON of the most recent batch as received from Convai                                                |
| **Last Step Started**    | Details of the most recently started step                                                            |
| **Last Step Succeeded**  | Details of the most recently succeeded step                                                          |
| **Last Unhandled Step**  | Details of the most recently unhandled step                                                          |

### Context Menu Actions

Right-click the `ConvaiActionDebugProbe` component header in the Inspector to access:

| Item                  | What It Does                                                                                                          |
| --------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Inject Test Batch** | Sends a `Move To` action targeting the first registered object — verifies executor wiring without a live conversation |
| **Reset Probe State** | Resets all counters and clears the last-seen text fields                                                              |

{% hint style="info" %}
**Inject Test Batch** is the fastest way to verify executor wiring. If it succeeds, your action definition, object target, and executor are all configured correctly. See [Debugging the Action System](/broken/pages/03fed912c70ba62a24e66d008b4fed7cee615deb) for the full diagnostic checklist.
{% endhint %}

***

## ConvaiRoomManager Runtime State

`ConvaiRoomManager` exposes diagnostic state as plain properties — no event subscription required. Read them from any script, from a `[ContextMenu]` method in the Editor, or from an in-scene debug panel.

### Public State Properties

| Property                  | Type           | Description                                                                                      |
| ------------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `CurrentState`            | `SessionState` | Active session state: `Disconnected`, `Connecting`, `Connected`, `Disconnecting`, `Reconnecting` |
| `IsConnected`             | `bool`         | `true` when the room is actively connected                                                       |
| `ConnectAttemptCount`     | `int`          | Total connection attempts since scene load                                                       |
| `ReconnectCount`          | `int`          | Total reconnection attempts since scene load                                                     |
| `LastSessionErrorCode`    | `string`       | Error code from the most recent error event                                                      |
| `LastSessionErrorMessage` | `string`       | Human-readable message from the most recent error                                                |

### IRoomDiagnostics Full Snapshot

For a richer snapshot, call `GetDiagnostics()` on `ConvaiRoomManager.DiagnosticsCoordinator`. This returns a `RoomDiagnosticsSnapshot` with connection statistics accumulated since the diagnostics instance was created.

```csharp
var room = FindObjectOfType<ConvaiRoomManager>();
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

### RoomDiagnosticsSnapshot Field Reference

| Field                      | Type        | Description                                                                |
| -------------------------- | ----------- | -------------------------------------------------------------------------- |
| `CurrentState`             | `string`    | State name at the moment the snapshot was taken                            |
| `TotalConnectionAttempts`  | `int`       | All connect attempts since startup or last `Reset()`                       |
| `SuccessfulConnections`    | `int`       | Attempts that reached the Connected state                                  |
| `FailedConnections`        | `int`       | Attempts that ended in failure                                             |
| `TotalErrors`              | `int`       | Total errors recorded                                                      |
| `LastConnectedAt`          | `DateTime?` | UTC timestamp of the last successful connection; `null` if never connected |
| `LastErrorAt`              | `DateTime?` | UTC timestamp of the last recorded error; `null` if no errors              |
| `LastErrorCode`            | `string`    | Error code from the last error                                             |
| `LastErrorMessage`         | `string`    | Human-readable message from the last error                                 |
| `SessionUptime`            | `TimeSpan?` | Time elapsed since the current session connected; `null` when disconnected |
| `RegisteredCharacterCount` | `int`       | `ConvaiCharacter` instances currently registered in the agent registry     |
| `RegisteredPlayerCount`    | `int`       | `ConvaiPlayer` instances currently registered                              |

{% hint style="info" %}
`DiagnosticsCoordinator` is `null` until the room's internal assembly has been created, which happens on the first connection attempt. Null-check before calling `GetDiagnostics()`.
{% endhint %}

***

## Session Metrics Console Messages

`SessionMetrics` logs session lifecycle events to the Console. Some messages appear at **Info** level (visible by default); others require the global log level to be set to **Debug**.

| Message                                                                   | Level   | When It Appears                                                   |
| ------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------- |
| `[SessionMetrics] Metrics reset`                                          | Debug   | Metrics were reset programmatically                               |
| `[SessionMetrics] Session started`                                        | Debug   | Session transitions to the Starting state                         |
| `[SessionMetrics] Connected - starting duration timer`                    | Debug   | Session reaches the Connected state                               |
| `[SessionMetrics] Reconnection attempt #N`                                | Debug   | Each reconnection attempt begins                                  |
| `[SessionMetrics] Reconnection successful (attempt #N, success rate: P%)` | Info    | A reconnection attempt succeeded                                  |
| `[SessionMetrics] Reconnection failed (error: X)`                         | Warning | A reconnection attempt failed                                     |
| `[SessionMetrics] Session error: X`                                       | Warning | A non-reconnect session error was recorded                        |
| `[SessionMetrics] Session ended (reason): {snapshot}`                     | Info    | Session terminated for any reason; snapshot includes full metrics |

{% hint style="info" %}
`[SessionMetrics]` messages tagged Debug only appear in the Unity Editor, Development Builds, or builds with the `CONVAI_DEBUG_LOGGING` scripting define. See [Log Levels](debug-tools-reference.md#log-levels) above.
{% endhint %}

***

## Client Latency Metrics

`ClientLatencyMetricsCollector` measures the end-to-end latency of the conversation pipeline from the moment the player stops speaking to the moment the character's audio starts playing. It is active in the Unity Editor and Development Builds.

Latency entries appear automatically in the Console after each completed turn:

```
[ClientLatency] Player: stop→finalTranscript=120ms | Character: stop→firstTranscript=450ms, stop→ttsStarted=520ms, stop→firstLipSync=600ms, stop→audioPlaying=650ms, ttsStart→audioPlaying=130ms
```

### Latency Segment Reference

| Segment                 | What It Measures                                                                         |
| ----------------------- | ---------------------------------------------------------------------------------------- |
| `stop→finalTranscript`  | From the player stopping speech to the final player transcript arriving at the client    |
| `stop→firstTranscript`  | From the player stopping to the first character transcript token arriving                |
| `stop→ttsStarted`       | From the player stopping to Convai beginning text-to-speech synthesis                    |
| `stop→firstLipSync`     | From the player stopping to the first lip sync data frame arriving                       |
| `stop→audioPlaying`     | From the player stopping to the character's audio actually playing through `AudioSource` |
| `ttsStart→audioPlaying` | Time between TTS start and audio playback — represents the audio buffer fill duration    |

### Interpreting the Numbers

| High Segment Value                                        | Likely Cause                                                           |
| --------------------------------------------------------- | ---------------------------------------------------------------------- |
| `stop→firstTranscript` > 500 ms                           | Network latency to Convai; check connection quality                    |
| `stop→ttsStarted` much higher than `stop→firstTranscript` | Convai processing time; expected for complex responses                 |
| `ttsStart→audioPlaying` > 200 ms                          | Audio buffer is large; acceptable but reduces perceived responsiveness |
| `stop→audioPlaying` > 1000 ms                             | Combined network + processing + buffering; investigate each segment    |

{% hint style="info" %}
Latency measurements appear only in Editor and Development Builds — the `[ClientLatency]` log calls are conditionally compiled. They are not available in release builds unless `CONVAI_DEBUG_LOGGING` is defined.
{% endhint %}

***

## Summary

| Tool                             | What It Diagnoses                                            | How to Access                                                        |
| -------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------- |
| **Logging configuration**        | All SDK subsystems — verbosity and filtering                 | Edit → Project Settings → Convai SDK → Logging                       |
| **ConvaiActionDebugProbe**       | Action dispatch, executor wiring, batch failures             | Add Component → Convai/Debug/Convai Action Debug Probe               |
| **ConvaiRoomManager properties** | Session state, error codes, connect/reconnect counts         | `FindObjectOfType<ConvaiRoomManager>()` — read properties directly   |
| **IRoomDiagnostics snapshot**    | Connection attempt counts, uptime, last error, agent counts  | `room.DiagnosticsCoordinator.GetDiagnostics()`                       |
| **Session Metrics messages**     | Reconnection success rate, session lifecycle, error timeline | Console filter `[SessionMetrics]`; requires Info or Debug level      |
| **Client Latency metrics**       | End-to-end conversation pipeline latency                     | Console filter `[ClientLatency]`; Editor and Development Builds only |
| **Custom log sinks**             | Route logs to files, telemetry, or overlays                  | `ConvaiLogger.RegisterSink(new YourSink())`                          |

***

## Next Steps

For platform-specific issues not covered on this page — WebGL AudioContext unlock, Android NDK mic handling, or Meta Quest Vision setup — see the Platform Guides section.

{% content-ref url="/broken/pages/fe37580548ba4d3fbd847afd84065782b15c5fb5" %}
[Broken link](/broken/pages/fe37580548ba4d3fbd847afd84065782b15c5fb5)
{% endcontent-ref %}

For feature-specific diagnostic tools, see the troubleshooting page inside each feature's section. The Actions, Emotion, Vision, and Narrative Design features each have detailed decision trees and console log references beyond what is covered here.
