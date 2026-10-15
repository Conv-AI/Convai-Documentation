---
title: Apply MetaHuman limit drivers
description: Apply the MetaHuman rig couplings, tuned gains, and fade envelope to the 251-channel stream so a character's lips stay closed while its jaw moves.
last_reviewed: "2.0.0"
---

Apply the MetaHuman rig couplings to every `mha` frame before you write it to a character's morph targets. Use this page when a character driven by the `mha` format shows its teeth on every jaw movement. At the end, the lips stay in contact while the jaw opens and the mouth reads as speech rather than flapping.

## Why the mha stream needs couplings

The `mha` stream is authored against Unreal's MetaHuman rig, which drives some controls from others. A glTF export of the same character has the morph targets but not those couplings. The most visible one is `jawOpen` driving the four `mouthLipsTogether*` controls: without it, every jaw opening separates the lips and bares the teeth.

Each coupling sets the target channel to the larger of its own value and the source value. The SDK applies these 11 couplings:

| Source | Target |
|---|---|
| `eyeBlinkL` | `eyeLidPressL` |
| `eyeBlinkR` | `eyeLidPressR` |
| `noseWrinkleL` | `noseWrinkleUpperL` |
| `noseWrinkleR` | `noseWrinkleUpperR` |
| `mouthStretchL` | `mouthStretchLipsCloseL` |
| `mouthStretchR` | `mouthStretchLipsCloseR` |
| `jawOpen` | `jawOpenExtreme` |
| `jawOpen` | `mouthLipsTogetherUL` |
| `jawOpen` | `mouthLipsTogetherUR` |
| `jawOpen` | `mouthLipsTogetherDL` |
| `jawOpen` | `mouthLipsTogetherDR` |

Names are the short form of the `CTRL_expressions_*` channels. `MHA_LIMIT_DRIVERS` exports the same table resolved to frame indices, as entries of `{ source, target, sourceIdx, targetIdx }`.

## Prerequisites

- Lip sync enabled with `blendshapeConfig.format` set to `'mha'`, and frames read from `client.blendshapeQueue`. See [Drive facial animation with blendshapes](README.md).
- A character whose morph targets are named after the `CTRL_expressions_*` channels. See [Blendshape channel order reference](../vanilla-typescript/mappings-reference.md).

## Apply the couplings to a frame

When you already write frames to the morphs yourself, call `applyMhaLimits` on each frame first. It changes the frame in place and does nothing to a frame shorter than 251 values.

The stream sends `noseWrinkleUpperL` and `noseWrinkleUpperR` at exactly 1.0 on every frame of a reply, which reads as a frozen sneer. `applyMhaLimits` and the lipsync processor treat a value of 0.999 or more on those two channels as unset, so the coupling derives them from `noseWrinkle`. If you write raw frames to the morphs without these helpers, clear those two channels yourself.

```ts
import { applyMhaLimits } from '@convai/web-sdk/lipsync-helpers';

function applyMhaFrame(frame: Float32Array) {
  const shaped = new Float32Array(frame);
  applyMhaLimits(shaped);
  applyFrame(shaped);
}
```

Copy the frame before changing it, as above, so the values held in the queue stay untouched.

## Use the lipsync processor

`createLipsyncProcessor('mha')` wraps the whole per-frame pipeline: mouth symmetry, then the couplings, then per-channel gains, then a fade envelope, then the write to the morph targets.

```ts
import { createLipsyncProcessor } from '@convai/web-sdk/lipsync-helpers';

const lipsync = createLipsyncProcessor('mha', { skipEyeChannels: true });
const bindings = lipsync.bindAll(gltf.scene);

// Each render tick: pass the frame to play, or null while the character is silent.
lipsync.tick(frameOrNull, deltaSeconds, bindings);
```

The processor returns these members:

| Member | What it does |
|---|---|
| `process(frame, deltaSeconds)` | Shapes a frame and returns the values to write this tick, or `null` once the envelope has settled after silence. The returned array is reused; copy it to keep it. |
| `bindMesh(mesh)` | Resolves one mesh's morph slots and returns a binding, or `null` when no channel matches. |
| `bindAll(root)` | Traverses a scene and binds every mesh with matching morph targets. |
| `apply(output, bindings)` | Writes a processed frame to the bindings. Does nothing for `null`. |
| `tick(frame, deltaSeconds, bindings)` | `process` and `apply` in one call. |
| `profile` | The format profile in use. |

