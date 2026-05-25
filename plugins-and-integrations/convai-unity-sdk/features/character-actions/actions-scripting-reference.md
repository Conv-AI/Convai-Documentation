---
title: Character actions scripting reference
description: API reference for the Convai character actions system — dispatcher types, executor interface, config classes, invocation objects, result types, and enums.
---

Complete API reference for all public types in the Convai character actions system. All types are in the `Convai.Runtime.Actions`, `Convai.Runtime.Components`, or `Convai.Shared.Actions` namespaces unless noted.

## ConvaiActionDispatcher

`MonoBehaviour` — `Convai.Runtime.Actions`

Menu path: `Add Component → Convai → Convai Action Dispatcher`

Constraints: `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)`

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `BatchPolicy` | `ConvaiActionBatchPolicy` | Current batch policy (read-only from code; set in Inspector) |
| `FailurePolicy` | `ConvaiActionBatchFailurePolicy` | Current failure policy (read-only from code; set in Inspector) |
| `OnBatchStarted` | `UnityEvent` | Fires when a batch begins execution |
| `OnStepStarted` | `ConvaiActionInvocationUnityEvent` | Fires at the start of each action step |
| `OnStepSucceeded` | `ConvaiActionInvocationUnityEvent` | Fires when an executor returns `Succeeded` |
| `OnStepFailed` | `ConvaiActionInvocationUnityEvent` | Fires when a step fails (Failed, Canceled, or TimedOut) |
| `OnStepUnhandled` | `ConvaiActionInvocationUnityEvent` | Fires when an executor returns `Unhandled` |
| `OnBatchCompleted` | `UnityEvent` | Fires when all batch steps finish without the batch being aborted |
| `OnBatchAborted` | `UnityEvent` | Fires when `StopBatch` policy cuts the batch short after a failure |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `EnqueueActions` | `void EnqueueActions(IReadOnlyList<ConvaiActionCommand> actions)` | Submits a batch to the dispatcher. Respects the active `BatchPolicy`. |

## ConvaiActionConfigSource

`MonoBehaviour` — `Convai.Runtime.Components`

Menu path: `Add Component → Convai → Convai Action Config Source`

Constraints: `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)`

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Definitions` | `IReadOnlyList<ConvaiActionDefinition>` | The authored action definitions list |
| `Objects` | `IReadOnlyList<ConvaiActionObjectDefinition>` | The authored actionable objects list |
| `Characters` | `IReadOnlyList<ConvaiActionCharacterDefinition>` | The authored actionable characters list |
| `InitialAttentionObject` | `string` | Object name to pre-seed as the NPC's focus at connect time |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `BuildActionConfig` | `ConvaiActionConfig BuildActionConfig()` | Builds and returns the connect-time payload. Returns `null` if no valid definitions exist. |
| `TryResolveObject` | `bool TryResolveObject(string objectName, out ConvaiActionObjectDefinition actionObject)` | Looks up a registered object by name (case-insensitive). Returns `true` if found. |

## ConvaiCharacter — action-relevant members

`MonoBehaviour` — `Convai.Runtime.Components`

### Events

| Event | Type | Description |
| --- | --- | --- |
| `OnActionsReceived` | `event Action<IReadOnlyList<ConvaiActionCommand>>` | Fires when Convai returns an action batch for this character. Fires before the dispatcher processes it. |

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `ActionConfig` | `ConvaiActionConfig` | Returns a clone of the active session's action config. May be `null` before connect. |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `GetActionConfigSource` | `ConvaiActionConfigSource GetActionConfigSource()` | Returns the `ConvaiActionConfigSource` on this `GameObject`, or `null`. |
| `SetCurrentAttentionObject` | `void SetCurrentAttentionObject(string objectName, string runLlm = "false")` | Updates backend grounding to the named object. Requires an active conversation. Silently ignored if the object name is not in the active action config. |
| `SetCurrentAttentionObject` | `void SetCurrentAttentionObject(ConvaiActionObjectDefinition actionObject, string runLlm = "false")` | Overload that accepts a definition reference. |
| `ClearCurrentAttentionObject` | `void ClearCurrentAttentionObject(string runLlm = "false")` | Clears the current attention object. Requires an active conversation. |

## RoomSessionConnectOptions — action fields

`Convai.Runtime.Room`

| Field | Type | Description |
| --- | --- | --- |
| `ActionConfigOverride` | `ConvaiActionConfig` | When set, replaces `ConvaiActionConfigSource.BuildActionConfig()` for this session. |
| `ActionDefinitionsOverride` | `List<ConvaiActionDefinition>` | When set, replaces the Inspector action definitions for this session. Filtered against `ActionConfigOverride.Actions` if both are set. |

## ConvaiActionCommand

`Convai.Shared.Types` — Serializable sealed class

Structured action command for one step, as returned by the backend.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Name` | `string` | Required. Action name selected by the backend (e.g., `"Move To"`). |
| `Target` | `string` | Optional. Object or character name the backend resolved as the target. `null` if no target. |
| `HasTarget` | `bool` | `true` when `Target` is non-empty. |

