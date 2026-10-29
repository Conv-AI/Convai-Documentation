---
title: How dynamic context works
description: Understand how Dynamic Context tracks scene state and events, batches updates, and reports acknowledgement and token feedback.
last_reviewed: "5.0.0-preview"
---

Dynamic Context gives characters a live, structured view of what is happening in the scene. Instead of relying only on the static system prompt configured on the Convai dashboard, a character can reference a trainee's current location, the equipment they have collected, or an alarm that recently triggered — because that information was injected directly into the session as it occurred. This page explains the underlying model: the two primitives the SDK tracks, how they assemble into a canonical context string, how updates batch and flush, and how the SDK reports back what happened to each update.

## States and events

Dynamic Context is built on two primitive types.

**States** are persistent, named key-value pairs. Each state has a name and a value. When you set a state, any previous value for that name is replaced. States are suitable for facts that change over time but have exactly one current value: the operator's current station, the hazard level in a zone, or whether a checklist item has been completed.

**Events** are chronological, one-time occurrences. Unlike states, events accumulate in sequence rather than being replaced. Each call to `AddEvent` appends a new line to the character's context, with one exception: if the exact same event text is already staged in the current pending batch, the repeat call is dropped and does not add a second line. This dedup window closes once the batch flushes — the same text can be added again in a later batch. A pending batch is limited to 64 distinct events. Beyond that, the oldest pending event is dropped and the first drop logs a warning; delivered history is not capped by this pending-batch limit. Events are suitable for things that happened during a session and that the character should be able to reference in order: "Trainee bypassed the manual lockout procedure", "Chemical alarm triggered at Bay 7".

Both primitives feed into the character's awareness simultaneously. States provide a stable, queryable snapshot of current conditions; events provide a chronological record of what has happened.

## Canonical context format

Before an update reaches Convai, the SDK assembles a canonical context string from all tracked states and events. Tracked text batches rebuild this base format. An attention-only batch can omit text; a `Reset` uses its own mode. For a text batch whose aggregated reaction is `Silent`, this is the full generated text:

```text
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

```text
Station is Bay 7
HazardLevel is High
Operator bypassed interlock
```

You supply only names, values, and event text. The SDK assembles and delivers the canonical string automatically.

## Delta narration on a non-Silent batch

The canonical block above is not the whole story whenever the pending batch's aggregated reaction is `Auto` or `MustRespond` — the common case, since `AddEvent`'s default reaction is `Auto` and any call passed a non-`Silent` reaction produces the same effect for its batch. On a non-`Silent` batch, the SDK appends a delta-narration line after the canonical block for every state that changed **in that batch** — not for every tracked state, only the ones this update touched:

- A state staged for the first time reports `"{StateName} is {Value}"`. The canonical block above omits that state's own "is" line on this batch, so it is not listed twice — it appears once, in the delta tail.
- A state that already had a value reports `"{StateName} changed from {PreviousValue} to {CurrentValue}"`, unless the new value is more than three whitespace-separated words long, in which case the destination is dropped and the tail reports only `"{StateName} changed from {PreviousValue}"`.

The recorded previous value is the value the state held before the *first* change staged for it in the current batch — if a state is set more than once before the batch flushes, only the first previous value and the final current value appear in the delta line, not every intermediate value.

Canonical and delta lines are joined with a newline, canonical block first:

```text
Station is Bay 7
HazardLevel is High
Operator bypassed interlock
Station changed from Bay 3 to Bay 7
```

**Example — a batch that escalates to `Auto`:**

```csharp
// Already delivered in an earlier batch: Station is "Bay 3", HazardLevel is "High".

