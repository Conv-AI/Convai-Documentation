---
title: Conversation targeting reference
description: Reference for every field, default, and event that controls how the Convai Unity SDK chooses which character the player is addressing.
last_reviewed: "4.6.0"
---

Reference for the public types and `ConvaiManager` members that drive conversation targeting, including every field, default, and event.

## `ConversationTargetingMode`

| Value | Number | Description |
|---|---|---|
| `LookAt` | `0` (default) | The character nearest the centre of the player's view, scored by angle with distance as a tiebreak. Reads the view direction rather than casting a ray, so it needs no colliders, no layers, and no input wiring. |
| `Proximity` | `1` | The nearest character, regardless of where the player is looking. |
| `Manual` | `2` | Nothing changes the target except the game, through `ConvaiManager.TalkTo`. |

## `ConversationTargetingOptions`

Exposed as `ConvaiManager.ConversationTargeting`. Never `null`. Every field has a working default; a scene that changes none of them still targets correctly.

| Field | Type | Default | Valid range | Description |
|---|---|---|---|---|
| `Mode` | `ConversationTargetingMode` | `LookAt` | — | How the character the player is talking to is chosen. |
| `MaxDistance` | `float` | `30` | `≥ 0` | How far away a character can be, in metres, and still be eligible to be addressed. |
| `MaxAngle` | `float` | `35` | `1`–`180` | How far from the centre of view a character can be, in degrees, and still be eligible. Measured from the view direction, so the default gives a 70-degree cone. |
| `SwitchMargin` | `float` | `10` | `0`–`90` | How much better a different character must score, in degrees, before the conversation moves to them. Applies to `LookAt` only. |
| `SwitchDelaySeconds` | `float` | `0.2` | `≥ 0` | How long a different character must stay the best choice before the conversation moves to them. Under `Proximity`, this is what separates two equidistant characters, since `SwitchMargin` has no meaning for a rule measured in metres. |

Out-of-range values assigned to `MaxAngle`, `SwitchMargin`, `MaxDistance`, or `SwitchDelaySeconds` are clamped to their valid range rather than throwing.

### `ConversationTargetingOptions` members

| Member | Signature | Description |
|---|---|---|
| `Validate()` | `void Validate()` | Clamps every field into its supported range. |
| `CreateDefault()` | `static ConversationTargetingOptions CreateDefault()` | Returns a new instance with the shipped defaults. |

## `IConversationTargetProvider`

Replaces the built-in modes outright when registered. See [Write a custom targeting rule](custom-targeting-rule.md).

| Member | Signature | Description |
|---|---|---|
| `ResolveTarget` | `ConvaiCharacter ResolveTarget(IReadOnlyList<ConvaiCharacter> candidates, ConvaiCharacter current)` | Returns the character the player should be addressing, `null` to leave the conversation where it is, or a character not in `candidates` — which also leaves the conversation where it is. `candidates` lists every character in the current room, in stable order, and is never null or empty when called. `current` is the character currently holding the conversation, or `null` when none does. |

## `ConversationTargetSwitchVerdict`

Returned by `ConvaiManager.ConversationTargetingStatus`. Names the reason the last targeting decision went the way it did.

| Value | Description |
|---|---|
| `AlreadyActive` | The proposed target matches the character already holding the conversation. |
| `Commit` | The change is allowed and has been sent. |
| `HeldForDelay` | Held: the proposal has not been the best choice for long enough yet. |
| `HeldForPlayerSpeech` | Held: the player is part-way through saying something. |
| `HeldForPendingCommand` | Held: a previous change is still in flight. |

## `ConvaiManager` targeting members

| Member | Signature | Description |
|---|---|---|
| `ConversationTargeting` | `ConversationTargetingOptions ConversationTargeting { get; }` | Tuning for automatic conversation targeting. Never `null`. |
| `ConversationTarget` | `ConvaiCharacter ConversationTarget { get; }` | The character the player is currently addressing, or `null` when the room holds no multi-character session. |
| `ConversationTargetingStatus` | `ConversationTargetSwitchVerdict ConversationTargetingStatus { get; }` | The outcome of the most recent targeting evaluation. |
| `InitialCharacter` | `ConvaiCharacter InitialCharacter { get; }` | The character the room opens on, or `null` when nothing has been chosen. The read half of `SetInitialCharacter`. |
| `TalkTo` | `void TalkTo(ConvaiCharacter character)` | Points the conversation at one character. Safe to call at any time; does nothing when the room is not multi-character or the character is not in it. |
| `SetInitialCharacter` | `void SetInitialCharacter(ConvaiCharacter character)` | Chooses which character speaks first when the room connects. Calling it on a connected room queues a reconnect rather than moving the current conversation. |
| `SetConversationTargetProvider` | `void SetConversationTargetProvider(IConversationTargetProvider provider)` | Replaces the SDK's targeting rule. Pass `null` to restore the behavior configured by `ConversationTargeting`. |

## Events

| Event | Signature | Raised when |
|---|---|---|
| `ConversationTargetRequested` | `event Action<ConvaiCharacter> ConversationTargetRequested` | After the SDK closes player input and immediately before it attempts to send the target change. The send can still fail. |
| `ConversationTargetChanged` | `event Action<ConvaiCharacter> ConversationTargetChanged` | When an authoritative response from Convai reconciles the target — a round trip after `ConversationTargetRequested`. The argument can be `null` when the authoritative response clears the route. |

These two `ConvaiManager` events are the shortest path to a single reaction to a target move. A project that has standardized on the domain event hub instead reaches for `ConvaiEvents.OnConversationTargetChanged` — `Action<ConversationTargetChanged>` — which carries the phase (`Requested`, `Confirmed`, `Failed`) and, on `Failed`, the reason the move was refused. See [Event system](../../core-concepts/event-system.md) for the full field reference and a subscription example.

## Errors and constraints

| Condition | Result |
|---|---|
| `TalkTo` called with a character not in the current room | The call is refused; the Console logs a warning naming the character. |
| `TalkTo` called while the player is mid-utterance | The request is held until the utterance ends, then sent. |
| A registered `IConversationTargetProvider.ResolveTarget` throws | The exception is caught and logged; the conversation stays where it is. |
| A room holds only one character | Targeting logic never runs — the single character holds the conversation. |

## Related reference

{% content-ref url="how-conversation-targeting-works.md" %}
[How conversation targeting works](how-conversation-targeting-works.md)
{% endcontent-ref %}

{% content-ref url="../../scripting-reference/convaimanager-api.md" %}
[ConvaiManager API](../../scripting-reference/convaimanager-api.md)
{% endcontent-ref %}
