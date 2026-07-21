---
description: >-
  Drive real-time facial animation on 3D characters using blendshape data
  streamed alongside the bot's audio.
icon: head-side-speak
---

# Lipsync & Blendshape

### How it works

1. Enable lipsync in config — the server starts generating blendshape frames alongside TTS audio.
2. Frames arrive in chunks of 10 and are buffered in `client.blendshapeQueue`.
3. Your render loop reads frames from the queue at 60 fps, synchronized to when the bot is speaking.
4. When the bot stops speaking, the queue drains and signals conversation end.

***

### Enable lipsync

```ts
const client = useConvaiClient({
  apiKey: '...',
  characterId: '...',
  enableLipsync: true,
  blendshapeConfig: {
    format: 'arkit', // or 'mha' (MetaHuman 251, default)
  },
});
```

Formats (server-verified — an unknown string rejects the connect with the valid list):

| `format`          | Frame dim | Channel naming             | Notes                                                                                                            |
| ----------------- | --------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `"mha"` (default) | 251       | `CTRL_expressions_*`       | Unreal MetaHuman Animation; MetaHuman-Lite characters (103 morphs) consume their named subset of the same stream |
| `"arkit"`         | 61        | ARKit names (`JawOpen`, …) | Apple ARKit standard                                                                                             |
| `"cc4_extended"`  | 170       | CC4 ExpressionPlus         | Reallusion Character Creator 4                                                                                   |
| `"cc5_hd"`        | —         | —                          | Accepted by the server but currently delivers **no frames**                                                      |
| `"visemes"`       | 15        | OVR viseme set             | `sil, PP, FF, TH, DD, kk, CH, SS, nn, RR, aa, E, ih, oh, ou`                                                     |

***

### Reading frames in the render loop

Access `client.blendshapeQueue` from your animation loop. The queue is time-indexed at 60 fps.

```ts
// Three.js / requestAnimationFrame example
let lipsyncStartTime: number | null = null;

function animate() {
  requestAnimationFrame(animate);

  const queue = client.blendshapeQueue;

  if (queue.isBotSpeaking()) {
    // Start clock when bot begins speaking
    if (lipsyncStartTime === null) {
      lipsyncStartTime = performance.now();
    }

    const elapsed = (performance.now() - lipsyncStartTime) / 1000;
    const result = queue.getFrameAtTime(elapsed);

    if (result) {
      applyBlendshapes(morphTargets, result.frame);
      queue.consumeFrames(result.frameIndex + 1);
    }
  } else {
    lipsyncStartTime = null;
  }

  renderer.render(scene, camera);
}
```

#### `getFrameAtTime(elapsedSeconds)`

Returns the frame closest to the given elapsed time (assuming 60 fps), or `null` if the queue is empty.

```ts
const result = queue.getFrameAtTime(elapsed);
// result.frame: Float32Array of blendshape values
// result.frameIndex: index in the queue
```

#### `getFrameWithAlpha(index)`

Same as `getFrame` but applies fade-in (first 10 frames) and fade-out (last 10 frames or on interrupt) automatically:

```ts
const frame = queue.getFrameWithAlpha(index);
// Smoothly fades in at start and out at end
```

***

### Applying blendshapes to a Three.js mesh

```ts
import { ARKIT_ORDER_61 } from '@convai/web-sdk/lipsync-helpers';

function applyBlendshapes(mesh: THREE.SkinnedMesh, frame: Float32Array) {
  const morphInfluences = mesh.morphTargetInfluences;
  if (!morphInfluences) return;

  ARKIT_ORDER_61.forEach((name, i) => {
    const morphIndex = mesh.morphTargetDictionary?.[name];
    if (morphIndex !== undefined) {
      morphInfluences[morphIndex] = frame[i];
    }
  });
}
```

`ARKIT_ORDER_61` is an ordered array of the 61 ARKit blendshape names matching the frame indices.

For MetaHuman (`"mha"` format), import `METAHUMAN_ORDER_251` instead.

***

### Custom mappers

Use a custom mapper to transform incoming blendshapes to match your character's morph target names.

#### ARKit name mapper

```ts
import { createARKitNameMapper } from '@convai/web-sdk/lipsync-helpers';

const mapper = createARKitNameMapper({
  // SDK name → your character's morph target name(s)
  'jawOpen': ['Jaw_Open', 'Mouth_Open'],
  'eyeBlinkLeft': ['Eye_Blink_L'],
  'eyeBlinkRight': ['Eye_Blink_R'],
  'mouthSmileLeft': ['Smile_L'],
  'mouthSmileRight': ['Smile_R'],
}, 'optimized'); // 'optimized' extracts only mapped targets; omit for all 61

const client = useConvaiClient({
  apiKey: '...',
  characterId: '...',
  enableLipsync: true,
  blendshapeConfig: {
    format: 'arkit',
    customMapper: mapper,
  },
});
```

The mapper is applied to every frame as it enters the queue.

#### Direct name-mapped characters (no mapper needed)

If your character's morph targets are named **exactly** like the stream's channels, skip mappers entirely and write frames by name:

* `format: 'mha'` channels are named `CTRL_expressions_jawOpen`, `CTRL_expressions_eyeBlinkL`, … — matching MetaHuman-style exports.
* `format: 'arkit'` channels use ARKit names (`JawOpen`, `EyeBlinkLeft`, …).

