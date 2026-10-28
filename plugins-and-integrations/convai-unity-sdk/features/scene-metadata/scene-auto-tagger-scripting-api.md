---
title: Scene Auto Tagger scripting API
description: Use the editor-only tagging API to prepare object descriptions, inspect typed failures, and apply approved results with Undo and conflict checks.
last_reviewed: "5.0.0-preview"
---

`Convai.Editor.SceneTagging.ConvaiSceneTagger` exposes the window's analysis pipeline for Editor tooling. It supports Windows and macOS Editors in Edit mode. Call from the Unity main thread and await the task; blocking on `.Result` can prevent capture frames from progressing.

{% hint style="warning" %}
These APIs depend on the same preview Core and service as the window. The reviewed Core is `unsigned-internal-prerelease` and has `customerDistributionReady: false`. An SDK/Core release owner must approve distribution and service availability before this workflow is presented as a supported public release.
{% endhint %}

## Analyze without changing the scene

The following are API signatures, not standalone scripts. Put caller code in an Editor assembly or guard it with `UNITY_EDITOR`.

```csharp
public static Task<ConvaiSceneTagResult> TagAsync(
    ConvaiSceneTagRequest request,
    IProgress<ConvaiSceneTagProgress> progress = null,
    CancellationToken cancellationToken = default)

public static Task<ConvaiSceneDescriptionResult> DescribeViewAsync(
    string characterId, Camera camera = null,
    CancellationToken cancellationToken = default)
```

Request/result types live in `Convai.Runtime.SceneTagging`; the executable API is Editor-only. `DescribeViewAsync` uses the supplied camera or last active Scene view to draft environment text. Neither method changes scene components.

| Request member | Constraint |
| --- | --- |
| `CharacterId` | Valid character GUID with service access |
| `Targets` | 1–300 `ConvaiSceneTagTarget` entries |
| `SceneDescription` | Up to 800 characters |
| `Focus` | Up to 400 characters |
| `Quality` | `Fast` by default, or `Accurate` |
| `IncludeLowInformation` | Whether captures with little visual detail may be analyzed |

Create a target with `new ConvaiSceneTagTarget(id, anchor, renderers, note)`. IDs and anchors must be unique within a request. Optional renderer sets must be nonempty and cannot share renderers across targets. A target accepts up to 4,096 renderers and a note up to 300 characters. Inactive, unloaded, uncapturable, player, or character objects can be ineligible.

Progress reports `Phase`, `Completed`, and `Total` on the main thread. Phases are `Capturing` and `Analyzing`. Cancellation is also triggered by script reload or entering Play mode; an in-flight Vision call completes before the task finishes cancellation.

## Inspect every result

`ConvaiSceneTagResult` exposes `Succeeded`, `Failure`, `Message`, and `Objects`. A successful run does not imply every object was tagged. Each object's `Status`, `Failure`, `Message`, and `IsTagged` explain its outcome; tagged entries include `Name`, `Description`, and `Confidence`.

| Status | Meaning |
| --- | --- |
| `Tagged` | A name and description were returned |
| `NotAnalyzed` | The run stopped before this target was analyzed |
| `NotEligible` | The target cannot be captured under the API's object rules |
| `CaptureFailed` | No usable capture was produced |
| `LowInformation` | Capture was not submitted because it lacked useful visual detail |
| `AnalysisFailed` | No usable description was returned |

Run-level failures include `InvalidRequest`, `MissingApiKey`, `Unauthorized`, `UsageLimitReached`, `RateLimited`, `ServiceError`, `NetworkError`, `InvalidResponse`, and `NativeCoreUnavailable`. `DescribeViewAsync` can also return `CaptureFailed`. Invalid null arguments, thread/mode misuse, and cancellation are exceptions rather than result failures.

## Apply approved results

```csharp
public static ConvaiSceneTagApplyResult Apply(
    IEnumerable<ConvaiSceneTagObjectResult> results,
    ConvaiSceneTagApplyOptions options = null)
```

Review results first, and use `WithText(name, description)` to make explicit corrections. Apply accepts results produced by this Editor session, with no duplicate tagged object in the same call. It writes a single Undo step and marks scenes dirty without saving.

`ConvaiSceneTagApplyOptions` defaults `IncludeSpatialContext`, `EnableGaze`, and `CreateActionTargets` to true. Inspect each returned `Items` entry's `Id` and `Outcome`; results can preserve authored metadata, edited companions, or an existing logical group instead of applying. Changed geometry, transforms, or materials require a fresh capture. Text is trimmed and fitted to 64/320 UTF-16 authoring limits without splitting surrogate pairs.

The API's per-target Apply does not replace the window's multi-object grouping review. Runtime payload size, targeting, navigation, and conversational behavior still require their own checks after authoring.

## Next steps

{% content-ref url="scene-auto-tagger-window-reference.md" %}
[Scene Auto Tagger window reference](scene-auto-tagger-window-reference.md)
{% endcontent-ref %}
{% content-ref url="scripting-api-reference.md" %}
[Scene metadata scripting API](scripting-api-reference.md)
{% endcontent-ref %}