context.SetState("Station", "Bay 7");                  // default reaction: Silent
context.AddEvent("Operator bypassed interlock");        // default reaction: Auto — outranks Silent for this batch
```

The `AddEvent` call's default `Auto` reaction outranks `SetState`'s default `Silent`, so the whole batch's aggregated reaction is `Auto`. `Station` is the only state that changed in this batch, so it is the only one that gets a delta line — `HazardLevel`, untouched by this update, appears only once, in the canonical block, exactly as it would on a `Silent` batch.

**Example — the word cap on a changed value:**

```csharp
context.SetState("HazardLevel", "Confirmed multi-agent chemical exposure across Bay 7", ConvaiRespondMode.Auto);
```

`"Confirmed multi-agent chemical exposure across Bay 7"` is seven whitespace-separated words, more than the three-word cap, so the delta line drops the destination: `HazardLevel changed from High`. The full new value still reaches the character — it is the current line in the canonical block above (`HazardLevel is Confirmed multi-agent chemical exposure across Bay 7`); the cap only shortens the narration line that follows it.

## Two entry points to the same tracker

Dynamic Context has two entry points that write to the same underlying tracker and produce identical network behavior.

**Inspector — `ConvaiDynamicContextRelay`**

`ConvaiDynamicContextRelay` is the Inspector entry point for Dynamic Context. Add it via **Convai → Dynamic Context → Convai Dynamic Context Relay**, either on the same GameObject as `ConvaiCharacter` or on any GameObject with an explicit **Character** reference assigned. If **Character** is empty and **Auto Resolve Character** is enabled (the default), the relay looks for a `ConvaiCharacter` on its own GameObject at call time.

The relay exposes public methods that call directly into `character.DynamicContext`: `SetState(name, value)`, `AddEvent(text)`, `SetCurrentAttentionObject(objectName)`, `ClearCurrentAttentionObject()`, `ResetContext()` / `ResetContext(removeStatic)`, and `Flush()`. Bind the zero- or one-parameter methods through Inspector `UnityEvent` listeners. `SetState` takes two parameters and needs a script adapter. One relay component can serve several different `UnityEvent` callbacks on the same character.

Two Inspector fields control calls through that relay instance: **Reaction Mode** sets the request for the state, event, and attention methods (default `Silent`), and **Flush Immediately**, when enabled, calls `Flush()` after staging, including `ResetContext`, to bypass the batch delay. Connection and room routing checks still apply. Because the relay always passes its configured **Reaction Mode** explicitly, a method's own scripting default does not apply when the call is routed through the relay — for example, `AddEvent`'s scripting default of `Auto` is overridden by whatever **Reaction Mode** the relay is set to.

The relay's **Events** section exposes `OnQueued` and `OnSkipped`. `OnSkipped` fires when the relay cannot resolve a `ConvaiCharacter`. `OnQueued` fires once the relay resolves a character and dispatches the call — it confirms dispatch, not that the value was accepted. An empty state name or a null value still logs a Console warning even when `OnQueued` fires.

**Scripting — `IConvaiDynamicContext`**

Access `character.DynamicContext` to get the `IConvaiDynamicContext` interface and call methods directly from C#. This gives full control over timing, batching, and respond mode.

```csharp
IConvaiDynamicContext context = _character.DynamicContext;
context.SetState("Station", "Bay 7");
context.AddEvent("Operator bypassed interlock");
```

Use this entry point when:
- Context updates depend on runtime logic or data that cannot be expressed as static Inspector fields
- Multiple states must change atomically (use `SetStates`)
- You need to read state values back (`TryGetStateValue`)
- The update source is an external system such as a state machine or analytics pipeline

## Batching and delivery timing

Tracked calls — `SetState`, `SetStates`, `AddEvent`, `RemoveState`, `SetCurrentAttentionObject`, `ClearCurrentAttentionObject`, and `Reset` — never send a network message immediately. Each call updates the local tracked state right away, then stages a pending batch for delivery. This exists so that a burst of related changes fired within the same frame collapses into one canonical update, rather than one network message and one potential LLM turn per call.

```mermaid
graph TD
    A["SetState / AddEvent / RemoveState call"] --> B["Staged locally; batch window opens or extends"]
    B --> C{"Flush called, or window elapses?"}
    C -->|No| B
    C -->|Yes| D["One context-update sent to Convai"]
    D --> E["DynamicContextUpdateResultReceived"]
