---
title: Multi-character sessions
description: Find guides for running several Convai characters in one shared room in Unity, choosing who the player is addressing, and changing the cast at runtime.
last_reviewed: "4.6.0"
---

A multi-character session puts every registered `ConvaiCharacter` in your scene into one room with Convai. Each character holds its own membership, its own audio track, and its own readiness, while the player's speech is routed to whichever membership is the current interaction target. Use these pages when a scene needs more than one character talking to the same player.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>How multi-character sessions work</strong><br>Understand roster creation at connect, the initial character, and the epoch-guarded command model that keeps the client and Convai in agreement.</td><td><a href="how-multi-character-sessions-work.md">how-multi-character-sessions-work.md</a></td></tr>
<tr><td><strong>Character identity and addressing</strong><br>Learn why a membership ID, a character ID, and a participant identity are three different things, and which one to use for each job.</td><td><a href="character-identity.md">character-identity.md</a></td></tr>
<tr><td><strong>Build your first multi-character session</strong><br>Put two characters in a scene, connect them as one room, and confirm that the room reaches a ready state.</td><td><a href="quick-start.md">quick-start.md</a></td></tr>
<tr><td><strong>Roster readiness and partial dispatch</strong><br>Understand what readiness means per character, why a ready secondary character does not make the session ready, and how start failures surface.</td><td><a href="readiness-and-partial-dispatch.md">readiness-and-partial-dispatch.md</a></td></tr>
<tr><td><strong>Switch the interaction target</strong><br>Route player input to a chosen character, then release the target without interrupting whoever is already speaking.</td><td><a href="switch-the-interaction-target.md">switch-the-interaction-target.md</a></td></tr>
<tr><td><strong>Add and remove characters at runtime</strong><br>Change a connected room's cast with <code>AddCharacterAsync</code> and <code>RemoveCharacterAsync</code>, including replacement targets and the clone rule.</td><td><a href="update-the-roster.md">update-the-roster.md</a></td></tr>
<tr><td><strong>Join an existing multi-character session</strong><br>Bring a second human participant into a room another client already created, using one room locator.</td><td><a href="join-an-existing-session.md">join-an-existing-session.md</a></td></tr>
<tr><td><strong>Route audio for each character</strong><br>Bind one audio source per participant identity, then enable or silence each character or human independently.</td><td><a href="route-character-audio.md">route-character-audio.md</a></td></tr>
<tr><td><strong>React to roster and target changes</strong><br>Subscribe to roster and interaction-target events, and rely on the ordering the SDK guarantees between them.</td><td><a href="handle-roster-events.md">handle-roster-events.md</a></td></tr>
<tr><td><strong>Multi-character room session reference</strong><br>Look up every member of the room session type, its membership and status fields, and the results its commands return.</td><td><a href="room-session-reference.md">room-session-reference.md</a></td></tr>
<tr><td><strong>Multi-character connection API reference</strong><br>Look up the connection operations, their option types, and every exception each operation can throw.</td><td><a href="connection-api-reference.md">connection-api-reference.md</a></td></tr>
<tr><td><strong>Multi-character usage examples</strong><br>See two worked patterns: look-to-address targeting with turn retention, and a scripted roster swap mid-scenario.</td><td><a href="usage-examples.md">usage-examples.md</a></td></tr>
<tr><td><strong>Troubleshoot multi-character sessions</strong><br>Fix roster rejections, readiness failures, misrouted audio, duplicated clones, epoch mismatches, and command timeouts.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr>
</tbody></table>

## How a scene becomes a multi-character session

A scene becomes a multi-character session as soon as two or more `ConvaiCharacter` components are registered with the manager when it connects. There is no opt-in flag and no Inspector toggle. [How multi-character sessions work](how-multi-character-sessions-work.md) covers roster ordering, the connect-time validation rules, and the command model.

{% hint style="info" %}
A scene with several `ConvaiCharacter` components needs an explicit conversation target, because the SDK only infers one automatically when the scene owns exactly one character. See [Build your first multi-character session](quick-start.md).
{% endhint %}

## Next steps

Start with [Build your first multi-character session](quick-start.md) to get two characters into one room, then read [Character identity and addressing](character-identity.md) before you write any code that resolves a message back to a character.

The Live API pages document the same feature at the protocol level, including the exact message shapes the SDK sends and receives on your behalf.

{% content-ref url="../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md" %}
[Use multi-character sessions](../../../../api-reference/core-api-reference/live-apis-beta/multi-character-sessions.md)
{% endcontent-ref %}
