---
title: Debug tools reference
description: Reference for Convai SDK debug tools, including the Troubleshooter, per-module editor windows, logging, and client latency metrics.
last_reviewed: "5.0.0-preview"
---

The Convai Unity SDK ships with a layered set of diagnostic tools: the Convai Troubleshooter, per-module editor windows, a configurable logging system with per-subsystem verbosity control, a live Inspector probe for action debugging, real-time session diagnostics on `ConvaiRoomManager`, session metrics emitted to the Console, and client-side latency measurements for conversation pipeline profiling. This page is the complete reference for all of them.

## Convai Troubleshooter

`Convai → Troubleshooter` reports what is stopping a `ConvaiCharacter` from working, module by module, with a fix beside each finding. Start here before the tools further down this page — most setup mistakes surface in the Troubleshooter with a one-click fix, without needing a Console search.

{% content-ref url="convai-troubleshooter.md" %}
[Convai Troubleshooter](convai-troubleshooter.md)
{% endcontent-ref %}

## Per-module editor windows

Each embodiment module and Actions has its own authoring and diagnostic window, reached from the `Convai` menu:

| Window | Menu path | What it shows |
| --- | --- | --- |
| Actions Editor | `Convai → Actions Editor` | Authoring, testing, and a **Live** tab — the batch in progress, a timeline of recent batches with each step's duration and outcome, the merged target registry, and per-action insights |
| Embodiment Editor | `Convai → Embodiment Editor` | **Setup**, **Presets**, and **Live** tabs for a character's embodiment stack |
| Gaze Editor | `Convai → Gaze Editor` | Setup and tuning for the Gaze module |
| Body Animation Editor | `Convai → Body Animation Editor` | Setup and tuning for the Body Animation module |
| Emotion Editor | `Convai → Emotion Editor` | Setup, the resolved expression mapping for the character's face, and a live view in Play mode |

## Diagnostics

Logging configuration lives in the Diagnostics section, reachable from `Convai → Settings` and from `Edit → Project Settings → Convai SDK`.

### Where to configure

Open `Convai → Settings` or `Edit → Project Settings → Convai SDK` and scroll to the **Diagnostics** section. Both entry points render the same `DiagnosticsSectionView`, so a change made in one place shows up in the other. The settings that control what appears in the Unity Console are:

