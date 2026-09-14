---
title: The room will not connect
description: Fix a chat experience room whose characters are still joining, an experience that will not open, and a character ID the picker cannot resolve.
last_reviewed: "2026-09-10"
---

A chat experience room opens empty and connects the moment you seat the first characters. When that does not happen, the room says so in the message box, in the character picker, or on the page that should have held the experience. Use this page to read those messages and get the room running.

## The characters are still joining

Joining takes several seconds, and the room says so while it happens.

Each character you picked takes a row in the [side panel](../running-the-room/room-controls-reference.md) straight away with **Joining the room…** under its name, and the message box is locked and reads **Waiting for characters to join…**. The roster controls are frozen for the same stretch, with **Connecting the room…** as the reason under **Add characters**.

All three clear on their own: the rows settle into ordinary rows, the thread adds a divider naming the characters and stating that they joined and were briefed, and the message box takes your first message.

If the room does not come up, the message box changes to **The room could not connect. Pick the characters again to retry.**, the joining rows go, and the room shows a notification with the reason. Note what it says, then follow the next section.

## The room could not connect

The message box reads **The room could not connect. Pick the characters again to retry.** when the room did not open. Nothing was seated, nothing was said, and no session was recorded.

{% stepper %}
{% step %}
### Open the character picker again

The room is empty, so **Add characters** sits where it does in any empty room: on the **Add the participants** card in the side panel, and under **Nobody is in the room yet** in the thread. Either one opens **Add characters to the room**.
{% endstep %}

{% step %}
### Pick the characters and confirm

Pick the same characters as before and confirm. The picker works as it did the first time, on the same two tabs. See [Add characters to the room](../add-characters-to-the-room.md) for either route through it.

The rows show **Joining the room…** again, and the message box returns to **Waiting for characters to join…**.
{% endstep %}

{% step %}
### Check that the room came up

The rows settle, the thread names the characters as joined and briefed, and the message box unlocks with a writing prompt in it. A retry starts a fresh conversation, so the prompt is the one a room shows before its first message: **Ask the group…**, or **Message** followed by the character's name in a room of one. The prompt changes once you have written to the room, and [Send your first message](../send-your-first-message.md) covers every form of it.
{% endstep %}
{% endstepper %}

## The experience will not open

An experience that will not open says so in place of the room or the list, and each of these states carries its own way back:

| What you see | What it means | What to do |
|---|---|---|
| A panel headed **This chat experience could not be loaded**, with a **Back to My Experiences** button under it | The panel names both possibilities itself: "It may have been deleted, or the server could not be reached." | Select **Back to My Experiences** and open the experience again from the list. An experience still missing from a list that has loaded cleanly has been deleted |
| "Chat experiences could not be loaded." on **My Experiences**, with **Retry** beside it | None of the list arrived, so nothing can be opened from it | Select **Retry**. The list fills with your experiences and the message goes |
| "Chat experiences could not be loaded. What is shown may not be everything." with **Retry** | Part of the list arrived, so an experience of yours can be absent from what is on show | Select **Retry** before you decide an experience is missing from the list |

## A character cannot be added

A character you look up under **By character ID** becomes a row under **Results**, and a row that did not resolve says which of three things happened:

| The row reads | What it means | What to do |
|---|---|---|
| **No access to** followed by a shortened form of the ID | "This character exists but hasn't been shared with you. Ask its owner to share it or make it public." | Ask the character's owner to share it with you, then look the ID up again |
| **No character with ID** followed by a shortened form of the ID | "No character with this ID is available to you. Check it for typos, or ask whoever shared it to share the character with you." | Check the ID against the one you were given and look it up again |
| **Could not look up** followed by a shortened form of the ID | "Something went wrong while looking this character up. Try again." | Select the look-up button again |

Any of the three is cleared when the row comes back with the character's name, its description, and an **Add** button on it.

On **From my workspaces**, a search that matches nothing reads "No characters match." Clear the search field to bring the grid back, and expand it with the button under the grid when the character you want is outside the eight most recently edited. If the search field is already empty, the tab has no characters to offer you at all, so look the character up under **By character ID** instead.

## Still blocked

If the room fails again with the same notification, or the list still will not load after a **Retry**, contact [support@convai.com](mailto:support@convai.com). Name the chat experience you were opening and quote the notification word for word.

## Related pages

These pages answer the chat experience symptoms this one does not.

{% content-ref url="composer-is-locked.md" %}
[You cannot send a message](composer-is-locked.md)
{% endcontent-ref %}

{% content-ref url="briefs-and-transcripts.md" %}
[Briefs and transcripts](briefs-and-transcripts.md)
{% endcontent-ref %}

{% content-ref url="../add-characters-to-the-room.md" %}
[Add characters to the room](../add-characters-to-the-room.md)
{% endcontent-ref %}
