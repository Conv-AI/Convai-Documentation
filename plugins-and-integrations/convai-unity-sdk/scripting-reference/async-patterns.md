---
title: Async patterns
description: Consume IConvaiOperation<T> and IConvaiStream<T> using async/await, coroutines, chaining, progress tracking, cancellation, and streams.
last_reviewed: "4.2.0"
---

`IConvaiOperation<T>` and `IConvaiStream<T>` support multiple consumption patterns so you can use the style that fits your codebase — pure async/await, Unity coroutines, or a mix of both. For type definitions and member references, see [Operation & Stream Types](operation-and-stream-types.md).

***

## Async/await

The most direct pattern. Works in any `async` method. Faulted operations throw `ConvaiOperationException`.

```csharp
using Convai.Runtime.Core.Async;
using Convai.Runtime.Facades;
using System.Threading;
using UnityEngine;

public class AsyncConnectExample : MonoBehaviour
{
    private async void Start()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null) return;

        try
        {
            var session = await manager.ConnectAsync(destroyCancellationToken);
            Debug.Log($"Connected. Room: {session.RoomId}");
        }
        catch (ConvaiOperationException ex)
        {
            Debug.LogError($"[{ex.Code}] Connect failed: {ex.Message}");
        }
        catch (OperationCanceledException)
        {
            Debug.Log("Connect canceled — scene unloaded.");
        }
    }
}
```

### `await operation` vs. `await operation.AsTask()`

Both produce the same result. Prefer `await operation` directly — it uses `GetAwaiter()` and avoids an extra allocation. Use `AsTask()` only when you need to pass the operation to a method that requires `Task<T>`, such as `Task.WhenAll`.

```csharp
// Direct await — preferred
var session = await manager.ConnectAsync();

// AsTask — only when needed
await Task.WhenAll(
    manager.ConnectAsync().AsTask(),
    someOtherTask
);
```

***

## Coroutines

Use coroutines when your script cannot use `async` (e.g., on Unity event callbacks that do not support async), or when you prefer a callback-based flow.

```csharp
using Convai.Runtime.Core.Async;
using Convai.Runtime.Facades;
using System.Collections;
using UnityEngine;

public class CoroutineConnectExample : MonoBehaviour
{
    private void Start()
    {
        var op = ConvaiManager.ActiveManager.ConnectAsync();
        StartCoroutine(op.ToCoroutine(
            onSuccess: session => Debug.Log($"Connected: {session.RoomId}"),
            onError:   err     => Debug.LogError($"[{err.Code}] {err.Message}")
        ));
    }
}
```

`ToCoroutine` yields until the operation completes. Both `onSuccess` and `onError` are optional — pass `null` for either if you do not need the callback.

{% hint style="warning" %}
In coroutines, faulted operations do **not** throw. If you omit the `onError` callback, failures are silent.

```csharp
// WRONG — silent failure
yield return op.ToCoroutine(onSuccess: result => Use(result));

// CORRECT
yield return op.ToCoroutine(
    onSuccess: result => Use(result),
    onError:   err    => Debug.LogError(err.Message));
```
{% endhint %}

***

## ContinueWith chaining

Transform the result of one operation into another without nesting `await` calls.

```csharp
// Synchronous transform
IConvaiOperation<string> roomIdOp = manager
    .ConnectAsync()
    .ContinueWith(session => session.RoomId);

string roomId = await roomIdOp;

// Async transform — selector returns a Task<TNext>
IConvaiOperation<string> nameOp = manager
    .ConnectAsync()
    .ContinueWith(async session =>
    {
        await SomeAsyncLookup(session.RoomId);
        return session.RoomId;
    });
```

`ContinueWith` propagates errors: if the source operation faults, the chained operation also faults with the same error without invoking the selector.

***

## Progress tracking

Poll `operation.Progress` to drive a UI progress indicator. The value advances from `0.0` to `1.0` as the operation completes. Not all operations report granular progress — check `Status` for definitive completion.

