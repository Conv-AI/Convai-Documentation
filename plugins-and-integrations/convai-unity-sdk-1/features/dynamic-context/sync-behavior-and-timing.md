---
title: Sync behavior and timing
description: >-
  Understand how the SDK transmits Replace, Append, and Reset messages for each
  Dynamic Context operation, including queueing and Apply() behavior.
last_reviewed: "4.2.0"
---

Every tracked Dynamic Context operation produces one or two RTVI `context-update` messages sent to Convai. This page documents the exact message sequence for each scenario, the pre-conversation queuing behavior, and how the SDK flushes pending context when a conversation starts.

## Canonical context format

Before describing sync scenarios, it helps to understand what the SDK sends. The canonical context is a newline-separated string assembled from all tracked states and events:

```
{StateName} is {Value}
{AnotherState} is {Value}
Event text line one
Event text line two
```

States appear first, in the order they were **first set** — not the order of the most recent update. Updating a state's value does not change its position in the output. Events follow in chronological order (call order).

**Example — state insertion order is preserved across updates:**

```csharp
context.SetState("Station", "Bay 3");       // position 1
context.SetState("HazardLevel", "High");    // position 2
context.AddEvent("Operator bypassed interlock");
context.SetState("Station", "Bay 7");       // updates value; position stays at 1
```

Canonical output after all four calls:

```
Station is Bay 7
HazardLevel is High
Operator bypassed interlock
```

## Sync scenarios during active conversations

### Adding a new state

**SDK call:** `SetState("Station", "Bay 3")` — `Station` has never been set.

**Messages sent:** One Append.

```
mode:  Append
text:  "Station is Bay 3"
```

The server appends this line to its existing context view.

### Updating an existing state

**SDK call:** `SetState("Station", "Bay 7")` — `Station` was previously `"Bay 3"`.

**Messages sent:** Two messages in sequence.

**Message 1 — Replace (full canonical context with updated value):**

```
mode:  Replace
text:  "Station is Bay 7\nHazardLevel is High\nOperator bypassed interlock"
```

**Message 2 — Append (delta for natural dialogue reference):**

```
mode:  Append
text:  "Station changed from Bay 3 to Bay 7"
```

The Replace gives the character an authoritative complete picture of the current state. The Append gives it a natural way to reference the transition in dialogue: _"I see you've moved from Bay 3 to Bay 7."_

{% hint style="info" %}
Two messages for one `SetState` call on an existing state is expected behavior. If you are monitoring network traffic during debugging, expect this pattern for every existing-state modification.
{% endhint %}

### Removing a state

**SDK call:** `RemoveState("Station")`.

**Messages sent:** One Replace containing the canonical context without the removed state.

```
mode:  Replace
text:  "HazardLevel is High\nOperator bypassed interlock"
```

### Batch update with `SetStates`

**SDK call:** `SetStates({ "Station": "Bay 7", "HazardLevel": "Extreme" })` — `Station` existed (`"Bay 3"`), `HazardLevel` is new.

Because at least one existing state was modified, two messages are sent:

**Message 1 — Replace (full canonical context, all values updated):**

```
mode:  Replace
text:  "Station is Bay 7\nHazardLevel is Extreme\n..."
```

**Message 2 — Append (all changes summarized):**

```
mode:  Append
text:  "Station changed from Bay 3 to Bay 7\nHazardLevel is Extreme"
```

**All-new states only:** If every state in `SetStates` is new (none existed before), only one Append is sent — no Replace. The Append contains all new state lines joined by newline.

### Adding an event

**SDK call:** `AddEvent("Operator bypassed interlock")`.

**Messages sent:** One Append.

```
mode:  Append
text:  "Operator bypassed interlock"
```

Events never trigger a Replace. The server appends the event text to its context view.

### Resetting all context

**SDK call:** `Reset()`.

**Messages sent:** One Reset-mode message.

```
mode:  Reset
text:  null
```

The server clears its Dynamic Context view. The local tracker is also cleared — all states and events are removed.

## Pre-conversation queuing

All tracked methods — `SetState`, `SetStates`, `AddEvent`, `RemoveState`, `Reset` — queue automatically when no conversation is active.

When the session connects, the SDK flushes the pending queue in one of two ways:

* **Pending sync (states or events queued):** A single Replace message containing the full canonical context at the moment of connection. All incremental changes are collapsed into one authoritative snapshot — they are not replayed as individual Append and Replace messages.
* **Pending reset (Reset was called while offline):** A Reset message. If both a reset and subsequent changes are pending, the reset takes priority and clears the queue.

**Example — all three calls queue safely before `ConnectAsync`:**

```csharp
void Start()
{
    // Safe to call before ConnectAsync — all three queue and flush at connection
    _character.DynamicContext.SetState("Facility", "Offshore Platform Alpha");
    _character.DynamicContext.SetState("Scenario", "Fire Drill");
    _character.DynamicContext.AddEvent("Session initialized");
}
```

The character receives one Replace at connection time:

```
Facility is Offshore Platform Alpha
Scenario is Fire Drill
Session initialized
```

## `Apply()` exception

`Apply()` bypasses the tracker entirely and does **not** queue pre-conversation.

* If the character is **not** in an active conversation: the update is discarded and a warning is emitted through the Convai logger. Enable Convai debug logging to see it in the Unity Console. No queue is built — the update is lost.
* If the character **is** in an active conversation: the message is sent directly to transport using the `ConvaiContextUpdateMode` you specify.
* The local state tracker is not updated. `TryGetStateValue` returns `false` for keys sent via `Apply()`.

{% hint style="danger" %}
Do not use `Apply()` for context that must be delivered before a conversation starts. Use `SetState`, `AddEvent`, or other tracked methods instead — they queue automatically and flush on connection.
{% endhint %}

## Next steps

{% content-ref url="dynamic-context-scripting-api.md" %}
[Dynamic Context scripting API](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}
