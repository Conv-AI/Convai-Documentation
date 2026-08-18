---
title: Add and remove characters at runtime
description: Add and remove characters in a connected Unity room at runtime, including replacement targets, the clone rule, and roster limits.
last_reviewed: "4.6.0"
---

Add a character to a running multi-character session with `AddCharacterAsync`, and remove one with `RemoveCharacterAsync`. Use this page once a room is connected and you need to change its cast without reconnecting.

## Prerequisites

- A connected multi-character session. See [Build your first multi-character session](quick-start.md).
- `IConvaiRoomConnectionService`, retrieved with `ConvaiManager.TryGetRoomConnectionService`.
- For an addition, a `ConvaiCharacter` instance that is not already a member of the room.

## Add a character to the roster

Call `AddCharacterAsync(IConvaiCharacterAgent character, string characterSessionId = null, CancellationToken cancellationToken = default)`. The optional `characterSessionId` resumes that character instance's earlier conversation instead of starting a new one.

This is also the path for a character that was inactive or disabled when the room connected. An inactive `ConvaiCharacter` is excluded from the startup roster without an error, but it stays owned — activate its `GameObject` and component, then call `AddCharacterAsync` with that instance to bring it into the room.

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

## Remove a character from the roster

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

The SDK enforces a 50-character ceiling only on the roster it sends when the room first connects: a scene with more than 50 registered characters fails the connect attempt with a `ConvaiOperationException` carrying `Multi-character rooms support at most 50 characters.`, before any request reaches Convai. See [Build your first multi-character session](quick-start.md#troubleshooting). `AddCharacterAsync` does not repeat that check on the client, since it is adding one membership to an already-accepted roster.

The roster cannot become empty. If a removal would leave the room with no memberships, Convai rejects it rather than accepting an empty room — see the [Live API roster update rules](../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md#update-the-roster) for the protocol-level statement of that rule.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `InvalidOperationException`: `No multi-character room session is active.` | The room connected as a single-character room, or the call ran before connect finished. | Check `CurrentMultiCharacterSession` is not `null` before calling. |
| `ArgumentException`: `The character must have a character ID.` | The `ConvaiCharacter` passed to `AddCharacterAsync` has an empty **Character ID**. | Set the field before adding the character. |
| `ArgumentException`: `This local character instance is already a member of the current room. Use another instance when adding a clone.` | The same component instance was passed to `AddCharacterAsync` twice. | Use a second `ConvaiCharacter` instance to add a clone. |
| `InvalidOperationException`: `The local character was added while this roster update was waiting.` | Another command added the same instance while this call was pending. | Re-read `session.Characters` before retrying. |
| `InvalidOperationException`: `The character membership was removed while this roster update was waiting.` | Another command already removed the membership this call targeted. | Re-read `session.Characters` before retrying. |
| `CharacterRosterUpdateException` with code `roster_epoch_mismatch` | Another accepted command changed the roster first. | Read `session.RosterEpoch` and retry the mutation. |

## Next steps

{% content-ref url="switch-the-interaction-target.md" %}
[Switch the interaction target](switch-the-interaction-target.md)
{% endcontent-ref %}

{% content-ref url="handle-roster-events.md" %}
[React to roster and target changes](handle-roster-events.md)
{% endcontent-ref %}

{% content-ref url="readiness-and-partial-dispatch.md" %}
[Roster readiness and partial dispatch](readiness-and-partial-dispatch.md)
{% endcontent-ref %}
