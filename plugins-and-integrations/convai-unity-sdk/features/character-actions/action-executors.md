---
title: Action executors
description: Reference for all 21 built-in action executor components, grouped by pack, with every Inspector field, default, and required peer.
last_reviewed: "4.5.0"
---

Executors are the components that perform in-scene behavior when the dispatcher runs an action step — an NPC that walks, points, changes mood, or plays a sound. 21 executor components ship with the Convai SDK, grouped into six packs. Every one carries a `ConvaiActionArchetype` attribute, so adding one from the Actions Editor's **+ Add Action ▾** catalog pre-fills its action name, description, target requirement, and any parameters — no manual authoring required to get a working action.

All 21 derive from `ConvaiActionExecutorBase` (`Convai.Runtime.Actions`), most through `ConvaiTargetedActionExecutor` or the generic `ConvaiCharacterActionExecutor<TPeer>`. An executor built on `ConvaiCharacterActionExecutor<TPeer>` exposes one extra Inspector field beyond what is listed per executor below — **Character Component**, a reference to the peer component (for example `ConvaiGazeController`) it works through. Leave it empty and the executor finds the peer automatically, searching this `GameObject`'s parents first and then its children; assign it explicitly only when the character carries more than one instance of that peer type.

## Flow & Utility pack (`Convai.Runtime`)

The module-free pack, in `SDK/Runtime/Actions/Executors/` — every behavior here works on any character in any project, with no Convai module required.

### Raise Unity Event

Runs whatever you wire into its event, then always succeeds. The no-code escape hatch for anything your scene can already do from a button — open a door, start a timeline, award a point.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiUnityEventActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Raise Unity Event` |
| **Archetype action name** | `Raise Unity Event` |
| **Target requirement** | None |
| **Required peer** | None |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_onExecute` | `UnityEvent` | Empty | Invoked each time the action runs. Wire any number of callbacks in the Inspector. |

Never fails — an event with nothing wired still reports success; the Actions Editor flags an unwired event at authoring time instead. Write a custom executor when the action needs to read parameters, take time, be cancelled, or report why it could not run.

### Wait

Pauses for a few seconds and does nothing else. Rarely useful alone; inside **Run In Order** it is what gives a performance its timing — point at the door, wait a beat, then walk to it.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiWaitActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Wait` |
| **Archetype action name** | `Wait` |
| **Target requirement** | None |
| **Required peer** | None |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_seconds` | `float` | `1` | How long to wait. The character can ask for a different length with the `seconds` parameter. |
| `_maxSeconds` | `float` | `30` | Longest allowed wait. Clamps both the Inspector value and anything the character asks for, so one bad number cannot stall the scene. |

The wait is frame-wise and cancellable — it never uses `Task.Delay` — so it runs at normal gameplay pace, respects pausing and time scale, and unwinds correctly when the action is cancelled.

### Run In Order

Runs several Action Behaviors one after another as a single action — "greet the visitor" can mean look, nod, and say hello, authored with no code. Every step receives the same target and parameters.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiSequenceActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Run In Order` |
| **Archetype action name** | `Run In Order` |
| **Target requirement** | None (passed through to each step) |
| **Required peer** | None |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_steps` | `List<MonoBehaviour>` | Empty | The Action Behaviors to run, top to bottom. Each entry must implement `IConvaiActionExecutor`. |

Stops at the first step that does not succeed and reports that step's own result, prefixed with its position — a failure names which step failed and why. An entry that is empty, is not an Action Behavior, or references this same component fails immediately with `ConvaiActionFailureReason.InvalidState`.

### Show Or Hide Object

Turns the target object on or off — the shortest path from "show them the map" to something visible happening, with no extra component on the object itself.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiSetActiveActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Show Or Hide Object` |
| **Archetype action name** | `Show Or Hide Object` |
| **Target requirement** | Object |
| **Required peer** | None |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_mode` | `ConvaiShowHideMode` (`Show`, `Hide`, `Toggle`) | `Show` | What to do to the object. The character can ask for a different mode with the `mode` parameter. |

