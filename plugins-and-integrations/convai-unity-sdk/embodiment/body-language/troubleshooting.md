---
title: Troubleshoot body language
description: Diagnose why a Convai character's Body Language controller shows no motion, fights other modules, or reads too subtle or theatrical.
last_reviewed: "4.5.0"
---

Diagnose the most common Body Language failure modes: no motion at all, motion that fights another module, a refused scripted gesture, motion that reads too subtle or too theatrical, and motion that scales oddly with camera distance.

## Symptom table

| Symptom | Likely cause | Fix | Verify |
|---|---|---|---|
| No motion at all | Rig binding failed, or no `Spine` bone resolved | Confirm the character has a Humanoid `Animator` with the spine chain mapped | Console shows no `Rig binding has no Spine bone` error, and the character breathes and sways at rest |
| Motion fights scripted animation | Another module is holding the pose — Body Animation playing a walk or full-body action, or gesture suppression | Check the Inspector's **Sharing This Body** card to see which module is reducing the motion | **Runtime Status** shows `GesticulationSuppression` return to `None` once the other module finishes |
| A `Nod`/`Shake`/`Tilt` request does nothing | `HeadGestureHandle.Refusal` is `Busy` or `Unavailable` | `Busy`: retry after a short delay. `Unavailable`: fix the rig or profile setup below | `handle.IsActive` is `true` on the next request, or `handle.Refusal` is `None` |
| Motion reads too subtle | `Expressiveness Preset` is `Subtle`, or amplitude fields are set low | Raise `Expressiveness Preset` to `Natural` or higher, or raise the relevant profile amplitude fields | The character's posture pulses and sway become visible at a normal 2-meter camera distance |
| Motion reads too theatrical | `Expressiveness Preset` is `Theatrical`, or amplitude fields are set high | Lower `Expressiveness Preset` to `Natural`, or lower the relevant profile amplitude fields | Gestures no longer look exaggerated at a normal conversational distance |
| Motion scales oddly with camera distance | `Enable Camera Distance Lod` is on and the main camera moved far from or close to the character | Confirm the behavior is intentional (it never affects breathing, posture, or gestures — only sway and idle hand motion), or turn `Enable Camera Distance Lod` off | Sway and hand micro-motion amplitude stay constant regardless of camera distance once the toggle is off |

## No motion at all

The controller is inert when it cannot resolve a `Spine` bone. Two distinct failures produce this, each logged once via `ConvaiLogger` under `LogCategory.BodyLanguage` — never per frame:

* No rig binding at all:

  ```text
  [ConvaiBodyLanguageController] No rig binding could be resolved. Body language needs a Humanoid character with a StandardRigBinding (added automatically for Humanoid Animators). The module stays inert.
  ```

  (`ConvaiBodyLanguageController.cs:1863-1865`)

* A rig binding exists, but it has no `Spine` bone:

  ```text
  [ConvaiBodyLanguageController] Rig binding has no Spine bone. Check that the Animator avatar is Humanoid and the spine chain is mapped; the module stays inert until a Spine bone exists.
  ```

  (`ConvaiBodyLanguageController.cs:1874-1876`)

Before pressing Play, the `ConvaiBodyLanguageController` Inspector's **This Character** section runs the same check and states the same cause in Inspector text, without needing a Play session:

* No `Animator` on the character: "no Animator on this character — Body Language layers motion onto an animated skeleton, so it has nothing to move" (`BodyLanguageSetupService.cs:451-454`).
* A Humanoid avatar with no spine mapped: "Humanoid avatar, but no Spine bone is mapped — check the Avatar's spine chain" (`BodyLanguageSetupService.cs:459`).
* A non-Humanoid avatar: "the avatar is not Humanoid, so no Spine bone can be resolved" (`BodyLanguageSetupService.cs:460`).

Fix the Animator's Humanoid avatar mapping, then re-enter Play mode. Everything else on the rig — chest, shoulders, hips, legs, and arms — is optional: a missing optional bone disables only the behavior that depends on it (for example, missing shoulders disable shoulder tension, but posture and breath still run). The **This Character** card reports each optional gap without treating it as a fault.

