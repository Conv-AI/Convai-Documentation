# quick start

The Dialogue Animation module requires three things: an Animator Controller with the correct four-layer structure, a clip library, and a runtime config. The SDK ships all of these as bundled assets — you can be up and running without authoring a single animation.

{% hint style="info" %}
**Prerequisites**

* A scene with `ConvaiRoomManager` and at least one `ConvaiCharacter`
* The character's root GameObject has an `Animator` component pointing to a controller (you will replace this below)
* The Unity Animation Rigging package is **not** required — it is optional for the advanced gaze bridge
{% endhint %}

***

## Setup Steps

{% stepper %}
{% step %}
**Duplicate the Sample Animator Controller**

The SDK includes a sample controller with the required four-layer structure. Duplicate it into your project so you can customize it without modifying the package.

1. In the Project window, navigate to:\
   `Packages/Convai SDK for Unity/SamplesShared/Art/Animations/Dialogue/Controllers/`
2. Right-click **ConvaiSample\_Animator Controller** → **Create** → **Copy Asset** (or Ctrl+D to duplicate in place, then drag to your Assets folder)
3. Assign the duplicated controller to your character's `Animator` component

The controller has four layers:

| Index | Layer Name   | Purpose                                          |
| ----- | ------------ | ------------------------------------------------ |
| 0     | Base Idle    | Full-body foundation idle, always playing        |
| 1     | Idle Overlay | Rotating ambient gesture clips                   |
| 2     | Body Talk    | Upper-body talk clips, fades in during speech    |
| 3     | Head Talk    | Head and neck talk clips, fades in during speech |
{% endstep %}

{% step %}
**Add ConvaiDialogueAnimationController**

Add the `ConvaiDialogueAnimationController` component to the character's root GameObject.

The component appears with three main Inspector sections: **Content** (library and config assets), **Animator Wiring** (target Animator and contract), and **Character Gender**.

Leave **Animator** blank — the component auto-discovers the first `Animator` in the hierarchy. Set it explicitly if your hierarchy has multiple animators.
{% endstep %}

{% step %}
**Assign a Library**

Drag one of the bundled libraries from\
`Packages/Convai SDK for Unity/SamplesShared/Resources/Embodiment/DialogueAnimation/Libraries/`\
into the **Library** field:

| Asset                                                    | Best For                                     |
| -------------------------------------------------------- | -------------------------------------------- |
| `ConvaiSamplesShared_DialogAnimationLib_Balanced.asset`  | General use — a mix of gesture scales        |
| `ConvaiSamplesShared_DialogAnimationLib_Expresive.asset` | Characters with wide, animated personalities |
| `ConvaiSamplesShared_DialogAnimationLib_Subtle.asset`    | Characters in formal or restrained contexts  |

The library contains both idle clips (played during silence) and talk clips (played during speech and reactions).
{% endstep %}

{% step %}
**Assign a Runtime Config**

Drag `ConvaiSamplesShared_DialogueAnimationRuntimeConfig.asset` (same folder as the libraries, one level up at `…/DialogueAnimation/`) into the **Config** field.

The runtime config controls fade durations, idle rotation cadence, speech energy modulation, and clip selection bias. You can share one config across multiple characters.

{% hint style="warning" %}
If **Config** is left empty, `ConvaiDialogueAnimationController` logs a warning and skips building the runtime. The component will not animate until a config is assigned.
{% endhint %}
{% endstep %}

{% step %}
**Set Character Gender**

Set the **Character Gender** field to match your rig's animation authorship:

* **Neutral** — accepts all clips regardless of their gender tag. Use this when you are unsure or when your library mixes clip styles freely.
* **Male** — only selects clips tagged `Male` or `Neutral`
* **Female** — only selects clips tagged `Female` or `Neutral`

Mismatched gender settings result in visually incorrect clips (masculine gestures on a feminine rig, or vice versa). See [Animation Libraries & Profiles](/broken/pages/cc256e6610756212db3fdf852998767014ffb0ff) for how gender tags are set on individual clips.
{% endstep %}

{% step %}
**Enter Play Mode**

Press Play. Talk to the character.

* During silence, the idle overlay layer crossfades to a new ambient gesture every 8–20 seconds
* When the character speaks or reacts, the body and head talk layers fade in
* Open the Animator window and watch layer weights change in real time
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You should see the idle overlay layer weight change as ambient clips crossfade, and the talk layers fade in when the character speaks. If the character's emotion module is also active, clip selection will bias toward animation clips that match the current emotion.
{% endhint %}

***

## Using a Profile Instead

If you configure multiple characters, a `ConvaiDialogueAnimationProfile` bundles all assets (library, config, contract, foundation idle clip, and gender) into a single ScriptableObject. Three bundled profiles are available:

| Asset                                                           | Contents                           |
| --------------------------------------------------------------- | ---------------------------------- |
| `ConvaiSamplesShared_DialogueAnimationProfile_Balanced.asset`   | Balanced library + shared config   |
| `ConvaiSamplesShared_DialogueAnimationProfile_Expressive.asset` | Expressive library + shared config |
| `ConvaiSamplesShared_DialogueAnimationProfile_Subtle.asset`     | Subtle library + shared config     |

Assign a profile in the **Profile** slot at the top of the component Inspector. Individual field overrides in the Content section take priority over the profile when both are set.

***

## Next Steps

{% content-ref url="/broken/pages/cc256e6610756212db3fdf852998767014ffb0ff" %}
[Broken link](/broken/pages/cc256e6610756212db3fdf852998767014ffb0ff)
{% endcontent-ref %}

{% content-ref url="/broken/pages/da72fb4f3f9be0c09f3781e47f8daffe0675c679" %}
[Broken link](/broken/pages/da72fb4f3f9be0c09f3781e47f8daffe0675c679)
{% endcontent-ref %}
