---
title: Choose who replies
description: Set who answers the next message in a chat experience room, tag individual characters, and address the whole room at once.
last_reviewed: "2026-09-10"
---

A chat experience room of two or more characters opens on **Auto · room brief decides**, where the [room brief](../the-room-brief/README.md) settles who answers. Two controls override it: the respond chip under the message box, which holds until you change it, and an `@` tag in the message, which applies to that message only. Use this page to set either one, to know which of them wins, and to see what a room holding a single character offers instead.

## Prerequisites

- A chat experience room with at least one character in it. See [Add characters to the room](../add-characters-to-the-room.md).
- The message box unlocked. The respond chip is disabled whenever the message box is. See [You cannot send a message](../troubleshooting/composer-is-locked.md).

## Set who answers with the respond chip

In a room of two or more characters, the respond chip sits in the row under the message box, to the right of the paperclip that attaches files. It shows who the next message will go to, and selecting it opens the respond menu.

{% stepper %}
{% step %}
### Open the respond menu

Select the chip. The menu opens under a section label asking who should respond.

Four modes are listed: **Auto · room brief decides**, **Everyone must respond**, **Anyone may respond**, and, below a divider, **Only the characters I tag**. A fifth, **Only one character**, sits at the foot of the menu with a chip for each character in the room.
{% endstep %}

{% step %}
### Pick a mode

Select the mode you want. Each carries a line describing what it asks of the characters, and the mode in force carries a check mark.

Selecting **Auto · room brief decides**, **Everyone must respond**, or **Anyone may respond** closes the menu and sets the chip. Selecting a character under **Only one character** sets the chip to **Only** followed by that name. Selecting **Only the characters I tag** closes the menu and types an `@` into the message box for you, which opens the tag list.
{% endstep %}
{% endstepper %}

The setting stays until you change it. It applies to every message you send from then on, not to one message.

For what each mode asks of the characters and what the thread shows afterwards, see [Respond modes reference](respond-modes-reference.md).

## Tag a character in the message

Tagging names a character inside the message itself, and it asks that character for a reply rather than leaving the choice to it.

{% stepper %}
{% step %}
### Type an @

Type `@` at the start of the message or after a space. The tag list opens above the box, holding the characters in the room.

Each row carries the character's name, its role, and its workspace. A character you have already tagged in this message is marked **already tagged**.
{% endstep %}

{% step %}
### Narrow the list

Keep typing the name without its spaces—Mira Song is tagged as `@MiraSong`—and the list keeps the characters whose name starts with what you have typed. Case does not matter, and typing a space ends the tag and closes the list.

Two characters sharing a name are offered as the name and the name with `(2)` after it, and the two resolve to different characters.
{% endstep %}

{% step %}
### Insert the tag

Press `Enter` or `Tab` to insert the character the list has highlighted, or select its row. The arrow keys move the highlight, and `Escape` closes the list without tagging.

The tag is written into the message as `@` followed by that name without its spaces, and it is highlighted in the box. Tag as many characters as you want in one message.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
Naming a character in ordinary prose—"Maya, what did you think of the price?"—may draw that character out under Auto, but nothing holds it to a reply. A tag is the explicit form: it asks the character outright, and the room holds it to that rather than leaving the decision to the character.
{% endhint %}

## Address every character at once

`@everyone` is the last option in the tag list, under a divider. It is offered only in a room of two or more characters, and only while what you have typed still matches `everyone`: type `@n` and it drops out of the list, the same narrowing the character rows follow. The row reads `@everyone` with the size of the room beside it—`all four must reply` in a room of four.

Selecting it addresses every character in the room. The chip changes to **Everyone must respond**, and each character is asked to reply in turn. A character that is asked to reply can still answer nothing, and the thread names it under the replies. See [Respond modes reference](respond-modes-reference.md).

## How a tag and the chip fit together

A tag in the message wins over the chip, for that message only.

The chip follows what you type, so it always reads what will happen to the message you are writing rather than what you last set. With no tags in the draft, the chip's own setting is what applies. [Respond modes reference](respond-modes-reference.md) lists every label the chip can carry.

Deleting the tags from the draft returns the chip to its own setting. Sending the message clears the draft, so the next message starts from the chip again.

{% hint style="success" %}
Read the chip before you send. If it names the mode you picked or the characters you tagged, the message is addressed the way you meant it. If it still reads **Auto · room brief decides**, nothing you have set or typed has taken effect.
{% endhint %}

## A one-character room has no respond chip

A room holding one character shows a sentence where the chip would be: "One character in the room: every message goes to ⟨name⟩." There is no menu and no mode to set, because every message reaches the only character there.

Typing `@` still opens the tag list with that one character in it, and `@everyone` is not offered. Tagging asks the character for a reply outright; left untagged, it answers when your message addresses it and stays quiet otherwise, which is what the briefing written for a single-character room tells it to do. See [How the room brief is written](../the-room-brief/how-the-room-brief-is-written.md).

Seat a second character and the chip appears.

## Next steps

{% content-ref url="respond-modes-reference.md" %}
[Respond modes reference](respond-modes-reference.md)
{% endcontent-ref %}

{% content-ref url="how-a-turn-works.md" %}
[How a turn works](how-a-turn-works.md)
{% endcontent-ref %}
