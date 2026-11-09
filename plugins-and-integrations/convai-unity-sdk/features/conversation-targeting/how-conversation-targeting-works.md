---
title: How conversation targeting works
description: Understand how the Convai Unity SDK scores view direction to decide who a player is addressing, and why the decision holds steady between switches.
last_reviewed: "5.0.0-preview"
---

Conversation targeting is the rule `ConvaiManager` runs, fifteen times a second, to decide which character in a multi-character room the player is currently addressing. Understanding the model behind it — how a character is scored, and why the target does not move the instant a better candidate appears — explains why targeting behaves the way it does in training simulations, interactive experiences, and games where a player faces more than one character at once.

## Why targeting lives on the manager, not a component

A scene where one character works must keep working the moment a second one is dropped into it. A rule that only takes effect once somebody finds and adds a targeting component is a manual step by another name, so the policy lives on `ConvaiManager`, the component every working scene already has. There is no collider to add, no layer mask to configure, and no field that must be filled in — a ready room with two active `ConvaiCharacter` components also needs a view transform. The SDK uses **Player Camera**, then `MainCamera`, then the `ConvaiPlayer` transform. Without one, automatic targeting logs a warning and waits.

Rooms with a single character never reach any of this logic. The one character holds the conversation, and there is nothing to decide.

## Scoring the view direction

Under the default mode, targeting reads the player's view direction rather than casting a ray at the scene. A ray needs a collider on every character and a layer mask configured correctly, and it fails silently when either is missing or a stray collider blocks the line of sight. Reading the camera's forward direction instead means a mouse, a gamepad, a touch screen, and a head-mounted display all drive targeting the same way, because none of them changes what the camera is pointed at.

Each ready, active candidate is scored by the angle from the view direction to its aim point, with distance as a tiebreak. The aim point is the humanoid head bone, otherwise the center of enabled renderer bounds, otherwise the character transform. The character with the best score is the character a player is judged to be looking at.

## The eligibility numbers versus the switching numbers

`ConversationTargetingOptions` separates eligibility from switching controls.

`MaxDistance` limits both automatic modes. `MaxAngle` limits `LookAt` only. `Proximity` scores straight-line distance from the view transform. `SwitchMargin` favors the current target by an angle in `LookAt`; `ProximityMargin` gives it a fractional distance advantage in `Proximity`. `SwitchDelaySeconds` requires the proposed target to stay selected before a change.

Without the switching controls, two characters standing near each other would trade the conversation back and forth on sub-degree camera movement, and sweeping the view across a room would hand the conversation to everyone it passes. Both faults are obvious in play and invisible in code, which is why the numbers that prevent them are tuned separately from the numbers that decide eligibility. See [Conversation targeting reference](targeting-reference.md) for the exact fields and defaults.

## Three rules that keep it from being annoying

The automatic policy also accounts for player speech, pending requests, and whether the current target can still hear.

**A glance is not an address.** A character has to be the clearly better choice for a moment before the conversation actually moves to them — a look that passes over a character without settling on them does not redirect the conversation. This is what `SwitchDelaySeconds` and the mode-specific margin enforce together: a challenger has to out-score the current target by the configured margin and hold that lead for the configured delay before targeting commits to the switch.

**The player's own sentence pins the target.** The conversation cannot move part-way through what the player is saying — the back half of a sentence reaching a different character than the front half is not something a later correction can fix. A glance made while the player is mid-utterance is not discarded, though: it is remembered, so a look held through an entire sentence moves the conversation the moment the sentence ends instead of requiring the same look twice.

**The target never clears itself.** When nobody currently qualifies as eligible, the last character addressed keeps the conversation rather than the conversation clearing. If that target is no longer ready and active, automatic targeting can fall back to the first ready member. `Manual` recovers a missing or failed membership, while an explicit clear remains clear.

A scripted move and a move made by another player hold against an unchanged local proposal. An active group conversation holds its current target while that character can hear. See [Targeting in group and shared rooms](group-and-shared-room-targeting.md).

## One character speaks at a time

The SDK routes player input to one conversation target in an ordinary multi-character room. A routing request is asynchronous, so a call to `TalkTo` is not proof that the previous response has ended. A scene where a line must always be heard in full — a briefing, a scripted beat — should either set targeting to `Manual` and move the conversation deliberately, or avoid moving the target while `ConvaiCharacter.IsSpeaking` is true.

## Related concepts

{% content-ref url="../multi-character-sessions/how-multi-character-sessions-work.md" %}
[How multi-character sessions work](../multi-character-sessions/how-multi-character-sessions-work.md)
{% endcontent-ref %}

{% content-ref url="choose-a-targeting-mode.md" %}
[Choose a targeting mode](choose-a-targeting-mode.md)
{% endcontent-ref %}
