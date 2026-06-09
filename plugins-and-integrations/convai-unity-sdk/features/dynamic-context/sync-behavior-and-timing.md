---
title: Sync behavior and timing
description: Understand when Unity batches, flushes, replays, and serializes runtime context, attention, and reset updates for active sessions.
last_reviewed: "4.2.0"
---

Tracked Dynamic Context calls update local state first. The SDK then sends one composed `context-update` message when the pending batch flushes. This page documents that timing and the payload shape.

## Batch timing

| Situation | Behavior |
|---|---|
| Tracked call during active conversation | Stages a pending batch and schedules an automatic flush. |
| Automatic flush | Runs about `0.5` seconds after pending changes, capped by a `3` second maximum batch window. |
| Manual `Flush()` | Sends the current pending batch immediately when the character is in conversation. |
| Tracked call before `CharacterReady` | Updates the local tracker and waits. The first ready signal flushes one composed update. |
| Disconnect or reconnect | Tracked context is marked pending and re-sent as a composed update after the next ready signal. |
| `Apply()` before active conversation | Discarded with a warning. It is not queued. |

## Outgoing message shape

Tracked text changes send `mode: "replace"` because the payload is the character's current composed Dynamic Context view.

```json
{
  "type": "context-update",
  "data": {
    "text": "Station is Bay 7\nHazardLevel is High",
    "mode": "replace",
    "run_llm": "auto",
    "update_id": "unity-character-id-1"
  }
}
```

The payload can also include `remove_static` and `current_attention_object`.

## New state

```csharp
context.SetState("Station", "Bay 3");
context.Flush();
```

Flush result:

```text
mode: replace
run_llm: false
text: Station is Bay 3
```

`SetState` defaults to `SyncOnly`, so `run_llm` is `false` unless you pass a different reaction mode.

## Existing state change

```csharp
context.SetState(
    "Station",
    "Bay 7",
    ConvaiDynamicContextReactionMode.ReactImmediately);
context.Flush();
```

Flush result:

```text
mode: replace
run_llm: true
text:
Station is Bay 7
Station changed from Bay 3 to Bay 7
```

The change line is included inside the same `replace` payload. It is not a second `context-update` message.

## Multiple states

Use `SetStates` when several values change at the same moment.

```csharp
context.SetStates(
    new Dictionary<string, string>
    {
        ["Station"] = "Bay 7",
        ["HazardLevel"] = "Extreme"
    },
    ConvaiDynamicContextReactionMode.ReactImmediately);
context.Flush();
```

Flush result:

```text
mode: replace
run_llm: true
text:
Station is Bay 7
Station changed from Bay 3 to Bay 7
HazardLevel is Extreme
```

The exact order depends on which states were already tracked and which states first appear in the current reactive batch. The important behavior is that the SDK sends one composed update.

## Events

```csharp
context.AddEvent("Operator bypassed interlock");
context.Flush();
```

Flush result:

```text
mode: replace
run_llm: auto
text: Operator bypassed interlock
```

`AddEvent` defaults to `Auto`. Duplicate event text inside one pending batch is ignored. The same text can be added again in a later batch if the event genuinely happens again.

## State removal

```csharp
context.RemoveState("Station");
context.Flush();
```

Flush result:

```text
mode: replace
run_llm: false
text: {canonical context without Station}
```

If the removed state was the only tracked content, the SDK sends an empty `text` value with `mode: "replace"`.

## Attention object only

```csharp
context.SetCurrentAttentionObject("lever");
context.Flush();
```

When no text changed, the SDK sends the attention object without changing the stored context text.

```json
{
  "type": "context-update",
  "data": {
    "mode": "append",
    "run_llm": "false",
    "current_attention_object": "lever",
    "update_id": "unity-character-id-2"
  }
}
```

If text changes and attention changes are batched together, both are included in the same update.

## Reset

```csharp
context.Reset(removeStatic: true);
context.Flush();
```

Flush result:

```json
{
  "type": "context-update",
  "data": {
    "mode": "reset",
    "run_llm": "false",
    "remove_static": true,
    "update_id": "unity-character-id-3"
  }
}
```

`Reset()` clears the local tracker. `removeStatic: true` also asks Convai to remove static connect-time context for the current session.

## Raw `Apply()`

`Apply()` sends the `ConvaiDynamicContextUpdate` you provide. It can use `Append`, `Replace`, or `Reset`, and it can include `currentAttentionObject`, `removeStatic`, or a custom `updateId`.

```csharp
context.Apply(new ConvaiDynamicContextUpdate(
    "External state snapshot: alarm active",
    ConvaiDynamicContextUpdateMode.Replace,
    ConvaiDynamicContextReactionMode.Auto,
    updateId: "alarm-sync-42"));
```

Use `Apply()` only when an external system already owns the full context text. It bypasses the local tracker, does not support pre-conversation queueing, and does not make values available through `TryGetStateValue`.

## Acknowledgements

Convai can acknowledge a `context-update` with token and response-decision metadata. Subscribe to `ConvaiManager.Events.OnDynamicContextUpdateResultReceived` to inspect `Status`, `UpdateId`, `ContextRevision`, token counts, requested and actual `run_llm`, downgrade reason, interruption status, LLM trigger status, prompt rebuild status, and raw extras.

## Next steps

{% content-ref url="dynamic-context-scripting-api.md" %}
[Dynamic context scripting API](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}
