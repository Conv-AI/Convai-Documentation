---
title: Dynamic context Blueprint reference
description: Reference the Blueprint controls that send runtime state, event, reset, timing, and delivery updates from an Unreal character to Convai during a live session.
last_reviewed: "4.0.0-beta.27"
---

Most dynamic context functions are exposed on `UConvaiChatbotComponent` (Blueprint display name **Convai Chatbot**) under the `Convai|DynamicContext` category. `Update Context` is an advanced direct `context-update` node in the `Convai` category; it bypasses the tracked state/event helper API. Properties appear under **Convai > DynamicContext** (debounce and delivery-timing settings) and **Convai** (`DynamicEnvironmentInfo`) in the Details panel.

Source of truth: `Source/Convai/Public/ConvaiChatbotComponent.h`, `Source/Convai/Private/ConvaiChatbotComponent.cpp`, `Source/Convai/Public/DynamicContext/ConvaiPendingContextBatch.h`, `Source/Convai/Public/DynamicContext/`, and `Source/Convai/Private/ConvaiSubsystem.cpp`.

## Functions

### `Set Context State`

Sets a single state property in the dynamic context. If a property with the same `Name` already exists, its value is replaced.

**Use when:** One current fact changes during gameplay — health, zone, equipment status.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Name` | `FString` | — | Key identifying this state property. Case-sensitive. |
| `Value` | `FString` | — | Current value of the state property. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | Contributes to batch aggregate `run_llm`. |
| `Delivery` | `EConvaiContextDelivery` | `Send Normally` | **Advanced.** `Wait Until Conversation Is Idle` holds the update until the conversation pauses, so it can't make the character interrupt itself. Applies only when the batch's aggregate `ShouldRespond` is `Auto`/`Always`. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass debounce and run the flush path in the current frame. With `Delivery` set to `Wait Until Conversation Is Idle`, the update still waits for a quiet moment but skips the full `Quiet Time Before Delivery (s)` window. Use after connection for data that must be delivered. |

**Flush behavior:** One Replace `context-update`. New keys enter canonical when aggregate is `Never`; otherwise new keys are deferred to delta lines on first flush. Updated keys always appear in canonical; delta lines describe the transition when aggregate is not `Never`.

**Pre-session:** With default debounce, stages safely and flushes after the session connects and the debounce deadline elapses. Do not use `bFlushImmediately = true` before connection for data that must be delivered.

---

### `Set Context States`

Sets multiple state properties at once. All keys share one canonical rebuild and one flush.

**Use when:** Several related facts change together — zone, equipment, and time of day after a scene transition.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `States` | `TMap<FString, FString>` | — | Map of key-value state properties to set or update. |
| `ShouldRespond` | `EC_RunLLMOption` | `Never` | Contributes to batch aggregate `run_llm` for all supplied keys. |
| `Delivery` | `EConvaiContextDelivery` | `Send Normally` | **Advanced.** `Wait Until Conversation Is Idle` holds the updates until the conversation pauses, so it can't make the character interrupt itself. Applies only when the batch's aggregate `ShouldRespond` is `Auto`/`Always`. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass debounce and run the flush path in the current frame. With `Delivery` set to `Wait Until Conversation Is Idle`, the update still waits for a quiet moment but skips the full `Quiet Time Before Delivery (s)` window. Use after connection for data that must be delivered. |

**Behavior:** Empty maps are ignored. Aggregate `ShouldRespond` merges with any other staged items in the same debounce window (`Always` > `Auto` > `Never`).

**Pre-session:** With default debounce, stages safely and flushes after the session connects and the debounce deadline elapses. Do not use `bFlushImmediately = true` before connection for data that must be delivered.

---

### `Add Context Event`

Appends a chronological event string to the dynamic context.

**Use when:** Something happened once — an alarm, a milestone, a narrative beat.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Text` | `FString` | — | Event description to append. |
| `ShouldRespond` | `EC_RunLLMOption` | `Auto` | Contributes to batch aggregate `run_llm`. |
| `Delivery` | `EConvaiContextDelivery` | `Send Normally` | **Advanced.** `Wait Until Conversation Is Idle` holds the event until the conversation pauses, so it can't make the character interrupt itself. Held events land at the end of the event history when finally sent. Applies only when `ShouldRespond` is `Auto`/`Always`. |
| `bEphemeral` | `bool` | `false` | **Advanced.** When `true`, the character sees the event exactly once, on the next update, and it is never committed to the persisted context — it never reappears on later updates. When `false` (default), the event stays in the running context. |
| `bFlushImmediately` | `bool` | `false` | **Advanced.** Bypass debounce and run the flush path in the current frame. With `Delivery` set to `Wait Until Conversation Is Idle`, the event still waits for a quiet moment but skips the full `Quiet Time Before Delivery (s)` window. Use after connection for data that must be delivered. |

