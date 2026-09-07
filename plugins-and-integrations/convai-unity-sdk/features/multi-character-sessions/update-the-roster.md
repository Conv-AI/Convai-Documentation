---
title: Characters joining and leaving
description: Understand how a Convai character joins or leaves a connected Unity room automatically, and when to edit the roster from code instead.
last_reviewed: "4.6.0"
---

A `ConvaiCharacter` that appears in the scene while the room is connected joins it without a reconnect — instantiating a character prefab or enabling a character `GameObject` is the whole integration. Use this page to understand that automatic behaviour, and to reach for `AddCharacterAsync` or `RemoveCharacterAsync` only when a scene needs to edit the roster deliberately from a script.

## A character that appears joins automatically

Nothing needs calling. Instantiate a second character prefab, or enable a `ConvaiCharacter` `GameObject` that was inactive, and the SDK adds it to the room as soon as the connection accepts the change. The Console confirms it:

```text
'Sofia' joined the room without reconnecting.
```

The character is discovered, injected, and ready the moment it appears — there is nothing else to set up for it to take a seat. It arrives in the roster as `Starting` until Convai announces it; see [Room readiness](readiness-and-partial-dispatch.md) for what that state means and how long it usually lasts.

## Disabling a character keeps its seat

`SetActive(false)` does not remove a character from the room. It keeps its membership and stops being addressable — targeting skips it and it cannot be spoken to — until it is enabled again, which needs no round trip and nothing to wait for. Use disabling for "behind a wall", "pooled", or "hidden for a beat"; it costs nothing to hold the seat open.

A character leaves the room only when the project says so: destroyed, or dropped from ownership. Either way the Console confirms it:

```text
'Sofia' left the room without reconnecting.
```

## A single-character room can't grow

A room that connected with exactly one character is opened for that character alone and carries no roster, so nothing can join it later — it waits for the next connection instead. The Console reports this rather than staying silent:

```text
'James' cannot join this conversation: the room was opened for a single character, so it has no
roster to join. It will be included the next time the room connects. To let characters come and go
during play, have every character you want active in the scene before the room connects — a
character that is present but disabled does not count, because the room is opened for the active
ones.
```

To let characters come and go during play, have more than one character active in the scene **before** the room connects. A character that is present but inactive at connect time does not count toward that — the room is opened for whichever characters are active at that moment.

Two other changes are never applied live, because they decide how the room was created rather than who is in it: a changed player, and a changed **Initial Character**. Either one queues a reconnect instead.

## Edit the roster explicitly from code

Reach for this when a script needs to add or remove a character deliberately — for example, spawning a character only after some other condition, or removing one and handing the conversation to a specific replacement in the same command. Retrieve `IConvaiRoomConnectionService` with `ConvaiManager.TryGetRoomConnectionService`.

### Add a character to the roster

Call `AddCharacterAsync(IConvaiCharacterAgent character, string characterSessionId = null, CancellationToken cancellationToken = default)`. The optional `characterSessionId` resumes that character instance's earlier conversation instead of starting a new one.

Adding the same local character instance twice throws an `ArgumentException` with the message `This local character instance is already a member of the current room. Use another instance when adding a clone.`. To add a clone of a character already in the room, instantiate a second `ConvaiCharacter` component and add that instance instead — it becomes an independently addressable membership even though it shares a `CharacterId` with the original.

The command shares a roster-mutation gate with `RemoveCharacterAsync`, so only one roster change is in flight at a time, and it faults with a `TimeoutException` carrying `Timed out waiting for the character-roster-update acknowledgement.` if no acknowledgement arrives within 15 seconds.

{% code title="Assets/Scripts/RosterAdder.cs" %}
```csharp
using System;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public class RosterAdder : MonoBehaviour
{
    public async void AddToRoom(IConvaiRoomConnectionService roomService, ConvaiCharacter character)
    {
        try
        {
            CharacterRosterUpdateResult result = await roomService.AddCharacterAsync(character);
            foreach (CharacterRoomMembership membership in result.Added)
                Debug.Log($"[MultiCharacter] Added {membership.CharacterId} as {membership.MembershipId}.");
        }
        catch (ArgumentException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
        }
        catch (CharacterRosterUpdateException error)
        {
            Debug.LogError($"[MultiCharacter] Roster update rejected ({error.Code}): {error.Message}");
        }
        catch (InvalidOperationException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
        }
        catch (TimeoutException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
        }
    }
}
```
{% endcode %}

