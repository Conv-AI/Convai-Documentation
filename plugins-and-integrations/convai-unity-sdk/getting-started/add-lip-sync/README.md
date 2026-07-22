---
title: Add lip sync
description: >-
  Connect Convai audio output to your character's facial blendshapes,
  synchronize mouth movement with speech, and tune playback latency.
last_reviewed: "4.4.0"
---

The Convai SDK for Unity includes a real-time lip sync system that drives `SkinnedMeshRenderer` blendshapes in sync with the character's voice audio. It supports three industry-standard blendshape formats and handles playback buffering, smoothing, and fade-out automatically.

## How it works

When Convai sends voice audio, it also streams a sequence of blendshape frames in the character's transport format (ARKit, MetaHuman, or CC4 Extended). The SDK buffers and interpolates these frames, applies optional smoothing, and writes the result to your character's `SkinnedMeshRenderer` every frame.

```mermaid
graph LR
    A[Convai: voice + blendshape frames] --> B[ConvaiLipSyncComponent]
    B --> C[Frame buffer + interpolation]
    C --> D[Smoothing]
    D --> E[SkinnedMeshRenderer blendshapes]
```

## Quick setup

{% stepper %}
{% step %}
### Add the component

Add `ConvaiLipSyncComponent` to the same GameObject as your `ConvaiCharacter` (or to any child GameObject).
{% endstep %}

{% step %}
### Set the profile ID

In the Inspector, set **Locked Profile ID** to the transport format your character uses:

* `arkit` — Apple ARKit (61 blendshapes)
* `metahuman` — Unreal MetaHuman (251 blendshapes)
* `cc4_extended` — Character Creator 4 Extended (170 blendshapes)
{% endstep %}

{% step %}
### Assign target meshes

In the **Target Meshes** list, add all `SkinnedMeshRenderer` components that have facial blendshapes.
{% endstep %}

{% step %}
### Enter Play Mode

Leave **Mapping** empty — the SDK auto-selects a matching bundled map for the chosen profile. Enter Play Mode and speak to the character.

The character's mouth moves in sync with its voice output.

{% hint style="warning" %}
If the mouth does not move, confirm that your `SkinnedMeshRenderer` blendshape names match the expected naming convention for the chosen profile. ARKit uses camelCase names (e.g., `jawOpen`, `mouthSmileLeft`). MetaHuman uses the `CTRL_expressions_` prefix. Use a custom map if your rig uses different names — see [Profiles and mappings](profiles-and-mappings.md).
{% endhint %}
{% endstep %}
{% endstepper %}

## Bundled profiles

Choose the profile that matches the blendshape format your character was rigged with.

| Profile      | Locked Profile ID | Blendshapes | Typical character source                  |
| ------------ | ----------------- | ----------- | ----------------------------------------- |
| ARKit        | `arkit`           | 61          | Apple-rigged characters, some custom rigs |
| MetaHuman    | `metahuman`       | 251         | Unreal MetaHuman exported to Unity        |
| CC4 Extended | `cc4_extended`    | 170         | Reallusion Character Creator 4 characters |

If your character was rigged with non-standard blendshape names, create a custom map to route the SDK's output channels to your rig's actual names.

{% content-ref url="profiles-and-mappings.md" %}
[Profiles and mappings](profiles-and-mappings.md)
{% endcontent-ref %}

## Playback settings

**Core setup:**

| Field              | Default        | Description                                                            |
| ------------------ | -------------- | ---------------------------------------------------------------------- |
| `_lockedProfileId` | `arkit`        | Transport format the SDK streams (`arkit`, `metahuman`, `cc4_extended`) |
| `_mapping`         | _(none)_       | Optional custom mapping asset (leave empty to use bundled auto-map)    |
| `_targetMeshes`    | _(empty list)_ | `SkinnedMeshRenderer` components to write blendshapes to               |

**Playback & behavior:**

