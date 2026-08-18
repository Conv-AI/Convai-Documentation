---
title: Scripted gaze
description: Direct a Convai character's gaze at a transform or point from code, and await the result to gate a follow-up action on it landing.
last_reviewed: "4.5.0"
---

Direct a character's gaze at a transform or a world-space point from code, and use the returned handle to know when the look has landed. Use this page when a cutscene beat, an action executor, or a UI event needs to control where a character looks, outside the automatic targeting the gaze policy already provides.

## Prerequisites

* `ConvaiGazeController` added to the character (`Convai/Embodiment/Gaze`).
* A reference to the character's `ConvaiGazeController`, resolved with `GetComponent<ConvaiGazeController>()` or a serialized field.

## Request a scripted gaze

Call `GazeAt` for a request that holds until released or its hold time elapses, or `GlanceAt` for a brief, one-line look. Both return a `GazeHandle` and never return `null` for a valid target.

```csharp
using Convai.Modules.Gaze.Components;
using UnityEngine;

public sealed class DisplayCaseCue : MonoBehaviour
{
    [SerializeField] private Transform displayCase;
    [SerializeField] private ConvaiGazeController gaze;

    private void OnTriggerEnter(Collider other)
    {
        // Hold the look for 2 seconds, allow a full-body turn if the case is off-axis.
        gaze.GazeAt(displayCase, new GazeOptions
        {
            HoldSeconds = 2f,
            Engagement = 1f,
            AllowBodyTurn = true
        });
    }
}
```

Use `GlanceAt` for a shorter, lower-priority look that never turns the body and resumes the policy target automatically:

```csharp
gaze.GlanceAt(displayCase, durationSeconds: 1.5f);
```

Scripted requests always outrank automatic targets. `GazeAt` requests outrank `GlanceAt` requests: any explicit `GazeAt` preempts a glance in progress.

## `GazeOptions` fields

| Field | Type | Default | Purpose |
|---|---|---|---|
| `Priority` | `int` | `0` | Priority among scripted requests (higher wins; recency breaks ties). |
| `HoldSeconds` | `float` | `0` | Hold duration in seconds from the request. Values `<= 0` hold until `GazeHandle.Release()` is called. |
| `Engagement` | `float` | `0` | Engagement override in `(0, 1]`. Values `<= 0` use the current dialogue state's engagement — pass an explicit value (for example `1`) when the gaze must land regardless of conversation state, since `Idle` defaults to `0`. |
| `AllowBodyTurn` | `bool` | `false` | Whether this request may trigger a full-body turn toward the target. |

`GlanceAt` builds its own `GazeOptions` internally: `HoldSeconds` from its `durationSeconds` parameter (default `1.2f`, clamped to at least `0.2f`), `Engagement` fixed at `1`, and `AllowBodyTurn` fixed at `false`.

## Await a handle in Unity

`GazeHandle.Settled` completes with `true` once gaze is aligned on the target, or `false` when the request ended before alignment. `GazeHandle.Completion` completes when the request ends — hold elapsed, released, or target lost. Await `Settled` before a follow-up action that depends on the character visibly looking first, such as a pick-up gesture.

```csharp
using System.Threading.Tasks;
using Convai.Modules.Gaze.Components;
using UnityEngine;

public sealed class LookThenReach : MonoBehaviour
{
    public async Task LookAtAndReachAsync(ConvaiGazeController gaze, Transform target)
    {
        GazeHandle handle = gaze.GazeAt(target, new GazeOptions { Engagement = 1f, AllowBodyTurn = true });
        if (handle == null) return;

        bool aligned = await handle.Settled;
        if (!aligned)
        {
            Debug.Log($"Gaze at '{handle.TargetName}' did not settle: {handle.Outcome}.");
            return;
        }

        // Aligned — safe to start a reach or pick-up animation here.
    }
}
```

{% hint style="warning" %}
`Settled` can complete `false` for a request that was deliberately not taken — see `GazeOutcome.HeldEyeContactInstead` below — not only for a genuine failure. Branch on `Outcome` rather than the boolean alone before treating a `false` result as an error.
{% endhint %}

Call `handle.Release()` to end a request early. `Release` is safe to call multiple times and from cancellation callbacks. Call `ConvaiGazeController.ReleaseAllScriptedGaze()` to end every scripted request on the character at once, for example when a cutscene aborts.

## `GazeOutcome` values

| Value | Integer | Meaning |
|---|---|---|
| `Taken` | `0` | The request is live, or it arrived on its target. Default until something says otherwise. |
| `Interrupted` | `1` | The request ended before gaze arrived — released, expired, superseded by a higher-priority look, or its target was destroyed. |
| `HeldEyeContactInstead` | `2` | The character deliberately held eye contact and the glance was folded into it instead of taken, because `LockBlocksGlances` is on. Nothing went wrong — the character chose the person over the thing. |

## How eye-contact locking changes scripted requests

`AllowScriptedOverridesDuringExactFocus` and `LockBlocksGlances`, both on `ConvaiGazeController`, decide whether a scripted request is honored while an eye-contact lock (`ConversationLock` or `AlwaysLock` `EyeContactMode`) is in force:

* While `FocusFidelity` is `Exact`, an explicit `GazeAt` request is rejected outright unless `AllowScriptedOverridesDuringExactFocus` is `true`. A rejected request returns a handle whose `Completion` is already finished and whose `Settled` resolves `false`.
* While `FocusFidelity` is `Social`, an explicit `GazeAt` request always preempts the lock.
* `GlanceAt` requests are absorbed while `LockBlocksGlances` is `true` (the default): the returned handle completes immediately with `Outcome` set to `HeldEyeContactInstead`, and gaze never leaves the player anchor. Set `LockBlocksGlances` to `false` to let glances play through the lock instead.

## Troubleshooting

### A `GazeAt` request never settles

**Symptom:** `handle.Settled` awaits and returns `false`.

**Cause:** the request was interrupted by a higher-priority scripted request, its target was destroyed, or `Exact` focus rejected it.

**Fix:** check `handle.Outcome` after `Settled` resolves to distinguish `Interrupted` from `HeldEyeContactInstead`, and raise `Priority` or set `AllowScriptedOverridesDuringExactFocus` if the request should win.

**Verify:** the follow-up action only runs once `Settled` resolves `true`.

## Next steps

{% content-ref url="targets-and-providers.md" %}
[Gaze targets and providers](targets-and-providers.md)
{% endcontent-ref %}

{% content-ref url="configure-eye-contact.md" %}
[Configure eye contact](configure-eye-contact.md)
{% endcontent-ref %}

{% content-ref url="scripting-reference.md" %}
[Gaze scripting reference](scripting-reference.md)
{% endcontent-ref %}
