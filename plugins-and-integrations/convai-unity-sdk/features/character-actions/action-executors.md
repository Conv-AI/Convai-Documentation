---
title: Action executors
description: Reference for all 21 built-in action executor components, grouped by pack, with every Inspector field, default, and required peer.
last_reviewed: "5.0.0-pre.1"
---

The Convai SDK ships 21 action executor components in six packs. Each defines a preset in the Actions Editor's **+ Add Action ▾** catalog. The preset fills in the action name, description, target requirement, and parameters. Check the requirements below for any scene targets, peer components, clips, or other assets the executor needs.

All 21 derive from `ConvaiActionExecutorBase` (`Convai.Runtime.Actions`). Executors that derive from `ConvaiCharacterActionExecutor<TPeer>` also expose a **Character Component** field for the peer component, such as `ConvaiGazeController`. An explicit assignment takes precedence. If the field is empty, the executor checks its own GameObject and its parents first, then its children, including inactive objects.

## Parameters and catalog defaults

The catalog adds the declared parameters. To let Convai supply an optional override, add it to the action's **Advanced** parameter list. If you submit a command from code with `ConvaiActionDispatcher.EnqueueActions`, you can set `ConvaiActionCommand.Parameters` directly. The dispatcher preserves your values when it parses the command and checks the action definition, executor, and required target before execution. See [Dispatcher and batch policies](dispatcher-and-batch-policies.md).

Unless marked otherwise, a catalog preset uses the dispatcher's default step timeout and failure policy, and the character's answer-delivery setting.

| Executor | Declared parameters | Optional overrides to author |
|---|---|---|
| Raise Unity Event | None | None |
| Wait | `seconds` (Number) | None |
| Run In Order | None | Any override used by a child executor |
| Show Or Hide Object | `mode` (Choice: `show`, `hide`, `toggle`) | None |
| Play Animator State | None | None |
| Play Sound | `volume` (Number) | None |
| Look At Target | None | `mode` (String, `glance` or `sustained`), `holdSeconds` (Number), `engagement` (Number) |
| Watch The Player | `mode` (Choice: `watch`, `stop`) | `engagement` (Number) |
| Scan Environment | None | `duration` (Number) |
| Set Mood | `mood` (Choice, Emotion Profile label), `intensity` (Number) | `transition` (Number) |
| React | `reaction` (Choice, Emotion Profile label), `intensity` (Number) | `holdSeconds` (Number) |
| Nod Or Shake Head | `response` (Choice: `yes`, `no`, `maybe`), `intensity` (Number) | None |
| Play Gesture | `gesture` (String) | `duration` (Number) |
| Point At Target | None | `duration` (Number) |
| Walk To Target | None | `arriveDistance` (Number) |
| Lead Player To Target | None | `arriveDistance` (Number) |
| Turn To Face Target | None | None |
| Follow The Player | `mode` (Choice: `follow`, `stop`) | None |
| Return To Start | None | None |
| Count Target Group | None | None |
| Measure Distance | `target` (Auto, optional) | None |

Use the listed **Choice** values in authoring. When you populate the parameter dictionary from a script, the executors also accept these aliases.

| Action | Choice aliases |
|---|---|
| Show Or Hide Object | `show` (`activate`, `enable`, `on`), `hide` (`deactivate`, `disable`, `off`), `toggle` (`switch`, `flip`) |
| Watch The Player | `watch` (`start`, `look`), `stop` (`stopwatching`, `stop_watching`, `release`, `away`) |
| Nod Or Shake Head | `yes` (`nod`, `agree`, `affirm`, `ok`), `no` (`shake`, `disagree`, `refuse`, `deny`), `maybe` (`tilt`, `think`, `consider`, `unsure`) |
| Follow The Player | `follow` (`start`, `come`, `accompany`), `stop` (`stay`, `wait`, `halt`, `stopfollowing`, `stop_following`) |

## Object groups and standing positions

A `ConvaiLogicalObjectGroup` names several physical objects as one target. Gaze, pointing, facing, distance, and target-audio lookup use a nearby active member. Show Or Hide operates on all stored physical members, including hidden ones, and keeps the logical root active. Walk To and Lead Player look for a reachable destination across members.

`ConvaiActionTargetGroup`, used by Count Target Group, is a different authored collection of action targets. See [Object groups and standing positions](../scene-metadata/group-objects-and-standing-positions.md) for logical groups and `ConvaiObjectMovementPoints`.

