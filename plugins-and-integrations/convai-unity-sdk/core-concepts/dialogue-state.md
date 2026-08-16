---
title: Dialogue state
description: Understand the eight-value dialogue state every embodiment module reads to know whether a character is idle, listening, or speaking.
last_reviewed: "4.5.0"
---

Every embodiment module — Gaze, Body Animation, Body Language, and Emotion — reads the same eight-value `DialogueState` to know what beat of the conversation a character is in. Conversation Flow is the one module that decides this value; every other module only reads it. Understanding what each state means makes the rest of the embodiment modules' behavior legible.

***

## The eight dialogue states

`DialogueState` (`SDK/Domain/Embodiment/Semantics/DialogueState.cs`) is the canonical conversation-phase model shared across the embodiment stack.

| State | Value | What it means in a conversation |
| --- | --- | --- |
| `Idle` | `0` | The character is not engaged in a turn. Idle micro-behavior — weight shift, ambient gaze — dominates. |
| `Listening` | `1` | The player is speaking and the character is actively listening. Gaze commits to the player, body language tends to lean in, and emotion holds near neutral. |
| `Attending` | `2` | The character is orienting toward a focus target — for example the player initiating a turn — before the player has started speaking, or it is holding a conversationally engaged stance between beats before cooling back to ambient idle. |
| `Thinking` | `3` | The player has finished speaking and the character has not yet replied. Models the natural cognitive pause: gaze can break, micro-saccades increase, and brows lift. |
| `Speaking` | `4` | The character is currently speaking. LipSync owns the mouth, and emotion and gesture intensity scale with speech energy. |
| `Reacting` | `5` | A short reaction beat after a significant event — unexpected player input, a high-intensity emotion arrival. Lets a module play a one-shot without disturbing the primary state. |
| `Interrupted` | `6` | The character was interrupted mid-turn. Expressed as a brief freeze and a quick settle before transitioning back to `Attending`. |
| `Settling` | `7` | Post-turn cooldown: the character has finished speaking, gaze softens, and emotion gradually decays back to its resting tone before handing off to `Attending`. |

The model is deliberately richer than a coarse idle/listening/talking split. Each state represents a distinct beat in a natural conversation, which is what lets Gaze, Body Language, Emotion, and Body Animation produce believable behavior without hard-coding overrides for each other.

***

## Who owns the state, and who reads it

`ConvaiConversationFlowController` (`SDK/Modules/ConversationFlow/Components/ConvaiConversationFlowController.cs`) is the single authored source of truth for a character's dialogue state. Every other embodiment module only reads it; none of them redefine or infer their own version of it.

The controller exposes two members on its own public surface:

| Member | Type | Description |
| --- | --- | --- |
| `Current` | `DialogueStateReading` | The character's current reading: a `Primary` state, the `BlendTo` state being transitioned toward, a `BlendWeight` in `[0, 1]`, `TimeInState` in seconds, and a normalized `EnergyLevel` in `[0, 1]` used to scale gesture and micro-behavior intensity. |
| `Changed` | `event Action<DialogueStateReading>` | Raised whenever the reading changes. |

A reading always describes a blend between two states rather than a hard cut, so a module can cross-fade its output instead of snapping. When no transition is in flight, `Primary` and `BlendTo` are equal and `BlendWeight` is `0`.

***

## When the controller is auto-added

A `ConvaiConversationFlowController` does not always have to be added by hand. `ConvaiBodyAnimationController` asks for one, so a character with body animation and no authored controller gets one automatically, and Convai logs once naming the character and why. The auto-added controller behaves exactly like one you add yourself — configure it afterward if the shipped timing does not fit your character.

The other modules do not ask for one. Gaze, Body Language, and Emotion read the dialogue state if it is there and fall back to `Idle` if it is not. A character with only those modules and no body animation therefore never leaves `Idle`, and its behavior stays flat and unresponsive to the conversation. If that is what you are seeing, add a `ConvaiConversationFlowController` yourself.

{% hint style="info" %}
The contract behind this reading, `IConversationFlowSource`, is `internal` to the package. Read `ConvaiConversationFlowController.Current` and subscribe to `Changed` — do not implement the interface yourself.
{% endhint %}

***

## Next steps

{% content-ref url="character-embodiment.md" %}
[Character embodiment](character-embodiment.md)
{% endcontent-ref %}

{% content-ref url="asset-ownership.md" %}
[Asset ownership and copy-on-write](asset-ownership.md)
{% endcontent-ref %}
