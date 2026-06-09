---
title: How dynamic context works
last_reviewed: 4.2.0
description: >-
  Understand the states and events model, canonical context format, and how
  updates queue and flush before and during conversations.
---

# How dynamic context works

Dynamic Context gives characters a live, structured view of what is happening in the scene. Instead of relying only on the static system prompt configured on the Convai dashboard, a character can reference a trainee's current location, the equipment they have collected, or an alarm that just triggered — because that information was injected directly into the session as it occurred. This page explains the underlying model: what the primitives are, how the SDK assembles them into a canonical context string, and why updates queue safely before a conversation starts.

### States and events

Dynamic Context is built on two primitive types.

**States** are persistent, named key-value pairs. Each state has a name and a value. When you set a state, any previous value for that name is replaced. States are suitable for facts that change over time but have exactly one current value: the operator's current station, the hazard level in a zone, or whether a checklist item has been completed.

**Events** are chronological, one-time occurrences. Unlike states, events accumulate in sequence and are never replaced or deduplicated. Each call to `AddEvent` appends a new line to the character's context. Events are suitable for things that happened during a session and that the character should be able to reference in order: "Trainee bypassed the manual lockout procedure", "Chemical alarm triggered at Bay 7".

Both primitives feed into the character's awareness simultaneously. States provide a stable, queryable snapshot of current conditions; events provide a chronological record of what has happened.

### Canonical context format

When the SDK sends an update to Convai, it assembles a canonical context string from all tracked states and events:

```
{StateName} is {Value}
{AnotherState} is {Value}
Event text line one
Event text line two
```

States appear first, in the order they were **first set** — updating a state's value does not change its position. Events follow in call order after all states.

The reason states preserve insertion order across updates is to give the character a stable, predictable view of the world. If `Station` was the first thing set, it always appears first in the character's context, regardless of how many times the value has changed. This makes the context easier for the model to interpret consistently.

**Example:**

```csharp
context.SetState("Station", "Bay 3");       // position 1
context.SetState("HazardLevel", "High");    // position 2
context.AddEvent("Operator bypassed interlock");
context.SetState("Station", "Bay 7");       // updates value; position stays at 1
```

Canonical context after all four calls:

```
Station is Bay 7
HazardLevel is High
Operator bypassed interlock
```

You supply only names, values, and event text. The SDK assembles and delivers the canonical string automatically.

### Two entry points

Dynamic Context has two entry points that write to the same underlying tracker and produce identical network behavior.

**Inspector — `ConvaiDynamicContextCommand`**

Add this `MonoBehaviour` to the NPC's GameObject and configure the command type, fields, and reaction mode in the Inspector. Call `Execute()` from a `UnityEvent`, trigger collider, timeline marker, or UI button. No scripting required. One component encapsulates one command; for multiple commands per NPC, place each on a child GameObject.

Use this entry point when:

* Context changes are tied to scene events that already fire `UnityEvent` callbacks
* Non-programmers need to configure or modify context triggers
* You want to prototype quickly without writing glue code

**Scripting — `IConvaiDynamicContext`**

Access `character.DynamicContext` to get the `IConvaiDynamicContext` interface and call methods directly from C#. This gives full control over timing, batching, and reaction mode.

```csharp
IConvaiDynamicContext context = _character.DynamicContext;
context.SetState("Station", "Bay 7");
context.AddEvent("Operator bypassed interlock");
```

Use this entry point when:

* Context updates depend on runtime logic or data that cannot be expressed as static Inspector fields
* Multiple states must change atomically (use `SetStates`)
* You need to read state values back (`TryGetStateValue`)
* The update source is an external system such as a state machine or analytics pipeline

### Pre-conversation queueing

Updates made before a conversation begins are automatically queued by all tracked methods — `SetState`, `SetStates`, `AddEvent`, `RemoveState`, and `Reset`. When the session connects, the SDK delivers a single Replace message containing the full canonical context at that moment.

This means you can set initial context freely from `Awake` or `Start` without timing concerns. The SDK handles delivery.

```csharp
void Start()
{
    // Safe — all three queue and flush as one Replace when ConnectAsync fires
    _character.DynamicContext.SetState("Facility", "Offshore Platform Alpha");
    _character.DynamicContext.SetState("Scenario", "Fire Drill");
    _character.DynamicContext.AddEvent("Session initialized");
}
```

The reason this collapses into one Replace rather than replaying individual messages is efficiency: the character receives one authoritative snapshot rather than a stream of incremental updates that could arrive out of order or create redundant LLM turns.

{% hint style="warning" %}
`Apply()` is the one exception: it does not queue. If called before a conversation starts, the update is discarded. Use `SetState`, `AddEvent`, or other tracked methods for pre-conversation context. See [Dynamic context scripting API](dynamic-context-scripting-api.md) for details.
{% endhint %}

### When to use which command type

| Goal                                                    | Use                                                         |
| ------------------------------------------------------- | ----------------------------------------------------------- |
| Track one current condition                             | `SetState`                                                  |
| Track several conditions that change at the same moment | `SetStates` (one canonical rebuild, one network round-trip) |
| Record that something happened                          | `AddEvent`                                                  |
| Remove a condition that no longer applies               | `RemoveState`                                               |
| Clear all runtime context (for a new scenario phase)    | `Reset`                                                     |
| Send externally constructed context text                | `Apply()` — advanced; does not queue                        |

### Next steps

{% content-ref url="dynamic-context-quick-start.md" %}
[dynamic-context-quick-start.md](dynamic-context-quick-start.md)
{% endcontent-ref %}

{% content-ref url="command-component-reference.md" %}
[command-component-reference.md](command-component-reference.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[sync-behavior-and-timing.md](sync-behavior-and-timing.md)
{% endcontent-ref %}
