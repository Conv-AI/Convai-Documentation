---
title: Dynamic context scripting API
description: >-
  Reference for the Convai Unity SDK dynamic context scripting interface,
  including every method, the respond mode enum, and the attention object API.
last_reviewed: "4.4.0"
---

`ConvaiCharacter.DynamicContext` returns the `IConvaiDynamicContext` interface — the scripting surface for tracked state, chronological events, attention-object updates, and raw context sends. This page documents every interface member, the `ConvaiRespondMode` enum that controls whether an update triggers a spoken reply, and the `ConvaiDynamicContextUpdate` type used by `Apply`.

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;

IConvaiDynamicContext context = character.DynamicContext;
```

`DynamicContext` is available on every `ConvaiCharacter` instance and requires no additional setup.

{% hint style="warning" %}
`ConvaiContextReactionMode` is removed as of SDK 4.3.0. Every method below takes a `ConvaiRespondMode` value instead. See [Migration from ConvaiContextReactionMode](#migration-from-convaicontextreactionmode) for the full migration table.
{% endhint %}

## Method reference

Every tracked method below stages its change in the local tracker; Convai receives the update in the next dynamic context batch — a background flush that fires after `ConvaiCharacter.DynamicContextBatchDelaySeconds` (0.5 seconds by default) or immediately when `Flush()` is called, capped at an internal maximum delay so staged changes are never held indefinitely. When more than one reaction is requested before a batch flushes, the strongest value wins for the whole batch, ranked `Silent` < `Auto` < `MustRespond`. See [Sync behavior and timing](sync-behavior-and-timing.md) for the exact batch window and message content.

### `SetState`

```csharp
void SetState(string name, string value,
    ConvaiRespondMode reaction = ConvaiRespondMode.Silent)
```

Sets or updates one tracked state entry. If `name` has not been set before, Convai adds it to the [canonical context](how-dynamic-context-works.md#canonical-context-format) in the order it was first set. If `value` is identical to the current value, the call is a no-op — nothing is staged.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `string` | — | State identifier. Must be non-empty and non-whitespace. Case-sensitive. |
| `value` | `string` | — | State value. May be an empty string. Cannot be `null`. |
| `reaction` | `ConvaiRespondMode` | `Silent` | Requested reaction for this change. |

### `SetStates`

```csharp
void SetStates(IReadOnlyDictionary<string, string> states,
    ConvaiRespondMode reaction = ConvaiRespondMode.Silent)
```

Sets or updates multiple tracked state entries in one call, each staged with the same `reaction` value. Prefer `SetStates` over sequential `SetState` calls when several values change at the same moment.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `states` | `IReadOnlyDictionary<string, string>` | — | Map of state names to values. Must have at least one entry. |
| `reaction` | `ConvaiRespondMode` | `Silent` | Requested reaction applied to every entry in this call. |

If `states` is `null` or empty, Convai logs a warning (`Cannot set empty dynamic context states`) and the call returns without staging anything. Individual invalid entries (empty name, `null` value) are skipped; the remaining valid entries in the same call still stage.

```csharp
character.DynamicContext.SetStates(
    new Dictionary<string, string>
    {
        { "Station", "Bay 7" },
        { "HazardLevel", "Extreme" }
    },
    ConvaiRespondMode.MustRespond
);
```

### `AddEvent`

```csharp
void AddEvent(string text, ConvaiRespondMode reaction = ConvaiRespondMode.Auto)
```

Appends a chronological event entry. Events accumulate after all states in the canonical context and are never replaced by a later call.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `string` | — | Event description. Must be non-empty and non-whitespace. |
| `reaction` | `ConvaiRespondMode` | `Auto` | Requested reaction. Note the default differs from `SetState` and `SetStates`, which default to `Silent`. |

Calling `AddEvent` with identical `text` more than once before the pending batch flushes stages only one entry. The dedup window resets after each flush — the same text staged in a later batch is added again.

### `RemoveState`

```csharp
void RemoveState(string name)
```

Removes a tracked state by name and stages an updated canonical context for the next batch. If `name` is not currently tracked, the call is a no-op — nothing is staged and no warning is logged.

| Parameter | Type | Description |
|---|---|---|
| `name` | `string` | Name of the state to remove. Must be non-empty; an empty or whitespace value logs a warning (`Dynamic context state name cannot be empty`) and the call returns immediately. |

`RemoveState` has no `reaction` parameter. The staged change always carries `ConvaiRespondMode.Silent` — removing a state never triggers an immediate reply on its own.

### `Reset`

```csharp
void Reset(bool removeStatic = false)
```

Clears every tracked state and event and stages a Reset message for Convai.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `removeStatic` | `bool` | `false` | When `true`, the reset also asks Convai to remove the character's static initial dynamic context for the current session. When `false`, only the runtime tracker is cleared. |

`Reset` has no `reaction` parameter — the staged Reset message always carries `ConvaiRespondMode.Silent`. See [Static context at connection time](static-context-at-connection-time.md) for how the static initial dynamic context is set.

### `SetCurrentAttentionObject`

```csharp
void SetCurrentAttentionObject(object currentAttentionObject,
    ConvaiRespondMode reaction = ConvaiRespondMode.Silent)
