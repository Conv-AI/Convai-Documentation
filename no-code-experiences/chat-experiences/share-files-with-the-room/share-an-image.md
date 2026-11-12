---
title: Share an image or a video
description: Attach a picture or a video to a message in a chat experience room, and understand what the characters are given from it.
last_reviewed: "2026-11-12"
---

A picture you attach to a message in a chat experience room reaches the characters as the picture, and a video reaches them as frames and a transcript of its speech. Use this page to attach either one, to send it with a message, and to read what the room reports about it.

## Prerequisites

- A chat experience room with at least one character already in it. See [Add characters to the room](../add-characters-to-the-room.md).
- A picture or a video in an accepted format and within its size limit. See [File limits reference](file-limits-reference.md).

## Attach a picture or a video and send it

{% stepper %}
{% step %}
### Pick the file

Select the paperclip at the left of the message box, below where you type, and pick the file. You can pick several files at once, with one video among them at most. Or drag the files from your computer onto the conversation and drop them. See [Drag files onto the conversation](README.md#drag-files-onto-the-conversation).

A chip appears above where you type, carrying the format, the file name, and a second line that opens with the size.
{% endstep %}

{% step %}
### Wait for the chip to settle

The second line reads `uploading` with a percentage, then `processing…`, and settles to `image ready` for a picture or to a frame count for a video. The send control stays unavailable until every chip is ready.

A video takes longer than a picture, because its frames are taken and its speech is transcribed before it can be sent.
{% endstep %}

{% step %}
### Write the message and send

Write your question and send the message as usual. The chip moves into the thread above your words, and the file is added to the **Shared in room** section of the side panel.

Ask about the file in the same message if you want an answer about something in particular. On the default, **Everyone must respond**, a file sent with no question is still addressed to every character.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The file reached the characters when its chip in the thread reads `image ready` or a frame count after the size, and the file is listed under **Shared in room** in the side panel.
{% endhint %}

## Who receives the file

Whoever the turn addresses is who gets the file. A character the message did not address is not given it, and the replies that follow do not pass it on. To put a file in front of every character, leave the respond chip on **Everyone must respond**, the mode a room opens on, or tag `@everyone`. See [Choose who replies](../running-the-room/choose-who-replies.md).

## What the characters are given

| What you attach | What the characters are given |
|---|---|
| A picture—`.png`, `.jpg`, `.jpeg`, or `.webp`, up to 10 MB | The picture itself |
| A video—`.mp4`, `.webm`, `.mkv`, `.m4v`, or `.mov`, up to 50 MB and 10 minutes | Up to 32 frames taken across the video, and a transcript of its speech when it has any |

A video is not played to the characters. They work from the frames and the transcript, so movement between frames and sound that is not speech do not reach them. Ask about what you want covered, and check an answer that turns on a moment of the video against the video itself.

## What the chip reports

The chip's second line always opens with the file's size. What follows tells you where the file has got to:

| What the second line reads | What it means |
|---|---|
| `1.1 MB · uploading 40%` | The file is being uploaded. The send control is waiting |
| `1.1 MB · processing…` | The file is being prepared. The send control is waiting |
| `1.1 MB · image ready` | A picture, ready to send |
| `24 MB · 32 frames · speech transcript ready` | A video, ready to send, with its speech transcribed |
| `24 MB · 32 frames · no speech transcript` | A video, ready to send, whose audio could not be transcribed. The characters are given the frames alone |
| `24 MB · 32 frames · no audio track` | A silent video, ready to send |
| A reason ending `Retry or remove.` | The file could not be prepared, and the message cannot be sent with it |

## When a file cannot be prepared

A picture or a video that cannot be prepared is not sent. Its chip gives the reason, ending "Retry or remove.", and the message is held back until you retry the file or take it off with the × on its chip.

A file over the size limit for its kind is refused when you pick it, with a message reading "⟨name⟩ is larger than ⟨limit⟩." A second video on one message is refused with "Attach one video per message. Send this one before adding another."

## Next steps

A PDF, a Word file, and plain-text formats are attached the same way and reported in their own words.

{% content-ref url="share-a-document.md" %}
[Share a document](share-a-document.md)
{% endcontent-ref %}

For the accepted formats, the limits, and what happens at each one:

{% content-ref url="file-limits-reference.md" %}
[File limits reference](file-limits-reference.md)
{% endcontent-ref %}

If a file drew an answer that missed it, or no answer at all, start from what you can see on screen: [Troubleshoot Chat Experiences](../troubleshooting/README.md).
