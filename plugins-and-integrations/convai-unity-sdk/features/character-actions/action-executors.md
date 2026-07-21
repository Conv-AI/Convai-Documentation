---
title: Action executors
description: Reference for all seven action executor components — look-at, event, NavMesh movement, animation trigger, and compound pickup/placement executors.
last_reviewed: "4.4.0"
---

Executors are the components that perform in-scene behavior when the dispatcher runs an action step. Seven executor components ship with the Convai SDK. This page documents every Inspector field and explains when to use each executor.

### LookAtTargetActionExecutor

Smoothly rotates the NPC to face a resolved target over a configurable duration. Uses `Quaternion.Slerp` and respects cancellation.

| Attribute | Value |
| --- | --- |
| **Menu path** | `Add Component → Convai → Actions → Look At Target Action Executor` |
| **Namespace** | `Convai.Runtime.Actions` |
| **Target required** | Yes — returns `Unhandled` if no target is resolved |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_rotateRoot` | `Transform` | `null` | The transform to rotate. If unassigned, uses the component's own `transform`. |
| `_duration` | `float` | `0.5` | Seconds to complete the rotation. `0` snaps immediately. |

**Behavior:** The executor interpolates from the current rotation toward the target's position over `_duration` seconds. If the root or target is destroyed mid-execution, it returns `Failed`.

### UnityEventActionExecutor

Fires a `UnityEvent` and immediately returns `Succeeded`. No target resolution is required. Use this to connect any backend action to Inspector-wired callbacks without writing code — toggle doors, play sounds, open UI panels.

| Attribute | Value |
| --- | --- |
| **Menu path** | `Add Component → Convai → Actions → Unity Event Action Executor` |
| **Namespace** | `Convai.Runtime.Actions` |
| **Target required** | No |

**Inspector fields:**

| Field | Type | Description |
| --- | --- | --- |
| `_onExecute` | `UnityEvent` | Invoked each time the action step runs. Wire any number of callbacks in the Inspector. |

{% hint style="danger" %}
**`TransformMoveToActionExecutor` is for prototyping only.** It teleports the character instantly with no animation or pathfinding. Replace it with `NavMeshMoveToActionExecutor` or a custom executor before shipping to users.
{% endhint %}

### TransformMoveToActionExecutor

Immediately snaps the NPC's transform to the resolved target's position plus an optional offset. Synchronous — completes in one frame.

| Attribute | Value |
| --- | --- |
| **Menu path** | `Add Component → Convai → Samples → Transform Move To Action Executor` |
| **Namespace** | `Convai.Sample.Behaviors` |
| **Target required** | Yes — returns `Failed` if no target is resolved |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_moveRoot` | `Transform` | `null` | The transform to move. If unassigned, moves the component's own `transform`. |
| `_offset` | `Vector3` | `(0, 0, 0)` | World-space offset applied to the target position. Use to stop slightly in front of the target. |

### NavMeshMoveToActionExecutor

Drives a `NavMeshAgent` to the resolved target's position and waits until the agent reaches stopping distance. The action step stays active until arrival, which means the dispatcher holds the next step until navigation completes.

| Attribute | Value |
| --- | --- |
| **Menu path** | `Add Component → Convai → Samples → NavMesh Move To Action Executor` |
| **Namespace** | `Convai.Sample.Behaviors` |
| **Target required** | Yes — returns `Failed` if no target is resolved |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_agent` | `NavMeshAgent` | Auto-resolved | The `NavMeshAgent` to drive. If unassigned, resolved from the same `GameObject` on `Awake`. |
| `_stoppingDistance` | `float` | `0.5` | Distance in world units at which the agent is considered to have arrived. |

{% hint style="warning" %}
The scene must have a baked NavMesh before this executor can navigate. Open **Window → AI → Navigation** and bake before entering Play mode. The executor returns `Failed` immediately if the agent is disabled, is not on a NavMesh, or `SetDestination` fails — it does not wait for `TimeoutSeconds` to expire in these cases.
{% endhint %}

### AnimatorTriggerActionExecutor

Maps backend action names to Animator trigger parameters via a configurable binding list. Fires the trigger and immediately returns `Succeeded` — it does not wait for the animation to finish.

| Attribute | Value |
| --- | --- |
| **Menu path** | `Add Component → Convai → Samples → Animator Trigger Action Executor` |
| **Namespace** | `Convai.Sample.Behaviors` |
| **Target required** | No |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_animator` | `Animator` | Auto-resolved | The `Animator` to drive. If unassigned, resolved from the same `GameObject` on `Awake`. |
| `_bindings` | `List<AnimatorTriggerActionBinding>` | Empty | Maps action names to trigger names. Each entry has two string fields (see below). |

