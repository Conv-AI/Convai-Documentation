---
title: Migrate from Attention
description: Replace the retired Attention and legacy Gaze components with Convai Gaze, and avoid losing scene references when you save.
last_reviewed: "4.5.0"
---

SDK 4.5.0 retired the Attention module and the previous Convai Gaze implementation, and deleted the seven documentation pages that covered them with no redirects. If a bookmark or a search result brought you here instead, this page is the replacement: it maps every removed component and asset to its Convai Gaze equivalent, calls out the one step that can silently break a scene if you skip it, and explains what changes visually even if you touch no code at all.

## Component and asset replacements

| Removed in 4.5.0 | Replaced by | Add through |
|---|---|---|
| `ConvaiAttentionController`, `ConvaiGazeCoordinator`, `ConvaiHeadLookActuator`, `ConvaiEyeGazeActuator` | `ConvaiGazeController` | **Add Component > Convai > Embodiment > Gaze** |
| `ConvaiAttentionProfile`, `ConvaiGazeCoordinationProfile`, `ConvaiGazeEyeProfile`, `ConvaiGazeHeadProfile` | `ConvaiGazeProfile` | **Assets > Create > Convai > Embodiment > Gaze Profile** |
| `IFocusTargetProvider`, `IGazeIntentProvider` | `IGazeTargetProvider`, registered with `RegisterTargetProvider` | Implement the interface, call `ConvaiGazeController.RegisterTargetProvider` |
| `ConvaiAttentionDynamicContextBridge` | `GazeDynamicContextBridge` | **Add Component > Convai > Gaze > Advanced > Dynamic Context Bridge** |
| `ConvaiWorldObjectFocusProvider` | `ConvaiGazeTarget` | **Add Component > Convai > Gaze > Target** |
| `DefaultFocusTargetProvider` (Attention's auto-created player provider) | Automatic — `ConvaiGazeController` creates its own player anchor when **Auto Create Player Anchor** is on | Nothing to add for the common case; add `PlayerAnchorTargetProvider` (**Convai > Gaze > Advanced > Player Anchor**) only for split-screen or multiplayer rigs |

`ConvaiGazeController` resolves the same head and eye bones from the character's rig itself, so there is nothing to re-point once it is on the `GameObject` that carries `ConvaiCharacter` and `EmbodimentContext`.

## Replace ConvaiWorldObjectFocusProvider before you save the scene

{% hint style="danger" %}
`ConvaiWorldObjectFocusProvider` was a `MonoBehaviour` living directly in your scenes. Because the type no longer exists in 4.5.0, Unity drops the component silently the next time the scene is saved — the `GameObject` stops being a gaze target and nothing in the console explains why.
{% endhint %}

Open every affected scene and add `ConvaiGazeTarget` (**Add Component > Convai > Gaze > Target**) to each object that carried the old component **before** you save. `ConvaiGazeTarget` covers the same job and adds controls the old component never had: a priority tier that can be set above the player's own tier of 10, a base relevance, the distances inside which the target is a candidate at all, and a local-space aim offset so the eyes land on an exact point instead of the object's pivot.

## Migrate scripted focus providers

If you implemented `IFocusTargetProvider` or `IGazeIntentProvider` to feed Attention or the previous Gaze implementation, implement `IGazeTargetProvider` instead — the shape is the same: you are asked for a candidate on the character's `TryGetCandidate` call, and you answer with a target point and a relevance.

```csharp
using Convai.Modules.Gaze.Components;
using Convai.Modules.Gaze.Providers;
using UnityEngine;

public sealed class DeskLampFocusProvider : MonoBehaviour, IGazeTargetProvider
{
    [SerializeField] private ConvaiGazeController gaze;

    private void OnEnable() => gaze.RegisterTargetProvider(this);

    private void OnDisable() => gaze.UnregisterTargetProvider(this);

    public bool TryGetCandidate(Transform characterRoot, out GazeTargetCandidate candidate)
    {
        candidate = new GazeTargetCandidate(
            GazeTargetKind.WorldObject,
            priority: 6,
            relevance: 0.8f,
            target: transform,
            worldPoint: transform.position,
            debugName: "Desk Lamp");
        return true;
    }
}
```

Register the provider with `ConvaiGazeController.RegisterTargetProvider` rather than any Attention-specific registration call, and unregister it on disable so a destroyed or pooled object cannot keep publishing candidates. If you drove the old actuators from code directly, the new entry points are `GazeAt` and `GlanceAt`: each returns a `GazeHandle` you can `Release()` early or await `Settled`/`Completion` on, replacing hand-written weights on an actuator.

## Re-tune your profile — tuning values do not carry over

Delete your `ConvaiAttentionProfile`, `ConvaiGazeCoordinationProfile`, `ConvaiGazeEyeProfile`, and `ConvaiGazeHeadProfile` assets once you have migrated — those types are gone and the assets will not deserialize. Do not try to transcribe their values field-for-field: `ConvaiGazeProfile` does not expose Attention's interest-budget model as separate acquire, release, hold, decay, recovery, and break-threshold numbers. It reaches the same "committed but not staring" result through its own **Targeting** and **Head & Body** sections. Start from a character with no profile assigned — the shipped defaults are tuned to look correct on their own — and only create a `ConvaiGazeProfile` when you want to author a distinct personality.

## What looks different with no code change

Even a project that does nothing beyond replacing the components will look different from the retired setup, because Gaze rewrites how a look is produced, not only what triggers it. The 4.5.0 release notes document roughly twenty behavior-level corrections in this area; a reader is most likely to notice:

- Looks are now shared across the body as one movement — eyes, head, chest, then feet — instead of three uncoordinated stages each guessing at the others' share, so a character no longer ends up looking at you out of the corner of its eyes while its head points elsewhere.
- An idle character's curiosity glance no longer snaps: it used to execute the first part of the turn at reflex speed; it now takes the turn time the profile actually specifies.
- Deciding to look somewhere new and continuing to track or hold on something are handled as two different kinds of movement, both timed by the Gaze Profile's **Head & Body** settings rather than by ad hoc thresholds.
- Head and chest turns lead with a natural cascade — the neck leads, the head arrives and settles a moment later, the chest leads both of them — instead of rotating as one rigid piece.
- A glance at the player aims at the player's eye line rather than the floor beneath them, when the player anchor is a rig transform rather than the main camera.
- The eyes hold still while the head turns instead of sweeping across the room at head speed and forcing extra corrective saccades.
- A walking character no longer glances at its own destination every few seconds by default, and no longer ducks its head toward its own feet on arrival.

None of this is configurable back to the old behavior beyond re-tuning the Gaze Profile — the fixes apply unconditionally. See the full list in [release notes](../../overview/release-notes.md).

## Verify the migration

- Enter Play mode. The `ConvaiGazeController` inspector reads **Ready**; **Not Working** appears only when the rig has no resolvable head bone, and names the fix.
- Confirm any migrated `IGazeTargetProvider` implementation registers in `OnEnable` and unregisters in `OnDisable`, and that it compiles without referencing `IFocusTargetProvider` or `IGazeIntentProvider` anywhere in the project.
- Open **Convai > Gaze Editor**, the **Setup** tab, and confirm the rig report shows the expected head and eye bones and the expected eye backend.
- Save an affected scene only after every `ConvaiWorldObjectFocusProvider` in it has been replaced with `ConvaiGazeTarget`.

## Next steps

{% content-ref url="quick-start.md" %}
[Gaze quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="how-gaze-works.md" %}
[How gaze works](how-gaze-works.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot gaze](troubleshooting.md)
{% endcontent-ref %}
