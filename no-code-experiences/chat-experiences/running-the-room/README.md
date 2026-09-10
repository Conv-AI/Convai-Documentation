---
title: Running the room
description: Understand what a chat experience room is made of, what the side panel, thread, and message box each do, and where the room's controls live.
last_reviewed: "2026-09-10"
---

A [chat experience](../README.md) room has three working parts: a side panel down the left, the thread in the middle, and the message box at the bottom. Each answers a different question—who is in the room, what has been said, and what happens to the next message you send. These pages cover how a turn runs, how to choose who replies and in which mode, how to change the roster mid-conversation, and what every control in the room does. Chat Experiences is in beta.

## What the room is made of

The room fills the page. The side panel runs the full height down the left, and a thin top bar sits above the thread and the message box:

| Part | What it is for |
|---|---|
| The top bar | Names the experience and carries the room's controls: the room type, the room ID, the **Text only** chip, [**Previous sessions**](../sessions-and-transcripts/README.md), and the three-dots menu at the end of the bar, which opens the room's actions |
| The side panel | Who is in the room, who you are in it, the room brief, and the files shared so far |
| The thread | The conversation, and what the room reports about each turn |
| The message box | Where you write, and where you set who answers |

The room opens the moment you select a chat experience on **My Experiences**. It opens empty, with nobody in it and nothing said.

## The side panel

The side panel is the roster. Its header reads **In this room**, with the number of characters after it once any are seated.

An empty room replaces the roster and your own row with an **Add the participants** card. Every character in the room takes a row of its own, carrying its name, its role, and the workspace it came from.

Your own row sits under the roster once anyone is in it. In a room of two or more characters it is labeled **Moderator** and described as "You ask, they answer"; in a one-character room it is labeled **You** and described as "Talking with ⟨name⟩". Your workspace follows the description when there is one to show.

Two sections close the panel. **Room brief** holds the room type and the purpose for the whole conversation, beside a **Fixed at creation** label. [**Shared in room**](../share-files-with-the-room/README.md) lists the files attached during the conversation, and reads "Files you attach show up here for every character." until one is.

Every control in the top bar and the panel, and what each one does, is listed in [Room controls reference](room-controls-reference.md).

## The thread

The thread is the conversation, and it is also where the room reports what happened to each message.

It opens with the time the room was opened. While nobody is in the room, a pinned **Room brief** card holds the purpose and the room type's rules, above the heading **Nobody is in the room yet**. Characters joining produce a divider naming who joined and saying they were briefed, followed by a box holding the briefing itself—titled **What each character was told on joining** in a room of two or more, and **What ⟨name⟩ was told on joining** when a single character is in the room.

A one-character room is not briefed by its room type. The rules listed in that box always read **One other person**, **Stay in character**, and **Respond when addressed**, and the wording around your purpose is written for one character rather than taken from the type—unless you reworded the briefing yourself in the create dialog, in which case your wording stands.

After that the thread carries the conversation. Your own messages sit to the right, each with a caption under it reporting what the turn asked for and what came back. Replies sit to the left under the character's name and role. Between them the room adds short notes: who stayed quiet, who did not answer, and who left the room.

## The message box

The message box is where you write, and where you decide who answers.

The prompt in the box invites you to write to the room, or to type @ to call on someone. Below the text is a row that starts with the paperclip for attaching files and then the respond chip, which shows what the next message will ask for—the respond mode, or the names when you have tagged someone—and opens the respond menu. A one-character room shows a sentence in place of the chip, because there is nobody to route between.

The box locks whenever the room cannot take a message—before any character is in the room, while the characters are joining, while a turn is running, and after the room fails to connect—and it always says why. See [You cannot send a message](../troubleshooting/composer-is-locked.md).

## Which page answers which question

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How a turn works</strong><br>Why the room answers one message at a time, what the turn caption counts, and why a character may say nothing.</td><td><a href="how-a-turn-works.md">how-a-turn-works.md</a></td></tr><tr><td><strong>Choose who replies</strong><br>Set who answers the next message, and tag individual characters when you want only them.</td><td><a href="choose-who-replies.md">choose-who-replies.md</a></td></tr><tr><td><strong>Respond modes reference</strong><br>All five respond modes, what each asks of the characters, and what the thread shows afterwards.</td><td><a href="respond-modes-reference.md">respond-modes-reference.md</a></td></tr><tr><td><strong>Add or remove characters mid-conversation</strong><br>Seat a character in a running room, remove one, and work with the controls that freeze during a turn.</td><td><a href="add-or-remove-characters.md">add-or-remove-characters.md</a></td></tr><tr><td><strong>Room controls reference</strong><br>Every control in the top bar and the side panel, and what each one does.</td><td><a href="room-controls-reference.md">room-controls-reference.md</a></td></tr></tbody></table>

The brief the room runs on is written before any of this, in the create dialog.

{% content-ref url="../the-room-brief/README.md" %}
[The room brief](../the-room-brief/README.md)
{% endcontent-ref %}
