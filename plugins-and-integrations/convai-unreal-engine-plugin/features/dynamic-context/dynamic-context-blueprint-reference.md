---
title: Dynamic context Blueprint reference
description: Reference the Blueprint controls that send runtime state, event, reset, and timing updates from an Unreal character to Convai during a live session.
last_reviewed: "4.0.0-beta.21"
---

Most dynamic context functions are exposed on `UConvaiChatbotComponent` (Blueprint display name **Convai Chatbot**) under the `Convai|DynamicContext` category. `Update Context` is an advanced direct `context-update` node in the `Convai` category; it bypasses the tracked state/event helper API. Properties appear under **Convai > DynamicContext** (debounce settings) and **Convai** (`DynamicEnvironmentInfo`) in the Details panel.

Source of truth: `Source/Convai/Public/ConvaiChatbotComponent.h`, `Source/Convai/Private/ConvaiChatbotComponent.cpp`, `Source/Convai/Public/DynamicContext/`, and `Source/Convai/Private/ConvaiSubsystem.cpp`.

## Functions

### `Set Context State`

Sets a single state property in the dynamic context. If a property with the same `Name` already exists, its value is replaced.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Name` | `FString` | — | Key identifying this state property. Case-sensitive. |
| `Value` | `FString` | — | Current value of the state property. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | Contributes to batch aggregate `run_llm`. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass debounce and run the flush path in the current frame. Use after connection for data that must be delivered. |

**Flush behavior:** One Replace `context-update`. New keys enter canonical when aggregate is `Never`; otherwise new keys are deferred to delta lines on first flush. Updated keys always appear in canonical; delta lines describe the transition when aggregate is not `Never`.

**Pre-session:** With default debounce, stages safely and flushes after the session connects and the debounce deadline elapses. Do not use `bFlushImmediately = true` before connection for data that must be delivered.

---

### `Set Context States`

Sets multiple state properties at once. All keys share one canonical rebuild and one flush.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `States` | `TMap<FString, FString>` | — | Map of key-value state properties to set or update. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | Contributes to batch aggregate `run_llm` for all supplied keys. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass debounce and run the flush path in the current frame. Use after connection for data that must be delivered. |

**Behavior:** Empty maps are ignored. Aggregate `ShouldRespond` merges with any other staged items in the same debounce window (`Always` > `Auto` > `Never`).

**Pre-session:** With default debounce, stages safely and flushes after the session connects and the debounce deadline elapses. Do not use `bFlushImmediately = true` before connection for data that must be delivered.

---

### `Add Context Event`

Appends a chronological event string to the dynamic context.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Text` | `FString` | — | Event description to append. |
| `ShouldRespond` | `EC_RunLLMOption` | `Auto` | Contributes to batch aggregate `run_llm`. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass debounce and run the flush path in the current frame. Use after connection for data that must be delivered. |

**Behavior:** Identical `Text` values staged multiple times in the same debounce window are deduplicated. At flush, the event is committed to the tracker and included in canonical. Regular context events are not duplicated into a separate delta line.

**Pre-session:** With default debounce, stages safely and flushes after the session connects and the debounce deadline elapses. Do not use `bFlushImmediately = true` before connection for data that must be delivered.

---

### `Remove Context State`

Removes a state property from the dynamic context and rebuilds canonical context without it.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Name` | `FString` | — | Key to remove. Case-sensitive. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass debounce and run the flush path in the current frame. Use after connection for data that must be delivered. |

**Returns:** Nothing. If `Name` does not exist, the call is a no-op.

**Behavior:** Sets `bForceReplace` on the pending batch so the flush sends updated canonical context without the removed key. No delta lines are added.

**Pre-session:** With default debounce, stages safely and flushes after the session connects and the debounce deadline elapses. Do not use `bFlushImmediately = true` before connection for data that must be delivered.

---

### `Reset Dynamic Context`

Clears all tracked state properties and events and resets remote context.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| — | — | — | No parameters. |

**Behavior:** Marks `bPendingReset`. Does not clear the tracker or discard staged updates up front. On flush: staged batch drains first, then a Reset `context-update` fires (`mode: reset`, `run_llm: "false"`, with `text` omitted for the empty Reset payload), then the local tracker is cleared. Clears `PendingTriggers` when the reset is requested. When connected, calls the flush path immediately; when offline, queues until the first post-connect flush.

---

### `Get Context State Value`

Returns the current client-side value of a tracked state property. Reads from the local tracker — does not query Convai.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Direction | Type | Default | Description |
|---|---|---|---|---|
| `Name` | In | `FString` | — | Key to look up. Case-sensitive. |
| `OutValue` | Out | `FString` | — | Current value if the key exists. |
| Return value | Return | `bool` | — | `true` if the key was found. |

---

### `Update Context`

Advanced direct node. Sends a raw `context-update` with explicit `Text`, `Mode`, and `ShouldRespond`. Staged state/event flushes use the same transport message type during `FlushDynamicContext()` without updating the tracker through this node. `Reset Dynamic Context` uses the same C++ `UpdateContext` send path for the reset message.

**Blueprint category:** `Convai`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Text` | `FString` | — | Context text to apply. Optional when `Mode` is `Reset`. |
| `Mode` | `EC_ContextUpdateMode` | `Append` | How the context is applied: `Append`, `Replace`, or `Reset`. |
| `ShouldRespond` | `EC_RunLLMOption` | `Auto` | Maps to `run_llm` on the wire. |

