---
title: Sync behavior and timing
description: Understand how dynamic context payloads flush after debounce, how offline queueing works, and when immediate flushes bypass batching.
last_reviewed: "4.0.0-beta.21"
---

Dynamic context updates do not send to Convai on every Blueprint call. By default, the plugin waits briefly so rapid changes can merge into one send. This page explains when flushes happen, what each flush contains, and when to bypass the debounce timer.

## When updates send

| Situation | What happens |
|---|---|
| Default debounced call while connected | Updates stage locally; one `Replace` `context-update` sends after `ContextDebounceWindow` (default `0.5` s) with no new updates in the window |
| Rapid burst of updates | All changes in the burst coalesce into one flush; timer resets on each call but cannot exceed `ContextMaxDebounceWindow` (default `3.0` s) from the first update |
| `bFlushImmediately = true` after connect | `FlushDynamicContext()` runs in the current frame, bypassing debounce |
| Updates before session connects | Changes accumulate in `PendingContextBatch`; first flush after connect and debounce deadline |
| `Reset Dynamic Context` | Drains staged content first, then sends a `Reset` `context-update`, then clears the local tracker |

## Transport message shape

`UConvaiSubsystem::UpdateContext` sends a `context-update` message with a JSON data payload:

| JSON field | Values (wire format) | When present |
|---|---|---|
| `mode` | `append`, `replace`, `reset` | Present on every message |
| `run_llm` | `"auto"`, `"true"`, `"false"` | Present on every message — maps from `EC_RunLLMOption` (`Auto`, `Always`, `Never`) |
| `text` | Context string | Omitted on `Reset` when text is empty |
| `current_attention_object` | Object name string | When attention is folded into the same message |

Blueprint enum display names (`Append`, `Replace`, `Reset`, `Auto`, `Always`, `Never`) differ from the wire strings above.

## Flush payload structure

Each flush that includes staged states or events builds one text payload:

```text
{StateName} is {Value}
{AnotherState} is {Value}
Event text line one
{Key} changed from {OldValue} to {NewValue}
{NewKey} is {NewValue}
```

The first block is **canonical context** — states in insertion order (`"{Key} is {Value}"` per line) followed by events in chronological order. It is built by `FConvaiDynamicContextTracker::BuildCanonicalContext()`.

When the batch's aggregate `ShouldRespond` is not `Never` and state delta lines exist, the plugin appends them on the **next line** after canonical context (one `\n` separator, not a blank line). Delta lines surface state changes at the tail of the prompt.

For state updates where the new value has more than three whitespace-separated words, the delta line uses `"{Key} changed from {OldValue}"` without repeating the long new value.

## Scenarios during an active session

### New state — aggregate `ShouldRespond` is `Never`

**Triggering call:** `Set Context State` or `Set Context States` with a key that has not been set before, and every staged item in the batch keeps aggregate `ShouldRespond` at `Never`.

The new key enters canonical immediately. No delta lines are added.

```text
Facility is Offshore Platform Alpha
```

### New state — aggregate `ShouldRespond` is `Auto` or `Always`

**Triggering call:** `Set Context State` or `Set Context States` with a new key, and at least one staged item raises aggregate `ShouldRespond` to `Auto` or `Always`.

On this flush, the new key is **excluded** from canonical. A delta line such as `Health is 50` is appended after the canonical block.

```text
Zone is Market District
Health is 50
```

On the **next flush**, the key enters canonical normally.

### Update to existing state — aggregate `ShouldRespond` is `Never`

**Triggering call:** `Set Context State` with an existing key, and the batch keeps aggregate `ShouldRespond` at `Never`.

The updated value enters canonical. No delta lines are added.

```text
Zone is Docks
```

### Update to existing state — aggregate `ShouldRespond` is `Auto` or `Always`

**Triggering call:** `Set Context State` with an existing key, and at least one staged item raises aggregate `ShouldRespond` to `Auto` or `Always`.

The updated value enters canonical. A delta line describing the transition is appended.

```text
Zone is Docks
Zone changed from Market District to Docks
```

