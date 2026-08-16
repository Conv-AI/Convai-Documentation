---
title: Character actions scripting reference
description: API reference for the Convai character actions system — executor base classes, dispatcher, config types, invocation objects, and enums.
last_reviewed: "4.5.0"
---

Complete API reference for the public types in the Convai character actions system. Types are in the `Convai.Runtime.Actions`, `Convai.Runtime.Components`, `Convai.Shared.Actions`, or `Convai.Shared.Types` namespaces unless noted.

## `IConvaiActionExecutor`

`Convai.Runtime.Actions` — Interface

The extension point for all action behavior. Implement on any `MonoBehaviour`, or derive from `ConvaiActionExecutorBase` instead — see [Write a custom action executor](writing-custom-executors.md).

```csharp
public interface IConvaiActionExecutor
{
    Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken);
}
```

Return `ConvaiActionExecutionResult.Unhandled` when the component cannot service the invocation (for example, a missing rig or peer) so the dispatcher can report it distinctly. Honor `cancellationToken` for batch replacement and timeouts.

## Executor base classes

`Convai.Runtime.Actions` — Abstract `MonoBehaviour` classes

Every shipped executor derives from one of these rather than implementing `IConvaiActionExecutor` directly. Deriving gives a component the Convai inspector automatically — sectioned fields, tooltips, and an action-binding status block — with no editor code.

| Class | Derives from | Adds |
| --- | --- | --- |
| `ConvaiActionExecutorBase` | `MonoBehaviour`, `IConvaiActionExecutor` | `CharacterTransform`, `ResolvePlayer()`, `DeclaredButNotSent(...)` |
| `ConvaiTargetedActionExecutor` | `ConvaiActionExecutorBase` | Target validation, peer resolution/caching, missing-peer diagnostics, parameter override helpers |
| `ConvaiCharacterActionExecutor<TPeer>` | `ConvaiTargetedActionExecutor` | Resolves one specific character-side component (`TPeer`) and hands it to `ExecuteCoreAsync` |
| `ConvaiActionExecutor<TParameters>` | `ConvaiActionExecutorBase` | Binds invocation parameters onto a typed `TParameters` object by name before execution |

### `ConvaiActionExecutorBase`

```csharp
public abstract class ConvaiActionExecutorBase : MonoBehaviour, IConvaiActionExecutor
{
    public abstract Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken);
}
```

| Member | Type | Description |
| --- | --- | --- |
| `CharacterTransform` | `Transform` (protected) | The Convai Character's transform, resolved on first use by searching upward and cached. Falls back to this component's own transform (uncached) when no character is found above it |
| `ResolvePlayer()` | `protected virtual Transform` | Where the player actually is; see `ConvaiPlayerBody` below. Override for split screen, multiple rigs, or a cutscene camera |
| `DeclaredButNotSent(invocation, parameterName)` | `protected static bool` | Whether the action declares `parameterName` and the Convai Character sent no value for it — distinguishes "nothing was said about this" from a value that happens to be empty |

### `ConvaiTargetedActionExecutor`

```csharp
public abstract class ConvaiTargetedActionExecutor : ConvaiActionExecutorBase
{
    protected virtual bool RequiresTarget => true;

    protected abstract Task<ConvaiActionExecutionResult> ExecuteCoreAsync(
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken);
}
```

`ExecuteAsync` is sealed: when `RequiresTarget` is `true` (the default) and the invocation has no resolved target `GameObject`, it returns `MissingTargetResult(invocation)` — `Unhandled` by default — without calling `ExecuteCoreAsync`. Set `RequiresTarget => false` for target-less actions (a scripted head gesture, for example).

| Member | Type | Description |
| --- | --- | --- |
| `MissingTargetResult(invocation)` | `protected virtual ConvaiActionExecutionResult` | Result returned when a required target is missing. Override to return `Failed(..., ConvaiActionFailureReason.TargetMissing)` instead of the default `Unhandled` |
| `ResolveTargetGameObject(invocation)` | `protected static GameObject` | The resolved target `GameObject`, or `null` |
| `ResolveTargetInteractionPoint(invocation)` | `protected static Transform` | The resolved target's `InteractionPoint`, falling back to its `GameObjectReference`'s transform |
| `TryResolvePeer<T>(ref T authored, out T peer)` | `protected bool` | Resolves a required peer: an explicit `authored` field always wins; otherwise looks up `GetComponentInParent<T>()` then `GetComponentInChildren<T>()` and remembers the result for the component's lifetime |
| `UnhandledMissingPeer<T>()` | `protected ConvaiActionExecutionResult` | Builds an `Unhandled` result for a missing peer of type `T`, logging it once per component instance |
| `GetOverride(invocation, name, defaultValue)` | `protected static float`/`bool`/`string` | Reads an invocation parameter override, falling back to the Inspector-authored default when absent or `invocation` is `null` |

