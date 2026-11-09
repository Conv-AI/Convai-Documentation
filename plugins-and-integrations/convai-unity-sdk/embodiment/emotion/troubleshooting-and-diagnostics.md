---
title: Troubleshoot emotion
description: Diagnose missing emotion signals, unmoving expressions, unknown vocabulary labels, profile ownership, and action reactions in the Unity SDK.
last_reviewed: "5.0.0-preview"
---

Start in Play mode with the Emotion Controller's **Live** section. **Feeling** and **Strength** describe the transient expression; **Mood** is separate. A resting mood can move the face even when no server emotion arrives, so a visible smile alone does not confirm that detection is working.

## Inspect live state

| What to inspect | Location | Meaning |
| --- | --- | --- |
| **Feeling**, **Strength**, **Mood**, **Held For** | Controller Inspector → Live | Current canonical emotion, score, resting mood, and dominant-label duration |
| **Everything it is feeling** | Emotion Editor → Live | Bars for emotions with nonzero scores |
| **Hold one expression** | Controller Inspector → Advanced | A serialized hold ignores incoming emotion until released |
| **Emotion detection** | Controller Inspector → Advanced | Off requests no conversation-driven emotion signal |
| `Current.AllScores` | Scripting API | The complete score table, including zero scores |

For a direct face test, enter Play mode, choose an expression and strength under **Live**, select **Try It**, then **Stop**. Neither the controller nor the Emotion Editor provides an Edit-mode facial preview.

## First checks

{% stepper %}
{% step %}
### Check detection and the connection

If the status shows **Off**, use **Turn Emotions On** or select a detection provider under **Advanced**. The mode is resolved when connecting; reconnect after changing it. Confirm the character connects and responds before expecting server emotion events.
{% endstep %}

{% step %}
### Check holds and component placement

Turn off **Advanced → Hold one expression**. If application code called `SetEmotionOverride`, call `ClearEmotionOverride`; this releases the override to neutral until the next accepted signal. Place the controller on the owning `ConvaiCharacter` or one of its children. A child is supported; a controller with no `ConvaiCharacter` ancestor cannot match character events.
{% endstep %}

{% step %}
### Check the personality and signal

An empty **Personality** field is valid: **Using SDK Defaults** runs a hidden Composed profile with a `trust` resting mood at `0.45`. Assign a profile when you need a different character type. Watch **Live → Feeling** and **Strength** during conversation, then use **Try It** to separate signal problems from facial-output problems.
{% endstep %}

{% step %}
### Check facial output

If values change but the face does not, confirm a skinned facial mesh has blendshapes. Inspect the resolved mapping in **Emotion Editor → Expressions**. ARKit, Reallusion CC3/CC4, and MetaHuman are supported conventions; map other naming conventions with a `CustomRigConventionMap`. See [Character rig setup](../character-rig-setup.md).
{% endstep %}
{% endstepper %}

## Setup findings

| Finding | Meaning and action |
| --- | --- |
| **Emotions are switched off** | Detection is Off. **Turn Emotions On** selects Responsive. |
| **Face rig not recognised** | Blendshapes exist but do not match a supported convention. Assign a custom rig convention map. |
| **No face to move** | No skinned mesh with blendshapes was found under the character. Provide a facial mesh before expecting visual output. |
| **Resting mood has no strength** | A profile mood is set at zero strength. **Give It Some Strength** restores a usable value. |
| **This character's resting mood has no strength** | The controller's own mood override is at zero. **Give It Some Strength** adjusts that override. |
| **Resting mood is not a real emotion** | The controller's resting label does not resolve. Choose a valid label or **Use The Personality's Mood**. |
| **Resting face will look frozen** | The profile has a resting mood but small movements are disabled. **Keep The Face Alive** enables them. |
| **Conversation reactions will never show** | Reaction strengths are nonzero but **Never Sits Perfectly Still** is off. Use **Keep The Face Alive**. |
| **Nobody to react to** | Picking up others' moods is enabled without another Convai character in the open scenes. Add one or choose **Turn That Off**. |
| **Nothing to react to yet** | Mood-after-action labels exist but the character has no Action Runner. Add the action setup if needed; the inactive settings cost nothing. |