```csharp
using Convai.Runtime.Facades;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class ConnectProgressBar : MonoBehaviour
{
    [SerializeField] private Slider _progressBar;

    private IEnumerator ConnectWithProgress()
    {
        var op = ConvaiManager.ActiveManager.ConnectAsync();

        while (!op.IsCompleted)
        {
            _progressBar.value = op.Progress;
            yield return null;
        }

        _progressBar.value = 1f;

        if (op.HasError)
            Debug.LogError($"Connect failed: {op.Error.Message}");
    }
}
```

***

## Cancellation

### Using `CancellationToken`

Pass a `CancellationToken` to any SDK method. The operation transitions to `Canceled` when the token is signaled.

```csharp
private CancellationTokenSource _cts;

private async void OnEnable()
{
    _cts = new CancellationTokenSource();

    try
    {
        await ConvaiManager.ActiveManager.ConnectAsync(_cts.Token);
    }
    catch (OperationCanceledException) { /* expected */ }
}

private void OnDisable()
{
    _cts?.Cancel();
    _cts?.Dispose();
}
```

### Using `destroyCancellationToken`

`MonoBehaviour.destroyCancellationToken` is the simplest cancellation pattern for operations scoped to a component's lifetime — the token is automatically signaled when the component is destroyed.

```csharp
private async void Start()
{
    await ConvaiManager.ActiveManager.ConnectAsync(destroyCancellationToken);
}
```

### Using `operation.Cancel()`

Call `Cancel()` on the operation handle directly for manual cancellation independent of a `CancellationToken`.

```csharp
var op = manager.ConnectAsync();

// Later — cancel the operation
op.Cancel();
```

### `CancellationToken` vs. `operation.Cancel()`

|                          | `CancellationToken`                              | `operation.Cancel()`                           |
| ------------------------ | ------------------------------------------------ | ---------------------------------------------- |
| **Source**               | External (`CancellationTokenSource`)             | The operation handle                           |
| **Use case**             | Component lifetime, timeout, linked cancellation | Single operation cancel from a button or event |
| **Coroutine compatible** | Pass at operation creation                       | Call on the handle at any time                 |

***

## Streams

Use `IConvaiStream<T>` with `await foreach` and `await using` for resource cleanup.

```csharp
await using var stream = GetTokenStream();

await foreach (var token in stream.ReadAllAsync(destroyCancellationToken))
{
    AppendToTranscriptUI(token);
}
```

`ReadAllAsync` returns `IAsyncEnumerable<T>`. The loop exits when the stream reaches `Completed`, `Faulted`, or `Canceled`. Always wrap in `await using` so `DisposeAsync()` is called even if the loop exits early.

{% hint style="danger" %}
Never block the Unity main thread with `.Result` — it deadlocks.

```csharp
// WRONG — deadlocks on the main thread
var session = manager.ConnectAsync().AsTask().Result;
```

Use `await` or `ToCoroutine()` instead.
{% endhint %}

{% hint style="warning" %}
Always dispose streams. Failing to `await using` a stream leaks the underlying resources.

```csharp
// WRONG — no disposal
var stream = GetTokenStream();
await foreach (var item in stream.ReadAllAsync()) { ... }

// CORRECT
await using var stream = GetTokenStream();
await foreach (var item in stream.ReadAllAsync()) { ... }
```
{% endhint %}

***

## Error handling decision table

| Scenario                              | Pattern                           | Reason                                                |
| ------------------------------------- | --------------------------------- | ----------------------------------------------------- |
| `async void` MonoBehaviour method     | Async/await with try/catch        | Natural fit; faults surface as exceptions             |
| UI button callback (no async support) | Coroutine with `onError` callback | Button callbacks are synchronous                      |
| Sequential operations with transforms | ContinueWith chaining             | Avoids nested awaits; propagates errors automatically |
| Progress bar or loading overlay       | Coroutine polling `Progress`      | `yield return null` loop per frame                    |
| Component lifetime scoping            | `destroyCancellationToken`        | Zero boilerplate; automatic cleanup                   |
| User-triggered cancel (button)        | `operation.Cancel()`              | Direct handle control without CTS                     |
| Continuous data stream                | `await foreach` + `await using`   | IAsyncEnumerable + guaranteed disposal                |

***

