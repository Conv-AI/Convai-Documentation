---
title: Face Sync AnimGraph node reference
description: Reference for all properties of the Convai Face Sync AnimGraph node — apply mode, face alphas, smoothing, starvation blending, and blendshape mapping.
last_reviewed: 2026-06-03
---

The `Convai Face Sync` node (`FAnimNode_ConvaiFaceSync`) is an Animation Blueprint node placed in the AnimGraph between a pose source and the output. It reads the current blendshape frame from the `UConvaiFaceSyncComponent` on the owning Actor, applies upper/lower face alphas, optional smoothing, starvation blending, and an optional remapping table, then writes the resulting curve values into the output pose.

The node resolves its chatbot component automatically from the owning Actor when the `Convai Chatbot Component` pin is unset. All properties listed as "pin hidden by default" are accessible through the node's **Details** panel in the Animation Blueprint editor.

## Links

| Property | Type | Default | Description |
|---|---|---|---|
| `SourcePose` | `FPoseLink` | — | The input pose to which facial curves are added or applied. Wire this from the preceding node in the AnimGraph. |
| `ConvaiChatbotComponent` | `UConvaiChatbotComponent*` | `nullptr` | Reference to the chatbot component to read facial data from. When `nullptr`, the node auto-discovers the first `UConvaiChatbotComponent` on the owning Actor. Pin shown by default. |

## Apply mode

| Property | Type | Default | Description |
|---|---|---|---|
| `ApplyMode` | `EConvaiFaceSyncApplyMode` | `Add` | Controls how curve values are written to the output pose. `Add` layers Convai values on top of existing curve values; `Override` replaces existing values entirely. |

### EConvaiFaceSyncApplyMode values

| Value | Behavior |
|---|---|
| `Add` | Adds Convai curve values to whatever curve values the source pose already contains. Use when body or idle animations also drive facial curves and you want to blend them together. |
| `Override` | Replaces existing curve values with Convai curve values. Use when Convai should be the sole driver of the animated curves. |

## Face split

| Property | Type | Default | Description |
|---|---|---|---|
| `UpperFaceBlendshapeNames` | `TArray<FName>` | `[]` | Curve names treated as upper-face shapes (brow, eyes, lids). Every curve not in this list is treated as lower face. Pin hidden by default. |
| `UpperFaceAlpha` | `float` | `0.8` | Scale applied to upper-face curve values. Clamped to `[0.0, 1.0]`. Pin hidden by default. |
| `LowerFaceAlpha` | `float` | `1.0` | Scale applied to lower-face curve values. Clamped to `[0.0, 1.0]`. Pin hidden by default. |

When `UpperFaceBlendshapeNames` is empty, all curves receive the `LowerFaceAlpha` scale.

## Smoothing

Smoothing uses `FMath::FInterpTo`, which is frame-rate independent. A higher speed value produces a faster response; a lower value produces a smoother but more lagged result.

| Property | Type | Default | Description |
|---|---|---|---|
| `bEnableLowerFaceSmoothing` | `bool` | `false` | Enables exponential moving-average smoothing for lower-face curves. |
| `LowerFaceSmoothingSpeed` | `float` | `1.0` | Interp speed for lower-face smoothing. Active only when `bEnableLowerFaceSmoothing` is `true`. Clamped to `[0.0, 1.0]`. Pin hidden by default. |
| `bEnableUpperFaceSmoothing` | `bool` | `false` | Enables exponential moving-average smoothing for upper-face curves. |
| `UpperFaceSmoothingSpeed` | `float` | `1.0` | Interp speed for upper-face smoothing. Active only when `bEnableUpperFaceSmoothing` is `true`. Clamped to `[0.0, 1.0]`. Pin hidden by default. |

## Starvation blending

When the lip-sync buffer runs out of frames — for example between speech turns or before the first frame arrives — the node blends the curve contribution to zero. When frames become available again, it blends back in. This prevents the face from snapping to neutral and back.

