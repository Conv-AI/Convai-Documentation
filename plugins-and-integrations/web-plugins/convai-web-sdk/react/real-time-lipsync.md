---
title: Add lip sync in React
description: Drive the face of a 3D character in a React Three Fiber scene from the blendshape frames Convai streams with the character's voice.
last_reviewed: "1.9.1"
---

Animate a character's face in a `@react-three/fiber` scene from the blendshape stream that the Convai Web SDK buffers alongside the character's voice. Use this page when you already render a character model with morph targets and want its mouth to follow its speech.

## Prerequisites

- A React app using the Convai Web SDK. See [Get started with React](README.md).
- `three` and `@react-three/fiber` installed, and a glTF character whose mesh has morph targets.
- Morph targets named after the stream's channels, or a mapping to them. The channel names are listed in the [Blendshape channel order reference](../vanilla-typescript/mappings-reference.md).

## Enable the blendshape stream

Set `enableLipsync: true` and choose the frame format with `blendshapeConfig.format`. `"mha"` sends 251 MetaHuman channels per frame and is the default; `"arkit"` sends 61 ARKit channels.

```tsx
const client = useConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableLipsync: true,
  blendshapeConfig: { format: 'arkit' },
});
```

Frames arrive in `client.blendshapeQueue`. Convai sends no frames unless `enableLipsync` is `true`.

## Bind the morph targets

Resolve, once per mesh, which morph target each frame channel writes to. `ARKIT_ORDER_61` and `METAHUMAN_ORDER_251` list the channel names in frame order.

{% code title="src/lipsync.ts" %}
```ts
import type { Mesh } from 'three';
import { ARKIT_ORDER_61 } from '@convai/web-sdk/lipsync-helpers';

export function bindMorphs(mesh: Mesh, channels: readonly string[] = ARKIT_ORDER_61) {
  const slots = new Int32Array(channels.length).fill(-1);
  channels.forEach((name, i) => {
    const slot = mesh.morphTargetDictionary?.[name];
    if (slot !== undefined) slots[i] = slot;
  });
  return slots;
}

export function applyFrame(mesh: Mesh, slots: Int32Array, frame: Float32Array) {
  const influences = mesh.morphTargetInfluences;
  if (!influences) return;
  for (let i = 0; i < slots.length; i++) {
    if (slots[i] >= 0) influences[slots[i]] = frame[i] ?? 0;
  }
}
```
{% endcode %}

If your morph targets use other names, pass a mapper as `blendshapeConfig.customMapper`, or build the slot table from your own name list. See [Drive facial animation with blendshapes](../lipsync-and-blendshape/README.md).

## Play frames in the render loop

Consume frames from the queue at its playback rate while the character speaks, and drain the remaining frames after it stops. `getPlaybackFps()` returns the frame rate of the current turn, and `getFrameWithAlpha()` fades the first and last 10 frames so the mouth does not snap open or freeze.

{% code title="src/Face.tsx" %}
```tsx
import { useEffect, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import type { Mesh } from 'three';
import type { BlendshapeQueue } from '@convai/web-sdk/core';
import { applyFrame, bindMorphs } from './lipsync';

export function Face({ mesh, queue }: { mesh: Mesh; queue: BlendshapeQueue }) {
  const slots = useRef<Int32Array | null>(null);
  const elapsed = useRef(0);

  useEffect(() => {
    slots.current = bindMorphs(mesh);
  }, [mesh]);

  useFrame((_, delta) => {
    if (!slots.current) return;

    // An interruption: return the face to neutral at once.
    if (queue.consumeNormalizationSignal()) {
      applyFrame(mesh, slots.current, new Float32Array(slots.current.length));
    }

    const playing =
      queue.isBotSpeaking() || (queue.hasReceivedEndSignal() && queue.hasFrames());

    if (!playing) {
      elapsed.current = 0;
      if (queue.isConversationEnded()) queue.reset();
      return;
    }

    elapsed.current += delta;
    const frameTime = 1 / queue.getPlaybackFps();
    let frame: Float32Array | null = null;

    while (elapsed.current >= frameTime && queue.hasFrames()) {
      frame = queue.getFrameWithAlpha(0);
      queue.consumeFrames(1);
      elapsed.current -= frameTime;
    }

    if (frame) applyFrame(mesh, slots.current, frame);
  });

  return null;
}
```
{% endcode %}

Render `<Face mesh={headMesh} queue={client.blendshapeQueue} />` inside your `<Canvas>`, where `headMesh` is the mesh that carries the face morph targets.

{% hint style="warning" %}
For `format: 'mha'` on a glTF character, apply the MetaHuman limit drivers to every frame before writing it, or the lips separate on every jaw opening. See [Apply MetaHuman limit drivers](../lipsync-and-blendshape/metahuman-limit-drivers-required-for-mha.md).
{% endhint %}

## Verify lip sync

Connect, play the character's audio through `ConvaiWidget` or `AudioRenderer`, and send a message. While the character answers, `client.blendshapeQueue.getDebugInfo()` reports a growing `framesConsumed`.

{% hint style="success" %}
The mouth opens and closes in time with the character's voice and returns to rest after the reply ends.
{% endhint %}

## Troubleshooting

### The face does not move

**Symptom:** The character speaks, but `getDebugInfo().frameCount` stays at `0`.

**Cause:** `enableLipsync` is not `true` in the config the client connected with.

**Fix:** Add `enableLipsync: true`, then disconnect and connect again so the new config is sent.

**Verify:** `frameCount` rises while the character speaks.

### Only some morphs move

**Symptom:** Frames are consumed, but parts of the face stay still.

**Cause:** Morph target names on the mesh do not match the channel names of the selected format.

**Fix:** Compare `mesh.morphTargetDictionary` with the [Blendshape channel order reference](../vanilla-typescript/mappings-reference.md) and map the differences.

**Verify:** The slot table returned by `bindMorphs` has no `-1` entry for the channels you expect.

## Next steps

{% content-ref url="../lipsync-and-blendshape/README.md" %}
[Drive facial animation with blendshapes](../lipsync-and-blendshape/README.md)
{% endcontent-ref %}

{% content-ref url="../lipsync-and-blendshape/metahuman-limit-drivers-required-for-mha.md" %}
[Apply MetaHuman limit drivers](../lipsync-and-blendshape/metahuman-limit-drivers-required-for-mha.md)
{% endcontent-ref %}

{% content-ref url="../vanilla-typescript/mappings-reference.md" %}
[Blendshape channel order reference](../vanilla-typescript/mappings-reference.md)
{% endcontent-ref %}
