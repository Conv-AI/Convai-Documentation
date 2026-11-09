---
title: React to the player starting to speak
description: React locally to the player starting to talk or pressing push-to-talk, before the service confirms it over the network connection.
last_reviewed: "5.0.0-preview"
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

public class LocalSpeechActivity : MonoBehaviour
{
    private SubscriptionToken _token;
    private IEventHub _hub;

    private void OnEnable()
    {
        _hub = ConvaiManager.ActiveManager?.Events?.Raw;
        if (_hub == null) return;

        _token = _hub.Subscribe<LocalPlayerActivityChanged>(HandleLocalActivity);
    }

    private void OnDisable()
    {
        _hub?.Unsubscribe(_token);
        _hub = null;
        _token = default;
    }

    private void HandleLocalActivity(LocalPlayerActivityChanged e)
    {
        Debug.Log($"[LocalSpeechActivity] {e.Source}: {(e.IsActive ? "active" : "inactive")} ({e.Level:F1})");
    }
}
```

Enable the subscriber after manager bootstrap so the event hub exists. If your UI outlives or replaces the manager, rebind it to the new hub; the example unsubscribes from the exact hub it used.

## What each source means

`LocalPlayerActivityChanged.Source` tells you which local evidence raised the event:

| Source | Raised by | Fires when |
| --- | --- | --- |
| `Microphone` | A level gate on the open microphone | The captured audio rises above the room's own learned noise floor. Stays active until it falls back near that floor, so a pause inside a sentence does not flicker the state. |
| `PushToTalk` | The push-to-talk control | The player presses the control — a decision, not a sound, so this fires before the player has said a word. |

The microphone source learns the room's own noise floor rather than using a fixed loudness threshold, so its threshold adapts to the input device and room noise. It stays closed while a character's own voice is audible through the player's speakers, unless acoustic echo cancellation is genuinely active on the input device — in which case the gate can use the echo-reduced input. Echo cancellation is not a guarantee that every playback sound disappears.

`LocalPlayerActivityChanged.Level` is the ratio above the measured noise floor captured on the rising edge. It is `0` for `PushToTalk` and the falling edge, and is not a continuous meter. For a meter, read `ConvaiRoomManager.MicrophoneLevel` only when `IsMicrophoneLevelAvailable` is true: it is the RMS level of the latest 20 ms after echo cancellation, normalized to `0`–`1`, and zero while muted. See [Audio API](../../scripting-reference/audio-api.md).

{% hint style="warning" %}
`LocalPlayerActivityChanged` is a hint, not a turn. It is a guess from local evidence and never routes a message, commits a turn, or bills anything. `PlayerSpeakingStateChanged` remains the service-side speaking verdict used for Listening. Read transcript subscriptions for text; the speaking-state event does not carry transcript content.
{% endhint %}

## What a character does with it

A character that notices local activity moves to the **Attending** dialogue state and no further — it cannot reach **Listening**, take a turn, or send anything from this signal alone, so a false positive costs a glance rather than a mistake.

## Whether a character acts on it

Whether this local evidence reaches a character's dialogue state is governed by `noticeYouLocally` on the Conversation Flow profile, which ships on and is not exposed for editing — the profile's Inspector does not draw it, and it has no public setter. A character using Conversation Flow can therefore act on local activity, and the `LocalPlayerActivityChanged` event reaches your own code either way. See [Conversation flow reference](../../embodiment/conversation-flow/reference.md) for the rest of the profile's fixed behavior.

## Verify the reaction

Enter Play mode, connect, and either speak into the microphone or press the push-to-talk control. Confirm your subscriber fires immediately, ahead of Convai's transcript for that utterance.

## Next steps

{% content-ref url="../../embodiment/conversation-flow/README.md" %}
[Conversation flow](../../embodiment/conversation-flow/README.md)
{% endcontent-ref %}

{% content-ref url="gate-your-ui.md" %}
[Gate your UI on availability](gate-your-ui.md)
{% endcontent-ref %}
