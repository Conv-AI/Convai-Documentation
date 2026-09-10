---
title: Share files with the room
description: Understand what reaches the characters when you attach a file to a message in a chat experience room, and what the room keeps afterwards.
last_reviewed: "2026-09-10"
---

A message you send in a [chat experience](../README.md) room can carry files. A file is never handed to the characters as a file: what reaches them is text—either the words the file already holds, or a description written for it. These pages cover what each kind of file becomes, what the room shows you about it, and what is kept once the conversation is over. Chat Experiences is in beta.

## What the characters receive

A file goes to the characters that turn is addressed to. A character the message did not address is not given the file, and the replies that follow do not pass it on. If you want every character to have a file, address the message to everyone—tag `@everyone`, or set the respond chip to **Everyone must respond**—before you send it. See [Choose who replies](../running-the-room/choose-who-replies.md).

Those characters receive text, and only text. A room carries writing, so every file you attach becomes writing before it travels.

There are two ways that happens. A file that holds words is shared as its own words: a PDF, a Word file, and every plain-text format reach the characters as the text they contain. A file that holds a picture cannot be shared that way, so a description of the picture is written and the characters receive the description instead. The characters are told that the words describe a picture you attached, and that description is all they have to answer from.

A file you share belongs to the conversation you shared it in. Every new conversation starts with nothing shared.

## What each kind of file becomes

| What you attach | What reaches the characters |
|---|---|
| A plain-text file—`.txt`, `.md`, `.csv`, or `.json` | The file's own text |
| A Word file—`.docx` | The text of the document |
| A PDF carrying a body of prose | The text of the document |
| A PDF carrying little text of its own | Whatever text it does hold, then a description of its first pages, written in words |
| A picture—`.png`, `.jpg`, or `.jpeg` | A description of the picture, written in words |

A PDF is the one format with two outcomes, and both are correct. [Share a document](share-a-document.md) sets out which one you get and how the room tells you.

## When a file cannot be read

A file the room could not read is still sent. Its name goes to the characters and nothing else, and the message is not held back.

Nothing tells you in advance whether a file's contents can be shared. You find out afterwards. Every file you attach gets a chip above where you type, and the chip's second line settles once the file has been dealt with. A file whose contents were not shared says so on that line, and a file the room could not read—or a picture it could not describe—also raises a message naming the file. A picture shared by its name alone raises no message, so the chip is the one place that reports every case.

The paperclip that attaches a file is greyed out only while the message box is locked. No file makes it unavailable. See [You cannot send a message](../troubleshooting/composer-is-locked.md) for every reason the box locks.

## What the room keeps

The room keeps file names, not file contents. Three places show a file after you send it:

- **The thread.** The message you sent carries a chip for every file that went with it.
- **The side panel.** Its **Shared in room** section lists the files sent so far in this conversation, each with its name, the same second line as the chip, and a note saying what the characters were given. [File limits reference](file-limits-reference.md) sets out what each note means, and [Running the room](../running-the-room/README.md) covers the panel's other sections.
- **A finished session's transcript.** It records the name of every file a turn carried, and a transcript you download lists those names under the turn they were sent with. See [Review a past session](../sessions-and-transcripts/review-a-past-session.md) and [Export a transcript](../sessions-and-transcripts/export-a-transcript.md).

**Clear conversation** in the room's three-dots menu empties the **Shared in room** list along with the thread. **Leave room** empties the room in the same way, but the **Shared in room** list survives it. See [Room controls reference](../running-the-room/room-controls-reference.md).

Because only names are kept, every file in a past session's thread is shown as a name, whatever happened to it at the time. A transcript records that a file was shared, not what the characters were given from it.

## Which page answers which question

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Share a document</strong><br>Attach a PDF, a Word file, or a plain-text file, and read what the chip reports about it.</td><td><a href="share-a-document.md">share-a-document.md</a></td></tr><tr><td><strong>Share an image</strong><br>Attach a picture, and understand what the characters are told about it.</td><td><a href="share-an-image.md">share-an-image.md</a></td></tr><tr><td><strong>File limits reference</strong><br>The accepted file types, the size and text limits, and what happens at each one.</td><td><a href="file-limits-reference.md">file-limits-reference.md</a></td></tr></tbody></table>

The message box, where a file is attached, is one of the room's three working parts.

{% content-ref url="../running-the-room/README.md" %}
[Running the room](../running-the-room/README.md)
{% endcontent-ref %}
