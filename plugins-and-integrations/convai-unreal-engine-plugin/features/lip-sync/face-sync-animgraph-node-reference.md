---
title: Face Sync AnimGraph node reference
description: Reference for all properties of the Convai Face Sync AnimGraph node — apply mode, face alphas, smoothing, starvation blending, and blendshape mapping.
last_reviewed: "4.0.0-beta.21"
---

The `Convai Face Sync` node (`FAnimNode_ConvaiFaceSync`) is an Animation Blueprint node placed in the AnimGraph between a pose source and the Output Pose. It reads facial data from the `Convai Chatbot` component on the same Actor, applies upper/lower face alphas, optional smoothing, starvation blending, and an optional remapping table, then writes the resulting curve values into the output pose.

The node resolves its chatbot component automatically from the owning Actor when the `Convai Chatbot Component` pin is unset. All properties listed as "pin hidden by default" are accessible through the node's **Details** panel in the Animation Blueprint editor.

## Pose input and component link

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

Smoothing uses an exponential moving average (EMA). The speed value is clamped to `[0.0, 1.0]` in the editor. `0.0` produces the most lag (the value barely moves toward the target each frame); `1.0` is instant (no smoothing, value reaches the target in one frame). At `0.5` and 60 fps, each curve moves roughly 50% toward its target per frame. Practical starting points: `0.3`–`0.5` for a smooth, responsive lower face; `0.1`–`0.2` for a more restrained upper face.

| Property | Type | Default | Description |
|---|---|---|---|
| `bEnableLowerFaceSmoothing` | `bool` | `false` | Enables exponential moving average smoothing for lower-face curves. |
| `LowerFaceSmoothingSpeed` | `float` | `1.0` | EMA speed for lower-face smoothing. Clamped to `[0.0, 1.0]` in the editor: `0.0` = maximum lag, `1.0` = instant. Active only when `bEnableLowerFaceSmoothing` is `true`. Pin hidden by default. |
| `bEnableUpperFaceSmoothing` | `bool` | `false` | Enables exponential moving average smoothing for upper-face curves. |
| `UpperFaceSmoothingSpeed` | `float` | `1.0` | EMA speed for upper-face smoothing. Clamped to `[0.0, 1.0]` in the editor: `0.0` = maximum lag, `1.0` = instant. Active only when `bEnableUpperFaceSmoothing` is `true`. Pin hidden by default. |

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

The tunable properties listed below can be overridden at launch by passing a `-LipSyncAnim*` flag. Overrides are resolved once per PIE session in `Initialize_AnyThread` and take precedence over the value authored in the Animation Blueprint. Flags not set on the command line fall through to the `UPROPERTY` value.

| Flag | Type | Example |
|---|---|---|
| `-LipSyncAnimUpperFaceAlpha` | `float` | `-LipSyncAnimUpperFaceAlpha=0.5` |
| `-LipSyncAnimLowerFaceAlpha` | `float` | `-LipSyncAnimLowerFaceAlpha=0.8` |
| `-LipSyncAnimStarvationBlendInDuration` | `float` | `-LipSyncAnimStarvationBlendInDuration=0.05` |
| `-LipSyncAnimStarvationBlendOutDuration` | `float` | `-LipSyncAnimStarvationBlendOutDuration=1.2` |
| `-LipSyncAnimGlobalMultiplier` | `float` | `-LipSyncAnimGlobalMultiplier=1.2` |
| `-LipSyncAnimGlobalOffset` | `float` | `-LipSyncAnimGlobalOffset=0.0` |
| `-LipSyncAnimLowerFaceSmoothingSpeed` | `float` | `-LipSyncAnimLowerFaceSmoothingSpeed=0.4` |
| `-LipSyncAnimUpperFaceSmoothingSpeed` | `float` | `-LipSyncAnimUpperFaceSmoothingSpeed=0.2` |
| `-LipSyncAnimEnableLowerFaceSmoothing` | `bool` (`1`/`true`) | `-LipSyncAnimEnableLowerFaceSmoothing=1` |
| `-LipSyncAnimEnableUpperFaceSmoothing` | `bool` (`1`/`true`) | `-LipSyncAnimEnableUpperFaceSmoothing=1` |
| `-LipSyncAnimBypassSmoothing` | `bool` (`1`/`true`) | `-LipSyncAnimBypassSmoothing=1` |
| `-LipSyncAnimBypassStarvationBlend` | `bool` (`1`/`true`) | `-LipSyncAnimBypassStarvationBlend=1` |
| `-LipSyncAnimApplyMode` | `Add` or `Override` | `-LipSyncAnimApplyMode=Override` |

{% hint style="info" %}
Command-line overrides apply per-process. They are useful for tuning lip sync behavior during development without editing and recompiling the Animation Blueprint. They do not persist across editor restarts.
{% endhint %}

## Related reference

{% content-ref url="face-sync-component-reference.md" %}
[Face Sync component reference](face-sync-component-reference.md)
{% endcontent-ref %}

{% content-ref url="lip-sync-usage-examples.md" %}
[Lip sync usage examples](lip-sync-usage-examples.md)
{% endcontent-ref %}
