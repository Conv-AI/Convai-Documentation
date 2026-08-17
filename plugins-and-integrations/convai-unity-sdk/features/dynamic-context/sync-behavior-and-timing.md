---
title: Sync behavior and timing
description: >-
  Understand how the SDK batches dynamic context updates before sending them
  and how action and attention changes are confirmed by Convai.
last_reviewed: "4.5.0"
---

Dynamic Context updates do not reach Convai the instant you call `SetState`, `AddEvent`, or any other tracked method. The SDK stages every call into a short-lived batch and sends one `context-update` message per batch, not one per call. This page explains why the SDK batches, exactly when a batch is sent, and how updates that carry an action config patch or an attention object are acknowledged before the SDK trusts them locally.

## Why dynamic context batches updates

A single gameplay frame can call several tracked methods at once — a hazard state, a location change, and an event firing together in one physics update. Sending an individual `context-update` message per call would multiply network traffic and could let Convai react to an intermediate state before the rest of the frame's changes land. Instead, `ConvaiCharacter` stages every call to `SetState`, `SetStates`, `AddEvent`, `RemoveState`, `SetCurrentAttentionObject`, and `ClearCurrentAttentionObject` into one pending batch and flushes that batch as a single message.

The reason a shared batch also needs a shared reaction decision is that Convai only sees one message, so it can only apply one respond mode. When several calls in the same window request different `ConvaiRespondMode` values, the strongest request wins for the whole batch: `MustRespond` beats `Auto`, and `Auto` beats `Silent`. A single `MustRespond` call in a batch of otherwise-silent updates makes the whole batch request an LLM run.

```csharp
using Convai.Runtime;
using Convai.Runtime.Components;
using Convai.Runtime.DynamicContext;
using UnityEngine;

public sealed class HazardZoneContext : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter character;

    public void OnHazardTriggered()
    {
        character.DynamicContext.SetState("Station", "Bay 7");
        character.DynamicContext.SetState("HazardLevel", "Extreme", ConvaiRespondMode.MustRespond);
        character.DynamicContext.AddEvent("Operator bypassed interlock");
    }
}
```

**Expected client outcome:** all three calls land in the same batch and produce one `context-update` message. Because `HazardLevel` requested `MustRespond`, the whole batch is sent with `MustRespond`, even though `SetState("Station", ...)` and `AddEvent(...)` default to weaker modes. Whether that request produces a character turn is reported by the backend result and must be verified in a live session.

## The batch window and its ceiling

The SDK debounces staged changes for `ConvaiCharacter.DynamicContextBatchDelaySeconds` — a fixed `0.5` seconds. Every additional staged change during that window pushes the flush out by another `0.5` seconds from the moment it was staged, measured from when Unity last processed a change.

A continuous stream of changes could in theory push the flush out indefinitely, so the SDK also enforces a ceiling: the wait can never exceed 3 seconds measured from the first staged change in the window. Whichever limit is reached first — the 0.5-second debounce settling, or the 3-second ceiling — triggers the flush.

| Timing behavior | Value | Effect |
|---|---|---|
| Per-change debounce | 0.5 seconds (`DynamicContextBatchDelaySeconds`) | Each staged change resets the flush countdown |
| Maximum wait per window | 3 seconds | The flush fires even while changes keep arriving |

```mermaid
sequenceDiagram
    participant Script
    participant Character as ConvaiCharacter
    participant Convai

    Script->>Character: SetState / AddEvent / SetCurrentAttentionObject
    Note over Character: debounce 0.5s per change,<br/>capped at 3s from the first staged change
    Character->>Convai: context-update (Replace or Append)
    opt Update carries an action config patch or attention object
        Convai-->>Character: DynamicContextUpdateResultReceived (update_id)
        Note over Character: committed locally only after a matching, successful acknowledgement
    end
```

`Reset()` goes through the same debounce window rather than sending immediately — calling `Reset()` does not bypass the 0.5-second wait.

{% hint style="warning" %}
A pending reset is not guaranteed to reach Convai as a reset. If `SetState`, `SetStates`, `AddEvent`, `RemoveState`, `SetCurrentAttentionObject`, or `ClearCurrentAttentionObject` is staged after `Reset()` but before the batch window flushes, the pending reset is dropped and replaced by a normal batch containing only the new call. Call `Flush()` immediately after `Reset()` if the reset must reach Convai before anything else can supersede it.
{% endhint %}

## What one flush sends

