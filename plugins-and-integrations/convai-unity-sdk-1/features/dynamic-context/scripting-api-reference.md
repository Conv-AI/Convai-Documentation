---
description: >-
  API reference for IConvaiDynamicContext — all seven method signatures, default
  parameters, pre-conversation queueing behavior, and Apply() caveats.
---

# Scripting API Reference

## IConvaiDynamicContext Method Reference

`IConvaiDynamicContext` is the C# surface for programmatic Dynamic Context control. Access it through the `DynamicContext` property on `ConvaiCharacter`:

```csharp
IConvaiDynamicContext context = _character.DynamicContext;
```

The property is lazy-initialized and safe to cache for the lifetime of the component. No additional setup is required.

***

## Method Reference

### `SetState`

```csharp
void SetState(string name, string value,
    ConvaiContextReactionMode reaction = ConvaiContextReactionMode.SyncOnly)
```

Sets or updates one tracked state entry. If the state does not exist, it is created and appended to the canonical context in the order it was first set. If the value is identical to the current value, the call is a no-op — no update is sent.

**Parameters**

| Parameter  | Type                        | Default    | Description                                                             |
| ---------- | --------------------------- | ---------- | ----------------------------------------------------------------------- |
| `name`     | `string`                    | —          | State identifier. Must be non-empty and non-whitespace. Case-sensitive. |
| `value`    | `string`                    | —          | State value. May be empty string. Cannot be `null`.                     |
| `reaction` | `ConvaiContextReactionMode` | `SyncOnly` | Controls whether the character generates an immediate response.         |

**Network behavior**

| Condition                     | Messages Sent                                                                       |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| New state                     | One Append: `"{name} is {value}"`                                                   |
| Existing state, value changed | Replace (full canonical context) + Append: `"{name} changed from {old} to {value}"` |
| Identical value               | None — idempotent no-op                                                             |

**Pre-conversation:** queues automatically; delivered as a single Replace at connection time.

***

### `SetStates`

```csharp
void SetStates(IReadOnlyDictionary<string, string> states,
    ConvaiContextReactionMode reaction = ConvaiContextReactionMode.SyncOnly)
```

Sets or updates multiple tracked state entries atomically. Prefer over sequential `SetState` calls when several values change simultaneously — produces one canonical rebuild rather than multiple.

**Parameters**

| Parameter  | Type                                  | Default    | Description                                                     |
| ---------- | ------------------------------------- | ---------- | --------------------------------------------------------------- |
| `states`   | `IReadOnlyDictionary<string, string>` | —          | Map of state names to values. Must have at least one entry.     |
| `reaction` | `ConvaiContextReactionMode`           | `SyncOnly` | Controls whether the character generates an immediate response. |

**Network behavior**

| Condition                       | Messages Sent                                                      |
| ------------------------------- | ------------------------------------------------------------------ |
| All states are new              | One Append listing all new state lines                             |
| Any existing state changed      | Replace (full canonical context) + Append (all changes summarized) |
| All values identical to current | None — no-op                                                       |

**Pre-conversation:** queues automatically.

```csharp
_character.DynamicContext.SetStates(
    new Dictionary<string, string>
    {
        { "Station", "Bay 7" },
        { "HazardLevel", "Extreme" }
    },
    ConvaiContextReactionMode.ReactImmediately
);
```

***

### `AddEvent`

```csharp
void AddEvent(string text,
    ConvaiContextReactionMode reaction = ConvaiContextReactionMode.Auto)
```

Appends a chronological event entry. Events accumulate in call order after all states in the canonical context. Unlike states, events are never replaced or deduplicated — each call adds a new line.

**Parameters**

| Parameter  | Type                        | Default | Description                                                                                                                                                           |
| ---------- | --------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`     | `string`                    | —       | Event description. Must be non-empty and non-whitespace.                                                                                                              |
| `reaction` | `ConvaiContextReactionMode` | `Auto`  | Controls whether the character generates an immediate response. Default is `Auto` — note the difference from `SetState` and `SetStates`, which default to `SyncOnly`. |

**Network behavior:** One Append message containing the event text.

**Pre-conversation:** queues automatically.

***

### `RemoveState`

```csharp
void RemoveState(string name)
```

Removes a tracked state by name and sends an updated canonical context to Convai. If the state is not present in the tracker, the call is a no-op — no message is sent and no warning is logged.

**Parameters**

| Parameter | Type     | Description                                     |
| --------- | -------- | ----------------------------------------------- |
| `name`    | `string` | Name of the state to remove. Must be non-empty. |

**Network behavior:** One Replace message containing the canonical context with the state removed. `RemoveState` has no reaction mode — removal never triggers an immediate LLM response.

**Pre-conversation:** queues automatically.

***

### `Reset`

```csharp
void Reset()
```

Clears all tracked states and events and sends a Reset message to Convai. Takes no parameters.

**Network behavior:** One Reset-mode message. The character's Dynamic Context view on the Convai side is cleared.

**Pre-conversation:** queues automatically.

{% hint style="warning" %}
`Reset()` clears the runtime Dynamic Context layer only. It does not affect Initial Dynamic Info Text (sent once at connection time) or facts in the character's system prompt on the Convai dashboard. The character's in-session conversational memory is also not cleared. See [Static Context at Connection Time](/broken/pages/2a2adf9190877c2daa0a245e4a6f8659dc37394e) for the full scope of what `Reset()` does and does not clear.
{% endhint %}

***

### `TryGetStateValue`

```csharp
bool TryGetStateValue(string name, out string value)
```

Reads the current value of a tracked state from the local tracker. No network call is made.

**Parameters**

| Parameter | Type         | Description                                             |
| --------- | ------------ | ------------------------------------------------------- |
| `name`    | `string`     | State name to look up.                                  |
| `value`   | `out string` | Set to the current value if found; `null` if not found. |

**Returns:** `true` if the state exists in the local tracker; `false` if it was never set, has been removed, or was sent via `Apply()` (which bypasses the tracker).

```csharp
if (_character.DynamicContext.TryGetStateValue("HazardLevel", out string level))
    Debug.Log($"Current hazard level: {level}");
