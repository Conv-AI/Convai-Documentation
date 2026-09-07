---
title: How conversation availability works
description: Understand how the Convai Unity SDK decides whether a character can hear the player, and why a connected room is not enough.
last_reviewed: "4.6.0"
---

A room can report itself connected before the character the player is addressing has been announced by Convai. Conversation availability answers a narrower question than "is the room connected" — it asks "can this specific character hear the player right now" — and it is what every input surface in the SDK checks before it lets the player speak or type.

## Why connected is not the same as available

A room reporting connected says nothing about whether the character being addressed has been confirmed by the service yet. A greeting typed in that gap is accepted, sent, and lost — nothing logs it, and nothing tells the player why nobody answered. `ConvaiManager.ConversationAvailability` closes that gap. Bind input to it instead of to whether the room is connected.

## The states, in lifecycle order

`ConvaiManager.ConversationAvailability` returns a `ConvaiConversationAvailability` value:

| State | Meaning |
| --- | --- |
| `NoCharacter` | No character is being addressed, or the scene is not set up yet. |
| `Offline` | There is no room. Nothing is listening. |
| `Connecting` | The room is being established. |
| `Preparing` | The room is connected, but this character has not been confirmed by the service yet. A message sent now is lost. |
| `Ready` | The character can hear the player. |
| `Answering` | The character is answering. Input is still accepted — interrupting a character mid-answer is ordinary conversation, not a rejected message. |
| `Unavailable` | The character failed to start, or left the room. Unlike `Connecting` and `Preparing`, this does not resolve on its own. |

Do not compare these values with `<` or `>`. `Ready` and `Answering` are the two states that accept player input, and they are not adjacent in the list.

## Which question to ask

Two extension methods answer the questions a UI actually has:

- `CanAcceptPlayerInput()` — whether a message sent now, typed or spoken, reaches the character. True only for `Ready` and `Answering`.
- `IsSettling()` — whether the state resolves on its own without telling the player to do anything. True only for `Connecting` and `Preparing`.

## Who is being asked

`ConvaiManager.ConversationAvailability` answers for `ConvaiManager.AddressedCharacter` — whichever character the player is currently talking to, whether or not the room keeps a roster for several characters. The same answer is also available per character on `ConvaiCharacter.ConversationAvailability`.

`ConvaiCharacter.ConversationAvailability` sits next to `ConvaiCharacter.IsCharacterReady`, and the two are easily confused. `IsCharacterReady` is set once by the character-ready signal from Convai and does not clear on its own. `ConversationAvailability` also accounts for whether the room is connected, whether the character still holds a seat in a shared room's roster, and whether the character is currently speaking — so a character can report `IsCharacterReady == true` from an earlier connection while `ConversationAvailability` reports `Unavailable`, because it no longer has a seat in the current room.

## Moving through a target switch

`ConvaiManager.ConversationAvailabilityChanged` fires whenever the verdict moves — including when the player starts addressing a different character whose availability differs from the one they left. While a targeting switch is in flight, availability reports `Preparing` even for a character that was `Ready` a moment earlier, so input closes for the moment the conversation is actually moving between characters rather than accepting a message that lands on neither.

## Related concepts

{% content-ref url="gate-your-ui.md" %}
[Gate your UI on availability](gate-your-ui.md)
{% endcontent-ref %}

{% content-ref url="../multi-character-sessions/how-multi-character-sessions-work.md" %}
[How multi-character sessions work](../multi-character-sessions/how-multi-character-sessions-work.md)
{% endcontent-ref %}
