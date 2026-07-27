# MetaHuman limit drivers — REQUIRED for \`mha\`

Unreal's MetaHuman rig applies built-in channel couplings that the stream is authored against. On a raw glTF character those couplings don't exist — most visibly, `jawOpen` must also drive the four `mouthLipsTogether*` channels so the lips stay in contact while the jaw moves. **Without this, every jaw opening fully separates the lips and bares the teeth** — the mouth flaps instead of speaking, and no amount of tuning fixes it.

Apply them to every frame before writing to the morphs:

```ts
import { applyMhaLimits } from '@convai/web-sdk/lipsync-helpers';

applyMhaLimits(frame); // in place: target = max(target, source) per coupling
```

`MHA_LIMIT_DRIVERS` exports the resolved coupling table if you need it raw (e.g. `jawOpen → jawOpenExtreme`, `jawOpen → mouthLipsTogetherUL/UR/DL/DR`, `eyeBlink → eyeLidPress`, and friends).

***

### Making lipsync feel natural & realistic

Raw stream playback reads robotic. Everything below is what separates a demo from a believable character, grouped by system. This guide is the distilled result of iterating a MetaHuman-style (`mha`) character against recorded close-up QA until open vowels, plosives, teeth, brows, head and eyes all read like footage of a person — every number here is the value that survived that process, with the failure it fixes. The stream-shaping patterns (§1) ship as a one-call processor; the procedural systems (§2–3) are implementation guides with reference code in `examples/react-three-fiber/src/hooks`.

#### 1. Stream shaping — the mouth (`mha`)

One call wraps the per-frame pipeline, in the right order:

```ts
import { createLipsyncProcessor } from '@convai/web-sdk/lipsync-helpers';

const lipsync = createLipsyncProcessor('mha', {
  skipEyeChannels: true,           // you run the blink/gaze in §2
  gainOverrides: { jawOpen: 0.72 } // per-character tuning, table below
});
const bindings = lipsync.bindAll(gltf.scene); // repairs names, maps morph slots

// per render tick:
lipsync.tick(frameOrNull, delta, bindings);
```

Internally: **symmetrize → limit couplings → gains → envelope → morphs.**

**1.1 Rig limit couplings (REQUIRED)**

See the section above — without `jawOpen → mouthLipsTogether*` every jaw opening bares the teeth. The processor applies them by default.

**1.2 Per-channel gains — the production table**

The stream is tuned for a reference face; on a real character the raw values over-open the jaw, drag the mouth sideways and retract the lips off the teeth. This table is the balance point between "mumbled / ventriloquist" (too little aperture) and "constant dental display" (too much), walked in both directions on camera:

| Channel                             | Gain     | Why                                                                                                |
| ----------------------------------- | -------- | -------------------------------------------------------------------------------------------------- |
| `jawOpen`                           | **0.72** | Conversational aperture. 0.6 read mumbled on open vowels; raw (1.0) bares the teeth.               |
| `jawOpenExtreme`                    | **0.42** | Same, for the extreme shape the limit driver feeds.                                                |
| `jawLeft/Right`, `mouthLeft/Right`  | **0**    | Lateral shifts only ever read as a lopsided mouth once you symmetrize (§1.3).                      |
| `mouthUpperLipRaiseL/R`             | **0.6**  | Raising the upper lip exposes the upper teeth; keep it a glimpse.                                  |
| `mouthLowerLipDepressL/R`           | **0.45** | In life the lower lip almost never drops below the lower incisors.                                 |
| `mouthLipsTogetherUL/UR/DL/DR`      | **0.8**  | Lips ride close to the teeth through normal speech; open vowels still show an upper-teeth glimpse. |
| `mouthFunnel*`, `mouthLipsPurse*`   | **1.15** | Rounding on /u/ /w/ is under-driven by the stream.                                                 |
| `mouthCornerPull*`, `mouthStretch*` | **1.0**  | Do NOT boost: amplified corner spread on /i/ /e/ (EE) reads as an extreme grimace.                 |

**1.3 Mouth symmetry**

Streams drive L/R pairs unevenly (measured up to 1.5×) which reads as a lopsided mouth — average every sided mouth/jaw pair each frame.

**1.4 Bloom & settle envelope**

