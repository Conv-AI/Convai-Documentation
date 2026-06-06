---
title: Dynamic context Blueprint reference
description: Reference for every Blueprint node, property, and enum in the dynamic context system, including pre-session queueing behavior and defaults.
last_reviewed: "4.0.0-beta.21"
---

Most dynamic context functions are exposed on `UConvaiChatbotComponent` (Blueprint display name **Convai Chatbot**) under the `Convai|DynamicContext` category. `Update Context` is a lower-level node in the `Convai` category. Properties appear in the **Convai > DynamicContext** section of the Details panel.

## Functions

### Set Context State

Sets a single state property in the dynamic context. If a property with the same `Name` already exists, its value is replaced.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Name` | `FString` | — | The key identifying this state property. Case-sensitive. |
| `Value` | `FString` | — | The current value of the state property. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | Whether Convai generates a spoken response after the update. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass the debounce timer and flush in the current frame. |

**Behavior:** At flush time the plugin sends a single Replace-mode message. For a **new key with `ShouldRespond = Never`**: the key enters canonical immediately, no delta lines added. For a **new key with `ShouldRespond = Auto` or `Always`**: the key is excluded from canonical on its first flush and appears only as a delta line; it enters canonical on the next flush. For an **update to an existing key**: the updated value enters canonical and a `"Name changed from X to Y"` delta line is appended.

**Pre-session:** Updates staged before the session connects queue safely and flush automatically when the session becomes connected.

---

### Set Context States

Sets multiple state properties at once. When `ShouldRespond` is `Auto` or `Always`, the change messages for all supplied states are combined into a single append so only one LLM response is triggered.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `States` | `TMap<FString, FString>` | — | Map of key-value state properties to set or update. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | Whether Convai generates a spoken response after the update. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass the debounce timer and flush in the current frame. |

**Behavior:** All supplied states are applied to the tracker in one operation, producing a single canonical rebuild. When `ShouldRespond` is `Auto` or `Always`, change messages for all supplied states are combined into a single delta block so only one LLM response is triggered.

**Pre-session:** Updates staged before the session connects queue safely and flush automatically when the session becomes connected.

---

### Add Context Event

Appends a chronological event string to the dynamic context. Events are not deduplicated; each call adds a new entry.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Text` | `FString` | — | The event description to append. |
| `ShouldRespond` | `EC_RunLLMOption` | `Auto` | Whether Convai generates a spoken response after the event lands. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass the debounce timer and flush in the current frame. |

**Behavior:** The event is appended directly using the provided `ShouldRespond` option. Events are emitted after the state block in the canonical context string.

**Pre-session:** Updates staged before the session connects queue safely and flush automatically when the session becomes connected.

---

### Remove Context State

Removes a state property from the dynamic context and rebuilds the canonical context without it.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Name` | `FString` | — | The key to remove. Case-sensitive. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass the debounce timer and flush in the current frame. |

**Returns:** Nothing. If `Name` does not exist in the tracker, the call is a no-op.

**Pre-session:** Queues safely and flushes when connected. If the key was never set, this is a no-op with no network traffic.

---

### Reset Dynamic Context

Clears all tracked state properties and events and resets the remote context to empty.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| — | — | — | No parameters. |

**Behavior:** Always flushes immediately if the session is connected. If called before the session connects, the reset is scheduled and fires at connect time — discarding any pending staged updates. There is no debounce option for this node.

---

### Get Context State Value

Returns the current client-side value of a tracked state property. This node reads from the local tracker — it does not query Convai.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Direction | Type | Default | Description |
|---|---|---|---|---|
| `Name` | In | `FString` | — | The key to look up. Case-sensitive. |
| `OutValue` | Out | `FString` | — | The current value if the key exists. |
| Return value | Return | `bool` | — | `true` if the key was found; `false` if it does not exist in the tracker. |

---

### Update Context

Low-level node. Sends a context update to Convai with an explicit `Text` string, a `Mode`, and a `ShouldRespond` option. The `SetContextState` family calls this internally.

**Blueprint category:** `Convai`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Text` | `FString` | — | The context text to apply. Optional when `Mode` is `Reset`. |
| `Mode` | `EC_ContextUpdateMode` | `Append` | How the context should be applied: `Append`, `Replace`, or `Reset`. |
| `ShouldRespond` | `EC_RunLLMOption` | `Auto` | Whether Convai generates a spoken response. |

Use `Update Context` only when the `SetContextState` family does not cover your format requirements.

When `Mode` is `Reset`, the `Text` parameter is ignored — pass an empty string.

## Default ShouldRespond reference

| Function | Default ShouldRespond |
|---|---|
| `Set Context State` | `Never` |
| `Set Context States` | `Never` |
| `Add Context Event` | `Auto` |
| `Remove Context State` | _(no ShouldRespond parameter)_ |
| `Reset Dynamic Context` | _(always silent)_ |
| `Update Context` | `Auto` |

## Properties

### ContextDebounceWindow

| Details panel label | Context Debounce Window (s) |
|---|---|
| Type | `float` |
| Default | `0.5` |
| Clamp | ≥ `0.1` |
| Category | `Convai|DynamicContext` (Advanced Display) |

Time in seconds to wait after the most-recent staged context update before flushing the batch. Each new update within the window resets this timer.

---

### ContextMaxDebounceWindow

| Details panel label | Max Debounce Window (s) |
|---|---|
| Type | `float` |
| Default | `3.0` |
| Clamp | ≥ `0.1` |
| Category | `Convai|DynamicContext` (Advanced Display) |

Upper bound in seconds on how long the first update in a debounce burst can be delayed before a forced flush. Acts as a safety cap when updates arrive faster than `ContextDebounceWindow`. Must be ≥ `ContextDebounceWindow`; smaller values are clamped at flush time.

---

### DynamicEnvironmentInfo

| Details panel label | Dynamic Environment Info |
|---|---|
| Type | `FString` |
| Default | `""` |
| Category | `Convai` |

Free-form text sent with every voice or text request. Not tracked by the dynamic context tracker. Use it for session-level static notes. For runtime-changing facts, use `SetContextState` instead.

## Enums

### EC_RunLLMOption

Controls whether Convai generates a spoken response after receiving a context update.

| Enumerator | Blueprint display name | Behavior |
|---|---|---|
| `EC_RunLLMOption::Auto` | Auto | Convai decides whether to generate a response. |
| `EC_RunLLMOption::Always` | Always | Convai always generates a spoken response. |
| `EC_RunLLMOption::Never` | Never | Convai updates context silently with no spoken response. |

---

### EC_ContextUpdateMode

Controls how a context string is applied when calling `Update Context` directly.

| Enumerator | Blueprint display name | Behavior |
|---|---|---|
| `EC_ContextUpdateMode::Append` | Append | The text is appended to the existing context. |
| `EC_ContextUpdateMode::Replace` | Replace | The full context is replaced with the supplied text. |
| `EC_ContextUpdateMode::Reset` | Reset | The context is cleared. `Text` is ignored when mode is `Reset`. |

## Next steps

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