```

While a conversation is active, the first staged change opens a batch window. Every subsequent staged change resets a countdown of `ConvaiCharacter.DynamicContextBatchDelaySeconds` — 0.5 seconds by default. The SDK also enforces an internal ceiling of 3 seconds measured from the first staged change in the window, so a steady stream of changes cannot postpone delivery indefinitely. Runtime action-target changes from `character.Actions` and scene metadata changes share this window, and every flush starts a new one. Calling `Flush()` attempts the pending send without the remaining countdown. Connection and room holds can extend delivery beyond the batching ceiling.

If a call happens before the character is in conversation, it stages locally only — no countdown starts. When the session's character-ready signal arrives, the SDK attempts to flush the staged batch, subject to room routing. Calls made in `Awake` or `Start` therefore do not need their own readiness timer:

```csharp
void Start()
{
    // Safe — stages locally, then flushes as soon as the character is ready
    _character.DynamicContext.SetState("Facility", "Offshore Platform Alpha");
    _character.DynamicContext.SetState("Scenario", "Fire Drill");
    _character.DynamicContext.AddEvent("Session initialized");
}
```

When the session disconnects, the SDK marks the tracked context for a full canonical resync, so the next reconnect rebuilds the same context even if nothing changed locally while offline.

When multiple staged changes carry different respond modes, the strongest one wins for the whole batch: `MustRespond` outranks `Auto`, which outranks `Silent`.

Dynamic context and dynamic vision context share one respond-mode vocabulary, `ConvaiRespondMode` (namespace `Convai.Runtime`), whose values are `Silent`, `Auto`, and `MustRespond`.

{% hint style="warning" %}
`Apply()` is the one exception: it does not stage or queue. Calling it while the character is not in conversation discards the update. Use `SetState`, `AddEvent`, or the other tracked methods for context that must survive until a conversation starts.
{% endhint %}

## Acknowledgement and token feedback

Convai acknowledgements arrive through `ConvaiManager.ActiveManager.Events.OnDynamicContextUpdateResultReceived`; submission does not guarantee an acknowledgement. Match a received event using its unique `UpdateId`. Tracked batches use a scoped SDK ID such as `unity-{characterId}-{scope}-{sequence}`. Raw text/reset updates need an explicit `updateId` if you want correlation; raw action or attention mutations generate one when omitted.

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Components;

ConvaiManager.ActiveManager.Events.OnDynamicContextUpdateResultReceived += result =>
{
    Debug.Log($"{result.Status}: revision {result.ContextRevision}, {result.RemainingTokens} tokens remaining");
};
```

| Property | Type | Meaning |
|---|---|---|
| `Status` | `string` | `"success"` when the update was applied; any other value means it was rejected. |
| `Message` | `string` | Human-readable detail accompanying the status. |
| `UpdateId` | `string` | Correlates the update when an ID was supplied or generated. |
| `CharacterId`, `ParticipantId` | `string` | Identity attached to the received event. In group rooms the relaying participant may differ from the intended member; use update ID and membership information for routing. |
| `ContextRevision` | `int` | The backend's revision counter for this character's context. |
| `TokenCount`, `StaticTokenCount`, `RuntimeTokenCount`, `RemainingTokens` | `int` | Token accounting for the character's context window after this update. |
| `RequestedRunLlm`, `ActualRunLlm` | `string` | The respond mode requested versus what the backend actually honored. |
| `DowngradeReason` | `string` | Explains why `ActualRunLlm` differs from `RequestedRunLlm`, when it does. |
| `Interrupted` | `bool` | Whether this update interrupted an in-flight character turn. |
| `LlmTriggered` | `bool` | Whether this update triggered a new character turn. |
| `PromptRebuild`, `PromptRebuildStatus` | `bool`, `string` | Whether the backend rebuilt the character's prompt to include this update, and the outcome. |

The same event also carries action-specific fields — `ActionConfigUpdated`, `ActionsCount`, `CurrentAttentionObject`, and related properties — when the update includes an action configuration patch. See [Update character actions at runtime](../character-actions/update-actions-at-runtime.md) for that acknowledgement flow.

## World objects and room delivery

Tracked world-object properties and [spatial context](spatial-context.md) use the same local state tracker, so they share batching and reaction aggregation with scripted updates. Ordinary multi-character rooms hold updates for a non-target character; group rooms route member context silently and hold it while the group starts. See [Context in multi-character and group rooms](multi-character-and-group-rooms.md).

## Next steps

{% content-ref url="dynamic-context-quick-start.md" %}
[Dynamic context quick start](dynamic-context-quick-start.md)
{% endcontent-ref %}

{% content-ref url="relay-component-reference.md" %}
[Relay component reference](relay-component-reference.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}
