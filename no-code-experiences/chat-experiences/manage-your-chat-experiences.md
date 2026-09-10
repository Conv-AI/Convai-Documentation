---
title: Manage your chat experiences
description: Find, search, rename, duplicate, and delete the chat experiences on your account, and run the same characters against different wording.
last_reviewed: "2026-09-10"
---

Every chat experience you create stays on **My Experiences** until you delete it. Use this page to find one again, to rename it, to delete it, and to duplicate it when you want to run the same kind of conversation with a different brief.

## Find a chat experience

Chat experiences are listed in the **Chat experiences** section of **My Experiences**, above the **3D experiences** section. See [Open My Experiences](open-my-experiences.md) for how to reach it. The heading carries the number of chat experiences on the account.

Selecting a card or a row opens a new room from that experience. It does not reopen the last conversation.

Three controls work on that list:

| Control | What it does |
|---|---|
| **Search chat experiences** | Filters the list. Every word you type has to appear in the experience name or in its purpose. A search with no results shows **No chat experiences match your search.** |
| The two view buttons beside the search box | Switch between a grid of cards and a list of rows. The browser remembers your choice. On a narrow window the list falls back to the grid, because the row cannot hold its columns. |
| The three-dots menu on a card or row | Opens **Previous sessions**, **Rename**, **Duplicate with a new brief**, and **Delete** for that experience. |

**Previous sessions** opens the conversations already run from that experience, each one a transcript you can read but not add to. See [Chat Experiences](README.md).

The grid shows a card per experience: its room type, its name, the first two lines of its purpose, and a session line reading either **No sessions yet** or the number of sessions and when the last one ran. The list shows the same experiences as rows, adding an **ID** column carrying the room ID, which you can copy from the row.

If the section reads **No chat experiences yet**, nothing has been created on the account. See [Create a chat experience](create-a-chat-experience.md).

## Rename a chat experience

Renaming changes the label on the card and in the room's top bar. It does not touch the brief.

{% stepper %}
{% step %}
### Open the rename dialog

Open the three-dots menu on the experience's card or row and select **Rename**.

The **Rename chat experience** dialog opens with the current name in the **Name** field.

An open room has its own route to the same rename. The pencil beside the room name and **Rename experience** on the top bar's three-dots menu both open a **Rename experience** dialog with an **Experience name** field.
{% endstep %}

{% step %}
### Save the new name

Type the new name and select **Save**.

The field grays out and shows **Saving…** while the change is being stored, and the dialog closes once it has been.
{% endstep %}
{% endstepper %}

## Duplicate an experience with a new brief

**Duplicate with a new brief** is how you run the same kind of conversation against different wording. The room type, the purpose, and the briefing are fixed when an experience is created, so changing any of them means creating another experience—and duplicating starts you from the original rather than from a blank dialog. See [Why the brief cannot be changed](the-room-brief/why-the-brief-cannot-be-changed.md).

To put the same characters through a different brief, duplicate the experience, change the wording, and add those characters to the new room.

{% stepper %}
{% step %}
### Start the duplicate

Select **Duplicate with a new brief**. It appears on the three-dots menu on the experience's card or row, on the three-dots menu in an open room's top bar, and in the tooltip on the room's **Fixed at creation** label.

That label sits in the room's side panel, and on the pinned **Room brief** card while the room is still empty.
{% endstep %}

{% step %}
### Change the wording

The **Create a chat experience** dialog opens prefilled from the original: the same room type, the same purpose, the same briefing if one was written by hand, and the original name with `(copy)` after it.

Every field is editable, because this is a new experience rather than an edit of the old one. Change the purpose, the room type, the briefing, or all three.

The **Custom** room type has one exception. While its purpose is empty and no briefing came across from the original, the briefing box shows an example of what a briefing looks like instead of taking your typing.
{% endstep %}

{% step %}
### Create it

Select **Create experience**.

The duplicate opens as its own empty room and appears as a separate card on **My Experiences**. The original is untouched, and its previous sessions stay with it.
{% endstep %}
{% endstepper %}

## Delete a chat experience

Deleting removes the experience from **My Experiences**, along with its list of previous sessions.

{% hint style="danger" %}
Deleting a chat experience cannot be undone. The dialog says so, and there is no way to restore the experience or its previous sessions afterwards.
{% endhint %}

{% stepper %}
{% step %}
### Open the delete dialog

Open the three-dots menu on the experience's card or row and select **Delete**.

The **Delete chat experience** dialog names the experience and asks you to confirm.
{% endstep %}

{% step %}
### Confirm the deletion

Select **Delete** to confirm, or **Cancel** to keep the experience.

The card disappears from the list, and a confirmation message reports that the chat experience was deleted.
{% endstep %}
{% endstepper %}

## Next steps

The brief you duplicate here is fixed for a reason, and the section that explains it also covers how a briefing is written. Creating an experience from scratch starts in the same dialog a duplicate opens.

{% content-ref url="the-room-brief/why-the-brief-cannot-be-changed.md" %}
[Why the brief cannot be changed](the-room-brief/why-the-brief-cannot-be-changed.md)
{% endcontent-ref %}

{% content-ref url="create-a-chat-experience.md" %}
[Create a chat experience](create-a-chat-experience.md)
{% endcontent-ref %}
