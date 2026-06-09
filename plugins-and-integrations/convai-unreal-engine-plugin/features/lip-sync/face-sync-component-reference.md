---
title: Face Sync component reference
description: Property reference for the Convai Face Sync component and all six lip-sync mode values with rig compatibility guidance for MetaHuman, CC4, CC5, and custom rigs.
last_reviewed: 2026-06-05
---

`UConvaiFaceSyncComponent` is a Scene Component (Blueprint display name **"Convai Face Sync"**) that receives precomputed facial animation data from Convai, buffers it, and exposes the current blendshape frame each tick. It implements `IConvaiLipSyncInterface` and sets `RequiresPrecomputedFaceData()` to `true`, which instructs the audio streamer to request facial data from Convai.

Add it to the same Actor as `UConvaiChatbotComponent`. The `FAnimNode_ConvaiFaceSync` AnimGraph node reads from it automatically when both components are on the same Actor.

## Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `LipSyncMode` | `EC_LipSyncMode` | `BS_MHA` | Selects the blendshape set Convai produces when the project-wide **Lip Sync Mode** is `Auto`. Must match the curves available on the character's Skeletal Mesh. Exposed in the **Details** panel under **Convai\|LipSync** and as a Blueprint read/write property. |
| `bEnableInterpolation` | `bool` | `false` | When `true`, the component interpolates between consecutive blendshape frames to smooth playback. Exposed in the **Details** panel under **Convai\|LipSync**; not a Blueprint read/write property. |

## EC_LipSyncMode values

`EC_LipSyncMode` is a Blueprint-exposed enum (`UENUM(BlueprintType)`) defined in `ConvaiDefinitions.h`.

| Value | Display name | Compatible rigs | Notes |
|---|---|---|---|
| `Off` | `Off` | — | Disables lip sync when used as the project-wide value, or when the project-wide value is `Auto` and the component value is `Off`. |
| `Auto` | `Auto` | Per-character rigs | As the project-wide value, uses the attached `UConvaiFaceSyncComponent`'s `LipSyncMode` at runtime to select the blendshape format. The selection happens locally in the plugin, not by Convai. |
| `VisemeBased` | `Viseme Based` | Custom rigs with OVR viseme curves | Produces 15 OVR viseme curve names: `sil`, `PP`, `FF`, `TH`, `DD`, `kk`, `CH`, `SS`, `nn`, `RR`, `aa`, `E`, `ih`, `oh`, `ou`. |
| `BS_MHA` | `MetaHuman Blendshapes` | MetaHuman, CC5 | Produces MetaHuman CTRL curve names. This is the default mode. |
| `BS_ARKit` | `ARKit Blendshapes` | CC4 | Produces 61 ARKit blendshape curve names (52 standard Apple ARKit + 9 head/eye rotation curves). |
| `BS_CC4_Extended` | `CC4 Extended Blendshapes` | CC4 with extended blendshape sets | Produces CC4 Extended curve names. Use when the CC4 character was exported with the extended blendshape option enabled in Character Creator 4. |

### Choosing the right mode

When the project-wide **Lip Sync Mode** is `Auto`, each component's `LipSyncMode` value must correspond to the curve names present on the character's Skeletal Mesh asset. If the mode does not match the rig, the AnimGraph node receives data but finds no matching curves to write, and the face does not animate.

- **MetaHuman characters:** use `BS_MHA`.
- **CC5 characters:** use `BS_MHA`.
- **CC4 characters (standard export):** use `BS_ARKit`.
- **CC4 characters (extended blendshape export):** use `BS_CC4_Extended`.
- **Custom rigs with OVR viseme targets:** use `VisemeBased`.

{% hint style="info" %}
You can set a project-wide default in **Edit > Project Settings > Plugins > Convai > Advanced > Lip Sync Mode**. Use `Auto` when characters in the project use different rigs so the plugin reads each component's `LipSyncMode` at runtime. For `BS_CC4_Extended`, leave the project-wide setting on `Auto` and set `LipSyncMode` on the `Convai Face Sync` component.
{% endhint %}

## Recording API (C++ only)

`UConvaiFaceSyncComponent` provides a C++ recording API that lets you capture a live lip-sync sequence during a conversation and replay it later — for example in a cutscene, a cached response, or an offline preview. These methods are plain C++ members with no `UFUNCTION` decoration and are not accessible from Blueprints.

| Method | Returns | Description |
|---|---|---|
| `StartRecordingLipSync()` | `void` | Begins capturing incoming blendshape frames from Convai into an internal buffer. Call this before or during a conversation turn to record the live facial data. |
| `FinishRecordingLipSync()` | `FAnimationSequenceBP` | Stops recording and returns the captured sequence as an `FAnimationSequenceBP`. The returned struct wraps an `FAnimationSequence` (frame array, duration, frame rate) and can be stored in a variable or passed to `PlayRecordedLipSync`. |
| `PlayRecordedLipSync(FAnimationSequenceBP RecordedLipSync, int StartFrame, int EndFrame, float OverwriteDuration)` | `bool` | Replays a previously captured sequence. `StartFrame` and `EndFrame` define the frame range to replay; pass `0` and `-1` to replay the full sequence. `OverwriteDuration` overrides the sequence's stored duration when greater than zero. Returns `false` if the sequence is invalid, if recording is active, or if the requested frame range is invalid. |

`FAnimationSequenceBP` is a C++ struct wrapping an `FAnimationSequence` (frame-indexed frame array with frame rate and duration). It is defined in `ConvaiDefinitions.h` and is the return type of `FinishRecordingLipSync`.

{% hint style="info" %}
Recorded sequences replay the exact blendshape data that was captured. They do not re-stream from Convai, and playback is independent of any active conversation.
{% endhint %}

## Status queries (C++ only)

These C++ methods let you poll the component's current playback state. They have no `UFUNCTION` decoration and are not accessible from Blueprints.

| Method | Returns | Description |
|---|---|---|
| `IsPlaying() const` | `bool` | Returns `true` when the component is actively replaying frames (either from a live stream or a recorded sequence). |
| `GetCurrentFrame()` | `TMap<FName, float>` | Returns the blendshape name-to-weight map for the frame the component is currently applying. Useful for debugging or driving secondary systems from the same data. |

## Related reference

{% content-ref url="face-sync-anim-node-reference.md" %}
[Face Sync AnimGraph node reference](face-sync-anim-node-reference.md)
{% endcontent-ref %}

{% content-ref url="recording-lip-sync.md" %}
[Record and replay lip sync](recording-lip-sync.md)
{% endcontent-ref %}

{% content-ref url="how-lip-sync-works.md" %}
[How lip sync works](how-lip-sync-works.md)
{% endcontent-ref %}
