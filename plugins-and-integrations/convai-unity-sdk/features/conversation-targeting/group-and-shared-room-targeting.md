---
title: Targeting in group and shared rooms
description: Understand why a group conversation, another player, or a scripted move can hold the conversation target despite an unchanged local proposal.
last_reviewed: "5.0.0-preview"
---

A targeting proposal is a local choice about whom to address. The confirmed room route can remain different because a group conversation, another player, or your own code has priority over an unchanged proposal.

## Holds on automatic targeting

| Situation | Verdict | Release condition |
|---|---|---|
| Active group conversation with a current target that can still hear | `HeldForGroupConversation` | The group hold ends or the current target can no longer hear. |
| Another player moves the confirmed route | `HeldForAnotherPlayer` | Your local proposal changes. |
| Your code confirms a target move or clear | `HeldForScriptedTarget` | The automatic proposal or confirmed route changes. |

A group hold skips the custom provider while it applies. The other holds still evaluate proposals, so the SDK can detect a changed choice. They do not expire merely because **Switch Delay (Seconds)** has elapsed.

## Scripted changes and recovery

`TalkToAsync` and `ClearConversationTargetAsync` expose confirmation through an operation. `TalkTo` submits a request without an awaitable return and reports failures through the conversation-target event phase. The route changes only after room confirmation.

In `Manual`, a missing or failed target membership can recover to the first ready member. An explicitly cleared route remains empty until another scripted request. Disabling a character component is not identical to a failed room membership.

## UI state and events

Use `ConversationTarget` for the confirmed room target. `AddressedCharacter` also includes a pending move and the pre-connect look target. Use `ConversationAvailability` to decide whether an input control can submit player speech or text.

`ConversationTargetChanged` can arrive without a local `ConversationTargetRequested` when another player changes the shared route. Do not require a local request before accepting an authoritative change.

## Related guides

{% content-ref url="script-the-conversation-target.md" %}
[Script the conversation target](script-the-conversation-target.md)
{% endcontent-ref %}

{% content-ref url="targeting-reference.md" %}
[Conversation targeting reference](targeting-reference.md)
{% endcontent-ref %}