The first frame must not pop the mouth open and the last must not freeze mid-viseme: a gain envelope blooms in over \~0.25 s at speech start (attack τ ≈ 0.09 s) and settles out over \~0.5 s after the last frame (release τ ≈ 0.18 s).

**1.5 Hard jaw cap**

Independent of the gain, clamp the _applied_ `jawOpen` at **0.55**. The gain scales everything; the cap kills only the rare peak excursions that read exaggerated on camera while leaving normal articulation untouched.

**1.6 Bilabial closure floor — why /p/ /b/ /m/ never seal on their own**

This one is structural, and no gain can fix it: the `mouthLipsTogether*` values come from `jawOpen` via the limit coupling — which is **near zero exactly when the jaw closes for a plosive**. So on "pumpkin" the lips stay visibly parted no matter how high you push the lips-together gain. Fix: drive the contact directly as the jaw closes during speech:

```ts
// bilabial: 1 when jaw (nearly) closed, fading out by jawRaw ≈ 0.18
const bilabial = 1 - clamp((jawRaw - 0.02) / 0.16, 0, 1);
if (bilabial > 0.45) {
  const seal = ((bilabial - 0.45) / 0.55) * 0.5 * envelope;
  lipsTogetherValue = Math.max(lipsTogetherValue, seal);
}
```

The **0.5 ceiling matters**: at 0.9 the plosives read as the lips colliding (a hard clamp); at 0.65 still over-pressed; 0.5 reads as lips _touching_. Measured seal at closures ≈ 0.5–0.6 is the target.

**1.7 Transient preservation**

Real speech has sharp attacks on hard consonants; heavy temporal smoothing melts them into mush. Use a light smoothing factor (**lerp ≈ 0.92** per frame at 60 fps, i.e. barely smoothing) — the envelope (§1.4) already guards the start/end, so per-frame smoothing doesn't need to be strong.

**1.8 Audio sync — give the mouth a visual lead**

Humans read lips slightly _ahead_ of the sound. If recordings show the mouth trailing the voice, play the frame \~**100 ms ahead** of the audio position (6 frames at 60 fps). Consume the queue with a dt-accumulator (1/60 s per frame) — never combine `getFrameAtTime()` with `consumeFrames()`, which double-advances and starves the mouth.

**1.9 Teeth & mouth shading — the other half of "too much teeth"**

Aperture and teeth exposure fight each other only if the mouth interior is lit like the face. A real mouth sits in shadow. On this stack the fix that finally allowed honest apertures was **material**, not animation:

* darken the enamel tint (\~0.4 grey-warm, from a 0.55 starting point);
* cut the teeth material's environment/IBL response (`envMapIntensity` ≈ 0.1) and specular (≈ 0.28);
* retract the upper/lower rows a few mm behind the lips and bake a gum-side + lateral lip shadow into the teeth shading if you can.

Result: open vowels show a _shadowed glimpse_ of the upper row — like footage — instead of a bright white band, and the lower teeth read hidden without choking articulation.

#### 2. Procedural facial life — the eyes

The stream's eye channels should be **owned by procedural systems** (set `skipEyeChannels: true`); two writers on different timers race each other into flicker.

**2.1 Blinking**

Humans blink every 2–6 s. Minimal recipe (\~10 lines): keep a countdown; when it fires, drive `eyeBlinkL/R` through a 0.2 s sine (close → open), then re-arm with `2 + random()*4` seconds. Add a resting lid droop (\~0.2) and occasional partial blinks. On camera, err toward MORE frequent (median gap \~2.8 s) — sparse blinks read as staring in video. Reference: `useBlink.ts`.

**2.2 Eye tracking (gaze)**

Eye contact with the camera is the strongest single realism cue:

1. Each frame, compute the direction from the character's eye position to the camera, in the head's local space.
2. Convert to normalized horizontal/vertical angles, clamped (±30° H, ±22° V) — eyes have limits before the head must turn.
3. Drive the **eye bones** if the rig has them, else the `eyeLook*` morphs (MetaHuman-style rigs rotate the eyeballs through morphs — scale by \~0.65, the shapes encode more rotation than 1.0 should apply).
4. Ease with a fast lerp (eyes are quick, \~0.2 factor) and let the LIDS follow the gaze slightly (eyeLook morphs double as lid-followers).
5. **While speaking, lock the gaze** — a speaker holds the listener's eyes. Ease saccade amplitude to zero during active speech…
6. …but not into a fixed stare: during **sustained energy dips** (the natural pauses between phrases — speech-energy below \~0.06 for a few hundred ms), let micro-saccades return at half amplitude. Full lock while words are flowing, subtle life in the gaps. Reference: `useEyeTracking.ts`.

