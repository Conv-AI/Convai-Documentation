---
title: Troubleshooting and diagnostics
description: Diagnose and fix gaze attention issues — objects not highlighting, attention never promoting, cursor not appearing, and component-scoped gaze not matching.
last_reviewed: "2026-06-05"
---

Use this page to diagnose and fix the most common gaze attention problems. Each entry follows a symptom / cause / fix / verify structure.

## Objects do not highlight when gazed at

**Symptom:** The player looks directly at a world actor but no silhouette or wireframe appears.

**Cause (most likely):** The actor does not have a `UConvaiObjectComponent`, or `bEnableGazeAttention` is `false` on the player component.

**Fix:**
1. Select the actor in the level. In the **Details** panel, confirm a `UConvaiObjectComponent` is listed under **Components**.
2. Select `UConvaiPlayerComponent` on the player pawn. Under **Convai | Gaze Attention**, confirm **Enable Gaze Attention** is checked.
3. If the actor uses a custom mesh with **No Collision** set on the primitive, the line trace will pass through it. Set the collision channel to at least **Visibility** and confirm the trace channel on `UConvaiPlayerComponent` matches (`GazeTraceChannel`, default `ECC_Visibility`).
4. If the actor is outside the trace range, increase `GazeMaxDistance` (default 5000 cm).

**Verify:** Enter Play mode. Point the crosshair at the actor. The pale-yellow silhouette should appear immediately, and the cursor dot should turn white.

---

## Object highlights but attention is never promoted

**Symptom:** The silhouette appears when looking at the object, but `OnAttentionGained` never fires and the character does not respond.

**Cause:** One of three conditions:
- The chatbot's attention slot is locked by an explicit `SetObjectInAttention` call elsewhere in a Blueprint graph.
- **Enable Actions** is `false` on the chatbot, so `SetObjectInAttention` calls have no effect.
- `GazeShouldRespond` is set to `Never`, so the character updates state silently rather than speaking.

**Fix:**
1. Open `UConvaiChatbotComponent` in the Details panel during Play mode. Read the `AttentionSource` property (under **Convai | Actions**). If it shows `Explicit (Blueprint/C++)`, a Blueprint call is holding the slot — find and clear it.
2. Confirm **Enable Actions** (`bEnableActions`) is `true` on the chatbot's **Convai | Action API** category.
3. If you want the character to speak, set `GazeShouldRespond` to `Always` or `Auto` on `UConvaiPlayerComponent`.
4. Confirm that `GazeAttentionDelay` is not set to an unexpectedly high value.

**Verify:** Add a Blueprint bind to `OnAttentionGained` on `UConvaiPlayerComponent` and print a screen message. Enter Play mode and hold gaze on the object for `GazeAttentionDelay` seconds. The message should appear.

---

## Attention is promoted but the character does not speak

**Symptom:** `OnAttentionGained` fires (verified via Blueprint print), but the character is silent.

**Cause:** `GazeShouldRespond` is `Never`, or the chatbot's microphone / session is not active.

**Fix:**
1. Set `GazeShouldRespond` to `Always` on `UConvaiPlayerComponent`.
2. Fill in `GazeAttentionText` with a descriptive sentence. Without text, the attention event carries no narrative context and Convai may not generate a meaningful response even when `ShouldRespond` is `Always`.
3. Confirm the chatbot is connected (session is active). If the session dropped, `SetObjectInAttention` succeeds locally but no request is sent to Convai. See [Session lifecycle](../../core-concepts/session-lifecycle.md) for how to diagnose connection state.

**Verify:** Set `GazeShouldRespond` to `Always`, enter Play mode, and look at the object for `GazeAttentionDelay` seconds. The character should begin speaking.

---

## Cursor does not appear

**Symptom:** No center-of-screen dot is visible when gaze tracking is on.

**Cause:** `bShowGazeCursor` is `false`, or the cursor widget class reference is invalid, or the cursor `IdleColor` alpha is `0` and gaze is not currently on a Convai object.

**Fix:**
1. Confirm **Show Gaze Cursor** (`bShowGazeCursor`) is `true` on `UConvaiPlayerComponent`.
2. In Play mode, aim the crosshair directly at a tagged Convai object. The cursor switches to `GazeCursorActiveColor` (default white). If it appears only when aimed at a Convai object, it is working correctly — the idle state is transparent by design.
3. To make the cursor always visible, set **Always Show Gaze Cursor** (`bAlwaysShowGazeCursor`) to `true`.
4. If the cursor still does not appear, check that `GazeCursorWidgetClass` has not been set to a class that was deleted or renamed.

