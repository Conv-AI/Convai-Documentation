---
title: Add lip sync in vanilla TypeScript
description: Play the facial animation frames that the Convai Web SDK streams with a character's voice on a 3D model in plain TypeScript, without a UI framework.
last_reviewed: "2.0.2"
---

Drive a three.js character's morph targets from the blendshape frames that Convai streams alongside the character's voice. Use this page when you render the character yourself in framework-free TypeScript. At the end, the character's mouth moves in time with its speech and settles to neutral when it stops or is interrupted.

## Prerequisites

- A connected `ConvaiClient`. See [Get started with vanilla TypeScript](README.md).
- A three.js mesh whose morph targets are named after the channels of the format you request. See [Blendshape channel order reference](mappings-reference.md).

## Enable lip sync

Set `enableLipsync: true` and choose the frame format in `blendshapeConfig.format`: `'mha'` (251 MetaHuman channels, the default) or `'arkit'` (61 values).

```typescript
import { ConvaiClient } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  enableLipsync: true,
  blendshapeConfig: { format: 'arkit' },
});

await client.connect();
```

Without `enableLipsync: true`, Convai sends no frames and the queue stays empty. Frames arrive in chunks and the SDK buffers them in `client.blendshapeQueue`.

## Bind the morph targets

Build a lookup from frame index to morph target slot once, after the model loads. The frame order is `ARKIT_ORDER_61` for `'arkit'` and `METAHUMAN_ORDER_251` for `'mha'`.

```typescript
import * as THREE from 'three';
import { ARKIT_ORDER_61 } from '@convai/web-sdk/lipsync-helpers';

function bindMorphs(mesh: THREE.Mesh, channelNames: readonly string[]): Int32Array {
  const dictionary = mesh.morphTargetDictionary ?? {};
  const slots = new Int32Array(channelNames.length).fill(-1);
  channelNames.forEach((name, i) => {
    // ARKit channels are PascalCase; many exports name the morphs in camelCase.
    const camel = name.charAt(0).toLowerCase() + name.slice(1);
    const slot = dictionary[name] ?? dictionary[camel];
    if (slot !== undefined) slots[i] = slot;
  });
  return slots;
}

const slots = bindMorphs(faceMesh, ARKIT_ORDER_61);

function applyFrame(frame: Float32Array) {
  const influences = faceMesh.morphTargetInfluences!;
  for (let i = 0; i < slots.length; i++) {
    if (slots[i] >= 0) influences[slots[i]] = frame[i];
  }
}

function clearFace() {
  const influences = faceMesh.morphTargetInfluences!;
  for (let i = 0; i < slots.length; i++) {
    if (slots[i] >= 0) influences[slots[i]] = 0;
  }
}
```

The last nine `'arkit'` values are head and eye rotations, not morph targets. They find no slot and are skipped.

## Play the frames

Run a `requestAnimationFrame` loop that advances a clock while the character speaks, plays the frame for that time, and consumes the frames it has passed. Read the frame with `getFrameWithAlpha`, which fades the face in over the first 10 frames of a turn and out over the last 10.

```typescript
const queue = client.blendshapeQueue;

let playing = false;
let lastTime = 0;
let elapsedMs = 0;
let lastFrameIndex = -1;

function tick(now: number) {
  // Interruption or a cancelled response: return the face to neutral.
  if (queue.consumeNormalizationSignal()) {
    clearFace();
    playing = false;
  }

  const speaking = queue.isBotSpeaking();
  const draining = queue.hasReceivedEndSignal() && queue.hasFrames();

  if (speaking || draining) {
    if (!playing) {
      playing = true;
      lastTime = now;
      elapsedMs = 0;
      lastFrameIndex = -1;
    }
    elapsedMs += now - lastTime;
    lastTime = now;

    const frameDurationMs = 1000 / queue.getPlaybackFps();
    const targetIndex = Math.floor(elapsedMs / frameDurationMs);
    const advance = Math.min(targetIndex - lastFrameIndex, queue.length);

    if (advance > 0) {
      const frame = queue.getFrameWithAlpha(advance - 1);
      if (frame) applyFrame(frame);
      queue.consumeFrames(advance);
      lastFrameIndex = targetIndex;
    }
  }

  // The turn is over and every frame is played: reset for the next turn.
  if (queue.isConversationEnded()) {
    clearFace();
    queue.reset();
    playing = false;
  }

  requestAnimationFrame(tick);
}

requestAnimationFrame(tick);
```

The loop never pairs `getFrameAtTime()` with `consumeFrames()`. `getFrameAtTime()` indexes from the front of the queue, so consuming frames after it advances playback twice. Use one of the two approaches, not both.

The client itself starts each turn on the queue when you send a message, fire a trigger, or the user starts speaking, and clears it when you call `sendInterruptMessage()`. Your loop only reads and consumes.

## Remap channels with a mapper

To translate frames into your rig's own layout as they enter the queue, set a mapper. A mapper receives each raw frame and returns a `Float32Array`. Pass it as `blendshapeConfig.customMapper`, or set it on a live queue:

```typescript
client.blendshapeQueue.setMapper((input) => {
  const out = new Float32Array(52); // your rig's channel count
  out[0] = input[17]; // ARKit JawOpen into your rig's slot 0
  return out;
});

client.blendshapeQueue.clearMapper(); // back to raw frames
```

With a mapper set, frames no longer follow `ARKIT_ORDER_61` or `METAHUMAN_ORDER_251`, so bind your slots to the mapper's output layout instead.

## Verify lip sync

Send a message and listen to the reply. The mouth moves while the character speaks and returns to neutral after the last word. Call `sendInterruptMessage()` mid-reply: the face settles at once instead of freezing on the last shape. For a snapshot of the queue while debugging, log `queue.getDebugInfo()`.

## Next steps

{% content-ref url="../lipsync-and-blendshape/README.md" %}
[Drive facial animation with blendshapes](../lipsync-and-blendshape/README.md)
{% endcontent-ref %}

{% content-ref url="../lipsync-and-blendshape/metahuman-limit-drivers-required-for-mha.md" %}
[Apply MetaHuman limit drivers](../lipsync-and-blendshape/metahuman-limit-drivers-required-for-mha.md)
{% endcontent-ref %}

{% content-ref url="convaiclient-core-api.md" %}
[ConvaiClient reference](convaiclient-core-api.md)
{% endcontent-ref %}