```

Stages the object Convai should treat as the character's current focus for reference grounding — resolving vague player language such as "pick that up" to a specific registered target.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `currentAttentionObject` | `object` | — | Accepts a `string` object name or a `ConvaiActionObjectDefinition` reference. Any other type, or `null`, is rejected. |
| `reaction` | `ConvaiRespondMode` | `Silent` | Requested reaction for the focus change. |

See [Attention and reference grounding](../character-actions/attention-and-reference-grounding.md) for the full grounding model, silent-failure conditions, and usage examples.

### `ClearCurrentAttentionObject`

```csharp
void ClearCurrentAttentionObject(ConvaiRespondMode reaction = ConvaiRespondMode.Silent)
```

Stages a clear for the current attention object. Convai treats the character as having no specific focus until the next `SetCurrentAttentionObject` call.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `reaction` | `ConvaiRespondMode` | `Silent` | Requested reaction for the clear. |

### `Flush`

```csharp
void Flush()
```

Sends any staged dynamic context (and pending scene-metadata) changes immediately, without waiting for the batch window. `Flush` is a no-op when the character is not in an active conversation — staged data remains pending and is included in the batch sent automatically once the character becomes ready.

### `TryGetStateValue`

```csharp
bool TryGetStateValue(string name, out string value)
```

Reads the current value of a tracked state from the local tracker. No network call is made.

| Parameter | Type | Description |
|---|---|---|
| `name` | `string` | State name to look up. |
| `value` | `out string` | Set to the current value if found; `null` if not found. |

**Returns:** `true` if the state exists in the local tracker; `false` if it was never set, has been removed, or was sent through `Apply` (which bypasses the tracker).

```csharp
if (character.DynamicContext.TryGetStateValue("HazardLevel", out string level))
    Debug.Log($"Current hazard level: {level}");
else
    Debug.Log("HazardLevel state not set.");
```

### `Apply`

```csharp
void Apply(ConvaiDynamicContextUpdate update)
```

Sends a raw typed update directly to the transport layer, bypassing the local tracker and the batch queue. Use for advanced cases that construct context text externally, or that combine a context update with a runtime action-config patch or attention-object change in one message — see [`ConvaiActionConfigPatch`](../character-actions/actions-scripting-reference.md#convaiactionconfigpatch) in the character actions scripting reference.

| Parameter | Type | Description |
|---|---|---|
| `update` | `ConvaiDynamicContextUpdate` | The update to send. See [`ConvaiDynamicContextUpdate`](#convaidynamiccontextupdate) below. |

| Condition | Result |
|---|---|
| `update` is `null` | Warning: `Raw dynamic context update cannot be null`. Call returns without sending. |
| `update.Mode` is not `Reset`, and `Text`, `ActionConfig`, and `CurrentAttentionObject` are all `null` | Warning: `Raw dynamic context updates require text, action_config, current_attention_object, or Reset mode`. Call returns without sending. |
| Character is not in an active conversation | Warning: `Cannot apply raw dynamic context update: not in conversation`. Update discarded. |

{% hint style="danger" %}
**`Apply` does not queue or batch.** If the character is not in an active conversation, Convai discards the update and logs a warning — nothing is sent and nothing is retried. Values sent through `Apply` bypass the local tracker: `TryGetStateValue` returns `false` for keys sent this way. Use the tracked methods (`SetState`, `SetStates`, `AddEvent`, `RemoveState`, `Reset`) for all standard context management.
{% endhint %}

## `ConvaiDynamicContextUpdate`

`Convai.Runtime.DynamicContext` — sealed class

Advanced typed request used by `Apply` to send raw dynamic context updates without exposing transport strings.

```csharp
new ConvaiDynamicContextUpdate(
    string text,
    ConvaiContextUpdateMode mode = ConvaiContextUpdateMode.Append,
    ConvaiRespondMode reaction = ConvaiRespondMode.Auto,
    bool removeStatic = false,
    object currentAttentionObject = null,
    string updateId = null,
    ConvaiActionConfigPatch actionConfig = null)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `string` | — | Context text to send. At least one of `text`, `actionConfig`, or `currentAttentionObject` must be set, or `mode` must be `Reset`. |
