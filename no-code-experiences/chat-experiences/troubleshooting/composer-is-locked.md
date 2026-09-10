---
title: You cannot send a message
description: Work out why the message box in a chat experience room will not take a message, using the reason the room shows, and what clears each one.
last_reviewed: "2026-09-10"
---

The message box in a chat experience room locks whenever the room cannot take a message, and it always says why. Chat Experiences is in beta. Use this page to read the reason the room gives you, to clear it, and to tell a locked box apart from a message that went nowhere.

## What each locked message means

The message box replaces its writing prompt with the reason it is locked. If you had already typed something or attached a file, the reason also appears on a line under the box, and your text and your files stay where they are. The box carries one of five reasons:

| What the box reads | What it means | What clears it |
|---|---|---|
| **Add at least one participant to start** | The room has nobody in it, so there is nobody to send to | Add at least one character. See [Add characters to the room](../add-characters-to-the-room.md) |
| **Waiting for characters to join…** | No character in the room has finished joining yet | Wait for the side panel to finish seating the characters: a row reads **Joining the room…** first, then settles into the character's name and role. Or add a character if you have removed the last one |
| **The room could not connect. Pick the characters again to retry.** | The room did not open. Any characters still listed in the side panel are not connected | Pick the characters again. See [The room will not connect](room-will-not-connect.md) |
| **Waiting for 2 of 4…** | A turn is running. The first number is how many characters have not started replying, the second how many the turn asked for | Wait for the turn to finish |
| **Finishing the turn…** | The turn is settling, or its last reply is still due | Wait. The box unlocks on its own |

Whichever reason you are clearing, you know it is gone when the reason leaves the box and the writing prompt takes its place: **Ask the group…** in a room of several characters, or **Message** followed by the character's name in a room of one. [Send your first message](../send-your-first-message.md) covers every form the prompt takes.

Three of the five reasons are about the room itself: nobody seated, characters still joining, and a room that did not open. The other two count a turn you have already sent, and [How a turn works](../running-the-room/how-a-turn-works.md) covers what the counts mean and why a turn asks a particular set of characters.

## The wait does not end

The room stops waiting two minutes after you send. It then reports "The room did not finish this turn in time.", unlocks the message box, and leaves whatever did arrive in the thread. The writing prompt is back, so you can send the message again straight away.

## The room reports a turn already in progress

A turn you have sent can report "The room reports a turn already in progress. If nobody answers, wait for it to finish and send again." Do exactly that. The message box stays locked while that turn is live and unlocks when it settles, and if the writing prompt comes back with nothing added to the thread, send the message again.

## Your message reads Not sent

A message the room never received stays in the thread greyed out, with **Not sent** under it, and the room reports "Could not send the message."

Nothing reached the characters and no reply is coming. The box is unlocked and the writing prompt is back in it, so write the message again and send it. The greyed message stays in the thread as a record that it did not go.

## You can type, but the send control is unavailable

The message box takes your text and carries no reason, but the send control does not respond. A file you have attached is still being read: the chip carrying it reads `reading…` after the file size, and `describing…` while a picture or a set of PDF pages is being described.

Nothing is blocked. The send control returns on its own once every chip has settled, and a picture takes seconds rather than the instant a text file takes. A send control that stays unavailable when no chip is waiting means the box is locked for a reason of its own, and the box says which.

{% content-ref url="../share-files-with-the-room/file-limits-reference.md" %}
[File limits reference](../share-files-with-the-room/file-limits-reference.md)
{% endcontent-ref %}

## The room says it is not connected

Sending in a room whose conversation has already ended reports "Not connected to a room.", and nothing is added to the thread.

A conversation that has ended cannot be rejoined, but a new one starts where you are: select **Add characters** in the side panel and pick the characters again. Going back to **My Experiences** and opening the experience again does the same thing. The brief carries over; the characters and the messages do not. The new conversation is ready when the rows settle and the writing prompt is back in the box.

{% hint style="warning" %}
Reloading the page while a room is open ends that conversation. Reloading to clear a locked message box costs you the conversation and leaves you in an empty room.
{% endhint %}

## The message sent but nobody answered

A character answers when it is addressed and stays quiet otherwise, so a message that addresses nobody in particular can draw no reply at all. To get an answer from a particular character, send another message that tags it with `@`.

{% content-ref url="../running-the-room/how-a-turn-works.md" %}
[How a turn works](../running-the-room/how-a-turn-works.md)
{% endcontent-ref %}

## Still blocked

When what you are seeing is on none of these pages, the troubleshooting hub lists every chat experience symptom against the page that answers it, and carries the support route for anything left over.

{% content-ref url="README.md" %}
[Troubleshoot Chat Experiences](README.md)
{% endcontent-ref %}

## Related pages

{% content-ref url="../running-the-room/choose-who-replies.md" %}
[Choose who replies](../running-the-room/choose-who-replies.md)
{% endcontent-ref %}

{% content-ref url="../running-the-room/add-or-remove-characters.md" %}
[Add or remove characters mid-conversation](../running-the-room/add-or-remove-characters.md)
{% endcontent-ref %}