* **Presets** — one-click buttons that set Global Log Level, Stack Trace Levels, and Colored Console Output together; see [Logging presets](#logging-presets)
* **Global Log Level** — minimum verbosity that applies to all log categories
* **Stack Trace Levels** — a severity mask selecting which entries include stack traces
* **Colored Console Output** — whether log entries are color-coded in the Unity Console
* **Category Overrides** — per-subsystem overrides that supersede the global level

The Diagnostics section header also has its own **Reset** button, which applies the same configuration as the `Default` preset below.

### Logging presets

Three preset buttons sit above the Global Log Level field. Each preset sets the global level, stack-trace mask, and color flag together, then clears every category override.

| Preset | Global Log Level | Stack Trace Levels | Colored Console Output | Category Overrides |
| --- | --- | --- | --- | --- |
| `Verbose` | `Trace` | `Warning` + `Error` | On | Cleared |
| `Default` | `Info` | `Error` | On | Cleared |
| `Errors Only` | `Error` | `Warning` + `Error` | On | Cleared |

`Default` matches the SDK's default logging configuration. Applying any preset overwrites Global Log Level, Stack Trace Levels, and Colored Console Output, and removes existing Category Overrides — reapply project-specific overrides after clicking a preset.

### Log levels

The SDK uses six log levels. Higher numeric value means more verbose.

| Level | Value | What appears in the Console |
| --- | --- | --- |
| **Off** | 0 | Nothing — silences all SDK logging |
| **Error** | 1 | Errors only |
| **Warning** | 2 | Errors and Warnings |
| **Info** | 3 | Errors, Warnings, and Info messages _(default)_ |
| **Debug** | 4 | All of the above plus Debug messages |
| **Trace** | 5 | Everything, including fine-grained internal traces |

The default is **Info**. Switching to **Debug** during an investigation produces significantly more output — disable it before releasing to production. Set **Global Log Level** to **Off** to silence all SDK logging.

{% hint style="warning" %}
`Debug`-level calls in the SDK source are decorated with `[Conditional("UNITY_EDITOR")]`, `[Conditional("DEVELOPMENT_BUILD")]`, and `[Conditional("CONVAI_DEBUG_LOGGING")]`. This means **Debug log calls are compiled out of non-development builds** unless you add `CONVAI_DEBUG_LOGGING` to your scripting define symbols. Setting `GlobalLogLevel` to `Debug` in a release build will not produce Debug messages because the call sites do not exist in the compiled code. Debug messages remain active in the Unity Editor and in Development Builds without any additional defines. This applies to Debug-tagged `[SessionMetrics]` lines. `[ClientLatency]` summaries use Info level and have a separate room debug-mode gate.
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
| `Animation` | Body animation system (layers, transitions, locomotion) |
| `Gaze` | Gaze system (targeting, policy, eye/head/body solvers) |
| `BodyLanguage` | Body language system (gesticulation, posture, breathing, fidgets) |
| `Actions` | Action system: which commands arrived, which were dropped and why, and how targets resolved |

### Custom log sinks

Forward SDK log entries to a custom destination — a file, telemetry service, or in-game debug overlay — by implementing `ILogSink` and registering it with `ConvaiLogger`.

`ILogSink` requires these members:

| Member | Description |
| --- | --- |
| `string Name { get; }` | Sink identifier shown in diagnostics |
| `bool IsEnabled { get; }` | Returns `false` to pause the sink without unregistering it |
| `void SetEnabled(bool enabled)` | Toggle the sink at runtime |
| `void Write(in LogEntry entry)` | Called for each log entry that passes the level filter |
| `bool IsEnabledFor(LogLevel level, LogCategory category)` | Thread-safe, nonblocking per-entry filter |
| `void Flush()` | Flush any buffered entries — call before application shutdown |
| `void Dispose()` | Clean up resources when the sink is removed |

{% code title="FileLogSink.cs" %}
```csharp
using System.IO;
using Convai.Domain.Logging;

public class FileLogSink : ILogSink
{
    private readonly string _path;
    private volatile bool _enabled = true;

    public FileLogSink(string path) => _path = path;

    public string Name => "FileLogSink";
    public bool IsEnabled => _enabled;
    public void SetEnabled(bool enabled) => _enabled = enabled;

    public bool IsEnabledFor(LogLevel level, LogCategory category) => _enabled;

    public void Write(in LogEntry entry)
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
// Method inside your MonoBehaviour, with Convai.Runtime.Logging imported.
private void Awake()
{
    ConvaiLogger.RegisterSink(new FileLogSink(UnityEngine.Application.persistentDataPath + "/sdk.log"));
}
```

Remove a sink when it is no longer needed:

```csharp
ConvaiLogger.UnregisterSink(mySink);
```

`ConvaiLogger.SinkCount` returns the number of currently registered sinks. `ClearSinks()` retires all registered sinks, including `UnityConsoleSink`. It is restored at the next subsystem-registration reset, not by merely reading a logger again. A sink that throws three consecutive delivery/filter failures stops receiving entries. Re-registering an active instance resets its failure count; an unregistered or cleared instance is retired and cannot be registered again. Create a fresh instance after retirement.

## ConvaiActionDebugProbe

`ConvaiActionDebugProbe` is the primary diagnostic tool for the Actions feature. It subscribes to every dispatcher event and surfaces live counters and the last-seen action data directly in the Inspector — no custom logging required. The component's Add Component entry is **Convai/Actions/Diagnostics/Convai Action Monitor**; its Inspector title is **Action Monitor**.

**Add via:** Add Component → **Convai/Actions/Diagnostics/Convai Action Monitor**

The component requires `ConvaiCharacter` on the same GameObject and auto-resolves `ConvaiActionDispatcher`. If `ConvaiActionDispatcher` is absent, the probe still records received action batches via `ConvaiCharacter.OnActionsReceived`, but dispatcher lifecycle events (step started, succeeded, failed) will not be tracked.

### Inspector fields and activity

The authored fields are **Character**, **Action Runner**, and **Log To Console**. Character and runner references resolve from the same object when left empty. Runtime counters and last-seen payloads are hidden serialized fields, presented through the **Activity** section rather than editable Inspector fields.

Activity includes **Batch Received**, **Step Started**, **Step Succeeded**, **Step Failed**, **Step Unhandled**, **Step Completed**, and **Batch Aborted**. The Inspector provides **Clear** to reset recorded state and **Copy** to copy its activity text.

`InjectTestBatch()` and `ResetProbeState()` are public methods, not component context-menu entries. Invoke them from your own development UI or use the Actions Editor's test workflow. A synthetic batch tests local dispatcher/executor wiring; it does not verify that Convai generated or delivered an action.

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

For a richer snapshot, call `GetDiagnostics()` on `ConvaiRoomManager.DiagnosticsCoordinator`. This returns a `RoomDiagnosticsSnapshot` with connection statistics accumulated since the diagnostics instance was created. `DiagnosticsCoordinator` is `null` until the room's internal assembly has been created, which happens on the first connection attempt — null-check before calling `GetDiagnostics()`.

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

## Session metrics console messages

`SessionMetrics` logs session lifecycle events to the Console. Messages tagged Debug follow the same conditional-compilation rule as every other Debug-level log call — see the [Log levels](#log-levels) hint above.

The standard logger format is `[HH:mm:ss.fff][Level][Category][optional-correlation]: [SourceFileName] message`. Some direct native or Editor messages bypass this format. The messages below are the message body that follows that prefix — search the Console for the message text, not the full line.

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

## Client latency metrics

`ClientLatencyMetricsCollector` records client observation timestamps while the room manager's debug mode is enabled. Its summary uses Info logging, so it is not compiled out by the Debug-log build defines. Enable the room's debug option before connection and allow Info output for the relevant category.

A file writer is created at room composition when debug mode is on. It writes `ConvaiDebugMetrics_<yyyy-MM-dd>.txt` under `UnityEngine.Application.persistentDataPath`. The Console reports the selected path. Enabling collection later does not retroactively create that composition-time file writer.

A summary can contain these segments; fields are omitted when their signals were not observed:

| Segment | Client-observed interval |
| --- | --- |
| `stop→finalTranscript` | Player stop to final player transcript |
| `stop→firstTranscript` | Player stop to first character transcript |
| `stop→ttsStarted` | Player stop to the TTS-start notification |
| `stop→firstLipSync` | Player stop to first lip-sync data |
| `stop→audioPlaying` | Player stop to playback notification |
| `ttsNotificationToPlaybackNotification` | TTS-start notification to playback notification |

The last interval is not a direct audio-buffer-fill or DAC measurement. Compare observations from the same client and investigate missing or delayed signals before attributing the difference to a particular service.

The metrics file uses names such as `stopToFinalPlayer_ms`, `stopToFirstCharTranscript_ms`, `stopToTtsStarted_ms`, `stopToFirstLipSync_ms`, `stopToAudioPlaying_ms`, and `ttsNotificationToPlaybackNotification_ms`. Optional `ClientBargeIn` details describe local interruption-detector activity. `[ClientBargeIn]` debug lines still follow the Debug-log build and level filters.

## LipSync drift monitor

Custom runtime sink injection is not supported — the SDK has no public extension seam for it. Drive lip sync through a supported map or profile on `ConvaiLipSyncComponent` instead. The related types `SkinnedMeshBlendshapeSink`, `LipSyncDriftMonitor`, `LipSyncDriftSample`, and `LipSyncDriftEvent` exist in the SDK but are internal, not part of the public API.

Open the drift monitor from a character's `ConvaiLipSyncComponent` Inspector: select **Open Drift Monitor** near the latency settings. The window opens titled **LipSync Drift**.

Monitoring is opt-in: enable the **Monitor** toggle, enter Play mode, and talk to a character to populate data. Select a character from the dropdown when more than one is registered — samples and events are tracked per character.

The window shows:

* The live drift error, in milliseconds, between the measured audio playhead and the visual (blendshape) clock; a positive value means the mouth is behind the audio
* A chart plotting drift error and the monitor's cumulative correction over a configurable time window (3-30 seconds), with lifecycle event markers overlaid
* Mean absolute error, max absolute error, and the correction rate, computed over the visible window
* A live audio/visual offset override slider for calibrating perceived sync by eye
* An event log listing lifecycle events (for example gate open, anchor, cancel) with timestamps

Click **Export CSV** to save the current samples and events to a file. The save dialog title is **Export drift samples**, and the default file name is `lipsync-drift-<characterId>.csv`. The exported file contains a sample table with columns `time_s`, `error_ms`, `audio_target_s`, `visual_clock_s`, `cumulative_correction_ms`, `buffered_s`, `headroom_s`, `state`, and `audio_active`, followed by a blank line and an event table with columns `event_time_s` and `label`.

## Quick reference

| Tool | What it diagnoses | How to access |
| --- | --- | --- |
| **Convai Troubleshooter** | Cross-module findings for one character or the whole scene, with fixes | `Convai → Troubleshooter` |
| **Actions Editor (Live)** | Action batches, target registry, and per-action insights in Play mode | `Convai → Actions Editor` |
| **Embodiment / Gaze / Body Animation / Emotion Editors** | Setup and tuning for each embodiment module | `Convai → Embodiment Editor`, `Convai → Gaze Editor`, `Convai → Body Animation Editor`, `Convai → Emotion Editor` |
| **Diagnostics** | All SDK subsystems — verbosity and filtering | `Convai → Settings` or `Edit → Project Settings → Convai SDK` (Diagnostics section) |
| **Convai Action Monitor (`ConvaiActionDebugProbe`)** | Action dispatch, executor wiring, batch failures | Add Component → Convai/Actions/Diagnostics/Convai Action Monitor |
| **ConvaiRoomManager properties** | Session state, error codes, connect/reconnect counts | `FindFirstObjectByType<ConvaiRoomManager>()` — read properties directly |
| **IRoomDiagnostics snapshot** | Connection attempt counts, uptime, last error, agent counts | `room.DiagnosticsCoordinator.GetDiagnostics()` |
| **Session Metrics messages** | Reconnection success rate, session lifecycle, error timeline | Console filter `[SessionMetrics]`; requires Info or Debug level |
| **Client Latency metrics** | End-to-end conversation pipeline latency | Room debug mode plus Info logging; Console filter `[ClientLatency]` |
| **LipSync Drift Monitor** | Audio-vs-visual lip sync alignment, drift error, CSV export | `ConvaiLipSyncComponent` Inspector → **Open Drift Monitor** |
| **Custom log sinks** | Route logs to files, telemetry, or overlays | `ConvaiLogger.RegisterSink(new YourSink())` |

## Next steps

For platform-specific issues — WebGL AudioContext unlock, Android microphone handling, or platform build settings — see the Platform Guides section.

{% content-ref url="../platform-guides/README.md" %}
[Platform guides](../platform-guides/README.md)
{% endcontent-ref %}

For feature-specific diagnostic tools, see the troubleshooting page inside each feature's section. The Actions, Emotion, Vision, and Narrative Design features each have detailed decision trees and console log references beyond what is covered here.