### `ConvaiCharacterActionExecutor<TPeer>`

```csharp
public abstract class ConvaiCharacterActionExecutor<TPeer> : ConvaiTargetedActionExecutor
    where TPeer : Component
{
    protected abstract Task<ConvaiActionExecutionResult> ExecuteCoreAsync(
        TPeer characterComponent,
        ConvaiActionInvocation invocation,
        CancellationToken cancellationToken);
}
```

Resolves `TPeer` once through `TryResolvePeer` and hands it directly to `ExecuteCoreAsync`; a missing component returns `Unhandled` via `UnhandledMissingPeer<TPeer>()` before your method runs. This is the shared base behind executors that need exactly one character-side controller — for example `ConvaiScanEnvironmentActionExecutor` (needs a `ConvaiGazeController`) and `ConvaiLeadPlayerActionExecutor` (needs a `ConvaiNavMeshLocomotion`).

### `ConvaiActionExecutor<TParameters>`

```csharp
public abstract class ConvaiActionExecutor<TParameters> : ConvaiActionExecutorBase
    where TParameters : new()
{
    protected abstract Task<ConvaiActionExecutionResult> ExecuteAsync(
        ConvaiActionInvocation invocation,
        TParameters parameters,
        CancellationToken cancellationToken);

    protected virtual TParameters BindParameters(ConvaiActionInvocation invocation);
}
```

Binds public fields and properties of `TParameters` by parameter name (supported member types: `string`, `float`, `double`, `int`, `bool`, `ConvaiResolvedActionTarget`, `ConvaiActionParameterValue`). Use `[ConvaiActionParameter("name")]` when the DTO member name differs from the authored parameter name.

## `ConvaiPlayerBody`

`Convai.Runtime.Actions` — `public static class`

Where the player actually is, for scene code that is not an executor. `ConvaiActionExecutorBase.ResolvePlayer()` (protected virtual, `ConvaiActionExecutorBase.cs:113`) is the executor-side shorthand for this.

| Method | Signature | Description |
| --- | --- | --- |
| `Resolve` | `static Transform Resolve()` | The transform to measure the player by: prefers a scene `ConvaiPlayer`, resolving to the transform its rig actually moves (a `CharacterController` or `Rigidbody` inside it, not the prefab root); falls back to `Camera.main`; `null` if neither exists |
| `TryResolveFloorPosition` | `static bool TryResolveFloorPosition(float floorHeight, out Vector3 position)` | Where the player is standing, flattened onto `floorHeight`. Returns `false` when there is nobody to measure to |

## `ConvaiActionExecutionResult`

`Convai.Runtime.Actions` — Readonly struct

