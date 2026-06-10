---
title: Troubleshoot gaze attention
description: Diagnose and fix gaze attention issues — objects not highlighting, attention never promoting, cursor not appearing, and component-scoped gaze not matching.
last_reviewed: "4.0.0-beta.21"
---

Use this page to diagnose and fix the most common gaze attention problems. Each entry follows a symptom / cause / fix / verify structure.

{% hint style="info" %}
If you have not completed the baseline setup yet, start with [Gaze attention quick start](gaze-attention-quick-start.md) and return here only when a specific symptom persists.
{% endhint %}

## Objects do not highlight when gazed at

**Symptom:** The player looks directly at a world actor but no silhouette or wireframe appears.

**Cause (most likely):** One of these conditions:

- The actor does not have a `UConvaiObjectComponent`.
- `bEnableGazeAttention` is `false` on the player component.
- `bGazeable` is `false` on the object's `UConvaiObjectComponent` (under **Convai | Object | Gaze**).

**Fix:**
1. Select the actor in the level. In the **Details** panel, confirm a `UConvaiObjectComponent` is listed under **Components**.
2. On that object component, expand **Convai | Object | Gaze** and confirm **Gazeable** (`bGazeable`) is checked.
3. Select `UConvaiPlayerComponent` on the player pawn. Under **Convai | Gaze Attention**, confirm **Enable Gaze Attention** is checked.
4. If the actor uses a custom mesh with **No Collision** set on the primitive, the line trace will pass through it. Set the collision channel to at least **Visibility** and confirm the trace channel on `UConvaiPlayerComponent` matches (`GazeTraceChannel`, default `ECC_Visibility`).
5. If the actor is outside the trace range, increase `GazeMaxDistance` (default 5000 cm).

**Verify:** Enter Play mode. Point the crosshair at the actor. A highlight should appear immediately (pale-yellow overlay on UE 5.3+, wireframe box on UE 5.0–5.2), and the cursor dot should turn white.

---

## Object highlights but attention is never promoted

**Symptom:** The silhouette appears when looking at the object, but `OnAttentionGained` never fires on `UConvaiPlayerComponent`.

**Cause:** One of three conditions:

- The player is not holding gaze on the same actor/primitive long enough to reach `GazeAttentionDelay`.
- `GazeAttentionDelay` is set higher than expected.
- The Blueprint event is bound to a different `UConvaiPlayerComponent` than the one running gaze attention.

**Fix:**
1. Keep the crosshair on the same highlighted object until the full `GazeAttentionDelay` duration elapses.
2. Confirm that `GazeAttentionDelay` is not set to an unexpectedly high value.
3. Bind the diagnostic print to `OnAttentionGained` on the same `UConvaiPlayerComponent` that has **Enable Gaze Attention** checked.

**Verify:** Add a Blueprint bind to `OnAttentionGained` on `UConvaiPlayerComponent` and print a screen message. Enter Play mode and hold gaze on the object for `GazeAttentionDelay` seconds. The message should appear.

---

## Attention is promoted but the character does not speak

**Symptom:** `OnAttentionGained` fires (verified via Blueprint print), but the character is silent.

**Cause:** One of these conditions:

| Cause | How to recognize it |
|---|---|
| `GazeShouldRespond` is `Never` | Attention updates silently; no LLM reply is requested. Default on a fresh player component. |
| **Enable Actions** is off | `SetObjectInAttention` and gaze fan-out have no effect on the chatbot. |
| `AttentionSource` is `Explicit (Blueprint/C++)` | A direct `SetObjectInAttention` call holds the slot; gaze updates are rejected. |
| Session is not active | Local attention state may update but no request reaches Convai. |

