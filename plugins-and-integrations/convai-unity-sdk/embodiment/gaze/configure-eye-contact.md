---
title: Configure eye contact
description: Configure how strongly a Convai character commits to eye contact with the player, from natural behavior to a permanent lock.
last_reviewed: "5.0.0-preview"
---

Configure how strongly a Convai character commits to the player's eye contact by setting `GazeEyeContactMode`, `GazeFocusFidelity`, and the player anchor aim mode on `ConvaiGazeController`. Use this page when the default per-state behavior is too soft for a presenter or kiosk character, or when a character needs to look at something other than the main camera.

## Prerequisites

- A character with `ConvaiGazeController` added — see [Gaze quick start](quick-start.md).

## Choose an eye contact mode

The **Eye contact style** segmented control under **Who It Looks At** in the `ConvaiGazeController` Inspector is the product-level switch for how strongly the character commits to the player. Set it there, or at runtime through `gaze.EyeContactMode`:

| Inspector label / API value | Behavior in conversational states | Behavior while `Idle` | Use for |
| --- | --- | --- | --- |
| **Natural** / `Natural` (default) | Follows the profile's per-dialogue-state policy table — authored, varied engagement. | Ambient life; the player is not a valid target. | Characters with an authored personality that should look natural, not fixed. |
| **Focused** / `SpeakingFocus` | Commits fully to the player only while the character is actually producing speech or the dialogue state is `Speaking`. Listening and thinking stay profile-driven. | Ambient life; the player is not a valid target. | Presenters and dialogue NPCs that should focus while talking but behave naturally otherwise. |
| **Held** / `ConversationLock` | Full commitment — engagement at maximum, no intentional look-away, full head participation, body turns allowed — in every non-`Idle` state. | Ambient life; the player is not a valid target. | A character that must never look away mid-conversation, but still has idle life between conversations. |
| **Always** / `AlwaysLock` | Full commitment, same as `ConversationLock`. | Full commitment — the player is a valid target even while `Idle`. | Kiosk greeters and demo booths that should never look away. |

```csharp
ConvaiGazeController gaze = GetComponent<ConvaiGazeController>();
gaze.EyeContactMode = GazeEyeContactMode.ConversationLock;
```

Changing `EyeContactMode` at runtime ramps smoothly to the new commitment level rather than snapping.

{% hint style="warning" %}
While `ConversationLock` or `AlwaysLock` is active, the profile's per-state policy table is bypassed for engagement and aversion. Use `Natural` for speaking-planning breaks. `SpeakingFocus` locks while speaking, including a `0.2`-second grace, and cancels those breaks; its listening and thinking behavior remains profile-driven.
{% endhint %}

An eye-contact lock also overrides `AttendToSpeaker` (the **Follows the conversation** setting that turns a character toward whoever else holds the floor in a multi-character conversation): while `ConversationLock` or `AlwaysLock` is active, the character never turns away to follow another speaker's turn, regardless of what **Follows the conversation** is set to. The lock is a promise to keep looking at the player, and it wins. See [Conversation attention](profile-reference.md#conversation-attention).

**Follows the conversation** uses **Off**, **Player**, **Characters**, and **Anyone** segments. These correspond to `GazeSpeakerAttention`; the scripting property remains `AttendToSpeaker`.

## Set focus fidelity

Open **Convai > Gaze Editor > Targets > Advanced targeting**. **Focus Style** offers **Relaxed** (`Social`) and **Locked** (`Exact`). The same section contains **Let Scripts Override A Locked Focus** and **Ignore Glances While Focused**.

`GazeFocusFidelity` controls how precisely a `ConversationLock`, `AlwaysLock`, or `SpeakingFocus` commitment holds the player anchor, once one of those modes is active:

| Value | Behavior |
| --- | --- |
| `Social` (default) | Keeps small fixation motion and socially useful head gestures while still treating the player as the conversational target. Recommended for dialogue characters. |
| `Exact` | Suppresses intentional look-aways and fixation offsets while the focus is active. Blinks, eyelids, pupils, vergence, and anatomical body turns still play. |

```csharp
gaze.FocusFidelity = GazeFocusFidelity.Social;
```

`Social` fidelity still allows an explicit `GazeAt()` request to preempt the lock, so a composed action that looks somewhere first and then acts keeps working. `Exact` fidelity rejects a scripted `GazeAt()` by default; enable `AllowScriptedOverridesDuringExactFocus` if an authored sequence needs to preempt it anyway. See [Scripted gaze](scripted-gaze.md).

## Choose how the anchor is aimed

In **Gaze Editor > Targets > Advanced targeting**, **Aim Point** offers **Automatic** (`Auto`), **Exact** (`ExactTransform`), and **Offset** (`LocalOffset`). **Aim Offset** appears only for **Offset**.

`GazeAnchorAimMode` controls where on the player anchor the character actually aims, independently of which eye contact mode is active:

| Value | Behavior |
| --- | --- |
| `Auto` (default) | Uses a camera's exact position when the anchor is a camera, and applies the conventional eye-line lift for a non-camera anchor. |
| `ExactTransform` | Uses the anchor's exact world position, with no lift applied. |
| `LocalOffset` | Transforms `PlayerAnchorAimOffset` from anchor-local space to world space, so the aim point moves with the anchor. |

Set the mode on `ConvaiGazeController` as `PlayerAnchorAimMode`, and set `PlayerAnchorAimOffset` when using `LocalOffset`. `LocalOffset` is recommended for a rotated custom anchor or an XR or cutscene rig, where `Auto`'s camera-position assumption does not apply.

For split-screen, multiplayer, or cutscene setups where the character should not follow `Camera.main`, assign **Who It Looks At > Who is the player?**, or set `PlayerAnchorOverride`, to the intended transform. The caption beneath an empty field reports the resolved camera or that no camera has been found.

## Verify the setting

Enter Play mode and start a conversation. With `ConversationLock` or `AlwaysLock` set, the character should hold eye contact through every conversational beat with no look-away, and with `AlwaysLock` it should also hold contact while `Idle`. With `Natural` or `SpeakingFocus`, contact should visibly soften during `Thinking` and idle periods.

## Next steps

{% content-ref url="profile-reference.md" %}
[Gaze profile reference](profile-reference.md)
{% endcontent-ref %}

{% content-ref url="scripted-gaze.md" %}
[Scripted gaze](scripted-gaze.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot gaze](troubleshooting.md)
{% endcontent-ref %}