**AnimatorTriggerActionBinding fields:**

| Field | Type | Description |
| --- | --- | --- |
| `ActionName` | `string` | The action name to match (case-insensitive). Must match an entry in `ConvaiActionConfigSource`'s Action Definitions. |
| `TriggerName` | `string` | The Animator trigger parameter to fire when the action is matched. Must match the exact trigger name in the Animator Controller. |

**Example binding list:**

| ActionName | TriggerName |
| --- | --- |
| `Wave` | `TriggerWave` |
| `Salute` | `TriggerSalute` |
| `Point At` | `TriggerPoint` |

If no binding matches the incoming action name, the executor returns `Failed` with message `No binding for '<action name>'`. If no `Animator` was resolved, it returns `Failed` with message `Animator not assigned` instead.

### PickUpActionExecutor

Compound executor that chains three behaviors: navigate to the target → fire an animation trigger → wait for the animation → attach the object to a hand transform. The step stays active until all three phases complete.

| Attribute | Value |
| --- | --- |
| **Menu path** | `Add Component → Convai → Samples → Pick Up Action Executor` |
| **Namespace** | `Convai.Sample.Behaviors` |
| **Target required** | Yes — returns `Failed` if no target is resolved |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_mover` | `NavMeshMoveToActionExecutor` | Required | Drives navigation to the target. Must be assigned — returns `Failed` if null. |
| `_animator` | `Animator` | `null` | The Animator to drive. Optional — skipped if null or if `_pickUpTrigger` is empty. |
| `_pickUpTrigger` | `string` | `"PickUp"` | The Animator trigger parameter to fire after arriving at the target. |
| `_attachPoint` | `Transform` | `null` | The transform the picked-up object is reparented to (e.g., hand bone). If a `HeldObjectActionState` is present and has no attach point set, this value is assigned to it; otherwise the target reparents to `_attachPoint` directly. Optional — object is not reparented if null and no `HeldObjectActionState` is present. |
| `_animationDuration` | `float` | `1.0` | Seconds to wait after firing the animation trigger before reparenting the object. Skipped when `0` or less. |

**Execution sequence:**

1. If no target is resolved, returns `Failed` with message `No target resolved`.
2. If a `HeldObjectActionState` component is present on the same `GameObject`, checks whether it is already holding an object: returns `Succeeded` immediately if it already holds the target, or `Failed` if it holds a different object.
3. `NavMeshMoveToActionExecutor.ExecuteAsync` navigates to the target. If it does not succeed, `PickUpActionExecutor` returns that result immediately.
4. If `_animator` is assigned and `_pickUpTrigger` is not empty, `_animator.SetTrigger(_pickUpTrigger)` is called.
5. Waits `_animationDuration` seconds (cancellable), skipped when `_animationDuration` is `0` or less.
6. Attaches the target: if a `HeldObjectActionState` is present, `HeldObjectActionState.TryAttach` reparents it (using `_attachPoint` to set the state's attach point first, when the state has none). Otherwise the target reparents directly to `_attachPoint` at local position/rotation zero, skipped if `_attachPoint` is null.
7. Returns `Succeeded`.

`PickUpActionExecutor` calls into `NavMeshMoveToActionExecutor` directly via `ExecuteAsync`. Both components should be on the same `GameObject` — `_mover` is a plain Inspector reference, not resolved automatically — and a baked NavMesh must be present in the scene. Add an optional `HeldObjectActionState` component (`Add Component → Convai → Samples → Held Object Action State`) to the same `GameObject` to track the currently held object across pick-up and put-down actions and stop the NPC from picking up a second object while one is already held.

### PutOnActionExecutor

Places one resolved target object on another. Unlike the other executors, it does not resolve a single primary target — it binds two named parameters from the backend command, `Item` and `Container`, each resolved to a `ConvaiResolvedActionTarget`.

| Attribute | Value |
| --- | --- |
| **Menu path** | `Add Component → Convai → Samples → Put On Action Executor` |
| **Namespace** | `Convai.Sample.Behaviors` |
| **Target required** | No single target — resolves `Item` and `Container` parameters instead |

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `_placementOffset` | `Vector3` | `(0, 0.5, 0)` | World-space offset added to the container's position when placing the item. |

If `Item` or `Container` does not resolve to a `GameObject`, the executor returns `Failed` with message `Item was not resolved.` or `Container was not resolved.` respectively. Otherwise it clears the item from any `HeldObjectActionState` on the same `GameObject` (if present), moves the item's transform to the container's position plus `_placementOffset`, and returns `Succeeded`.

## Choosing the right executor

| Use case | Recommended executor |
| --- | --- |
| NPC faces a target smoothly | `LookAtTargetActionExecutor` |
| Any no-target action wired to gameplay callbacks | `UnityEventActionExecutor` |
| Rapid prototyping without NavMesh | `TransformMoveToActionExecutor` |
| Production NPC movement with pathfinding | `NavMeshMoveToActionExecutor` |
| Play different animations for different actions | `AnimatorTriggerActionExecutor` |
| Navigate + pick up + attach in one command | `PickUpActionExecutor` |
| Place one held or scene object onto another | `PutOnActionExecutor` |
| Custom movement stack, inventory, UI, physics | [Write a custom action executor](writing-custom-executors.md) |

## Usage examples

### Example 1 — Safety instructor with gesture and movement

**Scenario:** A workplace safety training simulation. The instructor NPC uses two always-available executors to point at hazards and demonstrate equipment locations.

**Inspector setup on the NPC:**

* `LookAtTargetActionExecutor` — `_duration = 0.8`
* `UnityEventActionExecutor` — `_onExecute` → calls `HazardHighlightManager.HighlightActive()`

**ConvaiActionConfigSource definitions:**

| ActionName | TargetRequirement | Executor |
| --- | --- | --- |
| `Point At` | `Either` | `LookAtTargetActionExecutor` |
| `Flag Hazard` | `None` | `UnityEventActionExecutor` |

**Expected outcome:** "Point at the gas valve" → the NPC rotates to face the gas valve over 0.8 seconds. "Flag the hazard" → the `UnityEvent` fires and highlights the active hazard in the UI.

### Example 2 — Equipment retrieval with animation

**Scenario:** A medical training scenario. The instructor retrieves a defibrillator and hands it off.

**Inspector setup:**

* `NavMeshMoveToActionExecutor` — `_stoppingDistance = 0.6`
* `PickUpActionExecutor` — `_mover = NavMeshMoveToActionExecutor`, `_pickUpTrigger = "GrabItem"`, `_attachPoint = RightHandBone`, `_animationDuration = 1.2`

**ConvaiActionConfigSource definitions:**

| ActionName | TargetRequirement | Executor |
| --- | --- | --- |
| `Retrieve` | `Object` | `PickUpActionExecutor` |

**Expected outcome:** "Retrieve the defibrillator" → the NPC navigates to the defibrillator, plays the grab animation for 1.2 seconds, then the defibrillator attaches to the right hand bone.

## Next steps

{% content-ref url="dispatcher-and-batch-policies.md" %}
[Dispatcher and batch policies](dispatcher-and-batch-policies.md)
{% endcontent-ref %}

{% content-ref url="writing-custom-executors.md" %}
[Write a custom action executor](writing-custom-executors.md)
{% endcontent-ref %}
