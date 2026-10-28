---
title: Extend character behavior
description: Handle character events in priority order with behavior components, and choose when later behaviors in the same dispatcher should receive an event.
last_reviewed: "5.0.0-preview"
---

Add `CharacterBehaviorDispatcher` and components derived from `ConvaiCharacterBehaviorBase` to the same GameObject as `ConvaiCharacter`. The dispatcher discovers behaviors and calls them in descending priority order.

## Add a behavior

The following component updates a scene indicator without reading or logging transcript text. Assign an indicator GameObject in the Inspector.

{% code title="Assets/Scripts/SpeakingIndicator.cs" %}
```csharp
using Convai.Runtime.Behaviors;
using UnityEngine;

public sealed class SpeakingIndicator : ConvaiCharacterBehaviorBase
{
    [SerializeField] private GameObject indicator;

    public override bool OnSpeechStarted(IConvaiCharacterAgent agent)
    {
        if (indicator != null) indicator.SetActive(true);
        return false;
    }

    public override bool OnSpeechStopped(IConvaiCharacterAgent agent)
    {
        if (indicator != null) indicator.SetActive(false);
        return false;
    }

    public override void OnCharacterShutdown(IConvaiCharacterAgent agent)
    {
        if (indicator != null) indicator.SetActive(false);
    }
}
```
{% endcode %}

{% stepper %}
{% step %}
### Add the dispatcher and behavior

Add **Convai > Character Behavior Dispatcher** to the character GameObject, then add `SpeakingIndicator`. Child objects are not searched for behavior components.
{% endstep %}
{% step %}
### Set priority and references

Assign the indicator and set **Priority**. Higher values run first. Keep `false` returns when other behaviors should also receive the event.
{% endstep %}
{% step %}
### Verify event handling

Run a conversation and confirm the indicator follows speech start and stop. After adding behaviors or changing their order dynamically, call `DiscoverBehaviors()` to refresh the dispatcher's list.
{% endstep %}
{% endstepper %}

## Understand the dispatch boundary

Returning `true` from `OnSpokenLine`, `OnSpeechStarted`, `OnSpeechStopped`, or `OnTurnCompleted` stops lower-priority behaviors in this dispatcher. The dispatcher subscribes to public character events; the return value does not cancel audio playback or suppress other event subscribers.

`OnCharacterInitialized` is called when the dispatcher enables; it is not proof the remote character is ready. Use `OnCharacterReady` for the ready notification. Shutdown is called when the dispatcher disables. `OnTurnCompleted` may run while buffered audio is still playing, and its interruption flag reports a cut-short reply. A callback exception is logged and the dispatcher continues to the next behavior.

{% content-ref url="extending-the-sdk.md" %}
[Runtime module system](extending-the-sdk.md)
{% endcontent-ref %}
