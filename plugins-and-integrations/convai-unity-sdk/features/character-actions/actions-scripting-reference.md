---
title: Character actions scripting reference
description: API reference for the Convai character actions system — dispatcher types, executor interface, config classes, invocation objects, result types, and enums.
last_reviewed: "4.4.0"
---

Complete API reference for all public types in the Convai character actions system. Types are in the `Convai.Runtime.Actions`, `Convai.Runtime.Components`, `Convai.Shared.Actions`, or `Convai.Shared.Types` namespaces unless noted.

## `ConvaiActionDispatcher`

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
| `OnStepCompleted` | `ConvaiActionStepReportUnityEvent` | Fires after every step, success or not, with the full `ConvaiActionStepReport` |
| `OnBatchCompleted` | `UnityEvent` | Fires when all batch steps finish without the batch being aborted |
| `OnBatchAborted` | `UnityEvent` | Fires when `StopBatch` policy cuts the batch short after a failure |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `EnqueueActions` | `void EnqueueActions(IReadOnlyList<ConvaiActionCommand> actions)` | Submits a batch to the dispatcher. Respects the active `BatchPolicy`. |

## `ConvaiActionConfigSource`

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

## `ConvaiCharacter` — action-relevant members

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

{% hint style="info" %}
Runtime updates to the current attention object are handled by the dynamic context system, not by `ConvaiCharacter` directly. See [Dynamic context scripting API](../dynamic-context/dynamic-context-scripting-api.md).
{% endhint %}

## `RoomSessionConnectOptions` — action fields

`Convai.Runtime.Room`

| Field | Type | Description |
| --- | --- | --- |
| `ActionConfigOverride` | `ConvaiActionConfig` | When set, replaces `ConvaiActionConfigSource.BuildActionConfig()` for this session. |
| `ActionDefinitionsOverride` | `List<ConvaiActionDefinition>` | When set, replaces the Inspector action definitions for this session. Filtered against `ActionConfigOverride.Actions` if both are set. |

## `ConvaiActionCommand`

`Convai.Shared.Types` — Serializable sealed class

Structured action command for one step, as returned by the backend.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Name` | `string` | Required. Action name selected by the backend (e.g., `"Move To"`). |
| `Target` | `string` | Optional. Object or character name the backend resolved as the target. `null` if no target. |
| `ActionString` | `string` | Raw action string reconstructed from the backend `Name` and `Target`. |
| `Parameters` | `Dictionary<string, ConvaiActionParameterValue>` | Typed parameters parsed from the backend response and the active Unity template. Keyed case-insensitively. |
| `WaitForBotSpeech` | `bool` | Whether the first action in a fresh batch should wait for character speech before running. |
| `DelayAfterBotSpeechSeconds` | `float` | Optional delay applied after the speech gate releases. |
| `Enriched` | `bool` | `true` once the command has been enriched against the active action templates. The dispatcher enriches unmarked commands exactly once before dispatch. |
| `HasTarget` | `bool` | `true` when `Target` is non-empty. |

### Constructor

```csharp
new ConvaiActionCommand("Move To", "Crate")  // name + target
new ConvaiActionCommand("Wave")              // name only
```

The constructor normalizes `Name` and `Target` and derives `ActionString` from them. `Parameters`, `WaitForBotSpeech`, `DelayAfterBotSpeechSeconds`, and `Enriched` default to their empty values and are populated by the backend response or by enrichment.

## `ConvaiActionParameterValue`

`Convai.Shared.Types` — Serializable sealed class

One typed action parameter after enrichment. Every representation is populated best-effort from the raw text; `Type` says which one the authored template intends.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Type` | `ConvaiActionParameterType` | Effective type after coercion. An authored `Auto` resolves to a concrete type. |
| `RawValue` | `string` | Trimmed raw text this value was parsed from. |
| `StringValue` | `string` | The value as text (same as `RawValue` after trimming). |
| `NumberValue` | `float` | Parsed float, or `0` when the text is not numeric. |
| `BoolValue` | `bool` | Parsed bool, or `false` when the text is not a recognized boolean. |
| `ResolvedReference` | `ConvaiActionParameterReference` | Matched authored target when the text named one; `null` otherwise. |
| `IsConstraintMatch` | `bool` | `false` only when a `Choice` parameter's text is not one of its authored choices. |

Read parameters through `ConvaiActionInvocation.TryGetParameter`, `GetString`, `GetNumber`, `GetBool`, or `GetReference` rather than indexing `ConvaiActionCommand.Parameters` directly.

## `ConvaiActionParameterReference`

`Convai.Shared.Types` — Serializable sealed class

