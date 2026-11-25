---
title: Script the conversation target
description: Move the conversation to a specific character from a script, and choose which character a room opens on when it connects.
last_reviewed: "5.0.0-pre.1"
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

`SetInitialCharacter` chooses which character speaks first when the room connects — a different job from `TalkTo`. It is setup, not steering: it decides where a conversation starts, and calling it on an already-connected room queues a reconnect rather than moving the current conversation. Leave it unset to let the built-in **Look At** or **Proximity** rule select an eligible opening character before connection. Without an eligible proposal, the first connectable character in scene order opens the room. This fallback also applies in **Manual** and when a custom provider is registered.

```csharp
manager.SetInitialCharacter(receptionist);
```

{% hint style="warning" %}
`SetInitialCharacter` only decides who takes the first turn. Once the room is ready, automatic targeting can move the route after another character passes the eligibility, margin, and delay checks. To move the conversation in a live room, call `TalkTo`, not `SetInitialCharacter`.
{% endhint %}

## Read the current target

```csharp
ConvaiCharacter target = manager.ConversationTarget;
ConversationTargetSwitchVerdict why = manager.ConversationTargetingStatus;
```

`ConversationTarget` is the confirmed room route. For UI, `AddressedCharacter` can reflect a pending move, a pre-connect proposal, or a character the player is looking at whose membership is still starting. Bind input availability to `ConversationAvailability` and `Events.OnConversationAvailabilityChanged`; see [Conversation availability](../conversation-availability/README.md).

`ConversationTargetingStatus` names the reason the last targeting decision went the way it did — useful for telling a held target apart from a stuck one, since from the outside they look identical.

## Subscribe to targeting events

Subscribe to `ConvaiManager.Events.OnConversationTargetChanged`. The event carries `Phase`, `CharacterId`, `CharacterName`, `MembershipId`, and a `Reason` on failure. A cleared route can have empty identity fields.

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using UnityEngine;

public sealed class TargetChangeStatus : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;
    private ConvaiEvents _events;

    private void OnDisable()
    {
        if (_events == null) return;
        _events.OnConversationTargetChanged -= HandleTargetChange;
        _events = null;
    }

    private void Update()
    {
        if (_events != null || _manager == null || !_manager.IsInitialized) return;
        _events = _manager.Events;
        _events.OnConversationTargetChanged += HandleTargetChange;
    }

    private static void HandleTargetChange(ConversationTargetChanged change)
    {
        switch (change.Phase)
        {
            case ConversationTargetChangePhase.Requested:
                Debug.Log($"Switching to {change.CharacterName}");
                break;
            case ConversationTargetChangePhase.Confirmed:
                Debug.Log($"Confirmed target: {change.CharacterName}");
                break;
            case ConversationTargetChangePhase.Failed:
                Debug.LogWarning($"Target switch failed: {change.Reason}");
                break;
        }
    }
}
```

`Requested` fires after the SDK pauses player input and before it attempts the send. `Confirmed` reports the authoritative route. Another player's change or a roster handover can be confirmed without a local request. `Failed` reports a refused, superseded, or unsuccessful request and can arrive without a `Requested` phase. A refusal can also carry a newer authoritative route, which the SDK reports as `Confirmed` before reporting the failed request. Await the operation to track the outcome of one specific request.

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
