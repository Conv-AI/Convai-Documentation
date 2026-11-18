---
title: Gaze
description: Find guides for adding eye contact, attention shifts, and full-body turns to a Convai character with the Gaze embodiment module.
last_reviewed: "4.6.0"
---

Gaze is the Convai embodiment module that decides where a character looks: eye contact with the player, glances at objects and other characters, and full-body turns when the player moves out of view. One component, `ConvaiGazeController`, drives the eyes, head, and body together so the character's attention reads as a single coherent behavior instead of separate systems fighting for the same bones.

## What gaze gives a character

| Behavior | What it looks like |
| --- | --- |
| Eye contact | The character's eyes and head track the player while listening and speaking, and look away naturally between turns. |
| Attention shifts | Glances at scene objects, other Convai characters, and whatever the player is currently looking at. |
| Body turns | The character turns its body, not only its head, when the player moves far enough off-axis or walks behind it. |
| Conversation awareness | Engagement, aversion, and body participation all scale with the character's current dialogue state instead of running on a fixed loop. |

Add `ConvaiGazeController` to a character through **Convai > Embodiment > Gaze** and it works immediately on the SDK's built-in tuning — no profile asset or additional setup is required to see eye contact in Play mode.

## How it decides what to look at

Every tick, Gaze resolves a target from the available candidates, decides how strongly to commit to it based on the character's dialogue state, and moves the eyes, head, and body in that order to reach it. [How gaze works](how-gaze-works.md) covers target priority, the eye-then-head-then-body movement chain, and how [dialogue state](../../core-concepts/dialogue-state.md) drives engagement.

## Where to start

{% content-ref url="quick-start.md" %}
[Gaze quick start](quick-start.md)
{% endcontent-ref %}

## Explore gaze

### Getting started

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How gaze works</strong><br>Target priority, the eye-then-head-then-body movement chain, and how dialogue state drives engagement.</td><td><a href="how-gaze-works.md">how-gaze-works.md</a></td></tr><tr><td><strong>Gaze quick start</strong><br>Add the Gaze component to a character and see eye contact working in Play mode.</td><td><a href="quick-start.md">quick-start.md</a></td></tr></tbody></table>

### Configuring gaze

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Configure eye contact</strong><br>Set how strongly a character commits to the player, from natural behavior to a permanent lock.</td><td><a href="configure-eye-contact.md">configure-eye-contact.md</a></td></tr><tr><td><strong>Gaze targets and providers</strong><br>Mark scene objects as worth looking at and register a custom target source.</td><td><a href="targets-and-providers.md">targets-and-providers.md</a></td></tr><tr><td><strong>Scripted gaze</strong><br>Direct a character's gaze from code with GazeAt and GlanceAt.</td><td><a href="scripted-gaze.md">scripted-gaze.md</a></td></tr></tbody></table>

### Reference

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Gaze profile reference</strong><br>Every setting group on ConvaiGazeProfile, with defaults.</td><td><a href="profile-reference.md">profile-reference.md</a></td></tr><tr><td><strong>Gaze scripting reference</strong><br>The ConvaiGazeController public API: readings, handles, and enums.</td><td><a href="scripting-reference.md">scripting-reference.md</a></td></tr><tr><td><strong>Gaze usage examples</strong><br>Training, interview, and multi-character scenarios.</td><td><a href="usage-examples.md">usage-examples.md</a></td></tr><tr><td><strong>Troubleshoot gaze</strong><br>Eyes static, head not turning, and targets never selected.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>

## Next steps

Gaze is one of five embodiment modules. Add Body Animation next to give the same character idle motion, gestures, and NavMesh-driven movement that Gaze can watch and react to.

{% content-ref url="../body-animation/README.md" %}
[Body Animation](../body-animation/README.md)
{% endcontent-ref %}

{% content-ref url="../README.md" %}
[Embodiment](../README.md)
{% endcontent-ref %}