Name-and-kind handle a `Reference` parameter resolved to during enrichment.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Name` | `string` | Authored target name the raw value matched (trimmed, never `null`). |
| `Kind` | `ConvaiActionTargetKind` | Whether the name matched an authored object or character. |

`ConvaiActionParameterReference` is a lookup key, not a scene binding — it does not carry a `GameObjectReference`. Resolve it to a live `GameObject` through `ConvaiActionInvocation.GetReference(name)`, which returns a `ConvaiResolvedActionTarget`.

## `ConvaiActionConfig`

`Convai.Shared.Actions` — Serializable sealed class

Connect-time action affordances serialized into the session connect payload.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Actions` | `List<string>` | Action names allowed for this session. Only names are sent — executor bindings stay local. |
| `Objects` | `List<ConvaiActionObjectDefinition>` | Objects the backend may reference as targets. `GameObjectReference` is never serialized. |
| `Characters` | `List<ConvaiActionCharacterDefinition>` | Characters the backend may reference as targets. `GameObjectReference` is never serialized. |
| `CurrentAttentionObject` | `string` | Initial attention object name. Must match an entry in `Objects`. |

## `ConvaiActionConfigPatch`

`Convai.Shared.Actions` — Serializable sealed class

Runtime patch for the active session's action affordances.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Actions` | `List<string>` | Replacement action list. |
| `Characters` | `List<ConvaiActionCharacterDefinition>` | Replacement character-target list. |
| `Objects` | `List<ConvaiActionObjectDefinition>` | Replacement object-target list. |
| `CurrentAttentionObject` | `string` | Attention update resolved after list replacement. |

{% hint style="warning" %}
Each field follows omitted-versus-empty semantics: a `null` list or string preserves the current value, and an empty list or string explicitly clears that value. Set a field only when you intend to change it.
{% endhint %}

## `ConvaiActionDefinition`

`Convai.Runtime.Actions` — Serializable sealed class

Local Unity binding between a backend action name and an executor component. Only the rendered wire template (from `ToActionConfigString`) is sent to the backend.

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `ActionName` | `string` | The action name that maps to this definition. Case-insensitive matching at runtime. |
| `Description` | `string` | Optional description sent to Convai for grounding. |
| `Parameters` | `List<ConvaiActionParameterDefinition>` | Ordered typed parameters rendered into the wire template. |
| `TargetRequirement` | `ConvaiActionTargetRequirement` | What kind of target this action requires. |
| `Executor` | `MonoBehaviour` | The component that performs the behavior. Must implement `IConvaiActionExecutor`. |
| `TimeoutSeconds` | `float` | Maximum execution time in seconds. `0` = no timeout. |
| `FailurePolicyOverride` | `ConvaiActionFailurePolicyOverride` | Per-action override of the dispatcher's batch failure policy. |
| `WaitForBotSpeech` | `bool` | Whether the first step of a fresh batch waits for character speech. |
| `DelayAfterBotSpeechSeconds` | `float` | Optional delay after the speech gate releases. |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `ToActionConfigString` | `string ToActionConfigString()` | Renders the wire template string sent to Convai for this definition. |

## `ConvaiActionParameterDefinition`

`Convai.Runtime.Actions` — Serializable sealed class

Authoring definition for a single typed action parameter, referenced by `ConvaiActionDefinition.Parameters`.

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `Name` | `string` | Parameter name used as the wire key and template anchor. |
| `Description` | `string` | Optional description sent to Convai for grounding. |
| `Type` | `ConvaiActionParameterType` | Declared parameter type. `Auto` infers from the value. Default `Auto`. |
| `Connector` | `string` | Optional connector word rendered before the parameter in the wire template (for example `"on"` or `"in"`). |
| `Choices` | `List<string>` | Allowed values when `Type` is `Choice`. |

## `ConvaiActionObjectDefinition`

`Convai.Shared.Actions` — Serializable sealed class

### Properties

| Property | Type | Serialized | Description |
| --- | --- | --- | --- |
| `Name` | `string` | Yes (`"name"`) | Identifier used in action commands. Case-insensitive matching. |
| `Description` | `string` | Yes (`"description"`) | Natural language description sent to Convai for reference resolution. |
| `GameObjectReference` | `GameObject` | **No** (`[JsonIgnore]`) | Local scene reference. Never sent to Convai. |

## `ConvaiActionCharacterDefinition`

`Convai.Shared.Actions` — Serializable sealed class

### Properties

| Property | Type | Serialized | Description |
| --- | --- | --- | --- |
| `Name` | `string` | Yes (`"name"`) | Identifier for this character target. |
| `Bio` | `string` | Yes (`"bio"`) | Short description sent to Convai (e.g., "Site safety supervisor"). |
| `GameObjectReference` | `GameObject` | **No** (`[JsonIgnore]`) | Local scene reference. Never sent to Convai. |

## `ConvaiActionInvocation`

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

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `TryGetParameter` | `bool TryGetParameter(string name, out ConvaiActionParameterValue value)` | Attempts to read a typed parameter by name (case-insensitive). |
| `GetString` | `string GetString(string name, string fallback = "")` | Reads a string parameter, returning `fallback` when absent. |
| `GetNumber` | `float GetNumber(string name, float fallback = 0f)` | Reads a numeric parameter, returning `fallback` when absent. |
| `GetBool` | `bool GetBool(string name, bool fallback = false)` | Reads a boolean parameter, returning `fallback` when absent. |
| `GetReference` | `ConvaiResolvedActionTarget GetReference(string name)` | Resolves a reference parameter against the character's action config, falling back to the definition's target requirement when the parameter carries no explicit kind. |