| `mode` | `ConvaiContextUpdateMode` | `Append` | How Convai applies the text. |
| `reaction` | `ConvaiRespondMode` | `Auto` | Whether the update triggers a spoken reply. |
| `removeStatic` | `bool` | `false` | When `mode` is `Reset` and this is `true`, also asks Convai to remove the character's static initial dynamic context for the session. |
| `currentAttentionObject` | `object` | `null` | Attention object to set alongside this update. Accepts a `string` object name or a `ConvaiActionObjectDefinition` reference. |
| `updateId` | `string` | `null` | Correlates this update with its backend acknowledgement. Auto-generated when omitted. |
| `actionConfig` | `ConvaiActionConfigPatch` | `null` | Runtime action-config patch to apply alongside this context update. See [Character actions scripting reference](../character-actions/actions-scripting-reference.md#convaiactionconfigpatch). |

## `ConvaiContextUpdateMode`

Used by `Apply` and `ConvaiDynamicContextUpdate`.

| Value | Description |
|---|---|
| `Append` | Adds the text to the existing Dynamic Context without replacing prior content. |
| `Replace` | Replaces the entire Dynamic Context with the provided text. |
| `Reset` | Clears all Dynamic Context. The `text` parameter is ignored when `mode` is `Reset`. |

## `ConvaiRespondMode`

`Convai.Runtime` — the single respond-mode vocabulary shared by dynamic context and dynamic vision.

| Value | Wire string | Description |
|---|---|---|
| `Silent` | `silent` | Absorbed into the character's awareness; never triggers a spoken reply on its own. |
| `Auto` | `auto` | Convai decides whether the update warrants a spoken reply. |
| `MustRespond` | `must_respond` | Always triggers a spoken reply after the update. |

### Migration from `ConvaiContextReactionMode`

`ConvaiContextReactionMode` is removed in SDK 4.3.0. Every dynamic-context method uses `ConvaiRespondMode` instead.

| Old value (`ConvaiContextReactionMode`) | New value (`ConvaiRespondMode`) |
|---|---|
| `SyncOnly` | `Silent` |
| `ReactImmediately` | `MustRespond` |
| `Auto` | `Auto` (unchanged) |

The enum was renumbered as part of the rename — `ConvaiRespondMode` declares `Silent = 0, Auto = 1, MustRespond = 2`, while the removed `ConvaiContextReactionMode` declared `Auto = 0, ReactImmediately = 1, SyncOnly = 2`. A scene or prefab saved with a serialized reaction override against an unreleased beta build changes meaning after upgrading: old `Auto` (`0`) deserializes as `Silent`, old `ReactImmediately` (`1`) as `Auto`, and old `SyncOnly` (`2`) as `MustRespond`. Shipped SDK assets carry no such serialized values — this only affects scenes saved against pre-release beta builds. Re-check any serialized reaction field after upgrading if that applies to your project.

## Default reaction mode reference

| Method | Default reaction |
|---|---|
| `SetState` | `Silent` |
| `SetStates` | `Silent` |
| `AddEvent` | `Auto` |
| `RemoveState` | _(no `reaction` parameter; always `Silent`)_ |
| `Reset` | _(no `reaction` parameter; always `Silent`)_ |
| `SetCurrentAttentionObject` | `Silent` |
| `ClearCurrentAttentionObject` | `Silent` |
| `Apply` / `ConvaiDynamicContextUpdate` | `Auto` |

## Next steps

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}

{% content-ref url="relay-component-reference.md" %}
[Relay component reference](relay-component-reference.md)
{% endcontent-ref %}

{% content-ref url="../character-actions/attention-and-reference-grounding.md" %}
[Attention and reference grounding](../character-actions/attention-and-reference-grounding.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}
