---
title: Troubleshoot character movement
last_reviewed: "4.0.0-beta.27"
description: Diagnose why Convai Move To or Convai Escort fails, reports an unexpected result code, or never reaches its destination.
---

Use this page to diagnose `Convai Move To` and `Convai Escort` failures by the **Result Code** each node reports on its **Succeeded** or **Failed** pin. Each entry follows a symptom / cause / fix / verify structure.

{% hint style="info" %}
If you have not wired the nodes yet, start with [Move a character to an object](move-a-character-to-an-object.md) or [Escort a character](escort-a-character.md) and return here only when a specific result code persists.
{% endhint %}

## Before you start

- Open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md) and select the moving character. The **SURROUNDINGS** panel shows `— reached` or `— no path` for the destination object, which narrows most result codes before you touch a Blueprint graph.
- Confirm the moving pawn's **AI Controller**, movement component, and path-following component are all present — three of the result codes below exist specifically to name whichever one is missing.

## Convai Move To reports `Unknown Destination`

**Symptom:** `Convai Move To` fires **Failed** with **Result Code** `Unknown Destination`.

**Cause:** The destination actor referenced by `Destination.Ref` disappeared or could not be resolved.

**Fix:**
1. Confirm the actor set on **Destination** still exists in the level at the time the node fires.
2. If the actor is spawned or destroyed dynamically, make sure the reference is set after the actor exists and cleared before it is destroyed.

**Verify:** Trigger the move again with a live actor reference. **Result Code** should no longer read `Unknown Destination`.

## Convai Move To reports `Unreachable`

**Symptom:** `Convai Move To` fires **Failed** with **Result Code** `Unreachable`.

**Cause:** The destination is known, but no navmesh path reaches it from the character's current position — commonly no NavMesh coverage over the route, or every authored movement point is blocked.

**Fix:**
1. Add or extend a **Nav Mesh Bounds Volume** over the route and the destination.
2. If the destination uses movement points, check whether every enabled point is blocked. Either clear the obstruction or enable **Use Object as Fallback** on the destination's `FConvaiObjectEntry` so resolution falls back to the object itself when every point is unreachable.
3. Open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md) and check the destination's row in **SURROUNDINGS** for `— no path`.

**Verify:** Trigger the move again. **SURROUNDINGS** should show `— reached` once the character arrives, and **Result Code** should read `Reached`.

## Convai Move To reports `Invalid Character`

**Symptom:** `Convai Move To` fires **Failed** with **Result Code** `Invalid Character`.

**Cause:** `Moving Actor` is not a usable pawn.

**Fix:** Confirm **Moving Actor** is wired to a `Pawn` (or subclass, such as `Character`) actor reference, not a static mesh actor or another non-pawn type.

**Verify:** Trigger the move again with a valid pawn reference.

## Convai Move To reports `Missing AI Controller`

**Symptom:** `Convai Move To` fires **Failed** with **Result Code** `Missing AI Controller`.

**Cause:** The pawn set as **Moving Actor** is not controlled by an AI Controller.

**Fix:** Assign an `AAIController` (or subclass) to the pawn — either set **Auto Possess AI** on the pawn to spawn one automatically, or possess it explicitly at runtime.

**Verify:** Confirm the pawn's controller is an AI Controller, then trigger the move again.

## Convai Move To reports `Missing Movement Component`

**Symptom:** `Convai Move To` fires **Failed** with **Result Code** `Missing Movement Component`.

**Cause:** The pawn has no movement component.

**Fix:** Add a movement component to the pawn — for a `Character`, this is `CharacterMovementComponent`, added by default; for a custom `Pawn`, add a compatible movement component such as `FloatingPawnMovement`.

**Verify:** Confirm the pawn's **Components** panel lists a movement component, then trigger the move again.

## Convai Move To reports `Missing Path Following Component`

**Symptom:** `Convai Move To` fires **Failed** with **Result Code** `Missing Path Following Component`.

**Cause:** The pawn's AI Controller has no path-following component.

**Fix:** Confirm the AI Controller is a standard `AAIController` (or subclass that retains its default path-following component) rather than a custom controller that removed it.

**Verify:** Trigger the move again after confirming the AI Controller's setup.

## Convai Move To reports `Missing Navigation Data`

**Symptom:** `Convai Move To` fires **Failed** with **Result Code** `Missing Navigation Data`.

