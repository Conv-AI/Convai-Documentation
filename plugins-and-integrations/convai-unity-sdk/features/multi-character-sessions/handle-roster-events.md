---
title: React to roster and target changes
description: Subscribe to roster and interaction-target events in a shared Unity room, and rely on the order the SDK guarantees between them.
last_reviewed: "4.6.0"
---

Subscribe to `CharacterAdded`, `CharacterRemoved`, `CharacterStatusChanged`, and `InteractionTargetChanged` on `MultiCharacterRoomSession` to react to a roster or target change as it happens. Use this page when your scene needs to update UI, logging, or gameplay state as characters come and go instead of polling the roster.

## Prerequisites

- A connected multi-character session. See [Build your first multi-character session](quick-start.md).
- A reference to the current `MultiCharacterRoomSession`, from `IConvaiRoomConnectionService.CurrentMultiCharacterSession`.

## Subscribe to the roster and target events

| Event | Signature | Raised when |
| --- | --- | --- |
| `CharacterAdded` | `Action<CharacterRoomMembership>` | A membership is added to the room after it was already connected. |
| `CharacterRemoved` | `Action<CharacterRoomMembership>` | A membership is removed from the room. |
| `CharacterStatusChanged` | `Action<CharacterRoomMembership>` | A membership transitions into `Ready` or `Failed`, or a new membership is inserted into the roster. |
| `InteractionTargetChanged` | `Action<CharacterRoomMembership, CharacterRoomMembership>` | The canonical active membership changes; the current membership is `null` when the target is cleared. |

{% code title="Assets/Scripts/MultiCharacterEventLogger.cs" %}
```csharp
using Convai.Runtime.Room;
using UnityEngine;

public class MultiCharacterEventLogger : MonoBehaviour
{
    private MultiCharacterRoomSession _session;

    public void Attach(MultiCharacterRoomSession session)
    {
        Detach();
        _session = session;
        if (_session == null) return;

        _session.CharacterAdded += HandleCharacterAdded;
        _session.CharacterRemoved += HandleCharacterRemoved;
        _session.CharacterStatusChanged += HandleCharacterStatusChanged;
        _session.InteractionTargetChanged += HandleInteractionTargetChanged;
    }

    public void Detach()
    {
        if (_session == null) return;

        _session.CharacterAdded -= HandleCharacterAdded;
        _session.CharacterRemoved -= HandleCharacterRemoved;
        _session.CharacterStatusChanged -= HandleCharacterStatusChanged;
        _session.InteractionTargetChanged -= HandleInteractionTargetChanged;
        _session = null;
    }

    private void HandleCharacterAdded(CharacterRoomMembership membership) =>
        Debug.Log($"[MultiCharacter] Added {membership.CharacterId} ({membership.MembershipId}).");

    private void HandleCharacterRemoved(CharacterRoomMembership membership) =>
        Debug.Log($"[MultiCharacter] Removed {membership.CharacterId} ({membership.MembershipId}).");

    private void HandleCharacterStatusChanged(CharacterRoomMembership membership) =>
        Debug.Log($"[MultiCharacter] {membership.CharacterId} is now {membership.Status}.");

    private void HandleInteractionTargetChanged(CharacterRoomMembership previous, CharacterRoomMembership current) =>
        Debug.Log($"[MultiCharacter] Target changed from {previous?.MembershipId ?? "none"} to {current?.MembershipId ?? "none"}.");

    private void OnDestroy() => Detach();
}
```
{% endcode %}

## The ordering guarantee when the active character is removed

Removing the membership that currently holds the interaction target produces two events in a fixed order: `InteractionTargetChanged` fires first, with the removed membership as `previous` and `null` as `current`, and `CharacterRemoved` fires second. Code that reacts to `CharacterRemoved` can rely on the interaction target already being cleared by the time it runs — no separate check of `ActiveMembershipId` is needed to avoid a stale read.

Passing a replacement target does not suppress that first event. The SDK applies the removal before it applies the new target, so a removal with a replacement fires `InteractionTargetChanged` twice: once with `null` as `current`, then again with the replacement membership. Treat a `null` current target as a transition rather than a terminal state.

A related ordering guarantee applies to additions: when a new membership is inserted, `CharacterAdded` fires before `CharacterStatusChanged` for that same membership. `CharacterAdded` also fires exactly once for a given membership even when Convai's lifecycle message for it arrives before the roster-update acknowledgement does — the SDK deduplicates the two paths rather than raising the event twice.

{% hint style="info" %}
`CharacterAdded` does not fire for the characters present when the room first connects — those memberships are already in `session.Characters` by the time the session object exists. Read the initial roster directly instead of waiting for `CharacterAdded` events for it; the event is for characters added after the room is already up.
{% endhint %}

## Unsubscribe when the session ends

`MultiCharacterRoomSession` is replaced on every reconnect, so a handler attached to one session instance stops receiving events once that instance is discarded. Detach in `OnDisable` or `OnDestroy`, and reattach to the new `CurrentMultiCharacterSession` after `IConvaiRoomConnectionService.Connected` fires again.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `CharacterAdded` never fires for a character the scene started with | Those memberships were populated when the session object was created, not through the runtime-addition code path. | Read `session.Characters` right after connecting instead of waiting for `CharacterAdded`. |
| `InteractionTargetChanged` fires with `current` as `null` unexpectedly | The membership holding the target was removed. This event fires whether or not a replacement target was supplied. | Expected behavior. Pass `replacementTargetMembershipId` to [Add and remove characters at runtime](update-the-roster.md#remove-a-character-from-the-roster) so a second event immediately restores a target, and treat the `null` as a transition. |
| An event you expected does not fire at all | The underlying acknowledgement was a stale or duplicate one and was discarded by the epoch guard. | See [How multi-character sessions work](how-multi-character-sessions-work.md#epochs-and-the-command-acknowledgement-model). |

## Next steps

{% content-ref url="switch-the-interaction-target.md" %}
[Switch the interaction target](switch-the-interaction-target.md)
{% endcontent-ref %}

{% content-ref url="update-the-roster.md" %}
[Add and remove characters at runtime](update-the-roster.md)
{% endcontent-ref %}

{% content-ref url="character-identity.md" %}
[Character identity and addressing](character-identity.md)
{% endcontent-ref %}
