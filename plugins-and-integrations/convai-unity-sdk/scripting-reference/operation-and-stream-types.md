# operation and stream types

Most SDK methods that perform async work return `IConvaiOperation<T>` instead of `Task<T>`. Methods that produce a continuous sequence of values return `IConvaiStream<T>`. These types are designed to work across Unity's coroutine system, C# async/await, and progress-driven flows — without forcing a dependency on `Task` throughout your codebase.

For usage patterns and code examples, see [Async Patterns](/broken/pages/a2541cd5b9d0e9324142e7f69a7468f9a2c2697b).

***

## Why Custom Async Types?

| Requirement                   | `Task<T>`               | `IConvaiOperation<T>`                |
| ----------------------------- | ----------------------- | ------------------------------------ |
| Works in coroutines           | No                      | Yes — `ToCoroutine()`                |
| Typed error without exception | No                      | Yes — `Error` property               |
| Progress reporting            | No                      | Yes — `Progress` property            |
| Direct `await`                | Yes                     | Yes — `GetAwaiter()`                 |
| Cancellation                  | Via `CancellationToken` | Via `CancellationToken` + `Cancel()` |

***

## `IConvaiOperation<T>`

The result handle for any SDK async operation. Returned by `ConnectAsync`, `DisconnectAsync`, `StartListeningAsync`, `WaitForCharacterReadyAsync`, and other methods.

### Status Properties

| Property       | Type              | Description                                                                                                   |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------- |
| `Status`       | `OperationStatus` | Current lifecycle state of the operation                                                                      |
| `IsCompleted`  | `bool`            | True when status is `Succeeded`, `Faulted`, or `Canceled`                                                     |
| `IsSuccessful` | `bool`            | True when status is `Succeeded`                                                                               |
| `IsCanceled`   | `bool`            | True when status is `Canceled`                                                                                |
| `HasError`     | `bool`            | True when status is `Faulted`                                                                                 |
| `Error`        | `ConvaiError`     | Populated when `HasError` is true; default when successful or pending                                         |
| `Progress`     | `float`           | Completion estimate in the range 0.0–1.0. Not all operations report progress — check `Status` for completion. |

### Async/Await

| Member         | Description                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------------- |
| `GetAwaiter()` | Returns a `TaskAwaiter<T>`. Enables `await operation` directly. Throws `ConvaiOperationException` on failure. |
| `AsTask()`     | Returns the underlying `Task<T>`. Use when you need to pass to Task-based APIs.                               |

### Coroutine

| Member                                                                        | Description                                                                                                                                   |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `ToCoroutine(Action<T> onSuccess = null, Action<ConvaiError> onError = null)` | Returns an `IEnumerator`. Pass to `StartCoroutine()`. `onSuccess` receives the result; `onError` receives the error if the operation faulted. |

### Chaining

| Member                                               | Description                                                                                              |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `ContinueWith<TNext>(Func<T, TNext> selector)`       | Transforms the result when the operation succeeds. Returns a new `IConvaiOperation<TNext>`.              |
| `ContinueWith<TNext>(Func<T, Task<TNext>> selector)` | Async transform. Returns a new `IConvaiOperation<TNext>` that resolves when the selector task completes. |

### Cancellation

| Member     | Description                                                                                                       |
| ---------- | ----------------------------------------------------------------------------------------------------------------- |
| `Cancel()` | Requests cooperative cancellation. The operation transitions to `Canceled` when the SDK acknowledges the request. |

***

## `OperationStatus` Enum

| Value           | Description                                            |
| --------------- | ------------------------------------------------------ |
| `Created` (0)   | Operation has been created but not yet started         |
| `Running` (1)   | Operation is executing                                 |
| `Succeeded` (2) | Operation completed successfully. Result is available. |
| `Faulted` (3)   | Operation failed. `Error` is populated.                |
| `Canceled` (4)  | Operation was canceled before completing               |

