---
title: Show connection and audio levels
last_reviewed: "5.0.0-preview"
description: Show character readiness, microphone and voice levels, connection quality, and the waiting period before a reply in your scene interface.
---

Use character availability for a ready-to-talk indicator, audio levels for meters, and `IsAwaitingReply` for a waiting indicator. These signals answer different questions. A connected room can still be waiting for its character, and a zero audio reading can mean that measurement is unavailable.

## Add the built-in indicators

`ConnectionStatusIndicator` and `PlayerSpeakingIndicator` are in `Convai.Runtime.Presentation.Views.Transcript`. Both shipped chat prefabs include them.

{% stepper %}
{% step %}
### Assign connection indicator references

Add `ConnectionStatusIndicator` to your UI and assign `statusIndicator` (`Image`) and `statusText` (`TMP_Text`). Keep **Report Character Availability** enabled for ready-to-talk feedback. It shows **Getting ready** while the character is preparing and **Connected** for ready or answering states. Turning that option off makes the display report session transport state instead.
{% endstep %}
{% step %}
### Assign the speaking indicator

Add `PlayerSpeakingIndicator` and assign `microphoneIndicator`, or place it on the same object as the `Image`. The script defaults to alpha `1` while speaking and `0.5` while silent, with smooth transitions at speed `8`. It listens to speaking-state events; it is not a microphone amplitude meter.
{% endstep %}
{% step %}
### Initialize and check the indicators

Ensure `ConvaiManager` is initialized when the indicators resolve their services. If you create it later, inject the required services or re-enable the indicators after initialization. Connect and verify the status passes through readiness; speak and verify the microphone image changes opacity.
{% endstep %}
{% endstepper %}

## Draw microphone and character meters

Assign the scene's public `ConvaiRoomManager` component directly to your script. Assign the character's `ConvaiAudioOutput` separately. Do not access the manager's internal room reference.

The following example displays linear readings in sliders configured with a `0..1` range. It hides unavailable meters instead of labeling them as silence:

```csharp
using Convai.Runtime.Adapters.Networking;
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.UI;

public class ConversationMeters : MonoBehaviour
{
    [SerializeField] private ConvaiRoomManager room;
    [SerializeField] private ConvaiAudioOutput voice;
    [SerializeField] private Slider microphoneMeter;
    [SerializeField] private Slider voiceMeter;
    [SerializeField] private GameObject waitingIndicator;

    private void Update()
    {
        SetMeter(microphoneMeter, room != null && room.IsMicrophoneLevelAvailable,
            room != null ? room.MicrophoneLevel : 0f);
        SetMeter(voiceMeter, voice != null && voice.IsVoiceLevelAvailable,
            voice != null ? voice.VoiceLevel : 0f);
        if (waitingIndicator != null)
            waitingIndicator.SetActive(room != null && room.IsAwaitingReply);
    }

    private static void SetMeter(Slider meter, bool available, float value)
    {
        if (meter == null) return;
        meter.gameObject.SetActive(available);
        if (available)
            meter.value = Mathf.Lerp(meter.value, Mathf.Clamp01(value),
                1f - Mathf.Exp(-12f * Time.unscaledDeltaTime));
    }
}
```

The smoothing rate `12` is an example UI choice. Both readings are linear and unsmoothed, and device or voice gain affects their size. A decibel display can use `20 * log10(level)` with a positive floor before taking the logarithm. Poll from the main thread once per frame.

`MicrophoneLevel` reads the SDK capture path, or the published browser microphone track on WebGL. Check `IsMicrophoneLevelAvailable`: custom sources without measurement, unpublished microphones, and WebGL transport in the Editor can be unavailable. A muted microphone can still be measurable while reporting zero. An input level does not prove the audio was delivered to Convai.

`VoiceLevel` measures the character playback path. On native platforms it follows output gain and spatial attenuation. Browser playback uses Web Audio; Unity's `AudioListener.volume` and distance rolloff do not affect that browser voice. WebGL measurement can remain unavailable until audio is unlocked by a user gesture. The first native read after a track arrives can be zero.

## Report connection quality

`ConvaiRoomManager.ConnectionQuality` returns the local participant's reported media connection quality: `Unknown`, `Lost`, `Poor`, `Good`, or `Excellent` from `Convai.Infrastructure.Networking`. Observe `ConnectionQualityChanged` for changes on the main thread, and unsubscribe when your UI is disabled.

Treat `Unknown` as unavailable information. It can occur before the first report and after a session ends. The value describes the player's link, not the character's connection or guaranteed response latency. Pair a low-quality label with the existing readiness indicator instead of using it as a send-permission check.

## Show the wait before a reply

`IsAwaitingReply` and `AwaitingReplyChanged` describe the interval after a player turn finishes and before its addressed reply starts. A typed send starts the wait immediately. Voice waits for a non-empty final transcript and the end of the player's turn, including release of push-to-talk.

The wait ends on reply speech or completion, relevant no-reply or failure signals, leaving the connected session state, or the no-progress timeout. The timeout is 30 seconds without a reply signal and is held while a reply tool runs. It is evaluated in the enabled room manager's `Update`. This indicator is separate from animation Thinking state and from push-to-talk's whole-turn completion state.

## Troubleshooting

| Symptom | Cause | Fix and verification |
| --- | --- | --- |
| Connected is shown before the character can answer | Indicator reports transport state | Enable **Report Character Availability** and verify the preparing state |
| A meter always reads zero | Unavailable measurement, mute, or silence | Inspect its availability property, microphone policy, and mute state; speak after availability becomes true |
| WebGL voice meter is unavailable | Browser audio has not been unlocked or cannot be measured | Use the audio-enable interaction, then inspect availability again |
| Quality is Unknown after connection | No quality report has arrived | Keep an unknown state until the event supplies a report |
| Waiting stays visible while room manager is disabled | Its timeout cannot update | Keep the room manager enabled during the session and verify the indicator clears |

## Next steps

{% content-ref url="../troubleshooting/audio-and-microphone-issues.md" %}
[Audio and microphone issues](../troubleshooting/audio-and-microphone-issues.md)
{% endcontent-ref %}
