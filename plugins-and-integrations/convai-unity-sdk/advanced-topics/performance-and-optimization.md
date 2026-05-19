# performance and optimization

The Convai Unity SDK ships with sensible defaults that work well across training simulations, interactive experiences, and games. When you need to diagnose latency, reduce log noise in production, understand the AI pipeline's timing, or tune reconnection behavior — this page covers the available controls.

***

## Log Level Configuration

The SDK uses a structured logging system with per-subsystem categories. Log verbosity is controlled by `ConvaiSettings`, which updates at runtime without restarting.

### Log Levels

`LogLevel` controls the minimum severity a message must reach to appear in the Unity Console:

| Level     | Value | When To Use                                     |
| --------- | ----- | ----------------------------------------------- |
| `Off`     | 0     | Disable all SDK logging.                        |
| `Error`   | 1     | Production builds — errors only.                |
| `Warning` | 2     | Pre-release — warnings and errors.              |
| `Info`    | 3     | **Default.** Normal operation messages.         |
| `Debug`   | 4     | Active development — verbose lifecycle events.  |
| `Trace`   | 5     | Deep debugging — high-frequency internal state. |

The SDK evaluates: if `messageLevel <= configuredLevel`, the message is shown. Setting `Info` (3) shows `Error`, `Warning`, and `Info`; it hides `Debug` and `Trace`.

{% hint style="warning" %}
`Trace` and `Debug` levels generate a significant volume of output. In builds, SDK debug logs are stripped by the compiler unless the `CONVAI_DEBUG_LOGGING` scripting define symbol is present. Do not ship with `Trace` enabled.
{% endhint %}

### Configuring In The Inspector

Open **Project Settings → Convai** (or the `ConvaiSettings` asset in `Assets/Resources/`). Under the **Logging** header:

| Field                  | Description                                                                             |
| ---------------------- | --------------------------------------------------------------------------------------- |
| `Global Log Level`     | Minimum level for all SDK subsystems.                                                   |
| `Include Stack Traces` | Attach stack traces to Warning and Error messages.                                      |
| `Colored Output`       | Color-code log messages in the Unity Console.                                           |
| `Category Overrides`   | Per-subsystem overrides — add entries to set a different level for specific categories. |

### Log Categories

Each SDK subsystem has its own `LogCategory`. You can raise or lower verbosity per subsystem independently:

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

**Example:** To enable Debug logging for the Audio subsystem only, add a Category Override with `Category = Audio`, `Level = Debug`, while keeping the global level at `Info`.

### Configuring At Runtime

```csharp
using Convai.Runtime;
using Convai.Domain.Logging;

// Set global level at runtime
ConvaiSettings.Instance.SetGlobalLogLevel(LogLevel.Debug);

// Per-category override
ConvaiSettings.Instance.SetCategoryOverrides(new[]
{
    new LogLevelOverride(LogCategory.Audio, LogLevel.Debug),
    new LogLevelOverride(LogCategory.Transport, LogLevel.Warning)
});
```

Runtime changes take effect immediately — `LoggingConfig` caches settings and detects version changes on each `IsEnabled` check.

### `CONVAI_DEBUG_LOGGING` Scripting Define

Debug-level logs inside the SDK source are guarded by `#if CONVAI_DEBUG_LOGGING`. Without this define, the compiler strips all `ConvaiLogger.Debug(...)` calls entirely — zero overhead in production builds regardless of the `GlobalLogLevel` setting.

To enable verbose SDK debug logs in a build: add `CONVAI_DEBUG_LOGGING` to **Project Settings → Player → Scripting Define Symbols**.

***

## Custom Log Sinks

By default, `ConvaiLogger` routes all output to `UnityEngine.Debug`. Register a custom `ILogSink` to route logs to a file, a telemetry service, or your own aggregation pipeline:

```csharp
using System;
using Convai.Domain.Logging;
using Convai.Runtime.Logging;

public class FileSink : ILogSink
{
    private readonly System.IO.StreamWriter _writer;
    public string Name => "FileSink";
    public bool IsEnabled { get; private set; } = true;

    public FileSink(string path)
        => _writer = new System.IO.StreamWriter(path, append: true);

    public void Write(LogEntry entry)
        => _writer.WriteLine($"[{entry.Timestamp:HH:mm:ss.fff}] [{entry.Level}] [{entry.Category}] {entry.Message}");

    public void Flush() => _writer.Flush();
    public void SetEnabled(bool enabled) => IsEnabled = enabled;
    public void Dispose() => _writer?.Dispose();
}
```

Register after `ConvaiLogger.Initialize()` completes — use `ConvaiLogger.OnInitializationCompleted` for reliable timing:

```csharp
using Convai.Runtime.Logging;

ConvaiLogger.OnInitializationCompleted += logger =>
{
    string logPath = System.IO.Path.Combine(
        UnityEngine.Application.persistentDataPath, "convai_session.log");
    ConvaiLogger.RegisterSink(new FileSink(logPath));
};
```

Call `ConvaiLogger.UnregisterSink(sink)` before the sink is disposed. Always call `ConvaiLogger.FlushAllSinks()` on application quit.

***

## RTVI Server-Side Debug Metrics

When `ConvaiRoomManager.Debug` is `true`, Convai streams server-side pipeline metrics to the client after each AI turn. These metrics let you see where latency is coming from inside the AI pipeline — useful for identifying slow processors, unexpected queuing, or outlier turns.

### Enabling Debug Metrics

On the `ConvaiRoomManager` component in your scene hierarchy, set **Debug** to `true` in the Inspector, or at runtime:

