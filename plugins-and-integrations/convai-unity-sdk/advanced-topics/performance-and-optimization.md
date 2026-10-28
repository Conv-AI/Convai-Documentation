---
description: >-
  Configure SDK log verbosity per subsystem, route logs to custom sinks, read
  RTVI pipeline latency metrics, and understand connection retry limits.
title: Logging, metrics, and retry policy
last_reviewed: "5.0.0-preview"
---

The Convai Unity SDK ships with defaults that work across training simulations, interactive experiences, and games. When you need to diagnose latency, reduce log noise in production, understand the AI pipeline's timing, or understand retry limits, use the controls below.

**Jump to the topic you need:**

* [Log level configuration](performance-and-optimization.md#log-level-configuration) — reduce console noise in production builds
* [Custom log sinks](performance-and-optimization.md#custom-log-sinks) — route logs to a file or remote service
* [RTVI server-side debug metrics](performance-and-optimization.md#rtvi-server-side-debug-metrics) — measure AI pipeline latency per turn
* [Retry policy](performance-and-optimization.md#retry-policy) — understand fixed room retries and wrap your own operations

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
using Convai.Runtime;
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

`LogLevelOverride` is a struct with `Category` and `Level` fields. Later category overrides win. Use `SetStackTraceLevels(LogStackTraceLevels)` and `SetColoredOutput(bool)` for the other controls. `IncludeStackTraces` and `SetIncludeStackTraces` are obsolete; the default stack-trace mask is `Error`.

### `CONVAI_DEBUG_LOGGING` scripting define

`ConvaiLogger.Debug(...)` calls are guarded by three `[Conditional]` attributes: `UNITY_EDITOR`, `DEVELOPMENT_BUILD`, and `CONVAI_DEBUG_LOGGING`. The compiler strips them from any build where none of these symbols is defined — zero overhead in production release builds.

Enable **Advanced > Feature Flags > Debug Logging** in Convai settings to set `CONVAI_DEBUG_LOGGING` for the active build target group. Development Builds enable them automatically without this define.

***

## Custom log sinks

Route SDK log output to a file, a remote logging service, or any destination by implementing `ILogSink` and registering it with `ConvaiLogger`.

```csharp
// FileSink.cs
using System;
using System.IO;
using Convai.Domain.Logging;

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
```

Register a new sink in `Awake` or an `AfterSceneLoad` runtime initializer. Logger initialization normally runs before scene components, so a scene subscription to `OnInitializationCompleted` misses that event.

```csharp
using System.IO;
using Convai.Runtime.Logging;
using UnityEngine;

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

**Sink lifecycle:**

* `ILogSink` extends `IDisposable` — implementing classes must provide a `Dispose()` method.
* `UnregisterSink(sink)` retires and disposes it. A retired sink cannot be registered again; create a new instance.
* Three consecutive write failures disable a sink.
* Shutdown on application quit flushes and clears sinks. Session reset clears registrations, so register anew each Play session.

***

## RTVI server-side debug metrics

RTVI (Real-Time Voice Interaction) is Convai's session protocol. When `ConvaiRoomManager.Debug` is `true`, the connection requests pipeline metrics from Convai, showing how long each stage (speech-to-text, LLM, text-to-speech, etc.) took. Use this when you need to identify which pipeline stage is the bottleneck — e.g., is the AI slow to respond because of transcription latency or LLM generation time?

### Enabling debug metrics

`ConvaiRoomManager.Debug` is a read-only runtime property. Enable it by checking the **Debug** checkbox on the `ConvaiRoomManager` component in the Inspector before entering Play Mode.

{% hint style="warning" %}
Enable debug metrics for diagnostic sessions and inspect only the fields returned. Their presence and timing depend on Convai.
{% endhint %}

### Reading the metrics

```csharp
// MetricsLogger.cs
using Convai.Runtime.Adapters.Networking;
using Convai.Infrastructure.Protocol.Messages;
using UnityEngine;

public class MetricsLogger : MonoBehaviour
{
    [SerializeField] private ConvaiRoomManager _roomManager;

    private void OnEnable()
        => _roomManager.OnRtvMetricsReceived += OnMetricsReceived;

    private void OnDisable()
        => _roomManager.OnRtvMetricsReceived -= OnMetricsReceived;

    private void OnMetricsReceived(RTVIMetricsPayload payload)
    {
        if (payload.Ttfb       != null) Debug.Log($"[Metrics] TTFB: {payload.Ttfb}");
        if (payload.Processing != null) Debug.Log($"[Metrics] Processing: {payload.Processing}");
        if (payload.Custom     != null) Debug.Log($"[Metrics] Custom: {payload.Custom}");
    }
}
```

### Metrics fields

| Field        | Type      | Description                                                                                                         |
| ------------ | --------- | ------------------------------------------------------------------------------------------------------------------- |
| `Ttfb`       | `JToken?` | Time-to-first-byte per processor (seconds). Array of `{processor, value}` entries.                                  |
| `Processing` | `JToken?` | Total processing duration per processor for this turn (seconds).                                                    |
| `Custom`     | `JToken?` | Provider-specific metrics — format varies by processor (e.g., `output_fps`, `blendshapes_received` from NeuroSync). |

`Ttfb` and `Processing` are raw `JToken` values (from `Newtonsoft.Json.Linq`, included in Unity via the `com.unity.nuget.newtonsoft-json` package). Deserialize them as `payload.Ttfb.ToObject<List<MetricEntry>>()` where `MetricEntry` is a struct matching the `{processor, value}` shape. Not every turn includes every metric type — always null-check before accessing.

***

## Retry policy

The SDK uses `ExponentialBackoffPolicy` to handle transient connection failures. Default behavior:

| Attempt     | Delay before retry |
| ----------- | ------------------ |
| 1 (initial) | 0 s                |
| 2           | 1 s                |
| 3           | 2 s                |
| 4           | 4 s                |

After 4 total attempts (1 initial + 3 retries), the operation fails. The policy retries only transient errors: timeouts, network interruptions, and `OperationCanceledException`. Non-transient errors (auth failures, invalid configuration) fail immediately.

### Limits of retry customization

The room connection constructs its own `RetryExecutor` with `ExponentialBackoffPolicy`: four attempts with delays of `0`, `1`, `2`, and `4` seconds. There is no public hook to replace that policy. `ConvaiBootstrapConfigSnapshot` retry fields do not change it.

A custom policy applies only to operations your code wraps in its own executor. The default transient classification includes `TimeoutException`, `HttpRequestException`, and `OperationCanceledException`, including nested and aggregate exceptions. Configure room request timeout through **Advanced > Connection Timeout (s)**.

### Custom retry policy

Implement `IRetryPolicy` and use `RetryExecutor` to wrap any async operation:

```csharp
// AggressiveRetryPolicy.cs
using System;
using Convai.Runtime.Core.Policies;

public class AggressiveRetryPolicy : IRetryPolicy
{
    public int MaxAttempts => 6;

    public TimeSpan GetDelay(int attempt) => attempt switch
    {
        0 => TimeSpan.Zero,
        1 => TimeSpan.FromSeconds(2),
        2 => TimeSpan.FromSeconds(5),
        3 => TimeSpan.FromSeconds(10),
        4 => TimeSpan.FromSeconds(20),
        _ => TimeSpan.FromSeconds(30)
    };

    public bool ShouldRetry(Exception exception, int attempt)
    {
        if (attempt >= MaxAttempts) return false;
        return exception is TimeoutException
            || exception is System.Net.WebException
            || exception is OperationCanceledException;
    }
}
```

```csharp
using Convai.Runtime.Core.Policies;

// pseudocode: someAsyncOperation and cancellationToken belong to your application.
var executor = new RetryExecutor(new AggressiveRetryPolicy());

await executor.ExecuteAsync(async (attempt, ct) =>
{
    Debug.Log($"Connection attempt {attempt + 1}...");
    await someAsyncOperation(ct);
    return true;
}, cancellationToken);
```

***

## Production checklist

* [ ] `Global Log Level` set to `Warning` or `Error` in the production `ConvaiSettings` asset.
* [ ] `CONVAI_DEBUG_LOGGING` **not** present in release build Scripting Define Symbols.
* [ ] `ConvaiRoomManager.Debug` checkbox **unchecked** in production scenes.
* [ ] Your application handles a failed connection after the SDK's fixed retry sequence.
* [ ] **Advanced > Connection Timeout (s)** fits the target network (`5`–`120` seconds, default `30`).
* [ ] Custom sinks are registered each session and unregistered when their owner is destroyed.
* [ ] `ConvaiLogger.FlushAllSinks()` called in `Application.quitting` handler if any sinks buffer output.

***

## Troubleshooting

| Symptom                                                      | Likely cause                                                                           | Fix                                                                                                           |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Console flooded with SDK messages in a release build         | `CONVAI_DEBUG_LOGGING` define is present, or `GlobalLogLevel` is `Debug` or `Trace`    | Remove the scripting define and set the global level to `Warning` or `Error`.                                 |
| `OnRtvMetricsReceived` never fires                           | `ConvaiRoomManager.Debug` is unchecked, or the character has not completed a full turn | Enable the Debug checkbox and verify a full AI turn completes (user speaks, character responds).              |
| `Ttfb` / `Processing` fields are null                        | The server did not include those metric types for this turn                            | Handle null before accessing. Not every turn includes every metric type.                                      |
| Connection fails after 4 attempts and does not retry further | Default `ExponentialBackoffPolicy` reached `MaxAttempts = 4`                           | Handle failure in the application; a custom policy does not replace SDK room retries.         |
| Custom log sink missing early startup messages               | Sink registered after `ConvaiLogger.Initialize()` already fired                        | Register in an early runtime initialization callback if startup coverage is required; scene Awake runs after logger initialization. |

***

## Next steps

{% content-ref url="../troubleshooting/README.md" %}
[Troubleshooting](../troubleshooting/README.md)
{% endcontent-ref %}

{% content-ref url="extending-the-sdk.md" %}
[Runtime module system](extending-the-sdk.md)
{% endcontent-ref %}

{% content-ref url="implement-a-custom-module.md" %}
[Implement a custom module](implement-a-custom-module.md)
{% endcontent-ref %}
