---
title: Build your first multi-character session
description: Put two or more Convai characters in one Unity scene, connect them as a single shared room, and confirm that the room becomes ready for input.
last_reviewed: "4.6.0"
---

Build a scene in which two Convai characters share one room, connect it from a script, and confirm that both memberships appear in the roster. This page assumes you already have a working single-character scene and want to add a second character to it.

{% hint style="warning" %}
Adding a second `ConvaiCharacter` changes how the whole scene connects. With one registered character the SDK connects a single-character room; with two or more it sends a roster and the session gains a membership layer. Existing code that resolves messages by character ID needs the review described in [Character identity and addressing](character-identity.md).
{% endhint %}

## Prerequisites

- A Unity scene that already contains `ConvaiManager`, `ConvaiRoomManager`, and `ConvaiPlayer`. See [Build a custom scene](../../getting-started/build-a-custom-scene.md) if you are starting from an empty scene.
- A configured API key. See [Configure the API key](../../getting-started/configure-api-key.md).
- Two Character IDs from your Convai dashboard.

## Set up the scene

{% stepper %}
{% step %}
### Add a second character

Add a second `GameObject` with a `ConvaiCharacter` component, alongside the one your scene already has. Give each component a distinct **Character Name** so transcripts and logs stay readable.

Both components register themselves with the manager when the scene loads, which is what makes the room a multi-character room at connect.
{% endstep %}

{% step %}
### Give every character a Character ID

Set the **Character ID** field on both `ConvaiCharacter` components. A character with an empty ID fails the roster validation, and the connect attempt is rejected before any request is sent.

Two characters may use the same Character ID — that creates two independently addressable instances of one character. Give them different IDs for this walkthrough so each roster entry is distinguishable in the Console.
{% endstep %}

{% step %}
### Turn off automatic connection

Select the `GameObject` holding `ConvaiRoomManager` and clear **Connect On Start**. The script you add next sets the conversation target and then connects, which keeps both actions in a known order.
{% endstep %}

{% step %}
### Add the bootstrap script

Create the script below, add it to any `GameObject` in the scene, and assign one of your characters to the **Initial Character** field.

The assignment matters. The SDK infers a conversation target automatically only when the scene owns exactly one character, so a scene with two characters must name the target. That character is placed first in the roster and becomes the room's initial character.
{% endstep %}

{% step %}
### Enter Play mode

Enter Play mode and watch the Console. The script logs one line per membership once the room reports the initial character as ready.
{% endstep %}
{% endstepper %}

## Connect and wait for the room

`ConnectAsync` faults with a `ConvaiOperationException` when the roster is rejected or the connection fails, and its `Code` property carries the session error code. `WaitUntilReadyAsync` faults with an `InvalidOperationException` when the initial character fails to start, carrying the message `Initial character failed to start (<code>).`. Handle both — an unhandled fault in an `async void` method is silently swallowed by Unity.

{% code title="Assets/Scripts/MultiCharacterSessionBootstrap.cs" %}
```csharp
using System;
using System.Threading;
using Convai.Runtime.Components;
using Convai.Runtime.Core.Async;
using Convai.Runtime.Room;
using UnityEngine;

public class MultiCharacterSessionBootstrap : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _initialCharacter;

    private readonly CancellationTokenSource _lifetime = new();

    private async void Start()
    {
        ConvaiManager manager = ConvaiManager.ActiveManager;
        if (manager == null || _initialCharacter == null)
        {
            Debug.LogError("[MultiCharacter] Assign an initial character and add a ConvaiManager to the scene.");
            return;
        }

        manager.SetExplicitConversationTarget(_initialCharacter);

        try
        {
            await manager.ConnectAsync(_lifetime.Token);
        }
        catch (ConvaiOperationException error)
        {
            Debug.LogError($"[MultiCharacter] Connect failed ({error.Code}): {error.Message}");
            return;
        }
        catch (OperationCanceledException)
        {
            return;
        }

        if (!manager.TryGetRoomConnectionService(out IConvaiRoomConnectionService roomService))
            return;

        MultiCharacterRoomSession session = roomService.CurrentMultiCharacterSession;
        if (session == null)
        {
            Debug.LogWarning("[MultiCharacter] Connected as a single-character room. Check that both characters are registered.");
            return;
        }

        try
        {
            await session.WaitUntilReadyAsync(_lifetime.Token);
        }
        catch (InvalidOperationException error)
        {
            Debug.LogError($"[MultiCharacter] {error.Message}");
            return;
        }
        catch (OperationCanceledException)
        {
            return;
        }

        foreach (CharacterRoomMembership membership in session.Characters)
            Debug.Log(
                $"[MultiCharacter] {membership.CharacterId} membership {membership.MembershipId} " +
                $"is {membership.Status} (initial: {membership.IsInitial})");
    }

    private void OnDestroy()
    {
        _lifetime.Cancel();
        _lifetime.Dispose();
    }
}
```
{% endcode %}

## Verify the room

Confirm all four of the following in the Console before you build anything on top of the room.

- `CurrentMultiCharacterSession` is not `null`, which the script reports by not logging the single-character warning.
- `session.Characters` holds one membership per `ConvaiCharacter` in the scene.
- Exactly one membership logs `initial: True`, and it is the character you assigned.
- Every membership has a distinct `MembershipId`.

Speaking to the room now reaches the initial character. Routing input to any other membership is a separate step; the room stays on the initial character until you change the interaction target.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| The Console reports `Room ownership did not resolve an active conversation target.` | The scene owns two or more characters and none was named as the target. | Call `SetExplicitConversationTarget` before connecting, as the script above does. |
| Connect fails with `Every character in a multi-character room requires a Character ID.` | One `ConvaiCharacter` has an empty **Character ID**. | Set the field on every character in the scene, including inactive ones that still register. |
| Connect fails with `Multi-character roster contains null or duplicate character references.` | The same `ConvaiCharacter` component was registered twice. | Register each component once. Use a second component instance to add a clone of the same character. |
| Connect fails with `Multi-character rooms support at most 50 characters.` | More than 50 characters are registered with the manager. | Reduce the registered cast to 50 or fewer before connecting. |
| The script logs the single-character warning | Only one character was registered when the manager connected. | Confirm both `GameObject` instances are active in the scene before the connect call runs. |

## Next steps

Read [Character identity and addressing](character-identity.md) before writing code that maps audio or matches events, then [Roster readiness and partial dispatch](readiness-and-partial-dispatch.md) to handle a character that starts slowly or fails.

{% content-ref url="character-identity.md" %}
[Character identity and addressing](character-identity.md)
{% endcontent-ref %}

{% content-ref url="readiness-and-partial-dispatch.md" %}
[Roster readiness and partial dispatch](readiness-and-partial-dispatch.md)
{% endcontent-ref %}

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}