Asking for a state the object is already in succeeds and says so ("Already showing.") rather than failing — a satisfied request is fulfilled, not failed. No resolved target returns `Unhandled`.

### Play Animator State

**For characters that animate with their own Animator Controller, not the Body Animation module.** Sets a Trigger parameter mapped from the action name, and can optionally wait for the resulting state to finish.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiAnimatorStateActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Play Animator State (own Animator Controller)` |
| **Archetype action name** | `Play Animator State` |
| **Target requirement** | None |
| **Required peer** | `Animator` |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_bindings` | `List<ConvaiAnimatorActionBinding>` | Empty | One row per action this character can perform through the Animator. |

**`ConvaiAnimatorActionBinding` row fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `ActionName` | `string` | — | The action name to answer, matched case-insensitively. |
| `TriggerName` | `string` | — | The Animator Trigger parameter to set when that action runs. |
| `WaitForStateTag` | `string` | Empty | Optional. Tag the Animator state with the same word to wait for it before the action finishes. Leave empty to finish as soon as the trigger is set. |
| `NormalizedExitTime` | `float` | `0.95` | How far through the tagged state counts as finished (`0`–`1`). Only used when `WaitForStateTag` is set. |

An action name with no matching row is declined as `Unhandled` rather than failed, so another Action Behavior on the character still gets a chance to answer it. If the character has a `ConvaiBodyAnimationController`, the decline message names **Play Gesture** instead — the two behaviors drive the same Animator and would fight over it if used together.

### Play Sound

Plays a sound through an ordinary `AudioSource`. Works with or without a target — that choice is made when the action is authored: no target plus an assigned `AudioSource` plays the sound directly; a target with no `AudioSource` assigned plays from whatever the character was asked to act on.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiPlaySoundActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Play Sound` |
| **Archetype action name** | `Play Sound` |
| **Target requirement** | Either |
| **Required peer** | None |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_audioSource` | `AudioSource` | `null` | The source to play through. Leave empty to use one on the target object. |
| `_clip` | `AudioClip` | `null` | The sound to play. Leave empty to play whatever clip the `AudioSource` already has. |
| `_volume` | `float` | `1` | Playback volume, `0`–`1`. The character can ask for a different level with the `volume` parameter. |
| `_waitForSoundToFinish` | `bool` | `false` | Hold the action open until the clip finishes. |

Never plays through the character's own speech `AudioSource` — borrowing it would cut the character off mid-sentence. With neither an assigned source nor one on the target, the action declines and says what to assign. No clip resolves to `Failed`.

## Attention pack (`Convai.Modules.Gaze`)

`SDK/Modules/Gaze/Executors/` — every behavior here needs a `ConvaiGazeController` peer.

### Look At Target

