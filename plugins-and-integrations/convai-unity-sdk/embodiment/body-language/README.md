---
title: Body language
description: Find guides for adding ambient posture, breathing, weight shifts, and small reactive movements that keep a Convai character's body alive between animations.
last_reviewed: "4.5.0"
---

Body Language is the Convai embodiment module that gives a character continuous, ambient nonverbal behavior: breathing, weight shifts, small gestures, and reactive flinches that never stop between authored actions. Body Animation plays authored clips — a walk cycle, a wave — and Body Language never owns a clip; it only adds small procedural motion on top of whatever the character is already doing. One component, `ConvaiBodyLanguageController`, drives all of it.

***

## What body language gives a character

| Behavior | What it looks like |
| --- | --- |
| Breathing | The chest and shoulders expand and contract on a continuous cycle, with occasional sharper intakes on interruption, a settling sigh, and a deeper breath before the character starts speaking. |
| Weight shifts and sway | The character periodically transfers its weight between feet and drifts gently on the spot, the way a standing body constantly micro-balances rather than holding perfectly still. |
| Gesticulation | While speaking, small head beats and posture pulses ride the character's speech rhythm, and its hands stay subtly alive between authored gestures instead of sitting rigid. |
| Listening posture | While listening, the character leans in slightly and settles into stillness, with an occasional attentive head tilt. |
| Fidgets | While idle or thinking, a slow lateral weight shift keeps the character from looking frozen. |
| Reactions | A sudden emotion spike — surprise, amusement — can trigger a one-shot startle flinch or an amused bounce. |

Add `ConvaiBodyLanguageController` to a character through **Convai > Embodiment > Body Language** and it works immediately on the SDK's built-in tuning — no profile asset is required to see breathing and weight shifts in Play mode.

***

## How it differs from body animation

Body Animation and Body Language both move the character's skeleton, but they solve different problems and never fight over the same motion:

| | Body Animation | Body Language |
| --- | --- | --- |
| What it plays | Authored clips: idles, walk cycles, talk overlays, actions, pointing | No clips at all — continuous procedural motion computed every tick |
| What it owns | The character's locomotion and any deliberate, recognizable motion | Ambient life layered on top: breathing, weight shift, posture, small gestures |
| How the two combine | Plays its clip through the `PlayableGraph` as usual | Adds small, swing-only deltas on top of whatever Body Animation already posed |

A character can carry either module alone, or both together. When both are present, Body Language reduces itself rather than overriding Body Animation — see [How body language works](how-body-language-works.md) for the suppression rule that makes this coexistence reliable.

***

## Where to start

{% content-ref url="quick-start.md" %}
[Body language quick start](quick-start.md)
{% endcontent-ref %}

***

## Explore body language

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How body language works</strong><br>The behavior directors that produce this motion, and how it yields to scripted gestures.</td><td><a href="how-body-language-works.md">how-body-language-works.md</a></td></tr><tr><td><strong>Body language quick start</strong><br>Add the component to a character and see breathing, weight shift, and idle life running.</td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Tune expressiveness</strong><br>Make a character subtle or theatrical with the ExpressivenessPreset dial and per-behavior gains.</td><td><a href="tune-expressiveness.md">tune-expressiveness.md</a></td></tr><tr><td><strong>Trigger gestures and reactions</strong><br>Request a scripted head gesture, a semantic gesture cue, or a one-shot reaction from code.</td><td><a href="gestures-and-reactions.md">gestures-and-reactions.md</a></td></tr><tr><td><strong>Body language profile reference</strong><br>Every ConvaiBodyLanguageProfile field, grouped by section, with defaults.</td><td><a href="profile-reference.md">profile-reference.md</a></td></tr><tr><td><strong>Body language scripting reference</strong><br>The ConvaiBodyLanguageController public API: readings, handles, and enums.</td><td><a href="scripting-reference.md">scripting-reference.md</a></td></tr><tr><td><strong>Troubleshoot body language</strong><br>No motion, motion fighting a scripted animation, and refused gesture requests.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>
