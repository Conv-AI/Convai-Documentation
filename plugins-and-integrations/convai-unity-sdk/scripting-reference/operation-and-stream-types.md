---
title: Asynchronous operation reference
description: Check the result of an asynchronous SDK operation, handle cancellation and errors, and observe its completion from an async method or coroutine.
last_reviewed: "5.0.0-pre.1"
---

`IConvaiOperation<T>` in `Convai.Runtime.Core.Async` represents one asynchronous result. `RoomSession` and `Unit` are in `Convai.Runtime.Core.Coordinators`. `Unit` represents completion without a value.

## Operation members

| Member | Contract |
| --- | --- |
| `Status` | `Created`, `Running`, `Succeeded`, `Faulted`, or `Canceled` |
| `IsCompleted`, `IsSuccessful`, `IsCanceled`, `HasError` | State checks on the wrapped task |
| `Error` | Structured fault information |
| `GetAwaiter()`, `AsTask()` | Await the result and propagate the underlying exception |
| `Cancel()` | Request cancellation when the wrapper owns a cancellation source |

Pass a cancellation token to SDK methods that accept one. SDK methods normally wrap tasks without a wrapper-owned cancellation source.

## Error types

`ConvaiError` contains `Code`, `Message`, `Exception`, and `IsEmpty`. `FromException` preserves the code of a `ConvaiOperationException`. For other exceptions it uses the supplied fallback code, which defaults to `exception`.

`ConvaiOperationException.Code` is the SDK's machine-readable operation error. It falls back to `operation.failed` for an empty code. Also handle cancellation and ordinary argument or state exceptions where applicable.

## Producer APIs

| Member | Purpose |
| --- | --- |
| `ConvaiOperation<T>.FromTask(task)` | Wrap a task |
| `ConvaiOperation<T>.FromTask(task, cts)` | Wrap a task and give `Cancel()` a source to cancel |
| `ConvaiOperation<T>.Succeeded`, `Failed`, `Canceled` | Create completed operations |

## Migrate progress, coroutines, and streams

For coroutines, poll `IsCompleted` and handle success, failure, and cancellation. For chaining, await the result and pass it to the next method. Show a busy indicator while an SDK operation is pending. Use the [Transcript API](transcript-api.md) for room history and live captions. Integrations that previously used the standalone text stream can follow [Migrate from the standalone text client](../advanced-topics/interaction-text-client.md) to move to room chat.

## Related pages

- [Async patterns](async-patterns.md)
- [Runtime architecture](../core-concepts/runtime-architecture.md)
