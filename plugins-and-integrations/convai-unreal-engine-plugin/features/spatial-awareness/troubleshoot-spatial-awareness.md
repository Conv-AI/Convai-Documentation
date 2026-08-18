---
title: Troubleshoot spatial awareness
description: Fix a character that describes nothing, hides objects behind walls, reads everything as far away, or confuses duplicate object names.
last_reviewed: "4.0.0-beta.27"
---

Use this page to diagnose and fix the most common spatial awareness problems. Each entry follows a symptom / cause / fix / verify structure.

{% hint style="info" %}
If you have not completed the baseline setup yet, start with [Spatial awareness quick start](spatial-awareness-quick-start.md) and return here only when a specific symptom persists.
{% endhint %}

## A character describes nothing at all

**Symptom:** The **SURROUNDINGS** panel in the Convai Debug Overlay is empty for a selected chatbot, even with `UConvaiObjectComponent` Actors nearby.

**Cause:** One of these conditions:

- **Enable Spatial Awareness** (`bEnableSpatialAwareness`) is off under **Edit > Project Settings > Plugins > Convai > Spatial Awareness** — the master switch. No facts are generated for any chatbot while it is off.
- The nearby object's `UConvaiObjectComponent` has **Enabled** (`bConvaiEnabled`) unchecked, or **Include in Spatial Awareness** (`bIncludeInSpatialAwareness`) unchecked. Either one removes that single object from spatial awareness without affecting the rest of the system.
- The chatbot's own **Receive Surroundings** (`bReceiveSurroundings`) is off, under **Convai | Spatial Awareness** (Advanced Display) on the `UConvaiChatbotComponent`.

**Fix:**
1. Check **Enable Spatial Awareness** under **Edit > Project Settings > Plugins > Convai > Spatial Awareness**.
2. Select the object's `UConvaiObjectComponent` and confirm both **Enabled** and **Include in Spatial Awareness** are checked.
3. Select the chatbot's `UConvaiChatbotComponent`, expand **Convai | Spatial Awareness**, and confirm **Receive Surroundings** is checked.

**Verify:** Enter Play mode, open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md), select the chatbot, and confirm the object's row appears in **SURROUNDINGS**.

---

## Objects behind walls are still described

**Symptom:** A chatbot describes an object it should not be able to see — for example, one on the other side of a solid wall.

**Cause:** **Enable Line Of Sight** (`bEnableLineOfSight`) defaults to unchecked. With it off, every subject is described regardless of what is between it and the observer.

**Fix:** Under **Edit > Project Settings > Plugins > Convai > Spatial Awareness**, check **Enable Line Of Sight**. This adds one line trace per chatbot/subject pair on every poll, so enable it only where the cost is acceptable for your project.

**Verify:** Enter Play mode, position the chatbot so a wall blocks its view of a registered object, and confirm the object's row disappears from **SURROUNDINGS** in the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md).

---

## Everything reads "far away"

**Symptom:** Every object in the level reads as "far away" in the surroundings text, even objects that are close to the chatbot.

**Cause:** **Nearby Distance** and **Moderate Distance** are set in centimeters and default to `1000.0` cm and `4000.0` cm. A level built at a different scale (much larger rooms, a vehicle-scale map) can put every subject beyond `ModerateDistance` even at what feels like a short distance.

**Fix:** Under **Edit > Project Settings > Plugins > Convai > Spatial Awareness**, raise **Nearby Distance** and **Moderate Distance** to match your level's scale. Keep **Moderate Distance** larger than **Nearby Distance** — the values are not validated against each other.

**Verify:** Enter Play mode, stand a chatbot near a registered object, and confirm its row in **SURROUNDINGS** reads "close by" or "some distance away" rather than "far away."

---

## Relations between objects never appear

**Symptom:** Individual objects are described in **SURROUNDINGS**, but the chatbot never mentions how two objects relate to each other (for example, "the gun is on top of the crate").

**Cause:** One of these conditions:

- **Enable Relations** (`bEnableRelations`) is off under **Edit > Project Settings > Plugins > Convai > Spatial Awareness**.
- The two objects are farther apart than **Relation Cluster Distance** (`RelationClusterDistance`, default `600.0` cm).
- The chatbot's **Receive Relations** (`bReceiveRelations`) is off, under **Convai | Spatial Awareness** on the `UConvaiChatbotComponent`.

**Fix:**
1. Check **Enable Relations** under **Edit > Project Settings > Plugins > Convai > Spatial Awareness**.
2. Move the objects closer than **Relation Cluster Distance**, or raise the distance to cover them.
3. Select the chatbot's `UConvaiChatbotComponent` and confirm **Receive Relations** is checked.

**Verify:** Enter Play mode with two related objects within **Relation Cluster Distance** and confirm a relation fact for them appears — check **FACTS** in the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md).

---

## Duplicate object names confuse the character

**Symptom:** The chatbot addresses the wrong crate, or its responses show it cannot tell two same-named objects apart.

**Cause:** One of these conditions:

- The objects are meant to be told apart, but **Duplicate Name Suffix Style** (`ObjectNameSuffixStyle`) has produced a suffix the AI is not using correctly — check which style is set (`Numeric` or `Alphabetical`) under **Edit > Project Settings > Plugins > Convai > Objects**.
- The objects are meant to be treated as one thing — a pile of identical props — but **Merge With Same-Named Objects** is off on their `UConvaiObjectComponent`, so they are still being suffixed and addressed individually instead of merged.

**Fix:**
- To keep the objects distinct, confirm **Duplicate Name Suffix Style** produces names you expect, and reference an object by its full suffixed name (for example, "Crate 2") when scripting actions or dialogue that must target one specific member.
- To treat the objects as one thing, turn on **Merge With Same-Named Objects** on every member — see [Merge same-named objects](merge-same-named-objects.md).

**Verify:** Enter Play mode, open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md), and confirm **SURROUNDINGS** shows either one suffixed row per object (distinct) or a single merged row (merged), matching your intent.

---

## Spatial text is too long

**Symptom:** The context sent to Convai is noticeably larger than expected, or a chatbot's replies suggest it is receiving redundant location information.

**Cause:** **Describe From Player Perspective** (`bDescribePlayerPerspective`) adds a second clause to every spatial fact, roughly doubling its length. It defaults to checked.

**Fix:** Under **Edit > Project Settings > Plugins > Convai > Spatial Awareness**, uncheck **Describe From Player Perspective** if your chatbots do not need to give the player directions from the player's own point of view. See [Describe objects from the player's view](describe-from-player-perspective.md) for what the clause adds when it is on.

**Verify:** Enter Play mode, open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md), and confirm each row in **SURROUNDINGS** now shows only the chatbot's own frame, with no "From `<Player>`'s position, ..." clause.

---

## Next steps

{% content-ref url="how-spatial-awareness-works.md" %}
[How spatial awareness works](how-spatial-awareness-works.md)
{% endcontent-ref %}

{% content-ref url="spatial-awareness-reference.md" %}
[Spatial awareness settings reference](spatial-awareness-reference.md)
{% endcontent-ref %}

{% content-ref url="spatial-awareness-quick-start.md" %}
[Spatial awareness quick start](spatial-awareness-quick-start.md)
{% endcontent-ref %}
