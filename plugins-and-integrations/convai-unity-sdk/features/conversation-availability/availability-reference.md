---
title: Conversation availability reference
description: Reference for the conversation availability states, events, and methods used to gate player input in the Convai Unity SDK.
last_reviewed: "4.6.0"
---

Every public member involved in checking whether a character can hear the player, in lifecycle and call order.

## `ConvaiConversationAvailability` enum

| Value | Meaning |
| --- | --- |
| `NoCharacter` | No character is being addressed, or it is not set up yet. |
| `Offline` | There is no room. Nothing is listening. |
| `Connecting` | The room is being established. |
| `Preparing` | The room is connected, but this character has not been confirmed by the service yet. Messages sent now are lost. |
| `Ready` | The character can hear the player. |
| `Answering` | The character is answering. Input is still accepted — that is barge-in. |
| `Unavailable` | The character failed to start, or left the room. Unlike `Connecting` and `Preparing`, this does not resolve on its own. |

Values are listed in lifecycle order. Do not compare them with `<` or `>` — the two states that accept input, `Ready` and `Answering`, are not adjacent.

## `ConvaiConversationAvailabilityExtensions`

| Member | Returns | Description |
| --- | --- | --- |
| `CanAcceptPlayerInput()` | `bool` | Whether a message sent now — typed or spoken — will reach the character. True for `Ready` and `Answering`. |
| `IsSettling()` | `bool` | Whether the state resolves on its own, given a moment. True for `Connecting` and `Preparing`. |

## `ConvaiManager` members

| Member | Type | Description |
| --- | --- | --- |
| `ConversationAvailability` | `ConvaiConversationAvailability` | Whether the player can talk to `AddressedCharacter` right now, and if not, what is in the way. |
| `ConversationAvailabilityChanged` | `event Action<ConvaiConversationAvailability>` | Raised when `ConversationAvailability` changes — including when the player starts addressing a different character whose availability may differ. |
| `AddressedCharacter` | `ConvaiCharacter` | The character the player is talking to, in either shape of room and before either exists. |

## `ConvaiCharacter` members

| Member | Type | Description |
| --- | --- | --- |
| `ConversationAvailability` | `ConvaiConversationAvailability` | Whether the player can talk to this character right now, and if not, what is in the way. |
| `CanAcceptPlayerInput` | `bool` | Whether a message sent to this character right now — typed or spoken — will reach it. Equivalent to `ConversationAvailability.CanAcceptPlayerInput()`. |
| `IsCharacterReady` | `bool` | Whether the character has received the bot-ready signal from Convai. Set only by that signal, not by room connection — distinct from `ConversationAvailability`, which also accounts for room state and roster membership. |

## `ConversationAvailabilityChanged` domain event

Published on the SDK's event hub, and exposed as a typed property on `ConvaiEvents.OnConversationAvailabilityChanged`.

| Member | Type | Description |
| --- | --- | --- |
| `Availability` | `ConvaiConversationAvailability` | The verdict now. |
| `PreviousAvailability` | `ConvaiConversationAvailability` | The verdict this replaced. |
| `CharacterId` | `string` | Convai Character ID of the character being addressed, when there is one. |
| `CharacterName` | `string` | Display name of that character, for logs and UI. |
| `Timestamp` | `DateTime` | When the verdict moved, in UTC. |
| `CanAcceptPlayerInput` | `bool` | Whether the player may send speech or text right now. |

## `LocalPlayerActivityChanged` domain event

Published on the SDK's event hub with no typed property on `ConvaiEvents` — subscribe through `ConvaiEvents.Raw`.

| Member | Type | Description |
| --- | --- | --- |
| `IsActive` | `bool` | Whether `Source` currently sees the player. |
| `Source` | `LocalPlayerActivitySource` | Which local evidence this event is reporting. |
| `Level` | `float` | How loud the microphone was, relative to the noise it had settled on, when the level gate raised this. Zero for `PushToTalk` and for the falling edge. |
| `Timestamp` | `DateTime` | When the local evidence changed, in UTC. |

### `LocalPlayerActivitySource` enum

| Value | Meaning |
| --- | --- |
| `Microphone` | The open microphone is hearing sound loud enough to be someone talking. |
| `PushToTalk` | The player is holding the push-to-talk control. |

The same event hub also publishes `RoomRosterChanged` — a character joining, leaving, or being refused in a connected room — exposed as `ConvaiEvents.OnRoomRosterChanged`. It is not an availability signal; see [Handle room events](../multi-character-sessions/handle-roster-events.md) for its fields and subscription pattern.

## `ConvaiPlayer` members

| Member | Signature | Description |
| --- | --- | --- |
| `SendTextMessage` | `void SendTextMessage(string message)` | Sends a text message to the addressed character. Logs a warning and does nothing when refused. |
| `TrySendTextMessage` | `bool TrySendTextMessage(string message, out string reason)` | Sends a text message and reports why it was refused. Returns `true` when the message was handed to the room. |

## Related

{% content-ref url="how-availability-works.md" %}
[How conversation availability works](how-availability-works.md)
{% endcontent-ref %}

{% content-ref url="gate-your-ui.md" %}
[Gate your UI on availability](gate-your-ui.md)
{% endcontent-ref %}
