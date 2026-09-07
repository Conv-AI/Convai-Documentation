---
title: Build your first multi-character session
description: Add a second Convai character to a working Unity scene and confirm the room addresses whichever character the player looks at.
last_reviewed: "4.6.0"
---

Add a second character to a scene that already has one working Convai character, and confirm the room lets you talk to either one by looking at them. You finish with two characters sharing one room, with no script and no settings changed beyond their Character IDs.

## What you will build

A scene with two active `ConvaiCharacter` components, connected as one shared room. You look at the first character and ask it a question, then look at the second and ask it a question, and confirm the conversation follows your gaze.

## Prerequisites

- A Unity scene with a working single-character setup: `ConvaiManager`, `ConvaiRoomManager`, `ConvaiPlayer`, and one `ConvaiCharacter` that already talks back in Play mode.
- A second Character ID from your Convai dashboard at <code class="expression">space.vars.dashboard_url</code>.

## Add a second character

Drop a second working character into the scene. If your project ships a second character prefab, use it. Otherwise duplicate your existing character `GameObject` — Unity assigns the copy the same `ConvaiCharacter` component, `ConvaiAudioOutput`, and `AudioSource` your first character already uses, including its Character ID.

A duplicated character keeps the original's Character ID, which the Character inspector flags immediately — two characters cannot share one, and the room refuses to connect rather than half-working. Select the new character's `ConvaiCharacter` component and paste its own Character ID into the **Character ID** field.

## Confirm the scene setup

Select the `GameObject` holding **Convai Manager** and open its inspector. The **Scene Setup** section lists every `ConvaiCharacter` Convai Manager has found in the scene, each with a checkbox — confirm both characters appear here. Nothing needs enabling by hand; a character with its checkbox already ticked is included in the room. Use **Include Everyone** if either checkbox is cleared.

## Choose how the player addresses each character

Scroll to **Who The Player Talks To**. Leave **Chosen By** on its default, **Look At** — the room addresses whichever character is nearest the centre of the player's view.

## Enter Play mode

Enter Play mode. Look toward the first character and start talking or typing. The character answers, and the Console reports which character the room opened on.

## Talk to the second character

Turn to face the second character and speak again. The conversation moves to it — the first character's turn ends, and the second responds.

{% hint style="success" %}
Both characters answer depending on which one you are looking at. That confirms the room is addressing characters by gaze rather than by whichever one connected first.
{% endhint %}

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
