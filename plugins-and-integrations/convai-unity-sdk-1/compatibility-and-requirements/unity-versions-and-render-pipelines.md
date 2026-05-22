---
title: Unity versions and render pipelines
description: Reference for Convai Unity SDK environment requirements, including the minimum Unity version, required package dependencies, and render pipeline support.
last_reviewed: "4.2.0"
---

The Convai Unity SDK requires Unity 2023.1.1f1 or later. All three Unity render pipelines are supported with no additional configuration. Both installation methods — Package Manager and Asset Store — install required package dependencies automatically.

## Unity version requirements

| Requirement                  | Version              |
| ---------------------------- | -------------------- |
| Minimum                      | <code class="expression">space.vars.unity_min_version</code> |
| Recommended for new projects | <code class="expression">space.vars.unity_recommended_version</code> |

{% hint style="warning" %}
The Convai Unity SDK does not support Unity versions earlier than 2023.1.1f1. If your project is on an older LTS release, upgrade before installing.
{% endhint %}

## Required package dependencies

The SDK depends on three Unity packages. Both installation methods install these automatically — you do not need to add them manually unless you encounter a version conflict.

| Package                           | Version |
| --------------------------------- | ------- |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> |
| `com.unity.ugui`                  | <code class="expression">space.vars.dep_ugui_version</code> |
| `com.unity.inputsystem`           | <code class="expression">space.vars.dep_inputsystem_version</code> |

{% hint style="warning" %}
Do not downgrade these packages after installation. The SDK targets the versions listed above and behavior on lower versions is undefined. If your project already pins an older version of any of these in `Packages/manifest.json`, remove or update the pin before installing.
{% endhint %}

## Render pipeline support

The SDK runtime contains no pipeline-specific conditionals. All three Unity render pipelines are fully supported with no additional configuration required.

| Render Pipeline                        | Supported |
| -------------------------------------- | --------- |
| Built-in Render Pipeline               | ✅ Full    |
| Universal Render Pipeline (URP)        | ✅ Full    |
| High Definition Render Pipeline (HDRP) | ✅ Full    |

{% hint style="info" %}
The included sample scenes use URP materials. If your project uses the Built-in or HDRP pipeline, sample scene materials require reassignment. Optional depth-of-field camera scripts in `SamplesShared/Camera/` include pipeline-specific adapters (URP and HDRP) and are not required for SDK functionality.
{% endhint %}

## Next steps

With your Unity version and packages confirmed, check which platforms you are targeting.

{% content-ref url="platform-support-matrix.md" %}
[Platform support matrix](platform-support-matrix.md)
{% endcontent-ref %}
