---
title: Describe objects from the player's view
description: Make a character describe its surroundings from the player's own camera frame instead of its own, so it can give directions.
last_reviewed: "4.0.0-beta.27"
---

By default, every spatial fact a chatbot receives is written in the chatbot's own frame — "the crate is close by, in front of you" means in front of the character. **Describe From Player Perspective** adds a second clause, in the player's frame instead, so a character can tell the player where something is relative to the player's own point of view without doing the rotation itself. This guide turns that clause on and shows you how to confirm it in the overlay.

## Prerequisites

- Spatial awareness is enabled for the project — see [Spatial awareness quick start](spatial-awareness-quick-start.md).
- A `UConvaiPlayerComponent` is present on the player pawn, so there is a player camera frame to describe from.

## What the setting does

`bDescribePlayerPerspective` is a project-wide setting on `UConvaiSettings` — it applies to every chatbot's surroundings facts, not one character at a time. When it is on, each fact carries an extra clause that names the player and the direction explicitly, for example:

> "From Eshmawy's position, the crate is close by, ahead and to the left."

The player-perspective clause is never dropped by distance: a far subject still degrades to a bare "far away" in that clause rather than being omitted, so an earlier "close by" reading cannot linger as stale information once the player moves away.

## Turn on Describe From Player Perspective

{% stepper %}
{% step %}
### Open the Spatial Awareness settings

Go to **Edit > Project Settings > Plugins > Convai** and expand the **Spatial Awareness** category.
{% endstep %}

{% step %}
### Check Describe From Player Perspective

**Describe From Player Perspective** (`bDescribePlayerPerspective`) defaults to checked. If it has been turned off in your project, check it now. The setting has the edit condition `bEnableSpatialAwareness`, so the master switch must be on first.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
This clause roughly doubles the length of the spatial text delivered to every chatbot. Turn it off for characters that never need to give the player directions.
{% endhint %}

## Verify in the Convai Debug Overlay

Enter Play mode, open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md) with **Ctrl+Alt+K**, and select a chatbot that has `bReceiveSurroundings` on.

Check the **SURROUNDINGS** panel for an object near the player. The row's sentence should now contain two clauses: the chatbot's own frame first, followed by the "From `<Player>`'s position, ..." clause. Move the player to a different position relative to the object and confirm the second clause updates on the next poll.

## Next steps

{% content-ref url="how-spatial-awareness-works.md" %}
[How spatial awareness works](how-spatial-awareness-works.md)
{% endcontent-ref %}

{% content-ref url="spatial-awareness-reference.md" %}
[Spatial awareness settings reference](spatial-awareness-reference.md)
{% endcontent-ref %}
