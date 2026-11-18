---
title: React to the player starting to speak
description: React locally to the player starting to talk or pressing push-to-talk, before the service confirms it over the network connection.
last_reviewed: "4.6.0"
---

Whether the player is speaking has always been Convai's own call, announced back over the network — so a character did nothing until that round trip landed, and looked like it noticed the player late. The SDK also watches locally now and publishes `LocalPlayerActivityChanged` the moment it sees local evidence, in both turn-taking modes.

## Prerequisites

- A scene with `ConvaiManager` connected. See [Session lifecycle](../../core-concepts/session-lifecycle.md).

## Subscribe to the event

`LocalPlayerActivityChanged` has no typed property on `ConvaiEvents`, so subscribe through the raw event hub:

```csharp
using Convai.Domain.DomainEvents.Runtime;
using Convai.Domain.EventSystem;
using Convai.Runtime.Components;
using UnityEngine;

public class MicrophoneMeter : MonoBehaviour
{
    private SubscriptionToken _token;

    private void OnEnable()
    {
        var hub = ConvaiManager.ActiveManager?.Events?.Raw;
        if (hub == null) return;

        _token = hub.Subscribe<LocalPlayerActivityChanged>(HandleLocalActivity);
    }

    private void OnDisable()
    {
        ConvaiManager.ActiveManager?.Events?.Raw?.Unsubscribe(_token);
        _token = default;
    }

    private void HandleLocalActivity(LocalPlayerActivityChanged e)
    {
        Debug.Log($"[MicrophoneMeter] {e.Source}: {(e.IsActive ? "active" : "inactive")} ({e.Level:F1})");
    }
}
```

## What each source means

`LocalPlayerActivityChanged.Source` tells you which local evidence raised the event:

| Source | Raised by | Fires when |
| --- | --- | --- |
| `Microphone` | A level gate on the open microphone | The captured audio rises above the room's own learned noise floor. Stays active until it falls back near that floor, so a pause inside a sentence does not flicker the state. |
| `PushToTalk` | The push-to-talk control | The player presses the control — a decision, not a sound, so this fires before the player has said a word. |

The microphone source learns the room's own noise floor rather than using a fixed loudness threshold, so it behaves the same on a quiet headset and a loud desk microphone. It stays closed while a character's own voice is audible through the player's speakers, unless acoustic echo cancellation is genuinely active on the input device — in which case the character's voice never reaches the microphone signal to begin with.

`LocalPlayerActivityChanged.Level` is a ratio above the measured noise floor, useful for a microphone meter. It is `0` for `PushToTalk` and for the falling edge of `Microphone`.

{% hint style="warning" %}
`LocalPlayerActivityChanged` is a hint, not a turn. It is a guess from local evidence and never routes a message, commits a turn, or bills anything. `PlayerSpeakingStateChanged` remains Convai's own verdict — the only event that produces a transcript or moves a character into its listening state.
{% endhint %}

## What a character does with it

A character that notices local activity moves to the **Attending** dialogue state and no further — it cannot reach **Listening**, take a turn, or send anything from this signal alone, so a false positive costs a glance rather than a mistake.

## Whether a character acts on it

Whether this local evidence reaches a character's dialogue state is governed by `noticeYouLocally` on the Conversation Flow profile, which ships on and is not exposed for editing — the profile's Inspector does not draw it, and it has no public setter. Every character therefore acts on local activity, and the `LocalPlayerActivityChanged` event reaches your own code either way. See [Conversation flow reference](../../embodiment/conversation-flow/reference.md) for the rest of the profile's fixed behavior.

## Verify the reaction

Enter Play mode, connect, and either speak into the microphone or press the push-to-talk control. Confirm your subscriber fires immediately, ahead of Convai's transcript for that utterance.

## Next steps

{% content-ref url="../../embodiment/conversation-flow/README.md" %}
[Conversation flow](../../embodiment/conversation-flow/README.md)
{% endcontent-ref %}

{% content-ref url="gate-your-ui.md" %}
[Gate your UI on availability](gate-your-ui.md)
{% endcontent-ref %}
