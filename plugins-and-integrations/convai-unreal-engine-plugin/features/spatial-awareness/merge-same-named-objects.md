---
title: Merge same-named objects
description: Merge a pile of identically named objects, like a stack of crates, so a character perceives the whole set as one logical thing.
last_reviewed: "4.0.0-beta.27"
---

By default, `UConvaiObjectComponent` instances that share a name stay distinct — the second and later duplicates get a name suffix so the AI can still address each one individually. For a pile of props a character should treat as one thing — a stack of crates, a row of pressure plates — turn on **Merge With Same-Named Objects** instead. This guide merges a set of same-named objects and shows you how to confirm the merge in the overlay.

## Prerequisites

- Two or more Actors in the level, each with a `UConvaiObjectComponent`, sharing the same `Name` in **Object Entry** (case-insensitive).
- Spatial awareness is enabled for the project — see [Spatial awareness quick start](spatial-awareness-quick-start.md).

## What merging changes

Turning on **Merge With Same-Named Objects** on every member of the set changes how the AI perceives them:

- Its position is the average of all members' positions.
- Gazing at any one member highlights the whole set together, unless you opt a member out.
- The AI receives one description for the whole set — the first non-empty **Description** among the members, so you only need to fill it in on one of them.
- Members are not suffixed apart from one another — they share one name on purpose. If the name still collides with a separate merged set or a non-merged object, the whole merged set gets a single shared suffix to stay addressable.

Leaving **Merge With Same-Named Objects** off (the default) keeps same-named objects distinct, disambiguated by **Duplicate Name Suffix Style** instead — see [Spatial awareness settings reference](spatial-awareness-reference.md).

## Merge a set of objects

{% stepper %}
{% step %}
### Give every member the same Object Entry name

On each `UConvaiObjectComponent` in the set, expand **Object Entry** and set the same **Name** — for example, `Crate` on every crate in the pile.
{% endstep %}

{% step %}
### Turn on Merge With Same-Named Objects

On each of those components, expand **Convai | Object | Grouping** and check **Merge With Same-Named Objects** (`bMergeWithSameNamedObjects`). It defaults to unchecked.
{% endstep %}

{% step %}
### Set Merge Group Index if you have more than one set

If the level has two separate piles that both share the same object name and should merge independently, set **Merge Group Index** (`MergeGroupIndex`, default `0`) to a different value on each pile's members. Objects only merge when they share both the same **Name** and the same **Merge Group Index**. Leave it at `0` for the common case of a single pile.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
**Merge Group Index** only has an effect while **Merge With Same-Named Objects** is on — it is greyed out otherwise.
{% endhint %}

## Choose the highlight behavior

By default, gazing at any one member of a merged set highlights every member together. To highlight only the specific object the player is looking at instead — while the whole set still enters the AI's attention as one logical object — check **Highlight Only This Object When Gazed** (`bHighlightOnlyThisWhenGazed`) under **Convai | Object | Gaze** on that member. This setting only changes the visual highlight; it is purely cosmetic and has no effect on non-merged objects.

## Verify the merge

Enter Play mode and open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md) with **Ctrl+Alt+K**. Select the chatbot and check the **SURROUNDINGS** panel: the merged set should appear as a single row under the shared name, not one row per crate. Its position should read from a point roughly in the middle of the pile.

## Next steps

{% content-ref url="how-spatial-awareness-works.md" %}
[How spatial awareness works](how-spatial-awareness-works.md)
{% endcontent-ref %}

{% content-ref url="spatial-awareness-reference.md" %}
[Spatial awareness settings reference](spatial-awareness-reference.md)
{% endcontent-ref %}
