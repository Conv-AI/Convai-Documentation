# unity versions and render pipelines

The Convai Unity SDK requires Unity 2023.1.1f1 or later. Unity 6 (6000.x) is recommended for new projects.

***

## Unity Version Requirements

|                 | Version          |
| --------------- | ---------------- |
| **Minimum**     | Unity 2023.1.1f1 |
| **Recommended** | Unity 6 (6000.x) |

The SDK is tested on the minimum and recommended versions. Versions between 2023.1.1f1 and Unity 6 are expected to work but are not explicitly validated.

***

## Required Package Dependencies

The SDK declares the following dependencies in `package.json`. Unity's Package Manager resolves and installs these automatically.

| Package                           | Required version |
| --------------------------------- | ---------------- |
| `com.unity.nuget.newtonsoft-json` | 3.2.2            |
| `com.unity.ugui`                  | 2.0.0            |
| `com.unity.inputsystem`           | 1.18.0           |

{% hint style="warning" %}
Do not downgrade these packages after installation. The SDK targets the versions listed above and behavior on lower versions is undefined.
{% endhint %}

***

## Render Pipeline Support

| Render pipeline                        | Support level | Notes                                  |
| -------------------------------------- | ------------- | -------------------------------------- |
| Built-in Render Pipeline               | Full          | SDK core has no pipeline-specific code |
| Universal Render Pipeline (URP)        | Full          | Sample scenes are built with URP       |
| High Definition Render Pipeline (HDRP) | Full          | SDK core has no pipeline-specific code |

The SDK runtime contains no `#if USING_URP` or `#if USING_HDRP` conditionals. All three pipelines are supported without any additional configuration.

{% hint style="warning" %}
The included sample scenes (Basic Sample, LipSync Sample) use URP materials. If your project uses the Built-in render pipeline or HDRP, open the sample scenes and reassign the materials. The SDK components themselves require no changes.
{% endhint %}

The only pipeline-specific code in the package exists in `SamplesShared/Camera/` — optional depth-of-field camera scripts for the showcase camera. These are not required for SDK functionality.

***

## Next Steps

{% content-ref url="/broken/pages/9c9c7c5c2d09e0001c82e2a5a4a8fca9c3815b3b" %}
[Broken link](/broken/pages/9c9c7c5c2d09e0001c82e2a5a4a8fca9c3815b3b)
{% endcontent-ref %}

{% content-ref url="/broken/pages/e7c4053fcd48f371ba53dedc370bae1887369155" %}
[Broken link](/broken/pages/e7c4053fcd48f371ba53dedc370bae1887369155)
{% endcontent-ref %}
