---
description: >-
  Configure SDK log verbosity per subsystem, route logs to custom sinks, read
  RTVI pipeline latency metrics, and tune the connection retry policy.
title: Logging, metrics, and retry policy
last_reviewed: "4.2.0"
---

The Convai Unity SDK ships with defaults that work across training simulations, interactive experiences, and games. When you need to diagnose latency, reduce log noise in production, understand the AI pipeline's timing, or tune reconnection behavior — this page covers the available controls.

**Jump to the topic you need:**

* [Log level configuration](performance-and-optimization.md#log-level-configuration) — reduce console noise in production builds
* [Custom log sinks](performance-and-optimization.md#custom-log-sinks) — route logs to a file or remote service
* [RTVI server-side debug metrics](performance-and-optimization.md#rtvi-server-side-debug-metrics) — measure AI pipeline latency per turn
* [Retry policy](performance-and-optimization.md#retry-policy) — tune reconnection behavior for flaky networks

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

Open **Project Settings → Convai** (or select the `ConvaiSettings` asset at `Assets/Resources/ConvaiSettings.asset`). Under the **Logging** section:

| Field                  | Description                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| `Global Log Level`     | Minimum level for all SDK subsystems.                                                             |
| `Include Stack Traces` | Attach stack traces to Warning and Error messages.                                                |
| `Colored Output`       | Color-code log messages in the Unity Console.                                                     |
| `Category Overrides`   | Per-subsystem level overrides — add entries to set a finer-grained level for specific categories. |

### Log categories

| Category     | Subsystem                                   |
| ------------ | ------------------------------------------- |
| `SDK`        | General operations                          |
| `Character`  | Per-character session lifecycle             |
| `Audio`      | Microphone capture, playback, audio device  |
| `Transport`  | WebRTC / WebSocket connection layer         |
| `Events`     | Internal event bus                          |
| `Transcript` | Transcript processing and routing           |
| `Narrative`  | Narrative design system                     |
| `LipSync`    | Lip sync processing and blendshape playback |
| `Vision`     | Camera capture and video publishing         |
| `Bootstrap`  | SDK startup and initialization              |
| `UI`         | UI component lifecycle                      |
| `REST`       | REST API communication                      |
| `Player`     | Player identity and input                   |
| `Editor`     | Editor-only operations                      |

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

`LogLevelOverride` is a struct with two fields: `LogCategory Category` and `LogLevel Level`.

### `CONVAI_DEBUG_LOGGING` scripting define

`ConvaiLogger.Debug(...)` calls are guarded by three `[Conditional]` attributes: `UNITY_EDITOR`, `DEVELOPMENT_BUILD`, and `CONVAI_DEBUG_LOGGING`. The compiler strips them from any build where none of these symbols is defined — zero overhead in production release builds.

To enable debug logs in a release build: add `CONVAI_DEBUG_LOGGING` to **Project Settings → Player → Scripting Define Symbols**. Development Builds enable them automatically without this define.

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

    public void Write(LogEntry entry)
        => _writer.WriteLine($"[{entry.Timestamp:HH:mm:ss.fff}] [{entry.Level}] [{entry.Category}] {entry.Message}");

    public void Flush()             => _writer.Flush();
    public void SetEnabled(bool en) => IsEnabled = en;
    public void Dispose()           => _writer?.Dispose();
}
```

Register after `ConvaiLogger` initializes:

```csharp
using Convai.Runtime.Logging;

// OnInitializationCompleted fires when ConvaiLogger is ready — always register sinks here,
// never before, to avoid missing the initialization window.
ConvaiLogger.OnInitializationCompleted += _ =>
{
    string logPath = Path.Combine(Application.persistentDataPath, "convai_session.log");
    ConvaiLogger.RegisterSink(new FileSink(logPath));
};
```

**Sink lifecycle:**

* `ILogSink` extends `IDisposable` — implementing classes must provide a `Dispose()` method.
* Call `ConvaiLogger.UnregisterSink(sink)` before disposing the sink.
* Call `ConvaiLogger.FlushAllSinks()` on application quit to ensure buffered entries are written.

***

## RTVI server-side debug metrics

RTVI (Real-Time Voice Interaction) is Convai's session protocol. When `ConvaiRoomManager.Debug` is `true`, the server streams pipeline metrics to the client after each AI turn, showing how long each stage (speech-to-text, LLM, text-to-speech, etc.) took. Use this when you need to identify which pipeline stage is the bottleneck — e.g., is the AI slow to respond because of transcription latency or LLM generation time?

### Enabling debug metrics

`ConvaiRoomManager.Debug` is a read-only runtime property. Enable it by checking the **Debug** checkbox on the `ConvaiRoomManager` component in the Inspector before entering Play Mode.

{% hint style="warning" %}
Debug metrics add a small overhead to each turn. Check this option for profiling sessions only — do not ship with it enabled.
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

### When to customize the retry policy

The default policy (4 attempts, exponential back-off up to 4 s) covers most consumer network conditions. Consider a custom policy when:

* **Deployed on industrial or embedded hardware** with known intermittent connectivity — increase `MaxAttempts` and delay steps.
* **Kiosk or always-on installation** — a more aggressive retry (more attempts, longer max delay) avoids user intervention after a brief network dropout.
* **Low-latency training environment** with reliable networking — reduce `MaxAttempts` to fail fast and surface errors to your own reconnect UI rather than silently retrying.

If you only need more attempts without changing the delay curve, increase `maxRetryAttempts` in `ConvaiBootstrapConfigSnapshot` — no custom policy needed.

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
* [ ] `maxRetryAttempts` in `ConvaiBootstrapConfigSnapshot` is appropriate for your target network (default `3` suits most consumer connections).
* [ ] `connectionTimeoutSeconds` accounts for the slowest target device/network in your deployment (default `30` s).
* [ ] Custom `ILogSink` instances are unregistered and disposed on application quit.
* [ ] `ConvaiLogger.FlushAllSinks()` called in `Application.quitting` handler if any sinks buffer output.

***

## Troubleshooting

| Symptom                                                      | Likely cause                                                                           | Fix                                                                                                           |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Console flooded with SDK messages in a release build         | `CONVAI_DEBUG_LOGGING` define is present, or `GlobalLogLevel` is `Debug` or `Trace`    | Remove the scripting define and set the global level to `Warning` or `Error`.                                 |
| `OnRtvMetricsReceived` never fires                           | `ConvaiRoomManager.Debug` is unchecked, or the character has not completed a full turn | Enable the Debug checkbox and verify a full AI turn completes (user speaks, character responds).              |
| `Ttfb` / `Processing` fields are null                        | The server did not include those metric types for this turn                            | Handle null before accessing. Not every turn includes every metric type.                                      |
| Connection fails after 4 attempts and does not retry further | Default `ExponentialBackoffPolicy` reached `MaxAttempts = 4`                           | Increase `maxRetryAttempts` in `ConvaiBootstrapConfigSnapshot`, or implement a custom `IRetryPolicy`.         |
| Custom log sink missing early startup messages               | Sink registered after `ConvaiLogger.Initialize()` already fired                        | Register via the `OnInitializationCompleted` callback — never register sinks before initialization completes. |

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
