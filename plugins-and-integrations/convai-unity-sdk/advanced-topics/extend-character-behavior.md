---
title: Extend character behavior
description: Move character behavior callbacks to Unity SDK events, choose a character or room listener, and control how long each subscription stays active.
last_reviewed: "5.0.0-pre.1"
---

Subscribe to character events to drive application behavior when one character becomes ready, speaks, or completes a turn.

{% hint style="warning" %}
SDK 5.0 removes the character behavior dispatcher and its priority callbacks. Subscribe to the character or manager event that matches the behavior you need.
{% endhint %}

## Listen to one character

Add this script to a scene object and assign the character. It subscribes while enabled and removes the same handler on disable.

{% code title="Assets/Scripts/ReadyCharacterPanel.cs" %}
```csharp
using Convai.Runtime.Components;
using UnityEngine;

public sealed class ReadyCharacterPanel : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter character;
    [SerializeField] private GameObject readyPanel;

    private void OnEnable()
    {
        character.OnCharacterReady += ShowPanel;
        readyPanel.SetActive(character.IsCharacterReady);
    }

    private void OnDisable() => character.OnCharacterReady -= ShowPanel;

    private void ShowPanel() => readyPanel.SetActive(true);
}
```
{% endcode %}

Put ordered application decisions inside one handler when the order matters. For reactions across the room, subscribe through `ConvaiManager.Events` and filter by character or participant. Use `ConvaiCharacterEventRelay` for reactions configured in the Inspector.

## Verify the behavior

Connect the character and confirm the panel becomes visible when that character is ready. Disable the listener and check that it stops receiving callbacks. For input gating across reconnects, observe [Conversation availability](../features/conversation-availability/README.md).

{% content-ref url="../scripting-reference/character-events.md" %}
[Character events](../scripting-reference/character-events.md)
{% endcontent-ref %}
