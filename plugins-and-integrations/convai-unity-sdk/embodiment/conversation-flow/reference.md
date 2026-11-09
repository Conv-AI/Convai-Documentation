---
title: Conversation flow reference
description: Full reference for the Conversation Flow controller's public API, the dialogue-state reading it returns, and every timing field on its profile asset.
last_reviewed: "5.0.0-preview"
---

Reference for the public conversation-flow surface: `ConvaiConversationFlowController`, the `DialogueStateReading` struct it returns, and every field on `ConvaiConversationFlowProfile`. For what each `DialogueState` value means, see [Dialogue state](../../core-concepts/dialogue-state.md). The cross-module contract `IConversationFlowSource` is internal and is not part of this surface — read the controller's own members instead.

***

## `ConvaiConversationFlowController`

`ConvaiConversationFlowController` (`sealed class : ConvaiCharacterModule<ConvaiConversationFlowProfile>`, `[AddComponentMenu("Convai/Embodiment/Conversation Flow")]`, `[DisallowMultipleComponent]`) is the character's single authored source of `DialogueState`. Convai adds it automatically when another module needs one — see [Conversation flow](README.md#convai-adds-it-automatically-when-needed).

### Properties

| Member | Type | Description |
| --- | --- | --- |
| `Current` | `DialogueStateReading` | The character's current dialogue-state reading. Returns `DialogueStateReading.Idle` before the controller has ticked for the first time. |

### Methods

| Method | Signature | Behavior |
|---|---|---|
| `PulseReaction` | `void PulseReaction(float durationSeconds = 0.6f)` | Requests a `Reacting` beat for a game event. Duration is capped at `1.5` seconds; nonpositive values do nothing. A new call restarts the beat rather than queueing. A character that is not ready remains `Idle` and drops the beat. |

### Events

| Event | Signature | Raised when |
| --- | --- | --- |
| `Changed` | `event Action<DialogueStateReading>` | The reading's `Primary` state changes. Not raised on blend progress alone. The event reading has `TimeInState` and `EnergyLevel` set to `0`; read `Current` after a tick for sampled time and energy. |

***

## `DialogueStateReading`

`DialogueStateReading` (`readonly struct`, `SDK/Domain/Embodiment/Readings/DialogueStateReading.cs`) is the immutable snapshot exposed by `Current` and passed to `Changed`. The struct can describe a blend between states, but the current controller publishes both `Primary` and `BlendTo` as the newly entered state. Do not rely on it to retain the previous state.

| Field | Type | Description |
| --- | --- | --- |
| `Primary` | `DialogueState` | The current authoritative state. |
| `BlendTo` | `DialogueState` | The state being blended toward. The current controller sets this equal to `Primary`, including during blend progress. |
| `BlendWeight` | `float` | Progress from `0` to `1` over `Transition Duration`. The current controller does not expose the preceding state through `Primary`. |
| `TimeInState` | `float` | Seconds the character has been in `Primary`, clamped to `0` or above. |
| `EnergyLevel` | `float` | Normalized energy in `[0, 1]` used by gesture schedulers and micro-behavior intensity — higher during `Speaking` and `Reacting`, lower during `Idle`. |
| `IsTransitioning` | `bool` | `true` only when `Primary` and `BlendTo` differ and `BlendWeight` is greater than `0`; therefore `false` for the current controller's readings. |

`DialogueStateReading.Idle` is a static property that returns the steady-state reading for a character in `Idle` — `Primary` and `BlendTo` both `Idle`, `BlendWeight` `0`, `TimeInState` `0`, `EnergyLevel` `0`.

***

## `ConvaiConversationFlowProfile`

`ConvaiConversationFlowProfile` (`sealed class : ScriptableObject`, `[CreateAssetMenu(menuName = "Convai/Embodiment/Conversation Flow Profile")]`, `SDK/Modules/ConversationFlow/Profiles/ConvaiConversationFlowProfile.cs`) authors the state machine's timing parameters. Assign it to the controller's **Flow Profile** field; with none assigned, the controller runs on the values below as built-in defaults.

### Transition

| Field | Range | Default | Description |
| --- | --- | --- | --- |
| Transition Duration | `0`–`2` | `0.25` | Duration in seconds of the linear crossfade between two states — the value read back as `BlendWeight` progress. |

### Dialogue Beats

| Field | Range | Default | Description |
| --- | --- | --- | --- |
| Thinking Min Hold | `0`–`3` | `0.25` | Minimum duration the character remains in `Thinking` after the player commits a turn. |
| Thinking Max Hold | `0.5`–`10` | `2.5` | Maximum duration the character remains in `Thinking` before falling back to `Attending`. |
| Attending Grace Period | `0`–`2` | `0.3` | Grace period after the player stops speaking without committing a turn, before the character moves on from `Attending`. |
| Settling Duration | `0`–`3` | `0.6` | Duration of the post-turn settle beat before the character returns to `Idle`. |
| Idle Return Delay | `0`–`120` | `60` | Seconds of inactivity before the character cools from `Attending` back to `Idle`. |
| Interrupted Freeze Duration | `0`–`2` | `0.25` | Duration the character freezes in `Interrupted` after being interrupted. |

{% hint style="info" %}
If **Thinking Min Hold** is set above **Thinking Max Hold** in the Inspector, the asset raises **Thinking Max Hold** to match **Thinking Min Hold** automatically, so the two values shown in the Inspector always agree with what the character does at runtime.
{% endhint %}

### Energy

| Field | Range | Default | Description |
| --- | --- | --- | --- |
| Speaking Base Energy | `0.1`–`1` | `0.6` | Base energy level emitted during `Speaking`, read by `EnergyLevel` and used to scale body language intensity. |

### Fixed behavior

Three profile fields — `noticeYouLocally`, `stopWhenTheVoiceStops`, and `voiceEndHold` — are private serialized fields omitted by the standard profile Inspector. They remain editable through Unity's Debug Inspector or editor code using `SerializedObject`. There are no public setters; `NoticeYouLocally` is a read-only getter. Their defaults are `true`, `true`, and `0.4` seconds, respectively:

- The character reacts the moment it has local evidence you have started talking, ahead of Convai's own confirmation that it heard you.
- With `stopWhenTheVoiceStops` enabled, local voice or lip-sync evidence can end the speaking performance before the service confirmation.
- Before the controller treats silence as the end of a turn, it waits `0.4` seconds, since a pause between two sentences sounds the same as an ending. This hold only applies when the character has no Lip Sync reading; Lip Sync, when present, marks a response's end with no hold needed.

See [How a speaking turn ends](README.md#how-a-speaking-turn-ends) for the full model both behaviors are part of.

***

## Next steps

{% content-ref url="configure.md" %}
[Configure conversation flow](configure.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot conversation flow](troubleshooting.md)
{% endcontent-ref %}

{% content-ref url="../scripting-reference.md" %}
[Embodiment scripting reference](../scripting-reference.md)
{% endcontent-ref %}
