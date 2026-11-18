---
title: Conversation targeting reference
description: Reference for every field, default, and event that controls how the Convai Unity SDK chooses which character the player is addressing.
last_reviewed: "5.0.0-pre.1"
---

Reference for the public types and `ConvaiManager` members that drive conversation targeting, including every field, default, and event.

## `ConversationTargetingMode`

| Value | Number | Description |
|---|---|---|
| `LookAt` | `0` (default) | The character nearest the centre of the player's view, scored by angle with distance as a tiebreak. Reads the view direction rather than casting a ray, so it needs no colliders, no layers, and no input wiring. |
| `Proximity` | `1` | The character nearest the view transform, regardless of view direction. |
| `Manual` | `2` | Scripted changes select the target. A missing or failed membership can recover to the first ready member; an explicit clear stays clear. |

## `ConversationTargetingOptions`

Exposed as `ConvaiManager.ConversationTargeting`. Never `null`. Every field has a working default; a scene that changes none of them still targets correctly.

| Field | Type | Default | Valid range | Description |
|---|---|---|---|---|
| `Mode` | `ConversationTargetingMode` | `LookAt` | — | How the character the player is talking to is chosen. |
| `MaxDistance` | `float` | `30` | `≥ 0` | How far away a character can be, in metres, and still be eligible to be addressed. |
| `MaxAngle` | `float` | `35` | `1`–`180` | Under `LookAt` only, how far from the center of view a character can be, in degrees, and still be eligible. Measured from the view direction, so the default gives a 70-degree cone. |
| `SwitchMargin` | `float` | `10` | `0`–`90` | How much better a different character must score, in degrees, before the conversation moves to them. Applies to `LookAt` only. |
| `SwitchDelaySeconds` | `float` | `0.2` | `≥ 0` | How long a different character must stay the best choice before the conversation moves to them. Applies to both automatic modes and custom providers. |
| `ProximityMargin` | `float` | `0.15` | `0` to `0.9` | Fraction by which a challenger must be nearer under `Proximity`. |

Inspector labels are **Chosen By**, **Range (Metres)**, **Look Angle (Degrees)**, **Switch Margin (Degrees)**, **Proximity Margin (Fraction)**, and **Switch Delay (Seconds)**. The angle fields appear only in **Look At**; the fractional margin appears only in **Proximity**. **Player Camera** is a serialized camera reference on the manager, with the `MainCamera`-tagged camera, first eligible enabled Game camera, then `ConvaiPlayer` as fallbacks. **Manual** shows only **Chosen By**.

Out-of-range values assigned to `MaxAngle`, `SwitchMargin`, `ProximityMargin`, `MaxDistance`, or `SwitchDelaySeconds` are clamped to their valid range rather than throwing.

### `ConversationTargetingOptions` members

| Member | Signature | Description |
|---|---|---|
| `Validate()` | `void Validate()` | Clamps every field into its supported range. |
| `CreateDefault()` | `static ConversationTargetingOptions CreateDefault()` | Returns a new instance with the shipped defaults. |

## `IConversationTargetProvider`

Replaces the built-in modes outright when registered. See [Write a custom targeting rule](custom-targeting-rule.md).

| Member | Signature | Description |
|---|---|---|
| `ResolveTarget` | `ConvaiCharacter ResolveTarget(IReadOnlyList<ConvaiCharacter> candidates, ConvaiCharacter current)` | Returns the character the player should be addressing, `null` or a character outside `candidates` for no proposal. A valid current target remains selected; lost-target recovery can still apply. `candidates` lists every ready, active, enabled character in the current room, in stable order, and is never null or empty when called. `current` is the character currently holding the conversation, or `null` when none does. |

## `ConversationTargetSwitchVerdict`

Returned by `ConvaiManager.ConversationTargetingStatus`. Names the reason the last targeting decision went the way it did.

| Value | Description |
|---|---|
| `AlreadyActive` | The proposed target matches the character already holding the conversation. |
| `Commit` | The policy permits requesting the change. Submission and confirmation are separate. |
| `HeldForDelay` | Held: the proposal has not been the best choice for long enough yet. |
| `HeldForPlayerSpeech` | Held: the player is part-way through saying something. |
| `HeldForPendingCommand` | Held: a previous change is still in flight. |
| `HeldForAnotherPlayer` | The local proposal has not changed since another player moved the route. |
| `HeldForGroupConversation` | An active group conversation keeps the current target while it can hear. |
| `HeldForScriptedTarget` | The proposal has not changed since a confirmed scripted move or clear. |

