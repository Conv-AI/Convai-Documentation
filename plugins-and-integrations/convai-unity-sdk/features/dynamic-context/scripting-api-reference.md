---
description: >-
  Complete reference for every method, parameter, and return value on the
  Dynamic Context scripting interface — for developers driving character
  awareness from game code.
---

# Scripting API Reference

## Scripting API Reference: IConvaiDynamicContext

`IConvaiDynamicContext` is the C# scripting surface for Dynamic Context. It is exposed as a property on `ConvaiCharacter` and provides seven methods covering every context operation — from setting a single tracked state to sending raw typed updates. This page is the authoritative reference for developers driving Dynamic Context from game systems, inventory managers, event buses, or any other runtime logic.

## Accessing the Interface

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public class MyContextController : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _character;

    private void Start()
    {
        IConvaiDynamicContext context = _character.DynamicContext;
        // Safe to cache — lazy-initialized, never null after ConvaiCharacter is constructed.
    }
}
```

`ConvaiCharacter.DynamicContext` is a lazy-initialized property that returns an `IConvaiDynamicContext` facade. The returned reference is safe to cache. It is never null after the `ConvaiCharacter` component has been constructed.

## Methods

### SetState

```csharp
void SetState(string name, string value, 
ConvaiContextReactionMode reaction = ConvaiContextReactionMode.SyncOnly)
```

Sets a single tracked state on the character.

<table><thead><tr><th width="116.49993896484375">Parameter</th><th width="238.99993896484375">Type</th><th width="121">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>string</code></td><td>—</td><td>State name. Must be non-null and non-whitespace.</td></tr><tr><td><code>value</code></td><td><code>string</code></td><td>—</td><td>State value. Must be non-null. An empty string is a valid value.</td></tr><tr><td><code>reaction</code></td><td><code>ConvaiContextReactionMode</code></td><td><code>SyncOnly</code></td><td>Controls whether the character immediately generates a response after the update.</td></tr></tbody></table>

**Behavior:**

* If the state does not exist, it is created and an Append message (`"Name is Value"`) is sent.
* If the state already exists with a **different** value, a Replace message (full canonical context) is sent first, followed by an Append message (`"Name changed from OldValue to NewValue"`).
* If the state already exists with the **same** value, no message is sent — the operation is idempotent with no network traffic and no LLM re-prompt.

**Validation:** Logs a warning and returns without sending if `name` is null or whitespace, or if `value` is null.

***

### SetStates

```csharp
void SetStates(IReadOnlyDictionary<string, string> states, 
ConvaiContextReactionMode reaction = ConvaiContextReactionMode.SyncOnly)
```

Updates multiple tracked states in a single atomic operation. Prefer this over multiple sequential `SetState` calls when several values change at the same time.

| Parameter  | Type                                  | Default    | Description                                                          |
| ---------- | ------------------------------------- | ---------- | -------------------------------------------------------------------- |
| `states`   | `IReadOnlyDictionary<string, string>` | —          | Dictionary of state names to values. Must be non-null and non-empty. |
| `reaction` | `ConvaiContextReactionMode`           | `SyncOnly` | Applied to the entire batch.                                         |

**Behavior:**

* If **any** state in the dictionary already exists in the tracker (with any value), a Replace message (full canonical context with all updated values) is sent first, then a single Append message summarising all changes.
* If **all** states in the dictionary are new, a single Append message is sent for all of them.
* Dictionary entries with null or whitespace keys are skipped silently.

**Validation:** Logs a warning and returns if `states` is null or empty.

***

### AddEvent

```csharp
void AddEvent(string text, 
ConvaiContextReactionMode reaction = ConvaiContextReactionMode.Auto)
```

Appends a chronological event to the character's context.

| Parameter  | Type                        | Default | Description                                                                                                                                                   |
| ---------- | --------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`     | `string`                    | —       | Event text to append. Must be non-null and non-whitespace.                                                                                                    |
| `reaction` | `ConvaiContextReactionMode` | `Auto`  | Controls whether the event immediately triggers an LLM turn. Note: the default here is `Auto`, unlike `SetState` and `SetStates` which default to `SyncOnly`. |

**Behavior:** Events accumulate in chronological order after all tracked states in the canonical context. Calling `AddEvent` with the same text twice appends it twice — events are never deduplicated.

**Validation:** Logs a warning and returns if `text` is null or whitespace.

***

### RemoveState

```csharp
void RemoveState(string name)
```

Removes a tracked state by name. Does not expose a `reaction` parameter.

| Parameter | Type     | Description                                  |
| --------- | -------- | -------------------------------------------- |
| `name`    | `string` | Name of the state to remove. Case-sensitive. |

**Behavior:** After removing the state from the local tracker, a Replace message is sent with the remaining canonical context. Removal always produces a Replace (not Append) because the character must receive the authoritative updated state set. If `name` does not match any tracked state, the call is a no-op.

***

### Reset

```csharp
void Reset()
```

Clears all tracked states and events and notifies the character.

**Behavior:** The local tracker is cleared entirely. A Reset mode message is sent to the character — no text is included. The initial dynamic info text configured on `ConvaiCharacter` is **not** re-sent; only the runtime-tracked states and events are erased.

After `Reset()`, the character's dynamic context is empty. Subsequent `SetState` or `AddEvent` calls build new context from scratch.

***

### TryGetStateValue

```csharp
bool TryGetStateValue(string name, out string value)
```

Reads the current tracked value for a state from the local tracker.

