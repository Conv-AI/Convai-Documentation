---
title: Conversation targeting
description: Find guides for choosing a targeting mode, tuning it, and scripting which character the player is addressing in a Convai Unity SDK room.
last_reviewed: "4.6.0"
---

Conversation targeting is how the Convai Unity SDK decides which character a player is talking to when a room holds more than one. `ConvaiManager` re-evaluates the decision continuously and moves the conversation to the character the player is addressing, without a component to add or a field that must be filled in.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>How conversation targeting works</strong><br>Understand view-direction scoring, why the target only moves willingly, and why targeting lives on the manager rather than a component.</td><td><a href="how-conversation-targeting-works.md">how-conversation-targeting-works.md</a></td></tr>
<tr><td><strong>Choose a targeting mode</strong><br>Pick between Look At, Proximity, and Manual based on your camera and control scheme.</td><td><a href="choose-a-targeting-mode.md">choose-a-targeting-mode.md</a></td></tr>
<tr><td><strong>Tune conversation targeting</strong><br>Adjust range, look angle, switch margin, and switch delay to fit your scene.</td><td><a href="tune-targeting.md">tune-targeting.md</a></td></tr>
<tr><td><strong>Script the conversation target</strong><br>Move the conversation from code with <code>TalkTo</code>, and set which character a room opens on with <code>SetInitialCharacter</code>.</td><td><a href="script-the-conversation-target.md">script-the-conversation-target.md</a></td></tr>
<tr><td><strong>Write a custom targeting rule</strong><br>Replace the built-in modes entirely by implementing <code>IConversationTargetProvider</code>.</td><td><a href="custom-targeting-rule.md">custom-targeting-rule.md</a></td></tr>
<tr><td><strong>Conversation targeting reference</strong><br>Look up every public member of <code>ConversationTargetingOptions</code> and its defaults.</td><td><a href="targeting-reference.md">targeting-reference.md</a></td></tr>
<tr><td><strong>Troubleshoot conversation targeting</strong><br>Fix a target that will not switch, one that flickers, or one that never moves at all.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr>
</tbody></table>

## How targeting fits into a scene

Targeting only has something to decide once a scene registers more than one `ConvaiCharacter` with `ConvaiManager` — a room with one character has nothing to choose between. The setting lives under **Convai Manager → Who The Player Talks To** in the Inspector, and that section appears only once a second character is present. See [How multi-character sessions work](../multi-character-sessions/how-multi-character-sessions-work.md) for how a room assembles its roster before targeting has anything to act on.

## Next steps

Start with [How conversation targeting works](how-conversation-targeting-works.md) to understand the model, then [Choose a targeting mode](choose-a-targeting-mode.md) to pick the mode that fits your camera and controls.

{% content-ref url="../multi-character-sessions/README.md" %}
[Multi-character sessions](../multi-character-sessions/README.md)
{% endcontent-ref %}
