---
title: Add or remove characters mid-conversation
description: Seat a character in a chat experience room that is already running, remove one, and work with the controls that freeze during a turn.
last_reviewed: "2026-09-10"
---

The characters in a room can change while the conversation is running. A character seated halfway through receives the same [room brief](../the-room-brief/README.md) as the characters already seated, and a character removed stops answering from that point on. Use this page to change the roster of a live room and to recognize the moments when those controls are frozen.

## Prerequisites

- A chat experience room with the conversation already under way. See [Send your first message](../send-your-first-message.md).
- No turn running. The roster controls freeze while the characters are answering, and they say so.

## Add a character to a running room

Seating a character in a running room uses the picker that filled the room in the first place, reached from either of two controls in the side panel: the plus control in the **In this room** header, or **Add characters** under the list of characters. Both open the **Add characters to the room** dialog on its two tabs, **From my workspaces** and **By character ID**. See [Add characters to the room](../add-characters-to-the-room.md) for how to work the picker.

Each character you add takes a row in the side panel straight away, with **Joining the room…** under its name, and settles into a normal row once it is in. The thread marks the moment the briefing lands: a divider names each character that joined and says it was briefed. Each one receives the room brief on top of its own persona, exactly as the characters already seated did.

A character seated mid-conversation is counted from your next message onwards. The [turn captions](how-a-turn-works.md) on your earlier messages describe the room as it stood when you sent them, so they do not change.

## What changes when a one-character room becomes a group

A room holding one character reports itself differently from a room of two or more, and seating a second character switches it over.

- The message box replaces the line "One character in the room: every message goes to ⟨name⟩." with the respond chip, which sets who is expected to answer. See [Choose who replies](choose-who-replies.md).
- The section of the side panel holding your own row changes from **You** to **Moderator**, and the line under your name changes from "Talking with ⟨name⟩" to "You ask, they answer".
- Turn captions take their counted form from your next message onwards. The messages you sent while one character was seated keep the caption that names it, `Sent to ⟨name⟩`.

A room opened with one character runs on the single-character briefing, which has its own wording and its own rules rather than the ones a room type sets. Both forms are set out in [How the room brief is written](../the-room-brief/how-the-room-brief-is-written.md).

## Remove a character from the room

Removing takes a character out of the conversation without touching what it already said.

Open the menu on that character's row in the side panel—the dots at the right of the row—and select **Remove from room**. The row disappears at once, and the thread records a note reading "⟨name⟩ left the room" as soon as the room confirms it.

Messages the character already sent stay in the thread under its name, and the turn captions on your earlier messages still describe the room it was part of. Removing a character does not remove it from your workspace; it leaves this conversation only.

## Controls that freeze while a turn is running

The plus control, **Add characters** and **Remove from room** all freeze while the room is answering a message, and while the room is still opening. The reason is shown rather than left to guess.

| What the reason reads | When |
|---|---|
| **Wait for the current turn to finish** | A turn is running. The controls come back when the turn is over |
| **Connecting the room…** | The room is still opening, and there is nothing to change the roster of yet |

The reason sits with each frozen control. Hovering the plus control shows it, a line under **Add characters** carries it, and a character's row menu prints it under the frozen **Remove from room** item. In a room with nobody in it, hovering the **Add characters** button—on the **Add the participants** card in the side panel, or under **Nobody is in the room yet** in the thread—shows the same reason.

A room that stays on **Connecting the room…** has not opened yet. See [The room will not connect](../troubleshooting/room-will-not-connect.md).

## The roster belongs to this session

A character you seat now is seated for this session only, and seating it does not add it to the chat experience. Opening the experience again starts a new room with nobody in it, whatever you seated last time. Seating that new room is covered in [Add characters to the room](../add-characters-to-the-room.md).

{% hint style="warning" %}
Reloading the page while a room is open ends that session, roster and all. A session that has ended cannot be rejoined, so seat the characters again and start a new one.
{% endhint %}

## Related pages

{% content-ref url="room-controls-reference.md" %}
[Room controls reference](room-controls-reference.md)
{% endcontent-ref %}

{% content-ref url="how-a-turn-works.md" %}
[How a turn works](how-a-turn-works.md)
{% endcontent-ref %}
