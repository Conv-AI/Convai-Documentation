---
title: Conversation availability reference
description: Reference for the conversation availability states, events, and methods used to gate player input in the Convai Unity SDK.
last_reviewed: "5.0.0-preview"
---

Every public member involved in checking whether a character can hear the player, in lifecycle and call order.

The enum and its extension methods are in `Convai.Domain.DomainEvents.Session`. `CanAcceptPlayerInput()` describes readiness only; group rooms refuse typed text and require correlated push-to-talk.

## `ConvaiConversationAvailability` enum

| Value | Meaning |
| --- | --- |
| `NoCharacter` | No character is being addressed, or it is not set up yet. |
| `Offline` | There is no room. Nothing is listening. |
| `Connecting` | The room is being established. |
| `Preparing` | The room is connected, but this character has not been confirmed by the service yet. The shipped input gate blocks messages until readiness. |
| `Ready` | The character can hear the player. |
| `Answering` | The character is answering. Input is still accepted — that is barge-in. |
| `Unavailable` | The character failed to start, left the room, or the session is in `Error`. Unlike `Connecting` and `Preparing`, this does not resolve on its own. |

Values are listed in lifecycle order. Use `CanAcceptPlayerInput()` instead of relying on enum ordering or numeric ranges.

## `ConvaiConversationAvailabilityExtensions`

| Member | Returns | Description |
| --- | --- | --- |
| `CanAcceptPlayerInput()` | `bool` | The availability gate only: true for `Ready` and `Answering`. Input-mode restrictions still apply. |
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
| `CanAcceptPlayerInput` | `bool` | The character availability gate, equivalent to `ConversationAvailability.CanAcceptPlayerInput()`. It does not guarantee delivery or override input-mode restrictions. |
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
| `CanAcceptPlayerInput` | `bool` | Whether the availability state accepts input; input-mode restrictions remain separate. |

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

## `ConvaiPushToTalkController`

The component is under **Convai > Convai Push To Talk Controller** in Add Component. `Press()`, `Release()`, and `SetPressed(bool)` return whether the requested transition was accepted; inspect `BlockedReason` on refusal. `State`, `StateChanged`, `CommitCompleted`, and `RetryAsync` expose the correlated capture/commit lifecycle. Availability is only one gate: pending capture, microphone policy, speech holds, and group compatibility also apply.

See [Push-to-talk API](../../scripting-reference/push-to-talk-api.md) and [Push-to-talk lifecycle](../../core-concepts/push-to-talk-lifecycle.md) for complete signatures and lifecycle handling.

## Related

{% content-ref url="how-availability-works.md" %}
[How conversation availability works](how-availability-works.md)
{% endcontent-ref %}

{% content-ref url="gate-your-ui.md" %}
[Gate your UI on availability](gate-your-ui.md)
{% endcontent-ref %}
