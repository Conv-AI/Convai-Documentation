---
title: How body language works
description: Understand how Body Language directs a Convai character's posture, breathing, and gestures every tick, and how it yields to scripted gestures.
last_reviewed: "4.5.0"
---

Every tick, `ConvaiBodyLanguageController` reads the character's dialogue state and emotion, resolves what its behavior should look like right now, and composes that behavior onto the skeleton alongside whatever Body Animation and Gaze are already writing. This page describes what drives that decision, the pieces that produce the motion, and the rule that keeps Body Language from fighting a scripted gesture. For the composition-root model these mechanics build on, see [Character embodiment](../../core-concepts/character-embodiment.md).

***

## What drives the body every tick

In the embodiment `Cognition` tick, the controller reads the character's current [dialogue state](../../core-concepts/dialogue-state.md) and its emotion reading, then resolves the profile's policy for that state — gesticulation intensity, listening lean-in, posture bias, breathing rate and depth, fidget rate. A state change never snaps the policy: values blend over the profile's `Policy Transition Seconds` so a character does not visibly jolt the instant it starts speaking.

In the later `Expression` tick, after the Animator or `PlayableGraph` has posed the skeleton and before Gaze, the controller's solvers spring toward that tick's targets and accumulate every channel — spine, shoulders, pelvis, head-gesture fallback — onto one shared compositor that performs exactly one guarded write per bone. Two Body Language behaviors can never wind up an unbounded delta on the same bone, because there is only ever one writer.

***

## The behaviors that compose onto the body

Internally, ten cooperating pieces each produce one slice of this behavior. None of them are public API — you shape their effect through the profile fields covered in [Tune expressiveness](tune-expressiveness.md) and the [profile reference](profile-reference.md), not by calling them directly.

| Behavior | What it produces |
| --- | --- |
| Posture | The sustained openness, lean, and shoulder-tension silhouette for the current state and emotion. |
| Breathing | The continuous chest and shoulder expansion cycle, plus the catch-breath, sigh, and pre-speech inhale events. |
| Gesticulation | Head beats and posture pulses timed to speech energy while speaking, and idle hand and wrist micro-motion between gestures. |
| Listening posture | The lean-in and stillness that engages while the character is listening. |
| Fidgets | The slow idle weight shift that keeps a still character from reading as frozen. |
| Stance | The periodic pelvis weight-shift and yaw cycle a standing body performs. |
| Postural sway | A continuous, sub-degree drift on the spine that reads as constant micro-balancing rather than jitter. |
| Idle macro-cycle | A very slow, multi-minute drift on breath depth, sway, and fidget cadence so a long idle never settles into a visibly looping baseline. |
| Reactions | One-shot startle flinches and amused bounces, triggered automatically by a sudden emotion spike or on demand. |
| Head gestures | Nods, shakes, and tilts, whether from a co-speech beat, a listening tilt-hold, or a scripted request. |

A camera-distance scale also runs alongside these behaviors: the further the main camera sits from the character, the larger sway and hand micro-motion read, so a small swing does not disappear at a distance and does not look overplayed in a close-up. It never touches breathing, posture, or gestures — only the ambient texture.

***

## How it shares bones with Gaze and Body Animation

Body Language, Gaze, and Body Animation can all have an interest in the same spine, shoulders, and head. Convai resolves this with coordination rather than one module suppressing another: Gaze's own torso-aim behavior composes through the same shared compositor Body Language writes through, so the two never hold separate write guards that could race on the same bone. When Body Animation plays a walk cycle or a full-body action, it takes the body back for the duration — a deliberate hand-off, not a conflict.

{% hint style="info" %}
The contracts behind this coordination — how Gaze registers its torso-aim entry, how Body Animation reports what it is playing — are internal to the package. You do not implement or call them directly; you only see their effect in how the character moves.
{% endhint %}

***

## How it yields to scripted gestures

Body Animation's talk-clip system can report a suppression level every tick, and Body Language's entire co-speech system reads it before deciding how much to do:

| Suppression | Head beats | Posture pulses | Semantic gesture cues | Posture and breathing |
| --- | --- | --- | --- | --- |
| None (or no performer registered) | Full | Full | Eligible | Full weight |
| Upper body (an upper-body talk clip or locomotion is playing) | Full | Reduced | Refused | Posture reduced, breathing stays at full weight |
| Full body (a full-body action or turn is playing) | None | None | Refused | Both fade to zero |

This is why the two modules never look like they are fighting: while Body Animation plays an authored upper-body gesture, Body Language keeps the character breathing and keeps its head beats going, but steps back from adding its own posture pulses on top of the same motion. Breathing deliberately never suppresses, even under full suppression's posture and gesture fade — a character that stops breathing while gesturing reads as broken in a way nothing else does.

***

## Next steps

{% content-ref url="quick-start.md" %}
[Body language quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="tune-expressiveness.md" %}
[Tune expressiveness](tune-expressiveness.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot body language](troubleshooting.md)
{% endcontent-ref %}
