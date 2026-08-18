---
title: Unity versions and render pipelines
description: Reference for Convai Unity SDK environment requirements, including the minimum Unity version, required package dependencies, and render pipeline support.
last_reviewed: "4.5.0"
---

The Convai Unity SDK requires Unity <code class="expression">space.vars.unity_min_version</code>. There is no supported configuration on an earlier Unity release. All three Unity render pipelines are supported with no additional configuration, and both installation methods — Package Manager and Asset Store — resolve the required package dependencies automatically.

## Unity version requirements

| Requirement                  | Version              |
| ---------------------------- | -------------------- |
| Minimum                      | <code class="expression">space.vars.unity_min_version</code> |
| Recommended for new projects | <code class="expression">space.vars.unity_recommended_version</code> |

{% hint style="warning" %}
The minimum is a hard floor. Convai supports no configuration below Unity <code class="expression">space.vars.unity_min_version</code>, including earlier LTS releases. Upgrade the project before installing the SDK.
{% endhint %}

## Required package dependencies

The SDK depends on six Unity packages. Both installation methods install these automatically — you do not need to add them manually unless you encounter a version conflict.

| Package                           | Version |
| --------------------------------- | ------- |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> |
| `com.unity.ugui`                  | <code class="expression">space.vars.dep_ugui_version</code> |
| `com.unity.inputsystem`           | <code class="expression">space.vars.dep_inputsystem_version</code> |
| `com.unity.ai.navigation`         | <code class="expression">space.vars.dep_ai_navigation_version</code> |
| `com.unity.collections`           | <code class="expression">space.vars.dep_collections_version</code> |
| `com.unity.modules.xr`            | <code class="expression">space.vars.dep_modules_xr_version</code> |

{% hint style="warning" %}
Do not downgrade these packages after installation. The SDK targets the versions listed above and behavior on lower versions is undefined. If your project already pins an older version of any of these in `Packages/manifest.json`, remove or update the pin before installing.
{% endhint %}

## Render pipeline support

The SDK detects the active render pipeline at runtime and adapts automatically. The Vision module's camera capture path, for example, uses built-in render hooks when no render pipeline asset is assigned and an explicit render path on URP and HDRP. All three Unity render pipelines are fully supported with no manual configuration required.

| Render Pipeline                        | Supported |
| -------------------------------------- | --------- |
| Built-in Render Pipeline               | ✅ Full    |
| Universal Render Pipeline (URP)        | ✅ Full    |
| High Definition Render Pipeline (HDRP) | ✅ Full    |

Support requires no manual configuration on any pipeline, but the Vision module's `CameraVisionFrameSource` captures differently depending on the pipeline. On the Built-in pipeline it uses command-buffer render hooks with no extra render pass. On URP and HDRP it falls back to an explicit render-compatibility path that issues one additional `Camera.Render()` call per captured frame.

The included sample scenes use URP materials. If your project uses the Built-in or HDRP pipeline, sample scene materials require reassignment. The optional depth-of-field camera scripts in `SamplesShared/Camera/` support URP and HDRP; on the Built-in pipeline they skip depth-of-field and log a warning instead. None of these scripts are required for SDK functionality.

## Next steps

With your Unity version and packages confirmed, check which platforms you are targeting.

{% content-ref url="platform-support-matrix.md" %}
[Platform support matrix](platform-support-matrix.md)
{% endcontent-ref %}