**Cause:** The world has no compatible navigation data for this pawn — typically no `RecastNavMesh` actor exists, or it does not cover the pawn's navigation agent properties.

**Fix:**
1. Add a **Nav Mesh Bounds Volume** to the level if one does not exist.
2. Confirm the pawn's navigation agent properties (radius, height) match a navigation data instance in the level.

**Verify:** Trigger the move again once NavMesh coverage exists for the pawn.

## Convai Move To reports `Move Failed`

**Symptom:** `Convai Move To` fires **Failed** with **Result Code** `Move Failed`.

**Cause:** Unreal stopped the move even though the destination still resolved as reachable — for example, the pawn got physically stuck, or the underlying engine move request was interrupted.

**Fix:**
1. Check for obstructions or collision issues along the resolved path.
2. Confirm nothing else in the character's Blueprint is issuing a competing move or stop request while `Convai Move To` is active.

**Verify:** Trigger the move again in a clear path. **Result Code** should read `Reached`.

## Convai Move To reports `Already At Destination` unexpectedly

**Symptom:** `Convai Move To` fires **Succeeded** immediately with **Result Code** `Already At Destination`, but you expected the character to walk somewhere.

**Cause:** The character is already within `max(Acceptance Radius, 150 cm)` of a movement point, or `max(Acceptance Radius × 2, 150 cm)` of the object's bounding-box footprint when no movement points are authored.

**Fix:** If the character should walk a visible distance, increase **Acceptance Radius** on the destination's `FConvaiObjectEntry`, or reposition the character or the destination so they start further apart.

**Verify:** Trigger the move again. **Result Code** should read `Reached` after visible movement.

## Convai Escort reports `Character Unavailable`

**Symptom:** `Convai Escort` fires **Failed** with **Result Code** `Character Unavailable`.

**Cause:** `Escorted Character` disappeared or is not a valid escort target.

**Fix:** Confirm the actor referenced by **Escorted Character** still exists and is a valid pawn at the time the node fires.

**Verify:** Trigger the escort again with a live escorted-character reference.

## Convai Escort reports `Destination Unavailable`

**Symptom:** `Convai Escort` fires **Failed** with **Result Code** `Destination Unavailable`.

**Cause:** `Destination` disappeared or could not be reached from the guiding character's current position — the same reachability conditions as `Convai Move To`'s `Unreachable`.

**Fix:** Apply the same checks as [Convai Move To reports `Unreachable`](#convai-move-to-reports-unreachable) — NavMesh coverage, blocked movement points, and **Use Object as Fallback**.

**Verify:** Trigger the escort again. Both actors should reach the destination and **Result Code** should read `Reached`.

## Convai Escort reports `Invalid Escort Setup`

**Symptom:** `Convai Escort` fires **Failed** with **Result Code** `Invalid Escort Setup`.

**Cause:** `Escorting Actor` is missing setup required by escort — for example, no AI Controller, the same prerequisite `Convai Move To` needs.

**Fix:** Confirm **Escorting Actor** meets the same prerequisites as `Convai Move To`'s **Moving Actor**: an AI Controller, a movement component, and a path-following component.

**Verify:** Trigger the escort again after confirming the guiding character's setup.

## Convai Escort reports `Movement Failed`

**Symptom:** `Convai Escort` fires **Failed** with **Result Code** `Movement Failed`.

**Cause:** Unreal stopped the owned movement before the escort reached its destination.

**Fix:** Apply the same checks as [Convai Move To reports `Move Failed`](#convai-move-to-reports-move-failed) — obstructions, collision, or a competing move request on the guiding character.

**Verify:** Trigger the escort again in a clear path.

## Still blocked

If a result code is not listed here, or the character stops mid-move without reporting one, open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md), select the character, and check its action queue and results ribbon for the exact failure note. Include the **Result Code**, **Additional Note**, and a description of the level's NavMesh coverage when reporting the issue.

## Related pages

{% content-ref url="movement-blueprint-reference.md" %}
[Movement Blueprint reference](movement-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="how-character-movement-works.md" %}
[How character movement works](how-character-movement-works.md)
{% endcontent-ref %}

{% content-ref url="../../troubleshooting/convai-debug-overlay.md" %}
[Inspect a character with the Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md)
{% endcontent-ref %}