## Usage examples

### Example 1 — Loading overlay with progress bar and cancel button

A medical training simulation shows a loading overlay while the session connects, with a visual progress bar and a cancel button for learners who want to exit before the session starts.

{% code title="SessionLoadingOverlay.cs" %}
```csharp
using Convai.Runtime.Core.Async;
using Convai.Runtime.Facades;
using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class SessionLoadingOverlay : MonoBehaviour
{
    [SerializeField] private GameObject _overlayRoot;
    [SerializeField] private Slider     _progressBar;
    [SerializeField] private TMP_Text   _statusLabel;
    [SerializeField] private Button     _cancelButton;

    private IConvaiOperation<RoomSession> _connectOp;

    public void StartConnect()
    {
        _overlayRoot.SetActive(true);
        _connectOp = ConvaiManager.ActiveManager.ConnectAsync(destroyCancellationToken);
        _cancelButton.onClick.AddListener(OnCancelClicked);
        StartCoroutine(TrackConnect());
    }

    private IEnumerator TrackConnect()
    {
        _statusLabel.text = "Connecting…";

        while (!_connectOp.IsCompleted)
        {
            _progressBar.value = _connectOp.Progress;
            yield return null;
        }

        _overlayRoot.SetActive(false);
        _cancelButton.onClick.RemoveListener(OnCancelClicked);

        if (_connectOp.HasError)
            _statusLabel.text = $"Failed: {_connectOp.Error.Message}";
        else if (!_connectOp.IsCanceled)
            _statusLabel.text = "Connected.";
    }

    private void OnCancelClicked() => _connectOp?.Cancel();
}
```
{% endcode %}

### Example 2 — Streaming transcript tokens to a custom log widget

A corporate onboarding simulation streams individual transcript tokens from Convai and appends them to a custom log widget one token at a time, producing a typewriter-style effect.

{% code title="StreamingTranscriptLog.cs" %}
```csharp
using Convai.Runtime.Facades;
using TMPro;
using UnityEngine;

public class StreamingTranscriptLog : MonoBehaviour
{
    [SerializeField] private TMP_Text _log;

    // Call this method when a new character turn begins
    public async void AttachToStream(IConvaiStream<string> tokenStream)
    {
        try
        {
            await using (tokenStream)
            {
                await foreach (var token in tokenStream.ReadAllAsync(destroyCancellationToken))
                {
                    _log.text += token;
                }
            }
        }
        catch (System.OperationCanceledException)
        {
            // Component destroyed mid-stream — expected
        }
    }
}
```
{% endcode %}

***

## Troubleshooting

| Symptom                                                            | Likely Cause                                                                     | Fix                                                                                                     |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Operation stays in `Running` indefinitely                          | SDK method awaiting a response that never arrives (network timeout)              | Set a `CancellationToken` with a timeout: `new CancellationTokenSource(TimeSpan.FromSeconds(15)).Token` |
| `HasError` is `true` but `ConvaiOperationException` is not thrown  | Using coroutine path — errors are delivered to `onError` callback, not thrown    | Add an `onError` callback to `ToCoroutine()`                                                            |
| `catch (ConvaiOperationException)` block never hit on cancellation | Cancellation throws `OperationCanceledException`, not `ConvaiOperationException` | Add a separate `catch (OperationCanceledException)` block                                               |
| Cancellation has no effect after `operation.Cancel()`              | Operation already completed before cancel was called                             | Check `IsCompleted` before calling `Cancel()`                                                           |
| Stream hangs on scene unload                                       | `ReadAllAsync` loop not passing a `CancellationToken`                            | Pass `destroyCancellationToken` to `ReadAllAsync`                                                       |
| `ContinueWith` selector never runs                                 | Source operation faulted; error is propagated, selector is skipped               | Check the chained operation's `HasError` or catch `ConvaiOperationException` at the await site          |

***

## Next steps

For the full type reference behind these patterns, see [Operation & Stream Types](operation-and-stream-types.md). For SDK methods that return `IConvaiOperation<T>`, see [ConvaiManager API](convaimanager-api.md) and [Character & Player API](character-and-player-api.md).
