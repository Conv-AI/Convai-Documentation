---
title: Unity versions and render pipelines
description: Reference for Convai Unity SDK environment requirements, including the minimum Unity version, required package dependencies, and render pipeline support.
last_reviewed: "5.0.0-preview"
---

The Convai Unity SDK requires Unity <code class="expression">space.vars.unity_min_version</code>. There is no supported configuration on an earlier Unity release, and the source includes compatibility handling through Unity `6000.6` for its scene-identity API changes. The runtime supports Built-in, URP and HDRP through pipeline-specific capture paths. Confirm package resolution after installation; an Asset Store distribution may differ from this preview source.

## Unity version requirements

| Requirement                  | Version              |
| ---------------------------- | -------------------- |
| Minimum                      | <code class="expression">space.vars.unity_min_version</code> |
| Recommended for new projects | <code class="expression">space.vars.unity_recommended_version</code> |

{% hint style="warning" %}
The minimum is a hard floor. Convai supports no configuration below Unity <code class="expression">space.vars.unity_min_version</code>, including earlier LTS releases. Upgrade the project before installing the SDK.
{% endhint %}

On Unity 6000.6, legacy 32-bit instance IDs no longer resolve through the SDK tools. Pass the full ID returned by the current tool inspection; do not reuse IDs across Editor sessions.

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

See [Camera vision](../features/vision/frame-sources.md) for the current capture controls. Scene Auto Tagger has its own isolated Editor capture path, supporting Built-in, URP 17.x and HDRP 17.x; its distribution prerequisites remain separate.

The included sample scenes use URP materials. If your project uses the Built-in or HDRP pipeline, sample scene materials require reassignment. The optional depth-of-field camera scripts in `SamplesShared/Camera/` support URP and HDRP; on the Built-in pipeline they skip depth-of-field and log a warning instead. None of these scripts are required for SDK functionality.

## Next steps

With your Unity version and packages confirmed, check which platforms you are targeting.

{% content-ref url="platform-support-matrix.md" %}
[Platform support matrix](platform-support-matrix.md)
{% endcontent-ref %}
