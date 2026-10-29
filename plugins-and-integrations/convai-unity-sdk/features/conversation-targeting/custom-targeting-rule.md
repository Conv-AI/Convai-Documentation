---
title: Write a custom targeting rule
description: Replace conversation targeting with your own rule when none of the built-in modes fit how your game chooses who to address.
last_reviewed: "5.0.0-preview"
---

Implement `IConversationTargetProvider` when none of the three built-in targeting modes fit your game — the character a UI list has selected, the one a quest is currently about, or the one standing in a trigger volume. Use this page instead of falling back to `Manual` and rebuilding the parts of targeting that already work correctly.

## Prerequisites

- Familiarity with the model in [How conversation targeting works](how-conversation-targeting-works.md)
- A rule for choosing a target that the three built-in modes cannot express

## Implement the interface

`IConversationTargetProvider` has a single method, `ResolveTarget`. Evaluations run at most 15 times per second in a connected, ready multi-character room. They require a view transform even when your provider does not use it. The SDK skips the provider when the current character can hear and there is no alternative ready character, or an active group conversation holds that target.

```csharp
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.Conversation;
using UnityEngine;

public sealed class QuestTargetProvider : IConversationTargetProvider
{
    public ConvaiCharacter Speaker { get; set; }

    public ConvaiCharacter ResolveTarget(
        IReadOnlyList<ConvaiCharacter> candidates, ConvaiCharacter current) =>
        Speaker != null ? Speaker : current;
}
```

`candidates` lists every ready, active, enabled character in the room, in stable order, and is never null or empty when `ResolveTarget` is called. `current` is the character currently holding the conversation, or `null` when none does.

Return the character the player should be addressing. Returning `null` or a character outside `candidates` produces no proposal. A valid current target remains selected, but lost-target recovery can still choose a ready member.

## Register the provider

```csharp
ConvaiManager manager = ConvaiManager.ActiveManager;
var provider = new QuestTargetProvider();
manager.SetConversationTargetProvider(provider);
// Your quest code can assign provider.Speaker to a member of this room.
```

Pass `null` to `SetConversationTargetProvider` to remove the custom provider and restore the behavior configured by `ConversationTargeting.Mode`.

{% hint style="info" %}
A registered provider replaces the built-in modes outright, including `LookAt` and `Proximity`. The provider replaces range, angle, and margin scoring, including in `Manual` mode. `SwitchDelaySeconds`, player-speech and pending-command gates still apply.
{% endhint %}

## What still applies on top of your rule

A provider only chooses which character to address. Everything that keeps the choice pleasant still applies on top of what the provider returns: automatic commits wait while the player is speaking or a prior request is pending. The configured switch delay still applies, and the SDK can recover a lost target. Scripted and other-player moves can hold a target until your proposal changes. See the rules in [How conversation targeting works](how-conversation-targeting-works.md) for what this means in practice.

If `ResolveTarget` throws, the SDK logs an Error and produces no proposal. A valid current target stays selected; lost-target recovery can still select a ready member. See [Targeting in group and shared rooms](group-and-shared-room-targeting.md).

## Verify the provider is active

Enter Play mode and confirm the conversation follows your custom rule rather than the player's view or position. Check the Live section of the `ConvaiManager` Inspector — it reports the addressed character and the verdict behind the last targeting decision regardless of whether a built-in mode or a custom provider produced it.

## Next steps

{% content-ref url="script-the-conversation-target.md" %}
[Script the conversation target](script-the-conversation-target.md)
{% endcontent-ref %}

{% content-ref url="targeting-reference.md" %}
[Conversation targeting reference](targeting-reference.md)
{% endcontent-ref %}
