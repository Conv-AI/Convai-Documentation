---
title: How dynamic context works
description: Understand state properties, events, canonical context format, the debounce window, pre-session queuing, and ShouldRespond modes.
last_reviewed: "4.0.0-beta.21"
---

Dynamic context is the mechanism by which `UConvaiChatbotComponent` keeps Convai informed of runtime information that was not available — or had not yet occurred — when the session started. It has two channels: state properties and events. Both are batched by a debounce timer before being sent to Convai.

## State properties

A state property is a named key-value pair that represents a current, replaceable fact about the world — "Health" is `80`, "Zone" is `"Market District"`, "QuestActive" is `"true"`. The client-side tracker (`FConvaiDynamicContextTracker`) holds all current states in an insertion-ordered map: `SetState` adds or replaces the value for a given key, `RemoveState` deletes it, and `BuildCanonicalContext` assembles the full context string from all active states and events in the order they were added.

When `SetContextState` is called, the plugin records the new value in the tracker and schedules a flush. At flush time, the plugin sends a single Replace-mode message whose text is the full canonical context with an optional delta block appended after a blank line.

- For `ShouldRespond = Never`: the new key enters canonical directly. No delta lines are added.
- For `ShouldRespond = Auto` or `Always`: a brand-new state key is excluded from canonical on its first flush and appears only as a delta line at the payload tail. On the next flush, the key enters canonical normally.
- For an update to an existing key: the updated value appears in canonical, and a delta line such as `"Zone changed from Market District to Docks"` is appended.

{% hint style="info" %}
The reason a newly-set state with `Auto` or `Always` is surfaced as a delta line rather than silently absorbed into canonical is prominence: the LLM sees the delta line directly at the tail of the prompt, making it clear a notable change just occurred. Once the state is established and the LLM has acknowledged it, it belongs in canonical alongside the other background facts.
{% endhint %}

Sending a state update with `ShouldRespond = Never` (the default) silently updates Convai's view without triggering a spoken response. Use this for background facts the character should know but does not need to comment on.

## Canonical context format

When the plugin sends an update to Convai, `FConvaiDynamicContextTracker::BuildCanonicalContext` assembles a canonical string from all tracked states and events. States appear first, in insertion order; events follow in chronological order.

```text
{StateName} is {Value}
{AnotherState} is {Value}
Event text line one
Event text line two
```

Updating a state's value does not change its position in the canonical context. The reason states preserve insertion order is to give the character a stable, predictable view of the world. The canonical string is assembled automatically at flush time by `FConvaiDynamicContextTracker::BuildCanonicalContext`.

**Example — insertion order is preserved when a state is updated:**

```text
// Blueprint pseudocode — insertion order is preserved when a state is updated
Set Context State  Name="Zone"   Value="Market District"   → position 1
Set Context State  Name="Health" Value="80"                → position 2
Add Context Event  Text="Player picked up the red key"
Set Context State  Name="Zone"   Value="Docks"             → updates value; position stays at 1
```

Canonical context after all four calls:

```text
Zone is Docks
Health is 80
Player picked up the red key
```

You supply only names, values, and event text. The plugin assembles and delivers the canonical string automatically at flush time.

## Event strings

An event is a free-form chronological string — "Player picked up the red key", "Alarm triggered in sector 4", "Player entered the restricted area". Events are appended in order and never replaced. The `FConvaiDynamicContextTracker` stores them in a chronological list; `BuildCanonicalContext` emits all events after the state block.

`AddContextEvent` adds one event string and schedules a flush. Unlike state properties, events are not deduplicated — each call appends a new entry. Events default to `ShouldRespond = Auto`, which lets Convai decide whether the event warrants a spoken reaction.

## The debounce window

Every call to `SetContextState`, `SetContextStates`, `AddContextEvent`, or `RemoveContextState` schedules a debounced flush rather than sending immediately. Two properties on `UConvaiChatbotComponent` control the timing:

| Property | Details panel label | Default | Meaning |
|---|---|---|---|
| `ContextDebounceWindow` | Context Debounce Window (s) | `0.5` | After the most-recent staged update, wait this many seconds before flushing. Each new update within the window resets the timer. |
| `ContextMaxDebounceWindow` | Max Debounce Window (s) | `3.0` | Hard ceiling on the total delay from the first update of a burst. Prevents an unbroken stream of updates from postponing the flush indefinitely. |

The debounce timer starts when the first update in a burst arrives. Subsequent updates in the burst reset the timer back to `ContextDebounceWindow` from the most recent call, but never extend past `ContextMaxDebounceWindow` from the burst's start. When the timer fires, all staged updates are combined into a single `UpdateContext` call to Convai.

