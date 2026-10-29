---
title: Context in multi-character and group rooms
description: Understand when each character can receive context, how group updates stay silent, and how to distinguish submission from acknowledgement.
last_reviewed: "5.0.0-preview"
---

Dynamic Context belongs to an individual character's local tracker, but its delivery depends on the room. Ordinary multi-character rooms use the current conversation target. Group conversations have a separate member-addressed context route, so context can reach a member without making that member the target.

## Delivery by room type

| Room state | Tracked methods such as `SetState` | Raw `Apply` |
|---|---|---|
| No usable conversation or connection | Remain staged until the connection can send | Returns `false`; no raw update is queued |
| Ordinary multi-character room, character is target | Attempts submission when the batch is ready | Attempts immediate submission |
| Ordinary multi-character room, another character is target | Holds the batch until this character is targeted | Returns `false` |
| Group conversation starting | Holds context until member routing is available | Returns `false` while the route is unavailable |
| Active group conversation | Sends silent context addressed to the character's membership, whether targeted or not | Can submit to that member without changing the target; reaction is forced silent |

`Flush()` skips the debounce delay, not these routing conditions. A held tracked batch is retained. A local send refusal, such as an oversized serialized message, can instead drop it and log a warning; that is different from Convai rejecting an already submitted update.

The reason group context is silent is that the group conversation controls who responds. Sending a context update to several members should not independently start a response from every member.

## World-object reactions

Tracked properties on `ConvaiObjectMetadata` stage values in character context. During an active group conversation, a non-silent property reaction becomes silent per-character updates plus one scene-event submission with `volunteer: true`.

This lets a property change request group participation without forcing each member to speak. Submission is not a guarantee that a member volunteers, that the event is accepted, or that speech follows. [Spatial context](spatial-context.md) already uses `Silent` and does not itself create that scene event.

## Initial context and resets

An ordinary multi-character connection includes the active character's enabled initial context. Group connection uses empty shared initial text, then seeds each member's kept opening context separately. Runtime group updates preserve the relevant member's kept opening context unless removal is requested.

In 5.0, `Reset()` followed by newer tracked changes preserves the pending reset. The client attempts the reset before the newer batch. Connection and routing holds can postpone this sequence; local refusal can drop a submission. `Reset(removeStatic: true)` requests removal of static initial context as well as runtime context. It does not guarantee erasure of facts from conversation history or dashboard configuration.

## Submission and acknowledgement

`Apply` returns a local submission result. `true` means the SDK accepted the operation for sending; it does not mean Convai acknowledged or applied it. `false` means it was locally refused and no raw update was added to the tracker.

Tracked updates receive scoped IDs. Raw text/reset updates need an explicit unique `updateId` for correlation, while action or attention mutations generate one when omitted. Only action and attention mutations enter the SDK's pending local reconciliation queue. Plain text can produce acknowledgement events without requiring a matching event before later text is sent.

### Acknowledgement routing

`DynamicContextUpdateResultReceived` carries `UpdateId`, `CharacterId`, and `ParticipantId`, along with status and token information. Ordinary rooms reject action acknowledgements whose available character or participant identity does not match the character.

In a group conversation, any participant can relay an acknowledgement. The SDK checks an optional `membership_id` in `RawExtras`, then matches the unique update ID. Filtering group events solely by the sender's `CharacterId` would discard valid acknowledgements.

Matching occurs in the event callback. A separate one-second timer checks the 30-second expiry for pending action or attention mutations. Successful acknowledgements normally verify expected counts and attention values. Group responses that omit action verification counts can be applied as unverified, with a warning. An unverified result should not be presented as count-validated success.

## Related guides

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}

{% content-ref url="../conversation-targeting/group-and-shared-room-targeting.md" %}
[Targeting in group and shared rooms](../conversation-targeting/group-and-shared-room-targeting.md)
{% endcontent-ref %}
