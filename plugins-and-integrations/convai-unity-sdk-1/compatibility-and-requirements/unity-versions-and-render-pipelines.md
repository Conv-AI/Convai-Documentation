---
description: >-
  Minimum Unity version, required package dependencies, and render pipeline
  support for the Convai Unity SDK.
---

# Unity Versions and Render Pipelines

### Supported Environments

The Convai Unity SDK targets Unity 2023.1.1f1 as its minimum supported version. Unity 6 (6000.x) is recommended for new projects. All versions between the minimum and Unity 6 are expected to work but are not explicitly validated on every minor release.

### Unity Version Requirements

| Requirement                  | Version              |
| ---------------------------- | -------------------- |
| Minimum                      | **Unity 2023.1.1f1** |
| Recommended for new projects | **Unity 6 (6000.x)** |

{% hint style="warning" %}
The Convai Unity SDK does not support Unity versions earlier than 2023.1.1f1. If your project is on an older LTS release, upgrade before installing.
{% endhint %}

### Required Package Dependencies

The SDK depends on three Unity packages. Both installation methods (Package Manager and Asset Store) install these automatically — you do not need to add them manually unless you encounter a version conflict.

| Package                           | Version |
| --------------------------------- | ------- |
| `com.unity.nuget.newtonsoft-json` | 3.2.2   |
| `com.unity.ugui`                  | 2.0.0   |
| `com.unity.inputsystem`           | 1.18.0  |

{% hint style="warning" %}
Do not downgrade these packages after installation. The SDK targets the versions listed above and behavior on lower versions is undefined. If your project already pins an older version of any of these in `Packages/manifest.json`, remove or update the pin before installing.
{% endhint %}

### Render Pipeline Support

The SDK runtime contains no pipeline-specific conditionals. All three Unity render pipelines are fully supported with no additional configuration required on your end.

| Render Pipeline                        | Supported |
| -------------------------------------- | --------- |
| Built-in Render Pipeline               | ✅ Full    |
| Universal Render Pipeline (URP)        | ✅ Full    |
| High Definition Render Pipeline (HDRP) | ✅ Full    |

{% hint style="info" %}
The included sample scenes use URP materials. If your project uses the Built-in or HD pipeline, the SDK components require no changes — only the sample scene materials need reassignment. Optional depth-of-field camera scripts in `SamplesShared/Camera/` are also URP-specific and are not required for SDK functionality.
{% endhint %}

### Next Steps

With your Unity version and packages confirmed, check which platforms you are targeting.

{% content-ref url="/broken/pages/17cdf00d4d51e730cf08a14faa6f6a7782f03510" %}
[Broken link](/broken/pages/17cdf00d4d51e730cf08a14faa6f6a7782f03510)
{% endcontent-ref %}