| Parameter   | Type           | Description                                                         |
| ----------- | -------------- | ------------------------------------------------------------------- |
| `name`      | `string`       | State name to look up.                                              |
| `value`     | `string` (out) | Receives the current value if the state is found.                   |
| **Returns** | `bool`         | `true` if the state exists in the local tracker; `false` otherwise. |

**Important:** This method reads from the **local tracker only**. It does not query the Convai server. The local tracker reflects all `SetState`, `SetStates`, and `RemoveState` calls made through `IConvaiDynamicContext`. It does not reflect anything sent via `Apply()`.

Use `TryGetStateValue` for conditional logic — for example, skipping a `SetState` call when the value has not changed from the game's perspective, or checking equipment state before triggering a dialogue branch.

***

### Apply

```csharp
void Apply(ConvaiDynamicContextUpdate update)
```

Sends a raw typed update directly to the transport layer, bypassing the local state tracker entirely.

| Parameter | Type                         | Description               |
| --------- | ---------------------------- | ------------------------- |
| `update`  | `ConvaiDynamicContextUpdate` | The typed update to send. |

**Behavior:**

* Sends the update immediately if the character is in an active conversation.
* **Does not queue pre-conversation.** If the character is not in a conversation, `Apply()` is a silent no-op. Unlike `SetState` and `AddEvent`, this method does not queue its effect for later flush.
* Does not update the local tracker. `TryGetStateValue` results are not affected by `Apply()` calls.

**When to use:** Use `Apply()` when you need to send a `Reset` mode update, or when an external system constructs its own context text and does not need the SDK's state tracking. For all standard state management, prefer `SetState`, `SetStates`, `AddEvent`, and `RemoveState`.

## ConvaiDynamicContextUpdate

`ConvaiDynamicContextUpdate` is the typed parameter for `Apply()`. It packages a text string, an update mode, and a reaction mode into a single value.

```csharp
var update = new ConvaiDynamicContextUpdate(
    text: "Trainee score is 72",
    mode: ConvaiContextUpdateMode.Append,
    reaction: ConvaiContextReactionMode.SyncOnly
);
_character.DynamicContext.Apply(update);
```

| Parameter  | Type                        | Default  | Description                                           |
| ---------- | --------------------------- | -------- | ----------------------------------------------------- |
| `text`     | `string`                    | —        | Context text to send. Ignored when `mode` is `Reset`. |
| `mode`     | `ConvaiContextUpdateMode`   | `Append` | How the text is applied on the backend.               |
| `reaction` | `ConvaiContextReactionMode` | `Auto`   | Whether the character immediately responds.           |

## Pre-Conversation Queueing

All tracked methods — `SetState`, `SetStates`, `AddEvent`, `RemoveState`, and `Reset` — queue their effects automatically when the character is not yet in an active conversation. When the conversation begins, all pending updates are flushed as a single canonical sync, or as a Reset if `Reset()` was the last call made.

This means it is safe to call these methods from `Awake()`, `Start()`, or any initialization code that runs before the character connects — the updates will not be lost.

{% hint style="warning" %}
`Apply()` does **not** queue. If called before a conversation starts, it is silently discarded with no warning. Always ensure the character is in an active conversation before calling `Apply()`, or use the tracked methods which queue automatically.
{% endhint %}

## Enum Reference

### ConvaiContextReactionMode

Controls whether a context update triggers an immediate LLM response from the character.

<table><thead><tr><th width="172.5">Value</th><th width="104.5">Numeric</th><th>Behaviour</th></tr></thead><tbody><tr><td><code>Auto</code></td><td><code>0</code></td><td>The server decides whether the update warrants an immediate LLM turn. Recommended as the default for most cases — the character reacts when the update is significant without being forced to respond every time.</td></tr><tr><td><code>ReactImmediately</code></td><td><code>1</code></td><td>Always triggers an LLM turn immediately after the update is applied. The character generates a response reacting to the new context, even if mid-conversation. Use for high-impact events that require immediate acknowledgement.</td></tr><tr><td><code>SyncOnly</code></td><td><code>2</code></td><td>Stores the context without prompting the LLM. The character remains silent and incorporates the new information into its next natural response. Use for background state updates that do not require acknowledgement.</td></tr></tbody></table>

### ConvaiContextUpdateMode

Controls how context text is applied on the backend. Relevant when using `Apply()` or the `RawUpdate` command type. Tracked methods (`SetState`, `SetStates`, `AddEvent`, `RemoveState`) manage this automatically and do not expose it directly.

<table><thead><tr><th width="116">Value</th><th width="105.50006103515625">Numeric</th><th>Behaviour</th></tr></thead><tbody><tr><td><code>Append</code></td><td><code>0</code></td><td>Adds the text to the existing ephemeral context. The character's context grows.</td></tr><tr><td><code>Replace</code></td><td><code>1</code></td><td>Replaces the entire ephemeral context with the new text. Everything previously accumulated is discarded.</td></tr><tr><td><code>Reset</code></td><td><code>2</code></td><td>Clears all ephemeral context. The <code>text</code> field is ignored when this mode is used.</td></tr></tbody></table>

## What's Next

* [Sync Behavior and Timing](../../../unity-plugin-beta-overview/features/dynamic-context/sync-behavior-and-timing.md) — when and how each update type is transmitted, including the two-message Replace+Append pattern and the mechanics of the pre-conversation queue flush.

## Conclusion

`IConvaiDynamicContext` provides a precise, type-safe surface for every Dynamic Context operation. The tracked methods queue automatically before a conversation starts; `Apply()` does not — choose accordingly. For a complete breakdown of when and how each update type is transmitted, see [Sync Behavior and Timing](../../../unity-plugin-beta-overview/features/dynamic-context/sync-behavior-and-timing.md).
