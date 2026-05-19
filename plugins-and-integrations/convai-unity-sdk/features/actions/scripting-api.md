# Scripting API

## Controlling the Action Pipeline from Code

The Action system exposes a focused scripting surface that lets you subscribe to batch lifecycle events, manually enqueue command batches, inspect execution context at runtime, and integrate the pipeline with your own simulation logic. This page covers every public type, property, method, and event in the Action scripting API — verified directly against the SDK source.

{% hint style="info" %}
Most Inspector-based setups require no scripting at all. This page is for cases where you need runtime control, analytics, fallback logic, or programmatic configuration of the action pipeline.
{% endhint %}

## Accessing Action Components

All action components live on the same `GameObject` as `ConvaiCharacter`. Retrieve them in `Awake` using `GetComponent`, or use the convenience method on `ConvaiCharacter` for the config source.

{% code title="ActionSetup.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using Convai.Runtime.Actions;
using Convai.Runtime.Components;
using UnityEngine;

public class ActionSetup : MonoBehaviour
{
    private ConvaiCharacter _character;
    private ConvaiActionDispatcher _dispatcher;
    private ConvaiActionConfigSource _configSource;

    private void Awake()
    {
        _character = GetComponent<ConvaiCharacter>();
        _dispatcher = GetComponent<ConvaiActionDispatcher>();
        _configSource = _character.GetActionConfigSource();
    }
}
```
{% endcode %}

{% hint style="warning" %}
`GetActionConfigSource()` returns `null` if no `ConvaiActionConfigSource` is present on the character. Guard against null before calling any method on it.
{% endhint %}

## ConvaiCharacter — Action Received Event

`ConvaiCharacter` fires `OnActionsReceived` immediately when the Convai backend delivers an action batch — before the dispatcher processes it. Subscribe here for logging, analytics, or early inspection of commands.

| Member              | Type                                               | Description                                                     |
| ------------------- | -------------------------------------------------- | --------------------------------------------------------------- |
| `OnActionsReceived` | `event Action<IReadOnlyList<ConvaiActionCommand>>` | Fires once per batch, before the dispatcher queues the commands |

{% code title="ActionLogger.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Shared.Types;
using UnityEngine;

public class ActionLogger : MonoBehaviour
{
    private ConvaiCharacter _character;

    private void Awake()
    {
        _character = GetComponent<ConvaiCharacter>();
        _character.OnActionsReceived += HandleActionsReceived;
    }

    private void OnDestroy()
    {
        _character.OnActionsReceived -= HandleActionsReceived;
    }

    private void HandleActionsReceived(IReadOnlyList<ConvaiActionCommand> commands)
    {
        foreach (ConvaiActionCommand cmd in commands)
            Debug.Log($"Incoming action: {cmd.Name}, target: {cmd.Target ?? "none"}");
    }
}
```
{% endcode %}

{% hint style="info" %}
`OnActionsReceived` is the best point to read raw commands before resolution. To react to post-resolution step outcomes instead, subscribe to the dispatcher events described in the next section.
{% endhint %}

## ConvaiActionDispatcher

`ConvaiActionDispatcher` drives the full execution lifecycle: it receives commands, resolves targets, matches definitions, and calls executors in sequence.

### Properties

| Property        | Type                             | Description                                                                   |
| --------------- | -------------------------------- | ----------------------------------------------------------------------------- |
| `BatchPolicy`   | `ConvaiActionBatchPolicy`        | Controls how an incoming batch behaves when one is already running            |
| `FailurePolicy` | `ConvaiActionBatchFailurePolicy` | Controls whether a failed step aborts the remaining batch or lets it continue |

Both properties reflect the values set in the Inspector and are read-only at runtime. See [Dispatcher & Batch Policies](/broken/pages/0a4814770f30b55f9d3340eb6c34a12ffd90fd01) for full enum reference and behavior details.

### Methods

| Method                                                       | Returns | Description                                                                        |
| ------------------------------------------------------------ | ------- | ---------------------------------------------------------------------------------- |
| `EnqueueActions(IReadOnlyList<ConvaiActionCommand> actions)` | `void`  | Submits a command batch to the dispatcher as if it arrived from the Convai backend |

`EnqueueActions` respects the active `BatchPolicy`. Use it to trigger scripted sequences, automated demonstrations, or editor test flows.

{% code title="ManualActionTrigger.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using System.Collections.Generic;
using Convai.Runtime.Actions;
using Convai.Shared.Types;
using UnityEngine;

public class ManualActionTrigger : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;

    public void TriggerGreetingSequence()
    {
        var commands = new List<ConvaiActionCommand>
        {
            new ConvaiActionCommand("Wave", null),
            new ConvaiActionCommand("Move To", "Reception Desk")
        };
        _dispatcher.EnqueueActions(commands);
    }
}
```
{% endcode %}

### Dispatcher Events

The dispatcher exposes seven events covering every stage of batch and step execution. All events can be bound in the Inspector or subscribed to in code.

| Event              | Type                               | Fires when                                                    |
| ------------------ | ---------------------------------- | ------------------------------------------------------------- |
| `OnBatchStarted`   | `UnityEvent`                       | A new batch begins execution                                  |
| `OnStepStarted`    | `ConvaiActionInvocationUnityEvent` | An individual step begins executing                           |
| `OnStepSucceeded`  | `ConvaiActionInvocationUnityEvent` | A step's executor returned `Succeeded`                        |
| `OnStepFailed`     | `ConvaiActionInvocationUnityEvent` | A step's executor returned `Failed` or `TimedOut`             |
| `OnStepUnhandled`  | `ConvaiActionInvocationUnityEvent` | A step matched no definition or failed target validation      |
| `OnBatchCompleted` | `UnityEvent`                       | All steps in a batch finished (succeeded, failed, or skipped) |
| `OnBatchAborted`   | `UnityEvent`                       | The batch was cancelled mid-execution by policy or failure    |

`ConvaiActionInvocationUnityEvent` is a serializable `UnityEvent<ConvaiActionInvocation>`. Its callbacks receive a `ConvaiActionInvocation` with full context for that step — see [ConvaiActionInvocation](scripting-api.md#convaiactioninvocation) below.

{% hint style="warning" %}
Events bound in the Inspector and subscribed to in code both fire. Do not register the same handler twice or you will receive duplicate callbacks.
{% endhint %}

{% code title="BatchEventListener.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using Convai.Runtime.Actions;
using UnityEngine;

public class BatchEventListener : MonoBehaviour
{
    [SerializeField] private ConvaiActionDispatcher _dispatcher;

    private void OnEnable()
    {
        _dispatcher.OnBatchStarted.AddListener(HandleBatchStarted);
        _dispatcher.OnStepFailed.AddListener(HandleStepFailed);
        _dispatcher.OnBatchCompleted.AddListener(HandleBatchCompleted);
        _dispatcher.OnBatchAborted.AddListener(HandleBatchAborted);
    }

    private void OnDisable()
    {
        _dispatcher.OnBatchStarted.RemoveListener(HandleBatchStarted);
        _dispatcher.OnStepFailed.RemoveListener(HandleStepFailed);
        _dispatcher.OnBatchCompleted.RemoveListener(HandleBatchCompleted);
        _dispatcher.OnBatchAborted.RemoveListener(HandleBatchAborted);
    }

    private void HandleBatchStarted() => Debug.Log("Action batch started.");
    private void HandleBatchCompleted() => Debug.Log("Action batch completed.");
    private void HandleBatchAborted() => Debug.Log("Action batch aborted.");

    private void HandleStepFailed(ConvaiActionInvocation invocation)
    {
        Debug.LogWarning(
            $"Step failed: '{invocation.Command.Name}'" +
            $" → target: '{invocation.Command.Target ?? "none"}'");
    }
}
```
{% endcode %}

## ConvaiActionDefinition

`ConvaiActionDefinition` describes a single registerable action — its name, target requirement, executor, and timeout. You author these in the **Definitions** list of `ConvaiActionConfigSource`. At runtime, `ConvaiActionInvocation.Definition` carries the matched definition for the executing step.

| Field               | Type                            | Default | Description                                                                         |
| ------------------- | ------------------------------- | ------- | ----------------------------------------------------------------------------------- |
| `ActionName`        | `string`                        | `""`    | The action name the dispatcher matches against incoming commands (case-insensitive) |
| `TargetRequirement` | `ConvaiActionTargetRequirement` | `None`  | What kind of target, if any, must be resolved before the step can execute           |
| `Executor`          | `MonoBehaviour`                 | `null`  | The component that implements `IConvaiActionExecutor` and runs this action          |
| `TimeoutSeconds`    | `float`                         | `0`     | Maximum seconds allowed for `ExecuteAsync` to complete; `0` means no timeout        |

### ConvaiActionTargetRequirement Enum

The dispatcher validates the resolved target against `TargetRequirement` before calling `ExecuteAsync`. If validation fails, the step fires `OnStepUnhandled` and is skipped.

| Value       | Requirement                                                                   |
| ----------- | ----------------------------------------------------------------------------- |
| `None`      | No target required; the step runs regardless of whether a target was resolved |
| `Object`    | Target must resolve to a registered `ConvaiActionObjectDefinition`            |
| `Character` | Target must resolve to a registered `ConvaiActionCharacterDefinition`         |
| `Either`    | Target must resolve to either an object or a character                        |

{% hint style="info" %}
Set `TargetRequirement` to `None` for actions that operate on the character itself — animations, audio cues, state changes — rather than on an external scene object.
{% endhint %}

## ConvaiActionInvocation

`ConvaiActionInvocation` is passed to every step-level dispatcher event and to `IConvaiActionExecutor.ExecuteAsync`. It carries the full context of a single execution step.

| Property         | Type                         | Description                                            |
| ---------------- | ---------------------------- | ------------------------------------------------------ |
| `Command`        | `ConvaiActionCommand`        | The raw command as received from the Convai backend    |
| `Definition`     | `ConvaiActionDefinition`     | The matched definition from `ConvaiActionConfigSource` |
| `ResolvedTarget` | `ConvaiResolvedActionTarget` | The scene binding for the command's target string      |
| `Character`      | `ConvaiCharacter`            | The character that owns this action pipeline           |
| `BatchIndex`     | `int`                        | Zero-based index of the batch this step belongs to     |
| `StepIndex`      | `int`                        | Zero-based index of this step within its batch         |

{% code title="InvocationReader.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using Convai.Runtime.Actions;
using UnityEngine;

public class InvocationReader : MonoBehaviour
{
    public void LogStep(ConvaiActionInvocation invocation)
    {
        string targetName = invocation.ResolvedTarget?.Name ?? "unresolved";
        Debug.Log(
            $"[Batch {invocation.BatchIndex}, Step {invocation.StepIndex}] " +
            $"{invocation.Command.Name} → {targetName}");

        if (invocation.ResolvedTarget?.GameObjectReference != null)
            Debug.Log($"Target GameObject: {invocation.ResolvedTarget.GameObjectReference.name}");
    }
}
```
{% endcode %}

## ConvaiActionCommand

`ConvaiActionCommand` represents a single instruction as delivered by the Convai backend.

| Property    | Type     | Description                                           |
| ----------- | -------- | ----------------------------------------------------- |
| `Name`      | `string` | The action name (e.g., `"Move To"`, `"Pick Up"`)      |
| `Target`    | `string` | The target name, or `null` if no target was specified |
| `HasTarget` | `bool`   | `true` when `Target` is non-null and non-empty        |

{% hint style="info" %}
Action name matching is case-insensitive and normalised during resolution. `"move to"`, `"Move To"`, and `"MOVE TO"` all match a definition named `"Move To"`.
{% endhint %}

## ConvaiResolvedActionTarget

`ConvaiResolvedActionTarget` describes what the command's `Target` string resolved to in the scene.

| Property              | Type                              | Description                                                                |
| --------------------- | --------------------------------- | -------------------------------------------------------------------------- |
| `Kind`                | `ConvaiActionTargetKind`          | Whether the target resolved to an object, a character, or nothing          |
| `Name`                | `string`                          | The resolved name as registered in `ConvaiActionConfigSource`              |
| `ObjectBinding`       | `ConvaiActionObjectDefinition`    | Populated when `Kind == Object`; `null` otherwise                          |
| `CharacterBinding`    | `ConvaiActionCharacterDefinition` | Populated when `Kind == Character`; `null` otherwise                       |
| `GameObjectReference` | `GameObject`                      | The scene `GameObject` for the resolved target; `null` when `Kind == None` |

### ConvaiActionTargetKind Enum

| Value       | Meaning                                                                                |
| ----------- | -------------------------------------------------------------------------------------- |
| `None`      | No target was specified, or the target string could not be matched to any registration |
| `Object`    | Target resolved to a registered `ConvaiActionObjectDefinition`                         |
| `Character` | Target resolved to a registered `ConvaiActionCharacterDefinition`                      |

## ConvaiActionExecutionResult

Executor implementations return a `ConvaiActionExecutionResult` to communicate the outcome of a step to the dispatcher.

### Static Factory Methods

| Method                                                               | Status set  | When to use                                             |
| -------------------------------------------------------------------- | ----------- | ------------------------------------------------------- |
| `ConvaiActionExecutionResult.Succeeded()`                            | `Succeeded` | The behavior completed successfully                     |
| `ConvaiActionExecutionResult.Failed(string? message, Exception? ex)` | `Failed`    | The behavior could not complete due to an error         |
| `ConvaiActionExecutionResult.Canceled()`                             | `Canceled`  | The step was cancelled via the `CancellationToken`      |
| `ConvaiActionExecutionResult.TimedOut()`                             | `TimedOut`  | The step exceeded its configured `TimeoutSeconds`       |
| `ConvaiActionExecutionResult.Unhandled(string? message)`             | `Unhandled` | This executor does not handle the requested action name |

### ConvaiActionExecutionStatus Enum

| Value       | Dispatcher behaviour                                                     |
| ----------- | ------------------------------------------------------------------------ |
| `Succeeded` | `OnStepSucceeded` fires; batch continues to the next step                |
| `Failed`    | `OnStepFailed` fires; batch continues or aborts based on `FailurePolicy` |
| `Canceled`  | Batch abort is already in progress; no additional event is fired         |
| `TimedOut`  | Treated as `Failed`; `OnStepFailed` fires                                |
| `Unhandled` | `OnStepUnhandled` fires; batch continues regardless of `FailurePolicy`   |

## IConvaiActionExecutor Interface

Any `MonoBehaviour` that implements `IConvaiActionExecutor` can be assigned as an executor in `ConvaiActionConfigSource`.

{% code title="IConvaiActionExecutor.cs" overflow="wrap" lineNumbers="true" %}
```csharp
namespace Convai.Runtime.Actions
{
    public interface IConvaiActionExecutor
    {
        Task<ConvaiActionExecutionResult> ExecuteAsync(
            ConvaiActionInvocation invocation,
            CancellationToken cancellationToken);
    }
}
```
{% endcode %}

The dispatcher calls `ExecuteAsync` for each step and awaits its result before moving to the next. Always forward the `CancellationToken` to any async operations inside your implementation — it is triggered when the batch is aborted mid-execution.

For a complete guide to building and registering custom executors, see [Writing Custom Executors](/broken/pages/f94d8c5f578a6160c49293ff08ded994bc8d4d9f).

## ConvaiActionConfigSource — Runtime Methods

`ConvaiActionConfigSource` lets you read and snapshot the action configuration from code.

### Methods

| Method                                                                   | Returns                                 | Description                                                                                                                     |
| ------------------------------------------------------------------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `BuildActionConfig()`                                                    | `ConvaiActionConfig`                    | Returns a snapshot of the current config — action list, object definitions, character definitions, and current attention object |
| `TryResolveObject(string name, out ConvaiActionObjectDefinition result)` | `bool`                                  | Looks up a registered object definition by name; returns `false` if not found                                                   |
| `GetEffectiveDefinitions(IReadOnlyList<string>? allowed)`                | `IReadOnlyList<ConvaiActionDefinition>` | Returns action definitions filtered by an allowlist; pass `null` to return all definitions                                      |

### Properties

| Property                 | Type                                             | Description                                                                 |
| ------------------------ | ------------------------------------------------ | --------------------------------------------------------------------------- |
| `Definitions`            | `IReadOnlyList<ConvaiActionDefinition>`          | All registered action definitions                                           |
| `Objects`                | `IReadOnlyList<ConvaiActionObjectDefinition>`    | All registered object definitions                                           |
| `Characters`             | `IReadOnlyList<ConvaiActionCharacterDefinition>` | All registered character definitions                                        |
| `InitialAttentionObject` | `string`                                         | The name of the object set as the default attention target at session start |

{% code title="ObjectResolver.cs" overflow="wrap" lineNumbers="true" %}
```csharp
using Convai.Runtime.Components;
using Convai.Shared.Actions;
using UnityEngine;

public class ObjectResolver : MonoBehaviour
{
    [SerializeField] private ConvaiActionConfigSource _configSource;

    public GameObject FindSceneObject(string objectName)
    {
        if (_configSource.TryResolveObject(objectName, out ConvaiActionObjectDefinition def))
            return def.GameObjectReference;

        Debug.LogWarning($"No registered object named '{objectName}'.");
        return null;
    }
}
```
{% endcode %}

## Conclusion

The Action scripting API covers every integration point in the pipeline — from raw command receipt on `ConvaiCharacter` through batch lifecycle events, step invocation context, and executor result types. For complete end-to-end examples that combine Inspector configuration with these API calls, see [Usage Examples](/broken/pages/f695f415531b196f9b0124dee13a4a4654e81ad3). For diagnosing unexpected behaviour at runtime, see [Debugging & Troubleshooting](/broken/pages/adf3ce4e083972598bbda6b52f88d723dbb3719a).
