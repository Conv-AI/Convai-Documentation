---
title: File limits reference
description: Reference for the file types a chat experience room accepts, the size and length limits on an attachment, and what each chip line means.
last_reviewed: "2026-11-12"
---

A chat experience room accepts a short list of file formats and limits how much of a file it shares with the characters. This page lists the formats, the limits, and what the room does when a file passes one.

## Accepted file types

| Kind | Extensions | What reaches the characters |
|---|---|---|
| PDF | `.pdf` | The document itself |
| Pictures | `.png`, `.jpg`, `.jpeg`, `.webp` | The picture |
| Video | `.mp4`, `.webm`, `.mkv`, `.m4v`, `.mov` | Frames taken from the video, and a transcript of its speech |
| Word | `.docx` | The document's text |
| Plain text | `.txt`, `.md`, `.csv`, `.json` | The file's own text |

Whatever the kind, a file goes to the characters that turn is addressed to, and a character the message did not address is not given it. See [Share files with the room](README.md) for how to address everyone.

The room states the limits itself, on a line under the message box: "PDF: up to 10 MB, 33 pages. Video: MP4, WebM, MKV, M4V, MOV · up to 50 MB, 10 min. Images: PNG, JPG, WebP · up to 10 MB. Other documents: up to 25 MB."

Anything not in the table is refused when you pick or drop it, and nothing about it is sent.

## Size and length limits

| Limit | Value |
|---|---|
| One PDF | 10 MB and 33 pages |
| One picture | 10 MB |
| One video | 50 MB and 10 minutes |
| Videos on one message | 1 |
| One Word or plain-text file | 25 MB |
| Text shared from one Word or plain-text file | 30,000 characters |
| Text shared across one message | 60,000 characters |

The two character limits apply to Word and plain-text files, and count what is shared, not what the file holds.

A long PDF can leave less room than its page limit suggests, because the pages share space with the conversation so far and with the other files on the message.

## What happens at each limit

| What you did | What the room does |
|---|---|
| Picked a file whose format is not accepted | The file is not attached. A message reads "⟨name⟩ is not a supported file type." |
| Picked a file over the size limit for its kind | The file is not attached. A message reads "⟨name⟩ is larger than ⟨limit⟩.", for example "larger than 10 MB." |
| Added a second video to a message | The second video is not attached. A message reads "Attach one video per message. Send this one before adding another." |
| Attached a PDF of more than 33 pages, or a video longer than 10 minutes | The chip settles to the reason, ending "Retry or remove.", and the message cannot be sent until you remove the file |
| Attached a Word or plain-text file holding more than 30,000 characters | The file is attached and sent. The text is cut at the limit, the rest is not shared, and `truncated` is added to the chip |
| Attached Word or plain-text files that together pass 60,000 characters | The file that passed the limit is taken off the message. A message reads "⟨name⟩ would put this message over the 60,000-character limit for shared text. Send it on its own or remove another file." |
| Attached a Word or plain-text file the room could not read | The file is sent by name alone. The chip reads `could not read` after the size |

Picking several files at once checks each one on its own. A file refused for its format or its size does not stop the rest from being attached.

## What the chip's second line reports

Every file you attach carries a chip above where you type, and its second line opens with the file's size: bytes below 1 KB, whole kilobytes below 1 MB, and one decimal place above that. What follows the size depends on the file:

| Second line | What it means |
|---|---|
| `1.2 MB · reading…` | The file has just been attached. The send control is waiting |
| `1.2 MB · uploading 40%` | A PDF, picture, or video is being uploaded. The send control is waiting |
| `1.2 MB · validating PDF…` | A PDF is being checked. The send control is waiting |
| `24 MB · processing…` | A picture or video is being prepared. The send control is waiting |
| `1.2 MB · 14 pages · PDF ready` | A PDF, ready to send |
| `1.1 MB · image ready` | A picture, ready to send |
| `24 MB · 32 frames · speech transcript ready` | A video, ready to send, with its speech transcribed |
| `24 MB · 32 frames · no speech transcript` | A video, ready to send, whose audio could not be transcribed |
| `24 MB · 32 frames · no audio track` | A silent video, ready to send |
| A reason ending `Retry or remove.` | A PDF, picture, or video that could not be prepared. The message cannot be sent until you retry the file or remove it |
| `4 KB` | A text file, read |
| `12 KB · 240 rows` | A CSV file, read. The count includes the header row |
| `8 KB · 8 keys` | A JSON file holding a set of fields, read |
| `8 KB · 12 items` | A JSON file holding a list, read |
| `1.2 MB · document` | A Word file, read |
| `1.2 MB · could not read` | A Word or plain-text file shared by its name |
| `… · truncated` | Added to a Word or plain-text file whose text was cut at 30,000 characters |

A video is shared as up to 32 frames, about one for each second of a short clip and spread across a longer one.

The send control is unavailable while any chip is still waiting or has failed, and returns when every chip is ready. A send control that stays unavailable when no chip is waiting is locked for another reason: see [You cannot send a message](../troubleshooting/composer-is-locked.md).

## What the side panel reports

The **Shared in room** section of the side panel lists the files you have sent in this conversation. A file waiting as a chip above the message box is not in it yet, and a file you take off the message never reaches it. Until you send the first file, one line stands in place of the list: "Files you attach show up here for every character."

A Word or plain-text file that was shared by its name alone is marked `name only` in the list.

The list empties when the conversation ends, which **Clear conversation** and **Leave room** in the three-dots menu in the room's top bar both do. A file on a message that failed to send is not listed. See [Room controls reference](../running-the-room/room-controls-reference.md).

## Related pages

{% content-ref url="share-a-document.md" %}
[Share a document](share-a-document.md)
{% endcontent-ref %}

{% content-ref url="share-an-image.md" %}
[Share an image or a video](share-an-image.md)
{% endcontent-ref %}

{% content-ref url="README.md" %}
[Share files with the room](README.md)
{% endcontent-ref %}
