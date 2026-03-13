---
description: >-
  Learn how Convai Lip Sync uses profiles and maps to drive real-time facial
  blendshape animation, how built-in defaults work, and when to create custom
  assets.
---

# Lip Sync Profiles and Mappings

## Introduction

Convai Lip Sync drives facial blendshape animation in real time by matching incoming speech animation channels to the blendshapes on your character. To make that work reliably, the system needs two things:

* A **Profile**, which defines the channel schema the character uses
* A **Map**, which tells the SDK how those channels connect to actual blendshape names on the mesh

Together, these two assets make the Lip Sync pipeline predictable, editable, and easy to adapt in the Unity Editor.

## Overview

At a high level, the Lip Sync system answers two questions:

1. **Which facial rig schema is active?**\
   This is defined by the **Profile**.
2. **How should each incoming channel affect this specific character mesh?**\
   This is defined by the **Map**.

Both are stored as Unity `ScriptableObject` assets, so they can be inspected, assigned, and customized directly in the Editor.

## What Is a Profile?

A **Lip Sync Profile** defines the expected channel layout for a facial rig. It acts as the schema for incoming facial animation data.

For example, if a profile expects a channel called `jawOpen`, the system interprets that channel according to the rules of that profile. This allows the SDK to know what data is being sent and how to categorize it before any mesh-specific mapping happens.

A profile is not tied to a single character. It defines a reusable facial rig format that multiple characters can share.

## What Is a Map?

A **Lip Sync Map** connects profile channels to the actual blendshape names on a character's `SkinnedMeshRenderer`.

This is what makes Lip Sync work on real character assets. Even if the incoming channel schema is valid, the animation cannot be applied correctly unless the system knows which mesh blendshape each channel should drive.

A map can do more than simple one-to-one routing. It can also:

* Route one source channel to multiple target blendshapes
* Scale or offset individual channels
* Clamp overly strong values
* Disable channels that should not be driven
* Optionally allow unmapped names to pass through directly

### How Profiles and Maps Work Together

The flow is simple:

1. A Lip Sync profile determines which channel schema is active
2. A Lip Sync map reads channels from that schema
3. The map writes the processed values to the target blendshapes on the character mesh

This separation is important because it allows one profile to be reused across many different characters, while each character can still have its own map.

For example, two characters may both use the `arkit` profile, but one may use the default map while another uses a custom map because its blendshape names differ.

## Supported Profile Formats

Currently, Convai supports the following Lip Sync profile formats:

| Profile      | ID             |
| ------------ | -------------- |
| ARKit        | `arkit`        |
| MetaHuman    | `mha`          |
| CC4 Extended | `cc4_extended` |

These are the only supported transport formats at this time.

This means:

* You can create custom profile assets inside your project
* You can rename or organize profiles for your workflow
* You can override which supported transport format a profile uses
* You **cannot** introduce a brand-new transport format by entering a custom value

In other words, creating a custom profile does not add support for a new backend format. The transport format must still resolve to one of the supported values: `arkit`, `mha`, or `cc4_extended`.

### Built-in Profiles

The SDK includes built-in profiles for the supported formats. These represent the standard schemas used by the Lip Sync system and are intended to be the authoritative built-in definitions.

Each profile asset includes:

| Field                | Purpose                                            |
| -------------------- | -------------------------------------------------- |
| **Profile ID**       | Internal runtime identifier                        |
| **Display Name**     | Human-readable label shown in the Editor           |
| **Transport Format** | Supported format token used by the active pipeline |

Built-in profile assets are located under:

```
Resources/LipSync/Profiles/
```

### Profile Registries

Profiles are grouped into a **Profile Registry** rather than loaded one by one.

The built-in registry is located at:

```
Resources/LipSync/ProfileRegistries/LipSyncBuiltInProfileRegistry
```

At runtime, the SDK loads the built-in registry, scans for additional registries under the same `Resources` path, and merges them into a single catalog.

Registries are merged by priority:

* Lower priority values are processed first
* Higher priority values can override existing profile IDs
* Duplicate profile IDs produce a warning and the higher-priority definition wins

This lets you extend or override profile definitions without editing built-in SDK assets directly.

## Built-in Default Maps

The SDK also includes built-in default maps for supported profile types.

These are located under:

```
Resources/LipSync/DefaultMaps/
```

The built-in set includes:

<table><thead><tr><th width="291.9630126953125">Asset</th><th>Target Profile</th><th>Purpose</th></tr></thead><tbody><tr><td><code>ConvaiLipSyncDefaultMap_ARKit</code></td><td><code>arkit</code></td><td>Identity-style default mapping for ARKit channels</td></tr><tr><td><code>ConvaiLipSyncDefaultMap_MetaHuman</code></td><td><code>mha</code></td><td>Identity-style default mapping for MetaHuman channels</td></tr><tr><td><code>ConvaiLipSyncDefaultMap_CC4Extended</code></td><td><code>cc4_extended</code></td><td>Identity-style default mapping for CC4 Extended channels</td></tr><tr><td><code>ConvaiLipSyncDefaultMap_ARKitToCC4Extended</code></td><td><code>arkit</code></td><td>Cross-rig translation from ARKit channels to CC4 Extended blendshape names</td></tr></tbody></table>

These default maps are designed to cover common use cases out of the box.

#### Why some built-in channels are clamped or disabled

Some built-in mappings intentionally reduce or suppress certain channels to keep results stable and natural on common character setups.

Examples include:

* **Jaw open clamping** to reduce exaggerated mouth motion
* **Eye rotation channel disabling** for rigs that do not use blendshape-driven eye motion
* **Cosmetic channel disabling** on rigs where those channels are not appropriate for speech animation

### Default Map Registry

The **Default Map Registry** defines which default map is used automatically for each profile.

It is located at:

```
Resources/LipSync/DefaultMaps/LipSyncDefaultMapRegistry
```

This registry maps each supported profile ID to its default `ConvaiLipSyncMapAsset`.

### How Map Resolution Works

When a Lip Sync component initializes, the SDK determines which map to use through a fallback chain:

1. **Explicit map on the component**\
   If a map asset is assigned directly and its target profile matches the active profile, that map is used.
2. **Default map registry lookup**\
   If no valid explicit map is assigned, the system checks the Default Map Registry for the active profile.
3. **Safe disabled fallback**\
   If no valid map is found, the SDK creates a safe fallback that outputs zero values instead of animating the character.

This behavior ensures that missing or mismatched setups fail safely without crashing the scene.

## When to Create Custom Assets

You typically do **not** need custom assets if your character already matches one of the built-in supported formats and its blendshape names follow the expected naming convention.

You should create a **custom map** when:

* Your character uses different blendshape names
* You need custom clamping or scaling
* You want one source channel to drive multiple targets
* You want more control over which channels are enabled

You may create a **custom profile** when:

* You want a project-specific profile identity or label
* You want to organize supported formats differently inside your project
* You need a custom profile asset that still resolves to one of the currently supported transport formats

For step-by-step instructions, continue with:

* [**Creating a Profile**](creating-a-profile.md)
* [**Creating a Custom Map**](creating-a-custom-map.md)

## Conclusion

Profiles define the channel schema. Maps define how that schema drives a specific mesh.

Once you understand that separation, the Lip Sync workflow becomes straightforward: choose the supported profile format that matches your character setup, then use either a built-in map or a custom one to connect those channels to your character's blendshapes.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
