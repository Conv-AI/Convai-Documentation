---
title: Briefs and transcripts
description: Answers for a brief that cannot be edited, an experience that will not be created, and a past session or transcript that will not open or download.
last_reviewed: "2026-09-10"
---

A chat experience settles its brief when you create it, and keeps every conversation it runs as a session you can read but not rejoin. Use this page when the brief will not do what you expect, or when a session or a transcript will not open, download, or hold what you thought it would.

## The brief cannot be edited

There is no control that edits a brief, anywhere in the product. The room type, the purpose, and the briefing every character receives are settled when the experience is created, and stay as they were written for every room opened from it.

Where an edit control would sit, the room shows a **Fixed at creation** label instead: in the room brief section of the side panel, on the pinned **Room brief** card while the room is empty, and on the experience's **Previous sessions** page. To run the same characters against different wording, use **Duplicate with a new brief**, on the three-dots menu on the experience's card or row. It opens the create dialog prefilled from the original, with the fields ready to change—apart from the one **Custom** exception in the next section.

{% content-ref url="../the-room-brief/why-the-brief-cannot-be-changed.md" %}
[Why the brief cannot be changed](../the-room-brief/why-the-brief-cannot-be-changed.md)
{% endcontent-ref %}

## The experience will not be created

**Create experience** stays unavailable until three fields in the create dialog are settled:

| What is missing | What to do |
|---|---|
| **Experience name** is empty | Name the experience. The field takes up to 80 characters |
| **Purpose** is empty | Write what the conversation is about. A **Custom** room type opens with this field empty, and the briefing box cannot be typed into until it holds something |
| You cleared **What each character will be told** | The box stays open with this line under it: "A blank briefing sends the written-for-you one instead. Write what the characters should be told, or reset to it." Write a briefing, or select **Reset to the written-for-you version** |

**Create experience** becomes available as soon as all three hold text, and selecting it opens the new experience's room.

An experience does not always save. When it does not, the dialog stays open and reports that the chat experience could not be created. Everything you typed is still in the fields, your own briefing included. Select **Create experience** again.

## No sessions are listed

An experience lists a session only for a room that recorded one, and it records a room once the room opens—which happens when you seat the first characters in it. A room that never finished connecting is not recorded, so a session can be missing because the room never came up. See [The room will not connect](room-will-not-connect.md).

An experience with nothing recorded shows a panel in place of the list, headed "No sessions recorded yet." A room you opened and left without adding anyone records nothing, so it never reaches the list.

Select **Start new session** to open a room from this experience and seat characters in it. That session takes a row on the page once the room has opened, whether or not anyone wrote in it.

## A session will not open

A session that cannot be read says so on the row, or on the session's own page once you have opened it:

| Where | What you see | What to do |
|---|---|---|
| The row on the experience's page | **Couldn't load** with a **Retry** button beside it | Select **Retry**. The row settles into the session's first question, with its date and message count beside it |
| The row on the experience's page | **No messages recorded** in place of the first question, and `0 messages` as the count | Nothing to open. That session ended before anyone wrote |
| The session's own page | **Couldn't load this session**, with "The transcript could not be fetched. Try again, or go back to the sessions list." and a **Retry** button | Select **Retry**. The thread replaces the panel. If it does not, go back to the list and open another session |
| The session's own page | **No messages recorded** | Nothing was said in that session, so there is no thread to read |

## A transcript will not download

**Export transcript** reports what stopped it:

| What you see | What it means | What to do |
|---|---|---|
| "Connect to a room before exporting its transcript." | The room is not connected—either no characters have been seated in it yet, or you left the room | Seat characters and send a message, or export a finished session from the experience's page |
| "This room hasn't recorded any messages yet." | The room is running but nothing has been said in it | Send a message first |
| **No messages recorded** | The session you exported from the experience's page recorded nothing | Nothing to export. Pick a session with a message count on its row |
| "Could not export the transcript" | The export did not finish | Select **Export transcript** again |

An export that worked says so: the browser saves the file, and the page confirms with **Transcript downloaded**.

A session longer than 200 [turns](../running-the-room/how-a-turn-works.md) exports its first 200 turns and no more. A turn is one message of yours and the replies it draws, so a session holds more messages than turns, and a row whose count ends in a plus sign—`412+ messages`—is one of these. Open that session to read the note at the top of its thread saying how much of the conversation is on the page. See [Export a transcript](../sessions-and-transcripts/export-a-transcript.md) for what the downloaded file holds.

## What a transcript leaves out

A transcript records what was said, not every detail the room showed while it was being said. The one setting it cannot tell you is which of two [respond modes](../running-the-room/respond-modes-reference.md) a turn ran under: **Auto · room brief decides** and **Anyone may respond** are kept the same way, so a turn sent under either reads back as Auto. Every other respond mode is kept as you set it, and a finished thread differs from a live room in a few other ways worth knowing before you read one.

A transcript also opens only for the account that recorded it, so a link to one does not open for anyone else. The exported file is how you hand a conversation to someone.

{% content-ref url="../sessions-and-transcripts/review-a-past-session.md" %}
[Review a past session](../sessions-and-transcripts/review-a-past-session.md)
{% endcontent-ref %}

## Still blocked

If a **Retry** or a second **Export transcript** ends the same way, contact [support@convai.com](mailto:support@convai.com). Name the chat experience, the session you were opening or exporting, and quote what the page showed you word for word.

## Related pages

{% content-ref url="../sessions-and-transcripts/README.md" %}
[Sessions and transcripts](../sessions-and-transcripts/README.md)
{% endcontent-ref %}

{% content-ref url="../manage-your-chat-experiences.md" %}
[Manage your chat experiences](../manage-your-chat-experiences.md)
{% endcontent-ref %}

{% content-ref url="../the-room-brief/write-your-own-briefing.md" %}
[Write your own briefing](../the-room-brief/write-your-own-briefing.md)
{% endcontent-ref %}
