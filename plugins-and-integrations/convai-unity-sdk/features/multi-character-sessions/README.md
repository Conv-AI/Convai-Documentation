---
title: Multi-character sessions
description: Find guides for running several Convai characters in one Unity scene, choosing who the player talks to, and testing the shared room.
last_reviewed: "4.6.0"
---

A multi-character session is a Unity scene where two or more `ConvaiCharacter` components are active at once, sharing one room with Convai. The player addresses one character at a time, and the SDK works out which — no mode to switch on, no component to add, and no field to fill. Use these pages to add a second character to a working scene, understand how the room decides who is being addressed, and identify each character correctly once more than one shares the room.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>How multi-character sessions work</strong><br>Understand how the room forms around the active characters in a scene, and how it decides who the player is addressing.</td><td><a href="how-multi-character-sessions-work.md">how-multi-character-sessions-work.md</a></td></tr>
<tr><td><strong>Build your first multi-character session</strong><br>Add a second character to a working scene and confirm the room addresses whichever one the player looks at.</td><td><a href="quick-start.md">quick-start.md</a></td></tr>
<tr><td><strong>Character identity</strong><br>Give every character in a room its own Character ID, and understand what happens when two characters share one.</td><td><a href="character-identity.md">character-identity.md</a></td></tr>
<tr><td><strong>Multi-Character Sample</strong><br>Import the shipped sample scene and see several characters, interaction targeting, and a transcript UI working together.</td><td><a href="multi-character-sample.md">multi-character-sample.md</a></td></tr>
</tbody></table>

## Two questions a multi-character scene raises

Adding a second character to a scene raises two questions that a single-character scene never asks: who is the player talking to, and can the player talk right now. Each has its own feature area.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>Conversation targeting</strong><br>How the SDK decides which character the player is addressing, and how to script or tune that decision.</td><td><a href="../conversation-targeting/README.md">../conversation-targeting/README.md</a></td></tr>
<tr><td><strong>Conversation availability</strong><br>Whether the addressed character can hear the player yet, and how to gate your own UI on that state.</td><td><a href="../conversation-availability/README.md">../conversation-availability/README.md</a></td></tr>
</tbody></table>

## Next steps

Start with [Build your first multi-character session](quick-start.md) to add a second character to a scene and confirm the room reaches it, then read [Character identity](character-identity.md) before assigning Character IDs to more than one character.

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}
