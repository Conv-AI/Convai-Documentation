---
title: Drive facial animation with blendshapes
description: Stream blendshape frames alongside a character's voice and apply them to the morph targets of a 3D face so its mouth moves in time with speech.
last_reviewed: "2.0.1"
icon: head-side-speak
---

Turn on lip sync so Convai streams facial blendshape frames with the character's audio, then play those frames onto the morph targets of a 3D model. Use this page when you render your own character with three.js or another WebGL engine. At the end, the character's mouth moves in time with its voice and settles back to neutral when it stops talking.

## Prerequisites

- The Convai Web SDK installed, with a client that connects. See [Web SDK quickstart](../quickstart.md).
- A 3D model whose face is driven by morph targets, loaded in your renderer.
- The model's morph target names, so you can match them to a stream format.

## Enable lip sync

Set `enableLipsync` and choose the stream format in `blendshapeConfig`. The same options apply to `new ConvaiClient(...)` from `@convai/web-sdk/core` and to `useConvaiClient(...)` from `@convai/web-sdk/react`.

```ts
import { ConvaiClient } from '@convai/web-sdk/core';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableLipsync: true,
  blendshapeConfig: {
    format: 'mha', // or 'arkit'
  },
});
```

When `enableLipsync` is `true`, the SDK asks Convai for blendshapes in chunks of 10 frames and buffers them in `client.blendshapeQueue`. When it is `false` or omitted, no blendshape frames are sent.

The `format` decides the length and order of every frame:

| `format` | Frame length | Channel names |
|---|---|---|
| `"mha"` (default) | 251 | MetaHuman controls, for example `CTRL_expressions_jawOpen` |
| `"arkit"` | 61 | 52 ARKit blendshapes, for example `JawOpen`, then three head and six eye rotation values |

The full channel order for both formats is in [Blendshape channel order reference](../vanilla-typescript/mappings-reference.md).

## Tune delivery

`blendshapeConfig` takes three delivery options. Leave them at their defaults unless you have a measured reason to change them.

| Option | Default | Effect |
|---|---|---|
| `deliver_chunks_ahead` | `true` when `enableLipsync` is on | Convai sends indexed chunks ahead of the audio, so the queue holds a buffer before playback starts. Set `false` to fall back to the legacy paced delivery path. |
| `output_fps` | `60` | Frame rate of ahead-delivered chunks. Ignored when `deliver_chunks_ahead` is `false`. |
| `frames_buffer_duration` | `0.1` | Seconds of blendshapes Convai accumulates before releasing them with the audio. |

The queue plays frames at the frame rate carried in the chunk metadata, or 60 frames per second when a chunk carries none. Read it with `client.blendshapeQueue.getPlaybackFps()`.

## Play frames from the queue

Run one loop on `requestAnimationFrame`. Each tick, advance a time accumulator, take the frames that are due, write the newest one to the face, and remove them from the queue.

```ts
let lastTime = 0;
let carryMs = 0;

function tick(now: number) {
  const queue = client.blendshapeQueue;

  // An interruption stops the audio: return the face to neutral at once.
  if (queue.consumeNormalizationSignal()) {
    applyFrame(new Float32Array(frameLength));
    carryMs = 0;
  }

  const playing =
    queue.isBotSpeaking() || (queue.hasReceivedEndSignal() && queue.hasFrames());

  if (playing && queue.hasFrames()) {
    carryMs += lastTime ? now - lastTime : 0;
    const frameMs = 1000 / queue.getPlaybackFps();
    const due = Math.floor(carryMs / frameMs);
    if (due > 0) {
      const count = Math.min(due, queue.length);
      // Read before consuming: the fade depends on how many frames were played.
      const frame = queue.getFrameWithAlpha(count - 1);
      if (frame) applyFrame(frame);
      queue.consumeFrames(count);
      carryMs -= due * frameMs;
    }
  } else {
    carryMs = 0;
  }

  // The turn is over and every expected frame has played.
  if (queue.isConversationEnded()) {
    queue.reset();
  }

  lastTime = now;
  requestAnimationFrame(tick);
}

requestAnimationFrame(tick);
```

`frameLength` is 251 for `mha` and 61 for `arkit`. `getFrameWithAlpha` fades the first 10 frames of a turn in and the last 10 frames out, so the mouth neither pops open nor freezes mid-shape. `getFrame` returns the same frame without the fade.

{% hint style="warning" %}
Do not combine `getFrameAtTime` with `consumeFrames`. `getFrameAtTime` indexes from the front of the queue by elapsed time, and `consumeFrames` moves the front forward, so using both advances playback twice and the mouth runs ahead of the voice.
{% endhint %}

