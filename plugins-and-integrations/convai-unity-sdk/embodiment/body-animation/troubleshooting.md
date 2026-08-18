---
title: Troubleshoot body animation
description: Diagnose no motion, a T-pose, locomotion desync, a fighting Animator Controller, actions that never fire, and misaimed pointing gestures.
last_reviewed: "4.5.0"
---

Most body animation problems trace back to one of a small number of setup gaps, and `ConvaiBodyAnimationController`'s inspector reports most of them by name before you ever open the console. This page covers the symptoms that checklist does not fully explain, the `AnimTraceVerbosity` dial for deeper diagnosis, and a complete reference for every common failure.

## Diagnose with AnimTraceVerbosity

`ConvaiBodyAnimationConfig`'s **Trace Verbosity** field controls how much a character writes to the console, through the `AnimTraceVerbosity` enum: `Off`, `State`, `Detail`, `Firehose`. It ships as `Off`, which still logs every warning and error — a character that walks and talks transitions constantly, so a console full of routine play-by-play is where a real warning goes unread.

| Level | What it adds |
|---|---|
| `Off` | No trace output. Warnings and errors still log. |
| `State` | State-machine transitions, layer ownership changes, action lifecycle, and clip selections — raise the one character you are diagnosing to this level. |
| `Detail` | Adds selector decisions (angles, distances, foot phase), variant rolls with weights, and speed-warp clamps. |
| `Firehose` | Adds throttled per-tick dumps of layer weights and blend positions. Extremely chatty; use only for short debugging sessions. |

Raise **Trace Verbosity** to `State` on the character you are diagnosing, reproduce the symptom, then put it back to `Off`. The SDK's own `ConvaiSettings` log level also has to allow the line through: `State` logs at `Info`, `Detail`/`Firehose` at `Debug`. The same entries also feed a ring buffer that backs the controller inspector's compact **Live** strip and the **Body Animation Editor** window's deeper Live mode — verbosity gates the ring buffer too, so at `Off` the Live surfaces still show dialogue state, movement state, and any warning, but the rolling transition log needs `State` or higher to populate.

## Symptom quick reference

| Symptom | Likely cause | Fix | Verify |
|---|---|---|---|
| Character never idles or reacts to speech | No `Animator`, a non-Humanoid avatar, or no `ConvaiBodyAnimationSet` assigned | Add a Humanoid `Animator`, or assign a set to the component or its profile | Controller inspector shows **Ready** instead of **Not Set Up** |
| Character holds a T-pose | Same as above — the `PlayableGraph` never built, so the Animator falls back to its bind pose | Same fix as no motion | Character shows a looping idle in Play mode |
| Character glides, slides its feet, or its legs desync from movement | Locomotion clips have no measured metadata, or a custom locomotion provider does not implement `IConvaiManagedLocomotion` | Run **Measure Clips** on the set, or implement the managed-locomotion capability | `LocomotionClipsMissingMetadata` in the Setup checklist reads `0` |
| Legs or arms twitch or fight the intended pose | A Runtime Animator Controller is still assigned on the Animator | Clear the Animator's **Controller** field | The `rig.redundant-animator-controller` finding disappears from Setup |
| An action or gesture never plays | Action name does not match any `ActionName`/alias in the set, or the call ran before the runtime was ready | Compare the requested name to the set's authored names (case-insensitive, space/dash/underscore-equivalent); call from `RuntimeReady` instead of `Awake`/`Start` | Console shows the matching name reach `_actionLayer.Play` instead of the "no matching action" warning |
| Pointing arm aims at the wrong spot | Only one or a few directions are authored in the set's pointing table; `PointAt` snaps to the angularly closest one | Author more directional pointing clips covering the angles your scene needs | The played clip's authored yaw/pitch is close to the requested direction |

## No motion at all

A character with no motion at all — no idle sway, no talk gestures, nothing — almost always fails one of three setup checks the controller's own inspector reports before you open the console:

- **No Animator was found under the character root.** `ConvaiBodyAnimationController` needs a Humanoid `Animator` to build its `PlayableGraph`, so with none present the module stays inactive (`BodyAnimationTroubleshooter.cs:228-230`).
- **The Animator's avatar is not a valid Humanoid rig.** Set the model's **Animation Type** to **Humanoid** in its import settings (`BodyAnimationTroubleshooter.cs:238-239`).
- **No Animation Set is assigned**, directly or through a profile — the character has content it could play but nothing wired to it (`BodyAnimationTroubleshooter.cs:264-267`).

Open the controller's inspector or **Convai > Body Animation Editor**'s Setup mode; all three report as an error-severity finding that names the exact missing piece rather than a generic failure.

## Character stuck in T-pose