Return type for `IConvaiActionExecutor.ExecuteAsync`.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Status` | `ConvaiActionExecutionStatus` | The outcome of this execution step |
| `Message` | `string` | Optional diagnostic detail. Reaches the Console, the Actions Editor, and your own game code — never the Convai Character |
| `Answer` | `string` | What this action found out, written as one plain sentence the character could say aloud. Empty for actions that perform a visible act rather than answer a question |
| `HasAnswer` | `bool` | Whether this result carries a non-empty `Answer` |
| `Exception` | `Exception` | The exception captured when the executor threw |
| `FailureReason` | `ConvaiActionFailureReason` | Machine-readable failure reason; `None` for non-failures |

### Factory methods

| Method | Signature | Use when |
| --- | --- | --- |
| `Succeeded` | `static ConvaiActionExecutionResult Succeeded(string message = null)` | The behavior completed successfully and has nothing the player needs to hear |
| `Answered` | `static ConvaiActionExecutionResult Answered(string answer, string message = null)` | The behavior found something out that the player asked for — reading a gauge, counting a group, measuring a distance. `message` defaults to `answer` |
| `Failed` | `static ConvaiActionExecutionResult Failed(string message = null, Exception exception = null)` | An unclassified error occurred. Maps to `ConvaiActionFailureReason.Custom` when `message` is non-empty, otherwise `None` |
| `Failed` | `static ConvaiActionExecutionResult Failed(string message, ConvaiActionFailureReason reason, Exception exception = null)` | An error occurred with a known, structured cause. Preferred over the unclassified overload in new code |
| `Canceled` | `static ConvaiActionExecutionResult Canceled()` | The `CancellationToken` was signaled for a reason other than timeout. `FailureReason` is `Interrupted` |
| `TimedOut` | `static ConvaiActionExecutionResult TimedOut(string message = null)` | **Do not call manually.** The dispatcher returns this automatically when `TimeoutSeconds` expires. `FailureReason` is `Timeout` |
| `Unhandled` | `static ConvaiActionExecutionResult Unhandled(string message = null)` | This executor intentionally declines the invocation. `FailureReason` is `None` |

`Answered(...)` is what distinguishes a query action from every other kind: it is the only factory that populates `Answer`, and `Answer` is the only part of a result the Convai Character is ever told about. Whether it is spoken, silently remembered, or left to the character's judgement is decided separately by the action's `ConvaiActionAnswerDelivery` setting, not by the executor. See [Answer a question instead of acting](writing-custom-executors.md#answer-a-question-instead-of-acting) for the full pattern.

## `ConvaiActionFailureReason`

`Convai.Runtime.Actions`

Machine-readable reason a step failed, alongside the free-text `Message`.

| Value | Description |
| --- | --- |
| `None` | No failure, or the reason was not classified (default for `Succeeded`/`Unhandled`) |
| `TargetMissing` | The invocation required a resolved target and none was present |
| `TargetUnreachable` | A target was resolved but could not be reached |
| `PathBlocked` | A path to the target exists conceptually but is blocked (no valid NavMesh path, for example) |
| `PeerMissing` | A required peer component (controller, locomotion, rig) was not found on the character |
| `InvalidState` | The executor or a dependency was in a state that could not service the request |
| `Timeout` | The step exceeded its definition timeout |
| `Interrupted` | The step was interrupted before completion (canceled, replaced, or superseded) |
| `Custom` | Any other executor-specific failure conveyed only through `Message` |
| `TargetNotActionable` | A target was resolved but lacks the component this action needs to act on it (see `RequiredTargetComponent` on `ConvaiActionArchetypeAttribute`) |
| `Busy` | The character cannot take the request right now because it is performing something that uses the same part of it; the same request a moment later would normally succeed |

## `ConvaiActionDefinition`

`Convai.Runtime.Actions` — Serializable sealed class

Authoring definition that binds a backend action name to a local executor, its typed parameters, and its dispatch behavior. Only the rendered wire template (from `ToActionConfigString`) is sent to Convai.

### Fields and properties

| Member | Type | Description |
| --- | --- | --- |
| `ActionName` | `string` | The action name matched against backend commands (case-insensitive) |
| `Description` | `string` | Optional description sent to Convai for grounding |
| `Parameters` | `List<ConvaiActionParameterDefinition>` | Ordered typed parameters rendered into the wire template |
| `TargetRequirement` | `ConvaiActionTargetRequirement` | What kind of target this action requires |
| `Executor` | `MonoBehaviour` | The component that performs the behavior. Must implement `IConvaiActionExecutor`. An explicit reference here always wins over `ExecutorTypeHint` |
| `ExecutorTypeHint` | `string` | Optional short or full type name of an `IConvaiActionExecutor` to auto-bind on the character's hierarchy when `Executor` is `null` — used by definitions authored inside a `ConvaiActionSet` asset, which cannot hold a scene reference |
| `TimeoutSeconds` | `float` | Maximum execution time in seconds. `0` or less disables the timeout |
| `FailurePolicyOverride` | `ConvaiActionFailurePolicyOverride` | Per-action override of the dispatcher's batch failure policy |
| `AnswerDelivery` | `ConvaiActionAnswerDelivery` | What the character does with an `Answered(...)` result. Authoring-only — never sent to Convai |
| `WaitForBotSpeech` | `bool` | Whether the first step of a fresh batch waits for character speech |
| `DelayAfterBotSpeechSeconds` | `float` | Optional delay after the speech gate releases |
| `Category` | `string` (property) | Optional authoring label the action is filed under in the Actions Editor. Organization only — not sent to Convai |
| `Enabled` | `bool` (property) | Authored availability. A disabled action is excluded from the `action_config` sent to Convai. Defaults to `true` |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `ToActionConfigString` | `string ToActionConfigString()` | Renders the wire template string sent to Convai for this definition |

## `ConvaiActionAnswerDelivery`

`Convai.Runtime.Actions`

What a Convai Character does with the `Answer` an action returned. Authored per action in the Actions Editor as **When It Finishes**.

| Value | Integer | Description |
| --- | --- | --- |
| `UseCharacterSetting` | `0` | Defers to the character's `ConvaiActionFeedbackRelay`. Default |
| `RememberOnly` | `1` | The character keeps the answer without saying it out loud. It still reaches the character's memory |
| `MentionIfRelevant` | `2` | The character decides for itself whether the answer is worth bringing up |
| `TellThePlayer` | `3` | The character says what the action found. Use for actions that answer a direct question |

## `ConvaiActionParameterDefinition`

`Convai.Runtime.Actions` — Serializable sealed class

Authoring definition for a single typed action parameter, referenced by `ConvaiActionDefinition.Parameters`.

| Field | Type | Description |
| --- | --- | --- |
| `Name` | `string` | Parameter name used as the wire key and template anchor |
| `Description` | `string` | Optional description sent to Convai for grounding |
| `Type` | `ConvaiActionParameterType` | Declared parameter type. `Auto` infers from the value. Default `Auto` |
| `Connector` | `string` | Optional connector word rendered before the parameter in the wire template (for example `"on"` or `"in"`) |
| `Choices` | `List<string>` | Allowed values when `Type` is `Choice` |

## `ConvaiActionInvocation`

`Convai.Runtime.Actions` — Sealed class

Typed execution context passed to executors and all dispatcher events.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Command` | `ConvaiActionCommand` | The raw backend command for this step |
| `Definition` | `ConvaiActionDefinition` | The matched local action definition. `null` if no definition was found (step will fail) |
| `ResolvedTarget` | `ConvaiResolvedActionTarget` | The resolved target binding. `null` if the action has no target or resolution failed |
| `Character` | `ConvaiCharacter` | The NPC executing this action |
| `BatchIndex` | `int` | Sequential index of the containing batch across the dispatcher's lifetime |
| `StepIndex` | `int` | 0-based index of this step within the current batch |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `TryGetParameter` | `bool TryGetParameter(string name, out ConvaiActionParameterValue value)` | Attempts to read a typed parameter by name (case-insensitive) |
| `GetString` | `string GetString(string name, string fallback = "")` | Reads a string parameter, returning `fallback` when absent |
| `GetNumber` | `float GetNumber(string name, float fallback = 0f)` | Reads a numeric parameter, returning `fallback` when absent |
| `GetBool` | `bool GetBool(string name, bool fallback = false)` | Reads a boolean parameter, returning `fallback` when absent |
| `GetReference` | `ConvaiResolvedActionTarget GetReference(string name)` | Resolves a reference parameter against the character's action config, falling back to the definition's target requirement when the parameter carries no explicit kind |

