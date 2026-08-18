---
title: How gaze attention works
description: Understand the gaze trace pipeline, attention promotion timers, component-scoped targeting, highlight rendering, and the attention-source locking rule.
last_reviewed: "4.0.0-beta.27"
---

Gaze attention is a subsystem inside `UConvaiPlayerComponent` that translates where the player is looking into contextual focus for AI characters. When active, it runs every tick, manages visual feedback through a highlight actor and a cursor widget, and writes to the chatbot's "object in attention" slot after a configurable dwell period.

If you have not enabled gaze attention yet, start with [Gaze attention quick start](gaze-attention-quick-start.md). This page explains the mental model behind that setup.

## Three core ideas

Before the per-tick pipeline, keep these three stages in mind:

| Stage | What happens | What the player sees |
|---|---|---|
| **Gaze detection** | A line trace (and optional angle fallback) finds a gazeable `UConvaiObjectComponent` under the crosshair. | Highlight and cursor turn active immediately. |
| **Dwell promotion** | After `GazeAttentionDelay` seconds on the same target, the object is promoted to "in attention." | No new visual change; `OnAttentionGained` fires. |
| **Attention ownership** | Each chatbot tracks who set its attention slot via `AttentionSource`. Gaze can update the slot only when it is `None` or already owned by gaze. | The character may speak or stay silent depending on `GazeShouldRespond`. |

Tagged objects come from scene metadata — see [How scene metadata works](../scene-metadata/how-scene-metadata-works.md). Attention ownership and pronoun grounding overlap with [Attention and reference grounding](../character-actions/attention-and-reference-grounding.md).

## Tick pipeline

Each tick, `UConvaiPlayerComponent` calls `TickGazeAttention` when `bEnableGazeAttention` is `true`. The diagram below shows the full decision path; the numbered list that follows describes each stage in detail.

```mermaid
flowchart TD
    A([TickGazeAttention]) --> B{bEnableGazeAttention?}
    B -- No --> Z([Skip])
    B -- Yes --> C[Line trace along GazeTraceChannel\nup to GazeMaxDistance]
    C --> F[GatherMatchingObjects]
    F --> D{Valid gaze target?}
    D -- Yes --> I[Spawn / update\nAConvaiGazeHighlightActor]
    D -- No --> E{AngleTolerance > 0\nAND trace not blocked\nby non-Convai geometry?}
    E -- Yes --> G[Dot-product fallback:\nwalk subsystem pool]
    E -- No --> H([No gaze target this tick])
    G --> Q{Fallback target?}
    Q -- Yes --> I
    Q -- No --> H
    I --> J[Update UConvaiGazeCursorWidget\nstate: Active or Idle]
    J --> K[Tick GazeAccumulator\nor NoGazeAccumulator]
    K --> L{GazeAccumulator >=\nGazeAttentionDelay?}
    L -- Yes --> M([PromoteToAttention\nOnAttentionGained fires])
    L -- No --> N{NoGazeAccumulator >=\nGazeAttentionLossDelay?}
    N -- Yes --> O([ReleaseAttention\nOnAttentionLost fires])
    N -- No --> P([Accumulate — no state change])
```

1. A line trace fires forward from the player camera or VR HMD along `GazeTraceChannel` (default `ECC_Visibility`) up to `GazeMaxDistance` (default 5000 cm).
2. The trace result is tested for a gazeable `UConvaiObjectComponent` on the hit actor. The gaze target is accepted only when the object is whole-actor scoped or the hit primitive matches the object's configured component scope.
3. If the strict trace does not engage a valid gaze target, a dot-product fallback runs when `GazeAngleTolerance` is greater than zero and the primary trace was not blocked by non-Convai geometry. The fallback walks every `UConvaiObjectComponent` registered in the subsystem, discards any that are out of range, behind the camera, or outside the cone half-angle, and picks the one with the highest dot product against the view direction. This avoids a sphere-trace physics query and behaves in a distance-independent way — a distant object needs the same on-screen tolerance as a nearby one.
4. Any transition between gaze targets (entering or leaving) fires `OnGazeBegin` or `OnGazeEnd` on the player component and updates the cursor widget state.
5. Two accumulators run in parallel: `GazeAccumulator` counts how long the current target has been held, and `NoGazeAccumulator` counts how long the player has been looking away from any Convai object.

## Attention promotion and release

When `GazeAccumulator` reaches `GazeAttentionDelay` seconds (default 1.0), the gaze target is promoted to "in attention":

