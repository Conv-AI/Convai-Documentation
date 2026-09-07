---
title: Write a custom targeting rule
description: Replace conversation targeting with your own rule when none of the built-in modes fit how your game chooses who to address.
last_reviewed: "4.6.0"
---

Implement `IConversationTargetProvider` when none of the three built-in targeting modes fit your game — the character a UI list has selected, the one a quest is currently about, or the one standing in a trigger volume. Use this page instead of falling back to `Manual` and rebuilding the parts of targeting that already work correctly.

## Prerequisites

- Familiarity with the model in [How conversation targeting works](how-conversation-targeting-works.md)
- A rule for choosing a target that the three built-in modes cannot express

## Implement the interface

`IConversationTargetProvider` has a single method, `ResolveTarget`, called on every targeting evaluation.

```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.Conversation;
using UnityEngine;

public sealed class QuestTargetProvider : MonoBehaviour, IConversationTargetProvider
{
    public ConvaiCharacter ResolveTarget(
        IReadOnlyList<ConvaiCharacter> candidates, ConvaiCharacter current) =>
        QuestState.CurrentSpeaker ?? current;

    private void Start() =>
        ConvaiManager.ActiveManager.SetConversationTargetProvider(this);
}
```

`candidates` lists every character currently in the room, in stable order, and is never null or empty when `ResolveTarget` is called. `current` is the character currently holding the conversation, or `null` when none does.

Return the character the player should be addressing. Return `null` to leave the conversation where it is. Returning a character that is not in `candidates` also leaves the conversation where it is.

## Register the provider

```csharp
ConvaiManager manager = ConvaiManager.ActiveManager;
manager.SetConversationTargetProvider(new QuestTargetProvider());
```

Pass `null` to `SetConversationTargetProvider` to remove the custom provider and restore the behavior configured by `ConversationTargeting.Mode`.

{% hint style="info" %}
A registered provider replaces the built-in modes outright, including `LookAt` and `Proximity`. The `ConversationTargeting` settings on `ConvaiManager` have no effect while a provider is active.
{% endhint %}

## What still applies on top of your rule

A provider only chooses which character to address. Everything that keeps the choice pleasant still applies on top of what the provider returns: the conversation still never moves mid-sentence, it still does not commit to a new target on the first frame it becomes a valid choice, and it still never leaves the player with nobody listening. See the three rules in [How conversation targeting works](how-conversation-targeting-works.md) for what this means in practice.

If `ResolveTarget` throws, the SDK catches the exception, logs it, and leaves the conversation where it is rather than letting one faulty provider take the conversation down.

## Verify the provider is active

Enter Play mode and confirm the conversation follows your custom rule rather than the player's view or position. Check the Live section of the `ConvaiManager` Inspector — it reports the addressed character and the verdict behind the last targeting decision regardless of whether a built-in mode or a custom provider produced it.

## Next steps

{% content-ref url="script-the-conversation-target.md" %}
[Script the conversation target](script-the-conversation-target.md)
{% endcontent-ref %}

{% content-ref url="targeting-reference.md" %}
[Conversation targeting reference](targeting-reference.md)
{% endcontent-ref %}
