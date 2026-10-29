---
title: Async patterns
description: Await Unity SDK operations, handle connection failures, use coroutine callbacks, and pass cancellation tokens without implying unsupported progress.
last_reviewed: "5.0.0-preview"
---

SDK connection and audio methods return `IConvaiOperation<T>`. Awaiting an operation returns its value and throws on failure. A connection returns a `RoomSession`; it does not return an object with `IsSuccessful` or `Error` properties.

## Await a connection

Turn off **Starts Connected** on `ConvaiRoomManager` (or **Connect On Start** on its profile) if your script owns the initial connection. That setting also blocks each character's **Auto Connect**; explicit `ConnectAsync` calls still work. Assign the scene manager to this component. The script waits for bootstrap, connects, and cancels if it is disabled.

```csharp
using System;
using System.Threading;
using Convai.Runtime.Components;
using Convai.Runtime.Core.Async;
using UnityEngine;

public sealed class ConnectFromScript : MonoBehaviour
{
    [SerializeField] private ConvaiManager manager;
    private CancellationTokenSource cancellation;

    private async void OnEnable()
    {
        cancellation = new CancellationTokenSource();
        var token = cancellation.Token;
        try
        {
            while (!manager.IsInitialized)
            {
                token.ThrowIfCancellationRequested();
                await System.Threading.Tasks.Task.Yield();
            }
            await manager.ConnectAsync(token);
            Debug.Log("Room connected.");
        }
        catch (OperationCanceledException) { }
        catch (ConvaiOperationException error)
        {
            Debug.LogWarning($"Connection failed: {error.Code}");
        }
        catch (Exception error)
        {
            Debug.LogWarning($"Connection failed: {error.GetType().Name}");
        }
    }

    private void OnDisable()
    {
        cancellation?.Cancel();
        cancellation?.Dispose();
        cancellation = null;
    }
}
```

Observe `ConversationAvailability` separately before enabling player input. Connection success does not guarantee character readiness.

## Use a coroutine

An operation's `ToCoroutine(onSuccess, onError)` waits for completion and calls the relevant callback. A fault without an error callback is logged. Cancellation calls the supplied error callback with code `canceled`; without one it is silent.

```csharp
// Inside a MonoBehaviour, after manager.IsInitialized is true:
StartCoroutine(manager.ConnectAsync().ToCoroutine(
    session => Debug.Log("Room connected."),
    error => Debug.LogWarning($"Connection failed: {error.Code}")));
```

## Pass cancellation to the operation

Pass a `CancellationToken` to the SDK method that supports it. Cancel the source when the user cancels or the owning component is disabled. `operation.Cancel()` only works if the producer supplied a cancellation source to the operation wrapper; SDK task wrappers generally do not. It is not a substitute for passing a token.

In WebGL players, framework timer/thread-pool APIs such as `CancelAfter` and timer-based `CancellationTokenSource` do not reliably drive timeouts. Use a Unity frame-driven timer or coroutine to call `Cancel()` on your source. The SDK uses an internal player-loop timer for its own timeouts; that internal helper is not an application API.

## Chaining and progress

`ContinueWith` maps a successful result through a synchronous or task-returning function. Await the returned operation and handle its errors too.

Use an indeterminate loading indicator for SDK operations. `Progress` stays at zero until success, then becomes one unless a custom producer explicitly reports progress. A smooth percentage bar would imply progress the operation does not report.

## Transcript delivery

Room transcripts use `ConvaiTranscripts.Subscribe` and `SubscribeCaptions`, not `IConvaiStream` of tokens. The stream interface belongs to custom standalone conversation providers and has no default producer in the manager's room configuration.

## Verify the integration

Check successful connection, a refused connection, and cancellation while connecting. Confirm that your UI stops waiting in each case and that disabling the component removes its callbacks. For API details, see [Operation and stream types](operation-and-stream-types.md) and [Transcript API](transcript-api.md).
