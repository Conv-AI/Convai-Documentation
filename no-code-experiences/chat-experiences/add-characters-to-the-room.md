---
title: Add characters to the room
description: Add characters to a chat experience room from the workspace you are in or by pasting a character ID, and see each one join and be briefed.
last_reviewed: "2026-09-10"
---

A chat experience opens as an empty room, and the characters you seat in it are the ones that answer you. You add characters for each session: opening the experience again starts a new room with nobody in it. Use this page to add characters from your workspace or by character ID, and to recognize the point at which each one has joined and been briefed.

## Prerequisites

- A chat experience you have created. See [Create a chat experience](create-a-chat-experience.md).
- At least one character you can reach, either in the workspace you are working in or through a character ID someone has shared with you. See [What you need to use Chat Experiences](prerequisites.md).

## Open the character picker

Select **Add characters**. In an empty room the button appears in two places: on the **Add the participants** card in the side panel, and under **Nobody is in the room yet** in the thread. Once the room has characters in it, the same button sits under the list in the side panel. A plus control in the panel header does the same thing.

**Add characters** is unavailable while the room is connecting and while the characters are answering a message. The side panel prints the reason under the button, and the button becomes available again once the turn finishes.

The **Add characters to the room** dialog opens on two tabs: **From my workspaces** and **By character ID**. Both tabs feed one selection, so switching between them keeps what you have already picked.

## Add characters from your workspaces

**From my workspaces** lists the characters in the workspace you are working in, most recently edited first.

{% stepper %}
{% step %}
### Find the characters you want

The grid opens with the eight most recently edited characters, under a line that counts the characters in the list and says how many of them are on show. When there are more, a button below the grid expands it to the full list, carrying that count in its label, as in **Show all 24**.

To narrow the grid, type in the search field. It matches on both the character name and the character description. A search with no results shows "No characters match."
{% endstep %}

{% step %}
### Select them

Select a character card to add it to the selection, and select it again to drop it. A check mark appears in the corner of each selected card.

The footer counts the selection and names the first four characters in it.
{% endstep %}

{% step %}
### Confirm

Select the confirm button. Its label counts the selection, so three characters picked make it read **Add 3 to room**, and it stays unavailable until you have selected at least one.

The dialog closes and the characters begin joining.
{% endstep %}
{% endstepper %}

## Add a character by ID

**By character ID** finds a character from its ID. Use it for a character someone has shared with you from outside your own workspaces.

{% stepper %}
{% step %}
### Paste the IDs

Under **Character ID**, paste one character ID per line. The field takes several at once, and a note under it states the condition an ID has to meet: any character whose owner has shared it with you can join, even from outside your workspaces.
{% endstep %}

{% step %}
### Look them up

Select the look-up button. Its label counts the IDs you have entered, so three pasted IDs make it read **Look up 3**.

Each ID becomes a row under **Results**. A character that resolved shows its name, its description, and an **Add** button. An ID that did not resolve becomes a row that shows a shortened form of the ID and says which of three things happened:

- The character exists but has not been shared with you.
- No character with that ID is available to you.
- The look-up itself did not finish.
{% endstep %}

{% step %}
### Add and confirm

Select **Add** on each row you want. The button becomes **Added**, and the footer count of characters added by ID goes up.

Select **Done** to close the dialog.
{% endstep %}
{% endstepper %}

## Watch the characters join and be briefed

Each character appears in the side panel straight away, with **Joining the room…** under its name, and settles into a normal row once it is in. While the room is connecting, the message box is locked and reads **Waiting for characters to join…**.

The thread marks the moment the briefing lands. A divider names the characters and states that they joined and were briefed. A box titled **What each character was told on joining** holds the briefing itself, with a line per character noting that it also carries its own persona. In a one-character room the box is titled with that character's name instead. What the briefing contains, and how the room type and the purpose produce it, is covered in [The room brief](the-room-brief/README.md).

In a room of two or more characters, a note under that box states that the respond mode is set to Auto and that the brief decides who answers.

The side panel changes with the size of the room. With one character it labels your own row **You** and describes it as talking with that character; with two or more it labels the row **Moderator** and describes it as "You ask, they answer".

## The characters belong to this session only

The characters you add are seated for this session only. Opening the experience again starts a new session, and the room it opens is empty.

The brief carries over from one session to the next. The characters and the messages do not, so add the characters you want each time you open the experience.

{% hint style="warning" %}
Reloading the page while a room is open ends that session and returns you to an empty room. Add the characters again before continuing.
{% endhint %}

## Next steps

With at least one character in the room, the message box unlocks and you can address the room.

{% content-ref url="send-your-first-message.md" %}
[Send your first message](send-your-first-message.md)
{% endcontent-ref %}
