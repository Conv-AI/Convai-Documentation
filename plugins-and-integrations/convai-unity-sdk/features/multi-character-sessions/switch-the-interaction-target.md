---
title: Switch the interaction target
description: Route player input to a chosen character in a shared Unity room, and release the target without interrupting the character already speaking.
last_reviewed: "4.6.0"
---

Route player input to one character in a multi-character session with `SetInteractionTargetAsync`, and release it with `ClearInteractionTargetAsync`. Use this page once a room is connected and you need to change which character the player is addressing.

## Prerequisites

- A connected multi-character session. See [Build your first multi-character session](quick-start.md).
- `IConvaiRoomConnectionService`, retrieved with `ConvaiManager.TryGetRoomConnectionService`.
- The `IConvaiCharacterAgent` you want to address, or the `MembershipId` of its `CharacterRoomMembership` from `session.Characters`.

## Set the interaction target

Call `SetInteractionTargetAsync(IConvaiCharacterAgent, CancellationToken)` when you hold a local character instance, or `SetInteractionTargetAsync(string membershipId, CancellationToken)` when you only have the membership ID — for example, a membership without a bound `Character` because the scene has no matching component. Both overloads send the same command and share one gate, so only one target change is in flight at a time; a second call waits for the first to finish.

The command faults with a `TimeoutException` carrying `Timed out waiting for the interaction-target acknowledgement.` if no acknowledgement arrives within 10 seconds.

{% code title="Assets/Scripts/InteractionTargetSwitcher.cs" %}
```csharp
using System;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public class InteractionTargetSwitcher : MonoBehaviour
{
    public async void SwitchTo(IConvaiRoomConnectionService roomService, ConvaiCharacter character)
    {
        try
        {
            InteractionTargetResult result = await roomService.SetInteractionTargetAsync(character);
            Debug.Log($"[MultiCharacter] Target is now {result.ActiveMembershipId} (route epoch {result.RouteEpoch}).");
        }
        catch (InvalidOperationException error)
        {
            Debug.LogError($"[MultiCharacter] Could not switch target: {error.Message}");
        }
        catch (ArgumentException error)
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

`InteractionTargetResult` reports what the SDK applied, which is not always what you requested. This task only needs three of its fields:

| Field | Holds |
| --- | --- |
| `ActiveMembershipId` | The canonical target after this command was processed. |
| `RouteEpoch` | The route epoch that resulted from this command. |
| `Changed` | Whether the canonical target actually moved. |

See [Multi-character room session reference](room-session-reference.md#interactiontargetresult) for the full field list, including `CommandId` and `PreviousMembershipId`.

## Clear the interaction target

Call `ClearInteractionTargetAsync` to route no player input to any character. It shares the same gate, timeout, and exception types as `SetInteractionTargetAsync`.

{% hint style="warning" %}
Clearing the target does not interrupt a character that is already speaking. `ClearInteractionTargetAsync` only stops new input from being routed; audio already in flight plays to completion.
{% endhint %}

```csharp
try
{
    await roomService.ClearInteractionTargetAsync();
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

## Verify the interaction target changed

Check `InteractionTargetResult.Changed` rather than assuming a successful call always moved the target. The SDK discards a stale or duplicate acknowledgement instead of applying it: an acknowledgement whose route epoch is not strictly greater than the session's current `RouteEpoch` is dropped, and the canonical `ActiveMembershipId` is left exactly where it was. `Changed` is `false` in that case, even though the call completed without throwing. See [How multi-character sessions work](how-multi-character-sessions-work.md#epochs-and-the-command-acknowledgement-model) for why the guard exists.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `InvalidOperationException`: `No multi-character room session is active.` | The room connected as a single-character room, or the call ran before connect finished. | Check `CurrentMultiCharacterSession` is not `null` before calling. |
| `ArgumentException`: `The character is not a member of the current room.` | The `IConvaiCharacterAgent` passed to the character overload is not in `session.Characters`. | Add the character first with [Add and remove characters at runtime](update-the-roster.md), or target its membership by ID once it is present. |
| `ArgumentException`: `The membership is not part of the current room.` | The membership ID passed to the string overload does not match any current membership. | Re-read `session.Characters` and use a `MembershipId` that is currently in the roster. |
| `InvalidOperationException`: `The interaction target was removed while this update was waiting.` | Another command removed the target membership while this call was pending. | Re-read `session.Characters` and target a membership that is still present. |
| `InvalidOperationException`: `The multi-character room changed while this update was waiting.` | The session was replaced, typically by a reconnect, while the call was in flight. | Fetch `CurrentMultiCharacterSession` again after the exception and retry against the new session. |
| `TimeoutException`: `Timed out waiting for the interaction-target acknowledgement.` | No response arrived within 10 seconds. | Read `ActiveMembershipId` and `RouteEpoch` before retrying — Convai may already have applied the change. |

## Next steps

{% content-ref url="update-the-roster.md" %}
[Add and remove characters at runtime](update-the-roster.md)
{% endcontent-ref %}

{% content-ref url="handle-roster-events.md" %}
[React to roster and target changes](handle-roster-events.md)
{% endcontent-ref %}

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}