## `ConvaiResolvedActionTarget`

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

## `ConvaiActionExecutionResult`

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
| `Succeeded` | `static ConvaiActionExecutionResult Succeeded(string message = null)` | The behavior completed successfully. |
| `Failed` | `static ConvaiActionExecutionResult Failed(string message = null, Exception exception = null)` | A genuine error occurred. |
| `Canceled` | `static ConvaiActionExecutionResult Canceled()` | The `CancellationToken` was signaled. |
| `TimedOut` | `static ConvaiActionExecutionResult TimedOut()` | **Do not call manually.** The dispatcher returns this automatically when `TimeoutSeconds` expires. |
| `Unhandled` | `static ConvaiActionExecutionResult Unhandled(string message = null)` | This executor intentionally declines the invocation. |

## `ConvaiActionStepReport`

`Convai.Runtime.Actions` — Serializable sealed class

Completed-step report emitted on `ConvaiActionDispatcher.OnStepCompleted`.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Invocation` | `ConvaiActionInvocation` | The invocation the report describes. |
| `Result` | `ConvaiActionExecutionResult` | Raw executor result for the step. |
| `BatchAborted` | `bool` | Whether this step aborted the remaining batch. |
| `Message` | `string` | Success detail, or the failure message for non-success statuses. |
| `FailureMessage` | `string` | Failure detail including the batch consequence. Empty on success. |

## `IConvaiActionExecutor`

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

Return `ConvaiActionExecutionResult.Unhandled` when the component cannot service the invocation (for example, a missing rig or peer) so the dispatcher can report it distinctly. Honor `cancellationToken` for batch replacement and timeouts.

## Enumerations

The action system's enums, grouped here for reference — each is used by one or more of the types above.

### `ConvaiActionBatchPolicy`

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `Queue` | `0` | New batches wait until the current batch completes. Default. |
| `ReplaceCurrent` | `1` | Cancels the active step and all pending batches; starts the new batch immediately. |
| `DropIncoming` | `2` | Discards new batches until all current and queued work is finished. |

### `ConvaiActionBatchFailurePolicy`

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `StopBatch` | `0` | A failed step aborts the remaining batch. `OnBatchAborted` fires. Default. |
| `ContinueBatch` | `1` | Execution continues to the next step regardless. `OnBatchCompleted` fires. |

### `ConvaiActionTargetRequirement`

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `None` | `0` | Action does not require a target. |
| `Object` | `1` | Action requires a resolved object target. |
| `Character` | `2` | Action requires a resolved character target. |
| `Either` | `3` | Action accepts either an object or a character as target. |

### `ConvaiActionFailurePolicyOverride`

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `UseDispatcherDefault` | `0` | Follow the `ConvaiActionDispatcher` failure policy. Default. |
| `StopBatch` | `1` | A non-success result aborts the remaining batch. |
| `ContinueBatch` | `2` | A non-success result lets the remaining batch continue. |

### `ConvaiActionTargetKind`

`Convai.Shared.Types`

| Value | Integer | Description |
| --- | --- | --- |
| `None` | `0` | No target resolved. |
| `Object` | `1` | Target is a registered object. |
| `Character` | `2` | Target is a registered character. |

### `ConvaiActionParameterType`

`Convai.Shared.Types`

| Value | Integer | Description |
| --- | --- | --- |
| `Auto` | `0` | Infer reference, number, bool, or string best-effort, in that order. Default. |
| `Reference` | `1` | Resolve an authored object or character target by name. |
| `String` | `2` | Keep the raw text. |
| `Number` | `3` | Parse an invariant-culture float. |
| `Bool` | `4` | Parse `true`/`yes`/`1` or `false`/`no`/`0`. |
| `Choice` | `5` | Require one of the authored choice strings. A mismatch flags the value through `IsConstraintMatch`. |

### `ConvaiActionExecutionStatus`

`Convai.Runtime.Actions`

| Value | Integer | Dispatcher event fired |
| --- | --- | --- |
| `Succeeded` | `0` | `OnStepSucceeded` |
| `Failed` | `1` | `OnStepFailed` |
| `Canceled` | `2` | `OnStepFailed` |
| `TimedOut` | `3` | `OnStepFailed` |
| `Unhandled` | `4` | `OnStepUnhandled` |

## `ConvaiActionInvocationUnityEvent`

`Convai.Runtime.Actions` — Serializable class extending `UnityEvent<ConvaiActionInvocation>`

Wrapper type that makes `ConvaiActionInvocation` serializable as a UnityEvent parameter. Assign handlers in the Inspector like any standard UnityEvent. The event's single argument is the `ConvaiActionInvocation` for that step.

`ConvaiActionStepReportUnityEvent` is the equivalent wrapper for `ConvaiActionDispatcher.OnStepCompleted`; it extends `UnityEvent<ConvaiActionStepReport>` and carries the full `ConvaiActionStepReport` instead.

## `ConvaiActionDebugProbe`

`MonoBehaviour` — `Convai.Runtime.Actions`

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
