---
title: Conversation availability
description: Find guides for checking whether a Convai character can hear the player right now, and reacting in your UI when it cannot.
last_reviewed: "4.6.0"
---

Conversation availability is how the Convai Unity SDK answers whether the player can talk to a character right now, and what is in the way when they cannot. A connected room does not mean the addressed character can hear anything — the service has to announce the character first, and `ConvaiManager.ConversationAvailability` is the single place that answer lives. Everything in the SDK that takes player input already asks it.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>How conversation availability works</strong><br>Understand the states, why a connected room is not enough, and how availability differs from a character's readiness flag.</td><td><a href="how-availability-works.md">how-availability-works.md</a></td></tr>
<tr><td><strong>Gate your UI on availability</strong><br>Bind a custom chat field, send button, or microphone control to the current verdict.</td><td><a href="gate-your-ui.md">gate-your-ui.md</a></td></tr>
<tr><td><strong>Customise the chat field prompts</strong><br>Reword every state prompt the shipped chat field shows, and tune its slow-connect hint.</td><td><a href="customise-chat-prompts.md">customise-chat-prompts.md</a></td></tr>
<tr><td><strong>React to the player starting to speak</strong><br>Subscribe to local microphone and push-to-talk activity ahead of Convai's own confirmed verdict.</td><td><a href="local-player-activity.md">local-player-activity.md</a></td></tr>
<tr><td><strong>Conversation availability reference</strong><br>Look up every state, event, and method involved in gating player input.</td><td><a href="availability-reference.md">availability-reference.md</a></td></tr>
<tr><td><strong>Troubleshoot player input</strong><br>Fix a refused message, a chat field that stays disabled, or a microphone that will not open.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr>
</tbody></table>

## Where availability comes from

Availability is not a room-wide flag. It answers for `ConvaiManager.AddressedCharacter` — whoever the player is currently talking to — so the same room can report one character `Ready` while another is still `Preparing`. The same answer is also available per character on `ConvaiCharacter.ConversationAvailability`, for UI tied to one specific character rather than to whoever is currently addressed. See [How conversation availability works](how-availability-works.md) for the model behind the states.

## Next steps

Start with [How conversation availability works](how-availability-works.md) to understand the states, then [Gate your UI on availability](gate-your-ui.md) to wire your own input surface to it.

{% content-ref url="../multi-character-sessions/README.md" %}
[Multi-character sessions](../multi-character-sessions/README.md)
{% endcontent-ref %}