A T-pose is Unity's fallback when nothing is driving the Animator at all — it shares the same underlying cause as no motion at all, and reads more visibly wrong because the character has no authored idle to fall back to. Check the same three conditions: a Humanoid `Animator`, a valid Humanoid avatar, and an assigned `ConvaiBodyAnimationSet` with at least one looping idle entry. A set with no valid idle entry (`HasAnyIdle` false) leaves the character with nothing to blend to even once the graph itself builds successfully.

## Locomotion out of sync with the NavMeshAgent

Two distinct symptoms share this heading, and they have different causes.

**The character does not walk at all.** `ConvaiNavMeshLocomotion.MoveTo` logs the exact reason and returns `false`:

```text
[ConvaiNavMeshLocomotion] '<name>' cannot walk: it is not standing on a baked NavMesh. Bake a NavMesh for the floor (Window > AI > Navigation), and check the character starts on it.
```

(`ConvaiNavMeshLocomotion.cs:238-242`.) A destination with no walkable floor nearby logs a second, similar warning naming the destination (`ConvaiNavMeshLocomotion.cs:248-252`), and a destination on a disconnected piece of NavMesh logs a third naming the connectivity problem (`ConvaiNavMeshLocomotion.cs:260-264`). Bake a NavMesh covering both the character's start position and every destination you send it to.

**The character walks, but feet slide or the gait looks wrong at speed.** This is a measurement problem, not a NavMesh problem: locomotion clips assigned to the set need their ground speed measured by the Clip Motion Analyzer before the animation can track the agent's real speed. The Setup checklist reports this directly:

```text
{N} locomotion clip(s) have not been measured, so the character falls back to configured speeds instead of the clips' real ground speed — the usual cause of sliding feet. Directional starts and planted stops also stay off until their motion is measured.
```

(`BodyAnimationTroubleshooter.cs:359-363`.) Re-run **Measure Clips** — on the set's own inspector, or in the Body Animation Editor's Content mode — after any locomotion clip changes.

## An Animator Controller fighting the graph

`ConvaiBodyAnimationController`'s `PlayableGraph` replaces the Animator's output while active, but it does not clear a Runtime Animator Controller left assigned on the Animator component. When one is present, the Setup checklist reports it:

```text
An Animator Controller is assigned; the body animation PlayableGraph replaces its output while active. Remove it to avoid confusion, or leave it as an inert fallback.
```

(`BodyAnimationTroubleshooter.cs:247-249`.) In practice, a leftover controller most often surfaces as legs or arms twitching or briefly snapping toward a different pose than the graph intends. Clear the Animator's **Controller** field — the Setup checklist offers a one-click fix for this specific finding.

## Actions not firing

A `PlayAction` call that never plays fails in one of two ways, and the console tells you which:

- **The runtime was not ready yet.** A call made from `Awake()`/`Start()`, before the `PlayableGraph` finishes building, is queued in a single deferred slot and replayed automatically — but only until it expires:

  ```text
  PlayAction('<name>') requested before the animation graph was ready — it will be replayed automatically once the graph builds, or expire after 2s.
  ```

  (`ConvaiBodyAnimationController.cs:462-465`.) Subscribe to `RuntimeReady`, or check `IsRuntimeBuilt`, instead of relying on the deferred slot for anything that must not be dropped.

- **The name did not match any authored entry.** Matching is case-insensitive and treats spaces, dashes, and underscores as equivalent, but an unmatched name still fails:

  ```text
  PlayAction('<name>') — no matching action in set '<set display name>'.
  ```

  (`ConvaiBodyAnimationController.cs:472-473`.) Compare the exact name your code or a backend action sends against the `Action Name` and `Aliases` fields authored in the set.

`PlayAction` never returns `null` in either case — check `handle.Failed` and read `handle.FailureReason` instead of expecting an exception.

## Pointing looks wrong

`ConvaiBodyAnimationController.PointAt` fails outright (`handle.Failed`) only when the target is `null`, the runtime is not built, or the set authors no pointing clips at all — each reports its own `FailureReason` (`ConvaiBodyAnimationController.cs:594-667`).

A pointing gesture that plays but aims at the wrong spot is not a failure — it is expected behavior from how directions are selected. Each `PointingEntry` authors a fixed character-local yaw and pitch, and `PointAt` always plays whichever authored entry is angularly closest to the requested direction; it does not blend or procedurally aim between entries (`PointingEntry.cs:8-12,84-106`). A set with only a few authored directions snaps to the nearest one, which can be visibly off for a target well outside any authored angle. Author more directional pointing clips covering the range of angles your scene actually needs.

## Next steps

{% content-ref url="play-actions-and-gestures.md" %}
[Play actions and gestures](play-actions-and-gestures.md)
{% endcontent-ref %}

{% content-ref url="config-reference.md" %}
[Body animation config reference](config-reference.md)
{% endcontent-ref %}

{% content-ref url="../../overview/release-notes.md" %}
[Release notes](../../overview/release-notes.md)
{% endcontent-ref %}
