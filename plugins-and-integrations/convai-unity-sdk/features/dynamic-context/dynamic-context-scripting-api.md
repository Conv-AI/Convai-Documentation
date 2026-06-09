---
title: Dynamic context scripting API
description: Reference the Unity runtime API for tracked state, events, attention objects, flushing, raw updates, result events, and reset scope.
last_reviewed: "4.2.0"
---

`IConvaiDynamicContext` is the C# API for character-scoped Dynamic Context. Access it from `ConvaiCharacter.DynamicContext`.

```csharp
IConvaiDynamicContext context = character.DynamicContext;
```

The facade is lazy-initialized and can be cached for the lifetime of the character component.

## Namespace

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
```

## Method reference

### `SetState`

```csharp
void SetState(
    string name,
    string value,
    ConvaiDynamicContextReactionMode reaction = ConvaiDynamicContextReactionMode.SyncOnly)
```

Sets or updates one tracked state. The state name must be non-empty. The value can be an empty string but cannot be `null`. If the value has not changed, the call is a no-op.

### `SetStates`

```csharp
void SetStates(
    IReadOnlyDictionary<string, string> states,
    ConvaiDynamicContextReactionMode reaction = ConvaiDynamicContextReactionMode.SyncOnly)
```

Sets or updates multiple tracked states in one call. Use this when a simulation transition changes several facts at the same moment.

```csharp
character.DynamicContext.SetStates(
    new Dictionary<string, string>
    {
        ["Station"] = "Bay 7",
        ["HazardLevel"] = "Extreme"
    },
    ConvaiDynamicContextReactionMode.ReactImmediately);
```

### `AddEvent`

```csharp
void AddEvent(
    string text,
    ConvaiDynamicContextReactionMode reaction = ConvaiDynamicContextReactionMode.Auto)
```

Adds a chronological event line. The text must be non-empty. Duplicate event text inside the same pending batch is ignored.

### `RemoveState`

```csharp
void RemoveState(string name)
```

Removes one tracked state. If the state does not exist, the call is a no-op. Removal uses `SyncOnly`.

### `Reset`

```csharp
void Reset(bool removeStatic = false)
```

Clears tracked runtime states and events. Passing `removeStatic: true` also sends `remove_static: true` in the next reset update, which asks Convai to clear static connect-time context for the current session.

{% hint style="warning" %}
`Reset()` does not change the serialized fields on `ConvaiCharacter`, does not edit dashboard prompts, and does not erase in-session conversation memory. A later reconnect can send initial context again if it is still enabled on the character.
{% endhint %}

### `SetCurrentAttentionObject`

```csharp
void SetCurrentAttentionObject(
    object currentAttentionObject,
    ConvaiDynamicContextReactionMode reaction = ConvaiDynamicContextReactionMode.SyncOnly)
```

Sets the `current_attention_object` field used for action-reference grounding. Passing a string name is the usual path. If the active action config contains objects, the name must match one of those objects.

### `ClearCurrentAttentionObject`

```csharp
void ClearCurrentAttentionObject(
    ConvaiDynamicContextReactionMode reaction = ConvaiDynamicContextReactionMode.SyncOnly)
```

Clears the current attention object by sending an empty value.

### `Flush`

```csharp
void Flush()
```

Sends pending tracked changes immediately when the character is in conversation. If the character is not in conversation, tracked changes remain local and flush when `CharacterReady` arrives.

### `TryGetStateValue`

```csharp
bool TryGetStateValue(string name, out string value)
```

Reads the local tracker. This method does not call Convai.

```csharp
if (character.DynamicContext.TryGetStateValue("HazardLevel", out string level))
    Debug.Log($"Hazard level: {level}");
```

`TryGetStateValue` returns `false` for states that were never tracked, were removed, or were sent only through `Apply()`.

### `Apply`

```csharp
void Apply(ConvaiDynamicContextUpdate update)
```

Sends a raw typed update without mutating the local tracker.

```csharp
character.DynamicContext.Apply(new ConvaiDynamicContextUpdate(
    "External state snapshot: alarm active",
    ConvaiDynamicContextUpdateMode.Replace,
    ConvaiDynamicContextReactionMode.Auto));
```

Use `Apply()` only when another system owns the full context text. It does not queue before conversation start and does not make values readable through `TryGetStateValue`.

## Update object

```csharp
public ConvaiDynamicContextUpdate(
    string text,
    ConvaiDynamicContextUpdateMode mode = ConvaiDynamicContextUpdateMode.Append,
    ConvaiDynamicContextReactionMode reaction = ConvaiDynamicContextReactionMode.Auto,
    bool removeStatic = false,
    object currentAttentionObject = null,
    string updateId = null)
```

| Parameter | Description |
|---|---|
| `text` | Context text. Required unless `mode` is `Reset`. |
| `mode` | How Convai applies the text: `Append`, `Replace`, or `Reset`. |
| `reaction` | Whether the update should request an immediate response. |
| `removeStatic` | Sends `remove_static` on reset updates. |
| `currentAttentionObject` | Sends `current_attention_object` for action-reference grounding. |
| `updateId` | Optional client-provided update identifier. Generated tracked updates use `unity-{characterId}-{sequence}`. |

## Enum reference

### `ConvaiDynamicContextReactionMode`

| Value | `run_llm` | Description |
|---|---|---|
| `SyncOnly` | `false` | Store context without requesting an immediate response. |
| `Auto` | `auto` | Let Convai decide whether to respond immediately. |
| `ReactImmediately` | `true` | Request an immediate response. |

### `ConvaiDynamicContextUpdateMode`

| Value | Description |
|---|---|
| `Append` | Appends raw text when using `Apply()`. Tracked attention-only updates also use this mode with no text. |
| `Replace` | Replaces the current Dynamic Context text. Tracked text changes use this mode. |
| `Reset` | Clears Dynamic Context. `text` is ignored. |

## Default reactions

| Operation | Default reaction |
|---|---|
| `SetState` | `SyncOnly` |
| `SetStates` | `SyncOnly` |
| `AddEvent` | `Auto` |
| `RemoveState` | `SyncOnly` |
| `Reset` | `SyncOnly` |
| `SetCurrentAttentionObject` | `SyncOnly` |
| `ClearCurrentAttentionObject` | `SyncOnly` |
| `Apply()` | `Auto` from `ConvaiDynamicContextUpdate` |
| `ConvaiDynamicContextRelay` | `SyncOnly` |

## Result event

Subscribe to `ConvaiManager.Events.OnDynamicContextUpdateResultReceived` to inspect acknowledgements from Convai.

```csharp
manager.Events.OnDynamicContextUpdateResultReceived += result =>
{
    Debug.Log(
        $"Dynamic context {result.Status}: " +
        $"update={result.UpdateId}, revision={result.ContextRevision}, " +
        $"requested={result.RequestedRunLlm}, actual={result.ActualRunLlm}");
};
```

The event exposes `Status`, `Message`, `UpdateId`, `ContextRevision`, `TokenCount`, `StaticTokenCount`, `RuntimeTokenCount`, `RemainingTokens`, `RequestedRunLlm`, `ActualRunLlm`, `DowngradeReason`, `Interrupted`, `LlmTriggered`, `PromptRebuild`, `RawExtras`, and `Timestamp`.

## Next steps

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}

{% content-ref url="relay-component-reference.md" %}
[Relay component reference](relay-component-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}