else
    Debug.Log("HazardLevel state not set.");
```

***

### `Apply`

```csharp
void Apply(ConvaiDynamicContextUpdate update)
```

Sends a raw typed update directly to the transport layer, bypassing the local tracker. For advanced use cases that construct context text externally — for example, integrating with an external state machine that produces its own canonical text.

**Parameters**

| Parameter | Type                         | Description         |
| --------- | ---------------------------- | ------------------- |
| `update`  | `ConvaiDynamicContextUpdate` | The update to send. |

**`ConvaiDynamicContextUpdate` constructor:**

```csharp
new ConvaiDynamicContextUpdate(
    string text,
    ConvaiContextUpdateMode mode = ConvaiContextUpdateMode.Append,
    ConvaiContextReactionMode reaction = ConvaiContextReactionMode.Auto)
```

| Parameter  | Type                        | Default  | Description                                              |
| ---------- | --------------------------- | -------- | -------------------------------------------------------- |
| `text`     | `string`                    | —        | Context text to send. Required unless `mode` is `Reset`. |
| `mode`     | `ConvaiContextUpdateMode`   | `Append` | How Convai applies the text.                             |
| `reaction` | `ConvaiContextReactionMode` | `Auto`   | Whether the character responds immediately.              |

{% hint style="danger" %}
**`Apply()` does not queue.** If the character is not in an active conversation when `Apply()` is called, the update is discarded and a warning is emitted through the Convai logger. Enable Convai debug logging to see it in the Unity Console. No queue is built — the update is lost permanently.

Values sent via `Apply()` are **not** recorded in the local tracker. `TryGetStateValue` returns `false` for keys sent this way.

For all standard context management, use the tracked methods (`SetState`, `SetStates`, `AddEvent`, `RemoveState`, `Reset`). `Apply()` is an escape hatch for external systems, not the primary API.
{% endhint %}

***

## Enum Reference

### `ConvaiContextReactionMode`

| Value              | Description                                                                                                                |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| `Auto`             | Convai decides whether the update warrants an immediate character response.                                                |
| `ReactImmediately` | Always triggers an immediate LLM turn after the update. Use when the character must acknowledge the change.                |
| `SyncOnly`         | Context is updated silently. The character incorporates it into the next natural turn. No immediate response is generated. |

### `ConvaiContextUpdateMode`

Used by `Apply()` and `ConvaiDynamicContextCommand` with **Raw Update** command type.

| Value     | Description                                                                       |
| --------- | --------------------------------------------------------------------------------- |
| `Append`  | Adds the text to the existing Dynamic Context without replacing prior content.    |
| `Replace` | Replaces the entire Dynamic Context with the provided text.                       |
| `Reset`   | Clears all Dynamic Context. The `text` parameter is ignored when mode is `Reset`. |

***

## Default Reaction Mode Reference

| Method                                 | Default Reaction          |
| -------------------------------------- | ------------------------- |
| `SetState`                             | `SyncOnly`                |
| `SetStates`                            | `SyncOnly`                |
| `AddEvent`                             | `Auto`                    |
| `RemoveState`                          | _(no reaction parameter)_ |
| `Reset`                                | _(always `SyncOnly`)_     |
| `Apply()` `ConvaiDynamicContextUpdate` | `Auto`                    |

{% hint style="warning" %}
`ConvaiDynamicContextCommand` (the Inspector component) defaults **Reaction Mode** to `Auto` for all command types — including `SetState` and `SetStates`. This differs from the scripting API defaults above. When switching between Inspector and scripting, verify the reaction mode is what you expect.
{% endhint %}

## Next Steps

For timing and network details on each operation, see [Sync Behavior and Timing](/broken/pages/fd07c33dbde4c8f46f1472ab841d25ba0bc5951e). For Inspector-based control without code, see [Command Component Reference](/broken/pages/2cc3e062f8f38c3edb00be71bae54d5afaa96330). To diagnose unexpected behavior, see [Troubleshooting & Diagnostics](/broken/pages/3480f92daa72bcc66c4588342182879397d2b564).