**Verify:** Set `bAlwaysShowGazeCursor` to `true`, enter Play mode. A white dot should be visible at screen centre at all times.

---

## Highlight color does not match the configured value

**Symptom:** The silhouette appears but is white or a different color than set in `GazeHighlightColor`.

**Cause (UE 5.3+):** A custom `GazeOverlayMaterial` does not expose an `EmissiveColor` vector parameter, so the color cannot be applied.

**Cause (UE 5.0–5.2):** The wireframe fallback (`DrawDebugBox`) uses a fixed white color; `GazeHighlightColor` has no effect on the fallback path.

**Fix:**
1. If using a custom `GazeOverlayMaterial`, confirm the material exposes a vector parameter named `EmissiveColor`. Only this parameter name is driven by the highlight system.
2. On UE 5.0–5.2, the highlight appearance is limited to a wireframe box. Upgrade to UE 5.3 or later to use the overlay material system.
3. If `GazeOverlayMaterial` is unset and the silhouette is white (not pale yellow), the plugin asset `/ConvAI/Highlights/M_ConvaiGazeOverlay` may have been stripped from a cooked build. The fallback material `/Engine/EngineMaterials/EmissiveMeshMaterial` has no parameters. Re-package the plugin content.

**Verify:** Set `GazeHighlightColor` to a saturated red `(1.0, 0.0, 0.0, 1.0)` and enter Play mode. The silhouette should appear red when looking at a tagged object.

---

## Gaze engages objects behind thin walls

**Symptom:** Objects on the other side of a wall or floor are highlighted when the player looks in that direction.

**Cause:** The world geometry does not block the `GazeTraceChannel` — typically because the mesh uses **No Collision** or a channel set to **Ignore**.

**Fix:**
1. Select the wall or floor mesh. In the **Details** panel under **Collision**, confirm that the `GazeTraceChannel` (default `ECC_Visibility`) is set to **Block**.
2. Alternatively, change `GazeTraceChannel` on `UConvaiPlayerComponent` to a custom channel that only your interactable objects and blocking geometry respond to.

**Verify:** Enter Play mode and look at the wall. Objects on the other side should no longer highlight.

---

## Angle tolerance causes wrong object to be highlighted

**Symptom:** The player looks at one object but a nearby object is highlighted instead.

**Cause:** `GazeAngleTolerance` is set too high, causing the dot-product fallback to prefer a larger or differently placed object that better aligns with the view direction.

**Fix:** Reduce `GazeAngleTolerance` (default 5 degrees, advanced display). If the objects require precise aiming, set `GazeAngleTolerance` to `0` to disable the fallback entirely and require a direct line-trace hit.

**Verify:** Set `GazeAngleTolerance` to `0` and enter Play mode. Objects should only highlight when the crosshair is directly over them.

---

## Component-scoped highlight appears on the wrong sub-mesh or the whole actor

**Symptom:** A `UConvaiObjectComponent` with `ComponentName` set highlights the entire actor instead of only the named sub-mesh, or the highlight does not appear at all when looking at the intended part.

**Cause:** The `ComponentName` value does not match any component on the actor. Common reasons: typo, wrong case (matching is case-insensitive but the substring must appear in the component name), the component was renamed after the value was set, or the component is not a `UPrimitiveComponent` descendant.

**Fix:**
1. In Play mode, call `GetResolvedComponent(true)` on the `UConvaiObjectComponent` from Blueprint and print the return value. A `nullptr` result means the name did not resolve — check the exact component name in the Details panel hierarchy.
2. Confirm that `ComponentName` is a substring of the target component's label as shown in the **Components** panel (for example, `"Handle"` matches `SM_DoorHandle` but not `SM_Knob`).
3. If the actor's component tree is built at runtime (procedural generation, dynamic attachment), call `GetResolvedComponent(true)` after the tree is fully constructed rather than relying on the cached result from load time.
4. Confirm the target component has collision enabled on the `GazeTraceChannel`. A component with no collision will never be hit by the line trace, so the scoped match cannot fire even if the name resolves correctly.

**Verify:** After correcting `ComponentName`, enter Play mode and aim the crosshair at the specific sub-mesh. Only that mesh should highlight; other parts of the actor should remain unaffected. `GetResolvedComponent(false)` should return the correct component reference.

---

## Next steps

{% content-ref url="how-gaze-attention-works.md" %}
[How gaze attention works](how-gaze-attention-works.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-reference.md" %}
[Gaze attention reference](gaze-attention-reference.md)
{% endcontent-ref %}
