---
description: >-
  Learn how to add and configure the Convai Lip Sync component on your
  character, assign profiles and maps, configure playback and latency settings,
  and verify real-time facial animation in Unity.
---

# Adding Lip Sync to Your Character

## Introduction

The **Convai Lip Sync** component connects real-time speech animation to your character's face. While your character is speaking, it receives incoming Lip Sync data, processes it through the active Lip Sync map, and drives the blendshapes on your character's meshes automatically.

This page explains how to add the component, what each Inspector section does, and how to configure it correctly for a working Lip Sync setup in Unity.

***

## Before You Start

Before adding the component, make sure your setup includes:

* A character in the scene with at least one **`SkinnedMeshRenderer`** that contains facial blendshapes
* A **Convai Character** component on the same GameObject

***

## Add the Component

Select your character's root GameObject in the Hierarchy, then in the Inspector choose:

```
Add Component > Convai > Lip Sync > Convai Lip Sync
```

Once added, the component appears with four main sections in the Inspector:

* **Core Setup**
* **Playback & Behavior**
* **Streaming & Latency**
* **Live Status**

## Core Setup

This is the main setup section. It defines which Lip Sync profile the character uses, which map is applied, and which meshes will be animated.

<figure><img src="../../../../../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

### Profile

The **Profile** dropdown selects the Lip Sync profile used by the character.

This tells the system which channel schema to expect for the current setup.

Available options are:

| Option           | Use when your character is...                                                |
| ---------------- | ---------------------------------------------------------------------------- |
| **ARKit**        | A standard Unity character or any rig with ARKit-compatible blendshape names |
| **MetaHuman**    | An Unreal Engine MetaHuman brought into Unity                                |
| **CC4 Extended** | A character built with Reallusion Character Creator 4                        |

This setting must match the format your character is designed to work with. If the wrong profile is selected, incoming channels will not line up correctly and the face will animate incorrectly.

For more detail on profile behavior and supported formats, see [**Lip Sync Profiles and Mappings**](lip-sync-profiles-and-mappings/).

### Mapping

The **Mapping** field assigns the `ConvaiLipSyncMapAsset` used by the component.

A map connects incoming Lip Sync channels to the actual blendshape names on your character meshes.

Buttons next to the field:

| Button         | What it does                                                                          |
| -------------- | ------------------------------------------------------------------------------------- |
| **Create New** | Creates a new empty `ConvaiLipSyncMapAsset` and assigns it immediately                |
| **Edit**       | Opens the assigned map asset in the Inspector                                         |
| **Validator**  | Checks the active map against the assigned meshes and reports mapping coverage issues |

If this field is left empty, the component uses the built-in default map for the selected profile. For many standard ARKit, MetaHuman, or CC4 Extended setups, this is enough to get started.

If your character uses custom blendshape names, create and assign a custom map instead. For that workflow, see [**Creating a Custom Map**](lip-sync-profiles-and-mappings/creating-a-custom-map.md).

## Target Meshes

The **Target Meshes** list defines which `SkinnedMeshRenderer` components will receive blendshape animation.

<figure><img src="../../../../../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>

You can populate this list in three ways:

* Click **+** to add a slot manually
* Drag a `SkinnedMeshRenderer` into an existing slot
* Click **Auto-Find** to search the current GameObject and all children automatically

After the list is populated, the component shows a summary such as:

```
✓ 10 Meshes Found (294 Blendshapes)
```

This indicates how many meshes were found and how many total blendshape slots are available across them.

If this count is `0`, there is nothing for the Lip Sync system to animate.

For most characters, **Auto-Find** is the fastest way to build this list. After that, remove any meshes that should not be driven, such as clothing or accessories with no facial blendshapes.

## Playback & Behavior

This section controls how the facial animation feels during playback.

<figure><img src="../../../../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

### Lip Smoothing

**Lip Smoothing** controls how strongly incoming values are smoothed from frame to frame.

Range: `0` to `0.9`\
Default: `0.5`

Behavior:

* **0**: no smoothing, more direct but potentially jittery
* **0.9**: very smooth, but slower to react
* **0.5**: balanced default for most characters

A higher value makes facial motion feel softer and more stable. A lower value makes the face react more quickly to incoming changes.

### Fade Transition

**Fade Transition** controls how long it takes for the face to return to neutral after speech ends.

Range: `0.05` to `2` seconds\
Default: `0.2`

Behavior:

* **0.05**: nearly instant return to neutral
* **0.2**: natural default for most humanoid characters
* **2.0**: very slow fade

This helps avoid abrupt snapping when speech finishes.

### A/V Sync Offset

**A/V Sync Offset** shifts Lip Sync playback earlier or later relative to the audio.

Range: `-0.5` to `+0.5` seconds\
Default: `0`

Behavior:

* **Negative values**: lips move slightly before audio
* **Positive values**: lips move slightly after audio
* **0**: no timing offset

In most setups, this should remain at `0` unless you consistently notice visual desync during playback.

## Streaming & Latency

This section controls how incoming Lip Sync data is buffered and played back.

For most users, the default setting is the right choice.

<figure><img src="../../../../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

### Latency Mode

**Latency Mode** applies a preset buffering strategy.

Available modes:

| Mode                  | Best for                              | Trade-off                                    |
| --------------------- | ------------------------------------- | -------------------------------------------- |
| **Ultra Low Latency** | Very stable low-latency environments  | Lower delay, higher risk of stutter          |
| **Balanced**          | Most production use cases             | Best balance of stability and responsiveness |
| **Network Safe**      | Mobile or unstable network conditions | Higher delay, more stable playback           |
| **Custom**            | Advanced manual tuning                | Requires direct control of buffer settings   |

Internal values used by each preset:

| Mode              | Max Buffer | Min Headroom |
| ----------------- | ---------- | ------------ |
| Ultra Low Latency | 1.0 s      | 0.05 s       |
| Balanced          | 3.0 s      | 0.12 s       |
| Network Safe      | 6.0 s      | 0.25 s       |
| Custom            | unchanged  | unchanged    |

### Max Buffered Seconds

This defines how much animation data can accumulate before playback begins.

A larger value improves stability on inconsistent connections, but increases visible delay.

This field is editable only in **Custom** mode.

### Min Resume Headroom

If playback runs out of buffered frames and pauses, this determines how much data must build up before playback resumes.

A higher value makes resume behavior more conservative and stable.

This field is editable only in **Custom** mode.

For most projects, leave **Latency Mode** on **Balanced**.

## Live Status

The **Live Status** section is read-only and updates during Play mode.

It gives you a live view of what the Lip Sync component is doing internally, which makes it very useful for debugging.

<figure><img src="../../../../../.gitbook/assets/image (13) (1).png" alt=""><figcaption></figcaption></figure>

### Status Indicator

A colored status label in the Inspector shows the current playback state.

| State          | Color  | Meaning                                                       |
| -------------- | ------ | ------------------------------------------------------------- |
| **Idle**       | Green  | No speech data is being received                              |
| **Buffering**  | Yellow | Data is arriving and buffering before playback                |
| **Playing**    | Green  | Lip Sync is actively being applied to the meshes              |
| **Starving**   | Red    | Playback has run out of buffered data and is waiting for more |
| **Fading Out** | Orange | Speech ended and the face is returning to neutral             |

The profile badge also confirms which profile is active at runtime.

### Timing Counters

The component also shows runtime counters such as:

| Counter           | Meaning                                               |
| ----------------- | ----------------------------------------------------- |
| **Elapsed Time**  | Time since the current speech event started           |
| **Remaining**     | Seconds of buffered animation left                    |
| **Received Data** | Total Lip Sync data received for the current event    |
| **Headroom**      | Safety gap between playback and the end of the buffer |
| **Buffer Size**   | Total current buffer size in seconds                  |
| **Is Talking**    | Whether the character is currently speaking           |

If **Headroom** frequently drops near zero during testing, consider switching to **Network Safe** or reviewing network quality.

