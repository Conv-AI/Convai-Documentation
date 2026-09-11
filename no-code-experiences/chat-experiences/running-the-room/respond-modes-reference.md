---
title: Respond modes reference
description: Reference for the five respond modes in a chat experience room, what each one asks of the characters, and what the thread shows afterwards.
last_reviewed: "2026-09-10"
---

A respond mode decides who is expected to answer the next message. Five are available in a room of two or more characters, and a room opens on **Auto**, where the [room brief](../the-room-brief/README.md) decides who answers.

Two controls set the mode. The respond chip sits to the left of the message box, under what you are typing, and holds until you change it; an `@` tag written into the message applies to that one message. See [Choose who replies](choose-who-replies.md) for setting either. A room holding one character has no chip and no mode to set: the message box carries a sentence in place of the chip, and every message goes to the character in the room.

## The five respond modes

The menu describes each mode in one line:

| Mode | What the menu says |
|---|---|
| **Auto · room brief decides** | "The default. Characters answer when the room brief says it is their turn, and stay quiet otherwise." |
| **Everyone must respond** | "All ⟨number in the room⟩ characters reply in turn. Use for polls, comparisons and reviews." |
| **Anyone may respond** | "An open question. Characters answer only if they have something relevant; others pass." |
| **Only the characters I tag** | "Type @Name in the message. Every tagged character must reply; untagged ones stay silent." |
| **Only one character** | "Pick who answers. Same as tagging a single name." |

**Everyone must respond** is the one description that changes. It names the number of characters in the room at the moment you open the menu, so it reads "All 3 characters…" in a room of three and "All 6 characters…" after you seat three more.

## Where each mode sits in the menu

The menu opens under a section label asking who should respond, and lists the modes in this order:

| Position | Mode | Where it sits |
|---|---|---|
| 1 | **Auto · room brief decides** | The mode a room opens on |
| 2 | **Everyone must respond** | |
| 3 | **Anyone may respond** | |
| 4 | **Only the characters I tag** | Below a divider, and marked **set by tags** |
| 5 | **Only one character** | In a panel at the foot of the menu, holding a chip for every character in the room |

The mode in force carries a check mark.

## What the chip shows

The chip always shows what will happen to the message you are writing, so a tag typed into the message changes it:

| In force | Chip label |
|---|---|
| Auto | **Auto · room brief decides** |
| Everyone must respond, or `@everyone` in the message | **Everyone must respond** |
| Anyone may respond | **Anyone may respond** |
| One character tagged, or one picked under **Only one character** | **Only** followed by the name |
| Two or more characters tagged | **Tagged:** followed by the names |

A name in the chip is written the way the tag list offers it, so two characters sharing a name read as the name and the name with `(2)` after it.

**Only the characters I tag** has no chip label of its own. Until a name is tagged, the message behaves as **Auto** and the chip says so.

## What the thread shows after the turn

These are the captions a live room shows; a saved transcript captions the same turns in its own words, and [Review a past session](../sessions-and-transcripts/review-a-past-session.md) carries that wording. The caption under your message names the mode and reports the outcome, and some modes also put a short label beside each reply:

| Mode | Caption | Label beside each reply |
|---|---|---|
| Auto | `Auto · room brief decides` followed by `⟨k⟩ of ⟨n⟩ responded`, then `⟨j⟩ listening` and `⟨f⟩ did not answer` when either applies | `Relevant · answered` |
| Everyone must respond | `Everyone must respond · ⟨k⟩ of ⟨n⟩ replied` | None |
| Anyone may respond | `Anyone may respond` followed by who replied, or `nobody replied yet`, and `⟨p⟩ passed` when any did | `Volunteered` |
| Only the characters I tag, two or more tagged | `Tagged: ⟨names⟩ · ⟨k⟩ of ⟨n⟩ replied` | None |
| Only the characters I tag, one tagged | `Only ⟨name⟩`, then `replied` or `waiting` | None |
| Only one character | `Sent to ⟨name⟩`, then `replied` or `waiting` | None |

Every placeholder counts something of its own. ⟨k⟩ is how many characters replied, and ⟨n⟩ is what the turn asked: the room as it stood when you sent the message under **Auto** and **Everyone must respond**, and the number of characters tagged on a tagged turn. ⟨j⟩, ⟨f⟩ and ⟨p⟩ are counts in their own right, not the room total: the characters still listening, the characters reported as not answering, and the characters that passed. See [How a turn works](how-a-turn-works.md) for what each count means.

A turn addressed to a single character carries no outcome word once it is over and nothing came back. The caption is the label alone: `Only ⟨name⟩`, or `Sent to ⟨name⟩`.

Those two labels are the difference between the two ways of addressing one character. The chip reads **Only** followed by the name either way, and the caption records the route the turn took: `Only ⟨name⟩` when the name was tagged in the message, `Sent to ⟨name⟩` when it was picked under **Only one character**.

A room holding one character has a caption of its own, whatever the mode is set to. It names the character rather than the mode: `Sent to ⟨name⟩ · replied` once the character has answered, `Sent to ⟨name⟩ · waiting` while the room is still answering, and `Sent to ⟨name⟩` alone when the turn is over and no reply came.

A turn that tagged two or more characters adds a line under the replies naming everyone in the room left out of it: "Kai and Theo weren't tagged and won't reply to this one." With one character left out, the line reads "wasn't tagged".

## What a quiet character produces

In a live room, two modes let a character answer nothing, and each words the result differently:

| Mode | Note under the replies |
|---|---|
| Auto | "⟨names⟩ stayed quiet, as the brief asks. Tag them if you want their side." With more than one name, the last sentence reads "Tag one of them if you want their side." |
| Anyone may respond | "⟨names⟩ had nothing to add and passed." |

**Everyone must respond**, **Only the characters I tag**, and **Only one character** each ask every character the turn addresses to reply. A character that answers nothing under one of those three is named in a shorter note: "⟨names⟩ passed".

A transcript notes a quiet character in one wording whatever the mode the turn ran under. See [Review a past session](../sessions-and-transcripts/review-a-past-session.md).

## Related pages

{% content-ref url="choose-who-replies.md" %}
[Choose who replies](choose-who-replies.md)
{% endcontent-ref %}

{% content-ref url="how-a-turn-works.md" %}
[How a turn works](how-a-turn-works.md)
{% endcontent-ref %}
