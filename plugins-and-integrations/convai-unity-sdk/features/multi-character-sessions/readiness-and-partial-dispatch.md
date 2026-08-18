---
title: Roster readiness and partial dispatch
description: Understand when a shared Unity room is ready to take player input, why one slow character does not block the others, and how start failures are reported.
last_reviewed: "4.6.0"
---

Characters in a multi-character room start independently, so the room does not become usable all at once. Readiness is tracked per membership, while the session as a whole reports the readiness of one membership only. Understanding that split explains why a room can be ready while half its cast is still starting, and why a character that never becomes ready is a recoverable condition rather than a connection failure.

***

## The three states a membership can hold

`CharacterRoomStatus` has exactly three values, and `CharacterRoomMembership.Status` always holds one of them.

| Value | Meaning |
| --- | --- |
| `Starting` | The membership exists in the roster and Convai has not yet reported it either way. This is the state every new membership begins in. |
| `Ready` | The character has signalled that it can take input. Routing player input to it is safe from this point on. |
| `Failed` | The character did not start. `FailureCode` carries the reason Convai reported, and the membership stays in the roster. |

Two fields sit behind the status. `ProvisioningStatus` is the raw provisioning string Convai returned for that entry, and `FailureCode` is the reason string attached to a failure. A membership whose `ProvisioningStatus` is `dispatch_failed` is marked `Failed` the moment it is created, without waiting for a separate lifecycle message.

The SDK raises `CharacterStatusChanged` on every transition into `Ready` or `Failed`, and on the insertion of a new membership. A scene that shows per-character availability should drive its UI from that event rather than polling `Status`.

***

## Why session readiness follows the initial character only

`MultiCharacterRoomSession.IsReady` is true when the initial character's status is `Ready`, and is unaffected by every other membership. A ready secondary character does not make the session ready, and a failed secondary character does not make it un-ready.

The reason for that definition is the room's routing model. The initial character is the membership the player addresses when the room opens, so it is the only one the room needs before a conversation can begin. Secondary characters are addressable later, on demand, and the session has no way of knowing which of them a given scene actually requires. Treating any of them as blocking would delay a room that is already usable.

`InitialCharacter` is the membership Convai flagged as initial. When no entry carries that flag, the SDK falls back to the first membership in the roster, so the property is never `null` for a room that has any members at all.

***

## Waiting for the room to become usable

`WaitUntilReadyAsync(CancellationToken)` completes as soon as the initial character reaches `Ready`, and returns immediately when the session is already ready. It faults with an `InvalidOperationException` when the initial character reaches `Failed` instead, carrying the message `Initial character failed to start (<code>).` where `<code>` is the reported failure code, or `unknown` when Convai supplied none.

That fault can arrive before the first `await`. If the connect response already marked the initial character as failed, the wait faults on its first call rather than hanging. Handle the exception on every call site:

```csharp
try
{
    await session.WaitUntilReadyAsync(cancellationToken);
    BeginConversation();
}
catch (InvalidOperationException error)
{
    // The initial character failed to start; the rest of the roster may still be usable.
    ShowInitialCharacterUnavailable(error.Message);
}
```

Waiting for a specific secondary character is a different job. There is no per-membership wait method, so subscribe to `CharacterStatusChanged` and check `Status` on the membership you care about.

***

## Partial dispatch

`PartialDispatch` is set from the connect response and reports whether Convai accepted the roster in full. When it is `true`, at least one requested character did not dispatch, and the affected memberships carry a failed provisioning status and a failure code. The value is fixed for the life of the session — it describes what happened at connect, not the room's current health.

A partially dispatched room is still a working room. The memberships that started are ready or starting normally, and the ones that did not are present in `Characters` with `Status` set to `Failed`. Inspect the roster rather than treating the flag as a connection failure:

```csharp
if (session.PartialDispatch)
{
    foreach (CharacterRoomMembership membership in session.Characters)
    {
        if (membership.Status != CharacterRoomStatus.Failed) continue;
        Debug.LogWarning(
            $"[MultiCharacter] {membership.CharacterId} did not start: " +
            $"{membership.FailureCode ?? "no failure code reported"} ({membership.ProvisioningStatus}).");
    }
}
```

{% hint style="warning" %}
Do not route player input to a membership that is not `Ready`. A membership in `Starting` has no live conversation behind it yet, and one in `Failed` never will.
{% endhint %}

***

## How readiness reaches the client

Two paths mark a membership ready, and both end at the same place.

The direct path is the `character-status` lifecycle message. The SDK resolves the message to a membership, merges the roster epoch it carries, and marks the membership `Ready` or `Failed` from the reported status. A status message for a membership the client has not seen yet inserts that membership into the roster first, so a room can learn about a character and its readiness in the same message.

The second path is inference from observed activity. When a membership is still `Starting` and the SDK observes media, speech, or lip-sync data attributable to it, it marks that membership ready rather than waiting. This keeps a character from being stuck in `Starting` because a status message was lost, and it is why a character can become ready without any explicit lifecycle message appearing.

The session's own connection state follows the initial character. The room reports `Connected` when the initial membership's ready signal arrives, and ready signals from other memberships do not move it.

***

## Design implications of uneven readiness

Treat the roster as a set of independently available characters rather than one unit that is either up or down. Three habits follow from that.

Gate interaction per membership, not per room. Check `Status` on the membership you are about to address, and let the rest of the scene proceed while it is still starting.

Subscribe to `CharacterStatusChanged` for anything that needs to react — enabling a nameplate, unlocking a dialogue prompt, or logging an unavailable character. Polling misses the ordering guarantees the events provide.

Decide up front what a failed secondary character means for your scenario. A training simulation with a required assessor should surface the failure to the facilitator; one with an optional bystander should carry on without it. The SDK reports the failure and keeps the membership in the roster either way, which leaves that decision to the application.

***

## Next steps

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}

{% content-ref url="character-identity.md" %}
[Character identity and addressing](character-identity.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Build your first multi-character session](quick-start.md)
{% endcontent-ref %}
