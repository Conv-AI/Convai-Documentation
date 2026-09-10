---
title: File limits reference
description: Reference for the file types a chat experience room accepts, the size and text limits on an attachment, and what each chip and side-panel note means.
last_reviewed: "2026-09-10"
---

A chat experience room accepts a short list of file formats and limits how much of a file it shares with the characters. This page lists the formats, the limits, and what the room does when a file passes one. Chat Experiences is in beta.

## Accepted file types

| Kind | Extensions | What reaches the characters |
|---|---|---|
| Documents | `.pdf`, `.docx` | The document's text; for a PDF whose pages carry almost no text, a description of those pages instead |
| Plain text | `.txt`, `.md`, `.csv`, `.json` | The file's own text |
| Pictures | `.png`, `.jpg`, `.jpeg` | A description of the picture, written in words |

Whatever the kind, a file goes to the characters that turn is addressed to, and a character the message did not address is not given it. See [Share files with the room](README.md) for how to address everyone.

The room states the list itself, on a line under the message box: "Accepted: PDF, DOCX, TXT, MD, CSV, JSON, PNG, JPG · up to 25 MB each".

That line appears only after you have attached at least one file, so it is not on screen to read before you choose one. A file with a `.jpeg` extension is accepted alongside `.jpg`, although the line names JPG alone.

Anything not in the table is refused when you pick it, and nothing about it is sent.

## Size and text limits

| Limit | Value |
|---|---|
| Size of one file | 25 MB |
| Text shared from one file | 30,000 characters |
| Text shared across one message | 60,000 characters |
| Pages described from a PDF carrying little text | 4 |

The two character limits count what is shared, not what the file holds. A description written for a picture counts against them the same way a document's own text does.

## What happens at each limit

| What you did | What the room does |
|---|---|
| Picked a file whose format is not accepted | The file is not attached. A message reads "⟨name⟩ is not a supported file type." |
| Picked a file over 25 MB | The file is not attached. A message reads "⟨name⟩ is larger than 25 MB." |
| Attached a file holding more than 30,000 characters | The file is attached and sent. The text is cut at the limit, the rest is not shared, and `truncated` is added to the chip |
| Attached files that together pass 60,000 characters | The file that passed the limit is taken off the message. A message reads "⟨name⟩ would put this message over the 60,000-character limit for shared text. Send it on its own or remove another file." |
| Attached a PDF of more than four pages that carries little text | The first four pages are described. The characters are told which pages were not described |
| Attached a file the room could not read | The file is sent by name alone. The chip reads `could not read` after the size |

Picking several files at once checks each one on its own. A file refused for its format or its size does not stop the rest from being attached.

## What the chip's second line reports

Every file you attach carries a chip above where you type, and its second line opens with the file's size: bytes below 1 KB, whole kilobytes below 1 MB, and one decimal place above that. What follows the size depends on the file:

| Second line | What it means |
|---|---|
| `1.2 MB · reading…` | The file is being read. The send control is waiting |
| `1.1 MB · describing…` | The file is being described. The send control is waiting |
| `4 KB` | A text file, read |
| `12 KB · 240 rows` | A CSV file, read. The count includes the header row |
| `8 KB · 8 keys` | A JSON file holding a set of fields, read |
| `8 KB · 12 items` | A JSON file holding a list, read |
| `1.2 MB · document` | A Word file, read |
| `1.2 MB · 14 pages` | A PDF, read for its own text |
| `1.2 MB · 14 pages · 4 pages described` | A PDF whose pages were described instead |
| `1.1 MB · described` | A picture, described |
| `1.2 MB · could not read` | A file shared by its name |
| `1.1 MB · could not describe` | A picture shared by its name |
| `… · truncated` | Added to any outcome that shared text, when that text was cut at 30,000 characters |

The send control is unavailable while any chip still reads `reading…` or `describing…`, and returns when every chip has settled. A send control that stays unavailable when no chip is waiting is locked for another reason: see [You cannot send a message](../troubleshooting/composer-is-locked.md).

## What the side panel reports

The **Shared in room** section of the side panel lists the files you have sent in this conversation. A file waiting as a chip above the message box is not in it yet, and a file you take off the message never reaches it. Until you send the first file, one line stands in place of the list: "Files you attach show up here for every character."

Each file in the list carries at most one note:

| Note beside the file | What the characters were given |
|---|---|
| No note | The file's own text |
| `described` | A description written in words |
| `name only` | The file name alone |

**Clear conversation**, in the three-dots menu in the room's top bar, empties the list. **Leave room** keeps it. See [Room controls reference](../running-the-room/room-controls-reference.md).

## Related pages

{% content-ref url="share-a-document.md" %}
[Share a document](share-a-document.md)
{% endcontent-ref %}

{% content-ref url="share-an-image.md" %}
[Share an image](share-an-image.md)
{% endcontent-ref %}

{% content-ref url="README.md" %}
[Share files with the room](README.md)
{% endcontent-ref %}
