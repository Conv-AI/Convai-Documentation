---
description: >-
  Create and register a custom Lip Sync profile in Unity, understand profile
  fields, and configure supported transport formats for your project.
---

# Creating a Profile

## Introduction

A **Lip Sync Profile** defines the channel schema a character setup uses within the Lip Sync system. In most cases, the built-in profiles are enough. However, you may want to create a custom profile asset to better organize your project, use a project-specific identifier, or override how a supported transport format is represented in your Editor workflow.

This page explains the Profile Inspector, the Profile Registry, and how to create a custom profile correctly.

***

## Before You Start

Currently, Convai supports only these transport formats:

| Transport Format | Supported Schema |
| ---------------- | ---------------- |
| `arkit`          | ARKit            |
| `mha`            | MetaHuman        |
| `cc4_extended`   | CC4 Extended     |

This is important because creating a new profile asset does **not** create a new transport format.

A custom profile can help you:

* Rename or reorganize a supported schema
* Use a custom profile ID for your project
* Point that custom profile to one of the supported formats

A custom profile cannot be used to introduce an entirely new transport value outside `arkit`, `mha`, or `cc4_extended`.

***

## Understanding the Profile Inspector

When you select a `ConvaiLipSyncProfileAsset`, the Inspector is divided into three main areas.

<figure><img src="../../../../../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

### Runtime Identity

This section controls how the profile is identified internally.

**Profile ID**\
A unique normalized string used at runtime to identify the profile.

This ID is used for:

* profile catalog lookup
* map targeting
* registry merging
* component configuration

Choose this carefully. Once other assets reference this ID, changing it can break those references.

### Editor Label

**Display Name**\
This is the human-readable label shown in dropdowns and editor tools.

It has no direct effect on runtime behavior, but it is important for usability. Use a clear name that your team will recognize immediately.

### Transport Format

This section determines which supported transport format the profile resolves to.

**Override default token**\
When disabled, the profile uses its own `Profile ID` as the transport token.

When enabled, the profile can use a different supported transport token. This is useful when you want a custom internal profile ID, but still need the profile to resolve to one of the built-in supported formats.

**Transport Token**\
The transport token must be one of the currently supported values:

* `arkit`
* `mha`
* `cc4_extended`

For example, a profile with ID `my_metahuman_variant` can still use the `mha` transport token.

***

## Create a Custom Profile

{% stepper %}
{% step %}
### Create the profile asset

In the Unity Project window, create a new profile asset:

```
Create > Convai > LipSync > Profile Asset
```

Give it a descriptive name, such as:

```
ConvaiLipSyncProfile_MyCharacter
```
{% endstep %}

{% step %}
### Set the Profile ID

In the **Runtime Identity** section, enter a unique ID.

Example:

```
my_character
```

Use lowercase letters, numbers, and underscores. Avoid spaces.
{% endstep %}

{% step %}
### Set the Display Name

In the **Editor Label** section, enter the display name that should appear in the Inspector.

Example:

```
My Character
```
{% endstep %}

{% step %}
### Set the transport format

Choose which supported Lip Sync schema this profile should use.

Examples:

* Use `arkit` for ARKit-compatible blendshape layouts
* Use `mha` for MetaHuman rigs
* Use `cc4_extended` for CC4 Extended rigs

If your custom profile ID does not match one of those supported tokens, enable **Override default token** and enter the correct supported transport token manually.
{% endstep %}
{% endstepper %}

***

## Understanding Profile Registries

Profiles are discovered through **Profile Registry** assets.

A registry is a `ConvaiLipSyncProfileRegistryAsset` that contains one or more profile references and a priority value used during runtime merging.

<figure><img src="../../../../../../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

#### Registry fields

| Field        | Description                                     |
| ------------ | ----------------------------------------------- |
| **Priority** | Determines load and override order              |
| **Profiles** | List of profile assets included in the registry |

The built-in registry uses priority `0`. Your own custom registry should use a higher value, such as `1`, so it is merged after the built-in set.

### Register the Profile

{% stepper %}
{% step %}
### Create a Profile Registry

Create a registry asset in the Project window:

```
Create > Convai > LipSync > Profile Registry Asset
```

Give it a name such as:

```
MyProjectProfileRegistry
```
{% endstep %}

{% step %}
### Set the registry priority

Set **Priority** to a value higher than the built-in registry.

Recommended starting value:

```
1
```
{% endstep %}

{% step %}
### Add the profile to the registry

Add your new `ConvaiLipSyncProfileAsset` to the **Profiles** list.
{% endstep %}

{% step %}
### Place the registry in the correct Resources path

For the SDK to discover it automatically, the registry must be placed under:

```
Resources/LipSync/ProfileRegistries/
```

Once the asset is saved there, Unity will include it on the next domain reload or Play Mode refresh.
{% endstep %}
{% endstepper %}

## How Runtime Discovery Works

When the Lip Sync profile catalog initializes, it:

1. Loads the built-in registry
2. Scans for additional registries under `Resources/LipSync/ProfileRegistries/`
3. Sorts them by priority
4. Merges all discovered profiles into one runtime catalog

If two registries define the same `Profile ID`, the higher-priority definition replaces the lower-priority one and a warning is logged.

***

## Important Limitations

Keep these points in mind when creating custom profiles:

### Profile IDs should be treated as permanent

Once a profile is referenced by maps, registries, or components, changing the ID can silently break those references.

### Transport formats are fixed

Only these transport formats are supported:

* `arkit`
* `mha`
* `cc4_extended`

Entering a completely custom value does not add support for a new format.

### Registry priority affects replacement behavior

If two registries define the same profile ID, the higher-priority definition replaces the earlier one. There is no merge between duplicate IDs.

***

## Next Step

After creating and registering a profile, the next step is to create or assign a map that targets it.

Continue with [**Creating a Custom Map**](creating-a-custom-map.md) to define how that profile drives your character's actual blendshapes.

## Conclusion

A custom profile is primarily a way to organize and identify a supported Lip Sync schema inside your project. It gives you flexibility in naming and project structure, while still staying within the currently supported transport formats.

If your character needs custom routing to mesh blendshapes, create a map next.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
