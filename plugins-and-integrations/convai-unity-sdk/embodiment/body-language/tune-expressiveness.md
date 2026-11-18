---
title: Tune expressiveness
description: Make a Convai character's body language read as subtle or theatrical using the expressiveness preset, a runtime override, and per-behavior gains.
last_reviewed: "4.5.0"
---

Set how big, how frequent, and how rich a character's body language reads by choosing an `ExpressivenessPreset` on its `ConvaiBodyLanguageProfile`, or by overriding the dial at runtime through `ConvaiBodyLanguageController.Expressiveness`. Use this page when the shipped `Natural` tuning reads as too flat for a theatrical performer or too busy for a calm, understated character.

***

## Prerequisites

- A character with `ConvaiBodyLanguageController` added — see [Body language quick start](quick-start.md).
- A `ConvaiBodyLanguageProfile` assigned to the component, if you want to author the preset on the asset rather than only override it at runtime. Create one via **Assets > Create > Convai > Embodiment > Body Language Profile**.

***

## Choose an expressiveness preset

`ExpressivenessPreset` is the single dial on the profile's Expressiveness section. Every other amplitude, cadence, and optional-behavior toggle in the profile is scaled by whichever value you set here:

| Preset | Resolved value | Reads as |
| --- | --- | --- |
| `Subtle` | 0.25 | Minimal, understated motion — small amplitudes, slower cadences, and the optional behaviors mostly absent. |
| `Natural` (shipped default) | 0.5 | Clearly visible at a normal 2-meter conversational camera distance, without reading as performative. |
| `Expressive` | 0.75 | Larger, more frequent, more varied motion — an animated, lively character. |
| `Theatrical` | 1.0 | Maximum amplitude, frequency, and richness — a broad, theatrical performer. |
| `Custom` | The profile's own `Custom Expressiveness` field, 0–1 | Full author control over the exact resolved value instead of one of the four fixed anchors. |

Set **Expressiveness Preset** in the profile Inspector's Expressiveness section. Select `Custom` and set **Custom Expressiveness** when none of the four fixed anchors is exactly right.

***

## Override expressiveness at runtime

Set `ConvaiBodyLanguageController.Expressiveness` from a script to change a character's expressiveness without swapping its profile — useful for a character that should read as calmer under stress or livelier when excited:

```csharp
using UnityEngine;
using Convai.Modules.BodyLanguage.Components;

public class SetCharacterExpressiveness : MonoBehaviour
{
    [SerializeField] private ConvaiBodyLanguageController bodyLanguage;

    private void Start()
    {
        bodyLanguage = GetComponent<ConvaiBodyLanguageController>();
        bodyLanguage.Expressiveness = 0.75f;
    }
}
```

`Expressiveness` is a `0..1` float. Setting it wins over the profile's own resolved value until the next profile hot-swap, at which point the override clears and the controller falls back to the new profile's resolved value. Reading the property always returns the effective value as of the most recent tick — the override when you have set one, otherwise the profile's own resolved value.

***

## Understand what the dial actually changes

The resolved `0..1` value derives three separate gains, and each behavior category responds to them differently rather than being scaled by one flat multiplier:

| Gain | What it scales | At `Subtle` | At `Natural` | At `Theatrical` |
| --- | --- | --- | --- | --- |
| Amplitude | Degree and centimeter maxima — posture, breath, sway, stance, reactions, hand micro-motion, beat and pulse intensity | 0.62× | 1× | 1.75× |
| Frequency | How often scheduled behaviors happen — beats, weight shifts, fidgets, listening tilts fire more often as this rises | 0.75× | 1× | 1.5× |
| Richness | How much of the optional-behavior repertoire shows at all — shrugs, idle hand and wrist micro-motion, stance settle-steps | 0.45× | 1× | 1.5× |

Amplitude gain does not apply evenly across posture. The sustained posture silhouette — a character's overall openness, lean, and shoulder tension — gets half-strength amplitude coupling, so even a `Subtle` character still holds a readable shape. Transient motion — posture pulses on a speech beat, the lean-in while listening, a weight shift — gets the full amplitude gain, so `Subtle` still reads as visibly calmer moment to moment.

Breathing rate is never scaled by expressiveness. It is treated as physiology rather than performance, so a `Theatrical` character does not breathe unnaturally fast even though everything else about it is larger.

***

## Apply a demeanor preset for a one-time personality pass

The profile Inspector's **Demeanor** row — `Composed`, `Warm`, `Energetic`, `Reserved` — applies a one-shot multiplier pass over the profile's posture bias, fidget, sway, beat-intensity, and weight-shift-cadence fields when you select it. It is an ordinary, undoable asset edit, not a live-swappable runtime mode like `Expressiveness`.

{% hint style="info" %}
The same four demeanor names appear on the Emotion profile and the Body Animation config, so `Warm` is one word across all three inspectors. Each module still interprets a demeanor in its own terms, and applying one on this profile does not apply it anywhere else.
{% endhint %}

***

## Verify the setting

Enter Play mode and start a conversation. A character set to `Subtle` should hold a noticeably calmer, smaller-motion silhouette while still keeping a readable posture; a character set to `Theatrical` should shift weight and gesture more often and with visibly larger motion. Changing `Expressiveness` at runtime should ramp the difference in smoothly rather than snapping the character between looks.

***

## Next steps

{% content-ref url="gestures-and-reactions.md" %}
[Trigger gestures and reactions](gestures-and-reactions.md)
{% endcontent-ref %}

{% content-ref url="profile-reference.md" %}
[Body language profile reference](profile-reference.md)
{% endcontent-ref %}

{% content-ref url="how-body-language-works.md" %}
[How body language works](how-body-language-works.md)
{% endcontent-ref %}
