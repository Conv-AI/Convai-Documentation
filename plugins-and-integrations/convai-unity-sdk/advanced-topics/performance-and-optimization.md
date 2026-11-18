---
description: >-
  Configure SDK log verbosity per subsystem, route logs to custom sinks, read
  RTVI pipeline latency metrics, and understand connection retry limits.
title: Logging, metrics, and retry policy
last_reviewed: "5.0.0-pre.1"
---

The Convai Unity SDK ships with defaults that work across training simulations, interactive experiences, and games. When you need to diagnose latency, reduce log noise in production, understand the AI pipeline's timing, or understand retry limits, use the controls below.

**Jump to the topic you need:**

* [Log level configuration](performance-and-optimization.md#log-level-configuration) — reduce console noise in production builds
* [Custom log sinks](performance-and-optimization.md#custom-log-sinks) — route logs to a file or remote service
* [RTVI server-side debug metrics](performance-and-optimization.md#rtvi-server-side-debug-metrics) — measure AI pipeline latency per turn
* [Retry policy](performance-and-optimization.md#retry-policy) — understand fixed room retries and understand which failures the SDK retries

***

## Log level configuration

### Log levels

| Level     | Enum Value | When to use                                     |
| --------- | ---------- | ----------------------------------------------- |
| `Off`     | `0`        | Disable all SDK logging.                        |
| `Error`   | `1`        | Production builds — errors only.                |
| `Warning` | `2`        | Pre-release — warnings and errors.              |
| `Info`    | `3`        | **Default.** Normal operation messages.         |
| `Debug`   | `4`        | Active development — verbose lifecycle events.  |
| `Trace`   | `5`        | Deep debugging — high-frequency internal state. |

These values correspond to the `Convai.Domain.Logging.LogLevel` enum.

{% hint style="warning" %}
`Trace` and `Debug` levels generate significant output volume. SDK debug logs are active in the Unity Editor and in Development Builds. In release builds they are stripped by the compiler unless `CONVAI_DEBUG_LOGGING` is added to Scripting Define Symbols. Do not ship with `Trace` enabled.
{% endhint %}

### Configuring in the Inspector

Open **Edit > Project Settings > Convai SDK** and scroll to **Diagnostics**. Presets are **Verbose**, **Default**, and **Errors Only**.

| Field                  | Description                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| **Global Log Level** | Most verbose level emitted by default.                                                             |
| **Stack Trace Levels** | Choose which severity levels include stack traces.                                                |
| **Colored Console Output**       | Color-code log messages in the Unity Console.                                                     |
| **Category Overrides (N)**   | Per-subsystem level overrides — add entries to set a finer-grained level for specific categories. |

### Log categories

| Category       | Subsystem                                                                             |
| -------------- | -------------------------------------------------------------------------------------- |
| `SDK`          | General operations                                                                    |
| `Character`    | Per-character session lifecycle                                                       |
| `Audio`        | Microphone capture, playback, audio device                                            |
| `UI`           | UI component lifecycle                                                                |
| `REST`         | REST API communication                                                                |
| `Transport`    | WebRTC / WebSocket connection layer                                                   |
| `Events`       | Internal event bus                                                                    |
| `Player`       | Player identity and input                                                             |
| `Editor`       | Editor-only operations                                                                |
| `Vision`       | Camera capture and video publishing                                                   |
| `Bootstrap`    | SDK startup and initialization                                                         |
| `Transcript`   | Transcript processing and routing                                                     |
| `Narrative`    | Narrative design system                                                               |
| `LipSync`      | Lip sync processing and blendshape playback                                           |
| `Animation`    | Body animation system — layers, transitions, and locomotion                           |
| `Gaze`         | Gaze system — targeting, policy, and eye/head/body solvers                            |
| `BodyLanguage` | Body language system — gesticulation, posture, breathing, and fidgets                 |
| `Actions`      | Action system — which commands arrived, which were dropped, and how targets resolved  |

These values correspond to the `Convai.Domain.Logging.LogCategory` enum.

### Configuring at runtime

```csharp
using Convai.Runtime.Configuration;
using Convai.Domain.Logging;

// Set global level — applies immediately to all subsequent log calls.
ConvaiSettings.Instance.SetGlobalLogLevel(LogLevel.Debug);

// Override specific subsystems without changing the global level.
ConvaiSettings.Instance.SetCategoryOverrides(new[]
{
    new LogLevelOverride(LogCategory.Audio,     LogLevel.Debug),
    new LogLevelOverride(LogCategory.Transport, LogLevel.Warning)
});
```

`LogLevelOverride` is a struct with `Category` and `Level` fields. Later category overrides win. Use `SetStackTraceLevels(LogStackTraceLevels)` and `SetColoredOutput(bool)` for the other controls. The default stack-trace mask is `Error`.

### `CONVAI_DEBUG_LOGGING` scripting define

`ConvaiLogger.Debug(...)` calls are guarded by three `[Conditional]` attributes: `UNITY_EDITOR`, `DEVELOPMENT_BUILD`, and `CONVAI_DEBUG_LOGGING`. The compiler strips them from any build where none of these symbols is defined.

Enable **Advanced > Feature Flags > Debug Logging** in Convai settings to set `CONVAI_DEBUG_LOGGING` for the active build target group. Development Builds enable them automatically without this define.

***

## Custom log sinks

Route SDK log output to a file, a remote logging service, or any destination by implementing `ILogSink` and registering it with `ConvaiLogger`.

```csharp
// FileSink.cs
using System.IO;
using Convai.Domain.Logging;
using Convai.Runtime.Logging;
using UnityEngine;

public class FileSink : ILogSink
{
    private readonly StreamWriter _writer;

    public string Name      => "FileSink";
    public bool   IsEnabled { get; private set; } = true;

    public FileSink(string path)
        => _writer = new StreamWriter(path, append: true);

    public bool IsEnabledFor(LogLevel level, LogCategory category) => IsEnabled;

    public void Write(in LogEntry entry)
        => _writer.WriteLine($"[{entry.Timestamp:HH:mm:ss.fff}] [{entry.Level}] [{entry.Category}] {entry.Message}");

    public void Flush()             => _writer.Flush();
    public void SetEnabled(bool en) => IsEnabled = en;
    public void Dispose()           => _writer?.Dispose();
}

public sealed class FileLogging : MonoBehaviour
{
    private FileSink sink;
    private void Awake()
    {
        sink = new FileSink(Path.Combine(UnityEngine.Application.persistentDataPath, "convai_session.log"));
        ConvaiLogger.RegisterSink(sink);
    }
    private void OnDestroy()
    {
        if (sink != null) ConvaiLogger.UnregisterSink(sink);
    }
}
```

Attach `FileLogging` to a scene object. The component registers a sink in `Awake` and releases it in `OnDestroy`.

## Sink lifecycle

* `ILogSink` extends `IDisposable` — implementing classes must provide a `Dispose()` method.
* `UnregisterSink(sink)` retires and disposes it. A retired sink cannot be registered again; create a new instance.
* Three consecutive write failures disable a sink.
* Shutdown on application quit flushes and clears sinks. Session reset clears registrations, so register anew each Play session.

***

## RTVI server-side debug metrics

RTVI is the protocol the SDK uses in a conversation room. Turn on **Debug** on `ConvaiRoomManager` before connecting to request timing data for the session. Complete a turn and look for `RTVI metrics:` entries in the Unity Console. The SDK logs the `ttfb`, `processing`, and `custom` groups when Convai supplies values. These entries use `Info` in the `Transport` category. A missing group means the received metrics had no values for that group.

In SDK 5.0 the metrics are logged through `ConvaiLogger`. If you previously listened to `OnRtvMetricsReceived`, use a custom log sink for diagnostic collection. Leave **Debug** off in rooms that do not need pipeline metrics.

## Retry policy

For transient connect failures, the SDK makes up to four attempts total, with delays of one, two, and four seconds before retries. The policy examines exception types, including timeouts and HTTP request transport failures, rather than reading a retry flag from the service. Cancel the caller’s token to stop the pending connect operation.

Room rejoin and character session resume have separate settings. Configure them on `ConvaiRoomManager` or through `SetReconnectPolicy`. See [Session lifecycle](../core-concepts/session-lifecycle.md).

## Troubleshooting

| Symptom | Check | Verify |
| --- | --- | --- |
| Expected Debug logs are absent | Enable the appropriate log level and check the development build or scripting define | Confirm entries from the expected category appear |
| Pipeline metrics are absent | Enable room **Debug**, then allow `Info` logs in the `Transport` category | Reconnect and complete a turn; look for `RTVI metrics:` when Convai returns timing data |
| Connection repeatedly fails | Inspect the first failure and its error code | Confirm configuration and network access are correct before retrying |

## Related pages

- [Session lifecycle](../core-concepts/session-lifecycle.md)
- [Connection and API issues](../troubleshooting/connection-and-api-issues.md)
