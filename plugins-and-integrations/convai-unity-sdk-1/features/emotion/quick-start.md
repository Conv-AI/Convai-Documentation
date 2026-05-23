---
title: Emotion quick start
description: Build a working emotion pipeline on a Convai NPC — attach the Emotion Controller, assign the bundled sample profile, and verify expressions in Play Mode.
---

We will attach the Emotion Controller to an NPC, assign the bundled sample profile, and see the character's face react to live AI emotion signals in Play Mode. No custom assets are required for the initial setup.

## Prerequisites

- <code class="expression">space.vars.unity_min_version</code>
- Convai SDK for Unity installed and up to date
- A scene with a `ConvaiCharacter` component already set up and responding to speech
- Convai API key configured in **Tools → Convai → Configuration**

## Set up the Emotion Controller

{% stepper %}
{% step %}
### Add the Emotion Controller

Select your NPC's root GameObject in the Hierarchy. In the Inspector, click **Add Component** and search for **Emotion Controller**, or navigate to **Convai → Embodiment → Emotion Controller**.

The component appears with a **Profile** field that is currently empty.
{% endstep %}

{% step %}
### Locate the bundled sample profile

In the Project window, navigate to:

{% code overflow="wrap" %}
```
Packages / Convai SDK for Unity / SamplesShared / Resources / Embodiment / Modules / Emotion
```
{% endcode %}

You will find two assets:

| Asset | Purpose |
| --- | --- |
| `ConvaiSamplesShared_EmotionProfile` | Pre-configured expression slots for Reallusion characters, with smoothing, micro-burst, and neutral alternation already tuned. |
| `ConvaiSamplesShared_EmotionTaxonomy` | The default emotion vocabulary, already referenced by the profile above. |
{% endstep %}

{% step %}
### Assign the profile

Drag `ConvaiSamplesShared_EmotionProfile` from the Project window into the **Profile** field on the `ConvaiEmotionController` component.

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

<figure><img src="../../../../.gitbook/assets/TODO-emotion-controller-profile-field.png" alt="Unity Inspector showing the ConvaiEmotionController component with the Profile field empty"><figcaption><p>TODO: Replace with screenshot showing the ConvaiEmotionController Inspector — Profile field empty before assignment, then populated after step 3.</p></figcaption></figure>

<figure><img src="../../../../.gitbook/assets/TODO-emotion-sample-assets-project-window.png" alt="Unity Project window showing the bundled emotion sample assets inside the Convai SDK package"><figcaption><p>TODO: Replace with screenshot showing the bundled profile and taxonomy assets in the Project window.</p></figcaption></figure>

## How it works

When you spoke to the character, `ConvaiEmotionController` received the backend's emotion signal, resolved it through the taxonomy (mapping `"happy"` to `"joy"`), smoothed the intensity score over time, and wrote the score to the character's facial blendshapes every frame. For a full explanation of every stage, see [How the emotion system works](how-the-emotion-system-works.md).

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
