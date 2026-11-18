---
title: Emotion editor windows
description: Reference for the Emotion editor window, covering its four tabs and the Emotion Timeline recorder opened from the Live tab.
last_reviewed: "4.5.0"
---

`Convai > Emotion Editor` opens a depth-only workshop for Emotion — a wider surface than the Inspector for the same character, reached from the component inspector's **Advanced settings & expressions →** link or from the menu directly. This page documents its four tabs and the Emotion Timeline window opened from the Live tab.

***

## Open the window

`Convai > Emotion Editor` (`ConvaiEmotionEditorWindow`, window title **Convai Emotions**) opens the window, already showing whichever `ConvaiEmotionController` is selected in the scene, or the first one found. The component inspector's **Advanced settings & expressions →** link opens the same window already targeting that character. Opening the window is never a required step — the Inspector carries the common setup path on its own; this window carries everything that does not fit there.

The left pane lists every `ConvaiEmotionController` in the open scenes with a status dot — **Ready**, **Needs attention**, or **Not set up** — so a scene of characters can be swept without hunting through the Hierarchy.

***

## The four tabs

| Tab | What it shows |
| --- | --- |
| **Setup** | The same setup checklist the Inspector shows, full width, plus every finding with its fix. |
| **Feel** | Every setting on the assigned `ConvaiEmotionProfile`, grouped into sections — the complete surface behind the Inspector's handful of controls. |
| **Expressions** | What Convai resolved on this character's own face — naming convention, match confidence, and shape counts per mesh — followed by the authored expression recipes and material effects. |
| **Live** | The character's current feeling, strength, held-for duration, resting mood, mouth influence, and a bar per emotion carrying a non-zero score. Available only in Play mode. |

A character with no `ConvaiEmotionProfile` assigned shows a **No personality assigned** message on **Feel** and **Expressions** instead of empty fields, since there is nothing on that character to tune yet.

***

## Emotion Timeline window

The **Open Emotion Timeline** button on the **Live** tab opens `ConvaiEmotionTimelineWindow` (window title **Emotion Timeline**) already watching the character selected in the Emotion editor window. It has no menu item of its own — the timeline only makes sense once a character is already picked, which the Live tab has already done.

The timeline plots a Play-mode recording of one character's emotion life over time: one line per taxonomy label's output score, the resting mood score drawn as a separate emphasized line, and vertical markers wherever `DominantEmotionChanged` or `MoodChanged` fires. Assign a target, then:

| Control | What it does |
| --- | --- |
| **Start** | Begins recording. Only available in Play mode with a target assigned. |
| **Stop** | Ends the capture without discarding it. |
| **Clear** | Empties the plot. |

Samples are pulled from the target's public `Current` reading at a fixed sampling interval — the recorder never touches per-frame runtime state directly. Use the timeline to tune a character's temperament by eye, or to debug a reported "the mood feels wrong" session after the fact.

{% hint style="info" %}
The timeline is editor-only tooling. It has no runtime API and changes nothing about how a character behaves in a build.
{% endhint %}

***

## Next steps

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Emotion quick start](quick-start.md)
{% endcontent-ref %}
