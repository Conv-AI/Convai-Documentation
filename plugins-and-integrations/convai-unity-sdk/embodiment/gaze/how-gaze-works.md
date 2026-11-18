---
title: How gaze works
description: Understand how the Gaze module chooses a target, shares the look across eyes, head, and body, and reacts to the conversation's dialogue state.
last_reviewed: "4.6.0"
---

`ConvaiGazeController` decides what a character looks at and how committed the look is, then articulates it across the body in a fixed order so the eyes, head, and torso never disagree about the target. This page explains the pipeline behind that decision: how a target is chosen, how the character's [dialogue state](../../core-concepts/dialogue-state.md) changes how strongly it commits, and why an eye movement and a body turn feel like one gesture instead of two separate systems.

## The three-stage pipeline

Every cognition tick, Gaze runs the same three stages in order.

| Stage | Question | What decides it |
| --- | --- | --- |
| Targeting | Who or what should the character look at? | Candidates published by target providers, plus any scripted `GazeAt` request, resolved by priority. |
| Policy | How much should the character commit? | The current dialogue state's entry in the profile's state policy table, adjusted by emotion and speech activity. |
| Solvers | How does the look get there? | Torso, then neck and head, then eyes, then eyelids — each layered on top of the character's Animator pose. |

The reasoning behind separating targeting from policy is that "what" and "how much" change for different reasons: a new candidate can appear at any moment, but how strongly the character commits to it should follow the shape of the conversation, not the moment the candidate appeared.

## How a target is chosen

Target providers publish candidates every tick, and an arbiter resolves them by priority rather than by whichever one registered first.

1. **A scripted `GazeAt()` request wins first** while the character is in `Natural` or `Social`-fidelity focus — see [Scripted gaze](scripted-gaze.md). An `Exact`-fidelity focus rejects a scripted request unless `AllowScriptedOverridesDuringExactFocus` is enabled.
2. **Priority tier decides everything else.** The player anchor publishes at priority 10, other Convai characters at priority 7, and world objects at priority 5. A higher tier always preempts a lower one.
3. **Within a tier, the current target is sticky.** The character only glances to an equal-priority alternative when its interest in the held target runs out or a hold-time cap is reached.

Because the player anchor publishes at the highest tier, the player is the character's main target whenever the current dialogue state's policy allows it. To send a character's attention somewhere else — a cutscene camera, a second player in split-screen — either set an explicit anchor on the player target provider or register your own `IGazeTargetProvider` at a higher priority. See [Gaze targets and providers](targets-and-providers.md).

## How dialogue state changes commitment

`ConvaiGazeController` does not treat every moment of a conversation the same way. Its profile's state policy table pairs each [dialogue state](../../core-concepts/dialogue-state.md) with an engagement level, whether the player counts as a valid target, and whether a body turn is allowed:

| Dialogue state | Engagement | Player is a valid target | Body turn allowed |
| --- | --- | --- | --- |
| `Idle` | Lowest | No — ambient looking-around instead | No |
| `Attending` | High | Yes | Yes |
| `Listening` | Highest | Yes | Yes |
| `Thinking` | Reduced | Yes | No |
| `Speaking` | Full | Yes | Yes |
| `Reacting` / `Interrupted` | Full / near-full | Yes | Yes |
| `Settling` | Reduced | Yes | No |

A state not listed in the profile's table falls back to the `Idle` row. This is why a character ignores the player while `Idle`, commits through `Attending`, `Listening`, and `Speaking`, and softens contact again during `Thinking` and `Settling` — the same table drives every state transition, rather than a hand-authored rule per state. [Configure eye contact](configure-eye-contact.md) covers the `GazeEyeContactMode` setting that can override this table entirely for a character that must always hold the player's gaze.

## How the look moves through the body

Once a target and a commitment level are set, the solver stage moves the character toward it in a fixed order: torso first, then neck and head, then eyes, then eyelids. The eyes commit to a new target first, and the head follows a beat later — the same eyes-then-head sequence real people use, rather than the whole body snapping to a new heading at once. For a large enough angle — the player standing behind the character, for example — the body itself turns to bring the target back in front, using either the character's own turn-in-place animation or a smooth procedural rotation depending on which embodiment modules the character carries.