`bindMesh` and `bindAll` also repair a known export problem in place: a name with the underscore missing after the prefix, such as `CTRL_expressionsjawOpen`, is renamed to `CTRL_expressions_jawOpen` in the mesh's `morphTargetDictionary`.

The options and their defaults:

| Option | Default | Effect |
|---|---|---|
| `symmetrizeMouth` | `true` | Averages every left and right mouth and jaw pair. |
| `applyLimits` | `true` | Applies the 11 couplings above. |
| `useRecommendedGains` | `true` | Starts from the recommended gain table below. |
| `gainOverrides` | `{}` | Per-channel gains by short name, for example `{ jawOpen: 0.8 }`. |
| `skipEyeChannels` | `false` | Leaves the eye channels untouched. |
| `envelope` | `{ attack: 0.09, release: 0.18 }` | Fade-in and fade-out time constants in seconds. `false` disables the envelope. |

`createLipsyncProcessor` supports the `mha` format only. Any other format name throws an error that lists the available formats. To use another format, pass your own `LipsyncFormatProfile` in place of the format name.

{% hint style="info" %}
`getFrameWithAlpha` already fades the first and last 10 frames of a turn. When frames go through the processor's envelope, read them with `getFrame` instead so the fade is not applied twice.
{% endhint %}

## Recommended gains

With `useRecommendedGains` on, these channels are scaled. Every other channel keeps a gain of `1`.

| Channel | Gain |
|---|---|
| `jawOpen` | `0.72` |
| `jawOpenExtreme` | `0.42` |
| `jawLeft`, `jawRight`, `mouthLeft`, `mouthRight` | `0` |
| `mouthUpperLipRaiseL`, `mouthUpperLipRaiseR` | `0.6` |
| `mouthLowerLipDepressL`, `mouthLowerLipDepressR` | `0.45` |
| `mouthLipsTogetherUL`, `mouthLipsTogetherUR`, `mouthLipsTogetherDL`, `mouthLipsTogetherDR` | `0.8` |
| `mouthFunnelUL`, `mouthFunnelUR`, `mouthFunnelDL`, `mouthFunnelDR` | `1.15` |
| `mouthLipsPurseUL`, `mouthLipsPurseUR`, `mouthLipsPurseDL`, `mouthLipsPurseDR` | `1.15` |

The table is exported as `MHA_RECOMMENDED_GAINS`. `createMhaGainMask(overrides)` returns it as a 251-value `Float32Array` in frame order, with your overrides applied.

## Leave the eyes to procedural animation

When your application blinks or moves the eyes itself, two writers on the same channels flicker. Set `skipEyeChannels: true`, or skip the indices in `MHA_EYE_CHANNEL_INDICES` when you write frames yourself. They cover these channels: `eyeBlinkL`, `eyeBlinkR`, `eyeLookUpL`, `eyeLookUpR`, `eyeLookDownL`, `eyeLookDownR`, `eyeLookLeftL`, `eyeLookLeftR`, `eyeLookRightL`, `eyeLookRightR`, `eyeRelaxL`, `eyeRelaxR`, `eyeLowerLidUpL`, and `eyeLowerLidUpR`.

## Use the helpers one at a time

The processor is built from helpers you can also call on your own:

| Helper | Effect |
|---|---|
| `applyMhaLimits(frame)` | Applies the couplings in place. |
| `symmetrizeMhaMouth(frame)` | Averages every left and right mouth and jaw pair in place. |
| `createMhaGainMask(overrides)` | Returns the per-channel gains in frame order. |
| `mhaChannelIndex(shortName)` | Returns the frame index of a short channel name, or `undefined`. |

## Verify the result

Play a reply and watch the mouth on open vowels.

{% hint style="success" %}
The lips stay close to the teeth while the jaw opens, the teeth show only on wide vowels, and both corners of the mouth move together.
{% endhint %}

## Next steps

{% content-ref url="README.md" %}
[Drive facial animation with blendshapes](README.md)
{% endcontent-ref %}

{% content-ref url="../vanilla-typescript/mappings-reference.md" %}
[Blendshape channel order reference](../vanilla-typescript/mappings-reference.md)
{% endcontent-ref %}

{% content-ref url="../react/real-time-lipsync.md" %}
[Add lip sync in React](../react/real-time-lipsync.md)
{% endcontent-ref %}
