---
title: How dynamic context works
description: Understand state properties, event strings, the debounce window, and the ShouldRespond modes in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

Dynamic context is the mechanism by which `UConvaiChatbotComponent` keeps Convai informed of runtime information that was not available — or had not yet occurred — when the session started. It has two channels: state properties and events. Both are batched by a debounce timer before being sent to Convai.

## State properties

A state property is a named key-value pair that represents a current, replaceable fact about the world — "Health" is `80`, "Zone" is `"Market District"`, "QuestActive" is `"true"`. The client-side tracker (`FConvaiDynamicContextTracker`) holds all current states in an insertion-ordered map: `SetState` adds or replaces the value for a given key, `RemoveState` deletes it, and `BuildCanonicalContext` assembles the full context string from all active states and events in the order they were added.

When `SetContextState` is called, the plugin records the new value in the tracker and schedules a flush. At flush time, the plugin sends the full canonical context — all current states plus the change message describing what changed — to Convai using the `UpdateContext` node's `Replace` mode so the entire context snapshot is consistent.

Sending a state update with `ShouldRespond = Never` (the default) silently updates Convai's view without triggering a spoken response. Use this for background facts the character should know but does not need to comment on.

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

{% hint style="info" %}
Both `ContextDebounceWindow` and `ContextMaxDebounceWindow` are marked **Advanced Display** in the Details panel. Expand the **Advanced** section of the `Convai|DynamicContext` category to access them.
{% endhint %}

## The bFlushImmediately parameter

Every mutation function (`SetContextState`, `SetContextStates`, `AddContextEvent`, `RemoveContextState`) exposes an **Advanced** parameter `bFlushImmediately`. When `true`, the plugin bypasses the debounce timer and sends the update in the current frame. Use this only for time-critical updates, such as a scene transition or a dramatic narrative beat — high-frequency calls with `bFlushImmediately = true` spam the WebRTC channel.

`ResetDynamicContext` always flushes immediately; it has no debounce option.

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

## Next steps

- [Static context at connection time](static-context-at-connection-time.md) — understand what data is frozen at session start.
- [Quick start](quick-start.md) — push your first state update and event in a working Blueprint.
- [Dynamic context Blueprint reference](dynamic-context-blueprint-reference.md) — complete function and property reference.
