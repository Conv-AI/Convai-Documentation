# Quick Start

### Get Your First Emotionally Reactive NPC Working

You will attach the controller, assign the bundled sample profile, and see your character's face respond to live AI emotion signals in Play Mode. No configuration is required upfront — the bundled profile ships pre-configured for Reallusion characters and runs on any rig with no additional setup.

{% hint style="info" %}
**Prerequisites**

* Unity 2022.3 LTS or later
* Convai SDK for Unity installed and up to date
* A scene with a `ConvaiCharacter` component already set up and responding to speech
* Your Convai API key configured in **Tools → Convai → Configuration**
{% endhint %}

### Set Up the Emotion Controller

{% stepper %}
{% step %}
**Add the Emotion Controller**

Select your NPC's root GameObject in the Hierarchy. In the Inspector, click **Add Component** and search for **Emotion Controller**, or navigate to **Convai → Embodiment → Emotion Controller**.

The component appears with a **Profile** field that is currently empty.

{% hint style="success" %}
The `ConvaiEmotionController` component is now visible in the Inspector with all fields at their defaults. The **Profile** field shows "None".
{% endhint %}
{% endstep %}

{% step %}
**Locate the Bundled Sample Profile**

In the Project window, navigate to:

{% code overflow="wrap" %}
```
Packages / Convai SDK for Unity / SamplesShared / Resources / Embodiment / Modules / Emotion
```
{% endcode %}

You will find two assets:

| Asset                                 | Purpose                                                                                                                        |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `ConvaiSamplesShared_EmotionProfile`  | Pre-configured expression slots for Reallusion characters, with smoothing, micro-burst, and neutral alternation already tuned. |
| `ConvaiSamplesShared_EmotionTaxonomy` | The default emotion vocabulary (already referenced by the profile above).                                                      |

{% hint style="info" %}
The bundled profile is configured for **Reallusion** characters out of the box. If your character uses a different rig, the pipeline will still run — but you will need to update the blendshape names in the profile slots to match your character. See [Emotion Profile](/broken/pages/156047f7c23715c9cee58ca6189511fd29081b10) for how to do this.
{% endhint %}

{% hint style="success" %}
Both assets are visible in the Project window. Selecting `ConvaiSamplesShared_EmotionProfile` in the Inspector shows the pre-configured blendshape slots and smoothing values.
{% endhint %}
{% endstep %}

{% step %}
**Assign the Profile**

Drag `ConvaiSamplesShared_EmotionProfile` from the Project window into the **Profile** field on the `ConvaiEmotionController` component.

{% hint style="warning" %}
The bundled asset is **read-only** — it lives inside the package. To adjust any settings, duplicate it first (**Ctrl+D** on Windows / **Cmd+D** on macOS), move the copy into your own `Assets/` folder, and assign the copy instead.
{% endhint %}

{% hint style="success" %}
The **Profile** field now shows `ConvaiSamplesShared_EmotionProfile`. The controller is fully configured and ready to receive emotion signals.
{% endhint %}
{% endstep %}

{% step %}
**Enter Play Mode and Speak**

Press **Play**. Talk to the character using your configured microphone. As the AI responds, watch the `ConvaiEmotionController` in the Inspector — the **Current** reading updates live.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Expected result:** The NPC's facial expression changes as the conversation develops — a subtle smile during warm exchanges, a more serious expression during difficult topics. If you are using a Reallusion character with the default rig, you will see the shapes activate on the character's face immediately. The **Current → Dominant Label** field in the Inspector shows the active emotion, and **Current → Dominant Score** shows its smoothed intensity.
{% endhint %}

### What Just Happened

When you spoke to the character, the following occurred automatically:

1. The Convai backend processed your speech and decided on an emotional state for the character.
2. It sent a short message containing a label such as `"happy"` and an intensity value from 1 to 3.
3. `ConvaiEmotionController` received this, resolved `"happy"` to the canonical label `"joy"` via the taxonomy, and smoothed the intensity score over time.
4. The profile's pre-configured blendshape slots wrote the smoothed score to the character's facial blendshapes every frame.
5. `ConvaiEmotionController.Current` reflected the live state throughout.

All of this runs automatically for the lifetime of the session.

### Using a Non-Reallusion Character

If your character has different blendshape names, duplicate the bundled profile, open the copy, and update the **Blendshape Names** field in each slot to match your character's shapes. The slot structure, smoothing values, and all other settings remain valid — only the shape names need to change.

{% hint style="info" %}
Mapping blendshapes for a new character can be done quickly with the help of an AI coding assistant. Share your character's blendshape list and ask it to generate the slot configuration — the slot format is straightforward and maps directly to the Inspector fields.
{% endhint %}

For a complete walkthrough of how slots work and how to configure them for any rig, see [Emotion Profile](/broken/pages/156047f7c23715c9cee58ca6189511fd29081b10) and [Output Bindings](/broken/pages/1e2b2eb9321a550a8ea8a49276a5aaad36013bb2).

### Next Steps

{% content-ref url="/broken/pages/156047f7c23715c9cee58ca6189511fd29081b10" %}
[Broken link](/broken/pages/156047f7c23715c9cee58ca6189511fd29081b10)
{% endcontent-ref %}

{% content-ref url="/broken/pages/1e2b2eb9321a550a8ea8a49276a5aaad36013bb2" %}
[Broken link](/broken/pages/1e2b2eb9321a550a8ea8a49276a5aaad36013bb2)
{% endcontent-ref %}

{% content-ref url="/broken/pages/d16937e3d6537821e2c4af08d397101d0111d1ee" %}
[Broken link](/broken/pages/d16937e3d6537821e2c4af08d397101d0111d1ee)
{% endcontent-ref %}

{% content-ref url="/broken/pages/f0c2d9761c4ab0f268935974d43719702616404e" %}
[Broken link](/broken/pages/f0c2d9761c4ab0f268935974d43719702616404e)
{% endcontent-ref %}

{% content-ref url="/broken/pages/4b098f84798d0ee0505ec21ec2c0b631206339d3" %}
[Broken link](/broken/pages/4b098f84798d0ee0505ec21ec2c0b631206339d3)
{% endcontent-ref %}

### Conclusion

You now have a complete emotion pipeline running on your character — server-driven, smoothed, and reacting to live AI decisions. If your character is Reallusion-based, expressions are already active. If not, update the blendshape names in the profile and the rest of the configuration carries over unchanged.
