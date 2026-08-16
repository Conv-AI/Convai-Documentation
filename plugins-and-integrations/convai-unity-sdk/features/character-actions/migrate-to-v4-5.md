---
title: Migrate actions to v4.5.0
description: Repair scenes broken by the Character Actions changes in Convai Unity SDK 4.5.0, including a renamed executor, removed executors, and a timing fix.
last_reviewed: "4.5.0"
---

Convai Unity SDK 4.5.0 renamed one shipped action executor with a new component GUID, removed three unpublished experimental executors, and clarified what Point At Target's Hold Seconds field actually controls. This page walks through the repair each change needs, in order of how much it can break a scene.

{% hint style="warning" %}
If your project used `UnityEventActionExecutor`, read the first section before you open any scene or prefab in the Unity Editor. Unity drops the component silently the first time an affected scene or prefab is saved, and the wiring inside it is not recoverable afterward.
{% endhint %}

## Repair scenes after the ConvaiUnityEventActionExecutor rename

`UnityEventActionExecutor` was renamed to `ConvaiUnityEventActionExecutor` in `4.5.0`, bringing it in line with every other shipped executor. Its **Add Component** entry is now `Convai/Actions/Raise Unity Event`.

The new type carries a different component GUID. Unity identifies a component by its GUID, not its class name, so **Unity does not carry the component across** — it drops `UnityEventActionExecutor` from every scene and prefab that had one, along with every listener you wired into its `UnityEvent` field. There is no upgrade step or asset migration that recovers this data once it is gone.

Before you open any affected scene in the Unity Editor:

{% stepper %}
{% step %}
### Write down what each event called

For every `GameObject` carrying the old `UnityEventActionExecutor`, note which listener methods were wired into its `UnityEvent` field, and on which target objects. Once the scene is saved with the new SDK version, there is nothing left to read this from.
{% endstep %}

{% step %}
### Add the renamed executor

On each affected `GameObject`, add `ConvaiUnityEventActionExecutor` from **Add Component > Convai > Actions > Raise Unity Event**.
{% endstep %}

{% step %}
### Re-wire the event by hand

Using your notes from the first step, add each listener back to the new component's `UnityEvent` field in the Inspector.
{% endstep %}

{% step %}
### Re-point the action definition

In `ConvaiActionConfigSource`, open each action definition that was bound to the old executor and set its **Executor** field to the new `ConvaiUnityEventActionExecutor` component reference.
{% endstep %}
{% endstepper %}

The serialized field behind the `UnityEvent` is still named `_onExecute` and behaves identically to before, so code in your project that references `[SerializeField] private UnityEvent` on this executor needs no change beyond the type name.

## Replace the three removed experimental executors

`4.5.0` removes three executors that were never published to the public Action catalog or documented: `ConvaiGuidedTourActionExecutor`, `ConvaiAddressGroupActionExecutor`, and `ConvaiPerformAtTargetActionExecutor`. None of the three exists in the SDK source as of this release.

Because these executors were experimental and unpublished, there is no built-in successor for any of them. If your project referenced one of these types directly by name:

* The component itself behaves like any other deleted `MonoBehaviour` — Unity shows a missing script reference on the affected `GameObject` and drops the component the next time the scene is saved, along with any values that were configured on it.
* Rebuild the behavior you need from the shipped executors instead. A guided-tour or address-the-group sequence is usually a series of steps — `Move To`, `Look At`, `Point At` — enqueued together with `ConvaiActionDispatcher.EnqueueActions`, the same pattern shown in [Character actions examples](usage-examples.md).
* If no combination of shipped executors covers what you need, write your own executor against `IConvaiActionExecutor`. See [Write a custom action executor](writing-custom-executors.md).

## Adjust for the Point At Target timing change

`Point At Target` (`ConvaiPointAtActionExecutor`) previously exposed one setting, **Hold Seconds**, and it never controlled how long the whole gesture takes — it is only the pause at full extension. The arm's rise and fall come from the animation itself, and the shipped pointing clips put the apex halfway through five seconds, so even a one-second hold produced a roughly six-second gesture with no way to shorten it.

`4.5.0` adds two fields that reach the pointing animation directly:

| Field | Type | Default | Controls |
| --- | --- | --- | --- |
| **Hold Seconds** (`_holdSeconds`) | `float` | `3` | The pause at full extension only. Unchanged in meaning — its tooltip now says so explicitly. |
| **Gesture Speed** (`_gestureSpeed`) | `float`, range `0.25`–`3` | `1` | Multiplies the speed of the arm's rise and fall. Raise this when a point reads as slow. |
| **Release** (`_release`) | `PointingReleaseStyle` | `Play Tail` | What happens when the hold ends. `Play Tail` lowers the arm through the rest of the animation (fullest-looking, slowest). `Blend` drops the pose out instead, ending the gesture as soon as the hold does. |

{% hint style="info" %}
Both new fields default to the values that reproduce the previous behavior, so an existing scene with `Point At Target` on it looks identical after the upgrade. Nothing needs repairing unless you want a different result.
{% endhint %}

If your project set **Hold Seconds** low while trying to shorten the whole gesture and found a floor around five to six seconds regardless, that ceiling came from the animation's rise and fall, not from **Hold Seconds** — raising **Gesture Speed** and setting **Release** to `Blend` is what actually shortens it. A point of about a second is **Gesture Speed** `1.5` with **Release** set to `Blend`.

## Other changes to check

* **Four production-ready executors were added**: `ConvaiLeadPlayerActionExecutor`, `ConvaiScanEnvironmentActionExecutor`, `ConvaiCountTargetGroupActionExecutor`, and `ConvaiMeasureDistanceActionExecutor`. None of these require any action from an existing project — see [Character actions examples](usage-examples.md) for `ConvaiMeasureDistanceActionExecutor` in use.
* **`ConvaiActionTestSetup` and its three `Convai/Developer/*` menu items are gone.** Use the Actions Editor's **Try It** control against your own character and action instead — **Preview** in Edit mode, **Test Run** in Play mode.
* **`ConvaiActionDebugWindow` and its `Convai/Developer/Action Debug Window` menu item are gone.** Raw command injection, target-resolution testing, and the runtime patch composer now live under the Actions Editor's **Live > Advanced** group; setup checks live in the Convai Troubleshooter. See [Troubleshoot character actions](debugging-and-troubleshooting.md).
* **`LookAtTargetActionExecutor` is gone**, replaced by the Gaze module's `ConvaiLookAtActionExecutor` (`Convai/Actions/Look At Target`). The replacement needs a `ConvaiGazeController` on the character (`Convai/Embodiment/Gaze`) and gains `mode`, `holdSeconds`, and `engagement` settings the old executor never had.

## Verify the migration

* Open every scene and prefab that carried `UnityEventActionExecutor` and confirm `ConvaiUnityEventActionExecutor` is present with its listeners wired, not showing a missing script warning.
* Search your project for any remaining reference to `ConvaiGuidedTourActionExecutor`, `ConvaiAddressGroupActionExecutor`, or `ConvaiPerformAtTargetActionExecutor` — a project that still compiles with the current SDK has none.
* Open **Convai > Troubleshooter** on each character with actions configured and confirm the Actions row reports no errors. See [Troubleshoot character actions](debugging-and-troubleshooting.md).

## Next steps

{% content-ref url="action-executors.md" %}
[Action executors](action-executors.md)
{% endcontent-ref %}

{% content-ref url="debugging-and-troubleshooting.md" %}
[Troubleshoot character actions](debugging-and-troubleshooting.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Character actions examples](usage-examples.md)
{% endcontent-ref %}
