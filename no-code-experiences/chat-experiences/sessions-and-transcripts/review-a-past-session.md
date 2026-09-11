---
title: Review a past session
description: Open a chat experience's previous sessions, pick one of its finished conversations, and read the whole thread, including what a saved transcript leaves out.
last_reviewed: "2026-09-10"
---

A finished conversation stays with the chat experience that ran it and can be opened again as a read-only thread. Use this page to reach an experience's previous sessions, pick one, and read it.

## Prerequisites

- A chat experience with at least one recorded session. See [Send your first message](../send-your-first-message.md) for how to record one, and [Sessions and transcripts](README.md) for what a session is.

## Open an experience's previous sessions

Two routes reach the same place, the experience's own page, which lists every session it recorded:

| From | What to select |
|---|---|
| [**My Experiences**](../open-my-experiences.md) | The three-dots menu on the experience's card or row, then **Previous sessions**. The session count opens the same page: a card reads `3 sessions · last Mar 4` or `No sessions yet`, and a row stacks `3 sessions` over `last Mar 4` |
| An open room | **Previous sessions** in the top bar, then **Open experience page** at the foot of the menu |

The menu behind **Previous sessions** in a room lists the same sessions, so a conversation can be opened straight from it. The row marked `· you are here` is the room you are in; selecting it closes the menu and leaves you where you are.

## What the experience's page shows

The page lists every session the experience recorded, newest first, beside the brief they all share.

The experience's name heads the page with its [room type](../the-room-brief/room-types-reference.md) and [room ID](../running-the-room/room-controls-reference.md#the-room-id) beside it, and a line under it reading the number of recorded sessions and the date the experience was created. A link back to **My Experiences** sits above the name. **Start new session** opens a new room from this experience; nothing on this page resumes an old one.

The list sits under **Previous sessions**, with the reminder "Each session is its own thread. The brief carries over; the characters and the messages do not." Each row carries these:

| What the row shows | What it means |
|---|---|
| `Session 4` | Its place in the experience's list, counted from the first session recorded |
| The first question you asked | The opening line of that conversation. A session that recorded nothing reads `No messages recorded` here instead |
| `Sat Sep 6 · 16:57–17:05` | The day the session ran, and the span from the moment it opened to its last reply. A session that drew no reply shows the opening time alone, and one that ran past midnight names both days |
| `12 messages` | Your messages plus the replies that carried text |
| **Open** | Opens the session as a read-only thread |
| The three-dots menu on the row | Holds **Export transcript**. See [Export a transcript](export-a-transcript.md) |

If the experience ran rooms before it began recording sessions, a line above the list gives the total it counts and how many of those came earlier. An experience with nothing recorded shows a panel in place of the list: "No sessions recorded yet. Rooms opened before this experience began recording sessions are not listed; the next one will appear here."

The brief panel beside the session list holds [**Room brief**](../the-room-brief/README.md): the room type, the purpose, the room type's rules, and the **Fixed at creation** label. The written briefing itself is not repeated here. There is no roster on this page, because characters are picked for each session and no single cast belongs to the experience.

## Read a finished session

Selecting **Open** on a row shows that session as a read-only thread.

The header names the experience, its room type, and the session itself—`Session 4 · Sat Sep 6 · 16:57–17:05 · 12 messages`. The back chevron in the header returns to the list, and **Export transcript** is the other control it carries.

Under the header the conversation reads as it did at the time. Your own messages sit to the right with a caption under each one, replies sit to the left under the character that sent them, and a note names any character that stayed quiet on a turn.

Two things the live room has are absent, because a finished session has no use for them: there is no side panel and no message box. Each reply carries the character's name alone. The role that sits beside a name in a live room, and the workspace shown under the name in the side panel, are not part of a transcript.

{% hint style="warning" %}
A session page holds the first 200 turns. A longer one opens with a note at the top of the thread: "Showing the first 200 turns of ⟨total⟩. The rest are not on this page or in the export." Its message count on the row and in the header then ends in a plus sign, such as `412+ messages`, because that count is a floor taken from the turns on the page rather than the session's own total.
{% endhint %}

If a session will not open, or nothing is listed where you expected a session, see [Briefs and transcripts](../troubleshooting/briefs-and-transcripts.md).

## What a transcript does not record

A transcript records what was said, not every detail the room showed while it was being said. Three differences are worth knowing before you read one.

**Auto and Anyone may respond read back the same.** A turn sent under either one carries the caption `Auto · room brief decides`. Read that caption as a description of who answered rather than as a record of the setting you chose. Every other mode is kept, so an **Everyone must respond** turn still reads `Everyone must respond` and a tagged turn still names who was tagged. A turn addressed to one character reads `Only ⟨name⟩` whichever way you addressed it, where a live room writes `Sent to ⟨name⟩` for a character picked under **Only one character**. See [Respond modes reference](../running-the-room/respond-modes-reference.md).

**The quiet note is shorter.** A transcript names a character that said nothing and stops there. A live room says more, and how much more depends on the mode the turn ran under:

| Where | What the note reads |
|---|---|
| A live room on **Auto** | "⟨names⟩ stayed quiet, as the brief asks. Tag them if you want their side." The last sentence reads "Tag one of them if you want their side." when more than one character is named |
| A live room on **Anyone may respond** | "⟨names⟩ had nothing to add and passed." |
| A live room on **Everyone must respond**, **Only the characters I tag**, or **Only one character** | "⟨names⟩ passed" |
| A transcript, whatever the mode | "⟨names⟩ stayed quiet." |

**A caption carries one count.** In a live room a caption can carry up to three: the replies, the characters still listening, and the characters that did not answer. A transcript caption carries the reply count alone, such as `2 of 4 responded`. See [How a turn works](../running-the-room/how-a-turn-works.md).

## Next steps

{% content-ref url="export-a-transcript.md" %}
[Export a transcript](export-a-transcript.md)
{% endcontent-ref %}

{% content-ref url="../manage-your-chat-experiences.md" %}
[Manage your chat experiences](../manage-your-chat-experiences.md)
{% endcontent-ref %}
