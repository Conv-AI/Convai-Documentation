---
title: Unity versions and render pipelines
description: Reference for Convai Unity SDK environment requirements, including the minimum Unity version, required package dependencies, and render pipeline support.
last_reviewed: "4.5.0"
---

The Convai Unity SDK requires Unity <code class="expression">space.vars.unity_min_version</code>. There is no supported configuration on an earlier Unity release. The package contains paths for the Built-in Render Pipeline, URP, and HDRP; validate the pipeline, sample materials, and Vision capture path in the Unity version and build target you ship.

## Unity version requirements

| Requirement                  | Version              |
| ---------------------------- | -------------------- |
| Minimum                      | <code class="expression">space.vars.unity_min_version</code> |
| Recommended for new projects | <code class="expression">space.vars.unity_recommended_version</code> |

{% hint style="warning" %}
The minimum is a hard floor. Convai supports no configuration below Unity <code class="expression">space.vars.unity_min_version</code>, including earlier LTS releases. Upgrade the project before installing the SDK.
{% endhint %}

## Required package dependencies

The SDK manifest declares six Unity package dependencies. Unity Package Manager normally resolves them during installation. After importing through either supported installation path, confirm that Package Manager resolved the versions below and address any project-level version conflict before continuing.

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

The SDK detects the active render pipeline at runtime. The Vision module uses built-in render hooks when no render-pipeline asset is assigned; in URP and HDRP, `Auto` uses the explicit render-compatibility path and performs a bounded extra `Camera.Render()` at the configured capture rate. `SrpNative` is not a production backend in <code class="expression">space.vars.unity_sdk_version</code>.

| Render pipeline | SDK path in <code class="expression">space.vars.unity_sdk_version</code> | Project validation |
| --- | --- | --- |
| Built-in Render Pipeline | Built-in render hooks | Verify the target camera and captured frame in Play Mode and in the target build |
| Universal Render Pipeline (URP) | Explicit render compatibility | Verify frame content and account for the extra render at the configured capture rate |
| High Definition Render Pipeline (HDRP) | Explicit render compatibility | Verify frame content and account for the extra render at the configured capture rate |

The included sample scenes use URP materials. If your project uses the Built-in or HDRP pipeline, sample scene materials require reassignment. The optional depth-of-field camera scripts in `SamplesShared/Camera/` support URP and HDRP; on the Built-in pipeline they skip depth-of-field and log a warning instead. None of these scripts are required for SDK functionality.

## Next steps

With your Unity version and packages confirmed, check which platforms you are targeting.

{% content-ref url="platform-support-matrix.md" %}
[Platform support matrix](platform-support-matrix.md)
{% endcontent-ref %}
