---
title: Gaze
description: Find guides for adding eye contact and gaze behavior to a Convai character, and see how Gaze replaces the retired Attention module.
last_reviewed: "4.5.0"
---

Gaze is the Convai embodiment module that decides where a character looks: eye contact with the player, glances at objects and other characters, and full-body turns when the player moves out of view. One component, `ConvaiGazeController`, drives the eyes, head, and body together so the character's attention reads as a single coherent behavior instead of separate systems fighting for the same bones. Gaze replaced the previous gaze implementation and the entire Attention module in SDK 4.5.0 — see [Migrate from Attention](migrate-from-attention.md) if your project was built against either one.

***

## What gaze gives a character

| Behavior | What it looks like |
| --- | --- |
| Eye contact | The character's eyes and head track the player while listening and speaking, and look away naturally between turns. |
| Attention shifts | Glances at scene objects, other Convai characters, and whatever the player is currently looking at. |
| Body turns | The character turns its body, not only its head, when the player moves far enough off-axis or walks behind it. |
| Conversation awareness | Engagement, aversion, and body participation all scale with the character's current dialogue state instead of running on a fixed loop. |

Add `ConvaiGazeController` to a character through **Convai > Embodiment > Gaze** and it works immediately on the SDK's built-in tuning — no profile asset or additional setup is required to see eye contact in Play mode.

***

## How it decides what to look at

Every tick, Gaze resolves a target from the available candidates, decides how strongly to commit to it based on the character's dialogue state, and moves the eyes, head, and body in that order to reach it. [How gaze works](how-gaze-works.md) covers target priority, the eye-then-head-then-body movement chain, and how [dialogue state](../../core-concepts/dialogue-state.md) drives engagement.

***

## Where to start

{% content-ref url="quick-start.md" %}
[Gaze quick start](quick-start.md)
{% endcontent-ref %}

***

## Explore gaze

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How gaze works</strong><br>Target priority, the eye-then-head-then-body movement chain, and how dialogue state drives engagement.</td><td><a href="how-gaze-works.md">how-gaze-works.md</a></td></tr><tr><td><strong>Gaze quick start</strong><br>Add the Gaze component to a character and see eye contact working in Play mode.</td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Configure eye contact</strong><br>Set how strongly a character commits to the player, from natural behavior to a permanent lock.</td><td><a href="configure-eye-contact.md">configure-eye-contact.md</a></td></tr><tr><td><strong>Gaze targets and providers</strong><br>Mark scene objects as worth looking at and register a custom target source.</td><td><a href="targets-and-providers.md">targets-and-providers.md</a></td></tr><tr><td><strong>Scripted gaze</strong><br>Direct a character's gaze from code with GazeAt and GlanceAt.</td><td><a href="scripted-gaze.md">scripted-gaze.md</a></td></tr><tr><td><strong>Gaze profile reference</strong><br>Every setting group on ConvaiGazeProfile, with defaults.</td><td><a href="profile-reference.md">profile-reference.md</a></td></tr><tr><td><strong>Gaze scripting reference</strong><br>The ConvaiGazeController public API: readings, handles, and enums.</td><td><a href="scripting-reference.md">scripting-reference.md</a></td></tr><tr><td><strong>Migrate from Attention</strong><br>What replaces each retired Attention component, and what changes visually with no code change.</td><td><a href="migrate-from-attention.md">migrate-from-attention.md</a></td></tr><tr><td><strong>Gaze usage examples</strong><br>Training, interview, and multi-character scenarios.</td><td><a href="usage-examples.md">usage-examples.md</a></td></tr><tr><td><strong>Troubleshoot gaze</strong><br>Eyes static, head not turning, and targets never selected.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>
