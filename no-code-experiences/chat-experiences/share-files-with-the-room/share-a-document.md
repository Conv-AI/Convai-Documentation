---
title: Share a document
description: Attach a PDF, a Word file, or a plain-text file to a message in a chat experience room, and read what the chip reports about it.
last_reviewed: "2026-11-12"
---

A document you attach reaches the characters your message addresses: a PDF as the document itself, a Word or plain-text file as its text. Use this page to attach one, to send it with a message, and to read what the room reports about the file once it is ready.

## Prerequisites

- A chat experience room with at least one character already in it. See [Add characters to the room](../add-characters-to-the-room.md).
- A file in one of the accepted formats. See [File limits reference](file-limits-reference.md).

## Attach a document and send it

{% stepper %}
{% step %}
### Pick the file

Select the paperclip at the left of the message box, below where you type, and pick the file. You can pick several files at once. Or drag the files from your computer onto the conversation and drop them. See [Drag files onto the conversation](README.md#drag-files-onto-the-conversation).

A chip appears above where you type, carrying the file's format, its name, and a second line reading `reading…` after the size.
{% endstep %}

{% step %}
### Wait for the chip to settle

The second line changes once the file is ready. A PDF is uploaded and checked first, so its chip passes through `uploading` and `validating PDF…` before it settles.

The arrow button at the right of the message box stays unavailable while any chip is still waiting, and comes back when every chip is ready. The message box also locks for reasons of its own, and always says which. See [You cannot send a message](../troubleshooting/composer-is-locked.md).
{% endstep %}

{% step %}
### Write the message and send

Write your question and send the message as usual. The message carries the file with it, and the chip moves into the thread above your words.

A message can carry files and no words at all. On the default, **Everyone must respond**, a message carrying nothing but a file is still addressed to every character. Add a question if you want them to answer about something in particular.

Who the turn addresses also settles who has the document: it goes to the characters that turn is addressed to, and a character the message did not address is not given it. In a room of two or more, the default **Everyone must respond** already sends it to every character, and a tag or a narrower respond chip limits who gets it. In a room of one there is no chip to set, and every message already goes to that character. See [Choose who replies](../running-the-room/choose-who-replies.md).

Once the message is away, the chip sits with it in the thread and the file joins the **Shared in room** section of the side panel.
{% endstep %}
{% endstepper %}

To take a file off a message before you send it, select the × on its chip.

## What the chip reports for each format

The chip's second line always opens with the file's size. What follows depends on the format:

| What you attached | What the second line reads |
|---|---|
| A text file—`.txt` or `.md` | The size alone, for example `4 KB` |
| A CSV file | The size and the number of rows, for example `12 KB · 240 rows` |
| A JSON file | The size and the file's shape—`8 keys` for a set of fields, `12 items` for a list |
| A Word file | The size and `document`, for example `1.2 MB · document` |
| A PDF | The size, the page count, and `PDF ready`, for example `1.2 MB · 14 pages · PDF ready` |

`truncated` is added to the end of that line when a Word or plain-text file held more text than the room shares from a single file. The text is cut at the limit and the rest is not sent. See [File limits reference](file-limits-reference.md).

## What happens to a Word file

A `.docx` file reaches the characters as the document's text, and the chip reports `document` after the size rather than a page count. If its text cannot be read, the file goes with its name alone.

## What happens to a PDF

A PDF is handed to the characters as the document itself, so they read its pages as laid out, including pages that are scans or slides. The chip reports the page count and `PDF ready`.

A PDF can be up to 10 MB and 33 pages. A larger file is refused when you pick it, and one with more pages settles to a chip naming the problem, which you remove before sending.

## Plain-text formats

`.txt`, `.md`, `.csv`, and `.json` files each reach the characters as their own text, unchanged up to the limit above.

A CSV file and a JSON file each add a count to the chip, so you can check that the file was read as the shape you expected before you send it. The CSV row count includes the header row. A JSON file that does not parse as a set of fields or a list shows the size alone, and its text is still shared as it stands.

## When a document cannot be read or prepared

A Word or plain-text file the room could not read is still sent, by name alone. The chip's second line settles to `could not read` after the size, a message reads "Could not read ⟨name⟩; only its name will be shared", and the side panel notes the file as `name only`.

A PDF that could not be prepared is not sent. Its chip gives the reason, ending "Retry or remove.", and the message is held back until you retry the file or take it off.

## Next steps

A picture or a video is attached the same way and has limits of its own.

{% content-ref url="share-an-image.md" %}
[Share an image or a video](share-an-image.md)
{% endcontent-ref %}

For the accepted formats, the size and text limits, and what happens at each one:

{% content-ref url="file-limits-reference.md" %}
[File limits reference](file-limits-reference.md)
{% endcontent-ref %}