Turns the character's attention to the target — eyes lead, head follows, and the body turns when the target is somewhere the head cannot reach. Finishes as soon as the gaze visibly arrives, not when the hold ends, so later steps do not queue behind the hold.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiLookAtActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Look At Target` |
| **Archetype action name** | `Look At` |
| **Target requirement** | Either |
| **Required peer** | `ConvaiGazeController` |
| **Timeout** | 10s (archetype default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_mode` | `ConvaiGazeLookMode` (`Glance`, `Sustained`) | `Sustained` | Glance is a quick look and back; Sustained is a committed look the character holds, turning the body if needed. The character can ask for either with the `mode` parameter. |
| `_holdSeconds` | `float` | `2.5` | How long to keep looking once the gaze arrives. `0` keeps looking until something else takes the character's attention. |
| `_engagement` | `float` | `1` | How intently to look, `0`–`1`. |

A glance the character declines in order to keep eye contact with the person it is talking to reports `Unhandled` (eye-contact lock working as intended), not a failure.

### Watch The Player

Holds eye contact with the player until told to stop — a scoped, cancellable request, distinct from the character's own conversational eye-contact setting, which this never changes.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiWatchPlayerActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Watch The Player` |
| **Archetype action name** | `Watch The Player` |
| **Target requirement** | None (the player is implied) |
| **Required peer** | `ConvaiGazeController` |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_mode` | `ConvaiWatchPlayerMode` (`Watch`, `StopWatching`) | `Watch` | Whether this call starts watching or stops. The character can ask for either with the `mode` parameter (`watch` or `stop`). |
| `_engagement` | `float` | `1` | How intently to watch, `0`–`1`. |

No player found in the scene fails with `ConvaiActionFailureReason.TargetMissing`. The watch releases automatically if the component is disabled mid-watch.

### Scan Environment

Inspects several distinct points across the surrounding environment, preferring scene objects within a search radius and falling back to evenly spaced world points.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiScanEnvironmentActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Scan Environment` |
| **Archetype action name** | `Scan Environment` |
| **Target requirement** | None |
| **Required peer** | `ConvaiGazeController` |
| **Timeout** | 15s (archetype default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_durationSeconds` | `float` | `3.5` | Total scan duration. The character can override with the `duration` parameter. |
| `_stopCount` | `int` | `4` | Number of distinct points where the gaze pauses, `2`–`8`. |
| `_arcDegrees` | `float` | `150` | Horizontal field covered, centred on the character's forward direction, `20`–`320`. |
| `_allowBodyTurn` | `bool` | `false` | Whether wide scan points may turn the body as well as the head and eyes. |
| `_searchRadius` | `float` | `7` | Radius used to find scene colliders worth inspecting. `0` uses generated points only. |
| `_targetLayers` | `LayerMask` | Everything | Layers containing objects that may be selected as scan points. |
| `_fallbackDistance` | `float` | `4` | Distance of generated scan points when no scene object suits the arc. |
| `_fallbackHeight` | `float` | `1.5` | Height of generated scan points above the character's origin. |

Only runs in Play mode — it drives the live gaze rig, so it declines with `Unhandled` in Edit mode. Held gaze is released on completion, cancellation, disable, or destruction.

## Expression pack (`Convai.Modules.Emotion`, `Convai.Modules.BodyLanguage`)

Set Mood and React live in `SDK/Modules/Emotion/Executors/` and need a `ConvaiEmotionController` peer. Nod Or Shake Head lives in `SDK/Modules/BodyLanguage/Executors/` and needs a `ConvaiBodyLanguageController` peer.

### Set Mood

The lasting one: eases the character into a new mood and keeps it there until something else changes it. Use for a mood shift that should color the rest of the conversation.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiSetMoodActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Set Mood` |
| **Archetype action name** | `Set Mood` |
| **Target requirement** | None |
| **Required peer** | `ConvaiEmotionController` |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_defaultMood` | `string` (emotion label) | Empty | Mood to use when the character does not name one. Normally the `mood` parameter drives this instead. |
| `_defaultIntensity` | `float` | `0.6` | Strength, `0`–`1`. The character can ask for a different strength with the `intensity` parameter. |
| `_transitionSeconds` | `float` | `1.5` | How long the change takes. |

A mood the character does not have fails, listing the moods it does have — the emotion system otherwise treats an unknown mood as neutral, which would report success while doing nothing. Use **React** instead of this for a momentary reaction; using Set Mood for a passing beat leaves the character stuck in that mood.

### React

The passing one: shows a beat, holds it, and settles back to whatever the character was feeling before — a flinch, a flash of delight, a wince. The restore is guaranteed even if the action is cancelled mid-beat.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiReactActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → React` |
| **Archetype action name** | `React` |
| **Target requirement** | None |
| **Required peer** | `ConvaiEmotionController` |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_defaultReaction` | `string` (emotion label) | Empty | Reaction to use when the character does not name one. Normally the `reaction` parameter drives this instead. |
| `_defaultIntensity` | `float` | `0.85` | Strength, `0`–`1`. |
| `_holdSeconds` | `float` | `1.5` | How long the reaction is held before settling back. |

A reaction the character does not have fails, listing the reactions it does have — same reasoning as Set Mood.

### Nod Or Shake Head

Answers with the head: a nod for yes, a shake for no, a tilt for "let me think." Layered over whatever the body is already doing, so it does not read as a puppet jerk.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiHeadResponseActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Nod Or Shake Head` |
| **Archetype action name** | `Nod Or Shake Head` |
| **Target requirement** | None |
| **Required peer** | `ConvaiBodyLanguageController` |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_response` | `HeadGestureKind` (`Nod`, `Shake`, `Tilt`) | `Nod` | Response to give when the character does not name one. The character can ask for `yes`, `no`, or `maybe` with the `response` parameter. |
| `_intensity` | `float` | `1` | How big the movement is, `0`–`1`. |

Stays open until the gesture finishes, so a sequence can nod then speak, in that order. If the head is still finishing a previous gesture, the executor retries for up to 1.5 seconds before failing with `ConvaiActionFailureReason.Busy`.

## Gesture pack (`Convai.Modules.BodyAnimation`)

`SDK/Modules/BodyAnimation/Executors/` — content-driven: both behaviors play clips authored in the character's Animation Set, so a character without that content cannot perform them.

### Play Gesture

Plays one of the character's gestures by name — a wave, a shrug, a bow — blending over the current posture and back out.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiPlayGestureActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Play Gesture` |
| **Archetype action name** | `Play Gesture` |
| **Target requirement** | None |
| **Required peer** | `ConvaiBodyAnimationController` |
| **Timeout** | 15s (archetype default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_defaultGesture` | `string` | Empty | Gesture to play when the character does not name one. Matched against the Animation Set's gesture names and aliases. |
| `_holdSeconds` | `float` | `8` | How long to hold a gesture that would otherwise continue indefinitely (a dance, a thinking pose). `0` holds until something else stops it. |

An unknown gesture name declines as `Unhandled`; the Animation Set's real gesture names are logged once at Detail tracing verbosity. Characters that use a plain Animator Controller instead of the Body Animation module want **Play Animator State** instead.

### Point At Target

Points at the thing the action names, choosing the arm from where the target actually is; the rest of the body keeps doing what it was doing underneath.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiPointAtActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Point At Target` |
| **Archetype action name** | `Point At` |
| **Target requirement** | Either |
| **Required peer** | `ConvaiBodyAnimationController` |
| **Timeout** | 15s (archetype default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_holdSeconds` | `float` | `3` | How long the point is held **at full extension** — the pause in the middle of the gesture only. |
| `_gestureSpeed` | `float` | `1` | How quickly the arm rises and lowers, as a multiple of the animation's own speed, `0.25`–`3`. Does not affect `_holdSeconds`. |
| `_release` | `PointingReleaseStyle` (`PlayTail`, `Blend`) | `PlayTail` | What happens when the hold ends. `PlayTail` lowers the arm through the rest of the animation clip; `Blend` drops the pose out instead, ending the gesture roughly as soon as the hold does. |

{% hint style="warning" %}
**`_holdSeconds` no longer means the length of the whole gesture.** It is only the pause at full extension — the arm's rise and fall are the animation clip's own timing and add roughly 2.5 seconds each way with the shipped pointing clips, so a `_holdSeconds` of `1` still produces a gesture around 6 seconds long. `_gestureSpeed` and `_release` are new in this release and control the rise/fall directly; both default to the prior behavior, so an existing scene's timing is unchanged until you adjust one of them. Set `_release` to `Blend` for the shortest possible point.
{% endhint %}

No pointing clips in the Animation Set declines as `Unhandled`. No resolved target declines the same way — pointing always needs a target.

## Movement pack (`Convai.Modules.BodyAnimation`)

`SDK/Modules/BodyAnimation/Executors/` — every behavior here needs a `ConvaiNavMeshLocomotion` peer, except **Turn To Face Target**, which needs no NavMesh.

### Walk To Target

Walks to the target, pathing around obstacles and stopping a comfortable distance short rather than walking into the object.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiWalkToActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Walk To Target` |
| **Archetype action name** | `Walk To` |
| **Target requirement** | Either |
| **Required peer** | `ConvaiNavMeshLocomotion` |
| **Timeout** | 45s (archetype default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_arriveDistance` | `float` | `1` | How far short of the target to stop, in metres. The character can override with the `arriveDistance` parameter. |

No baked NavMesh, or a target off the mesh, fails with `ConvaiActionFailureReason.PathBlocked` and names the destination. Needs a baked NavMesh.

### Lead Player To Target

Guides the player to a destination: walks ahead, pauses when the player falls behind, and resumes when they catch up.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiLeadPlayerActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Lead Player To Target` |
| **Archetype action name** | `Lead Player` |
| **Target requirement** | Either |
| **Required peer** | `ConvaiNavMeshLocomotion` |
| **Timeout** | 120s (archetype default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_arriveDistance` | `float` | `1.4` | How far short of the destination the character stops. |
| `_waitWhenFartherThan` | `float` | `4.5` | Pause the journey when the player is farther away than this. |
| `_resumeWhenCloserThan` | `float` | `2.8` | Resume the journey once the player returns within this distance. |
| `_maximumWaitSeconds` | `float` | `12` | Longest to wait before continuing to the destination without the player. |

No player in the scene fails with `ConvaiActionFailureReason.TargetMissing`. No path to the destination fails with `PathBlocked`.

### Turn To Face Target

Turns on the spot to face the target without walking toward it — most of the time "look at the customer" means this, not crossing the room. Needs no NavMesh.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiTurnToFaceActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Turn To Face Target` |
| **Archetype action name** | `Turn To Face` |
| **Target requirement** | Either |
| **Required peer** | `ConvaiBodyAnimationController` |
| **Timeout** | 10s (archetype default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_turnStyle` | `ConvaiTurnStyle` (`SteppingTurn`, `SmoothRotation`) | `SteppingTurn` | `SteppingTurn` plays the character's own turn animation; `SmoothRotation` rotates directly over `_smoothTurnSeconds` and needs no clips. |
| `_smoothTurnSeconds` | `float` | `0.5` | Duration of a `SmoothRotation` turn. Ignored by `SteppingTurn`. |
| `_toleranceDegrees` | `float` | `8` | How close to facing the target counts as done, `0`–`45`. |

`SteppingTurn` with no turn clips in the Animation Set declines as `Unhandled`, naming `SmoothRotation` as the alternative.

### Follow The Player

"Come with me." Keeps a comfortable distance, closing the gap when the player walks off and standing still when they stop.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiFollowPlayerActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Follow The Player` |
| **Archetype action name** | `Follow The Player` |
| **Target requirement** | None (the player is implied) |
| **Required peer** | `ConvaiNavMeshLocomotion` |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_mode` | `ConvaiFollowMode` (`Follow`, `Stop`) | `Follow` | Whether this call starts following or stops. The character can ask for either with the `mode` parameter (`follow` or `stop`). |
| `_followDistance` | `float` | `2.2` | Distance the character tries to keep from the player. |
| `_slack` | `float` | `0.8` | How far the player must move beyond `_followDistance` before the character closes the gap. |

{% hint style="info" %}
**Following has no natural end.** The action reports success as soon as the character starts following, and the following itself continues afterward — otherwise it would sit open until it timed out and block every later action. Send the action again with `mode: stop`, or disable the character, to end it. A following character still responds to other movement actions (Walk To Target, Return To Start): following stands down for the duration of any move it did not order, and resumes beside the player once that move ends.
{% endhint %}

No player found fails with `ConvaiActionFailureReason.TargetMissing`.

### Return To Start

Walks back to where the character started — or to a spot you choose — and optionally restores the original facing. The undo for everything else in this pack.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiReturnToStartActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Return To Start` |
| **Archetype action name** | `Return To Start` |
| **Target requirement** | None |
| **Required peer** | `ConvaiNavMeshLocomotion` |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_homeSpot` | `Transform` | `null` | Where "back" is. Leave empty to use wherever the character was standing when the scene started. |
| `_restoreFacing` | `bool` | `true` | Turn back to the original facing after arriving. |
| `_turnBackSeconds` | `float` | `0.6` | How long that final turn takes. |
| `_arriveDistance` | `float` | `0.2` | How close counts as home. |

The home position is recorded in `Awake`, before anything else on the character can move it. No path back fails with `PathBlocked`.

## Observation pack (`Convai.Runtime`)

`SDK/Runtime/Actions/Executors/` — the new pack in this release. Both behaviors return an answer through `ConvaiActionExecutionResult.Answered` and are authored with `AnswerDelivery = TellThePlayer` by default, so the character speaks the result unless you change the action's **When It Finishes** setting.

### Count Target Group

Counts the enabled members of a `ConvaiActionTargetGroup` and answers with the result — "how many crates are left."

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiCountTargetGroupActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Count Target Group` |
| **Archetype action name** | `Count Target Group` |
| **Target requirement** | Object |
| **Required target component** | `ConvaiActionTargetGroup`, on the resolved target object (not on the character) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_availableMembersOnly` | `bool` | `true` | Ignore disabled member components and inactive member objects when counting. |
| `_includeMemberNames` | `bool` | `true` | Include member names in the answer as well as the count. |
| `_memberLabel` | `string` | Empty | Optional plural label, e.g. `"crates"`. Leave empty to use the target group's own name. |

A resolved target with no `ConvaiActionTargetGroup` component, or an empty group, declines as `Unhandled` rather than reporting a misleading zero.

### Measure Distance

Measures ground-plane distance from the character to the target, or to the player when no target is named, and answers in plain terms — "about 3 metres away."

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiMeasureDistanceActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Measure Distance` |
| **Archetype action name** | `Measure Distance` |
| **Target requirement** | Either |
| **Required peer** | None |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_withinReachMetres` | `float` | `1.2` | Distances up to this value are described as "within reach." |
| `_aFewStepsMetres` | `float` | `3.5` | Distances up to this value are described as "a few steps away." |
| `_acrossAreaMetres` | `float` | `9` | Distances up to this value are described as "across the area." Beyond it: "a long way away." |
| `_includeMetres` | `bool` | `true` | Include the measured value in metres in the answer. |

No target and no player in the scene fails with `ConvaiActionFailureReason.TargetMissing`.

## Choosing the right executor

| Use case | Recommended executor |
| --- | --- |
| No-code hook into existing gameplay | Raise Unity Event |
| Pace a sequence, or pause between steps | Wait |
| Chain several behaviors as one action | Run In Order |
| Toggle a scene object's visibility | Show Or Hide Object |
| Character animates with its own Animator Controller | Play Animator State |
| Play a one-off sound with or without a target | Play Sound |
| Turn the character's gaze toward a target | Look At Target |
| Hold eye contact with the player on request | Watch The Player |
| Visibly inspect the surrounding area | Scan Environment |
| Shift the character's ongoing mood | Set Mood |
| A momentary emotional beat that passes | React |
| Answer yes, no, or "let me think" with the head | Nod Or Shake Head |
| Play a named gesture from the Animation Set | Play Gesture |
| Point at a named person, place, or object | Point At Target |
| Navigate to a target with pathfinding | Walk To Target |
| Guide the player somewhere | Lead Player To Target |
| Turn in place to face a target | Turn To Face Target |
| Accompany the player as they move | Follow The Player |
| Undo movement — walk back to the start | Return To Start |
| Count how many known objects are available | Count Target Group |
| Answer "how far away is that" | Measure Distance |
| Gameplay no shipped executor covers | [Write a custom action executor](writing-custom-executors.md) |

## Next steps

{% content-ref url="dispatcher-and-batch-policies.md" %}
[Dispatcher and batch policies](dispatcher-and-batch-policies.md)
{% endcontent-ref %}

{% content-ref url="writing-custom-executors.md" %}
[Write a custom action executor](writing-custom-executors.md)
{% endcontent-ref %}
