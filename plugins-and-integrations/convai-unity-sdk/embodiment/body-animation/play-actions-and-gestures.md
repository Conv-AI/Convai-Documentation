---
title: Play actions and gestures
description: Play named actions, anchored actions, and pointing gestures on a Convai character from script, and read the handles each call returns.
last_reviewed: "4.5.0"
---

Play a named action or gesture, walk a character to an anchor and perform an action there, or point at a target — all from script, through `ConvaiBodyAnimationController` and the handle each call returns. Use this page once Convai Body Animation is running on a character and its animation set authors the actions or pointing directions you want to trigger.

***

## Prerequisites

* `ConvaiBodyAnimationController` added to the character, with an animation set assigned. See [Build an animation set](build-an-animation-set.md) for authoring actions and pointing directions.
* A reference to the controller, resolved with `GetComponent<ConvaiBodyAnimationController>()` on the character.

{% hint style="info" %}
`PlayAction`, `PlayActionAt`, and `PointAt` never return `null`. On failure — the runtime is not built yet, the action or gesture is unknown, or the request cannot be honored — each returns an already-completed, already-failed handle instead. Check `Failed` and `FailureReason` on the handle rather than null-checking it.
{% endhint %}

***

## Play a named action or gesture

Call `PlayAction` with the action's name or an alias — matching is case-insensitive and treats spaces, dashes, and underscores as equivalent.

```csharp
using Convai.Modules.BodyAnimation;
using Convai.Modules.BodyAnimation.Components;
using UnityEngine;

public sealed class WaveOnCue : MonoBehaviour
{
    [SerializeField] private ConvaiBodyAnimationController bodyAnimation;

    public async void PlayWave()
    {
        BodyAnimationActionHandle handle = bodyAnimation.PlayAction("wave",
            new ActionPlayOptions { HoldSeconds = 3f });

        if (handle.Failed)
        {
            Debug.Log($"Wave didn't play: {handle.FailureReason}");
            return;
        }

        bool completedNaturally = await handle.Completion; // false when interrupted
    }
}
```

`ActionPlayOptions` fields:

| Field | Type | Default meaning | Description |
|---|---|---|---|
| `SpeedMultiplier` | `float` | `<= 0` = entry default | Playback speed multiplier on top of the entry's authored speed. |
| `HoldSeconds` | `float` | `<= 0` = hold until stopped | For hold-until-stopped actions: automatically requests the stop after this many seconds of the main loop. |
| `FadeInSeconds` | `float` | `<= 0` = entry / config default | Layer blend-in override. |
| `FadeOutSeconds` | `float` | `<= 0` = entry / config default | Layer blend-out override. Also used by `StopActionImmediate`. |
| `WeightMultiplier` | `float` | `<= 0` = existing behavior | Action layer weight multiplier. |

`BodyAnimationActionHandle` (returned by `PlayAction`):

