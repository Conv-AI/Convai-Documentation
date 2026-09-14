---
title: Room controls reference
description: Reference for the controls in a chat experience room's top bar and side panel, and what each one does to the conversation.
last_reviewed: "2026-09-10"
---

A chat experience room carries controls in a top bar above the conversation and in the side panel down the left. This page lists both, in the order they appear on screen. The message box under the thread holds controls of its own—the respond chip and the paperclip—covered in [Choose who replies](choose-who-replies.md) and [Share files with the room](../share-files-with-the-room/README.md).

## The top bar

The top bar runs above the thread and names the experience the room was opened from. It carries these, from left to right:

| Part | What it does |
|---|---|
| Back arrow | Returns to **My Experiences** and ends the conversation |
| The experience name | Names the chat experience this room was opened from |
| Pencil | Opens **Rename experience**, where you change the name. The room type, the purpose, and the briefing are untouched |
| Room type chip | The room type the experience was created with, for example **Focus group** |
| Room ID chip | Copies the room ID. See [The room ID](#the-room-id) below |
| Character avatars | One avatar per character in the room, followed by the count: `1 character`, or `4 characters` in a room of four |
| **Text only** chip | The room's mode. Hovering it shows **Room mode**. The characters answer in writing |
| **Previous sessions** | Lists the sessions already recorded for this experience, newest first, and offers **Open experience page**. See [Review a past session](../sessions-and-transcripts/review-a-past-session.md) |
| Three-dots menu | Opens the room's actions, listed below |

The bar drops what it has no room for as the window narrows. The room ID and the character count go first, and a people icon appears beside the back arrow to open the side panel over the thread. Narrower still, the room type chip, the avatars, and the **Text only** chip go as well, and **Previous sessions** shows as an icon alone.

## The three-dots menu

The three-dots menu sits at the right of the top bar and holds these actions:

| Item | What it does |
|---|---|
| **Rename experience** | Opens the same rename dialog as the pencil |
| **Duplicate with a new brief** | Opens the create dialog prefilled from this experience, with every field editable. See [Why the brief cannot be changed](../the-room-brief/why-the-brief-cannot-be-changed.md) |
| **Export transcript** | Downloads the conversation in this room as a Markdown file. See [Export a transcript](../sessions-and-transcripts/export-a-transcript.md) |
| **Clear conversation** | Ends the conversation and empties the room: the thread, the characters, and the **Shared in room** list |

{% hint style="warning" %}
**Clear conversation** ends the conversation as soon as you select it. It does not ask you to confirm, and a conversation that has ended cannot be rejoined. The room stays open, emptied and waiting for characters, so the room you are looking at afterwards is a new one.
{% endhint %}

## The room ID

The room ID is the short identifier in the top bar, beginning with `rm_`. Selecting the chip copies it and confirms with **Room ID copied**.

The ID belongs to the chat experience, so every room opened from that experience shows the same one. It is also shown in the list view of **My Experiences**, where you can copy it from the row.

The ID names the room inside your own account. A chat experience and the rooms opened from it are reachable only by the account that created them, so the ID does not give anyone else a way into the room.

Belonging to the experience, the ID cannot tell one session from another. Each session has an identifier of its own, and an exported transcript is named from it. See [Export a transcript](../sessions-and-transcripts/export-a-transcript.md).

## The side panel

The side panel holds the roster, your own row, the brief, and the files shared so far. On a narrow screen it opens over the thread from the people icon beside the back arrow, and an X in its header closes it again. From top to bottom it carries these:

| Part | What it does |
|---|---|
| **In this room** | Names the section. The number of characters follows it once any are seated |
| The plus in the header | Opens the character picker. Present once the room has characters in it |
| A character's row | Names the character, its role, and where it came from: your workspace, or "Shared with you" for a character added by ID |
| The dots at the right of a character's row | Hold **Remove from room** |
| **Add characters** | Opens the character picker. Sits under the list of characters, and on the **Add the participants** card while the room is empty |
| **Moderator** or **You** | The section holding your own row. **Moderator** in a room of two or more characters, **You** in a one-character room |
| Your row | Your name with **(you)** after it, described as "You ask, they answer" or "Talking with ⟨name⟩", followed by your workspace when there is one to show |
| **Room brief** | The room type and the purpose set when the experience was created, the same in every session |
| **Fixed at creation** | The lock beside the brief. Hovering it explains why the brief cannot change and offers **Duplicate with a new brief** |
| **Shared in room** | The files attached during this conversation. Reads "Files you attach show up here for every character." until one is attached |

The panel shows the same room type and purpose whatever the size of the room. In a one-character room, though, the briefing that character was given is written in wording of its own rather than from the room type. See [How the room brief is written](../the-room-brief/how-the-room-brief-is-written.md).

The plus, **Add characters**, and **Remove from room** are all disabled while a turn is running or while the room is opening. The reason is written under **Add characters** and inside the row menu, and the plus carries it when you hover. See [Add or remove characters mid-conversation](add-or-remove-characters.md).

An empty room replaces the roster and your own row with a single **Add the participants** card, reading "Each character receives the room brief the moment they join."

## Related pages

{% content-ref url="add-or-remove-characters.md" %}
[Add or remove characters mid-conversation](add-or-remove-characters.md)
{% endcontent-ref %}

{% content-ref url="choose-who-replies.md" %}
[Choose who replies](choose-who-replies.md)
{% endcontent-ref %}
