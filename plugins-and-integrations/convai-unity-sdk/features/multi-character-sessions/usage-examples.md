---
title: Multi-character usage examples
description: Use the manager targeting API for scripted conversations and perform a guarded roster handover after the incoming character becomes ready.
last_reviewed: "5.0.0-pre.1"
---

Use the manager's targeting API to choose who receives player input, and the room service to edit membership. The two examples below assume an established classic multi-character session.

## Scripted targeting

For ordinary look-based targeting, choose **Look At** in **Who The Player Talks To**; no custom raycast is needed. For application-owned choices, set **Chosen By > Manual** and call `TalkTo` or await `TalkToAsync`. Otherwise the manager's automatic rule can select another character on its next evaluation.

This helper awaits the manager API and returns the current canonical target. Its caller should handle failures and observe the manager's Requested, Confirmed, and Failed target phases.

```csharp
using System;
using System.Threading.Tasks;
using Convai.Runtime.Components;

public static class ScenarioTargeting
{
    public static async Task<ConvaiCharacter> AddressAsync(
        ConvaiManager manager, ConvaiCharacter character)
    {
        if (manager == null) throw new ArgumentNullException(nameof(manager));
        if (character == null) throw new ArgumentNullException(nameof(character));
        await manager.TalkToAsync(character);
        return manager.ConversationTarget;
    }
}
```

The manager can defer a request while the player's utterance is in progress. A result with `Changed == false` can mean the target was already current; read `ConversationTarget` or the session's `ActiveMembershipId` rather than resending every frame until Changed becomes true. Target operations cannot retract an already-sent command through cancellation.

Canonical room target updates, including another player's choice, update the manager's target state and Confirmed events. They need not have a local Requested phase.

## Scripted roster handover

Keep the outgoing and incoming characters selected while the new character joins. Wait for the new character’s readiness and confirm the target change before removing the outgoing character from the selection.

```csharp
using System.Threading.Tasks;
using Convai.Runtime.Components;

public static class RosterHandover
{
    public static async Task HandoverAsync(
        ConvaiManager manager, ConvaiCharacter outgoing,
        ConvaiCharacter incoming, ConvaiCharacter companion)
    {
        manager.SetCharactersToConnect(new[] { outgoing, incoming, companion });
        await incoming.WaitForCharacterReadyAsync().AsTask();
        await manager.TalkToAsync(incoming).AsTask();
        manager.SetCharactersToConnect(new[] { incoming, companion });
    }
}
```

This example uses an existing roster room and three scene character references. In your caller, handle a refused or failed join and leave the outgoing character selected when the handover cannot complete. Subscribe to `OnRoomRosterChanged` for the join and departure outcomes.

## Next steps

{% content-ref url="update-the-roster.md" %}
[Characters joining and leaving](update-the-roster.md)
{% endcontent-ref %}
{% content-ref url="troubleshooting.md" %}
[Troubleshoot multi-character sessions](troubleshooting.md)
{% endcontent-ref %}