| Member | Description |
|---|---|
| `ActionName` | `string` — the requested name or alias. |
| `Failed` / `FailureReason` | Whether the request never started, and why. |
| `IsDone` | `true` once the action fully finished or was interrupted. |
| `Completion` | `Task<bool>` — resolves `true` when played to completion, `false` when interrupted. |
| `Stop()` | Requests a graceful stop; the entry's outro plays when authored. Safe to call repeatedly. |
| `StopImmediate(float blendOutSeconds = -1f)` | Immediately stops and cross-dissolves out over `blendOutSeconds` (`<= 0` = the action's resolved fade-out), skipping the remaining chain or outro. |

Stop or interrupt the currently playing action from the controller directly with `StopAction()` (graceful, outro plays) or `StopActionImmediate(float blendOutSeconds = -1f)` (immediate cross-dissolve). `CurrentActionName` reads the name of the action playing now, empty when none.

Backend-triggered gestures resolve through the same name/alias matching as `PlayAction`, so an action named `"pick_up"` in Convai's response triggers an entry named `"Pick Up"` or an alias `"pick-up"` with no extra wiring.

***

## Play an anchored action

`PlayActionAt` walks the character to an anchor, root-aligns to its pose, then plays the named action — the "sit on the bench" / pick-up / use-prop flow.

```csharp
using Convai.Modules.BodyAnimation;
using Convai.Modules.BodyAnimation.Components;
using UnityEngine;

public sealed class SitOnBench : MonoBehaviour
{
    [SerializeField] private ConvaiBodyAnimationController bodyAnimation;
    [SerializeField] private Transform benchAnchor;

    public async void SitDown()
    {
        PlayActionAtHandle handle = bodyAnimation.PlayActionAt(benchAnchor, "sit");
        bool completedNaturally = await handle.Completion; // false when canceled/refused
    }
}
```

| Method | Description |
|---|---|
| `PlayActionAt(Transform anchor, string actionNameOrAlias)` | Walk to `anchor`, align, and play. |
| `PlayActionAt(Transform anchor, string actionNameOrAlias, ActionAnchorOptions anchorOptions, ActionPlayOptions playOptions = default)` | Same, with explicit approach/alignment tuning and action playback tweaks. The explicit `anchorOptions` overrides the action entry's own authored defaults. |

`ActionAnchorOptions` has no public constructor for building one from script with custom values — its fields are set only through the Inspector, on the action entry's **Anchor Options** field in the animation set. Pass an existing authored instance to the overload only to reuse another entry's tuning; otherwise call the two-argument overload and let the entry's own authored defaults apply.

The anchor's height is ignored for alignment — only its XZ position and yaw matter, so place anchors at the character's intended stand point, not at seat or prop height.

`PlayActionAtHandle` (returned by `PlayActionAt`):

| Member | Description |
|---|---|
| `ActionName` | `string` — the requested action name. |
| `Phase` | `PlayActionAtPhase` — the request's current stage. |
| `Failed` / `FailureReason` | Whether the request never started, and why. |
| `IsDone` | `true` once the request finished or was canceled. |
| `Completion` | `Task<bool>` — resolves `true` when the action played to completion, `false` when canceled. |
| `Cancel()` | Cancels wherever the request currently is: stops locomotion during `Approaching`, freezes the alignment lerp during `Aligning`, or gracefully stops the action during `PlayingAction`. Idempotent. |

***

## Point at a target or position

`PointAt` raises the arm toward a world position or a moving transform, holds at the apex, then lowers.

```csharp
using Convai.Modules.BodyAnimation;
using Convai.Modules.BodyAnimation.Components;
using UnityEngine;

public sealed class PointAtProp : MonoBehaviour
{
    [SerializeField] private ConvaiBodyAnimationController bodyAnimation;
    [SerializeField] private Transform target;

    public async void Point()
    {
        BodyAnimationPointingHandle handle = bodyAnimation.PointAt(target, holdSeconds: 3f);
        await handle.Completion;
    }
}
```

| Overload | Description |
|---|---|
| `PointAt(Vector3 worldPosition, float holdSeconds = -1f)` | Points at a fixed world position. |
| `PointAt(Transform target, float holdSeconds = -1f)` | Points at a (moving) transform, re-aiming while the hold lasts. |
| `PointAt(Transform target, in PointingPlayOptions options)` | Same, with playback tweaks: speed, blend-in/out durations, and how an elapsed hold auto-releases. |

`holdSeconds < 0` (or `PointingPlayOptions.HoldSeconds <= 0`) holds until `StopPointing`/`Release()` is called.

{% hint style="warning" %}
**`HoldSeconds` changed in SDK 4.5.0.** It has always meant only the pause at the apex of the point, not the total gesture duration — the raise and lower belong to the animation clip. Before 4.5.0 there was no way to shorten that raise/lower, so a one-second hold on a five-second apex clip still produced a roughly six-second point. `PointingPlayOptions.Speed` now multiplies the raise and fall, and `ReleaseStyle` set to `Blend` drops the pose out when the hold ends instead of playing the lower-arm tail. Both default to the pre-4.5.0 behavior, so an existing scene is unaffected; a point of about a second is `Speed = 1.5f` with `ReleaseStyle = PointingReleaseStyle.Blend`.
{% endhint %}

`PointingPlayOptions` fields:

| Field | Type | Default meaning | Description |
|---|---|---|---|
| `Speed` | `float` | `<= 0` = native (`1`) | Raise/lower speed multiplier. The hold itself is unaffected. |
| `HoldSeconds` | `float` | `<= 0` = hold until released | Seconds to hold at the apex. |
| `BlendInSeconds` | `float` | `<= 0` = config `PointingFadeSeconds` | Layer blend-in seconds. |
| `BlendOutSeconds` | `float` | `<= 0` = config `PointingFadeSeconds` | Layer blend-out seconds. |
| `ReleaseStyle` | `PointingReleaseStyle` | `PlayTail` | What an elapsed `HoldSeconds` auto-release does: play the lower-arm tail (`PlayTail`, default) or cross-dissolve the pose out immediately (`Blend`). |
| `WeightMultiplier` | `float` | `<= 0` = existing behavior | Pointing layer weight multiplier. |

`BodyAnimationPointingHandle` (returned by every `PointAt` overload):

| Member | Description |
|---|---|
| `Failed` / `FailureReason` | Whether the request never started, and why. |
| `IsDone` | `true` once the point gesture fully finished (arm lowered). |
| `Completion` | `Task` — resolves once the gesture is fully finished. |
| `Release()` | Ends the hold now; the lower-arm tail plays before completion. |
| `ReleaseImmediate(float blendOutSeconds = -1f)` | Stops now and cross-dissolves the pose out, skipping the lower-arm tail. |
| `SetSpeed(float speed)` | Live-adjusts the raise/lower speed of the running gesture. No-op while holding. |

Stop the current pointing hold from the controller directly with `StopPointing()` (graceful, tail plays) or `StopPointingImmediate(float blendOutSeconds = -1f)` (immediate cross-dissolve).

***

## Face a direction and set the conversation anchor

`FaceTowards(Vector3 worldDirection, string reason = "FaceTowards")` rotates the character to face a direction with the animated turn-in-place family — no `NavMeshAgent` required. It returns `false` when the request cannot be honored (feature disabled, clips missing, locomotion busy).

```csharp
bodyAnimation.FaceTowards(playerTransform.position - character.position, "greeting turn");
```

`SetConversationAnchor(Transform anchor)` overrides the transform social spacing, proximity expressiveness, and ambient suppression treat as "the person this character is talking to" — the default resolution ladder ends at `Camera.main`, which is the wrong anchor for an XR rig, a second local player, or a cutscene camera with no `MainCamera` tag. `ClearConversationAnchor()` reverts to the default ladder.

***

## Troubleshooting

### A handle's `Failed` is `true`

**Symptom:** the call returns immediately and nothing plays.

**Cause:** `FailureReason` names it — common reasons are `"runtime not built"` (the graph is not ready yet), `"unknown action"` (no matching name or alias in the animation set), `"an active non-interruptible action is still playing"`, `"no locomotion"` (`PlayActionAt` with no `ConvaiNavMeshLocomotion` on the character), or `"set has no pointing clips"`.

**Fix:** for `"runtime not built"`, subscribe to `ConvaiBodyAnimationController.RuntimeReady` and call from the handler instead of `Start()`/`Awake()` — a call made too early is also recorded in a single deferred slot and replayed automatically, but the event guarantees the call lands. For the other reasons, check the animation set's authored actions and pointing directions, or add `ConvaiNavMeshLocomotion`.

**Verify:** `handle.Failed` is `false` and `Completion` resolves once the gesture plays.

***

## Next steps

{% content-ref url="configure-locomotion.md" %}
[Configure locomotion](configure-locomotion.md)
{% endcontent-ref %}

{% content-ref url="config-reference.md" %}
[Body animation config reference](config-reference.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Body animation scripting reference](scripting-reference.md)
{% endcontent-ref %}