Build an index table once per mesh, then apply frames with zero per-frame lookups:

```ts
import { METAHUMAN_ORDER_251 } from '@convai/web-sdk/lipsync-helpers';

// Once, after the model loads:
const slots = new Int32Array(METAHUMAN_ORDER_251.length).fill(-1);
METAHUMAN_ORDER_251.forEach((name, i) => {
  const slot = mesh.morphTargetDictionary?.[name];
  if (slot !== undefined) slots[i] = slot;
});

// Per frame:
function applyFrame(frame: Float32Array) {
  const infl = mesh.morphTargetInfluences!;
  for (let i = 0; i < slots.length; i++) {
    if (slots[i] >= 0) infl[slots[i]] = frame[i];
  }
}
```

> Exports sometimes mangle names (e.g. a missing separator: `CTRL_expressionsjawOpen`). Normalize `morphTargetDictionary` keys at load rather than adjusting every consumer.

#### Set mapper after connect

```ts
client.blendshapeQueue.setMapper((frame) => {
  // frame: Float32Array of raw blendshape values
  const output = new Float32Array(52); // your character's morph count
  // ... remap indices ...
  return output;
});

// Remove mapper (passthrough)
client.blendshapeQueue.clearMapper();
```

***

### BlendshapeQueue API

`client.blendshapeQueue` is the live queue instance.

#### State checks

```ts
queue.isBotSpeaking()         // true while bot audio is playing
queue.isConversationActive()  // true from user message until turn-stats arrive
queue.isConversationEnded()   // true after turn ends and all frames consumed
queue.hasFrames()             // true when frames are waiting
queue.length                  // number of frames in queue
```

#### Frame access

```ts
queue.getFrameAtTime(elapsed) // { frame, frameIndex } | null — time-based lookup
queue.getFrame(index)         // Float32Array | null — direct index access
queue.getFrameWithAlpha(index) // Float32Array | null — with fade in/out applied
queue.getFrames()             // Float32Array[] — all frames
```

#### Consumption

```ts
queue.consumeFrames(count)    // remove N frames from the front
queue.getFramesConsumed()     // total frames consumed this turn
```

#### Turn stats

```ts
queue.getTurnStats()
// { fps, total_audio_bytes, total_audio_duration_ms, total_blendshapes, total_turn_duration_ms }

queue.getTimeLeftMs()         // estimated ms until queue is empty
queue.isAllFramesConsumed()   // true when framesConsumed >= total_blendshapes
```

#### Interruption

```ts
queue.consumeNormalizationSignal()
// Returns true (once) when the bot was interrupted — use to lerp morphs back to 0
```

#### Debug

```ts
console.log(queue.getDebugInfo());
// { frameCount, conversationActive, botSpeaking, conversationEnded,
//   interrupted, framesConsumed, turnStats, timeLeftMs }
```

***

### Making lipsync feel natural

Patterns proven on production characters — each one addresses a specific artifact you will otherwise see:

#### Fade the stream in and out

Raw frames hit the face at full strength on the first frame and freeze the last viseme when frames stop. Scale every stream-driven value by an eased envelope: bloom in over \~0.25 s at speech start, settle out over \~0.5 s after the last frame (keep the final frame and fade it to zero — don't drop it mid-shape).

```ts
// Per render frame:
const target = isSpeaking ? 1 : 0;
const tau = target > env ? 0.09 : 0.18; // fast attack, gentler release
env += (target - env) * (1 - Math.exp(-delta / tau));
// ...then apply: infl[slot] = frame[i] * env;
```

(`getFrameWithAlpha` does this automatically if you consume the queue directly; apply your own envelope when you buffer/apply frames yourself.)

#### Let procedural systems own their channels

If you run procedural blinking or camera-following gaze, the stream must **never write the eye channels** — two writers on different timers race each other into flicker (blinks never visibly close). Keep a skip mask of channel indices the stream leaves untouched, and let your blink/gaze code own them outright.

#### End-of-speech detection

Frames can stop arriving before any explicit end event. Treat \~300 ms without a new frame as end-of-speech and start your fade-out — the official end signal can then arrive late without a visible freeze.

#### Per-channel gains

Streams are tuned for a reference face; your character's shapes may read too strong. A per-channel gain table fixes this surgically — e.g. on one MetaHuman-style rig we ship `jawOpen × 0.7` and lateral jaw/mouth shifts × 0 (they read as lopsidedness), leaving everything else at 1.

#### Mouth symmetry

If the stream drives L/R mouth pairs unevenly (we've measured up to 1.5× side-to-side), average each sided pair (`…L`/`…R`) before applying — an open mouth reads far better symmetric.

#### Apply after your animation mixer

If body animation clips also touch the head, re-apply the current lipsync frame **after** the mixer updates each render frame so speech always wins on the face.

***

### Buffer tuning

The `frames_buffer_duration` option controls how many seconds of blendshapes the server accumulates before releasing them with the audio. Higher values increase lipsync accuracy at the cost of latency.

```ts
blendshapeConfig: {
  format: 'arkit',
  frames_buffer_duration: 0.2, // 200ms buffer (default: 0.1)
}
```

