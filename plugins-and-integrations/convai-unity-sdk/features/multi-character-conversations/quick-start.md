---
title: Multi-character conversations quick start
description: >-
  Build a Unity scene where two Convai characters share one room, then confirm
  the initial character is ready for player input.
last_reviewed: "4.6.0"
---

We will connect two active Convai characters through one room and confirm that the selected initial character is ready. The result is a shared roster that can accept runtime target changes without opening another connection.

## What we will build

The scene starts with one `ConvaiManager`, one `ConvaiRoomManager`, one `ConvaiPlayer`, and two active `ConvaiCharacter` instances. A small bootstrap component declares room ownership during `Awake`, selects the initial character, and connects during `Start`.

## Prerequisites

- A scene that passes [Validate your setup](../../getting-started/validate-your-setup.md)
- **Starts Connected** disabled in the `ConvaiRoomManager` **Connection** section
- At least two active and enabled `ConvaiCharacter` instances with configured audio output
- A different non-empty **Character ID** on each character

{% hint style="warning" %}
Do not reuse one **Character ID** for both characters in this walkthrough. Membership-aware APIs can distinguish local instances, but character-ID-keyed audio and registry operations cannot promise independent behavior for duplicate IDs.
{% endhint %}

## Configure the shared startup roster

{% stepper %}
{% step %}
### Add the bootstrap component

Create `Assets/Scripts/MultiCharacterBootstrap.cs` and add it to an empty `GameObject` in the scene.

{% code title="Assets/Scripts/MultiCharacterBootstrap.cs" lineNumbers="true" overflow="wrap" %}
```csharp
using System;
using System.Collections.Generic;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public sealed class MultiCharacterBootstrap : MonoBehaviour
{
    [SerializeField] private ConvaiManager manager;
    [SerializeField] private ConvaiCharacter[] roomCharacters;
    [SerializeField] private ConvaiCharacter initialCharacter;

    private void Awake()
    {
        try
        {
            ValidateConfiguration();

            // Configure ownership before ConvaiRoomManager performs startup composition.
            manager.SetExplicitCharacters(roomCharacters);
            manager.SetExplicitConversationTarget(initialCharacter);
        }
        catch (Exception exception)
        {
            Debug.LogError($"Multi-character configuration failed: {exception.Message}", this);
            enabled = false;
        }
    }

    private async void Start()
    {
        try
        {
            await manager.ConnectAsync();

            if (!manager.TryGetRoomConnectionService(out IConvaiRoomConnectionService roomService))
                throw new InvalidOperationException("The room connection service is unavailable.");

            MultiCharacterRoomSession session = roomService.CurrentMultiCharacterSession
                ?? throw new InvalidOperationException("A multi-character room was not created.");

            await session.WaitUntilReadyAsync();

            Debug.Log(
                $"Multi-character room ready: roster={session.Characters.Count}, " +
                $"initial={session.InitialCharacter.CharacterId}");
        }
        catch (Exception exception)
        {
            Debug.LogError($"Multi-character startup failed: {exception.Message}", this);
        }
    }

    private void ValidateConfiguration()
    {
        if (manager == null)
            throw new InvalidOperationException("Assign a ConvaiManager.");
        if (initialCharacter == null)
            throw new InvalidOperationException("Assign an initial character.");
        if (!initialCharacter.isActiveAndEnabled)
            throw new InvalidOperationException("The initial character must be active and enabled.");
        if (roomCharacters == null || Array.IndexOf(roomCharacters, initialCharacter) < 0)
            throw new InvalidOperationException("The initial character must be in Room Characters.");

        int activeCharacterCount = 0;
        var seenCharacters = new HashSet<ConvaiCharacter>();
        var seenCharacterIds = new HashSet<string>(StringComparer.Ordinal);
        foreach (ConvaiCharacter character in roomCharacters)
        {
            if (character == null)
                throw new InvalidOperationException("Room Characters contains an empty reference.");
            if (!seenCharacters.Add(character))
                throw new InvalidOperationException("Room Characters contains the same component more than once.");
            if (string.IsNullOrWhiteSpace(character.CharacterId))
                throw new InvalidOperationException("Every room character needs a non-empty Character ID.");
            if (!seenCharacterIds.Add(character.CharacterId))
                throw new InvalidOperationException("Use a distinct Character ID for every character in this walkthrough.");
            if (character.isActiveAndEnabled)
                activeCharacterCount++;
        }

        if (activeCharacterCount < 2)
            throw new InvalidOperationException("At least two room characters must be active and enabled.");
    }
}
```
{% endcode %}
{% endstep %}

{% step %}
### Assign the room characters

In the `MultiCharacterBootstrap` Inspector, assign the scene's `ConvaiManager`. Add both active character instances to **Room Characters**, then assign one of those instances as **Initial Character**.

The array can also contain inactive characters that you plan to add later. Only active and enabled entries are captured in the startup roster.
{% endstep %}

{% step %}
### Confirm manual connection control

Select the `ConvaiRoomManager`. In **Connection**, confirm that **Starts Connected** is disabled so the room does not connect before `MultiCharacterBootstrap` applies ownership.
{% endstep %}
{% endstepper %}

## Run the shared room

Enter Play mode. The bootstrap applies ownership before room startup, selects the initial character, sends the active character roster, and waits for the initial membership to become ready.

{% hint style="success" %}
The Console reports `Multi-character room ready` with a roster count of at least `2`. `CurrentMultiCharacterSession.IsReady` is `true`, and `ActiveMembershipId` identifies the initial membership.
{% endhint %}

Secondary characters can still be `Starting` when this message appears. Check each membership's `Status` before making application behavior depend on that character.

## Scale the example to ten characters

The same bootstrap supports a ten-character staging scenario: assign ten distinct `ConvaiCharacter` instances to **Room Characters**, keep all ten active and enabled before connection, give every instance a unique non-empty **Character ID**, and select exactly one **Initial Character**. The room becomes connected when that initial membership is ready; inspect the other nine membership statuses individually.

Ten is a validation scenario, not a product maximum. The client rejects more than `50` startup roster entries, while the effective deployment or account limit can be lower. At the reviewed preview commit, runtime add operations do not enforce that total locally, so keep an application-owned cap and confirm the allowed capacity before designing gameplay that requires all ten characters.

## Troubleshoot startup

### A multi-character room was not created

**Symptom:** The bootstrap reports `A multi-character room was not created.`

**Cause:** Fewer than two owned characters were active and enabled when connection started, so the SDK used the legacy single-character path.

**Fix:** Enable at least two entries in **Room Characters**, keep **Starts Connected** disabled, and restart Play mode.

**Verify:** The bootstrap reports a roster count of at least `2`.

### No active conversation target is resolved

**Symptom:** The Console reports `[ConvaiRoomManager] Room ownership did not resolve an active conversation target. Assign an explicit conversation target in ConvaiManager, or ensure ownership resolves to a single character before startup.`

**Cause:** The room connected before the bootstrap assigned **Initial Character**, or the selected character was not part of the explicit list.

**Fix:** Keep **Starts Connected** disabled and assign **Initial Character** to an entry in **Room Characters**.

**Verify:** `session.InitialCharacter.Character` resolves to the selected local `ConvaiCharacter`.

## Next steps

{% content-ref url="choose-active-character.md" %}
[Choose the active character](choose-active-character.md)
{% endcontent-ref %}

{% content-ref url="manage-characters-at-runtime.md" %}
[Manage characters at runtime](manage-characters-at-runtime.md)
{% endcontent-ref %}

{% content-ref url="how-it-works.md" %}
[How multi-character conversations work](how-it-works.md)
{% endcontent-ref %}