| Field              | Default | Range    | Description                                                    |
| ------------------ | ------- | -------- | -------------------------------------------------------------- |
| `_smoothingFactor` | `0.5`   | 0–0.9    | Exponential smoothing per frame (higher = smoother but slower) |
| `_fadeOutDuration` | `0.2`   | 0.05–2.0 | Seconds to fade all blendshapes to 0 after audio ends          |
| `_fadeInDuration`  | `0.1`   | 0–0.5    | Seconds to blend from the pre-playback pose into the first sampled frames at the start of playback, removing the first-frame pop when a response begins (`0` disables it) |
| `_timeOffset`      | `0.0`   | -0.5–0.5 | Shift playback timing relative to audio (negative = earlier)   |

**Streaming & latency:**

| Field                       | Default    | Range    | Description                                          |
| --------------------------- | ---------- | -------- | ---------------------------------------------------- |
| `_latencyMode`              | `Balanced` | —        | Preset that controls buffer depth vs. responsiveness |
| `_maxBufferedSeconds`       | `3.0`      | 1–10     | Ring buffer capacity in seconds                      |
| `_minResumeHeadroomSeconds` | `0.12`     | 0.05–0.3 | Buffer refill threshold after starvation             |
| `_deliverChunksAhead`       | `false`    | —        | Preview opt-in for indexed NeuroSync chunks          |

**Latency mode options:**

| Mode              | Use case                                                         |
| ----------------- | ---------------------------------------------------------------- |
| `Balanced`        | Default. Recommended for most deployments                        |
| `UltraLowLatency` | Minimal delay; susceptible to starvation on unstable connections |
| `NetworkSafe`     | High buffering; best for unreliable or high-latency networks     |
| `Custom`          | Unlocks manual control over buffer fields above                  |

## Ahead chunk delivery preview

**Ahead Chunk Delivery (Preview)** enables the SDK to request indexed NeuroSync chunks before their playback position. Leave it disabled for normal projects. Enable it only when you are testing the preview ahead-chunk path for a character that already uses `ConvaiLipSyncComponent`.

When `_deliverChunksAhead` is enabled, the SDK sends `deliver_chunks_ahead=true` in the room connection lip sync configuration. The default request does not include this field, so existing lip sync behavior stays unchanged unless you turn on the preview option.

The SDK buffers ahead chunks by their frame index and waits until frames are contiguous from the start of the response before it starts feeding them to the playback engine. Visual output still waits for the character audio playback signal, so the mouth does not start moving before audible speech begins. If Convai cancels the current NeuroSync timeline or the character turn ends because of an interruption, the SDK clears buffered mouth frames before the next response.

## Usage examples

### Example 1: ARKit character

**Scenario:** A corporate training simulation uses a character rigged with Apple ARKit blendshapes.

**Setup:**

1. Add `ConvaiLipSyncComponent` to the NPC GameObject (same as `ConvaiCharacter`).
2. Set `_lockedProfileId` to `arkit`.
3. In the **Target Meshes** list, add the `SkinnedMeshRenderer` from the avatar's head mesh.
4. Leave `_mapping` empty — the bundled ARKit auto-map covers standard camelCase ARKit blendshape names (`jawOpen`, `mouthSmileLeft`, etc.).

**Expected outcome:** The avatar's mouth, lips, and jaw animate in sync with the character's voice during conversation. Blendshapes return to neutral smoothly after each response ends (`_fadeOutDuration` = 0.2s default).

### Example 2: MetaHuman character

**Scenario:** A high-fidelity medical simulation uses an Unreal MetaHuman character exported to Unity.

**Setup:**

1. Add `ConvaiLipSyncComponent` to the NPC GameObject.
2. Set `_lockedProfileId` to `metahuman`.
3. In the **Target Meshes** list, add all `SkinnedMeshRenderer` components on the MetaHuman head and teeth meshes — MetaHuman separates these into multiple renderers.
4. Leave `_mapping` empty — the bundled MetaHuman map targets `CTRL_expressions_` prefixed blendshapes.
5. Increase `_smoothingFactor` to `0.7` for more fluid animation on high-poly rigs.

**Expected outcome:** All facial regions animate together — lips, jaw, cheeks, and tongue shapes — producing highly realistic mouth movement. Smoothing reduces per-frame jitter visible on high-resolution meshes.

## Next steps

After lip sync is configured, validate your complete setup.

{% content-ref url="../validate-your-setup.md" %}
[Validate your setup](../validate-your-setup.md)
{% endcontent-ref %}