**Behavior:** Identical `Text` values staged multiple times in the same debounce window are deduplicated (ephemeral and persistent events are tracked separately, so an ephemeral event with the same text as a persistent one is not deduplicated against it). At flush, a non-ephemeral event is committed to the tracker and included in canonical. An ephemeral event is appended once to the outgoing flush text and dropped afterward — it is never written to the tracker, so it does not appear in canonical context on later updates. Regular (non-ephemeral) context events are not duplicated into a separate delta line.

**Pre-session:** With default debounce, stages safely and flushes after the session connects and the debounce deadline elapses. Do not use `bFlushImmediately = true` before connection for data that must be delivered.

---

### `Remove Context State`

Removes a state property from the dynamic context and rebuilds canonical context without it.

**Use when:** A condition no longer applies — an item was used, an alert was cleared.

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

**Use when:** A simulation restarts or you need to discard all prior runtime context.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Type | Default | Description |
|---|---|---|---|
| — | — | — | No parameters. |

**Behavior:** Marks `bPendingReset`. Does not clear the tracker or discard staged updates up front. On flush: staged batch drains first, then a Reset `context-update` fires (`mode: reset`, `run_llm: "false"`, with `text` omitted for the empty Reset payload), then the local tracker is cleared. Clears `PendingTriggers` when the reset is requested. When connected, calls the flush path immediately; when offline, queues until the first post-connect flush.

---

### `Get Context State Value`

Returns the current client-side value of a tracked state property. Reads from the local tracker — does not query Convai.

**Use when:** A Blueprint condition needs the current local value before sending a redundant update.

**Blueprint category:** `Convai|DynamicContext`

| Parameter | Direction | Type | Default | Description |
|---|---|---|---|---|
| `Name` | In | `FString` | — | Key to look up. Case-sensitive. |
| `OutValue` | Out | `FString` | — | Current value if the key exists. |
| Return value | Return | `bool` | — | `true` if the key was found. |

---

### `Update Context`

Advanced direct node. Sends a raw `context-update` with explicit `Text`, `Mode`, and `ShouldRespond`. Staged state/event flushes use the same transport message type during `FlushDynamicContext()` without updating the tracker through this node. `Reset Dynamic Context` uses the same C++ `UpdateContext` send path for the reset message.

**Use when:** The tracked node family does not cover your format requirements.

**Blueprint category:** `Convai`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Text` | `FString` | — | Context text to apply. Optional when `Mode` is `Reset`. |
| `Mode` | `EC_ContextUpdateMode` | `Append` | How the context is applied: `Append`, `Replace`, or `Reset`. |
| `ShouldRespond` | `EC_RunLLMOption` | `Auto` | Maps to `run_llm` on the wire. |

Use `Update Context` only when the tracked node family does not cover your format requirements. It does not update `FConvaiDynamicContextTracker`, so `Get Context State Value` cannot read values sent only through this node. Pass an empty string when `Mode` is `Reset`; the SDK omits `text` only for an empty Reset payload.

## Default ShouldRespond reference

| Function | Default `ShouldRespond` | Default `Delivery` |
|---|---|---|
| `Set Context State` | `Never` | `Send Normally` |
| `Set Context States` | `Never` | `Send Normally` |
| `Add Context Event` | `Auto` | `Send Normally` |
| `Remove Context State` | _(no `ShouldRespond` parameter)_ | _(no `Delivery` parameter)_ |
| `Reset Dynamic Context` | _(Reset always uses `Never` on the wire)_ | _(no `Delivery` parameter)_ |
| `Update Context` | `Auto` | _(no `Delivery` parameter)_ |

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

### `ConversationIdleSettleSeconds`

| Details panel label | Quiet Time Before Delivery (s) |
|---|---|
| Type | `float` |
| Default | `2.0` |
| Clamp | ≥ `0.0` |
| Category | `Convai|DynamicContext` (Advanced Display) |

How long the conversation must stay continuously quiet before an update whose `Delivery` is `Wait Until Conversation Is Idle` is delivered. Any conversation activity restarts the wait — there is deliberately no upper bound on the total hold, so a waiting update never interrupts an ongoing exchange. Set to `0` to deliver as soon as idle is detected.

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

---

### `EConvaiContextDelivery`

Controls **when** a state, event, or fact update reaches the character, separately from the debounce batching described in [Sync behavior and timing](sync-behavior-and-timing.md).

| Enumerator | Blueprint display name | Behavior |
|---|---|---|
| `EConvaiContextDelivery::SendNormally` | Send Normally | Default. Batched into the next scheduled send — the same behavior as before this option existed. |
| `EConvaiContextDelivery::WaitUntilConversationIsIdle` | Wait Until Conversation Is Idle | Held back until the conversation has stayed quiet for `Quiet Time Before Delivery (s)`, so the update can't make the character interrupt itself or talk over the user. There is deliberately no time limit on the wait. |

Waiting only applies when `ShouldRespond` is `Auto`/`Always` — a silent (`Never`) update has nothing to interrupt with, so it is always sent normally regardless of `Delivery`.

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

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}
