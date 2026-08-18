---
title: Spatial awareness quick start
description: Turn on spatial awareness, tune the distance bands for your level's scale, and confirm what a character actually receives.
last_reviewed: "4.0.0-beta.27"
---

This guide turns on spatial awareness for your project, tunes the distance bands to match your level's scale, and confirms — with the Convai Debug Overlay — that a chatbot actually receives the sentences the system generates.

## Prerequisites

- The Convai Unreal Engine plugin is installed.
- At least one `UConvaiChatbotComponent` is placed in the level.
- At least one other Actor in the level has a `UConvaiObjectComponent`, so there is something for the chatbot to be told about.

## Confirm the master switch is on

{% stepper %}
{% step %}
### Open Project Settings

Go to **Edit > Project Settings > Plugins > Convai** and expand the **Spatial Awareness** category.
{% endstep %}

{% step %}
### Confirm Enable Spatial Awareness is checked

**Enable Spatial Awareness** (`bEnableSpatialAwareness`) defaults to checked. If it is unchecked, no proximity, line-of-sight, or relation facts are generated for any chatbot in the project — check it now.
{% endstep %}
{% endstepper %}

## Tune the distance bands for your level's scale

Spatial awareness buckets every subject a chatbot can perceive into "close by," "some distance away," or "far away" using two thresholds, both in centimeters. The defaults assume a human-scale level; a much larger or smaller level needs different values.

{% stepper %}
{% step %}
### Set Nearby Distance

**Nearby Distance** (`NearbyDistance`, default `1000.0` cm) is the ceiling under which a subject reads as "close by." Set it to roughly the range at which a character in your level should treat something as within arm's reach or a few steps away.
{% endstep %}

{% step %}
### Set Moderate Distance

**Moderate Distance** (`ModerateDistance`, default `4000.0` cm) is the ceiling under which a subject reads as "some distance away." Beyond it, a subject reads "far away." Keep `ModerateDistance` larger than `NearbyDistance` — the system does not enforce the ordering for you.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
Both distances have the edit condition `bEnableSpatialAwareness`, so they are greyed out until the master switch is on.
{% endhint %}

## Confirm the chatbot is set to receive surroundings

The project settings above decide what the spatial system computes; each chatbot's own preferences decide what it actually receives.

{% stepper %}
{% step %}
### Select the chatbot's Convai Chatbot component

In the character Blueprint or level Actor, select the `UConvaiChatbotComponent`.
{% endstep %}

{% step %}
### Confirm Receive Surroundings is on

Expand **Convai | Spatial Awareness** (Advanced Display) and confirm `bReceiveSurroundings` is checked. It defaults to `true`. If it is off, this chatbot never receives surroundings facts regardless of the project settings above.
{% endstep %}
{% endstepper %}

## Verify what the character receives

Enter Play mode, open the [Convai Debug Overlay](../../troubleshooting/convai-debug-overlay.md) with **Ctrl+Alt+K**, and select the chatbot.

Check the **SURROUNDINGS** panel for the object with the `UConvaiObjectComponent` from your prerequisites. Its row shows the verbatim sentence the chatbot receives — for example, "the crate is close by, in front of you." This is the exact text delivered to Convai, not a summary, so it is the fastest way to confirm your distance-band tuning produced the phrasing you expect.

{% hint style="success" %}
If the row shows the object at the wrong band, adjust `NearbyDistance` or `ModerateDistance` and re-enter Play mode to see the change reflected immediately.
{% endhint %}

For every panel, glyph, and label the overlay shows, see [Convai Debug Overlay reference](../../troubleshooting/convai-debug-overlay-reference.md).

## Next steps

{% content-ref url="how-spatial-awareness-works.md" %}
[How spatial awareness works](how-spatial-awareness-works.md)
{% endcontent-ref %}

{% content-ref url="spatial-awareness-reference.md" %}
[Spatial awareness settings reference](spatial-awareness-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-spatial-awareness.md" %}
[Troubleshoot spatial awareness](troubleshoot-spatial-awareness.md)
{% endcontent-ref %}
