---
title: Emotion editor windows
description: Reference for the Emotion editor window, covering its four tabs and the Emotion Timeline recorder opened from the Live tab.
last_reviewed: "5.0.0-preview"
---

`Convai > Emotion Editor` opens the detailed Emotion editor for a character, reached from the component inspector's **Advanced settings & expressions →** link or from the menu directly. This page documents its four tabs and the Emotion Timeline window opened from the Live tab.

***

## Open the window

`Convai > Emotion Editor` (`ConvaiEmotionEditorWindow`, window title **Convai Emotions**) opens the window, targeting the first `ConvaiEmotionController` found in the open scenes. The component inspector's **Advanced settings & expressions →** link opens the same window already targeting that character. Opening the window is never a required step — the Inspector carries the common setup path on its own; this window carries everything that does not fit there.

Choose a character in the **CHARACTERS** pane to change the target. The left pane lists every `ConvaiEmotionController` in the open scenes with a status dot — **Ready**, **Needs attention**, or **Not set up** — so a scene of characters can be swept without hunting through the Hierarchy.

***

## The four tabs

| Tab | What it shows |
| --- | --- |
| **Setup** | The same setup checklist the Inspector shows, full width, plus every finding with its fix. |
| **Feel** | Every setting on the assigned `ConvaiEmotionProfile`, grouped into sections — the complete surface behind the Inspector's handful of controls. |
| **Expressions** | What Convai resolved on this character's own face — naming convention, match confidence, and shape counts per mesh — followed by the authored expression recipes and material effects. |
| **Live** | The character's current feeling, strength, held-for duration, resting mood, mouth influence, and a bar per emotion carrying a non-zero score. Readings require Play mode. Outside Play mode this tab shows a prompt and still offers **Open Emotion Timeline**. |

The **Feel** tab starts with **Character Type**, followed by the complete profile sections. Editing a package-owned profile through **Feel** or **Expressions** creates a project copy and assigns it to the selected character. A shared project profile remains shared unless you choose **Make Unique**.

A character with no `ConvaiEmotionProfile` assigned shows a **No personality assigned** message on **Feel** and **Expressions** instead of empty fields, since there is nothing on that character to tune yet.

***

## Emotion Timeline window

The **Open Emotion Timeline** button on the **Live** tab opens `ConvaiEmotionTimelineWindow` (window title **Emotion Timeline**) already watching the character selected in the Emotion editor window. It has no menu item of its own — the timeline only makes sense once a character is already picked, which the Live tab has already done.

The timeline plots a Play-mode recording of one character's emotion life over time: one line per taxonomy label's output score, the resting mood score drawn as a separate emphasized line, and vertical markers wherever `DominantEmotionChanged` or `MoodChanged` fires. Assign a target, then:

| Control | What it does |
| --- | --- |
| **Character** / **Use Selection** | Choose the controller directly or resolve it from the Hierarchy selection. |
| **Start** / **Stop** | One button begins or stops recording; Start requires a target. Recording controls appear in Play mode. Stopping retains the samples. |
| **Window** | Display the most recent 5–60 seconds; the default is 20 seconds. |
| **Clear** | Empties the plot. |

Samples are pulled from the target's public `Current` reading at a 0.1-second sampling interval, retaining up to 600 samples in memory — the recorder never touches per-frame runtime state directly. Use the timeline to tune a character's temperament by eye, or to debug a reported "the mood feels wrong" session after the fact.

{% hint style="info" %}
The timeline is editor-only tooling. It has no runtime API and changes nothing about how a character behaves in a build.
{% endhint %}

***

{% hint style="warning" %}
**Screenshot required before publishing:** capture **Convai > Emotion Editor**, select a configured test character in **CHARACTERS**, and show **Feel** with **Character Type** and the profile sections. Use the exact 5.0 preview UI and keep project paths and credentials out of view.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-emotion-editor.png" alt="Placeholder: Emotion Editor Feel tab with selected character and Character Type controls"><figcaption><p>Capture pending: the Emotion Editor's character and personality controls.</p></figcaption></figure>

## Next steps

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[Emotion quick start](quick-start.md)
{% endcontent-ref %}