## Unknown server labels

An unknown label produces a warning once per label and falls back to neutral. Inspect the Console for the unresolved value, then check **Emotion Editor → Live → Everything it is feeling** or `Current.AllScores`.

1. Use **Live → Try It** with a known canonical label to check the face.
2. Create or edit a project taxonomy and add the unknown word to the intended entry's aliases. For example, map a custom `optimistic` label to `anticipation` if that fits your authored vocabulary.
3. Check for duplicates. Canonical labels take priority; the first duplicate alias wins. `excited` already belongs to `joy` in the default vocabulary, so remapping it requires removing that earlier alias.
4. Rebuild the runtime pipeline by re-entering Play mode or disabling and enabling the controller. Confirm the new signal resolves.

The profile's **Unknown emotions** diagnostics help catch invalid authored labels. They do not prove what a backend will send; test with your actual character configuration.

## Late emotion after interruption

The 5.0 receive path drops emotion effects for interrupted or aborted replies and group lines cut off by a push-to-talk press. Those events do not reach the manager event, character event, or relay. A missing callback for an obsolete reply is expected; verify callbacks with a newly accepted reply.

## Facial expression and LipSync

During speech, LipSync has priority over Emotion on the mouth region. Outside speech, the emotion mouth influence can contribute again. Upper-face expression should remain available independently. If the entire face stops moving, inspect the resolved facial mapping and custom convention rather than changing mouth priority. See [Facial composition](../facial-composition.md).

For shader effects, verify the slot's shader property name and its material. Material effects target resolved facial meshes with blendshapes, not arbitrary body renderers. If none of the authored properties exists on any target material, the binding warns once per bind. See [Emotion output bindings](output-bindings.md).

## Profile ownership

A package profile's own Inspector is read-only. **Create A Project Copy** saves a copy under `Assets/Convai/ConvaiEmotionProfile/` and selects it; it cannot reassign a character because no character is targeted. Assign that copy to **Personality** yourself.

Editing a package profile through a character's Inspector or the Emotion Editor instead creates and assigns a copy for that character. Shared project profiles affect all characters that use them unless you choose **Make Unique**. See [Asset ownership](../../core-concepts/asset-ownership.md).

## Relay callbacks and UI labels

Confirm **Auto Resolve Character** finds a `ConvaiCharacter` on the relay's GameObject, or explicitly assign **Character**. Keep the relay enabled and verify detection, connection, and an accepted reply.

The event sends `CharacterEmotionRelayData`, not a string. Use a receiver method to extract `Emotion`; directly wiring a dynamic UI `text` property cannot do that. See the [UI receiver example](usage-examples.md#scenario-6-display-the-raw-emotion-in-a-ui-label). Mood transitions use the controller's C# `MoodChanged` event, not the relay.

## Console messages

| Message or identifying phrase | Meaning and action |
| --- | --- |
| `No facial blendshapes could be resolved` | Emotion state can update without visible output. Check mesh and convention mapping. |
| `The backend sent the emotion` | The server label is absent from the vocabulary; neutral is used. Add an alias if appropriate. |
| `Ignored an emotion event without a character id` | An unscoped event is rejected to prevent cross-character effects. Fix the event producer. |
| `has no ConvaiCharacter on itself or any parent` | Move the controller to its character or a child. |
| `SetEmotionOverride was given` / `SetMood was given` | A scripted label is unknown. Validate with `TryResolveEmotionLabel` before calling. |
| `Mood After Actions uses` | An outcome label is unknown and the reaction is skipped. Choose a defined label. |
| `none of the authored shader properties` | Material-property names missed every resolved target material. Check spelling and material assignment. |
| `marks no emotion as the neutral one` | Set exactly one taxonomy entry as neutral; runtime otherwise uses a stand-in. |
| `only the first is used` | Multiple neutral entries are marked. Untick the extras. |

Unknown-label warnings are deduplicated; lack of a repeated warning does not mean the vocabulary was fixed. Re-test after rebuilding the runtime pipeline.

## Next steps

{% content-ref url="emotion-inspector.md" %}
[Emotion Inspector](emotion-inspector.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}