Every `BlendshapeQueue` method is listed in [ConvaiClient reference](../vanilla-typescript/convaiclient-core-api.md).

## Apply frames to morph targets

When the model's morph targets use the stream's channel names, build a slot table once after the model loads, then write each frame through it. This needs no mapper.

```ts
import { METAHUMAN_ORDER_251 } from '@convai/web-sdk/lipsync-helpers';
import type { Mesh } from 'three';

function bindFace(mesh: Mesh) {
  const slots = new Int32Array(METAHUMAN_ORDER_251.length).fill(-1);
  METAHUMAN_ORDER_251.forEach((name, i) => {
    const slot = mesh.morphTargetDictionary?.[name];
    if (slot !== undefined) slots[i] = slot;
  });

  return (frame: Float32Array) => {
    const influences = mesh.morphTargetInfluences;
    if (!influences) return;
    for (let i = 0; i < slots.length; i++) {
      if (slots[i] >= 0) influences[slots[i]] = frame[i] ?? 0;
    }
  };
}

const applyFrame = bindFace(faceMesh);
```

For `arkit`, use `ARKIT_ORDER_61` in place of `METAHUMAN_ORDER_251`. Both are exported from `@convai/web-sdk/lipsync-helpers`.

For an `mha` character, also apply the MetaHuman rig couplings, or the lips part every time the jaw opens. `createLipsyncProcessor('mha')` binds the meshes, repairs known name mangling, and applies the couplings, gains, and a fade envelope in one call. See [Apply MetaHuman limit drivers](metahuman-limit-drivers-required-for-mha.md).

## Remap channels with a custom mapper

When the morph targets use different names, pass a mapper. The SDK runs it on every frame as the frame enters the queue.

```ts
import { createARKitNameMapper } from '@convai/web-sdk/lipsync-helpers';

const mapper = createARKitNameMapper({
  jawOpen: ['Jaw_Open'],
  eyeBlinkLeft: ['Eye_Blink_L'],
  eyeBlinkRight: ['Eye_Blink_R'],
  mouthSmileLeft: ['Mouth_Smile'],
  mouthSmileRight: ['Mouth_Smile'], // averaged with mouthSmileLeft
});

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableLipsync: true,
  blendshapeConfig: { format: 'arkit', customMapper: mapper },
});
```

`createMetaHumanNameMapper` does the same for `mha`, keyed by the full `CTRL_expressions_*` names or the short form (`jawOpen`). Source names that do not exist in the format are skipped with a console warning. When several sources map to one target, their values are averaged. Only the targets you map are output.

The second argument selects the output shape. Both give every frame its own values, and both survive the fade in `getFrameWithAlpha`:

| Output | Each queued frame | How to read it |
|---|---|---|
| `'object'` (default) | A `Float32Array` of the target values, in target order, with the names attached | `getBlendshapeObject(frame)` for a name-to-value object |
| `'optimized'` | `{ names, values, nameToIndex, length }` | `frame.values[frame.nameToIndex.get('Jaw_Open')]`, or `getBlendshapeObject(frame)` |

To change the mapper after connecting, call `client.blendshapeQueue.setMapper(fn)`. `clearMapper()` returns to raw frames, and `hasMapper()` reports whether one is set.

## Verify lip sync

Connect, send a message, and watch the face while the character answers.

{% hint style="success" %}
The mouth starts moving when the character's voice starts, follows its syllables, and returns to neutral within a fraction of a second after the voice stops.
{% endhint %}

If the face never moves, confirm that `enableLipsync` is `true` and that `client.blendshapeQueue.length` rises while the character speaks. If frames arrive but the face stays still, the morph target names do not match the format: log `mesh.morphTargetDictionary` and compare it with the channel order reference.

## Next steps

{% content-ref url="metahuman-limit-drivers-required-for-mha.md" %}
[Apply MetaHuman limit drivers](metahuman-limit-drivers-required-for-mha.md)
{% endcontent-ref %}

{% content-ref url="../react/real-time-lipsync.md" %}
[Add lip sync in React](../react/real-time-lipsync.md)
{% endcontent-ref %}

{% content-ref url="../vanilla-typescript/real-time-lipsync.md" %}
[Add lip sync in vanilla TypeScript](../vanilla-typescript/real-time-lipsync.md)
{% endcontent-ref %}

{% content-ref url="../vanilla-typescript/mappings-reference.md" %}
[Blendshape channel order reference](../vanilla-typescript/mappings-reference.md)
{% endcontent-ref %}
