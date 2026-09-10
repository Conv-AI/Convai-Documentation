---
title: Write your own briefing
description: Replace the briefing written for you in the create dialog with your own wording, and put the written-for-you version back when you want it.
last_reviewed: 2026-09-10
---

The briefing every character receives is written for you, and the create dialog is the one place where you can replace that wording with your own—creating the experience settles the briefing, and **Duplicate with a new brief** opens the same dialog on a copy when you want different wording later. Chat Experiences is in beta. Use this page to rewrite the briefing in the **What each character will be told** box, to put the written-for-you version back, and to understand what your own wording replaces.

## Prerequisites

- The **Create a chat experience** dialog open, with a room type picked. See [Create a chat experience](../create-a-chat-experience.md).
- Text in the **Purpose** field. A purpose is required before the experience can be created.

{% hint style="info" %}
The **Custom** room type opens with an empty **Purpose** field. Until you write one, **What each character will be told** shows an example briefing rather than yours, and it cannot be typed into. Write the purpose first—the box then holds the briefing written from your words and accepts your edits. See [Room types reference](room-types-reference.md).
{% endhint %}

## Replace the briefing with your own words

{% stepper %}
{% step %}
### Find the briefing box

Below **Purpose**, the **What each character will be told** box is already open. Its header line closes the box and opens it again.

The box holds the briefing written for you: the sentence the room type opens with, the purpose you entered in the middle, and the rules that room type closes with. Under the briefing sit the rules chips—the short form of those rules—and a footnote stating that the briefing goes to every character on top of its own persona, and that it is fixed once the experience is created.

What the box shows is the briefing for a room of two or more characters. A room you seat a single character in is briefed in its own words: a different opening sentence, different closing rules, and a fixed set of three rules chips beside them, whichever room type you picked. See [How the room brief is written](how-the-room-brief-is-written.md).
{% endstep %}

{% step %}
### Type your own briefing

Select the text in the briefing field and replace it. The field takes up to 4,000 characters, the same cap the written-for-you briefing obeys.

A **Reset to the written-for-you version** button appears directly under the briefing field, above the rules chips, as soon as the text is your own. That button is how you can tell the briefing is no longer being written for you.
{% endstep %}

{% step %}
### Create the experience

Select **Create experience**.

The characters receive the words in the field, on top of their own personas—your wording, whichever room type you picked and however many characters you seat. Nothing is added to them and nothing is rewritten.

Once characters have joined the room, the thread shows what you wrote under **What each character was told on joining**, or under **What ⟨character name⟩ was told on joining** in a room holding one character.
{% endstep %}
{% endstepper %}

## Put the written-for-you briefing back

Select **Reset to the written-for-you version**, directly under the briefing field.

The button is present only while the text in the field is your own, and it disappears once the briefing has been reset. After a reset, the box follows the room type and the purpose again: edit either field and the briefing in the box is rewritten to match.

## What an emptied briefing does

An empty field is not a briefing, and the dialog refuses to create the experience while it stays empty.

Clearing the field shows this line under it: "A blank briefing sends the written-for-you one instead. Write what the characters should be told, or reset to it." The box stays open while it is empty, and **Create experience** is unavailable until you write something or reset. See [Briefs and transcripts](../troubleshooting/briefs-and-transcripts.md) for the other things that hold **Create experience** back.

## What your wording replaces, and what it does not

Your wording replaces the entire briefing, including the purpose that would otherwise sit in the middle of it. The characters are told your words and nothing else.

The purpose you wrote is still stored on the experience. It is shown on the experience's card or row, in the room's side panel, and on the pinned **Room brief** card, and it is matched by the search box on **My Experiences**. It is no longer part of what the characters are told, unless you put it there yourself. See [The room brief](README.md) for everywhere the brief appears.

Your wording changes the briefing and nothing else in the dialog:

| Element | Behavior after you rewrite the briefing |
|---|---|
| The rules chips | They keep describing the room type. See [Room types reference](room-types-reference.md). |
| The **Room type** menu | Picking a different type keeps your wording in the field and swaps the chips. It may also replace the filled-in name and purpose, unless you typed your own into either field. |
| The **Purpose** field | It stays editable, but editing it no longer rewrites your briefing. |

## Next steps

The briefing, the purpose, and the room type are settled the moment the experience is created. What is left is to seat the characters that receive the briefing.

{% content-ref url="../add-characters-to-the-room.md" %}
[Add characters to the room](../add-characters-to-the-room.md)
{% endcontent-ref %}

{% content-ref url="why-the-brief-cannot-be-changed.md" %}
[Why the brief cannot be changed](why-the-brief-cannot-be-changed.md)
{% endcontent-ref %}

{% content-ref url="how-the-room-brief-is-written.md" %}
[How the room brief is written](how-the-room-brief-is-written.md)
{% endcontent-ref %}
