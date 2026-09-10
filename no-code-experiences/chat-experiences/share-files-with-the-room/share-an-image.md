---
title: Share an image
description: Attach a picture to a message in a chat experience room, and understand that the characters receive a written description rather than the picture.
last_reviewed: "2026-09-10"
---

A picture you attach to a message in a chat experience room reaches the characters as words. Use this page to attach a `.png`, `.jpg`, or `.jpeg` picture, to send it with a message, and to know exactly what the characters are told about it. Chat Experiences is in beta.

## Prerequisites

- A chat experience room with at least one character already in it. See [Add characters to the room](../add-characters-to-the-room.md).
- A picture in an accepted format. See [File limits reference](file-limits-reference.md).

## Attach a picture and send it

{% stepper %}
{% step %}
### Pick the picture

Select the paperclip at the left of the message box, below where you type, and pick the file. You can pick several files at once.

A chip appears above where you type, carrying the format, the file name, and a second line reading `reading…` after the size.
{% endstep %}

{% step %}
### Wait for the description

The second line changes to `describing…` while the picture is being described, and settles to `described` when it is done. The send control stays unavailable until every chip has settled.

Describing a picture takes seconds rather than the instant a text file takes. The wait is normal and the send control returns on its own.
{% endstep %}

{% step %}
### Write the message and send

Write your question and send the message as usual. The chip moves into the thread above your words, and the file is added to the **Shared in room** section of the side panel.

Ask about the picture in the same message if you want an answer about it. Under **Auto · room brief decides**, the mode a room opens on, a picture sent with no question addresses nobody in particular, and a character that is not addressed stays quiet.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The picture reached the characters when its chip in the thread reads `described` after the size, and the file is listed under **Shared in room** in the side panel.
{% endhint %}

## Who receives the picture

Whoever the turn addresses is who gets the picture. A character the message did not address is not given the description, and the replies that follow do not pass it on. To put a picture in front of every character, tag `@everyone` or set the respond chip to **Everyone must respond** before you send. See [Choose who replies](../running-the-room/choose-who-replies.md).

## What the characters are told

The characters never receive the picture. They receive a description of it, written in words, and the description is what they answer from.

The description does not arrive on its own: the characters are told these words describe a picture you attached, and are asked to answer from them as though they were looking at the picture rather than saying they cannot see it. An answer therefore reads as though the character had seen the picture, and whatever the description left out is answered with the same confidence as whatever it covered.

Two things follow, and both are worth knowing before you attach:

- **A description is not the picture.** Detail the description does not mention is detail the characters do not have, and nothing in the answer marks the difference. Check an answer that turns on fine detail against the picture in front of you.
- **Ask about what you want covered.** A question naming what matters in the picture gives you a more useful answer than attaching it with no question at all.

## What the chip reports

The chip's second line always opens with the file's size. What follows tells you what the characters were given:

| What the second line reads | What the characters received |
|---|---|
| `1.1 MB · describing…` | Nothing yet. The picture is being described and the send control is waiting |
| `1.1 MB · described` | A description of the picture, written in words |
| `1.1 MB · could not describe` | The file name alone |

The side panel repeats that second line and adds a short note beside it. In **Shared in room**, a described picture is marked `described`, and a picture shared by its name alone is marked `name only`.

## When a picture is shared by name alone

A picture that could not be described is still sent, by name alone. The characters are given the file name and nothing else, and the message is not held back.

The room tells you in two places at once. The chip's second line settles to `could not describe` after the size, and a message reads "Could not describe ⟨name⟩; only its name will be shared".

{% hint style="warning" %}
Check the chip before you send a picture the conversation depends on. A file name tells the characters that something was attached and nothing about what is in it, so they answer without any account of the picture at all.
{% endhint %}

## Next steps

A PDF carrying little text of its own is described the same way a picture is, and its chip reports the page count as well.

{% content-ref url="share-a-document.md" %}
[Share a document](share-a-document.md)
{% endcontent-ref %}

For the accepted formats, the size and text limits, and what happens at each one:

{% content-ref url="file-limits-reference.md" %}
[File limits reference](file-limits-reference.md)
{% endcontent-ref %}

If a picture drew an answer that missed it, or no answer at all, start from what you can see on screen: [Troubleshoot Chat Experiences](../troubleshooting/README.md).