A flush sends exactly one message, and its mode depends on what changed during the window. If any tracked state text changed — a new state, an updated value, or a removed state — the message mode is Replace, carrying the full canonical context plus a short delta tail describing what changed. If the only staged change in the window was an attention-object update with no state text change, the message mode is Append instead.

This mirrors the single-call behavior documented on the [dynamic context scripting API](dynamic-context-scripting-api.md) page, with one difference: the SDK now coalesces every call in the window into that one message rather than sending a message per call.

## Forcing a flush before the window closes

Call `Flush()` on `IConvaiDynamicContext` to attempt the pending send without waiting out the debounce window. Use it when client ordering matters, while remembering that `Flush()` does not await backend application or a character turn.

```csharp
character.DynamicContext.SetState("Player location", "market square");
character.DynamicContext.Flush();
```

`Flush()` only sends when the character `IsInConversation`. If the character is not connected, the staged batch remains pending and is not force-sent — see the next section for what happens to it.

## Timing around connect, reconnect, and disconnect

A flush only sends while the character `IsInConversation`. Calls staged before a conversation starts, or while reconnecting after a drop, stay queued in the tracker rather than being discarded.

When a session moves to `Disconnected` or `Error`, the SDK stages a canonical resync of whatever content the tracker is currently holding, rather than replaying the individual calls that produced it. The reason a disconnect resyncs the full canonical context instead of replaying history is that Convai only needs the character's current state, not the sequence of intermediate values it passed through while offline.

When the character receives its ready signal — on initial connect or after a reconnect — the SDK flushes any pending batch immediately, without waiting for the debounce window. This is what delivers context staged before a conversation existed: it is not discarded, and it does not wait out a fresh 0.5-second timer once the character is ready.

## Acknowledgement timing for action and attention updates

Plain state and event updates are fire-and-forget once flushed — the SDK updates the tracker immediately and does not wait for a backend result before keeping that text locally. Updates that carry an action config patch or an attention object are different: they change resolved runtime action state, so the SDK does not commit those mutations locally until their acknowledgement path succeeds.

Each action-config or attention update is sent with an `update_id` and tracked while waiting for a matching `DynamicContextUpdateResultReceived` event. The SDK checks for a match once per second and gives up on any single update after 30 seconds without a matching acknowledgement, discarding the pending mutation and logging a warning rather than retrying it. Pending updates are committed in the order they were sent — an older update waiting on its acknowledgement blocks newer ones from committing, even if a newer update's acknowledgement arrives first.

Every tracked action/attention mutation requires a matching result whose status is `success`. For an action-config patch, the SDK additionally validates the returned action-config flag, action/object/character counts, and expected attention metadata before commit. An attention-only update does not run those action-config count checks. A failed, mismatched, malformed, or timed-out result is discarded with a warning instead of committing the pending mutation.

Subscribe to the event to observe backend results. Do not use this event alone as proof of local action-state commit, because the ordered queue and action-config validation run separately:

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Components;
using UnityEngine;

ConvaiManager.ActiveManager.Events.OnDynamicContextUpdateResultReceived += result =>
{
    Debug.Log($"Dynamic context {result.Status}: revision {result.ContextRevision}");
};
```

If an acknowledgement reports its action generation strategy status as `requires_reconnect`, the SDK surfaces that status but does not reconnect automatically — the calling code decides whether and when to reconnect.

## Apply() bypasses batching

`Apply()` sends its update directly to the transport, skipping the tracker and the debounce window described above. It does not bypass acknowledgement tracking: an `Apply()` call that carries an action-config patch or a current attention object still joins the same pending-update queue, with the same 30-second timeout and 1-second poll interval described in "Acknowledgement timing" above. A text-only `Apply()` forwards `updateId` only when you supply one; it does not need or generate an ID solely for local commit because it never enters that queue.

{% hint style="danger" %}
If the character is not in an active conversation when `Apply()` is called, the update is discarded immediately — it is not staged, and it does not flush later when the character becomes ready. Use `SetState`, `SetStates`, `AddEvent`, `RemoveState`, `SetCurrentAttentionObject`, or `ClearCurrentAttentionObject` for anything that must survive being called before a conversation starts.
{% endhint %}

`Apply()` exists for callers that already generate their own canonical context text — an external state machine, for example — and need direct control over exactly what is sent and when, without the SDK reshaping it into a batch.

## Next steps

{% content-ref url="dynamic-context-scripting-api.md" %}
[Dynamic context scripting API](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}