## Step-by-Step Setup

Follow this flow to set up Lip Sync on a character from scratch.

{% stepper %}
{% step %}
### Add the Convai Lip Sync component

Select your character's root GameObject, then add:

```
Convai > Lip Sync > Convai Lip Sync
```

<figure><img src="../../../../../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Select the correct profile

In **Core Setup > Profile**, choose the profile that matches your character:

* **ARKit**
* **MetaHuman**
* **CC4 Extended**

If you are unsure why this matters, review [**Lip Sync Profiles and Mappings**](lip-sync-profiles-and-mappings/).

<figure><img src="../../../../../.gitbook/assets/image (8) (1).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Assign target meshes

Under **Target Meshes**, click **Auto-Find**.

Make sure the component reports a non-zero number of meshes and blendshapes. If some meshes should not receive Lip Sync animation, remove them manually.

<figure><img src="../../../../../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Check or assign a map

If your character already uses standard blendshape names for the selected profile, you can leave **Mapping** empty and use the built-in default map or you can choose a map from **provided maps.**

If your character uses different blendshape names, create a custom map and assign it here.

For that process, see [**Creating a Custom Map**](lip-sync-profiles-and-mappings/creating-a-custom-map.md).

<figure><img src="../../../../../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Run the Validator

Click **Validator** next to the Mapping field.

This checks how well the active map matches the assigned meshes and helps identify unmapped or mismatched channels.

A high coverage result, especially on mouth-related channels, is a strong indicator that the setup is correct.

<figure><img src="../../../../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../../../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Choose a latency mode

Under **Streaming & Latency**, keep **Latency Mode** on **Balanced** unless you already know you need a lower-latency or more network-safe configuration.
{% endstep %}

{% step %}
### Enter Play Mode and test

Start Play Mode and trigger a speech event from your Convai character.

Watch the **Live Status** section. In a working setup, the status typically moves through:

```
Idle -> Buffering -> Playing
```

At the same time, your character's face should animate in sync with the voice.

If the status never leaves **Idle**, check that the **Convai Character** component is on the same GameObject and fully configured.
{% endstep %}
{% endstepper %}

## Common Issues

| Symptom                               | Likely cause                                        | Fix                                                                                      |
| ------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Status stays Idle                     | Convai Character component missing or not connected | Make sure the Convai Character component exists on the same GameObject                   |
| Headroom is frequently red            | Network jitter or insufficient buffering            | Switch Latency Mode to Network Safe                                                      |
| Wrong facial shapes move              | Incorrect profile selected                          | Select the profile that matches the character rig                                        |
| Some blendshapes do not animate       | Incomplete map coverage                             | Run Validator, fix unmapped entries, or use a custom map                                 |
| Animation feels too strong            | Map multiplier is too high                          | Lower the map multiplier or reduce specific entry values                                 |
| Animation feels too weak              | Map multiplier is too low                           | Increase the map multiplier                                                              |
| Lips move before the audio            | Offset needs earlier correction                     | Use a small positive or negative adjustment and retest carefully                         |
| Lips move after the audio             | Offset needs later correction                       | Use a small positive or negative adjustment and retest carefully                         |
| Component disables itself during Play | Validation or setup failure                         | Check the Console for errors related to profile, character setup, or required references |

## Related Pages

For more detailed setup and customization, continue with:

* [**Lip Sync Profiles and Mappings**](lip-sync-profiles-and-mappings/)
* [**Creating a Profile**](lip-sync-profiles-and-mappings/creating-a-profile.md)
* [**Creating a Custom Map**](lip-sync-profiles-and-mappings/creating-a-custom-map.md)

## Conclusion

The Convai Lip Sync component is the runtime layer that brings profiles, maps, and character meshes together into a working facial animation setup.

Once the correct profile is selected, the target meshes are assigned, and the map is valid, Lip Sync playback becomes mostly automatic. From there, playback smoothing, fade timing, and latency settings help you refine how the final result feels in your project.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
