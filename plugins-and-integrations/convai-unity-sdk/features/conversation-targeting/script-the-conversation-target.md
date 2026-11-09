---
title: Script the conversation target
description: Move the conversation to a specific character from a script, and choose which character a room opens on when it connects.
last_reviewed: "5.0.0-preview"
---

Move the conversation to a specific character from a script with `ConvaiManager.TalkTo`, or choose which character a room opens on with `ConvaiManager.SetInitialCharacter`. Use this page when a dialogue menu, a quest step, or a trigger volume needs to decide who the player is addressing, rather than the player's view or position.

## Prerequisites

- Two or more `ConvaiCharacter` components registered in the scene
- A reference to the active `ConvaiManager`

## Point the conversation at a character

`TalkTo` is the verb for a scripted conversation change. It reports a failed target change if the character is null, is not a room member, or no multi-character session is active.

```csharp
ConvaiManager manager = ConvaiManager.ActiveManager;
manager.TalkTo(questGiver);
```

`TalkTo` works under any targeting mode, including `LookAt` and `Proximity` — it does not require `Manual`. Under an automatic mode, a confirmed scripted target holds until the automatic proposal changes. Choose `Manual` to drive normal moves from code; it still recovers a missing or failed target membership.

{% hint style="info" %}
If the player is mid-sentence when `TalkTo` is called, the request is held until that utterance ends, so a call made while the player is speaking does not split their sentence across two characters.
{% endhint %}

## Await or clear the target

Use `TalkToAsync(character).AsTask()` when subsequent work depends on confirmation. Use `ClearConversationTargetAsync().AsTask()` to request an empty route. Await either task inside your async method and handle failures; a rejected request faults the operation. An explicit clear remains held in `Manual`, and automatic modes release their hold when the proposal changes.

## Choose which character a room opens on

`SetInitialCharacter` chooses which character speaks first when the room connects — a different job from `TalkTo`. It is setup, not steering: it decides where a conversation starts, and calling it on an already-connected room queues a reconnect rather than moving the current conversation. Leaving it unset is normal — the first character in scene order takes the first turn.

```csharp
manager.SetInitialCharacter(receptionist);
```

{% hint style="warning" %}
`SetInitialCharacter` only decides who takes the first turn. Under `LookAt` and `Proximity`, the conversation is re-evaluated from the moment the room is ready and moves off this character as soon as another one scores better. To move the conversation in a live room, call `TalkTo`, not `SetInitialCharacter`.
{% endhint %}

## Read the current target

```csharp
ConvaiCharacter target = manager.ConversationTarget;
ConversationTargetSwitchVerdict why = manager.ConversationTargetingStatus;
```

`ConversationTarget` is the confirmed room route. For UI, `AddressedCharacter` also reflects a pending move or a pre-connect look target. Bind input availability to `ConversationAvailability` and `ConversationAvailabilityChanged`; see [Conversation availability](../conversation-availability/README.md).

`ConversationTargetingStatus` names the reason the last targeting decision went the way it did — useful for telling a held target apart from a stuck one, since from the outside they look identical.

## Subscribe to targeting events

```csharp
// pseudocode: ShowHint and Confirm are your UI callbacks.
manager.ConversationTargetRequested += character => ShowHint(character);
manager.ConversationTargetChanged   += character => Confirm(character);
```

`ConversationTargetRequested` fires after the SDK closes player input and immediately before it attempts to send the target change; the send can still fail. `ConversationTargetChanged` fires when an authoritative response from Convai reconciles the route — a round trip later. In a shared room, `ConversationTargetChanged` can also arrive without a local `ConversationTargetRequested` when another player changes the route.

## One character speaks at a time

`TalkTo` requests a route change; confirmation happens later. To avoid interrupting a scripted line, wait until `ConvaiCharacter.IsSpeaking` is false before requesting the move. See [One character speaks at a time](how-conversation-targeting-works.md#one-character-speaks-at-a-time) for the full rule and how to avoid cutting off a scripted line.

## Verify the change

Call `TalkTo` in Play mode and confirm the conversation moves to the specified character — the character's audio and lip sync should start on the next response, and `ConversationTarget` should return that character.

## Next steps

{% content-ref url="custom-targeting-rule.md" %}
[Write a custom targeting rule](custom-targeting-rule.md)
{% endcontent-ref %}

{% content-ref url="targeting-reference.md" %}
[Conversation targeting reference](targeting-reference.md)
{% endcontent-ref %}
