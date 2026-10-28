---
title: Multi-character usage examples
description: Use the manager targeting API for scripted conversations and perform a guarded roster handover after the incoming character becomes ready.
last_reviewed: "5.0.0-preview"
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

Canonical room target updates, including another player's choice, update the manager's target state and Confirmed events. They need not have a local Requested phase. The removed room-level `SetInteractionTargetAsync` API is not the 5.0 scripting path.

## Scripted roster handover

Use this helper when the scenario owns an explicit transition. Avoid racing the automatic live roster: first decide whether that system or your code owns the add. The helper reuses a membership already present, guards an empty add result, and waits through the membership's built-in readiness API.

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Convai.Runtime.Components;
using Convai.Runtime.Room;

public static class ScenarioRoster
{
    public static async Task<CharacterRosterUpdateResult> ReplaceAsync(
        IConvaiRoomConnectionService roomService,
        ConvaiCharacter outgoing, ConvaiCharacter incoming,
        CancellationToken cancellationToken = default)
    {
        if (roomService == null) throw new ArgumentNullException(nameof(roomService));
        if (outgoing == null) throw new ArgumentNullException(nameof(outgoing));
        if (incoming == null) throw new ArgumentNullException(nameof(incoming));
        var session = roomService.CurrentMultiCharacterSession;
        if (session == null) throw new InvalidOperationException("No roster is active.");

        var incomingMember = session.FindByCharacter(incoming);
        if (incomingMember == null)
        {
            var add = await roomService.AddCharacterAsync(
                incoming, cancellationToken: cancellationToken);
            if (add.Added.Count == 0)
                throw new InvalidOperationException("The add returned no membership.");
            incomingMember = add.Added[0];
        }
        await incomingMember.WaitUntilReadyAsync(cancellationToken);

        if (!ReferenceEquals(session, roomService.CurrentMultiCharacterSession))
            throw new InvalidOperationException("The room changed during the handover.");
        var outgoingMember = session.FindByCharacter(outgoing);
        if (outgoingMember == null)
            throw new InvalidOperationException("The outgoing character has already left.");

        return await roomService.RemoveCharacterAsync(
            outgoingMember.MembershipId, incomingMember.MembershipId, cancellationToken);
    }
}
```

Both characters require distinct Character IDs and Live versions. The awaited helper propagates `ConvaiOperationException`, `CharacterRosterUpdateException`, argument errors, readiness failures, timeout, and cancellation to the scenario owner; catch them there and keep the current roster visible instead of hiding a failed handover.

If the incoming member fails, leaves, or its session retires before readiness, `WaitUntilReadyAsync` faults and the helper does not remove the outgoing character. An accepted removal with the replacement raises one handover event followed by `CharacterRemoved`. A caller timeout can leave a command pending until canonical recovery finishes; inspect session state before retrying.

## Next steps

{% content-ref url="update-the-roster.md" %}
[Characters joining and leaving](update-the-roster.md)
{% endcontent-ref %}
{% content-ref url="troubleshooting.md" %}
[Troubleshoot multi-character sessions](troubleshooting.md)
{% endcontent-ref %}
