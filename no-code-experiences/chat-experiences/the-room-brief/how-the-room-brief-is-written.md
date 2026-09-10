---
title: How the room brief is written
description: Understand how a room type and a purpose become the one briefing every character receives, and what is trimmed when that briefing runs long.
last_reviewed: "2026-09-10"
---

The briefing a character receives is one paragraph, written from the room type and the purpose you set when you created the chat experience. A one-character room is briefed in different words from a room of two or more, and the two are labeled differently as well. Knowing how that paragraph is assembled tells you what the characters are working from, which wording they received, and what is shortened when the briefing grows too long. Chat Experiences is in beta.

## The three parts of a briefing

In a room of two or more characters, a briefing opens with a sentence from the room type, carries your purpose in the middle, and closes with the rules that room type sets. A one-character room is briefed in wording of its own, which the next section sets out.

Both of those are written for you. The **Create a chat experience** dialog is the one place where you can replace that wording with your own, and your own wording replaces the whole paragraph: no opening sentence, no closing rules, and no room-type wording at all. Everything on this page describes the briefing written for you. See [Create a chat experience](../create-a-chat-experience.md) and [Write your own briefing](write-your-own-briefing.md).

A **Focus group** experience left on its prefilled purpose produces these three parts:

| Part | Where it comes from | Wording |
|---|---|---|
| The opening sentence | The room type | "You are joining a focus group run by a moderator. You are one of several participants." |
| The purpose | What you wrote | "Taste-test debrief for the new spicy chicken sandwich. Five regular customers share honest reactions to the flavor, the price and the packaging." |
| The closing rules | The room type | "The moderator asks the questions. Answer when you are asked, and only when what you know is relevant. Discuss with other participants when the moderator invites it. Otherwise, listen. Stay in character and draw on your own background." |

The three parts arrive as one paragraph, not as three. Each room type supplies a different opening sentence and a different set of closing rules, so the same purpose produces a different briefing under a different type. See [Room types reference](room-types-reference.md) for what each type sets.

**Custom** differs from the five preset types in two ways. Its opening sentence, "You are joining a room with a purpose set by its creator:", ends in a colon, so your purpose reads as its continuation. It is also the only type that starts with an empty **Purpose** field.

A purpose that does not end in a period, a question mark, or an exclamation mark gets one added, so it reads as a sentence in the middle of the paragraph. That happens whichever room type you picked, and in a one-character room as well.

## What a one-character room receives

A one-character room is briefed as a conversation between two people rather than as a group:

| Part | Wording in a one-character room |
|---|---|
| The opening sentence | "You are joining a chat experience with a purpose set by its creator:" |
| The purpose | The purpose you wrote, as one sentence |
| The closing rules | "One other person is in the room. Stay in character, draw on your own background, and respond when addressed." |

The room type still decides the purpose you started from and the room type chip shown on the room, but the opening sentence and the closing rules above replace the room type's own. A room of two or more characters uses the room type's wording instead.

The **Create a chat experience** dialog previews the briefing for a room of two or more characters. Which of the two a character actually receives is settled when the room opens, from the number of characters seated at that moment.

## How the room labels the brief

The room labels the same brief differently depending on how many characters are in it. In the thread, the briefing box is titled **What ⟨name⟩ was told on joining** in a one-character room and **What each character was told on joining** in a room of two or more. The side panel changes with it: the section holding your own row is named differently, and so is the line under your name. See [Room controls reference](../running-the-room/room-controls-reference.md) for the side panel in full.

The labels differ, but they name the same room brief. What changes with the number of characters is the briefing wording set out above.

## The rules chips beside the briefing

The rules chips are the short form of the rules the briefing sets. They sit beside the briefing in the **Create a chat experience** dialog, in the thread, and on the experience's **Previous sessions** page. The room's side panel shows the brief without them.

In a room of two or more characters, the chips are the room type's own, and every type has its own set. Two of the six set no leader at all. See [Room types reference](room-types-reference.md) for the chips each type shows.

In a one-character room, the chips read **One other person**, **Stay in character**, and **Respond when addressed**, whichever room type the experience was created under.

## When the briefing runs long

A briefing is capped at 4,000 characters, and the purpose is the only part that is shortened to fit.

The opening sentence and the closing rules are kept whole. The purpose is cut at the point where the paragraph would run past the cap, ending in an ellipsis.

A briefing you write yourself obeys the same cap. The **What each character will be told** box in the **Create a chat experience** dialog stops accepting text at 4,000 characters, so the wording you can see in the box is the wording the characters receive. That same box holds the finished briefing while it is still being written for you, so you can read the whole paragraph, ellipsis and all, before you create the experience.

## Related pages

The purpose that sits in the middle of a briefing is written once, in the create dialog. That is also where the briefing can be replaced with your own wording, and after that nothing about the brief can be changed.

{% content-ref url="../create-a-chat-experience.md" %}
[Create a chat experience](../create-a-chat-experience.md)
{% endcontent-ref %}

{% content-ref url="write-your-own-briefing.md" %}
[Write your own briefing](write-your-own-briefing.md)
{% endcontent-ref %}

{% content-ref url="why-the-brief-cannot-be-changed.md" %}
[Why the brief cannot be changed](why-the-brief-cannot-be-changed.md)
{% endcontent-ref %}