## `ConvaiResolvedActionTarget`

`Convai.Runtime.Actions` — Serializable sealed class

Resolved target for one action step, produced by the resolution ladder described in [How action target resolution works](attention-and-reference-grounding.md).

| Property | Type | Description |
| --- | --- | --- |
| `Kind` | `ConvaiActionTargetKind` | Whether the resolved target is an Object, Character, or None |
| `Name` | `string` | The resolved name (from the backend command) |
| `ObjectBinding` | `ConvaiActionObjectDefinition` | The matched object definition. `null` if `Kind != Object` |
| `CharacterBinding` | `ConvaiActionCharacterDefinition` | The matched character definition. `null` if `Kind != Character` |
| `GameObjectReference` | `GameObject` | The scene `GameObject` from the matching binding |
| `InteractionPoint` | `Transform` | The binding's explicit interaction point when set, otherwise `GameObjectReference`'s transform, otherwise `null`. Every shipped targeted executor moves to or aims at this rather than the raw `GameObjectReference` transform |

## `ConvaiActionCommand`

`Convai.Shared.Types` — Serializable sealed class

Structured action command for one step, as returned by the backend.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Name` | `string` | Required. Action name selected by the backend (e.g., `"Move To"`) |
| `Target` | `string` | Optional. Object or character name the backend resolved as the target. `null` if no target |
| `ActionString` | `string` | Raw action string reconstructed from the backend `Name` and `Target` |
| `Parameters` | `Dictionary<string, ConvaiActionParameterValue>` | Typed parameters parsed from the backend response and the active Unity template. Keyed case-insensitively |
| `WaitForBotSpeech` | `bool` | Whether the first action in a fresh batch should wait for character speech before running |
| `DelayAfterBotSpeechSeconds` | `float` | Optional delay applied after the speech gate releases |
| `Enriched` | `bool` | `true` once the command has been enriched against the active action templates. The dispatcher enriches unmarked commands exactly once before dispatch |
| `HasTarget` | `bool` | `true` when `Target` is non-empty |

### Constructor

```csharp
new ConvaiActionCommand("Move To", "Crate")  // name + target
new ConvaiActionCommand("Wave")              // name only
```

The constructor normalizes `Name` and `Target` and derives `ActionString` from them. `Parameters`, `WaitForBotSpeech`, `DelayAfterBotSpeechSeconds`, and `Enriched` default to their empty values and are populated by the backend response or by enrichment.

## `ConvaiActionParameterValue`

`Convai.Shared.Types` — Serializable sealed class

One typed action parameter after enrichment. Every representation is populated best-effort from the raw text; `Type` says which one the authored template intends.

| Property | Type | Description |
| --- | --- | --- |
| `Type` | `ConvaiActionParameterType` | Effective type after coercion. An authored `Auto` resolves to a concrete type |
| `RawValue` | `string` | Trimmed raw text this value was parsed from |
| `StringValue` | `string` | The value as text (same as `RawValue` after trimming) |
| `NumberValue` | `float` | Parsed float, or `0` when the text is not numeric |
| `BoolValue` | `bool` | Parsed bool, or `false` when the text is not a recognized boolean |
| `ResolvedReference` | `ConvaiActionParameterReference` | Matched authored target when the text named one; `null` otherwise |
| `IsConstraintMatch` | `bool` | `false` only when a `Choice` parameter's text is not one of its authored choices |
| `Presence` | `ConvaiActionParameterPresence` | Whether the Convai Character supplied a value for this parameter at all |

Read parameters through `ConvaiActionInvocation.TryGetParameter`, `GetString`, `GetNumber`, `GetBool`, or `GetReference` rather than indexing `ConvaiActionCommand.Parameters` directly.

## `ConvaiActionParameterPresence`

`Convai.Shared.Types`

Whether a parameter's value came from the Convai Character at all. An action that declares three parameters always comes back with three, because unfilled slots are padded to keep values lined up with the authored order — `Presence` is how an executor tells a padded slot from an answered one.

| Value | Integer | Description |
| --- | --- | --- |
| `Provided` | `0` | A value was supplied for this slot. The default |
| `Missing` | `1` | No value reached this slot; the parameter exists only because the action declares it |

Check this before acting on an empty value: `Missing` means nothing was said about the parameter, and the executor should decide for itself — refuse, ask, or apply its own default — rather than read the emptiness as an instruction. `Missing` is also logged once through the `Actions` log category.

## `ConvaiActionParameterReference`

`Convai.Shared.Types` — Serializable sealed class

Name-and-kind handle a `Reference` parameter resolved to during enrichment.

| Property | Type | Description |
| --- | --- | --- |
| `Name` | `string` | Authored target name the raw value matched (trimmed, never `null`) |
| `Kind` | `ConvaiActionTargetKind` | Whether the name matched an authored object or character |

`ConvaiActionParameterReference` is a lookup key, not a scene binding — it does not carry a `GameObjectReference`. Resolve it to a live `GameObject` through `ConvaiActionInvocation.GetReference(name)`, which returns a `ConvaiResolvedActionTarget`.

## `ConvaiActionConfig`

`Convai.Shared.Actions` — Serializable sealed class

Connect-time action affordances serialized into the session connect payload.

| Property | Type | Description |
| --- | --- | --- |
| `Actions` | `List<string>` | Action names allowed for this session. Only names are sent — executor bindings stay local |
| `Objects` | `List<ConvaiActionObjectDefinition>` | Objects the backend may reference as targets. `GameObjectReference` is never serialized |
| `Characters` | `List<ConvaiActionCharacterDefinition>` | Characters the backend may reference as targets. `GameObjectReference` is never serialized |
| `CurrentAttentionObject` | `string` | Initial attention object name. Must match an entry in `Objects` |

## `ConvaiActionConfigPatch`

`Convai.Shared.Actions` — Serializable sealed class

Runtime patch for the active session's action affordances, sent through `character.DynamicContext.Apply(...)`.

| Property | Type | Description |
| --- | --- | --- |
| `Actions` | `List<string>` | Replacement action list |
| `Characters` | `List<ConvaiActionCharacterDefinition>` | Replacement character-target list |
| `Objects` | `List<ConvaiActionObjectDefinition>` | Replacement object-target list |
| `CurrentAttentionObject` | `string` | Attention update resolved after list replacement |

{% hint style="warning" %}
Each field follows omitted-versus-empty semantics: a `null` list or string preserves the current value, and an empty list or string explicitly clears that value. Set a field only when you intend to change it.
{% endhint %}

## `ConvaiActionObjectDefinition`

`Convai.Shared.Actions` — Serializable sealed class

| Property | Type | Serialized | Description |
| --- | --- | --- | --- |
| `Name` | `string` | Yes (`"name"`) | Identifier used in action commands. Case-insensitive matching |
| `Description` | `string` | Yes (`"description"`) | Natural language description sent to Convai for reference resolution |
| `GameObjectReference` | `GameObject` | **No** (`[JsonIgnore]`) | Local scene reference. Never sent to Convai |
| `TextOnly` | `bool` | **No** (`[JsonIgnore]`) | Declares that this entry deliberately has no `GameObjectReference`. Without it, a missing reference is reported as a setup error |
| `Aliases` | `List<string>` | **No** (`[JsonIgnore]`) | Alternate names the resolution ladder matches exactly (step 2) before falling through to normalized/contains matching |
| `InteractionPoint` | `Transform` | **No** (`[JsonIgnore]`) | Explicit point to move to or aim at. Falls back to `GameObjectReference`'s transform when `null` |
| `Available` | `bool` | **No** (`[JsonIgnore]`) | Local resolution toggle, `true` by default. Unavailable entries are skipped by the resolution ladder |

## `ConvaiActionCharacterDefinition`

`Convai.Shared.Actions` — Serializable sealed class

| Property | Type | Serialized | Description |
| --- | --- | --- | --- |
| `Name` | `string` | Yes (`"name"`) | Identifier for this character target |
| `Bio` | `string` | Yes (`"bio"`) | Short description sent to Convai (e.g., "Site safety supervisor") |
| `GameObjectReference` | `GameObject` | **No** (`[JsonIgnore]`) | Local scene reference. Never sent to Convai |
| `TextOnly` | `bool` | **No** (`[JsonIgnore]`) | Same local-only meaning as on `ConvaiActionObjectDefinition` |
| `Aliases` | `List<string>` | **No** (`[JsonIgnore]`) | Same local-only meaning as on `ConvaiActionObjectDefinition` |
| `InteractionPoint` | `Transform` | **No** (`[JsonIgnore]`) | Same local-only meaning as on `ConvaiActionObjectDefinition` |
| `Available` | `bool` | **No** (`[JsonIgnore]`) | Same local-only meaning as on `ConvaiActionObjectDefinition` |

## `ConvaiActionTarget`

`Convai.Runtime.Actions` — `MonoBehaviour`

Menu path: `Add Component → Convai → Actions → Convai Action Target`

Marks any `GameObject` as a runtime action grounding target with no code required. While enabled, it is visible to selected characters' merged action config and participates in the resolution ladder exactly like an authored object or character, except that an authored entry of the same name always wins.

| Property | Type | Description |
| --- | --- | --- |
| `TargetName` | `string` | Target name the resolution ladder matches. Defaults to this `GameObject`'s name when blank |
| `Kind` | `ConvaiActionTargetKind` | Whether this is an actionable object or character |
| `Description` | `string` | Sent to Convai for grounding (Object kind) |
| `Bio` | `string` | Sent to Convai for grounding (Character kind) |
| `Aliases` | `List<string>` | Alternate names the resolution ladder matches exactly (step 2) |
| `InteractionPoint` | `Transform` | Optional explicit point to move to or aim at |
| `ApplyTo` | `ConvaiActionTargetApplyScope` | Which characters register this target while enabled: `AllCharacters` or `SpecificCharacters` |
| `SpecificCharacters` | `List<ConvaiCharacter>` | Characters to register onto when `ApplyTo` is `SpecificCharacters` |
| `RegisterOnEnable` | `bool` | Whether the target registers on enable and unregisters on disable. Default `true` |

## Built-in executor types

The shipped executor catalog changed in this release. Full field-level reference for every executor lives on [Action executors](action-executors.md); this section records only what changed.

**Added:**

| Executor | Menu path | Notes |
| --- | --- | --- |
| `ConvaiLeadPlayerActionExecutor` | `Convai/Actions/Lead Player To Target` | Body Animation pack; requires a `ConvaiNavMeshLocomotion` peer |
| `ConvaiScanEnvironmentActionExecutor` | `Convai/Actions/Scan Environment` | Gaze pack; requires a `ConvaiGazeController` peer |
| `ConvaiCountTargetGroupActionExecutor` | `Convai/Actions/Count Target Group` | Observation pack; requires a `ConvaiActionTargetGroup` on the resolved target; returns `Answered(...)` |
| `ConvaiMeasureDistanceActionExecutor` | `Convai/Actions/Measure Distance` | Observation pack; no required peer; returns `Answered(...)` |

The Observation pack is genuinely new: it is the first pair of built-in executors whose job is to answer a question rather than perform a visible act, using `ConvaiActionExecutionResult.Answered(...)` instead of `Succeeded(...)`.

**Removed:** `ConvaiGuidedTourActionExecutor`, `ConvaiAddressGroupActionExecutor`, `ConvaiPerformAtTargetActionExecutor` are no longer present in the SDK. A scene referencing one of these components has a broken reference after upgrading; rebind the action to a built-in or custom replacement. See [Migrate actions to v4.5.0](migrate-to-v4-5.md) for the upgrade path.

## `ConvaiActionDispatcher`

`MonoBehaviour` — `Convai.Runtime.Actions`

Menu path: `Add Component → Convai → Convai Action Runner`

Constraints: `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)`

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `BatchPolicy` | `ConvaiActionBatchPolicy` | Current batch policy (read-only from code; set in Inspector) |
| `FailurePolicy` | `ConvaiActionBatchFailurePolicy` | Current failure policy (read-only from code; set in Inspector) |
| `IsBusy` | `bool` | Whether a batch is currently executing |
| `PendingBatchCount` | `int` | Number of batches queued behind the current one |
| `CurrentActionName` | `string` | Display name of the action currently executing, or empty |
| `CancelOnUserSpeech` | `bool` | When enabled, the dispatcher cancels the in-flight batch and clears the queue the moment the player starts speaking. Default off |
| `EnablePerformanceReactions` | `bool` | Whether batch/step lifecycle notifies `IActionPerformanceReactor` peers (Gaze, Body Language, Emotion). Default on |
| `OnBatchStarted` | `UnityEvent` | Fires when a batch begins execution |
| `OnStepStarted` | `ConvaiActionInvocationUnityEvent` | Fires at the start of each action step |
| `OnStepSucceeded` | `ConvaiActionInvocationUnityEvent` | Fires when an executor returns `Succeeded` or `Answered` |
| `OnStepFailed` | `ConvaiActionInvocationUnityEvent` | Fires when a step fails (Failed, Canceled, or TimedOut) |
| `OnStepUnhandled` | `ConvaiActionInvocationUnityEvent` | Fires when an executor returns `Unhandled` |
| `OnStepCompleted` | `ConvaiActionStepReportUnityEvent` | Fires after every step, success or not, with the full `ConvaiActionStepReport` |
| `OnBatchCompleted` | `UnityEvent` | Fires when all batch steps finish without the batch being aborted |
| `OnBatchAborted` | `UnityEvent` | Fires when `StopBatch` policy cuts the batch short after a failure |
| `OnCancelledByUserSpeech` | `event Action<string>` | Fires when `CancelOnUserSpeech` cancels an in-flight action, carrying its display name |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `EnqueueActions` | `void EnqueueActions(IReadOnlyList<ConvaiActionCommand> actions)` | Submits a batch to the dispatcher. Respects the active `BatchPolicy` |

See [Dispatcher and batch policies](dispatcher-and-batch-policies.md) for batch/failure policy behavior and tuning guidance.

## `ConvaiActionConfigSource`

`MonoBehaviour` — `Convai.Runtime.Components`

Menu path: `Add Component → Convai → Convai Actions`

Constraints: `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)`

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `Definitions` | `IReadOnlyList<ConvaiActionDefinition>` | The authored inline action definitions list |
| `ActionSets` | `IReadOnlyList<ConvaiActionSet>` | Reusable action-set assets merged ahead of `Definitions`; an inline definition always wins a name collision against any set |
| `Objects` | `IReadOnlyList<ConvaiActionObjectDefinition>` | The authored actionable objects list |
| `Characters` | `IReadOnlyList<ConvaiActionCharacterDefinition>` | The authored actionable characters list |
| `InitialAttentionObject` | `string` | Object name to pre-seed as the NPC's focus at connect time |
| `ActionExecutionMode` | `ConvaiActionExecutionMode` | Declares whether `ConvaiActionDispatcher` or custom code runs this character's actions. Changes nothing at runtime; used by the SDK's own setup checks |
| `BehaviorHost` | `GameObject` | The object newly authored action behaviors are added to: the assigned child, or the character itself when none is assigned |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `BuildActionConfig` | `ConvaiActionConfig BuildActionConfig()` | Builds and returns the connect-time payload. Returns `null` if no valid definitions exist |

## `ConvaiActionExecutionMode`

`Convai.Runtime.Components`

| Value | Integer | Description |
| --- | --- | --- |
| `ConvaiActionDispatcher` | `0` | The shipped `ConvaiActionDispatcher` on this character runs the commands. Default; setup checks expect a dispatcher component in this mode |
| `CustomCode` | `1` | Your own code subscribes to `ConvaiCharacter.OnActionsReceived` or `ConvaiManager.Events.OnCharacterActionReceived` instead |

## `ConvaiCharacter` — action-relevant members

`MonoBehaviour` — `Convai.Runtime.Components`

### Events

| Event | Type | Description |
| --- | --- | --- |
| `OnActionsReceived` | `event Action<IReadOnlyList<ConvaiActionCommand>>` | Fires when Convai returns an action batch for this character. Fires before the dispatcher processes it |

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `ActionConfig` | `ConvaiActionConfig` | Returns a clone of the active session's action config. May be `null` before connect |

### Methods

| Method | Signature | Description |
| --- | --- | --- |
| `GetActionConfigSource` | `ConvaiActionConfigSource GetActionConfigSource()` | Returns the `ConvaiActionConfigSource` on this `GameObject`, or `null` |

{% hint style="info" %}
Runtime updates to the current attention object are handled by the dynamic context system, not by `ConvaiCharacter` directly. See [How action target resolution works](attention-and-reference-grounding.md#runtime-attention-api).
{% endhint %}

## `RoomSessionConnectOptions` — action fields

`Convai.Runtime.Room`

| Field | Type | Description |
| --- | --- | --- |
| `ActionConfigOverride` | `ConvaiActionConfig` | When set, replaces `ConvaiActionConfigSource.BuildActionConfig()` for this session |
| `ActionDefinitionsOverride` | `List<ConvaiActionDefinition>` | When set, replaces the Inspector action definitions for this session. Filtered against `ActionConfigOverride.Actions` if both are set |

## `ConvaiActionStepReport`

`Convai.Runtime.Actions` — Serializable sealed class

Completed-step report emitted on `ConvaiActionDispatcher.OnStepCompleted`.

| Property | Type | Description |
| --- | --- | --- |
| `Invocation` | `ConvaiActionInvocation` | The invocation the report describes |
| `Result` | `ConvaiActionExecutionResult` | Raw executor result for the step |
| `FailureReason` | `ConvaiActionFailureReason` | Passthrough for `Result.FailureReason` |
| `BatchAborted` | `bool` | Whether this step aborted the remaining batch |
| `Message` | `string` | Success detail, or the failure message for non-success statuses |
| `FailureMessage` | `string` | Failure detail including the batch consequence. Empty on success |

## Enumerations

The action system's remaining enums, grouped here for reference.

### `ConvaiActionBatchPolicy`

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `Queue` | `0` | New batches wait until the current batch completes. Default |
| `ReplaceCurrent` | `1` | Cancels the active step and all pending batches; starts the new batch immediately |
| `DropIncoming` | `2` | Discards new batches until all current and queued work is finished |

### `ConvaiActionBatchFailurePolicy`

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `StopBatch` | `0` | A failed step aborts the remaining batch. `OnBatchAborted` fires. Default |
| `ContinueBatch` | `1` | Execution continues to the next step regardless. `OnBatchCompleted` fires |

### `ConvaiActionTargetRequirement`

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `None` | `0` | Action does not require a target |
| `Object` | `1` | Action requires a resolved object target |
| `Character` | `2` | Action requires a resolved character target |
| `Either` | `3` | Action accepts either an object or a character as target |

### `ConvaiActionFailurePolicyOverride`

`Convai.Runtime.Actions`

| Value | Integer | Description |
| --- | --- | --- |
| `UseDispatcherDefault` | `0` | Follow the `ConvaiActionDispatcher` failure policy. Default |
| `StopBatch` | `1` | A non-success result aborts the remaining batch |
| `ContinueBatch` | `2` | A non-success result lets the remaining batch continue |

### `ConvaiActionTargetKind`

`Convai.Shared.Types`

| Value | Integer | Description |
| --- | --- | --- |
| `None` | `0` | No target resolved |
| `Object` | `1` | Target is a registered object |
| `Character` | `2` | Target is a registered character |

### `ConvaiActionParameterType`

`Convai.Shared.Types`

| Value | Integer | Description |
| --- | --- | --- |
| `Auto` | `0` | Infer reference, number, bool, or string best-effort, in that order. Default |
| `Reference` | `1` | Resolve an authored object or character target by name |
| `String` | `2` | Keep the raw text |
| `Number` | `3` | Parse an invariant-culture float |
| `Bool` | `4` | Parse `true`/`yes`/`1` or `false`/`no`/`0` |
| `Choice` | `5` | Require one of the authored choice strings. A mismatch flags the value through `IsConstraintMatch` |

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

Menu path: `Add Component → Convai → Actions → Diagnostics → Convai Action Monitor`

Constraints: `DisallowMultipleComponent`, `RequireComponent(ConvaiCharacter)`

See [Troubleshoot character actions](debugging-and-troubleshooting.md) for the full Inspector field reference and usage guide.

### Context menu actions

| Command | Effect |
| --- | --- |
| `Inject Test Batch` | Submits a `Move To` command targeting the first registered object to the dispatcher. Tests the pipeline without a live conversation |
| `Reset Probe State` | Resets all counters and text fields to zero/empty |

## Next steps

{% content-ref url="action-executors.md" %}
[Action executors](action-executors.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Character actions examples](usage-examples.md)
{% endcontent-ref %}

{% content-ref url="debugging-and-troubleshooting.md" %}
[Troubleshoot character actions](debugging-and-troubleshooting.md)
{% endcontent-ref %}