## `ConvaiManager` targeting members

| Member | Signature | Description |
|---|---|---|
| `ConversationTargeting` | `ConversationTargetingOptions ConversationTargeting { get; }` | Tuning for automatic conversation targeting. Never `null`. |
| `ConversationTarget` | `ConvaiCharacter ConversationTarget { get; }` | The character the player is currently addressing, or `null` when the room holds no multi-character session. |
| `ConversationTargetingStatus` | `ConversationTargetSwitchVerdict ConversationTargetingStatus { get; }` | The outcome of the most recent targeting evaluation. |
| `InitialCharacter` | `ConvaiCharacter InitialCharacter { get; }` | The explicitly assigned opening character, or `null` when the SDK resolves the opening character at connect time. |
| `TalkTo` | `void TalkTo(ConvaiCharacter character)` | Points the conversation at one character. Reports a Failed phase for an invalid request. |
| `TalkToAsync` | `IConvaiOperation<InteractionTargetResult> TalkToAsync(ConvaiCharacter character)` | Completes on confirmation and faults on failure. |
| `ClearConversationTargetAsync` | `IConvaiOperation<InteractionTargetResult> ClearConversationTargetAsync()` | Requests an empty route and completes on confirmation. |
| `AddressedCharacter` | `ConvaiCharacter AddressedCharacter { get; }` | UI target, including a pending move, a pre-connect proposal, or a looked-at character whose roster membership is still starting. |
| `SetInitialCharacter` | `void SetInitialCharacter(ConvaiCharacter character)` | Chooses which character speaks first when the room connects. Calling it on a connected room queues a reconnect rather than moving the current conversation. |
| `SetConversationTargetProvider` | `void SetConversationTargetProvider(IConversationTargetProvider provider)` | Replaces the SDK's targeting rule. Pass `null` to restore the behavior configured by `ConversationTargeting`. |

## Events

`ConvaiManager.Events.OnConversationTargetChanged` is an `Action<ConversationTargetChanged>`. The event in `Convai.Domain.DomainEvents.Runtime` carries `Phase`, `CharacterId`, `CharacterName`, `MembershipId`, `Reason`, and `Timestamp`.

| Phase | When it is raised |
|---|---|
| `Requested` | The SDK has claimed the routing window and is about to send a target change. Player input is paused. |
| `Confirmed` | The SDK has reconciled the authoritative route. This can also occur after a remote route change or roster handover. Identity fields can be empty when the route is clear or no local character is bound. |
| `Failed` | A requested change was unsuccessful. `Reason` describes the failure. If the refusal also reconciles a newer route, the SDK publishes that route as `Confirmed` first. |

An invalid request or a deferred request superseded before sending can fail without a `Requested` phase. Use the operation returned by `TalkToAsync` or `ClearConversationTargetAsync` to track your specific request.

## Errors and constraints

| Condition | Result |
|---|---|
| `TalkTo` called with a character not in the current room | The call is refused; the Console logs a warning naming the character. |
| `TalkTo` called while the player is mid-utterance | The request is held until the utterance ends, then sent. |
| A registered `IConversationTargetProvider.ResolveTarget` throws | An Error is logged and no proposal is produced; lost-target recovery can still apply. |
| The SDK cannot resolve a view camera or player transform | Automatic/provider targeting warns that there is no camera or player to measure from. |
| `TalkToAsync(null)` | The operation faults with `ArgumentNullException`; the Failed phase is reported. |
| A room holds only one character | Targeting logic never runs — the single character holds the conversation. |

## Related reference

{% content-ref url="how-conversation-targeting-works.md" %}
[How conversation targeting works](how-conversation-targeting-works.md)
{% endcontent-ref %}

{% content-ref url="../../scripting-reference/convaimanager-api.md" %}
[ConvaiManager API](../../scripting-reference/convaimanager-api.md)
{% endcontent-ref %}
