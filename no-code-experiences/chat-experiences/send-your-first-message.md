---
title: Send your first message
description: Write and send a message in a chat experience room, address a character so it answers, and read the replies as they arrive.
last_reviewed: "2026-09-10"
---

You are the moderator of a chat experience, and the characters answer you rather than talk among themselves. Use this page to send the first message in a room, to address a character so that it replies, and to read what the thread reports once the turn is over. Chat Experiences is in beta.

## Prerequisites

- A chat experience room with at least one character already in it. See [Add characters to the room](add-characters-to-the-room.md).

## Send a message

{% stepper %}
{% step %}
### Write the message

Select the message box at the bottom of the room and type.

The prompt in the box tells you who you are writing to. In a room with several characters it reads **Ask the group…** before the conversation starts, and **Ask the group, or @tag someone…** afterwards. In a one-character room it reads **Message** followed by that character's name.
{% endstep %}

{% step %}
### Send it

Press `Enter`, or select the send button—the upward arrow at the bottom right of the message box. `Shift`+`Enter` starts a new line instead of sending.

Your message appears in the thread, and the message box locks until the turn finishes.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
A message that addresses nobody in particular can produce no reply at all. Characters answer when they are addressed and stay quiet otherwise, so name a character or tag one when you want a specific answer.
{% endhint %}

## Address a character so it answers

A room runs on **Auto** unless you change it, and under Auto the brief decides who answers—a character replies when it is addressed and stays quiet otherwise. The chip under what you are typing shows the mode the next message will use, and reads **Auto · room brief decides** until you change it.

Before the first message in a room of two or more characters, the thread states the rule you are working under: "Respond mode is set to Auto: the brief decides who answers. Use @tags or the chip to override on any message." What each room type asks of its characters is set out in [How the room brief is written](the-room-brief/how-the-room-brief-is-written.md).

Addressing a character means naming it. Writing "Maya, what did you think of the price?" addresses Maya; writing "What did you think of the price?" addresses nobody in the room.

Tagging is the explicit version, and the only one the room enforces. Type `@` in the message box and pick the character you want from the list that opens.

A tagged character is required to reply, and the room holds it to that rather than leaving the decision to the character. In a room of two or more characters, the chip changes to show who the message is going to, and every character you did not tag stays out of that turn.

For the rest of the tag list, and for setting the chip so that it holds from one message to the next, see [Choose who replies](running-the-room/choose-who-replies.md).

## What the thread shows after you send

Every character in the room appears in the thread with its name and an animated typing indicator while the turn runs, whether or not it ends up answering. A reply replaces that character's indicator when it arrives, and the indicators still standing clear together when the turn finishes.

Under your own message, a caption reports what the turn asked for and what came back. In a room of two or more characters running on Auto, the caption reads **Auto · room brief decides**, followed by an outcome built from up to three counts:

| Count | Meaning |
|---|---|
| `2 of 4 responded` | How many of the characters in the room when you sent the message have replied, out of how many were in it |
| `1 listening` | How many have not replied and have not been reported as not answering. While the turn runs, these are the characters still to answer; once it is over, they are the ones that stayed quiet |
| `1 did not answer` | How many the room reported as not answering |

In a one-character room the caption names that character instead—**Sent to** followed by the name—and adds `replied` once the reply is in, or `waiting` while the turn is still running. If the character stays quiet, the caption carries no outcome at all.

While the turn is running, the message box carries the wait in place of the usual prompt: **Waiting for 2 of 4…**, where the first number is how many replies are still outstanding rather than how many have arrived. It reads **Finishing the turn…** as the turn settles, and unlocks when the turn is over.

For what the counts read in the other respond modes, see [How a turn works](running-the-room/how-a-turn-works.md).

## When a character stays quiet

A character that had nothing to answer is named in a note below the replies, and the note tells you how to get its side.

Under Auto, the note names the characters and reads "stayed quiet, as the brief asks. Tag them if you want their side." When more than one character stayed quiet, the last sentence reads "Tag one of them if you want their side." instead. A room where every character stayed quiet produces this note and no replies.

A character named in that note is counted under `listening` in the caption, not under `did not answer`. The two are different outcomes: a quiet character chose to say nothing.

To get an answer from a character named in that note, send another message that tags it.

## Next steps

Once you have run a conversation, the experience is one of several on **My Experiences**, and finding it again, renaming it, or duplicating it with a new brief are separate tasks.

{% content-ref url="manage-your-chat-experiences.md" %}
[Manage your chat experiences](manage-your-chat-experiences.md)
{% endcontent-ref %}

To decide who answers rather than leaving it to the brief, read what each respond mode asks of the characters.

{% content-ref url="running-the-room/respond-modes-reference.md" %}
[Respond modes reference](running-the-room/respond-modes-reference.md)
{% endcontent-ref %}