This coalescing behaviour keeps high-frequency update sources — animation ticks, rapidly changing health values, physics-driven state — from flooding the WebRTC channel with redundant messages.

Both `ContextDebounceWindow` and `ContextMaxDebounceWindow` are marked **Advanced Display** in the Details panel. Expand the **Advanced** section of the `Convai|DynamicContext` category to access them.

## The bFlushImmediately parameter

Every mutation function (`SetContextState`, `SetContextStates`, `AddContextEvent`, `RemoveContextState`) exposes an **Advanced** parameter `bFlushImmediately`. When `true`, the plugin bypasses the debounce timer and sends the update in the current frame. Use this only for time-critical updates, such as a scene transition or a dramatic narrative beat — high-frequency calls with `bFlushImmediately = true` spam the WebRTC channel.

`ResetDynamicContext` always flushes immediately; it has no debounce option.

## Pre-session queuing

Calls to `SetContextState`, `SetContextStates`, `AddContextEvent`, and `RemoveContextState` made before `StartSession` completes queue safely in the internal batch. The plugin's tick function (`TickDynamicContext`) checks the session connection state before each flush attempt. While the session is not yet connected, the batch accumulates without flushing. When the session becomes connected, the next tick fires `FlushDynamicContext` automatically, delivering all pending updates in a single Replace-mode payload.

The practical consequence: you can populate initial state freely from `BeginPlay` without needing deferred execution, guards, or delays. The character receives one authoritative snapshot at connect time rather than a stream of incremental updates.

```text
// Blueprint pseudocode — safe to call from BeginPlay before StartSession
Event BeginPlay
  → Set Context State  Name="Facility"  Value="Offshore Platform Alpha"  ShouldRespond=Never
  → Set Context State  Name="Scenario"  Value="Fire Drill"               ShouldRespond=Never
  → Add Context Event  Text="Session initialized"                         ShouldRespond=Never
  → Start Session   (or bAutoInitializeSession handles this automatically)
```

{% hint style="warning" %}
`ResetDynamicContext` called before connect clears the local tracker and discards any pending batch. If you call it to clean up from a previous scenario, call it before issuing fresh `SetContextState` or `AddContextEvent` calls so the new data is not discarded.
{% endhint %}

## ShouldRespond modes

The `EC_RunLLMOption` enum controls whether Convai generates a spoken response after receiving the context update:

| Value | Blueprint display name | Behavior |
|---|---|---|
| `EC_RunLLMOption::Auto` | Auto | Convai decides whether the update warrants a spoken reaction. Use for events that may or may not require a response. |
| `EC_RunLLMOption::Always` | Always | Convai always generates a spoken response after the update. Use for dramatic narrative beats that need an immediate reaction. |
| `EC_RunLLMOption::Never` | Never | Convai updates its context silently. No spoken response is triggered. Use for background facts and state bookkeeping. |

The default for `SetContextState` and `SetContextStates` is `Never` — most state changes are background bookkeeping. The default for `AddContextEvent` is `Auto` — events are usually narrative beats where a response is plausible but not mandatory.

## UpdateContext and DynamicEnvironmentInfo

`UpdateContext` is a lower-level node that accepts an explicit `Text` string, a `Mode` (`EC_ContextUpdateMode::Append`, `Replace`, or `Reset`), and a `ShouldRespond` option. The `SetContextState` family calls it internally. You can call it directly when you need precise control over the context text and update mode, for example when integrating a custom context format.

`DynamicEnvironmentInfo` is a `FString` property on `UConvaiChatbotComponent` that is sent with every request. It carries free-form text that is not tracked by the dynamic context tracker — it is frozen per-request, not batched and coalesced. Use the `SetContextState` family for runtime state that must arrive reliably through the debounce pipeline; use `DynamicEnvironmentInfo` only for static context text that applies for the entire session and does not change.

## When to use which function

| Goal | Use |
|---|---|
| Track one current condition | `Set Context State` |
| Track several conditions that change simultaneously | `Set Context States` — one canonical rebuild, one flush |
| Record that something happened | `Add Context Event` |
| Remove a condition that no longer applies | `Remove Context State` |
| Clear all runtime context | `Reset Dynamic Context` |
| Send externally constructed context text | `Update Context` — advanced; bypasses the tracker |

## Next steps

{% content-ref url="static-context-at-connection-time.md" %}
[Static context at connection time](static-context-at-connection-time.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-blueprint-reference.md" %}
[Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}
