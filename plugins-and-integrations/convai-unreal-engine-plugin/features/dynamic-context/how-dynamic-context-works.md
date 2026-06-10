---
title: How dynamic context works
description: Understand how dynamic context tracks runtime state, batches events, chooses response behavior, and assembles payloads for Convai.
last_reviewed: "4.0.0-beta.21"
---

Dynamic context is how a Convai character learns about runtime information that was not available — or had not yet occurred — when the session started. You push updates from Blueprint; the plugin stores them locally, batches rapid changes, and sends assembled payloads to Convai.

Think of dynamic context as two channels:

| Channel | What it represents | Blueprint node | Example |
|---|---|---|---|
| State | A current fact that can be replaced | `Set Context State` / `Set Context States` | `Health` is `80` |
| Event | A one-time moment in the session | `Add Context Event` | `Alarm triggered in sector 4` |

## State properties and events

A **state property** is a named key-value pair that represents a current, replaceable fact — `Health` is `80`, `Zone` is `Market District`, `QuestActive` is `true`. `Set Context State` and `Set Context States` write through to the local tracker immediately. At flush time the plugin sends one `Replace`-mode `context-update` whose text is the canonical context, optionally followed by delta lines on the next line.

An **event** is a free-form chronological string — `Player picked up the red key`, `Alarm triggered in sector 4`. `Add Context Event` stages the text in the pending batch. At flush, the event is committed to the tracker's chronological event list and included in canonical context. Regular context events are not duplicated into a separate delta line.

| Channel | Replaceable | Typical use |
|---|---|---|
| State property | Yes — latest value only | Current health, zone, equipment loadout |
| Event | No — append-only | Alarms, milestones, one-time narrative beats |

## What the character receives

At flush time, the plugin assembles a newline-separated context string from all active states and events:

```text
{StateName} is {Value}
{AnotherState} is {Value}
Event text line one
Event text line two
```

States appear first, in insertion order. Updating a value does not move its position. Events follow in chronological order.

```text
// Blueprint pseudocode — insertion order is preserved when a state is updated
Set Context State  Name="Zone"   Value="Market District"   ShouldRespond=Never
Set Context State  Name="Health" Value="80"                ShouldRespond=Never
Add Context Event  Text="Player picked up the red key"     ShouldRespond=Auto
Set Context State  Name="Zone"   Value="Docks"             ShouldRespond=Never
```

Canonical context after all four calls:

```text
Zone is Docks
Health is 80
Player picked up the red key
```

You supply names, values, and event text. The plugin assembles and delivers the canonical string at flush time.

## Debounce batching

Calls to `Set Context State`, `Set Context States`, and `Add Context Event` schedule a debounced flush rather than sending immediately. `Remove Context State` schedules a debounced flush only when the key exists in the local tracker.

Rapid updates within a short window coalesce into one send. Two properties on `UConvaiChatbotComponent` control timing:

| Property | Details panel label | Default | Meaning |
|---|---|---|---|
| `ContextDebounceWindow` | `Context Debounce Window (s)` | `0.5` | After the most recent staged update, wait this many seconds before flushing. Each new update within the window resets the timer. |
| `ContextMaxDebounceWindow` | `Max Debounce Window (s)` | `3.0` | Hard ceiling on total delay from the first update of a burst. Prevents an unbroken stream of updates from postponing the flush indefinitely. |

The debounce timer starts when the first update in a burst arrives. Subsequent updates reset the timer to `ContextDebounceWindow` from the most recent call, but never extend past `ContextMaxDebounceWindow` from the burst start. When the timer fires, all staged changes combine into a single `context-update` message.

Both properties are marked `Advanced Display` under `Convai > DynamicContext` in the Details panel.

## When the character may respond

Each staged state or event carries its own `ShouldRespond` value. The batch merges them into one aggregate rank: `Always` > `Auto` > `Never`. The flush sends a single `context-update` with that aggregate value as `run_llm`.

The aggregate rank controls whether state delta lines are emitted:

- **Aggregate `Never`** — no delta lines. New state keys enter canonical immediately so Convai retains them.
- **Aggregate `Auto` or `Always`** — delta lines are appended after the canonical block (separated by a single newline). Brand-new state keys in the batch are excluded from canonical on that flush and appear only as delta lines; they enter canonical on the next flush.

Per-key `ShouldRespond` on individual calls still contributes to the aggregate rank, but first-appearance deferral applies to every new state key in the batch when aggregate is not `Never`.

## Immediate flushing

Every mutation function exposes an `Advanced` parameter `bFlushImmediately`. When `true`, the plugin calls `FlushDynamicContext()` in the current frame, bypassing the debounce timer. Use this only for time-critical updates after the chatbot is connected. High-frequency use can send one `context-update` per call when connected with staged work.

`Reset Dynamic Context` does not expose `bFlushImmediately`. When the character is connected, it calls the flush path immediately; when offline, it queues the reset for the next post-connect flush.

## Pre-session queueing

Default debounced calls made before `IsChatbotConnected()` returns `true` accumulate in `PendingContextBatch`. `TickDynamicContext()` returns early while disconnected, so no messages are sent. After the session connects, the next tick that reaches the debounce deadline calls `FlushDynamicContext()` and delivers the pending batch as one `Replace`-mode snapshot. Do not use `bFlushImmediately = true` before connection for data that must be delivered, because it bypasses the disconnected tick guard.

You can populate initial state from `BeginPlay` without deferred execution or connection guards:

```text
// Blueprint pseudocode — safe to call from BeginPlay before Start Session
Event BeginPlay
  → Set Context State  Name="Facility"  Value="Offshore Platform Alpha"  ShouldRespond=Never
  → Set Context State  Name="Scenario"  Value="Fire Drill"               ShouldRespond=Never
  → Add Context Event  Text="Session initialized"                         ShouldRespond=Never
```

## Reset ordering

`Reset Dynamic Context` marks `bPendingReset` on the pending batch. When connected, it flushes immediately; when disconnected, it schedules the reset for the next post-connect flush. It does **not** clear the tracker or discard staged updates up front. On flush:

1. Staged states, events, and optional attention are sent as one `Replace` `context-update`.
2. Pending environment metadata drains if queued. Queued narrative triggers that already existed when `Reset Dynamic Context` was called were cleared by that reset request; triggers queued after a pending offline `Reset` can still drain before the `Reset`.
3. A `Reset` `context-update` fires last (`mode: reset`, `run_llm: "false"`, no `text` field for the empty `Reset` payload), then the local tracker is cleared.

If you call `Reset Dynamic Context` and stage new updates in the same offline window, the first post-connect flush delivers the staged content first, then the `Reset` clears remote and local context. Let the reset flush complete before staging fresh data when you intend to start from an empty dynamic layer.

## Event deduplication within a batch

Identical event strings staged multiple times within the same debounce window are deduplicated — only the first occurrence is kept for that flush. Different event strings in the same burst are all retained in chronological order.

## Dynamic environment info is a separate lane

`DynamicEnvironmentInfo` is a `FString` property on `UConvaiChatbotComponent`. Changing it calls `update-dynamic-info` with `dynamic_info.text` when a session proxy exists, and the value is also sent on attendee connect. It is not tracked by `FConvaiDynamicContextTracker` and does not pass through the debounce batch. See [Static context at connection time](static-context-at-connection-time.md).

## When to use which function

| Goal | Use |
|---|---|
| Track one current condition | `Set Context State` |
| Track several conditions that change together | `Set Context States` |
| Record that something happened | `Add Context Event` |
| Remove a condition that no longer applies | `Remove Context State` |
| Clear all runtime context | `Reset Dynamic Context` |
| Send externally constructed context text | `Update Context` — bypasses the tracker |
| Push session-level free-form notes | `DynamicEnvironmentInfo` — separate `update-dynamic-info` lane |

## Next steps

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-quick-start.md" %}
[Dynamic context quick start](dynamic-context-quick-start.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-blueprint-reference.md" %}
[Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}
