---
title: Unity versions and render pipelines
description: Reference for Convai Unity SDK environment requirements, including the minimum Unity version, required package dependencies, and render pipeline support.
last_reviewed: "4.4.0"
---

The Convai Unity SDK requires Unity <code class="expression">space.vars.unity_min_version</code>. All three Unity render pipelines are supported with no additional configuration. Both installation methods — Package Manager and Asset Store — install required package dependencies automatically.

## Unity version requirements

| Requirement                  | Version              |
| ---------------------------- | -------------------- |
| Minimum                      | <code class="expression">space.vars.unity_min_version</code> |
| Recommended for new projects | <code class="expression">space.vars.unity_recommended_version</code> |

{% hint style="warning" %}
The Convai Unity SDK does not support Unity versions earlier than <code class="expression">space.vars.unity_min_version</code>. If your project is on an older LTS release, upgrade before installing.
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

The SDK detects the active render pipeline at runtime and adapts automatically — for example, the Vision module's camera capture path switches between built-in render hooks and an explicit SRP-compatible path. All three Unity render pipelines are fully supported with no manual configuration required.

| Render Pipeline                        | Supported |
| -------------------------------------- | --------- |
| Built-in Render Pipeline               | ✅ Full    |
| Universal Render Pipeline (URP)        | ✅ Full    |
| High Definition Render Pipeline (HDRP) | ✅ Full    |

{% hint style="info" %}
The included sample scenes use URP materials. If your project uses the Built-in or HDRP pipeline, sample scene materials require reassignment. Optional depth-of-field camera scripts in `SamplesShared/Camera/` support URP and HDRP; on the Built-in pipeline they skip depth-of-field and log a warning instead. None of these scripts are required for SDK functionality.
{% endhint %}

## Next steps

With your Unity version and packages confirmed, check which platforms you are targeting.

{% content-ref url="platform-support-matrix.md" %}
[Platform support matrix](platform-support-matrix.md)
{% endcontent-ref %}