## Flow & Utility pack (`Convai.Runtime`)

These executors live in `SDK/Runtime/Actions/Executors/` and require no optional Convai module.

### Raise Unity Event

Invokes the callbacks wired to its Unity event and reports success when they return. Use it to run existing scene logic, such as opening a door, starting a Timeline, or awarding a point.

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

An unwired event still reports success at runtime. The Actions Editor flags it during authoring. Write a custom executor when the action needs to read parameters, take time, be cancelled, or report why it could not run.

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

Stops at the first step that does not succeed and includes its position in the result. An empty entry, a component that does not implement `IConvaiActionExecutor`, or a reference to the sequence itself fails with `ConvaiActionFailureReason.InvalidState`. A sequence whose steps all succeed returns a single success result without forwarding individual observation answers.

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

Asking for a state the object is already in succeeds. No resolved target or a logical group without stored physical members returns `Unhandled`. Show and hide change all members. Toggle hides all members if any is currently visible, or shows all if none are visible.

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

**Binding row fields.** Each row is configured in the Inspector; the row type is internal to the SDK, so a script cannot construct one.

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `ActionName` | `string` | — | The action name to answer, matched case-insensitively. |
| `TriggerName` | `string` | — | The Animator Trigger parameter to set when that action runs. |
| `WaitForStateTag` | `string` | Empty | Optional. Tag the Animator state with the same word to wait for it before the action finishes. Leave empty to finish as soon as the trigger is set. |
| `NormalizedExitTime` | `float` | `0.95` | How far through the tagged state counts as finished (`0`–`1`). Only used when `WaitForStateTag` is set. |

An action name with no matching row returns `Unhandled`. If the executor finds a `ConvaiBodyAnimationController` in its parent hierarchy, the message recommends **Play Gesture**. With a matching row and **Wait For State Tag** set, the executor returns `Timeout` if the tagged state does not reach **Normalized Exit Time** within 10 seconds.

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

An assigned source takes precedence. Automatic lookup searches the physical target and its children, skipping sources with `ConvaiAudioOutput`. An explicitly assigned voice source plays the sound with speech and logs a warning. The executor ignores a source's clip marked `DontSave` and uses an explicitly assigned clip when available. Cancellation stops a non-voice source only while the executor is waiting for playback. No usable source returns `Unhandled`. No usable clip fails with `InvalidState`.

## Attention pack (`Convai.Modules.Gaze`)

`SDK/Modules/Gaze/Executors/` — every behavior here needs a `ConvaiGazeController` peer.

### Look At Target

