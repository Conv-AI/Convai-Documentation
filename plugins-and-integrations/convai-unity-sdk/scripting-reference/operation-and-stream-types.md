---
title: Operation and stream types
description: Reference the Unity SDK operation and stream contracts, including completion state, structured errors, cancellation, and custom producers.
last_reviewed: "5.0.0-preview"
---

`IConvaiOperation<T>` represents one asynchronous result. `IConvaiStream<T>` represents a producer-owned sequence. These types are in `Convai.Runtime.Core.Async`; `Unit` and `RoomSession` are in `Convai.Runtime.Core.Coordinators`.

## Operation members

| Member | Contract |
| --- | --- |
| `Status` | `Created`, `Running`, `Succeeded`, `Faulted`, or `Canceled` |
| `IsCompleted`, `IsSuccessful`, `IsCanceled`, `HasError` | State checks on the wrapped task |
| `Error` | Structured fault information; not the result value |
| `Progress` | Producer-reported progress, or zero until success and one afterward |
| `GetAwaiter()`, `AsTask()` | Await the result; rethrow the original task exception |
| `ToCoroutine(onSuccess, onError)` | Unity coroutine adapter |
| `ContinueWith(selector)` | Transform a successful value, with synchronous or task-returning selectors |
| `Cancel()` | Cancels only the source supplied when constructing the wrapper |

SDK methods normally wrap tasks without a cancellation source. Pass cancellation to the method's token parameter. No SDK operation supplies intermediate progress through `ReportProgress`, so use a busy indicator rather than a percentage estimate.

Await can throw `ConvaiOperationException`, `OperationCanceledException`, or ordinary argument/state exceptions. Catch the cases your call can produce. `ToCoroutine` maps a fault to `ConvaiError`; it logs an unhandled fault when `onError` is absent and passes `canceled` when cancellation has an error callback.

## Error types

`ConvaiError` contains `Code`, `Message`, `Exception`, and `IsEmpty`. `FromException` preserves the code of a `ConvaiOperationException`; other exceptions use the supplied fallback code, defaulting to `exception`.

`ConvaiOperationException.Code` is the SDK's machine-readable operation error. It falls back to `operation.failed` for an empty code. Do not assume every failed task throws this type.

## Producer APIs

Use these when implementing your own operation, not when consuming an SDK operation.

| Type/member | Purpose |
| --- | --- |
| `ConvaiOperation<T>.FromTask(task)` | Wrap a task without wrapper-owned cancellation |
| `FromTask(task, cts)` | Give `Cancel()` a source to cancel |
| `Succeeded`, `Failed`, `Canceled` | Create already-completed operations |
| `ConvaiOperationSource<T>.Operation` | Operation exposed to consumers |
| `Token` | Producer's cancellation token |
| `ReportProgress` | Publish intermediate progress |
| `SetResult`, `SetException`, `SetCanceled` | Complete the operation |
| `TrySetResult`, `TrySetException`, `TrySetCanceled` | Complete without throwing if already completed |

A producer must actually observe its token for cancellation to stop its work.

## Streams

`IConvaiStream<T>` exposes `Status`, `Error`, `ReadAllAsync(CancellationToken)`, and asynchronous disposal. `StreamStatus` is `Created`, `Streaming`, `Completed`, `Faulted`, or `Canceled`. `ConvaiStream<T>` is the concrete implementation for custom producers.

The room transcript API does not return this type. The standalone `IConversationSession.OpenResponseStream` contract returns `IConvaiStream<ConversationResponsePart>` for a custom provider; the default manager does not install a standalone conversation provider.

## Related pages

- [Async patterns](async-patterns.md)
- [Runtime architecture](../core-concepts/runtime-architecture.md)