Use `Update Context` only when the tracked node family does not cover your format requirements. It does not update `FConvaiDynamicContextTracker`, so `Get Context State Value` cannot read values sent only through this node. Pass an empty string when `Mode` is `Reset`; the SDK omits `text` only for an empty Reset payload.

## Default ShouldRespond reference

| Function | Default `ShouldRespond` |
|---|---|
| `Set Context State` | `Never` |
| `Set Context States` | `Never` |
| `Add Context Event` | `Auto` |
| `Remove Context State` | _(no `ShouldRespond` parameter)_ |
| `Reset Dynamic Context` | _(Reset always uses `Never` on the wire)_ |
| `Update Context` | `Auto` |

## Properties

### `ContextDebounceWindow`

| Details panel label | Context Debounce Window (s) |
|---|---|
| Type | `float` |
| Default | `0.5` |
| Clamp | ≥ `0.1` |
| Category | `Convai|DynamicContext` (Advanced Display) |

Seconds to wait after the most recent staged context update before flushing. Each new update within the window resets this timer.

---

### `ContextMaxDebounceWindow`

| Details panel label | Max Debounce Window (s) |
|---|---|
| Type | `float` |
| Default | `3.0` |
| Clamp | ≥ `0.1` |
| Category | `Convai|DynamicContext` (Advanced Display) |

Upper bound on how long the first update in a debounce burst can be delayed. Must be ≥ `ContextDebounceWindow`; smaller values are clamped at flush time.

---

### `DynamicEnvironmentInfo`

| Details panel label | Dynamic Environment Info |
|---|---|
| Type | `FString` |
| Default | `""` |
| Category | `Convai` |

Free-form text sent through `update-dynamic-info` on attendee connect and when the property changes on a connected session. Not tracked by `FConvaiDynamicContextTracker`. For runtime-changing facts, use `Set Context State`.

## Enums

### `EC_RunLLMOption`

Controls whether Convai generates a spoken response after receiving a context update.

| Enumerator | Blueprint display name | Wire string (`run_llm`) | Behavior |
|---|---|---|---|
| `EC_RunLLMOption::Auto` | Auto | `"auto"` | Sends the update with automatic response handling requested. |
| `EC_RunLLMOption::Always` | Always | `"true"` | Sends the update with response handling requested. |
| `EC_RunLLMOption::Never` | Never | `"false"` | Sends the update without response handling requested. |

---

### `EC_ContextUpdateMode`

Controls how a context string is applied when calling `Update Context` directly.

| Enumerator | Blueprint display name | Wire value (`mode`) | Behavior |
|---|---|---|---|
| `EC_ContextUpdateMode::Append` | Append | `append` | Text is appended to existing context. |
| `EC_ContextUpdateMode::Replace` | Replace | `replace` | Full context is replaced with the supplied text. |
| `EC_ContextUpdateMode::Reset` | Reset | `reset` | Context is cleared. Pass empty `Text` for the standard Reset payload. |

## Transport messages

### `context-update`

Sent by `UConvaiSubsystem::UpdateContext` for tracked dynamic context flushes and direct `Update Context` calls.

| JSON field | Description |
|---|---|
| `mode` | `append`, `replace`, or `reset` |
| `run_llm` | String value `"auto"`, `"true"`, or `"false"` |
| `text` | Assembled context string; omitted on empty Reset |
| `current_attention_object` | Optional attention object name when attention is folded into the flush |

Tracked flushes from `FlushDynamicContext` always use `mode: replace` for staged batch content.

### `update-dynamic-info`

Sent by `UpdateDynamicInfo` for `DynamicEnvironmentInfo` changes and on attendee connect.

| JSON field | Description |
|---|---|
| `dynamic_info.text` | Free-form environment text |

## Connection helper

| Function | Category | Description |
|---|---|---|
| `Get Chatbot Connection State` | `Convai|Connection` | Returns `EC_ConnectionState` (`Disconnected`, `Connecting`, `Connected`, `Reconnecting`) for the chatbot session. |

## Next steps

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
