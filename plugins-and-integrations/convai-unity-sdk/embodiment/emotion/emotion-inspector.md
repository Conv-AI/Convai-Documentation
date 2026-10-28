---
title: Emotion Inspector
description: Find the Emotion Controller's setup, personality, live readings, detection, expression hold, and action outcome controls in Unity.
last_reviewed: "5.0.0-preview"
---

Use the Emotion Controller Inspector for character setup and everyday tuning. Open **Advanced settings & expressions →** for the selected character's full [Emotion Editor](emotion-editor.md).

## Setup and Personality

The checklist shows **Character**, **Face**, **Face Rig**, and **Personality**. A missing owning `ConvaiCharacter` or skinned facial mesh with blendshapes blocks **Set Up Emotions**. An unrecognized Face Rig allows limited output; add a custom rig convention map before expecting complete expressions.

Choose **Composed**, **Warm**, **Energetic**, or **Reserved** under **Character Type**. The setup picker starts on Warm. Setup creates and assigns a project personality asset. An empty **Personality** field instead reports **Using SDK Defaults** and runs a hidden Composed profile at runtime, resting at `trust` with strength `0.45`.

Editing a package-owned personality through the character creates and assigns a project copy. A shared project asset can affect several characters; use **Make Unique** before changing only this one. See [Asset ownership](../../core-concepts/asset-ownership.md).

## Live

In Play mode, the live row shows:

| Reading | Meaning |
| --- | --- |
| **Feeling** | Dominant canonical transient emotion |
| **Strength** | Its smoothed score from 0 to 1 |
| **Mood** | Resting mood, tracked independently |
| **Held For** | Seconds the dominant label has remained active |

Choose an expression and strength, then select **Try It** to hold it. Select **Stop** to release it before testing conversation. These buttons are disabled outside Play mode. To inspect all emotion scores, open **Emotion Editor → Live → Everything it is feeling**, or read `Current.AllScores` from code.

{% hint style="warning" %}
**Screenshot required before publishing:** capture a configured character's Emotion Controller in Play mode with **Live** expanded, showing Feeling, Strength, Mood, Held For, and the Try It/Stop row. Include the Personality field, without unrelated components or identifying character data.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-emotion-inspector.png" alt="Placeholder: Emotion Controller Inspector with Personality and Play-mode Live controls"><figcaption><p>Capture pending: live expression readings and the temporary expression test.</p></figcaption></figure>

## Advanced

| Control | Use |
| --- | --- |
| **Emotion detection** | Choose **Off**, **Responsive**, or **Accurate**. The mode is read when connecting. Responsive is the default; Off disables conversation-driven emotion detection. |
| **Hold one expression** | Serialize a fixed expression for testing or cutscenes. **Expression** chooses the label; **How strong** sets intensity. It takes effect in Play mode and ignores incoming emotion while held. |
| **Mood after actions** | Set brief success/failure moods. Requires an Action Runner with performance reactions enabled; the controls are disabled when no Action Runner exists. |

The persistent hold is different from authoring a resting mood: a held transient expression ignores incoming emotion, while a resting mood remains underneath changing conversation reactions. See [Moods](moods.md) for the outcome controls and mood precedence.

## Findings and fixes

The Inspector and Editor Setup tab report the same actionable findings. **Emotions are switched off** offers **Turn Emotions On**. **Conversation reactions will never show** offers **Keep The Face Alive** because the reactions require the small-movements layer. Read [Troubleshoot emotion](troubleshooting-and-diagnostics.md) for the complete finding table.

## Next steps

{% content-ref url="emotion-profile.md" %}
[Emotion profile](emotion-profile.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}
