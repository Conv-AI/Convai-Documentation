---
title: Emotion quick start
description: >-
  Enable emotion detection, attach the Emotion Controller, assign the sample
  profile, and verify expression output in Play Mode.
---

We will enable emotion detection, attach the Emotion Controller to an NPC, assign the bundled sample profile, and see the character's face react to live Convai emotion signals in Play Mode. No custom assets are required for the initial setup.

## Prerequisites

Before starting, verify:

* [ ] A `ConvaiCharacter` is in the scene and responds to speech in Play Mode

## Set up the Emotion Controller

{% stepper %}
{% step %}
### Enable emotion detection

Select the GameObject with `ConvaiCharacter`. In the Inspector, open **Emotion Detection (Connection Request)** and set **Detection Source** to `Llm` or `Nrclex`.

Use `Llm` when you want Convai to classify emotion with the conversation model. Use `Nrclex` when you want the `nrclex` provider and local threshold fields. `Disabled` sends no `emotion_config`, so Convai will not send live emotion events for that character session.
{% endstep %}

{% step %}
### Add the Emotion Controller

Select your NPC's root GameObject in the Hierarchy. In the Inspector, click **Add Component** and search for **Emotion Controller**, or navigate to **Convai → Embodiment → Emotion Controller**.

The component appears with a **Profile** field that is currently empty.

<figure><img src="../../../../.gitbook/assets/image (497).png" alt="Unity Inspector showing ConvaiEmotionController added to the NPC root GameObject with the Profile field empty, ready for a profile asset to be assigned"><figcaption><p>ConvaiEmotionController added to the NPC root. The Profile field is empty until an EmotionProfile asset is assigned. No blendshape mapping is active yet.</p></figcaption></figure>
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
### Enter Play Mode and speak

Press **Play**. Talk to the character using your configured microphone. As the AI responds, watch the `ConvaiEmotionController` in the Inspector — the **Current** reading updates live.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Expected result:** The NPC's facial expression changes as the conversation develops. The **Current → Dominant Label** field shows the active emotion and **Current → Dominant Score** shows its smoothed intensity. If you are using a Reallusion character with the default rig, blendshapes activate on the character's face immediately.
{% endhint %}

## How it works

When you spoke to the character, `ConvaiEmotionController` received Convai's emotion signal, resolved it through the taxonomy, smoothed the intensity score over time, and wrote the score to the character's facial blendshapes every frame. For example, the raw label `"Joy"` resolves to the canonical presentation label `joy`; the higher-intensity label `"Ecstasy"` also resolves to `joy`.

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