| Property | Type | Default | Description |
|---|---|---|---|
| `StarvationBlendInDuration` | `float` | `0.1` | Seconds to blend curve contribution from `0` to `1` when frames become available. Set to `0` for an instant transition. Pin hidden by default. |
| `StarvationBlendOutDuration` | `float` | `0.8` | Seconds to blend curve contribution from `1` to `0` when the buffer is empty. Set to `0` for an instant transition. Pin hidden by default. |

Both values apply as a constant rate. A mid-transition reversal takes proportionally less time than a full transition.

## Blendshape mapping

| Property | Type | Default | Description |
|---|---|---|---|
| `BlendshapeMapping` | `TMap<FName, FConvaiBlendshapeParameters>` | `{}` | Optional remapping table. The key is the source curve name from Convai; the value is a `FConvaiBlendshapeParameters` struct that defines target curve names, a per-entry multiplier, offset, clamping, and optional override. When empty, curves are applied 1:1 with no remapping. Pin hidden by default. |
| `GlobalMultiplier` | `float` | `1.0` | Multiplier applied to all mapped curve values, unless `IgnoreGlobalModifiers` is set on the entry. Pin hidden by default. |
| `GlobalOffset` | `float` | `0.0` | Offset added to all mapped curve values, unless `IgnoreGlobalModifiers` is set on the entry. Pin hidden by default. |

### FConvaiBlendshapeParameters fields

`FConvaiBlendshapeParameters` defines the per-entry mapping behavior. All fields are Blueprint read/write.

| Field | Type | Default | Description |
|---|---|---|---|
| `TargetNames` | `TArray<FName>` | `[]` | One or more target curve names on the Skeletal Mesh to write the source value to. A single source curve can fan out to multiple targets. |
| `Multiplyer` | `float` | `1.0` | Per-entry scale applied before `GlobalMultiplier` (unless `IgnoreGlobalModifiers` is `true`). Note: the field name contains a typo in the source — it is `Multiplyer`, not `Multiplier`. |
| `Offset` | `float` | `0.0` | Per-entry offset added after scaling. |
| `UseOverrideValue` | `bool` | `false` | When `true`, the curve is set to `OverrideValue` regardless of the incoming data. Useful for pinning a curve to a fixed value. |
| `OverrideValue` | `float` | `0.0` | The fixed value to use when `UseOverrideValue` is `true`. |
| `IgnoreGlobalModifiers` | `bool` | `false` | When `true`, `GlobalMultiplier` and `GlobalOffset` are not applied to this entry. |
| `ClampMinValue` | `float` | `0.0` | Minimum value the curve is allowed to reach after all scaling and offsets. |
| `ClampMaxValue` | `float` | `1.0` | Maximum value the curve is allowed to reach after all scaling and offsets. |

## Command-line overrides

Property values can be overridden at launch using `-LipSyncAnim*` command-line flags. Overrides are resolved once per PIE session during `Initialize_AnyThread`. The following properties support a corresponding command-line flag:

- `UpperFaceAlpha`
- `LowerFaceAlpha`
- `StarvationBlendInDuration`
- `StarvationBlendOutDuration`
- `GlobalMultiplier`
- `GlobalOffset`
- `LowerFaceSmoothingSpeed`
- `UpperFaceSmoothingSpeed`
- `bEnableLowerFaceSmoothing`
- `bEnableUpperFaceSmoothing`
- A bypass flag for smoothing (`bBypassSmoothing`)
- A bypass flag for starvation blending (`bBypassStarvationBlend`)
- `ApplyMode`

Exact flag names are documented in the plugin source at `Convai/Docs/LipSyncAnimCommandLineFlags.md` inside the plugin directory.

## Related reference

{% content-ref url="face-sync-component-reference.md" %}
[Face Sync component reference](face-sync-component-reference.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