### Constructor

```csharp
new ConvaiActionCommand("Move To", "Crate")  // name + target
new ConvaiActionCommand("Wave")              // name only
```

## ConvaiActionConfig

`Convai.Shared.Actions` — Serializable sealed class

Connect-time action affordances serialized into the session connect payload.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Actions` | `List<string>` | Action names allowed for this session. Only names are sent — executor bindings stay local. |
| `Objects` | `List<ConvaiActionObjectDefinition>` | Objects the backend may reference as targets. `GameObjectReference` is never serialized. |
| `Characters` | `List<ConvaiActionCharacterDefinition>` | Characters the backend may reference as targets. `GameObjectReference` is never serialized. |
| `CurrentAttentionObject` | `string` | Initial attention object name. Must match an entry in `Objects`. |

## ConvaiActionDefinition

`Convai.Runtime.Actions` — Serializable sealed class

Local Unity binding between a backend action name and an executor component. Only `ActionName` is sent to the backend.

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `ActionName` | `string` | The action name that maps to this definition. Case-insensitive matching at runtime. |
| `TargetRequirement` | `ConvaiActionTargetRequirement` | What kind of target this action requires. |
| `Executor` | `MonoBehaviour` | The component that performs the behavior. Must implement `IConvaiActionExecutor`. |
| `TimeoutSeconds` | `float` | Maximum execution time in seconds. `0` = no timeout. |

## ConvaiActionObjectDefinition

`Convai.Shared.Actions` — Serializable sealed class

### Properties

| Property | Type | Serialized | Description |
| --- | --- | --- | --- |
| `Name` | `string` | Yes (`"name"`) | Identifier used in action commands. Case-insensitive matching. |
| `Description` | `string` | Yes (`"description"`) | Natural language description sent to Convai for reference resolution. |
| `GameObjectReference` | `GameObject` | **No** (`[JsonIgnore]`) | Local scene reference. Never sent to Convai. |

## ConvaiActionCharacterDefinition

`Convai.Shared.Actions` — Serializable sealed class

### Properties

| Property | Type | Serialized | Description |
| --- | --- | --- | --- |
| `Name` | `string` | Yes (`"name"`) | Identifier for this character target. |
| `Bio` | `string` | Yes (`"bio"`) | Short description sent to Convai (e.g., "Site safety supervisor"). |
| `GameObjectReference` | `GameObject` | **No** (`[JsonIgnore]`) | Local scene reference. Never sent to Convai. |

## ConvaiActionInvocation

`Convai.Runtime.Actions` — Sealed class

Typed execution context passed to executors and all dispatcher events.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Command` | `ConvaiActionCommand` | The raw backend command for this step. |
| `Definition` | `ConvaiActionDefinition` | The matched local action definition. `null` if no definition was found (step will fail). |
| `ResolvedTarget` | `ConvaiResolvedActionTarget` | The resolved target binding. `null` if the action has no target or resolution failed. |
| `Character` | `ConvaiCharacter` | The NPC executing this action. |
| `BatchIndex` | `int` | Sequential index of the containing batch across the dispatcher's lifetime. |
| `StepIndex` | `int` | 0-based index of this step within the current batch. |

## ConvaiResolvedActionTarget

`Convai.Runtime.Actions` — Serializable sealed class