**Lifecycle:** `Created → Running → Succeeded / Faulted / Canceled`

***

## `ConvaiError` Struct

Carries structured error information without requiring exception handling. Populated in `IConvaiOperation<T>.Error` when `HasError` is true.

| Member      | Type        | Description                                                            |
| ----------- | ----------- | ---------------------------------------------------------------------- |
| `Code`      | `string`    | Machine-readable error code, e.g. `"connection.timeout"`               |
| `Message`   | `string`    | Human-readable description                                             |
| `Exception` | `Exception` | Underlying exception, if the error originated from one. May be `null`. |
| `IsEmpty`   | `bool`      | True when this is a default (no-error) value                           |

### Static Factory

```csharp
ConvaiError.FromException(Exception exception, string code = "exception")
```

Creates a `ConvaiError` from an exception. Useful in custom error paths.

### Equality

`ConvaiError` is a struct and supports `Equals`, `GetHashCode`, and `ToString()`.

***

## `ConvaiOperationException`

Thrown when you `await` an `IConvaiOperation<T>` and the operation faulted. Extends `Exception`.

| Property  | Type     | Description                                      |
| --------- | -------- | ------------------------------------------------ |
| `Code`    | `string` | The error code from the underlying `ConvaiError` |
| `Message` | `string` | Inherited — human-readable description           |

**`HasError` vs. thrown exception:**

* When using **coroutines** (`ToCoroutine`), errors are delivered to the `onError` callback. No exception is thrown.
* When using **async/await**, a faulted operation throws `ConvaiOperationException`. Catch it with `try/catch`.
* `HasError` is `true` in both cases — you can poll it at any time regardless of consumption pattern.

***

## `IConvaiStream<T>`

Returned by methods that produce a continuous sequence of values over time, such as streaming transcript tokens or streaming audio frames. Implements `IAsyncDisposable`.

### Properties

| Property | Type           | Description                           |
| -------- | -------------- | ------------------------------------- |
| `Status` | `StreamStatus` | Current lifecycle state of the stream |
| `Error`  | `ConvaiError`  | Populated when `Status` is `Faulted`  |

### Methods

| Method                                         | Returns               | Description                                                                         |
| ---------------------------------------------- | --------------------- | ----------------------------------------------------------------------------------- |
| `ReadAllAsync(CancellationToken ct = default)` | `IAsyncEnumerable<T>` | Yields items as they arrive. Completes when the stream ends. Respects cancellation. |
| `DisposeAsync()`                               | `ValueTask`           | Disposes the stream and releases resources. Always call in an `await using` block.  |

```csharp
await using var stream = GetSomeStream();
await foreach (var item in stream.ReadAllAsync(destroyCancellationToken))
{
    ProcessItem(item);
}
```

***

## `StreamStatus` Enum

| Value           | Description                                          |
| --------------- | ---------------------------------------------------- |
| `Created` (0)   | Stream created but not yet streaming                 |
| `Streaming` (1) | Stream is actively yielding items                    |
| `Completed` (2) | All items have been delivered; stream ended normally |
| `Faulted` (3)   | Stream encountered an error. `Error` is populated.   |
| `Canceled` (4)  | Stream was canceled before completing                |

**Lifecycle:** `Created → Streaming → Completed / Faulted / Canceled`

***

## `Unit` Struct

```csharp
Unit.Value // the only instance
```

A void-equivalent used as the type parameter when an operation has no meaningful return value. Operations like `DisconnectAsync()` and `StopListeningAsync()` return `IConvaiOperation<Unit>` — you `await` them for the side effect, not the result.

`Unit` supports equality (`==`, `!=`, `Equals`) and `ToString()` returns `"()"`.

***

## Next Steps

{% content-ref url="/broken/pages/a2541cd5b9d0e9324142e7f69a7468f9a2c2697b" %}
[Broken link](/broken/pages/a2541cd5b9d0e9324142e7f69a7468f9a2c2697b)
{% endcontent-ref %}