## Motion fights scripted animation

Body Language shares the spine, shoulders, and head with Body Animation and Gaze. When Body Animation plays a walk or a full-body action, it takes the body back for the duration — `GestureSuppression` reports `UpperBody` or `FullBody` for as long as that motion runs, and Body Language's own posture and gesticulation duck accordingly. This is a deliberate hand-off, not a fault.

| `GestureSuppression` | Effect |
|---|---|
| `None` | Nothing suppressed — posture, breath, and gesture cues are all eligible. |
| `UpperBody` | Semantic gesture clips are refused, but posture (at the profile's `Upper Body Suppression Posture Weight`) and breath stay live. |
| `FullBody` | Gesture cues are refused and procedural posture/breath fade to zero. |

The `ConvaiBodyLanguageController` Inspector's **Sharing This Body** card names every module sharing the character's body and what each one changes, before Play. While playing, **Runtime Status** adds what is happening at this instant: **Body Shared With** states whether anything is currently reducing the motion, and **Head Moved By** states whether Gaze or Body Language itself is moving the head.

## A `Nod`/`Shake`/`Tilt` request does nothing

`Nod` never returns `null` and never throws — check `HeadGestureHandle.IsActive` and `HeadGestureHandle.Refusal` instead of assuming the gesture played:

* `Refusal == HeadGestureRefusal.Busy`: the character is already performing a head gesture, with one more queued behind it. Transient — retry the same request a moment later.
* `Refusal == HeadGestureRefusal.Unavailable`: the character cannot perform head gestures at all right now — no usable rig, no Body Language profile, or the component is disabled or not playing. Fix the underlying rig or profile issue instead of retrying.

See [Trigger gestures and reactions](gestures-and-reactions.md) for the full handling pattern, including the shipped `ConvaiHeadResponseActionExecutor`, which already retries a `Busy` refusal for up to 1.5 seconds.

{% hint style="info" %}
A `PulseGesture` request built from a `GestureCueKind` value with no shipped animation — `Emphatic`, `Beat`, `PalmToPlayer`, `HandToChest`, `IndicateObject`, or `Enumerate` — always falls back to a head-beat and posture pulse. That is expected behavior, not a bug: see [Body language scripting reference](scripting-reference.md#gesturecuekind) for which values have shipped content.
{% endhint %}

## Motion reads too subtle or too theatrical

Check, in order:

1. `Expressiveness Preset` on the assigned `ConvaiBodyLanguageProfile` — `Subtle` removes optional behaviors (shrugs, hand micro-life) entirely and reduces amplitude; `Theatrical` maximizes them.
2. The runtime `ConvaiBodyLanguageController.Expressiveness` override — it wins over the profile until the next profile hot-swap, so a script may have set it away from the profile's authored value.
3. Individual amplitude fields in the profile — `Max Openness Degrees`, `Max Lean Degrees`, `Posture Pulse Amplitude`, and the other fields listed on [Body language profile reference](profile-reference.md).

The `ConvaiBodyLanguageController` Inspector's **Posture (target → current)** section shows the live target and current posture values. If the target never moves off near-zero, the state policy and emotion are not reaching the directors — check the profile's **State Policies** section. If the target moves but current does not follow, check **Master Weight**: `0` means the module has not ramped in yet, or the rig did not bind.

## Motion scales oddly with camera distance

`Enable Camera Distance Lod` scales sway amplitude and idle hand-motion weight by how far the main camera is from the character — subtler close up, larger far away, neutral at a normal conversational distance. It never touches breathing, posture, or gestures. If a character's sway looks different depending on shot framing, this toggle is working as intended; turn it off on the profile if the scene requires constant amplitude regardless of camera distance.

## Next steps

{% content-ref url="gestures-and-reactions.md" %}
[Trigger gestures and reactions](gestures-and-reactions.md)
{% endcontent-ref %}

{% content-ref url="tune-expressiveness.md" %}
[Tune expressiveness](tune-expressiveness.md)
{% endcontent-ref %}

{% content-ref url="profile-reference.md" %}
[Body language profile reference](profile-reference.md)
{% endcontent-ref %}