**Fix:**
1. Set `GazeShouldRespond` to `Always` on `UConvaiPlayerComponent`.
2. Fill in `GazeAttentionText` with a descriptive sentence. Without text, the attention event carries no narrative context and Convai may not generate a meaningful response even when `ShouldRespond` is `Always`.
3. On the chatbot, expand **Convai | Actions** → **Environment** and confirm **Enable Actions** (`EnvironmentData.bEnableActions`) is checked.
4. During Play mode, read `AttentionSource` on `UConvaiChatbotComponent` (under **Convai | Actions**). If it shows `Explicit (Blueprint/C++)`, find the Blueprint call that set `SetObjectInAttention` and clear the slot with an empty `FConvaiObjectEntry`.
5. Confirm the chatbot session is connected. See [Session lifecycle](../../core-concepts/session-lifecycle.md) for connection diagnostics.

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

**Cause (UE 5.0–5.2):** The wireframe fallback (`DrawDebugBox`) uses `GazeHighlightColor`, but it does not use `GazeOverlayMaterial` or `GazeHighlightEmissiveIntensity`. Material-only changes have no effect on the fallback path.

**Fix:**
1. If using a custom `GazeOverlayMaterial`, confirm the material exposes a vector parameter named `EmissiveColor`. Only this parameter name is driven by the highlight system.
2. On UE 5.0–5.2, set `GazeHighlightColor` directly because the highlight appearance is limited to a wireframe box. Upgrade to UE 5.3 or later to use the overlay material system.
3. If `GazeOverlayMaterial` is unset and the UE 5.3+ silhouette is white (not pale yellow), the plugin asset `/ConvAI/Highlights/M_ConvaiGazeOverlay` may have been stripped from a cooked build. The fallback material `/Engine/EngineMaterials/EmissiveMeshMaterial` has no parameters. Re-package the plugin content.

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

**Symptom:** A `UConvaiObjectComponent` with `ObjectEntry.ComponentName` set highlights the entire actor instead of only the named sub-mesh, or the highlight does not appear at all when looking at the intended part.

**Cause:** One of four conditions:

- `ObjectEntry.MoveTargetMode` is still `Actor as goal` (the default). Gaze ignores `ComponentName` until **Move Target Mode** is `Component as goal`.
- The `ComponentName` value does not match any component on the actor (typo, renamed component, or substring mismatch).
- The component tree changed at runtime and the cached resolve is stale.
- The target sub-mesh has no collision on `GazeTraceChannel`, so the line trace never hits it.

**Fix:**
1. On the `UConvaiObjectComponent`, expand **Object Entry** and set **Move Target Mode** to `Component as goal`.
2. In Play mode, call `GetResolvedComponent(true)` on the `UConvaiObjectComponent` from Blueprint and print the return value. A `nullptr` result means the name did not resolve — check the exact component name in the Details panel hierarchy.
3. Confirm that `ObjectEntry.ComponentName` is a substring of the target component's label as shown in the **Components** panel (for example, `"Handle"` matches `SM_DoorHandle` but not `SM_Knob`).
4. If the actor's component tree is built at runtime (procedural generation, dynamic attachment), call `GetResolvedComponent(true)` after the tree is fully constructed rather than relying on the cached result from load time.
5. Confirm the target component has collision enabled on the `GazeTraceChannel`. A component with no collision will never be hit by the line trace, so the scoped match cannot fire even if the name resolves correctly.

**Verify:** After correcting **Move Target Mode** and `ComponentName`, enter Play mode and aim the crosshair at the specific sub-mesh. Only that mesh should highlight; other parts of the actor should remain unaffected. `GetResolvedComponent(false)` should return the correct component reference.

---

## Next steps

{% content-ref url="gaze-attention-quick-start.md" %}
[Gaze attention quick start](gaze-attention-quick-start.md)
{% endcontent-ref %}

{% content-ref url="how-gaze-attention-works.md" %}
[How gaze attention works](how-gaze-attention-works.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-reference.md" %}
[Gaze attention reference](gaze-attention-reference.md)
{% endcontent-ref %}

{% content-ref url="gaze-attention-usage-examples.md" %}
[Gaze attention usage examples](gaze-attention-usage-examples.md)
{% endcontent-ref %}