- The player component calls an internal method on the chatbot component, passing the `FConvaiObjectEntry` for the target plus the values of `GazeAttentionText` and `GazeShouldRespond`. This is handled automatically — no Blueprint wiring is required.
- `OnAttentionGained` fires on the player component.
- The chatbot's `AttentionSource` property is stamped to `EConvaiAttentionSource::Gaze`.

When `NoGazeAccumulator` reaches `GazeAttentionLossDelay` seconds (default 5.0) and the player is no longer gazing at the current attention actor/primitive pair, the slot is released:

- The player component calls an internal method on the chatbot component to clear the attention slot. Again, this is automatic.
- `OnAttentionLost` fires on the player component.
- The chatbot's `AttentionSource` resets to `EConvaiAttentionSource::None`.

## Attention-source locking rule

The chatbot tracks who last set its attention slot via `AttentionSource` (`EConvaiAttentionSource`). The `AttentionSource` property on `UConvaiChatbotComponent` advances through three states:

```mermaid
stateDiagram-v2
    [*] --> None
    None --> Gaze : TrySetObjectInAttentionFromGaze()
    Gaze --> Gaze : New gaze target promoted
    Gaze --> None : TryClearObjectInAttentionFromGaze()\nor loss timer expires
    None --> Explicit : SetObjectInAttention() called\nfrom Blueprint/C++
    Gaze --> Explicit : SetObjectInAttention() called\nfrom Blueprint/C++
    Explicit --> None : SetObjectInAttention() with\nempty FConvaiObjectEntry
    Explicit --> Explicit : SetObjectInAttention() with\na new object
```

| Value | Meaning |
|---|---|
| `None` | Attention slot is empty. |
| `Gaze` | Slot was last set by the gaze system. |
| `Explicit (Blueprint/C++)` | Slot was last set by a direct `SetObjectInAttention` call. |

Gaze-driven updates only succeed when `AttentionSource` is `None` or `Gaze`. A direct call to `SetObjectInAttention` from Blueprint or C++ sets `AttentionSource` to `Explicit`, locking the slot. Gaze calls are rejected while the slot is locked, and the rejection logs a warning naming the object and the reason. To release an explicit lock, call `SetObjectInAttention` with an empty `FConvaiObjectEntry`.

{% hint style="warning" %}
If a character's attention slot stays on one object regardless of where the player looks, check whether a Blueprint graph is calling `SetObjectInAttention` and never clearing it. The `AttentionSource` read-only property on the chatbot shows which system currently owns the slot.
{% endhint %}

## Attention and the actions system

`SetObjectInAttention` has no effect when `Enable Actions` (`bEnableActions`) is `false` on the chatbot. Convai only resolves object attention when the `action_config` block was included at session connect — which requires actions to be enabled. Gaze attention therefore requires the actions system to be active on the chatbot. A call that has no effect for this reason, or because the target object is not yet on the chatbot's environment list or was not part of the objects sent at connect time, logs a warning naming the object and the specific reason — see [Diagnose a "no effect" warning from SetObjectInAttention](troubleshoot-gaze-attention.md#diagnose-a-no-effect-warning-from-setobjectinattention).

## The one-flush attention cue

When a gaze promotion (or an explicit `SetObjectInAttention` call) succeeds and `GazeShouldRespond`/`ShouldRespond` is `Auto` or `Always`, the chatbot stages a single ephemeral event reading `"<observer> is paying attention to <object name>"` — `<observer>` is the conversation partner's name, or "The user" when none is set. This cue is never persisted in context and fires once per promotion; it does not repeat while attention stays on the same object. It is on by default and can be turned off per call by passing `bAddAttentionEvent = false` to `SetObjectInAttention`. Setting `ShouldRespond`/`GazeShouldRespond` to `Never` also suppresses it — the slot still updates, silently.

## Component-scoped gaze

`ObjectEntry.ObjectReference` (`EConvaiObjectReference`, Details panel label **Object Is**) says what the object *is* for every system that reads `FConvaiObjectEntry` — gaze, movement fallback, and vision tagging alike. It has two values:

- **Whole Actor** (default) — the whole actor is the object. Gaze matches any of the actor's primitives.
- **Specific Component** — one named sub-component is the object. Gaze matches only that component. Set `ObjectEntry.ComponentName` to a case-insensitive substring of the target component's name; a non-empty `ComponentName` has no effect while `ObjectReference` is still **Whole Actor**.

`GatherMatchingObjects` divides `UConvaiObjectComponent` instances on a hit actor into two groups:

