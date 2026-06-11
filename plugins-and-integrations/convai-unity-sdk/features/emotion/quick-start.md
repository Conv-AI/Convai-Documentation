---
title: Emotion quick start
description: >-
  Build a working emotion pipeline on a Convai NPC — attach the Emotion
  Controller, assign the bundled sample profile, and verify expressions in Play
  Mode.
last_reviewed: "4.2.0"
---

We will attach the Emotion Controller to an NPC, assign the bundled sample profile, and see the character's face react to live AI emotion signals in Play Mode. No custom assets are required for the initial setup.

## Prerequisites

Before starting, verify:

* [ ] A `ConvaiCharacter` is in the scene and responds to speech in Play Mode

## Set up the Emotion Controller

{% stepper %}
{% step %}
### Add the Emotion Controller

Select your NPC's root GameObject in the Hierarchy. In the Inspector, click **Add Component** and search for **Emotion Controller**, or navigate to **Convai → Embodiment → Emotion Controller**.

The component appears with a **Profile** field that is currently empty.

<figure><img src="../../../../.gitbook/assets/image (497).png" alt="Unity Inspector showing ConvaiEmotionController added to the NPC root GameObject with the Profile field empty, ready for a profile asset to be assigned"><figcaption><p>ConvaiEmotionController added to the NPC root — the Profile field is empty until an EmotionProfile asset is assigned in step 3. No blendshape mapping is active yet.</p></figcaption></figure>
{% endstep %}

{% step %}
### Locate the bundled sample profile

In the Project window, navigate to:

{% code overflow="wrap" %}
```text
Packages / Convai SDK for Unity / SamplesShared / Resources / Embodiment / Modules / Emotion
```
{% endcode %}

You will find two assets:

| Asset                                 | Purpose                                                                                                                        |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `ConvaiSamplesShared_EmotionProfile`  | Pre-configured expression slots for Reallusion characters, with smoothing, micro-burst, and neutral alternation already tuned. |
| `ConvaiSamplesShared_EmotionTaxonomy` | The default emotion vocabulary, already referenced by the profile above.                                                       |
{% endstep %}

{% step %}
### Assign the profile

Drag `ConvaiSamplesShared_EmotionProfile` from the Project window into the **Profile** field on the `ConvaiEmotionController` component.

<figure><img src="../../../../.gitbook/assets/image (508).png" alt="Unity Inspector showing ConvaiEmotionController with ConvaiSamplesShared_EmotionProfile assigned to the Profile field"><figcaption><p>ConvaiSamplesShared_EmotionProfile assigned — the controller is now configured with pre-tuned expression slots for Reallusion characters and will begin driving blendshapes as soon as Play Mode starts.</p></figcaption></figure>

{% hint style="warning" %}
The bundled asset is **read-only** — it lives inside the package. To adjust any settings, duplicate it first (**Ctrl+D** on Windows / **Cmd+D** on macOS), move the copy into your own `Assets/` folder, and assign the copy instead.
{% endhint %}
{% endstep %}

{% step %}
### Enable emotion detection on connect

On the same NPC root GameObject, open the `ConvaiCharacter` component. In the **EMOTION** section, set **Detection Source** to **Llm**.

Use **Llm** for the first setup. Use **Nrclex** only when you want to tune local text-analysis thresholds before the session connects.
{% endstep %}

{% step %}
### Enter Play Mode and speak

Press **Play**. Talk to the character using your configured microphone. As the AI responds, watch the `ConvaiEmotionController` in the Inspector — the **Current** reading updates live.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Expected result:** The NPC's facial expression changes as the conversation develops. The **Current → Dominant Label** field shows the active emotion and **Current → Dominant Score** shows its smoothed intensity. If you are using a Reallusion character with the default rig, blendshapes activate on the character's face immediately.
{% endhint %}

## How it works

When you spoke to the character, `ConvaiCharacter` sent `emotion_config.provider = "llm"` on room connect. Convai then streamed `bot-emotion` messages during responses. `ConvaiEmotionController` received each emotion signal, resolved it through the taxonomy (mapping `"serenity"` to `"joy"`), smoothed the intensity score over time, and wrote the score to the character's facial blendshapes every frame. For a full explanation of every stage, see [How the emotion system works](how-the-emotion-system-works.md).

The bundled profile is configured for Reallusion characters. For other rigs, duplicate the profile and update the blendshape names in each slot to match your character's shapes. See [Emotion profile](emotion-profile.md) and [Emotion output bindings](output-bindings.md) for how to configure slots for any rig.

## Next steps

The quick start runs end-to-end with the bundled profile. These pages cover tuning and extending the setup.

{% content-ref url="how-the-emotion-system-works.md" %}
[How the emotion system works](how-the-emotion-system-works.md)
{% endcontent-ref %}

{% content-ref url="emotion-profile.md" %}
[Emotion profile](emotion-profile.md)
{% endcontent-ref %}

{% content-ref url="output-bindings.md" %}
[Emotion output bindings](output-bindings.md)
{% endcontent-ref %}

{% content-ref url="scripting-api.md" %}
[Emotion scripting API](scripting-api.md)
{% endcontent-ref %}