This layered order is also why gaze and the character's Animator pose never conflict: every solver stage runs after the Animator has posed the skeleton for that frame, so a gaze-driven head rotation adjusts the animated pose instead of racing it. See [How embodiment works](../how-embodiment-works.md) for the shared tick order every embodiment module runs in.

## Following the conversation

`ConvaiGazeController.AttendToSpeaker` (`GazeSpeakerAttention`) controls whether a character turns to look at whoever else is currently speaking in a room with more than one participant — the "everyone looks at the person talking" behavior of a group conversation. It only applies while the character is not in its own turn, so it never competes with the character's own conversational eye contact.

| Mode | Behavior |
| --- | --- |
| `Off` | The character never follows anyone else's turn. |
| `Player` | Turns to the player while the player is speaking; ignores other characters' turns. |
| `Characters` | Turns to another character while that character is speaking; never to the player. |
| `Anyone` (default) | Turns to whoever holds the floor, player or character. A player who interrupts a speaking character takes the floor immediately. |

### Attention decays, it does not time out

Every listener tracks how much of its attention each other participant currently holds. A speech onset, being addressed, or being expected to answer raises that value; nothing else does, and between those events it fades continuously rather than holding until a fixed deadline and releasing all at once. The listener looks at whoever holds the highest value, so a conversation that outlives a pause reads as drifting toward idle life rather than a light switching off. Each listener draws its own reaction delay for a given event, scaled by how near and central the speaker is to that listener, so a group of listeners never turns in the same frame — and the room additionally enforces a minimum gap between any two listeners' reactions to one event, so independent draws that would otherwise land together are pushed apart. The four settings that shape this — typical reaction delay, how much that delay varies, how long attention takes to fade, and the minimum gap between listeners — live in the profile's [Conversation attention](profile-reference.md#conversation-attention) group.

The character currently being addressed is untouched by this system: its own dialogue state policy governs its eye contact, so it reads as the person being spoken to rather than as one more listener. An eye-contact lock (`GazeEyeContactMode.ConversationLock` or `AlwaysLock`) overrides attention entirely — a lock is a promise that the character keeps looking at the player.

### It follows the floor, not a speech flag

Whoever is talking holds the floor, and the floor has memory: a speaker keeps it through their own pauses, so a listener does not release them the instant they draw breath. Taking the floor from whoever holds it needs sustained speech — a cough, a "mm-hmm", or one false positive from voice detection is short enough to read as an interjection rather than a turn change, so it does not turn every head in the room. The floor is noticed from the player's own microphone locally, rather than only from the service's round-tripped confirmation, so the room starts turning on the player's first word instead of waiting for a network round trip. A player who sends a typed message takes the floor exactly as one who talks.

### Small movement does not trigger a re-plan

Every gaze target is smoothed before the movement detector evaluates it, so ordinary conversational sway and camera jitter do not trigger a fresh head movement plan. A large, sudden displacement — a camera cut or a teleport — still triggers immediate re-acquisition instead of a dragged, unnatural follow.

### Personalities author their own values

Every personality preset on `ConvaiGazeProfile` — `Default`, `Confident`, `Warm`, `Attentive`, `Shy`, `Stoic` — authors its own values for the Conversation attention group, alongside every other field that carries feel. `Confident` reacts more slowly and holds its attention on a speaker longer than `Warm` does, for example, which is part of what makes the two presets read differently in a group scene.

In Play mode, the `ConvaiGazeController` Inspector's Live section, the Gaze editor window, and the `Convai.DiagnoseGaze` assistant tool each report one line naming who the character is watching, or which gate — distance, angle, or line of sight — turned a speaker away.

## Next steps

{% content-ref url="quick-start.md" %}
[Gaze quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="configure-eye-contact.md" %}
[Configure eye contact](configure-eye-contact.md)
{% endcontent-ref %}

{% content-ref url="targets-and-providers.md" %}
[Gaze targets and providers](targets-and-providers.md)
{% endcontent-ref %}
