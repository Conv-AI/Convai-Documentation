---
title: Troubleshoot conversation flow
description: Diagnose a dialogue state stuck on Idle, timing that feels wrong, and conflicts between conversation flow drivers in multi-character scenes.
last_reviewed: "4.5.0"
---

Use this page when a character's dialogue state never changes, changes at the wrong pace, or a multi-character scene shows one character reacting to another's conversation. Start by entering Play mode and expanding the **Live** section on the `ConvaiConversationFlowController` component — most of the symptoms below are visible there directly.

***

## Troubleshooting table

| Symptom | Likely cause | Fix | Verify |
| --- | --- | --- | --- |
| **State** stays `Idle` in the **Live** section even while the character is speaking | The character's ready signal never arrived — the `ConvaiCharacter` has not finished connecting, or events for it are not reaching this controller | Confirm the character finishes connecting before you expect embodiment behavior. If `ConvaiConversationFlowController` sits under a different `GameObject` than the `ConvaiCharacter` it should track, move it under the same hierarchy | **State** changes away from `Idle` once the character connects and the conversation starts |
| Character lingers in `Thinking`, `Attending`, or `Settling` far longer or shorter than expected | The assigned `ConvaiConversationFlowProfile` sets a longer or shorter hold than intended, or no profile is assigned and the built-in defaults do not match the pace you want | Open the assigned profile (or assign one) and check its **Dialogue Beats** fields against [Conversation flow reference](reference.md) | **Time In State** in the **Live** section stops advancing past the tuned duration for that state |
| A `ConvaiConversationFlowController` appeared on a character you never added it to | Convai auto-provisioned it because another module — currently Body Animation, with **Auto Create Conversation Flow** enabled — needed a dialogue state and none existed | Nothing to fix — this is expected. Configure the auto-added controller like any other, or disable **Auto Create Conversation Flow** on the Body Animation component if you want to add the controller yourself | The Console logged the message quoted below once, naming the character |
| In a multi-character scene, one character's dialogue state reacts to another character's player speech | More than one `ConvaiConversationFlowController` is active at once; each driver scopes itself to its own character once it detects other active drivers, but a scene with no scoped conversation target can briefly share unscoped signals | Give each character's conversation flow driver a scoped conversation target instead of relying on unscoped player speech and transcript events | The Console warning quoted below stops appearing, and each character's **State** only changes for its own turns |

***

## State never leaves Idle

The state machine's first rule is unconditional: while the character is not ready, the reading stays `Idle` regardless of any other signal. "Ready" here means the character has connected and Convai has confirmed it, not merely that the `GameObject` is active in the scene.

If the character does become ready but **State** still does not move, confirm `ConvaiConversationFlowController` is on the same `GameObject` hierarchy as the `ConvaiCharacter` it is meant to track — a controller resolved against the wrong character never sees that character's speech and transcript events.

***

## Timing feels wrong

Every hold, grace period, and delay the state machine uses comes from the assigned `ConvaiConversationFlowProfile` — or, if none is assigned, from the same values shown as defaults in [Conversation flow reference](reference.md). If the character replies too slowly, lower **Thinking Max Hold**; if it settles back to `Idle` too quickly during pauses, raise **Idle Return Delay**. Watch **Time In State** in the **Live** section while you tune a value to see the effect immediately in Play mode without needing to script anything.

One field pair is self-correcting rather than silently wrong: if **Thinking Min Hold** is set above **Thinking Max Hold**, the profile raises **Thinking Max Hold** to match the moment you edit it in the Inspector, so the two fields never disagree with what the character actually does.

***

## Conversation flow appeared without being added

Convai adds `ConvaiConversationFlowController` automatically when a module on the character demands a dialogue state and none exists yet. Currently only Body Animation does this, through its **Auto Create Conversation Flow** setting (enabled by default). The Console logs once, naming the character:

```text
[ConvaiConversationFlowController] Added to '<character name>' because an embodiment module on this character needs the dialogue state. Add the component yourself if you want to configure it.
```

This is not an error. The auto-added controller behaves exactly like one you add yourself — see [Configure conversation flow](configure.md) to assign it a profile.

***

## Duplicate drivers in multi-character scenes

`ConvaiConversationFlowController` disallows more than one instance on the same `GameObject`, but a scene can still run several controllers at once — one per character. When more than one is active, each driver scopes player speech and transcript events to its own character so one character's `Listening` state does not leak into another's. Until a controller has a scoped conversation target, it logs a warning instead of silently ignoring the wrong signals:

```text
[ConvaiConversationFlowController] '<character name>' is ignoring unscoped player speech/transcript events because multiple conversation flow drivers are active. Provide a scoped conversation target to drive per-character player-turn state in multi-character scenes.
```

Give each character a scoped conversation target so its driver only reacts to that character's own turns.

***

## Next steps

{% content-ref url="configure.md" %}
[Configure conversation flow](configure.md)
{% endcontent-ref %}

{% content-ref url="reference.md" %}
[Conversation flow reference](reference.md)
{% endcontent-ref %}

{% content-ref url="../troubleshooting.md" %}
[Troubleshoot embodiment](../troubleshooting.md)
{% endcontent-ref %}