Resolved target for one action step.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Kind` | `ConvaiActionTargetKind` | Whether the resolved target is an Object, Character, or None. |
| `Name` | `string` | The resolved name (from the backend command). |
| `ObjectBinding` | `ConvaiActionObjectDefinition` | The matched object definition. `null` if `Kind != Object`. |
| `CharacterBinding` | `ConvaiActionCharacterDefinition` | The matched character definition. `null` if `Kind != Character`. |
| `GameObjectReference` | `GameObject` | The scene `GameObject` from the matching binding. The primary access point in executors. |

## ConvaiActionExecutionResult

`Convai.Runtime.Actions` — Readonly struct

Return type for `IConvaiActionExecutor.ExecuteAsync`.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Status` | `ConvaiActionExecutionStatus` | The outcome of this execution step. |
| `Message` | `string` | Optional human-readable detail. Available in event handlers and logs. |
| `Exception` | `Exception` | The exception that caused failure, if any. |

### Factory methods

| Method | Signature | Use when |
| --- | --- | --- |
| `Succeeded` | `static ConvaiActionExecutionResult Succeeded()` | The behavior completed successfully. |
| `Failed` | `static ConvaiActionExecutionResult Failed(string message = null, Exception exception = null)` | A genuine error occurred. |
| `Canceled` | `static ConvaiActionExecutionResult Canceled()` | The `CancellationToken` was signaled. |
| `TimedOut` | `static ConvaiActionExecutionResult TimedOut()` | **Do not call manually.** The dispatcher returns this automatically when `TimeoutSeconds` expires. |
| `Unhandled` | `static ConvaiActionExecutionResult Unhandled(string message = null)` | This executor intentionally declines the invocation. |

## IConvaiActionExecutor

`Convai.Runtime.Actions` — Interface

The extension point for all action behavior. Implement on any `MonoBehaviour`.

```csharp
public interface IConvaiActionExecutor
{
    Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken);
}
```

## Enumerations

### ConvaiActionBatchPolicy

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `Queue` | `0` | New batches wait until the current batch completes. Default. |
| `ReplaceCurrent` | `1` | Cancels the active step and all pending batches; starts the new batch immediately. |
| `DropIncoming` | `2` | Discards new batches until all current and queued work is finished. |

### ConvaiActionBatchFailurePolicy

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `StopBatch` | `0` | A failed step aborts the remaining batch. `OnBatchAborted` fires. Default. |
| `ContinueBatch` | `1` | Execution continues to the next step regardless. `OnBatchCompleted` fires. |

### ConvaiActionTargetRequirement

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `None` | `0` | Action does not require a target. |
| `Object` | `1` | Action requires a resolved object target. |
| `Character` | `2` | Action requires a resolved character target. |
| `Either` | `3` | Action accepts either an object or a character as target. |

### ConvaiActionTargetKind

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `None` | `0` | No target resolved. |
| `Object` | `1` | Target is a registered object. |
| `Character` | `2` | Target is a registered character. |

### ConvaiActionExecutionStatus

`Convai.Runtime.Actions`

| Value | Integer | Dispatcher event fired |
| --- | --- | --- |
| `Succeeded` | `0` | `OnStepSucceeded` |
| `Failed` | `1` | `OnStepFailed` |
| `Canceled` | `2` | `OnStepFailed` |
| `TimedOut` | `3` | `OnStepFailed` |
| `Unhandled` | `4` | `OnStepUnhandled` |

## ConvaiActionInvocationUnityEvent

`Convai.Runtime.Actions` — Serializable class extending `UnityEvent<ConvaiActionInvocation>`

Wrapper type that makes `ConvaiActionInvocation` serializable as a UnityEvent parameter. Assign handlers in the Inspector like any standard UnityEvent. The event's single argument is the `ConvaiActionInvocation` for that step.

## ConvaiActionDebugProbe

`Convai.Runtime.Actions` — Sealed `MonoBehaviour`

Menu path: `Add Component → Convai → Debug → Convai Action Debug Probe`

Constraints: `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)`

See [Troubleshoot character actions](debugging-and-troubleshooting.md) for the full Inspector field reference and usage guide.

### Context menu actions

| Command | Effect |
| --- | --- |
| `Inject Test Batch` | Submits a `Move To` command targeting the first registered object to the dispatcher. Tests the pipeline without a live conversation. |
| `Reset Probe State` | Resets all counters and text fields to zero/empty. |

## Next steps

{% content-ref url="usage-examples.md" %}
[Character actions examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="debugging-and-troubleshooting.md" %}
[Troubleshoot character actions](debugging-and-troubleshooting.md)
{% endcontent-ref %}
