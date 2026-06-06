---
title: Sync behavior and timing
description: Understand the RTVI payload sent at each debounce flush, the first-appearance deferral rule, and how pre-session updates reach Convai at connection time.
last_reviewed: "4.0.0-beta.21"
---

Every batched context flush in the Convai Unreal Engine plugin produces exactly one Replace-mode RTVI message sent to Convai. This page explains the structure of that payload, how each operation type contributes to it, why new states are handled differently from existing ones on their first flush, and how updates made before a session connects are delivered at connection time.

## Flush payload structure

Each flush produces a single Replace-mode message. The message body has two optional blocks separated by a blank line:

```text
{StateName} is {Value}
{AnotherState} is {Value}
Event text line one

StateName changed from OldValue to NewValue
```

The first block is the **canonical context** — a newline-joined string of all active states in insertion order (`"{Key} is {Value}"` per line) followed by all events in chronological order. It is built by `FConvaiDynamicContextTracker::BuildCanonicalContext()`.

The second block, when present, contains **delta lines** — human-readable change descriptions appended after the blank line separator. Delta lines surface only when `AggregateRunLLM` is not `Never`. They appear after the canonical block so the LLM sees them at the tail of the prompt.

This is a single Replace-mode message, not two messages. Developers familiar with the Unity SDK, which sends separate Append and Replace messages for the same operation, should expect one consolidated payload here.

## Scenarios during an active session

The eight sections below map each operation to the exact message it produces during a connected session.

### New state — ShouldRespond = Never

**Triggering call:** `SetContextState` or `SetContextStates` with a key that has not been set before, and `ShouldRespond` is `Never`.

The new key enters canonical immediately. No delta lines are added.

```text
// Canonical context (new key included):
Facility is Offshore Platform Alpha
```

### New state — ShouldRespond = Auto or Always

**Triggering call:** `SetContextState` or `SetContextStates` with a new key, and `ShouldRespond` is `Auto` or `Always`.

On this first flush, the new key is **excluded** from canonical. A delta line describing the new state is appended after the canonical block instead.

```text
// Canonical context (new key absent):
Zone is Market District

// Delta block:
Health is 50
```

On the **next flush**, the key enters canonical normally. No further deferral occurs.

{% hint style="info" %}
The reason new states are excluded from canonical on their first flush is prompt placement. When the LLM needs to generate a response that references a change, surfacing that change at the tail of the prompt — in the delta block — produces more reliable responses than burying the new fact inside the canonical block alongside established background context. Once the state is established, it belongs in canonical with the other background facts and no longer needs special handling.
{% endhint %}

### Update to existing state — ShouldRespond = Never

**Triggering call:** `SetContextState` on a key that already exists, with `ShouldRespond` set to `Never`.

The updated value enters canonical. No delta lines are added.

```text
// Canonical context (updated value):
Zone is Docks
```

### Update to existing state — ShouldRespond = Auto or Always

**Triggering call:** `SetContextState` on an existing key, with `ShouldRespond` set to `Auto` or `Always`.

The updated value enters canonical. A delta line describing the transition is appended.

```text
// Canonical context (updated value):
Zone is Docks

// Delta block:
Zone changed from Market District to Docks
```

### Multiple states at once

**Triggering call:** `SetContextStates` with a map of key-value pairs, potentially mixing new and existing keys.

All values are written to the tracker. First-appearance deferral applies per key: new keys with `ShouldRespond` set to `Auto` or `Always` are excluded from canonical and appear as delta lines; existing keys with `ShouldRespond` set to `Auto` or `Always` appear in both canonical and the delta block. All changes are aggregated into one flush — one Replace-mode message.

```text
// Canonical context (existing keys updated; new key deferred):
Zone is Docks
Scenario is Active

// Delta block:
Zone changed from Market District to Docks
Difficulty is Hard
```

### Add context event

**Triggering call:** `AddContextEvent`.

Events are never subject to first-appearance deferral. The event text is appended to the tracker's chronological event list, so it appears in canonical. A duplicate of the event text also appears as a delta line to surface it prominently at the tail of the prompt.

```text
// Canonical context (event included in the events block):
Zone is Docks
Player reached the extraction point

// Delta block:
Player reached the extraction point
```

### Remove context state

**Triggering call:** `RemoveContextState`.

The key is removed from the tracker. `PendingContextBatch.bForceReplace` is set to `true`, producing a Replace containing the updated canonical without the removed key. No delta lines are added for removals.

```text
// Canonical context (removed key absent):
Zone is Docks
```

### Reset dynamic context

**Triggering call:** `ResetDynamicContext`.

The local tracker is cleared via `FConvaiDynamicContextTracker::Reset()`. `PendingTriggers` is also cleared. A Reset-mode message is sent — the message text is ignored by Convai; only the mode matters.

When the character is connected, the Reset fires immediately. When the character is not connected, the Reset is queued and fires at connect time before any other context.

## Pre-session queuing

All mutation calls — `SetContextState`, `SetContextStates`, `AddContextEvent`, `RemoveContextState`, and `ResetDynamicContext` — accumulate in `PendingContextBatch` when `IsChatbotConnected()` returns `false`. No messages are sent while the session is offline.

`TickDynamicContext()` checks `IsChatbotConnected()` each frame. When the session connects, the next tick calls `FlushDynamicContext()` and delivers the pending batch.

At that point, the pending batch collapses into one authoritative Replace-mode snapshot. The individual staged changes are not replayed as a sequence — Convai receives only the current canonical state.

```text
// BeginPlay — all three queue safely before the session connects
Set Context State  Name="Facility"  Value="Offshore Platform Alpha"
Set Context State  Name="Scenario"  Value="Fire Drill"
Add Context Event  Text="Session initialized"

// Character receives at connect — one Replace-mode message:
// Facility is Offshore Platform Alpha
// Scenario is Fire Drill
// Session initialized
```

If `ResetDynamicContext` was called while offline, a Reset-mode message is sent at connect time before any other context. If both a reset and subsequent changes are pending, the reset fires first, then the follow-up flush delivers the post-reset state.

## bFlushImmediately

Each mutation function — `SetContextState`, `SetContextStates`, `AddContextEvent`, `RemoveContextState` — exposes an **Advanced** parameter called `bFlushImmediately`. When set to `true`, the function calls `FlushDynamicContext()` in the current frame, bypassing the debounce timer entirely.

Use `bFlushImmediately` only for time-critical updates where the debounce delay would cause a perceptible lag: scene transitions, dramatic narrative beats, or safety-critical state changes. Each call with `bFlushImmediately = true` sends one Replace-mode RTVI message to Convai. Calling it on every tick therefore generates one message per frame — avoid this pattern.

`ResetDynamicContext` always flushes immediately when the character is connected. It has no debounce option.

{% hint style="warning" %}
High-frequency use of `bFlushImmediately` — for example, syncing a value that updates every frame — generates a message-per-frame to Convai. Use the default debounce behavior for values that change continuously, and reserve `bFlushImmediately` for discrete, low-frequency events.
{% endhint %}

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-blueprint-reference.md" %}
[Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md)
{% endcontent-ref %}