| Group | Condition | Fires when |
|---|---|---|
| Whole-actor | `ObjectReference` is `Whole Actor`, or `ObjectReference` is `Specific Component` with an empty `ComponentName` | Any hit on the actor when the actor has no resolved component-scoped objects. If a component-scoped object on the same actor matches, whole-actor objects fire as piggyback. |
| Component-scoped | `ObjectReference` is `Specific Component` and `ComponentName` resolves to a component on the actor | Hit primitive matches (or is attached to) the resolved component |

When a component-scoped component matches, any whole-actor component on the same actor also fires ("piggyback" rule). If the actor has resolved component-scoped objects but the hit primitive does not match any of them, no gaze object fires for that hit.

**Example — a door actor with two Convai objects:**

```text
BP_Door
├── ConvaiObjectComponent "Door"        → Object Is: Whole Actor
└── ConvaiObjectComponent "DoorHandle"  → Object Is: Specific Component, Component Name: "Handle"
    └── targets SM_Handle on the actor
```

- Player looks at door frame → no gaze object fires, because the actor has a resolved component-scoped object and the hit primitive does not match it.
- Player looks at handle → `ConvaiObjectComponent "DoorHandle"` fires; `ConvaiObjectComponent "Door"` also fires (piggyback). The highlight actor scopes to `SM_Handle` only.

`ComponentName` matching is case-insensitive substring lookup. `GetResolvedComponent()` revalidates the cached match on every call — if the cached component's owner or name no longer fits the filter, it rescans automatically, so no manual refresh call is needed even after the actor's component tree changes at runtime. An unresolved `ComponentName` logs a warning the first time resolution is attempted, and that component is excluded from scoped gaze passes until the name resolves.

{% hint style="info" %}
Use component-scoped `UConvaiObjectComponent` instances to let a single complex prop expose multiple independent interaction points — each with its own `Name`, `Description`, and gaze events — without duplicating the parent actor.
{% endhint %}

## Visual feedback

### Highlight actor

When a gaze target is identified, `UConvaiPlayerComponent` spawns (or reuses) an `AConvaiGazeHighlightActor` over the target. The highlight actor paints the target's meshes using `UMeshComponent::SetOverlayMaterial` on UE 5.3 and later. By default, the highlight actor loads `/ConvAI/Highlights/M_ConvaiGazeOverlay`, a Fresnel rim silhouette material referenced by the plugin source. The actor writes `GazeHighlightColor` to the material's `EmissiveColor` and `Color` vector parameters, then writes `GazeHighlightEmissiveIntensity` to the `EmissiveIntensity` scalar parameter.

On UE 5.0–5.2, `SetOverlayMaterial` is not available on `UMeshComponent`. The actor falls back to a `DrawDebugBox` wireframe around the target's bounds using `FallbackBoxThickness` and `FallbackBoxPadding`.

When a component-scoped `UConvaiObjectComponent` matches, the highlight scopes to that specific sub-mesh rather than every mesh on the actor. See [Component-scoped gaze](#component-scoped-gaze) above for the matching rules.

### Cursor widget

A `UConvaiGazeCursorWidget` is added to the viewport while gaze tracking is active when `bShowGazeCursor` is `true`. The widget has two visual states:

- **Idle** — gaze is not over any Convai object. Drawn with `GazeCursorIdleColor` (default alpha 0, fully transparent).
- **Active** — gaze is on a Convai object. Drawn with `GazeCursorActiveColor` (default white).

The transition between states is interpolated over `GazeCursorFadeInTime` and `GazeCursorFadeOutTime`. When `bAlwaysShowGazeCursor` is `true`, the cursor stays in the Active visual state even when gaze is not over a Convai object.

The cursor is a pure C++ widget that uses Unreal's `FCoreStyle::WhiteBrush`. No texture asset ships with the plugin. To display a custom reticle, subclass `UConvaiGazeCursorWidget` in Blueprint, override `OnGazeStateChanged`, and assign the subclass to `GazeCursorWidgetClass` on the player component.

## Next steps

{% content-ref url="gaze-attention-quick-start.md" %}
[Gaze attention quick start](gaze-attention-quick-start.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-reference.md" %}
[Gaze attention reference](gaze-attention-reference.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-usage-examples.md" %}
[Gaze attention usage examples](gaze-attention-usage-examples.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-gaze-attention.md" %}
[Troubleshoot gaze attention](troubleshoot-gaze-attention.md)
{% endcontent-ref %}
