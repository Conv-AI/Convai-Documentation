---
title: Dialogue Animation quick start
description: Add ConvaiDialogueAnimationController to a character, assign a library and runtime config, and verify gesture animation in Play Mode.
last_reviewed: "4.2.0"
---

Add gesture animation to an AI character using the bundled sample assets. The Dialogue Animation module needs three things: a four-layer Animator Controller with named placeholder clips, a `DialogueAnimationLibrary` with idle and talk clips, and a `DialogueAnimationRuntimeConfig` that controls timing. This guide walks through the quickest path using the bundled sample assets.

## Prerequisites

* `ConvaiRoomManager` and at least one `ConvaiCharacter` are already in your scene
* The character GameObject has an `Animator` component with a humanoid Avatar configured
* You know the path to the SDK's sample assets: `Packages/`<code class="expression">space.vars.sdk_package_id</code>`/SamplesShared/`

***

## Setup

{% stepper %}
{% step %}
### Duplicate the sample Animator Controller

In the Project window, navigate to:

```
Packages/com.convai.convai-sdk-for-unity/SamplesShared/Art/Animations/Dialogue/Controllers/
```

Duplicate `ConvaiSample_Animator Controller` and move it into your project's `Assets/` folder. Assign it to the `Animator` component on your character's root GameObject.

The sample controller already has the required four-layer structure and placeholder clips. See [Animator Controller requirements](animator-controller-requirements.md) for the full layer and clip contract, or [Build a compatible Animator Controller](animator-controller-setup.md) if you need to build your own.
{% endstep %}

{% step %}
### Add ConvaiDialogueAnimationController

Select your character's root GameObject. In the Inspector, click **Add Component** and search for **Dialogue Animation** (or navigate via **Convai → Embodiment → Dialogue Animation**).

The component appears with empty `Library` and `Config` fields and a default `Character Gender` of **Neutral**.
{% endstep %}

{% step %}
### Assign a library

In the Project window, navigate to:

```
Packages/com.convai.convai-sdk-for-unity/SamplesShared/Resources/Embodiment/DialogueAnimation/Libraries/
```

Three bundled libraries are available:

| Library                                            | Character style                                               |
| -------------------------------------------------- | ------------------------------------------------------------- |
| `ConvaiSamplesShared_DialogAnimationLib_Balanced`  | Professional, measured gestures — suitable for most scenarios |
| `ConvaiSamplesShared_DialogAnimationLib_Subtle`    | Restrained, low-energy movement                               |
| `ConvaiSamplesShared_DialogAnimationLib_Expresive` | High-energy, expressive gestures                              |

Drag your chosen library into the **Library** field on the component.
{% endstep %}

{% step %}
### Assign a runtime config

Navigate to:

```
Packages/com.convai.convai-sdk-for-unity/SamplesShared/Resources/Embodiment/DialogueAnimation/
```

Drag one of the bundled `ConvaiDialogueAnimationProfile_*` assets into the **Config** field — or assign a `DialogueAnimationRuntimeConfig` asset directly.

{% hint style="danger" %}
Leaving **Config** empty disables all animation. The component will not animate until a config is assigned.
{% endhint %}
{% endstep %}

{% step %}
### Set character gender

Set **Character Gender** to match your character rig:

* **Neutral** — clips with no gender tag are eligible (default; safe for most rigs)
* **Male** — adds Male-tagged clips to the eligible pool
* **Female** — adds Female-tagged clips to the eligible pool

A Neutral character only receives Neutral-tagged clips. Male and Female characters receive both gender-specific and Neutral clips.
{% endstep %}

{% step %}
### Enter Play Mode

Press Play. Your character should begin playing idle animation immediately. When a conversation starts and the character speaks, the talk layers fade in with gesture animation matching the detected emotion.

**Expected result:** Idle clips cycle with natural crossfades at rest. When the character speaks, the body talk and head talk layers fade in. The `CurrentTalkLayerWeight` property on the controller rises above `0` during speech.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Inspector screenshot required before publishing: capture `ConvaiDialogueAnimationController` on the character root with the Library, Config, and Character Gender fields assigned as described in steps 3–5.
{% endhint %}

<figure><img src="../../../.gitbook/assets/TODO-dialogue-animation-controller-inspector.png" alt="Unity Inspector showing ConvaiDialogueAnimationController with Library, Config, and Character Gender fields assigned"><figcaption><p>TODO: Replace with screenshot showing ConvaiDialogueAnimationController with all required fields assigned.</p></figcaption></figure>

***

## Alternative: use a bundled profile

Rather than assigning Library and Config separately, you can assign a `ConvaiDialogueAnimationProfile` to the **Profile** slot. A profile bundles Library, RuntimeConfig, AnimatorContract, CharacterGender, and FoundationIdleClip into a single asset.

Three bundled profiles are available at:

```
Packages/com.convai.convai-sdk-for-unity/SamplesShared/Resources/Embodiment/DialogueAnimation/
```

Assign `ConvaiDialogueAnimationProfile_Balanced`, `_Expressive`, or `_Subtle` to the profile slot. Individual Library and Config fields on the component take precedence over a profile if both are assigned.

***

## Next steps

Your character now plays gesture animation driven by dialogue state and emotion. Read Animation Libraries & Profiles to learn how to author custom clip libraries, or Animator Controller requirements for the full four-layer contract reference.

{% content-ref url="animation-libraries-and-profiles.md" %}
[Animation libraries and profiles](animation-libraries-and-profiles.md)
{% endcontent-ref %}

{% content-ref url="animator-controller-requirements.md" %}
[Animator Controller requirements](animator-controller-requirements.md)
{% endcontent-ref %}
