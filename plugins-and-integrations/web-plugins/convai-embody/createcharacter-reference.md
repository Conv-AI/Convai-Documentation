---
title: createCharacter reference
description: Reference for the createCharacter function in Convai Embody, including every option, its default, and the character handle it returns.
last_reviewed: "1.0.1-beta.0"
---

`createCharacter` is exported from `@convai/embody`. It resolves a character's body, loads it, opens a Convai Web SDK connection, and resolves to a `CharacterHandle`. The React components accept the same options as props.

```typescript
function createCharacter(options: CreateCharacterOptions): Promise<CharacterHandle>
```

## Options

`characterId` and one credential are required. Every other option has a working default.

### Identity and connection

| Option | Type | Default | Description |
|---|---|---|---|
| `characterId` | `string` | required | The character to render. |
| `token` | `string` | none | A Convai auth token. The credential to use in a browser. Takes precedence over `apiKey`. |
| `authToken` | `string` | none | The same as `token`, under the name the Convai Web SDK uses. |
| `apiKey` | `string` | none | A Convai API key. Use only in trusted contexts. |
| `baseUrl` | `string` | the release's Convai host | Backend host. Change only to point at a different Convai environment. |
| `session` | `SessionOptions` without `characterId`, `apiKey`, `authToken` | none | Extra Convai Web SDK connection options, such as voice, memory, transport, and `endUserId`. |
| `client` | `ConvaiClient` | none | A client your app already created and connected. Convai Embody drives lip sync from it and never disconnects it. Read once, when the character is created. |
| `connect` | `boolean` | `true` | `false` renders the body with no connection, no audio, and no lip sync. `client` on the handle is then `null`. |
| `resolver` | `CharacterResolver` | an HTTP resolver built from the credential | Resolves the body manifest yourself: a model you host, a private asset backend, a test fixture, or a prefetched manifest. See [Resolvers and the body manifest](#resolvers-and-the-body-manifest). |

### Body and loading

| Option | Type | Default | Description |
|---|---|---|---|
| `supportedRigs` | `string[]` | `['convai-mha-1']` | Rig profiles to accept, in preference order. |
| `modelVariant` | `'auto' \| 'full' \| 'lite'` | `'auto'` | Which model file to load when the body ships a Full and a Lite file. `'auto'` loads Lite on phones, tablets, and GPUs too small for Full's blendshapes, and Full everywhere else. |
| `dracoDecoderPath` | `string` | `'https://www.gstatic.com/draco/versioned/decoders/1.5.7/'` | Base URL for the Draco decoder. Set it to self-host the decoder. |
| `targetHeight` | `number` | `1.7` | Height the body is scaled to, in meters. |
| `groundY` | `number` | `0` | Height of the floor the feet are placed on, in meters. |
| `animations` | `Record<string, string>` | none | Extra clips, name to the URL of a GLB that holds an animation with that name. Merged over the character's own clips by name. Read once, when the character is created. See [Add your own animations](add-your-own-animations.md). |
| `idleClip` | `string \| false` | a clip named `idle`, otherwise the first clip | Clip to play on load. `false` starts paused. |
| `faceMaterials` | `boolean \| FaceMaterialTuning` | `true` | Eye, teeth, and eye-socket shading for MetaHuman materials named `Eyes*`, `Teeth*`, and `Eyeocclusion*`. `false` leaves every material as the model shipped it. |
| `decorators` | `CharacterDecorator[]` | none | Functions run once after loading and before the first frame. |

### Motion and speech

| Option | Type | Default | Description |
|---|---|---|---|
| `motion` | `boolean` | `true` | `false` turns off gaze, breathing, eye movement, and blinking, keeping only animation clips and lip sync. |
| `gaze` | `GazeConfig` | built-in tuning | Head and neck gaze tracking. |
| `eyeGaze` | `EyeGazeConfig` | built-in tuning | Eye movement. |
| `blink` | `BlinkConfig` | built-in tuning | Blinking and eyelids. |
| `breathing` | `BreathingConfig` | built-in tuning | Additive chest and spine breathing. |
| `mouth` | `MouthTuning` | built-in tuning | Lip sync tuning, such as the jaw-open cap and lip-seal thresholds. |
| `correctiveMap` | `CorrectiveMap` | none | A table, built by `compileCorrectiveMap`, that re-weights each lip sync frame toward the full rig. Use it for a body that drives one morph per control and so renders none of the rig's corrective shapes or joint movement. Replace it at any time through `handle.lipsync.correctiveMap`. |

## CharacterHandle

| Member | Type | Description |
|---|---|---|
| `root` | `THREE.Object3D` | The character. Add it to your scene. |
| `client` | `ConvaiClient \| null` | The live Convai Web SDK client. `null` only when `connect` is `false`. |
| `camera` | `THREE.Camera \| undefined` | Set this to your camera. Gaze tracking does nothing without it. |
| `animations` | `AnimationController` | Plays and crossfades the character's clips. See [AnimationController](#animationcontroller). |
| `model` | `ModelVariant` | The model file that loaded, one of `representation.model`. |
| `lipsync` | `LipsyncSystem` | The lip sync system. |
| `gaze` | `GazeSystem` | The head and neck gaze system. |
| `bundle` | `CharacterBundle` | The resolved body manifest. |
| `representation` | `Representation` | The rig representation that was loaded. |
| `rig` | `ResolvedRig` | Bones and morph targets resolved on the loaded model. |
| `pipeline` | `Pipeline` | The ordered per-frame systems. |

### update

```typescript
update(delta: number, queue?: BlendshapeQueue): void
```

Advances the character by `delta` seconds. Call it once per frame. `queue` overrides which conversation turn the body lip-syncs to, for when one client drives several characters.

### dispose

```typescript
dispose(): void
```

Releases the model, materials, textures, and animation mixer. Closes the connection when Convai Embody opened it. A client passed in through `client` is left connected.

## AnimationController

`character.animations` plays the character's clips, one at a time, and blends between them.

| Member | Type | Description |
|---|---|---|
| `names` | `string[]` | Every clip the character has. |
| `playing` | `string \| null` | The clip playing now. |
| `play(name)` | `(name: string) => void` | Starts a clip from its first frame and loops it, with no blend. |
| `crossfadeTo(name, options?)` | `(name: string, options?: ClipTransition) => void` | Blends from the current clip to `name`. Does nothing when `name` is already playing. |
| `register(clips)` | `(clips: THREE.AnimationClip[]) => { name: string; kept: number; dropped: number }[]` | Adds clips, such as the `animations` of a GLB you loaded. Tracks for bones the model does not have are dropped and reported. |
| `mixer` | `THREE.AnimationMixer` | The underlying mixer. |

`ClipTransition`:

| Field | Type | Default | Description |
|---|---|---|---|
| `duration` | `number` | `0.35` | Blend time in seconds. |
| `once` | `boolean` | `false` | Play once and hold the last frame instead of looping. |
| `thenBackTo` | `string` | none | With `once`, blend to this clip when the clip finishes. |

`play` and `crossfadeTo` throw for a name the character does not have. Convai Embody does not change clips when the character speaks; listen for the client's `speakingChange` event to do it, as in [Add your own animations](add-your-own-animations.md#switch-to-a-talking-clip-while-the-character-speaks).

## Resolvers and the body manifest

A `CharacterResolver` has one method, `resolve(characterId: string): Promise<CharacterBundle>`. The default, `httpResolver({ baseUrl?, apiKey?, authToken? })`, asks Convai. Supply your own to load a model you host; see [Use your own 3D model](use-your-own-3d-model.md).

`CharacterBundle`:

| Field | Type | Description |
|---|---|---|
| `characterId` | `string` | The character the manifest is for. |
| `avatarId` | `string` | Identifies the body. |
| `gender` | `string` | Optional. The body's gender, as Convai reports it. |
| `fallback` | `boolean` | Optional. `true` when Convai served a default body because the character has none of its own. |
| `thumbnail` | `string` | Optional. An image of the body. |
| `representations` | `Representation[]` | The body for each rig it was built for. |

`Representation`:

| Field | Type | Description |
|---|---|---|
| `rig` | `string` | The rig profile, `'convai-mha-1'` for a MetaHuman body. |
| `model` | `ModelVariant[]` | The model files: `{ url, lod?, morphTargets?, size? }`. `lod` 0 is Full and 1 is Lite; `morphTargets` is the most blendshapes on any one mesh, which `modelVariant: 'auto'` compares with the GPU's limit. |
| `clips` | `Record<string, { url: string }>` | Optional. Clip name to the GLB that holds an animation with that name. |

In React, a resolver is part of what identifies the character: a new resolver object loads the model again. Define it outside the component or memoize it.

## Errors

| Condition | Result |
|---|---|
| No `token`, `authToken`, `apiKey`, or `resolver` | Throws an error whose message begins `@convai/embody: a credential is required`. No request is sent. |
| Convai cannot resolve a body for the character | Rejects with `embodiment resolve failed for <characterId>: HTTP <status>`, followed by the reason Convai gave, such as `Character has no 3D embodiment configured.` |
| The body offers no rig in `supportedRigs` | Rejects with `no supported representation: character offers [<rigs>], embody supports [<rigs>]` |
| `play` or `crossfadeTo` with a clip the character does not have | Throws `[embody] unknown clip "<name>" (have: <names>)` |

## Related reference

{% content-ref url="react-api-reference.md" %}
[React API reference](react-api-reference.md)
{% endcontent-ref %}