```csharp
ConvaiRoomManager roomManager = FindObjectOfType<ConvaiRoomManager>();
roomManager.Debug = true;
```

{% hint style="warning" %}
Debug metrics add a small overhead to each turn. Enable this flag for profiling sessions only — do not ship with it enabled.
{% endhint %}

### Reading The Metrics

Subscribe to `ConvaiRoomManager.OnRtvMetricsReceived` to receive `RTVIMetricsPayload` on each completed turn:

```csharp
using Convai.Runtime.Adapters.Networking;
using Convai.Runtime.Infrastructure.Protocol.Messages.Inbound;
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
        // TTFB: time from first input to first output, per processor (seconds)
        if (payload.Ttfb != null)
            Debug.Log($"[Metrics] TTFB: {payload.Ttfb}");

        // Processing: total processing duration per processor (seconds)
        if (payload.Processing != null)
            Debug.Log($"[Metrics] Processing: {payload.Processing}");

        // Custom: provider-specific metrics (e.g., NeuroSync blendshape fps)
        if (payload.Custom != null)
            Debug.Log($"[Metrics] Custom: {payload.Custom}");
    }
}
```

### Metrics Fields

| Field        | Type     | Description                                                                                                         |
| ------------ | -------- | ------------------------------------------------------------------------------------------------------------------- |
| `Ttfb`       | `JToken` | Time-to-first-byte per processor (seconds). Array of `{processor, value}` entries.                                  |
| `Processing` | `JToken` | Total processing duration per processor for this turn (seconds).                                                    |
| `Custom`     | `JToken` | Provider-specific metrics — format varies by processor (e.g., `output_fps`, `blendshapes_received` from NeuroSync). |

`Ttfb` measures how long each stage of the AI pipeline waited before producing its first output token. High `Ttfb` on the LLM processor means the model is slow to start responding; high `Ttfb` on the TTS processor suggests queuing or audio encoding delay.

{% hint style="info" %}
`Ttfb` and `Processing` are raw JSON tokens because the processor list is dynamic — different configurations yield different processor arrays. Deserialize using `payload.Ttfb.ToObject<List<MetricEntry>>()` where `MetricEntry` is a struct you define to match the `{processor, value}` shape.
{% endhint %}

***

## Retry Policy

The SDK uses `ExponentialBackoffPolicy` to handle transient connection failures. By default:

| Attempt     | Delay Before Retry |
| ----------- | ------------------ |
| 1 (initial) | 0 s                |
| 2           | 1 s                |
| 3           | 2 s                |
| 4           | 4 s                |

After 4 total attempts (1 initial + 3 retries), the operation fails. The policy retries only transient errors: timeouts, network interruptions, and `OperationCanceledException`. Non-transient errors (auth failures, invalid configuration) fail immediately without retrying.

### Custom Retry Policy

If your deployment requires different retry timing or attempt counts — for example, a training simulation on a high-latency satellite link — implement `IRetryPolicy` and use `RetryExecutor`:

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Core.Policies;

public class AggressiveRetryPolicy : IRetryPolicy
{
    // 1 initial + 5 retries = 6 total
    public int MaxAttempts => 6;

    public TimeSpan GetDelay(int attempt) => attempt switch
    {
        0 => TimeSpan.Zero,       // immediate
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

Use `RetryExecutor` to wrap any async operation with the custom policy:

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

## Optimization Checklist

Run this checklist before shipping:

* [ ] `Global Log Level` set to `Warning` or `Error` in production `ConvaiSettings` asset.
* [ ] `CONVAI_DEBUG_LOGGING` **not** present in release build Scripting Define Symbols.
* [ ] `ConvaiRoomManager.Debug` is `false` in production scenes.
* [ ] `maxRetryAttempts` in `ConvaiBootstrapConfigSnapshot` is appropriate for your target network (default 3 is suitable for most consumer connections).
* [ ] `connectionTimeoutSeconds` accounts for the slowest target device/network in your deployment (default 30 s).
* [ ] Custom `ILogSink` instances are unregistered and disposed on application quit.

***

## Troubleshooting

| Symptom                                                      | Likely Cause                                                                         | Fix                                                                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| Console flooded with SDK messages in a release build         | `CONVAI_DEBUG_LOGGING` define is present, or `GlobalLogLevel` is `Debug` or `Trace`  | Remove the scripting define and set the global level to `Warning` or `Error`.                         |
| `OnRtvMetricsReceived` never fires                           | `ConvaiRoomManager.Debug` is `false`, or the character has not completed a full turn | Set `Debug = true` and verify a full AI turn completes (user speaks, character responds).             |
| `Ttfb` / `Processing` fields are null                        | The server did not include those metric types for this turn                          | Handle null before accessing. Not every turn includes every metric type.                              |
| Connection fails after 4 attempts and does not retry further | Default `ExponentialBackoffPolicy` reached `MaxAttempts = 4`                         | Increase `maxRetryAttempts` in `ConvaiBootstrapConfigSnapshot`, or implement a custom `IRetryPolicy`. |

***

## Next Steps

{% content-ref url="/broken/pages/4e021981603a577052860a59c010e462fba5e40b" %}
[Broken link](/broken/pages/4e021981603a577052860a59c010e462fba5e40b)
{% endcontent-ref %}

{% content-ref url="/broken/pages/0a699b8af504d5615fbf8de9767391fa0b01a1c0" %}
[Broken link](/broken/pages/0a699b8af504d5615fbf8de9767391fa0b01a1c0)
{% endcontent-ref %}
