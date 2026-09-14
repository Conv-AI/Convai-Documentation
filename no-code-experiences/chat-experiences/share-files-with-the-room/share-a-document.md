---
title: Share a document
description: Attach a PDF, a Word file, or a plain-text file to a message in a chat experience room, and read what the chip reports about it.
last_reviewed: "2026-09-10"
---

A document you attach reaches the characters your message addresses, as text. Use this page to attach a PDF, a Word file, or a plain-text file, to send it with a message, and to read what the room reports about the file once it has been read or described.

## Prerequisites

- A chat experience room with at least one character already in it. See [Add characters to the room](../add-characters-to-the-room.md).
- A file in one of the accepted formats. See [File limits reference](file-limits-reference.md).

## Attach a document and send it

{% stepper %}
{% step %}
### Pick the file

Select the paperclip at the left of the message box, below where you type, and pick the file. You can pick several files at once.

A chip appears above where you type, carrying the file's format, its name, and a second line reading `reading…` after the size.
{% endstep %}

{% step %}
### Wait for the chip to settle

The second line changes once the file has been read or described, and what it reads then tells you what the characters will be given.

The arrow button at the right of the message box stays unavailable while any chip still reads `reading…` or `describing…`, and comes back when every chip has settled. The message box also locks for reasons of its own, and always says which. See [You cannot send a message](../troubleshooting/composer-is-locked.md).
{% endstep %}

{% step %}
### Write the message and send

Write your question and send the message as usual. The message carries the file with it, and the chip moves into the thread above your words.

A message can carry files and no words at all. Add a question if you want the characters to answer about the file: under the default **Auto · room brief decides**, a message carrying nothing but a file usually draws no reply, while a respond chip that names who answers draws a reply whether or not you wrote anything.

Who the turn addresses also settles who has the document: it goes to the characters that turn is addressed to, and a character the message did not address is not given it. In a room of two or more, tag `@everyone` or set the respond chip beside the paperclip to **Everyone must respond** before you send. In a room of one there is no chip to set, and every message already goes to that character. See [Choose who replies](../running-the-room/choose-who-replies.md).

Once the message is away, the chip sits with it in the thread and the file joins the **Shared in room** section of the side panel, carrying the note `described` when the characters were given a description, `name only` when the name was all they got, and no note at all when the file's own text was shared.
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
| A PDF whose text was read | The size and the page count, for example `1.2 MB · 14 pages` |
| A PDF whose pages were described | The size, the page count, and how many pages were described, for example `574 B · 1 page · 1 page described` |

`truncated` is added to the end of that line when that one file held more text than the room shares from a single file. The text is cut at the limit and the rest is not sent. See [File limits reference](file-limits-reference.md).

## What happens to a Word file

A `.docx` file reaches the characters as the document's text, and the chip reports `document` after the size rather than a page count. A Word file is never described the way a PDF carrying little text is: if its text cannot be read, the file goes with its name alone.

## What happens to a PDF

A PDF is read in one of two ways, and both are the room working correctly. The chip is what tells you which one you got.

A PDF carrying a body of prose is shared as that prose. The characters receive the document's own words, and the chip reports the page count.

A PDF carrying little text of its own is described instead. Its first pages are described in words, up to four of them, and the chip reports how many were described. The characters receive those descriptions, and, where the file runs past the pages that were described, a line naming the pages that were not.

A one-page PDF holding a single line is described rather than read, and its chip reads `1 page · 1 page described` after the size. To see a PDF's own text reach the characters, attach one with a real body of prose in it.

## Plain-text formats

`.txt`, `.md`, `.csv`, and `.json` files each reach the characters as their own text, unchanged up to the limit above.

A CSV file and a JSON file each add a count to the chip, so you can check that the file was read as the shape you expected before you send it. The CSV row count includes the header row. A JSON file that does not parse as a set of fields or a list shows the size alone, and its text is still shared as it stands.

## When a document cannot be read

A document the room could not read is still sent, by name alone. The characters are given the file name and nothing else.

The room tells you as soon as the file settles, in two places. The chip's second line settles to `could not read` after the size, and a message reads "Could not read ⟨name⟩; only its name will be shared". A PDF that could be neither read nor described settles to `could not describe` instead, and its message reads "Could not describe ⟨name⟩; only its name will be shared". Either outcome sends the name on its own, and the side panel notes the file as `name only`.

## Next steps

A picture follows different rules, and what the characters are told about one is worth reading before you attach it.

{% content-ref url="share-an-image.md" %}
[Share an image](share-an-image.md)
{% endcontent-ref %}

For the accepted formats, the size and text limits, and what happens at each one:

{% content-ref url="file-limits-reference.md" %}
[File limits reference](file-limits-reference.md)
{% endcontent-ref %}
