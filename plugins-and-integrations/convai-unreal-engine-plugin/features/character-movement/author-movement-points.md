---
title: Author movement points
last_reviewed: "4.0.0-beta.27"
description: >-
  Place named destinations on a Convai Object Component using the viewport
  visualizer or the Details panel, so characters approach it correctly.
---

Movement points are designer-authored access points that describe where a character should stand when it approaches an object — for example, one point on each side of a door. Place them on a `Convai Object Component` either directly in the viewport or through the **Details** panel.

## Prerequisites

- The target actor has a `Convai Object Component` added.
- You can select the actor (or, when editing a Blueprint, the component) in the level or Blueprint editor.

## Add movement points in the viewport

{% stepper %}
{% step %}
### Select the object

Select the actor carrying the `Convai Object Component` in the level, or select the component itself while editing its owning Blueprint. Every existing movement point draws as a grab handle: a vertical pin topped with a colored point, an acceptance-radius ring, and a tether line to the object. Spring green means the point is enabled, grey means disabled, and white marks the currently selected point.
{% endstep %}

{% step %}
### Add a point in the Details panel

In the **Details** panel, expand **Convai | Object**, then **Movement Points**, and click **Add Element**. A new point appears at the object's location with **Enabled** checked and **Attachment** set to `Relative To Object`.
{% endstep %}

{% step %}
### Position the point

Click the new point's grab handle in the viewport. This normalizes the selection to the owning actor so the transform gizmo appears, positioned at the point. Drag the gizmo to place the point where the character should stand. Each point's index and name (`[0]`, `[1] Other Side`, and so on) is labeled above its handle so you can tell which array element you are editing.
{% endstep %}

{% step %}
### Set how the point tracks the object

On the point's entry in **Movement Points**, set **Attachment**:

- `Relative To Object` (default) — the point moves with the object. Right for most cases, such as a door's approach points.
- `Keep World Position` — the point stays fixed in world space even if the object moves. Right for something like an elevator's floor landings, which must stay put while the platform rides between them.

Switching between the two converts the stored position for you, so the point does not jump.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
An acceptance-radius ring is drawn around every point, sized to the object entry's **Acceptance Radius** (or 150 cm, whichever is larger — the resolver never tests a tighter tolerance than that).
{% endhint %}

## Turn a point into its own destination

By default, a movement point is one of several places to stand when a character is sent to the object itself. To let a character be sent to that exact point by name instead:

{% stepper %}
{% step %}
### Enable Create Separate Destination

On the point's entry, check **Create Separate Destination** (`bCreatesSeparateDestination`).
{% endstep %}

{% step %}
### Name the destination

Fill in **Destination Name**. The character addresses it as `"<Object> <Destination Name>"` — a point named `Other Side` on an object named `Door` becomes `"Door Other Side"`. Keep the name short: the character says it out loud.
{% endstep %}
{% endstepper %}

## Disable a point without deleting it

Untick **Enabled** on a point's entry. A disabled point is never selected during destination resolution — characters are not sent there — but it stays in the list for later reuse. If every point on an entry is disabled, the object behaves as if it had no movement points at all, and movement falls back to the object reference.

## Verify the points

Enter Play mode and send a character to the object with [Move a character to an object](move-a-character-to-an-object.md) or [Escort a character](escort-a-character.md). The character should walk to the reachable point with the shortest walking path, not the object's raw location.

{% hint style="success" %}
Open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md) and look for a `◇` marker over each named, enabled movement point in world space — it confirms the point is registered and enabled.
{% endhint %}

## Next steps

{% content-ref url="how-character-movement-works.md" %}
[How character movement works](how-character-movement-works.md)
{% endcontent-ref %}

{% content-ref url="movement-blueprint-reference.md" %}
[Movement Blueprint reference](movement-blueprint-reference.md)
{% endcontent-ref %}