**2.3 Micro-saccades**

Real eyes never hold still: every 0.6–2.6 s dart to a small random offset (mostly ≤ 30% of range, occasionally re-fixating dead-center) with a crisp ease (\~30/s), riding on top of the camera gaze. Governed by the speech gating in 2.2.

#### 3. Head & body

**3.1 Head tracking**

The head should orient toward the camera with the neck sharing the load:

1. Compute yaw/pitch from the head to the camera in character space. For the _range decision_, measure the facing from the **skeleton root** (a static node) — never from the animated spine: the spine breathes and sways a few degrees, and any threshold fed by it flips state with the sway.
2. **Hold at the limit, release only in the blind spot.** Don't disengage tracking at the ±90° edge — a viewer strafing near the boundary cycles the head through full engage/disengage swings (reads as the head banging). Clamp the target at the max turn while the viewer is anywhere visible, and fade to the clip pose only well behind the character (≈ max+20° … max+43°), where the face can't be seen anyway.
3. Distribute anatomically: the head alone takes only the first \~**25°** of yaw; the **neck carries the rest** (\~0.75 of the remainder). With a 60° head-only zone the head cranks to \~50° for a side viewer — a near-joint-limit pose where every correction reads as jerking.
4. Ease the target angles with **time-based** smoothing (`1 − exp(−rate·dt)`, rate ≈ 5/s) and cap the retarget velocity (\~80°/s). Per-frame lerp factors turn frame drops into visible stepping.
5. Blend with the animation by LOW-PASSING the clip's head pose first (τ ≈ 0.2 s) and keeping the camera-lock strength high (\~0.9 idle, \~0.95 speaking) — raw clip motion entering the blend is where head wobble comes from.
6. Add life on top: slow multi-sine drift (\~2°), occasional gaze shifts held 1.5–4 s eased time-based, and a slight roll "bank" into yaw turns. Reference: `useHeadTracking.ts`.

**3.2 Speech-energy coupling — the upper face talks too**

Compute a 0–1 **speech-energy envelope** from mouth activity (jaw + lip channel magnitudes, fast attack / slow release). Two systems consume it:

* **Brows/cheeks:** lift the brow-raise / cheek-raise channels with energy (coupling ≈ 0.9 into the emotion overlay's upper-face weights). A face whose brows never move while asking a question reads pasted-on.
* **Emphasis nods:** detect energy **onsets** — a fast envelope (τ ≈ 0.1 s) rising above its own slow average (τ ≈ 0.55 s). Pitch the head down a few degrees on the onset and release. Post-smooth the nod itself asymmetrically (dip τ ≈ 0.09 s, release τ ≈ 0.22 s) — driving the head straight off the onset signal tracks energy jitter and reads jerky. Sustained loudness must produce **no** nod (no constant bow); only stressed syllables mark.

**3.3 Emotion overlay**

Keep a low resting emotion (a subtle smile recipe) that **max-combines** with the speech frames rather than overwriting them, and damp its mouth-region channels while speaking so it never fights the visemes. Boost the smile floor briefly on social beats (a wave, a greeting). Reference: `useEmotion.ts`.

**3.4 Apply after the animation mixer**

If body clips also touch face/head, re-apply the current lipsync frame and tracking pose AFTER the mixer updates each frame, so speech always wins on the face.

**3.5 Breathing & idle micro-motion**

A ±0.7° additive chest/spine pitch at \~13 breaths/min (asymmetric: quicker inhale, longer exhale) keeps the body from reading frozen. Reference: `useBreathing.ts`. For walking characters, secondary physics (hair spring chains, acceleration-driven torso lean, stance-foot IK) compound the effect — see `useHairPhysics.ts`, `useLocomotionDynamics.ts` and `useFootLock.ts`.

#### 4. Timing & frame-pacing robustness

Realism survives only at a steady frame rate; most "glitches" people report are pacing artifacts:

* **End-of-speech detection:** treat \~300 ms without a new frame as end of speech and start the settle — the official end event can arrive late without a visible freeze.
* **Interruption:** `queue.consumeNormalizationSignal()` returns true (once) when the bot was interrupted — lerp morphs back to zero.
* **Clamp the animation-mixer step** (≤ 33 ms). A main-thread stall (UI re-render, TTS audio setup, GC) otherwise advances the whole rig by the stalled delta in one frame — a pose teleport your smoothing then visibly chases.
* **Divide velocities by real elapsed time**, never by a clamped dt — a stall frame otherwise inflates apparent velocity several-fold and spooks state machines (foot locks, gaze gates).
* **Every ease must be time-based** (`1 − exp(−dt/τ)`), never a per-frame constant, or long frames become visible steps.
* **No per-frame allocations** in the hot path (including debug logging) — the GC pauses land exactly where they're most visible.
* **Overlay UI must not repaint every frame.** A chat panel's animated visuals repainting at 60 fps forces the compositor to re-blend the panel over the WebGL canvas continuously and can halve the frame rate; throttle visualizers to 30 fps, stop painting when idle, and never drive per-frame SVG filters (drop-shadow blur) or React setState from an animation loop.

#### 5. Character preparation

* **Naming is the contract:** morphs must match the format's channel names exactly. Inspect your GLB in a glTF viewer before writing code.
* **Name mangling:** some exports drop separators (`CTRL_expressionsjawOpen`) — `bindAll`/`bindMesh` repair the dictionaries automatically; do the same if you bind by hand.
* **Lite vs Full rigs:** a MetaHuman-Lite model (103 morphs) consumes its named subset of the 251 stream — it works, but lacks the brow/cheek/eye detail channels. Use the full rig for hero characters.
* **No jaw/tongue bones on morph rigs:** MetaHuman-style glTF exports are usually fully morph-driven — jaw motion lives entirely in `jawOpen`/`jawOpenExtreme`. Don't budget for a jaw-bone driver that has nothing to drive.
* **Mouth materials ship too bright:** exports typically leave teeth under full IBL. Budget a material pass (§1.9) alongside the animation tuning — half of "the teeth look wrong" is shading.

***

### Buffer tuning

The `frames_buffer_duration` option controls how many seconds of blendshapes the server accumulates before releasing them with the audio. Higher values increase lipsync accuracy at the cost of latency.

```ts
blendshapeConfig: {
  format: 'arkit',
  frames_buffer_duration: 0.2, // 200ms buffer (default: 0.1)
}
```

#### Ahead-delivery (send-ahead contract)

With `deliver_chunks_ahead: true` the server ships **indexed** NeuroSync chunks _before_ audio playback, so the client holds a real visual buffer (\~2 s ahead in practice) instead of racing the voice. The SDK uses the chunk metadata (`fps`, `start_frame_index`, `response_id`, `neurosync_turn_id`, `epoch`) to order frames and drop buffered visuals for interrupted turns — use `client.blendshapeQueue` and the SDK-style player path so that owner-scoped cancellation works.

```ts
blendshapeConfig: {
  format: 'arkit',
  deliver_chunks_ahead: true, // opt-in
  output_fps: 60,
  frames_buffer_duration: 0.2,
}
```

It is **opt-in (default off)** while the server side of the contract is being validated. Current server status (verified 2026-07-27, session ids on file): ahead-delivery works for `arkit`, `cc4_extended` and `visemes`; **requesting it with `format: 'mha'` currently stalls the TTS/blendshape stream entirely** (text replies still arrive) — keep the flag off for `mha` until the server ships the fix. `cc5_hd` delivers no frames in any mode.

***

### Example: React Three Fiber

See the full working example in `examples/react-three-fiber` which demonstrates:

* MHA-251 blendshapes direct-name-mapped onto a MetaHuman-style character (`blendshapeConfig.format: 'mha'`, no custom mapper)
* The full naturalness stack from the section above: stream fade envelope, eye-channel skip mask, per-channel gains, L/R mouth symmetrization, re-apply after the animation mixer
* Procedural blink, camera-locked gaze while speaking, head tracking, breathing — layered with body animation clips and a scripted intro scene
* Character actions (`actionConfig` → `actionResponse` → gesture clips) and a narrative-design trigger driving the greeting
