---
title: Share files with the room
description: Understand what reaches the characters when you attach a file to a message in a chat experience room, and what the room keeps afterwards.
last_reviewed: "2026-11-12"
---

A message you send in a [chat experience](../README.md) room can carry files. A PDF, a PowerPoint deck, a picture, or a video reaches the characters as the file itself, and a Word or plain-text file reaches them as its text. These pages cover what each kind of file becomes, what the room shows you about it, and what is kept once the conversation is over.

## What the characters receive

A file goes to the characters that turn is addressed to. A character the message did not address is not given the file, and the replies that follow do not pass it on. A room opens on **Everyone must respond**, so a file reaches every character unless you narrow the turn with a tag or the respond chip. See [Choose who replies](../running-the-room/choose-who-replies.md).

A PDF, a PowerPoint deck, a picture, and a video are handed to the characters as they are: the characters read the PDF's pages and the deck's slides, look at the picture, and are given frames from the video along with a transcript of what is said in it. A Word file and every plain-text format are shared as the text they contain.

A file you share belongs to the conversation you shared it in. Every new conversation starts with nothing shared.

## What each kind of file becomes

| What you attach | What reaches the characters |
|---|---|
| A PDF | The document itself, page by page |
| A PowerPoint deck—`.pptx` | The whole deck, slide by slide, with frames and a speech transcript for audio and video embedded in it |
| A picture—`.png`, `.jpg`, `.jpeg`, or `.webp` | The picture |
| A video—`.mp4`, `.webm`, `.mkv`, `.m4v`, or `.mov` | Frames taken from the video, and a transcript of its speech when it has any |
| A Word file—`.docx` | The text of the document |
| A plain-text file—`.txt`, `.md`, `.csv`, or `.json` | The file's own text |

Each kind has its own size limit, and a message carries one video at most. See [File limits reference](file-limits-reference.md).

## When a file cannot be prepared

Every file you attach gets a chip above where you type, and the chip's second line settles once the file is ready. The send control waits until every chip has settled.

A PDF, a deck, a picture, or a video that cannot be prepared says why on its chip and holds the message back until you retry the file or remove it. A Word or plain-text file that cannot be read is still sent, by name alone: its chip reads `could not read`, and a message names the file.

The paperclip that attaches a file is greyed out only while the message box is locked. No file makes it unavailable. See [You cannot send a message](../troubleshooting/composer-is-locked.md) for every reason the box locks.

## Drag files onto the conversation

Dragging files from your computer onto the conversation attaches them exactly as the paperclip does: the same formats, the same size limit, and the same chips. Drop them on the top bar, the thread, or the message box. While you drag, the conversation reads "Drop files to attach them" and "They are added to your next message."

While the message box is locked, the conversation reads "Files can't be attached right now" with the reason the box is locked, and a drop attaches nothing. A file dropped outside the conversation, such as on the side panel, is ignored.

## What the room keeps

The room keeps file names, not file contents. Three places show a file after you send it:

- **The thread.** The message you sent carries a chip for every file that went with it.
- **The side panel.** Its **Shared in room** section lists the files sent so far in this conversation, each with its name and the same second line as the chip. [File limits reference](file-limits-reference.md) sets out what each note means, and [Running the room](../running-the-room/README.md) covers the panel's other sections.
- **A finished session's transcript.** It records the name of every file a turn carried, and a transcript you download lists those names under the turn they were sent with. See [Review a past session](../sessions-and-transcripts/review-a-past-session.md) and [Export a transcript](../sessions-and-transcripts/export-a-transcript.md).

The **Shared in room** list holds the files on the messages you have sent in the current conversation, so it empties when the conversation ends: **Clear conversation** and **Leave room** in the room's three-dots menu both empty it. A message that failed to send adds nothing to it. See [Room controls reference](../running-the-room/room-controls-reference.md).

Because only names are kept, every file in a past session's thread is shown as a name, whatever happened to it at the time. A transcript records that a file was shared, not what the characters were given from it.

## Which page answers which question

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Share a document</strong><br>Attach a PDF, a PowerPoint deck, a Word file, or a plain-text file, and read what the chip reports about it.</td><td><a href="share-a-document.md">share-a-document.md</a></td></tr><tr><td><strong>Share an image or a video</strong><br>Attach a picture or a video, and understand what the characters are given from it.</td><td><a href="share-an-image.md">share-an-image.md</a></td></tr><tr><td><strong>File limits reference</strong><br>The accepted file types, the size and length limits, and what happens at each one.</td><td><a href="file-limits-reference.md">file-limits-reference.md</a></td></tr></tbody></table>

The message box, where a file is attached, is one of the room's three working parts.

{% content-ref url="../running-the-room/README.md" %}
[Running the room](../running-the-room/README.md)
{% endcontent-ref %}