### Remove a character from the roster

Call `RemoveCharacterAsync(IConvaiCharacterAgent character, string replacementTargetMembershipId = null, CancellationToken cancellationToken = default)` when you hold the local instance, or `RemoveCharacterAsync(string membershipId, string replacementTargetMembershipId = null, CancellationToken cancellationToken = default)` when you only have the membership ID.

`replacementTargetMembershipId` is optional, but pass one whenever the membership you are removing currently holds the interaction target — otherwise the target clears to none, and player input stops being routed to anyone until you set a new target. When you do pass one, it must name a membership that is currently in the room and that is not the membership being removed; either violation throws an `ArgumentException` with `The replacement target is not part of the current room.` or `The replacement target cannot be the membership being removed.`.

```csharp
try
{
    CharacterRosterUpdateResult result = await roomService.RemoveCharacterAsync(
        membershipId: assessorMembership.MembershipId,
        replacementTargetMembershipId: trainerMembership.MembershipId);
    Debug.Log($"[MultiCharacter] Active target is now {result.ActiveMembershipId}.");
}
catch (ArgumentException error)
{
    Debug.LogError($"[MultiCharacter] {error.Message}");
}
catch (CharacterRosterUpdateException error)
{
    Debug.LogError($"[MultiCharacter] Roster update rejected ({error.Code}): {error.Message}");
}
catch (InvalidOperationException error)
{
    Debug.LogError($"[MultiCharacter] {error.Message}");
}
catch (TimeoutException error)
{
    Debug.LogError($"[MultiCharacter] {error.Message}");
}
```

`CharacterRosterUpdateException` carries a backend `Code`. Two values are confirmed: `roster_epoch_mismatch`, when another accepted command changed the roster first, and `unauthorized_sender`. Treat any other value as an unrecognized backend rejection and log both `Code` and `Message`.

## Roster limits

A Convai room supports at most 50 characters. The SDK enforces this client-side ceiling on both paths into a roster: the full cast a room connects with, and a single character added later with `AddCharacterAsync`. Either path over the limit fails with the same message, naming the requested count and pointing at **Convai Manager > Characters Joining the Room**:

```text
A Convai room supports at most 50 characters, and this one asks for <count>. The Convai plan for this
API key may allow fewer still; use Convai Manager > Characters Joining the Room to send only the
characters this conversation needs.
```

At connect this surfaces as a `ConvaiOperationException`; from `AddCharacterAsync` it surfaces as a plain `InvalidOperationException`, since it is adding one membership to an already-accepted roster rather than validating a whole connect request.

The roster cannot become empty. If a removal would leave the room with no memberships, Convai rejects it rather than accepting an empty room — see the [Live API roster update rules](../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md#update-the-roster) for the protocol-level statement of that rule.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| A character enabled during play never joins | The room was opened for a single character and carries no roster. Have every character you want active in the scene before it connects. | See [A single-character room can't grow](#a-single-character-room-cant-grow) above. |
| `InvalidOperationException`: `No multi-character room session is active.` | The room connected as a single-character room, or the call ran before connect finished. | Check `CurrentMultiCharacterSession` is not `null` before calling. |
| `ArgumentException`: `The character must have a character ID.` | The `ConvaiCharacter` passed to `AddCharacterAsync` has an empty **Character ID**. | Set the field before adding the character. |
| `ArgumentException`: `This local character instance is already a member of the current room. Use another instance when adding a clone.` | The same component instance was passed to `AddCharacterAsync` twice. | Use a second `ConvaiCharacter` instance to add a clone. |
| `InvalidOperationException`: message starting `A Convai room supports at most 50 characters` | The roster (at connect, or after this add) would exceed 50 characters. | Reduce the cast, or use **Characters Joining the Room** to send only the characters this conversation needs. |
| `CharacterRosterUpdateException` with code `roster_epoch_mismatch` | Another accepted command changed the roster first. | Read `session.RosterEpoch` and retry the mutation. |

## Next steps

{% content-ref url="../conversation-targeting/README.md" %}
[Conversation targeting](../conversation-targeting/README.md)
{% endcontent-ref %}

{% content-ref url="handle-roster-events.md" %}
[Handle room events](handle-roster-events.md)
{% endcontent-ref %}

{% content-ref url="readiness-and-partial-dispatch.md" %}
[Room readiness](readiness-and-partial-dispatch.md)
{% endcontent-ref %}
