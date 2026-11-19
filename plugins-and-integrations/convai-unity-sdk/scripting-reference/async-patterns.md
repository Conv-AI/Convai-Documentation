---
title: Async patterns
description: Await Unity SDK operations, handle connection failures, observe completion from a coroutine, and pass a cancellation token to the connection.
last_reviewed: "5.0.0-pre.1"
---

SDK connection and audio methods return `IConvaiOperation<T>`. Awaiting an operation returns its value and throws on failure. A connection returns a `RoomSession`; it does not return an object with `IsSuccessful` or `Error` properties.

## Await a connection

Turn off **Connect On Start** on `ConvaiRoomManager` when your script owns the initial connection. Assign the scene manager to the component below. It waits for bootstrap, connects, and cancels if you disable it.

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

Poll the operation from your coroutine. After it completes, handle its state before accessing the result.

```csharp
// Inside a MonoBehaviour, after manager.IsInitialized is true:
private System.Collections.IEnumerator ConnectCoroutine(
    ConvaiManager manager, CancellationToken cancellationToken)
{
    var connection = manager.ConnectAsync(cancellationToken);
    yield return new WaitUntil(() => connection.IsCompleted);

    if (connection.IsSuccessful)
        Debug.Log("Room connected.");
    else if (connection.HasError)
        Debug.LogWarning($"Connection failed: {connection.Error.Code}");
}
```

## Pass cancellation to the operation

Pass a `CancellationToken` to the SDK method that supports it. Cancel the source when the user cancels or the owning component is disabled. `operation.Cancel()` only works if the producer supplied a cancellation source to the operation wrapper; SDK task wrappers generally do not. It is not a substitute for passing a token.

In WebGL players, framework timer/thread-pool APIs such as `CancelAfter` and timer-based `CancellationTokenSource` do not reliably drive timeouts. Use a Unity frame-driven timer or coroutine to call `Cancel()` on your source. The SDK uses an internal player-loop timer for its own timeouts; that internal helper is not an application API.

## Follow a connection with another operation

Await the connection before making a second SDK call. Treat each await as a separate failure point. Use an indeterminate loading indicator while a connection is pending.

For transcript updates as replies arrive, use [Transcript API](transcript-api.md).

## Verify the integration

Check successful connection, a refused connection, and cancellation while connecting. Confirm that your UI stops waiting in each case and that disabling the component removes its callbacks. For API details, see [Asynchronous operation reference](operation-and-stream-types.md) and [Transcript API](transcript-api.md).
