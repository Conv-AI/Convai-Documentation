---
title: Export a transcript
description: Download a chat experience conversation as a Markdown file from a past session, from the sessions list, or from the room while it is still running.
last_reviewed: "2026-09-10"
---

A conversation held in a chat experience can be downloaded as a Markdown file, whether it has finished or is still running. Use this page to export one, and to know what the file holds before you open it.

## Prerequisites

- A chat experience session with messages in it. See [Sessions and transcripts](README.md).

## Export a session from an experience's history

**Export transcript** sits in three places: on a session's row on the experience's page, in the header of a session you have opened, and in the room's own menu while the conversation is still running. Every one of them produces the same file. The steps below take the first.

{% stepper %}
{% step %}
### Open the experience's history

Open the three-dots menu on the experience's card or row on **My Experiences** and select **Previous sessions**.

The experience's page opens with every session it recorded, newest first.
{% endstep %}

{% step %}
### Choose the session to export

Find the session by its number, its first question, or the day it ran. Each row carries all three.
{% endstep %}

{% step %}
### Export from the session's menu

Open the three-dots menu at the right of the session's row and select **Export transcript**.

The same export is available from inside the session: select **Open** on the row, then **Export transcript** at the top right of the header.
{% endstep %}

{% step %}
### Confirm the download

The browser saves the file, and the page confirms with **Transcript downloaded**. Any other message means no file was written, and it names what to do instead. See [Briefs and transcripts](../troubleshooting/briefs-and-transcripts.md).
{% endstep %}
{% endstepper %}

## Export the conversation you are in

A room exports the conversation recorded for the session running in it, covering every message sent so far. Characters have to be seated and the conversation under way before there is anything to export. Open the three-dots menu in the room's top bar and select **Export transcript**.

Going back to **My Experiences** afterwards does not cost you the conversation. It is recorded as a session of that experience and can be exported again from the experience's page.

## What the Markdown file holds

{% hint style="warning" %}
A session longer than 200 [turns](../running-the-room/how-a-turn-works.md) exports its first 200 turns and no more, whichever of the three routes produced the file. A session that ran past the limit says so in a note at the top of its own thread, before you export it.
{% endhint %}

The file is plain Markdown, readable in any text editor. It opens with a heading reading `# Room` followed by the session's identifier, which is the only thing in the file tying it to a session: neither the session's number, nor the experience's name, nor the date it ran is written into it.

After the heading comes one section per turn: your message, followed by one line for each reply it drew. A turn that carried files adds an italic line naming them between the two:

{% code title="room-3f8c1a44-e2d7-4f5c-9d0e-2a416f0c2b7e.md" %}
```markdown
# Room 3f8c1a44-e2d7-4f5c-9d0e-2a416f0c2b7e

## Turn 1 — open

Here is last quarter's pricing. What stands out?

_Attachments: q3-pricing.pdf_

**Maya**: The renewal rate is the outlier.
**Luis**: _passed_

## Turn 2 — tagged

Maya, what did you think of the price?

**Maya**: It felt high for what you get.
```
{% endcode %}

Turns are numbered from the start of the conversation, and the word after the turn number is how the turn was addressed: `all` for a message everyone had to answer, `tagged` for one that named the characters it wanted, and `open` for one the room was free to answer or leave. That last word covers a turn sent under **Auto · room brief decides** and one sent under **Anyone may respond** alike, so the file does not say which of the two a turn ran under. See [what a transcript does not record](review-a-past-session.md#what-a-transcript-does-not-record) for the rest of what a saved conversation leaves behind.

A character that stayed quiet on an `open` turn takes a line of its own reading `_passed_`, rather than the single note the session's page shows in its place. The attachments line names the files shared on a turn, and the names are all of them it keeps: no file contents travel with the transcript.

## What the file is called

The name is `room-` followed by the session's own identifier and `.md`, so the example above downloads as `room-3f8c1a44-e2d7-4f5c-9d0e-2a416f0c2b7e.md`.

Every session has an identifier of its own. Exporting several sessions of one experience therefore produces several differently named files, and none of them overwrites another. The name does not use the room ID shown in the room's top bar, which is the same for every session of an experience.

## Next steps

{% content-ref url="review-a-past-session.md" %}
[Review a past session](review-a-past-session.md)
{% endcontent-ref %}

{% content-ref url="../troubleshooting/briefs-and-transcripts.md" %}
[Briefs and transcripts](../troubleshooting/briefs-and-transcripts.md)
{% endcontent-ref %}

{% content-ref url="README.md" %}
[Sessions and transcripts](README.md)
{% endcontent-ref %}