Turns the character's attention to the target. Sustained gaze can turn the body if the head cannot reach the target. The action finishes once the gaze settles, so the hold can continue while later steps run.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiLookAtActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Look At Target` |
| **Archetype action name** | `Look At` |
| **Target requirement** | Either |
| **Required peer** | `ConvaiGazeController` |
| **Timeout** | 10s (archetype default) |
| **Failure policy** | `ContinueBatch` (catalog default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_mode` | `ConvaiGazeLookMode` (`Glance`, `Sustained`) | `Sustained` | Glance is a quick look and back; Sustained is a committed look the character holds, turning the body if needed. The character can ask for either with the `mode` parameter. |
| `_holdSeconds` | `float` | `2.5` | How long to keep looking, in seconds. A sustained hold of `0` lasts until another gaze request takes over. A glance of `0` uses 1.2 seconds. |
| `_engagement` | `float` | `1` | How intently to look in sustained mode, `0`–`1`. |

A glance blocked by conversational eye contact returns `Unhandled`. The `mode` override accepts `glance` (also `quick` or `brief`) and `sustained` (also `hold`, `stare`, or `watch`). It uses the Inspector mode for an empty or unrecognized value.

A logical group uses its nearest active physical member. A group without active physical members declines instead of acting on the generated root.

### Watch The Player

Starts a standing request to watch the player and completes once the gaze settles. Send the action with `mode: stop` or disable the executor to release the watch. A higher-priority gaze request can temporarily take over.

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

If the gaze controller cannot find a player anchor, starting the watch fails with `ConvaiActionFailureReason.TargetMissing`.

### Scan Environment

Looks at several points in the surrounding environment. It prefers authored gaze targets and World Objects with **Gaze Enabled** in range, and generates evenly spaced points for any gaps.

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiScanEnvironmentActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Scan Environment` |
| **Archetype action name** | `Scan Environment` |
| **Target requirement** | None |
| **Required peer** | `ConvaiGazeController` |
| **Timeout** | 15s (archetype default) |
| **Failure policy** | `ContinueBatch` (catalog default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_durationSeconds` | `float` | `3.5` | Total scan duration in seconds, at least `0.5`. The character can override it with the `duration` parameter. |
| `_stopCount` | `int` | `4` | Number of distinct points where the gaze pauses, `2`–`8`. |
| `_arcDegrees` | `float` | `150` | Horizontal field covered, centred on the character's forward direction, `20`–`320`. |
| `_allowBodyTurn` | `bool` | `false` | Whether wide scan points may turn the body as well as the head and eyes. |
| `_searchRadius` | `float` | `7` | Radius for scene candidates. `0` uses generated points only. |
| `_includeColliders` | `bool` | `false` | Also consider nearby non-trigger physics colliders. |
| `_targetLayers` | `LayerMask` | Everything | Layers to query when **Include Colliders** is enabled. |
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
| `_transitionSeconds` | `float` | `1.5` | How long the change takes, in seconds. The `transition` override accepts `0` or higher. |

The mood must match a label supported by the character's Emotion Profile. An unknown label fails and lists available labels. If the command and **Default Mood** are both empty, the executor returns `Unhandled`.

### React

Plays a temporary emotion over the character's current mood. The reaction fades after the hold. Cancelling it lets the reaction begin fading immediately.

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
| `_holdSeconds` | `float` | `1.5` | How long the reaction is held, in seconds. The `holdSeconds` override is clamped to at least `0.1`. |

The reaction must match a label supported by the character's Emotion Profile. An unknown label fails and lists available labels. If the command and **Default Reaction** are both empty, the executor returns `Unhandled`.

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

`SDK/Modules/BodyAnimation/Executors/` — both executors need a `ConvaiBodyAnimationController` and matching clips in its active Animation Set. The set can come from the character's Body Animation Profile.

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
| **Failure policy** | `ContinueBatch` (catalog default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_defaultGesture` | `string` | Empty | Gesture to play when the character does not name one. Matched against the Animation Set's gesture names and aliases. |
| `_holdSeconds` | `float` | `8` | How long to hold a gesture that can play indefinitely. The `duration` parameter overrides this value in seconds. `0` leaves the gesture active until it is stopped. |

Gesture resolution uses the supplied `gesture` value first. A declared but omitted `gesture` parameter declines rather than silently substituting a default. Otherwise it uses **Default Gesture**, then the action name. In 5.0, an unknown gesture declines with a message naming the source of the requested name, the Animation Set, and up to eight available gesture names. The Body Animation authoring checks also flag mismatches before Play mode. Characters that use a plain Animator Controller instead of the Body Animation module want **Play Animator State** instead.

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
| **Failure policy** | `ContinueBatch` (catalog default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_holdSeconds` | `float` | `3` | How long the point is held at full extension. The `duration` override sets this hold in seconds, with a minimum of `0.1`. |
| `_gestureSpeed` | `float` | `1` | How quickly the arm rises and lowers, as a multiple of the animation's own speed, `0.25`–`3`. Does not affect `_holdSeconds`. |
| `_release` | `PointingReleaseStyle` (`PlayTail`, `Blend`) | `PlayTail` | What happens when the hold ends. `PlayTail` lowers the arm through the rest of the animation clip; `Blend` drops the pose out instead, ending the gesture roughly as soon as the hold does. |

{% hint style="warning" %}
The animation clip adds time on either side of the hold. **Gesture Speed** changes the clip speed and **Blend** releases the pose without playing the clip's lowering motion.
{% endhint %}

No pointing clips in the Animation Set declines as `Unhandled`. No resolved target declines the same way — pointing always needs a target.

A logical group uses its nearest active physical member. A group without active physical members declines instead of acting on the generated root.

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

Needs a baked NavMesh. With a usable agent on the NavMesh, Walk To evaluates complete paths across logical members, preferring usable standing points per member and falling back to normal projected destinations. It picks the shortest complete path. An exact selected standing point supplies position and facing and ignores `arriveDistance`. An empty group declines with `This object group has no active physical members.` No complete path to any candidate fails with `PathBlocked`.

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
| `_arriveDistance` | `float` | `1.4` | How far short of the destination the character stops, in metres. The `arriveDistance` override accepts `0` or higher. An exact standing point takes precedence. |
| `_waitWhenFartherThan` | `float` | `4.5` | Pause the journey when the player is farther away than this. |
| `_resumeWhenCloserThan` | `float` | `2.8` | Resume the journey once the player returns within this distance. |
| `_maximumWaitSeconds` | `float` | `12` | Longest to wait before continuing to the destination without the player. |

Leading requires a destination and a baked NavMesh. If the player cannot be found, the action fails with `ConvaiActionFailureReason.TargetMissing`. A destination with no complete path fails with `PathBlocked`.

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
| **Failure policy** | `ContinueBatch` (catalog default) |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_turnStyle` | `ConvaiTurnStyle` (`SteppingTurn`, `SmoothRotation`) | `SteppingTurn` | `SteppingTurn` plays the character's own turn animation; `SmoothRotation` rotates directly over `_smoothTurnSeconds` and needs no clips. |
| `_smoothTurnSeconds` | `float` | `0.5` | Duration of a `SmoothRotation` turn, at least `0.05` seconds. `SteppingTurn` uses the turn animation. |
| `_toleranceDegrees` | `float` | `8` | How close to facing the target counts as done, `0`–`45`. |

`SteppingTurn` with no turn clips in the Animation Set declines as `Unhandled`, naming `SmoothRotation` as the alternative.

A logical group uses its nearest active physical member. A group without active physical members declines instead of acting on the generated root.

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

Walks back to where the character started or to a home spot you assign, then optionally turns to face the home direction.

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
| `_homeSpot` | `Transform` | `null` | Transform whose position and rotation define home. Leave empty to use the character's starting transform. |
| `_restoreFacing` | `bool` | `true` | Face the home direction after arriving. |
| `_turnStyle` | `ConvaiTurnStyle` (`SteppingTurn`, `SmoothRotation`) | `SmoothRotation` | Use direct rotation or try the Body Animation controller's turn clips. Smooth rotation finishes the turn if an animated turn is unavailable or falls short. |
| `_turnBackSeconds` | `float` | `0.6` | Duration of a smooth turn, at least `0.05` seconds. |
| `_arriveDistance` | `float` | `0.2` | Distance in metres at which the character counts as already home when the action starts. |

The executor records the character's starting position and rotation in `Awake`. The action fails with `PathBlocked` if there is no path home.

## Observation pack (`Convai.Runtime`)

`SDK/Runtime/Actions/Executors/` holds the observation executors. Both behaviors return an answer through `ConvaiActionExecutionResult.Answered` and are authored with `AnswerDelivery = TellThePlayer` by default, requesting that the optional [Action Feedback Relay](action-feedback.md) submit the result to tell the player.

### Count Target Group

Counts members of a `ConvaiActionTargetGroup` and answers with the result. By default it counts only active, enabled members.

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

A target without `ConvaiActionTargetGroup` or a group with an empty member list returns `Unhandled`. A populated group can report zero available members if none are active and enabled.

### Measure Distance

Measures ground-plane distance from the character to the target, or to the player when no target is named, and answers in plain terms — "about 3 metres away."

| Attribute | Value |
| --- | --- |
| **Class** | `ConvaiMeasureDistanceActionExecutor` |
| **Menu path** | `Add Component → Convai → Actions → Measure Distance` |
| **Archetype action name** | `Measure Distance` |
| **Target requirement** | None (**No target** in the Actions Editor) |
| **Required peer** | None |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_withinReachMetres` | `float` | `1.2` | Distances up to this value are described as "within reach." |
| `_aFewStepsMetres` | `float` | `3.5` | Distances up to this value are described as "a few steps away." |
| `_acrossAreaMetres` | `float` | `9` | Distances up to this value are described as "across the area." Beyond it: "a long way away." |
| `_includeMetres` | `bool` | `true` | Include the measured value in metres in the answer. |

Keep the catalog's **No target** setting and use its optional `target` parameter to name an object or character. The executor checks that parameter first, then the command target. It measures to the player when neither names a target. A named target without a physical position, or a player fallback with no player, fails with `ConvaiActionFailureReason.TargetMissing`.

A logical group uses its nearest active physical member. A group without active physical members declines instead of acting on the generated root.

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
