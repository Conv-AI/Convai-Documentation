---
title: Script the conversation target
description: Move the conversation to a specific character from a script, and choose which character a room opens on when it connects.
last_reviewed: "4.6.0"
---

Move the conversation to a specific character from a script with `ConvaiManager.TalkTo`, or choose which character a room opens on with `ConvaiManager.SetInitialCharacter`. Use this page when a dialogue menu, a quest step, or a trigger volume needs to decide who the player is addressing, rather than the player's view or position.

## Prerequisites

- Two or more `ConvaiCharacter` components registered in the scene
- A reference to the active `ConvaiManager`

## Point the conversation at a character

`TalkTo` is the verb for a scripted conversation change. Call it at any time — it does nothing when the room is not a multi-character room or the character is not in it.

```csharp
ConvaiManager manager = ConvaiManager.ActiveManager;
manager.TalkTo(questGiver);
```

`TalkTo` works under any targeting mode, including `LookAt` and `Proximity` — it does not require `Manual`. Under an automatic mode, the next evaluation can move the conversation again once the player looks elsewhere or moves. Choose `Manual` when nothing but scripted calls should ever move the target.

{% hint style="info" %}
If the player is mid-sentence when `TalkTo` is called, the request is held until that utterance ends, so a call made while the player is speaking does not split their sentence across two characters.
{% endhint %}

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

`ConversationTargetingStatus` names the reason the last targeting decision went the way it did — useful for telling a held target apart from a stuck one, since from the outside they look identical.

## Subscribe to targeting events

```csharp
manager.ConversationTargetRequested += character => ShowHint(character);
manager.ConversationTargetChanged   += character => Confirm(character);
```

`ConversationTargetRequested` fires after the SDK closes player input and immediately before it attempts to send the target change; the send can still fail. `ConversationTargetChanged` fires when an authoritative response from Convai reconciles the route — a round trip later. Anything Convai does as a consequence of the move, including ending the previous character's turn, happens between the two events.

## One character speaks at a time

Calling `TalkTo` ends the previous character's turn immediately, even mid-sentence — see [One character speaks at a time](how-conversation-targeting-works.md#one-character-speaks-at-a-time) for the full rule and how to avoid cutting off a scripted line.

## Verify the change

Call `TalkTo` in Play mode and confirm the conversation moves to the specified character — the character's audio and lip sync should start on the next response, and `ConversationTarget` should return that character.

## Next steps

{% content-ref url="custom-targeting-rule.md" %}
[Write a custom targeting rule](custom-targeting-rule.md)
{% endcontent-ref %}

{% content-ref url="targeting-reference.md" %}
[Conversation targeting reference](targeting-reference.md)
{% endcontent-ref %}
