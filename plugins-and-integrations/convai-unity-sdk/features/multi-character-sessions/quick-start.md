---
title: Build your first multi-character session
description: Add a second Convai character to a working Unity scene and confirm the room lets you talk to either one by looking at them.
last_reviewed: "4.6.0"
---

Add a second `ConvaiCharacter` to a scene that already has one working character, and confirm the room lets you talk to either one depending on where you look. There is no multi-character mode to switch on, no component to add, and no field to fill: a room holds every active Convai character in the loaded scenes automatically.

## Prerequisites

* [ ] A Unity scene with a working single-character setup: `ConvaiManager`, `ConvaiRoomManager`, `ConvaiPlayer`, and one `ConvaiCharacter` that already talks back in Play mode.
* [ ] A second Character ID from your [Convai dashboard](https://convai.com).

## Set up and test the second character

{% stepper %}
{% step %}
### Add a second character

Drop a second working character into the scene — use a second character prefab if your project ships one, or duplicate your existing character's `GameObject`. Duplicating carries over every component the original has, including `ConvaiCharacter`, and it carries over the original's Character ID too — a duplicate never gets one of its own.

Select the new character's `ConvaiCharacter` component. Its Inspector reports **Another character has this Character ID** immediately, above every other section, because two characters cannot share one and the room refuses to connect while they do. Paste the second character's own Character ID from the [Convai dashboard](https://convai.com) into the **Character ID** field, and the message clears.
{% endstep %}

{% step %}
### Confirm the scene setup

Select the `GameObject` holding `ConvaiManager` and open its Inspector. The **Scene Setup** section now reports **Characters in Scene** as `2` and **Joining the Room** as `All 2` — both characters count toward the next room connection.

Scroll down to **Characters Joining the Room**. It lists one row per character with a ticked checkbox, since every character joins by default — nothing needs enabling by hand. If either checkbox is cleared, click **Include Everyone** to send both.
{% endstep %}

{% step %}
### Leave Who The Player Talks To on Look At

With two characters selected for the room, the `ConvaiManager` Inspector adds a **Who The Player Talks To** section. Leave **Chosen By** on its default, **Look At** — it measures the angle from the player's camera to each character's head, so it needs no colliders, no layer masks, and no input wiring. That is why nothing else here needs setting.
{% endstep %}

{% step %}
### Enter Play mode and address each character

Enter Play mode. Look toward the first character and start talking or typing — it answers.

Turn to face the second character and speak again. The conversation moves to it: the first character's turn ends, and the second one responds.
{% endstep %}
{% endstepper %}

## Verify the setup

{% hint style="success" %}
**Success:** both characters answer depending on which one you are looking at, not on which one connected first or spoke last.
{% endhint %}

Select `ConvaiManager` again while still in Play mode. Its **Live** section is the fastest way to confirm two characters are actually sharing the room:

* **Characters in Room** reads the number the room actually opened for.
* **Talking To** names the character you are addressing right now, and updates as you turn your head.
* **Player Can Talk** reads **Yes** once that character can hear you — it reads **Not yet — this character is still joining** for the brief moment right after it joins the room.
* **Room Holds** reads **Several characters** once the room has grown past one.
* **Room Roster**, below that, lists one row per character. The one you are addressing is marked `· addressed`, and a character that can currently hold the conversation reads `Ready`.

If **Talking To** never changes when you look at the other character, check **Range** and **Look Angle** in **Who The Player Talks To** first, then confirm the second character's row in **Room Roster** actually reads `Ready`.

## Next steps

{% content-ref url="how-multi-character-sessions-work.md" %}
[How multi-character sessions work](how-multi-character-sessions-work.md)
{% endcontent-ref %}

{% content-ref url="character-identity.md" %}
[Character identity](character-identity.md)
{% endcontent-ref %}

{% content-ref url="../conversation-targeting/choose-a-targeting-mode.md" %}
[Choose a targeting mode](../conversation-targeting/choose-a-targeting-mode.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot multi-character sessions](troubleshooting.md)
{% endcontent-ref %}
