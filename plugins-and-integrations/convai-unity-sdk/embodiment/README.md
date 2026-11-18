---
title: Embodiment
description: Find the modules that give a Convai character eye contact, gestures, posture, and expression, and learn which one to add first.
last_reviewed: "4.5.0"
---

A Convai character that only talks can feel static: its eyes stay fixed on nothing, its posture never shifts, and its face does not react to what it is saying. Embodiment is Convai's name for the group of components that give a character that missing behavior — where it looks, how it moves, how it holds itself, and what its face shows while it speaks. Each module is optional and works on its own, so add the ones your project needs and leave the rest out.

***

## The five embodiment modules

| Module | Component | What it does for the character |
| --- | --- | --- |
| Conversation Flow | `ConvaiConversationFlowController` | Tracks whether the character is idle, listening, thinking, or speaking. The other four modules read this state instead of tracking their own. |
| Gaze | `ConvaiGazeController` | Decides where the character looks — eye contact with the player, glances, and attention shifts. |
| Body Animation | `ConvaiBodyAnimationController` | Plays idles, talk motion, walking, and gestures from an animation set. |
| Body Language | `ConvaiBodyLanguageController` | Adds ambient posture, breathing, and small reactive movements that keep the body alive between deliberate actions. |
| Emotion | `ConvaiEmotionController` | Drives facial expression and mood, partly from signals that arrive with Convai's response. |

All five derive from the same base module and register with one shared object per character, so they cooperate instead of overriding each other. See [Character embodiment](../core-concepts/character-embodiment.md) for that shared model, and [Dialogue state](../core-concepts/dialogue-state.md) for the state Conversation Flow tracks.

***

## Where to start

Add **Gaze** first. It is a single component, needs no animation set or profile to author, and its effect — the character making eye contact with the player — is the easiest embodiment behavior to recognize in Play mode. Conversation Flow is foundational, but you rarely add it yourself: Convai adds it automatically the first time another module needs a dialogue state to read.

{% content-ref url="quick-start.md" %}
[Embodiment quick start](quick-start.md)
{% endcontent-ref %}

***

## The modules

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Gaze</strong><br>Eye contact, glances at objects and other characters, and body turns toward what the character is attending to.</td><td><a href="gaze/README.md">gaze</a></td></tr><tr><td><strong>Body animation</strong><br>Idles, talk motion, walking, gestures, and pointing, played from an animation set with no Animator Controller to author.</td><td><a href="body-animation/README.md">body-animation</a></td></tr><tr><td><strong>Body language</strong><br>Continuous ambient motion — posture, breathing, weight shifts, fidget, and reaction beats.</td><td><a href="body-language/README.md">body-language</a></td></tr><tr><td><strong>Conversation flow</strong><br>The dialogue-state clock the other modules read to time themselves.</td><td><a href="conversation-flow/README.md">conversation-flow</a></td></tr><tr><td><strong>Emotion</strong><br>Facial expression and longer-lived mood, driven by signals that arrive with Convai's response or set from your own code.</td><td><a href="emotion/README.md">emotion</a></td></tr></tbody></table>

***

## Explore embodiment

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How embodiment works</strong><br>The runtime picture: what Convai provisions per character and the order modules run in.</td><td><a href="how-embodiment-works.md">how-embodiment-works.md</a></td></tr><tr><td><strong>Embodiment quick start</strong><br>Add one module to an existing character and see it working in Play mode.</td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Character rig setup</strong><br>How Convai detects bones and blendshapes, and when to override the mapping.</td><td><a href="character-rig-setup.md">character-rig-setup.md</a></td></tr><tr><td><strong>Embodiment presets</strong><br>Bundle every module's settings into one asset and swap it at runtime.</td><td><a href="embodiment-presets.md">embodiment-presets.md</a></td></tr><tr><td><strong>Facial composition</strong><br>How Emotion and LipSync share the mouth, brow, and other facial regions.</td><td><a href="facial-composition.md">facial-composition.md</a></td></tr><tr><td><strong>Embodiment Editor window</strong><br>The Setup, Presets, and Live tabs for inspecting a character's embodiment state.</td><td><a href="embodiment-editor.md">embodiment-editor.md</a></td></tr><tr><td><strong>Embodiment scripting reference</strong><br>The public embodiment API shared across modules.</td><td><a href="scripting-reference.md">scripting-reference.md</a></td></tr><tr><td><strong>Troubleshoot embodiment</strong><br>Diagnose rigs Convai could not detect, missing bones, and modules that are not ticking.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>
