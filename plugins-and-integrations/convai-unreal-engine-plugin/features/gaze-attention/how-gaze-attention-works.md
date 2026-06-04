---
title: How gaze attention works
description: Understand how the gaze trace pipeline, attention promotion timers, highlight rendering, and the attention-source locking rule interact at runtime.
last_reviewed: "2026-06-04"
---

Gaze attention is a subsystem inside `UConvaiPlayerComponent` that translates where the player is looking into contextual focus for AI characters. When active, it runs every tick, manages visual feedback through a highlight actor and a cursor widget, and writes to the chatbot's "object in attention" slot after a configurable dwell period.

## Tick pipeline

Each tick, `UConvaiPlayerComponent` calls `TickGazeAttention` when `bEnableGazeAttention` is `true`. The pipeline runs in this order:

1. A line trace fires forward from the player camera along `GazeTraceChannel` (default `ECC_Visibility`) up to `GazeMaxDistance` centimetres (default 5000 cm).
2. The trace result is tested for a `UConvaiObjectComponent` on the hit actor. If the hit actor (or any of its sub-components) carries a `UConvaiObjectComponent`, the actor becomes the current gaze target.
3. If the line trace misses, a dot-product fallback runs when `GazeAngleTolerance` is greater than zero. The fallback walks every `UConvaiObjectComponent` registered in the subsystem, discards any that are out of range, behind the camera, or outside the cone half-angle, and picks the one with the highest dot product against the view direction. This avoids a sphere-trace physics query and behaves in a distance-independent way — a distant object needs the same on-screen tolerance as a nearby one.
4. Any transition between gaze targets (entering or leaving) fires `OnGazeBegin` or `OnGazeEnd` on the player component and updates the cursor widget state.
5. Two accumulators run in parallel: `GazeAccumulator` counts how long the current target has been held, and `NoGazeAccumulator` counts how long the player has been looking away from any Convai object.

## Attention promotion and release

When `GazeAccumulator` reaches `GazeAttentionDelay` seconds (default 1.0), the gaze target is promoted to "in attention":

- The player component calls an internal method on the chatbot component, passing the `FConvaiObjectEntry` for the target plus the values of `GazeAttentionText` and `GazeShouldRespond`. This is handled automatically — no Blueprint wiring is required.
- `OnAttentionGained` fires on the player component.
- The chatbot's `AttentionSource` property is stamped to `EConvaiAttentionSource::Gaze`.

When `NoGazeAccumulator` reaches `GazeAttentionLossDelay` seconds (default 5.0) and no new target has been gazed at, the slot is released:

- The player component calls an internal method on the chatbot component to clear the attention slot. Again, this is automatic.
- `OnAttentionLost` fires on the player component.
- The chatbot's `AttentionSource` resets to `EConvaiAttentionSource::None`.

## Attention-source locking rule

The chatbot tracks who last set its attention slot via `AttentionSource` (`EConvaiAttentionSource`). The enum has three values:

| Value | Meaning |
|---|---|
| `None` | Attention slot is empty. |
| `Gaze` | Slot was last set by the gaze system. |
| `Explicit (Blueprint/C++)` | Slot was last set by a direct `SetObjectInAttention` call. |

Gaze-driven updates only succeed when `AttentionSource` is `None` or `Gaze`. A direct call to `SetObjectInAttention` from Blueprint or C++ sets `AttentionSource` to `Explicit`, locking the slot. Gaze calls are silently rejected while the slot is locked. To release an explicit lock, call `SetObjectInAttention` with an empty `FConvaiObjectEntry`.

{% hint style="warning" %}
If a character's attention slot stays on one object regardless of where the player looks, check whether a Blueprint graph is calling `SetObjectInAttention` and never clearing it. The `AttentionSource` read-only property on the chatbot shows which system currently owns the slot.
{% endhint %}

## Attention and the actions system

`SetObjectInAttention` has no effect when `Enable Actions` (`bEnableActions`) is `false` on the chatbot. Convai only resolves object attention when the `action_config` block was included at session connect — which requires actions to be enabled. Gaze attention therefore requires the actions system to be active on the chatbot.

## Visual feedback

### Highlight actor

When a gaze target is identified, `UConvaiPlayerComponent` spawns (or reuses) an `AConvaiGazeHighlightActor` over the target. The highlight actor paints the target's meshes using `UMeshComponent::SetOverlayMaterial` on UE 5.3 and later. The default overlay material is `/ConvAI/Highlights/M_ConvaiGazeOverlay`, a Fresnel rim silhouette that reads an `EmissiveColor` vector parameter driven by `GazeHighlightColor * GazeHighlightEmissiveIntensity`.

On UE 5.0–5.2, `SetOverlayMaterial` is not available on `UMeshComponent`. The actor falls back to a `DrawDebugBox` wireframe around the target's bounds using `FallbackBoxThickness` and `FallbackBoxPadding`.

If a `UConvaiObjectComponent` has a `ComponentName` filter set (component-scoped attention), the highlight is stamped only on the specific sub-mesh rather than every mesh on the actor. This lets an actor expose different logical parts independently — for example, a door's "Handle" component triggers a highlight only on the handle mesh.

### Cursor widget

A `UConvaiGazeCursorWidget` is added to the viewport while gaze tracking is active when `bShowGazeCursor` is `true`. The widget has two visual states:

- **Idle** — gaze is not over any Convai object. Drawn with `GazeCursorIdleColor` (default alpha 0, fully transparent).
- **Active** — gaze is on a Convai object. Drawn with `GazeCursorActiveColor` (default white).

The transition between states is interpolated over `GazeCursorFadeInTime` and `GazeCursorFadeOutTime`. When `bAlwaysShowGazeCursor` is `true`, the cursor stays in the Active visual state even when gaze is not over a Convai object.

The cursor is a pure C++ widget that uses Unreal's `FCoreStyle::WhiteBrush`. No texture asset ships with the plugin. To display a custom reticle, subclass `UConvaiGazeCursorWidget` in Blueprint, override `OnGazeStateChanged`, and assign the subclass to `GazeCursorWidgetClass` on the player component.

## Next steps

{% content-ref url="quick-start.md" %}
[Quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-reference.md" %}
[Gaze attention reference](gaze-attention-reference.md)
{% endcontent-ref %}
