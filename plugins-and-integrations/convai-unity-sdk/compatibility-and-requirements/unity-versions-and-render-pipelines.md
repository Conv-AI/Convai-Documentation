---
title: Unity versions and render pipelines
description: Reference for Convai Unity SDK environment requirements, including the minimum Unity version, required package dependencies, and render pipeline support.
last_reviewed: "5.0.0-pre.1"
---

The Convai Unity SDK requires Unity <code class="expression">space.vars.unity_min_version</code>. Check the installed package version and dependencies in Package Manager. Vision has separate camera capture paths for the Built-in Render Pipeline, URP, and HDRP.

## Unity version requirements

| Requirement                  | Version              |
| ---------------------------- | -------------------- |
| Minimum                      | <code class="expression">space.vars.unity_min_version</code> |
| Recommended for new projects | <code class="expression">space.vars.unity_recommended_version</code> |

{% hint style="warning" %}
The minimum is a hard floor. Convai supports no configuration below Unity <code class="expression">space.vars.unity_min_version</code>, including earlier LTS releases. Upgrade the project before installing the SDK.
{% endhint %}

Pass the full instance ID returned by the current tool inspection. Keep it as a string when passing it to a command, and inspect again after switching scenes or restarting the Editor.

## Required package dependencies

The SDK depends on seven Unity packages. Package Manager resolves the manifest dependencies. Check an imported Asset Store package against this list and resolve any missing or conflicting dependency.

| Package                           | Version |
| --------------------------------- | ------- |
| `com.unity.ai.inference`          | <code class="expression">space.vars.dep_ai_inference_version</code> |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> |
| `com.unity.ugui`                  | <code class="expression">space.vars.dep_ugui_version</code> |
| `com.unity.inputsystem` | <code class="expression">space.vars.dep_inputsystem_version</code> |
| `com.unity.collections` | <code class="expression">space.vars.dep_collections_version</code> |
| `com.unity.modules.ai` | <code class="expression">space.vars.dep_modules_ai_version</code> |
| `com.unity.modules.xr` | <code class="expression">space.vars.dep_modules_xr_version</code> |

{% hint style="warning" %}
Do not downgrade these packages after installation. The SDK targets the versions listed above and behavior on lower versions is undefined. If your project already pins an older version of any of these in `Packages/manifest.json`, remove or update the pin before installing.
{% endhint %}

NavMesh-driven locomotion needs one more package the SDK does not install. `ConvaiNavMeshLocomotion` drives a built-in Unity `NavMeshAgent`, but NavMesh authoring — `Window > AI > Navigation` and the `NavMeshSurface` component — comes from `com.unity.ai.navigation`. If your project bakes a NavMesh for character movement, install `com.unity.ai.navigation` yourself through Package Manager.

## Render pipeline support

The Vision module selects a capture path for Built-in, URP or HDRP. Use the frame source's Inspector and diagnostic status to confirm the active path. Pipeline support does not remove the need to configure the source camera and test the resulting frames.

| Render pipeline | SDK capture path |
| --- | --- |
| Built-in | Supported camera capture. |
| URP | Supported pipeline-specific capture. |
| HDRP | Supported pipeline-specific capture. |

See [Camera vision](../features/vision/frame-sources.md) for the current capture controls. The [Scene Auto Tagger](../features/scene-metadata/scene-auto-tagger.md) uses an isolated Editor capture path and has its own requirements.

The included sample scenes use URP materials. If your project uses the Built-in or HDRP pipeline, sample scene materials require reassignment. The optional sample camera effects are separate from SDK capture.

## Next steps

With your Unity version and packages confirmed, check which platforms you are targeting.

{% content-ref url="platform-support-matrix.md" %}
[Platform support matrix](platform-support-matrix.md)
{% endcontent-ref %}
