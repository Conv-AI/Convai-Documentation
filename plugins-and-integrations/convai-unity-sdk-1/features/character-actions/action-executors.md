---
title: Action executors
description: Reference for all six action executor components — core look-at and event executors, plus sample NavMesh, animation, and pickup executors.
---

Executors are the components that perform in-scene behavior when the dispatcher runs an action step. The Convai SDK ships two executors in the core runtime (always available) and four additional executors in the sample pack (require import). This page documents every Inspector field and explains when to use each executor.

## Core runtime executors

These two executors are part of the core SDK runtime. No sample import is required.

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

## Sample executors

These four executors are included in the Convai SDK sample pack. Import them via **Window → Package Manager → Convai SDK for Unity → Samples → Import**.

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
The scene must have a baked NavMesh before this executor can navigate. Open **Window → AI → Navigation** and bake before entering Play Mode. If the agent starts off the NavMesh, `SetDestination` will fail silently and the executor will loop forever until the `TimeoutSeconds` expires.
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

If no binding matches the incoming action name, the executor returns `Failed` with message `No binding for '<action name>'`.

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
| `_animator` | `Animator` | `null` | The Animator to drive. Optional — skipped if null. |
| `_pickUpTrigger` | `string` | `"PickUp"` | The Animator trigger parameter to fire after arriving at the target. |
| `_attachPoint` | `Transform` | `null` | The transform the picked-up object is reparented to (e.g., hand bone). Optional — object is not reparented if null. |
| `_animationDuration` | `float` | `1.0` | Seconds to wait after firing the animation trigger before reparenting the object. |

**Execution sequence:**

1. `NavMeshMoveToActionExecutor.ExecuteAsync` navigates to the target. If it fails or is canceled, `PickUpActionExecutor` returns that result immediately.
2. `_animator.SetTrigger(_pickUpTrigger)` is called.
3. Waits `_animationDuration` seconds (cancellable).
4. Target `GameObject` is reparented to `_attachPoint` at local position/rotation zero.
5. Returns `Succeeded`.

{% hint style="info" %}
`PickUpActionExecutor` calls into `NavMeshMoveToActionExecutor` directly via `ExecuteAsync`. Both components must be on the same `GameObject` and a baked NavMesh must be present in the scene.
{% endhint %}

## Choosing the right executor

| Use case | Recommended executor |
| --- | --- |
| NPC faces a target smoothly | `LookAtTargetActionExecutor` |
| Any no-target action wired to gameplay callbacks | `UnityEventActionExecutor` |
| Rapid prototyping without NavMesh | `TransformMoveToActionExecutor` |
| Production NPC movement with pathfinding | `NavMeshMoveToActionExecutor` |
| Play different animations for different actions | `AnimatorTriggerActionExecutor` |
| Navigate + pick up + attach in one command | `PickUpActionExecutor` |
| Custom movement stack, inventory, UI, physics | [Write a custom action executor](writing-custom-executors.md) |

## Usage examples

### Example 1 — Safety instructor with gesture and movement (core executors only)

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

### Example 2 — Equipment retrieval with animation (sample executors)

**Scenario:** A medical training scenario. The instructor retrieves a defibrillator and hands it off.

**Inspector setup (requires sample import):**

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