### Multiple states at once

**Triggering call:** `Set Context States` with a map of key-value pairs, potentially mixing new and existing keys.

All values are written to the tracker. First-appearance deferral applies per new key when aggregate is not `Never`. All changes share one flush — one `Replace` `context-update`.

```text
Zone is Docks
Scenario is Active
Zone changed from Market District to Docks
Difficulty is Hard
```

### Add context event

**Triggering call:** `Add Context Event`.

The event text is committed to the tracker's event list and appears in canonical. Regular context events are not duplicated into a separate delta line.

Identical event strings staged multiple times in the same debounce window are deduplicated — only the first occurrence is kept for that flush.

```text
Zone is Docks
Player reached the extraction point
```

### Remove context state

**Triggering call:** `Remove Context State`.

The key is removed from the tracker. `bForceReplace` is set so the flush sends canonical context without the removed key. No delta lines are added for removals.

### Dynamic context reset

**Triggering call:** `Reset Dynamic Context`.

The plugin drains any staged context batch first, then sends a `Reset` `context-update` (`mode: reset`, `run_llm: "false"`) with no `text` field for the empty `Reset` payload. The local tracker is cleared after the `Reset` message.

Queued triggers that already exist when `Reset Dynamic Context` is called are cleared immediately. Triggers queued after a pending offline `Reset` may still drain before the `Reset` during `FlushDynamicContext()`.

When connected, `Reset Dynamic Context` calls the flush path immediately. When offline, the reset flag waits for the first post-connect flush.

## Pre-session queueing

Default debounced mutation calls — `Set Context State`, `Set Context States`, `Add Context Event`, `Remove Context State`, and `Reset Dynamic Context` — accumulate in `PendingContextBatch` while `IsChatbotConnected()` is `false`.

`TickDynamicContext()` keeps accumulating until the session connects. When connected and the debounce deadline is reached, `FlushDynamicContext()` delivers the pending batch.

Offline updates collapse into the flush behavior described above — not replayed as a sequence of individual messages. After connection, on the first tick where the debounce deadline has elapsed, a batch whose aggregate `ShouldRespond` remains `Never` sends the current canonical snapshot from the tracker; batches with aggregate `Auto` or `Always` follow the canonical-plus-delta behavior described above. Any pending `Reset` clears context last.

```text
// BeginPlay — all three queue safely before the session connects
Set Context State  Name="Facility"  Value="Offshore Platform Alpha"
Set Context State  Name="Scenario"  Value="Fire Drill"
Add Context Event  Text="Session initialized"  ShouldRespond=Never

// After connection and the debounce deadline — one Replace context-update, then Reset if queued:
// Facility is Offshore Platform Alpha
// Scenario is Fire Drill
// Session initialized
```

If `Reset Dynamic Context` and subsequent updates are all pending offline, the flush sends staged content first, then `Reset` last.

{% hint style="warning" %}
Do not use `bFlushImmediately = true` before connection for context that must be delivered. Immediate flush bypasses the disconnected tick guard and can clear staged work before a valid session can send it.
{% endhint %}

## `bFlushImmediately`

Each mutation function — `Set Context State`, `Set Context States`, `Add Context Event`, `Remove Context State` — exposes an **`Advanced`** parameter `bFlushImmediately`. When `true`, `FlushDynamicContext()` runs in the current frame.

Use `bFlushImmediately` for time-critical updates where the default debounce delay would cause perceptible lag. Each immediate call runs `FlushDynamicContext()` in the current frame and sends a `context-update` when the chatbot is connected with deliverable staged work. Avoid calling it every tick on continuously changing values.

`Reset Dynamic Context` calls the flush path immediately when connected. It has no `bFlushImmediately` parameter.

{% hint style="warning" %}
High-frequency use of `bFlushImmediately` — for example, syncing a value that updates every frame — can generate one `context-update` per call when connected. Use the default debounce behavior for continuously changing values.
{% endhint %}

## Next steps

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-blueprint-reference.md" %}
[Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md)
{% endcontent-ref %}
