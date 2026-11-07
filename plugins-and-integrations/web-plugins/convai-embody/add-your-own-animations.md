---
title: Add your own animations to a character
description: Load your own animation clips onto a Convai Embody character, including Mixamo FBX files, play and crossfade them, and switch to a talking clip while the character speaks.
last_reviewed: "1.1.1"
---

Give a Convai Embody character animations of your own, such as a wave, a gesture, or a different idle, from your own GLB files or straight from Mixamo. Use this page when the clips that come with the character's body are not the ones you want. At the end, the character plays your clips, crossfades between them, and switches to a talking clip while it speaks.

## Prerequisites

- A page that already renders a character. See [Add a 3D character to a React app](add-a-3d-character-to-a-react-app.md) or [Add a 3D character to a three.js scene](add-a-3d-character-to-a-three-js-scene.md).
- Your animations as GLB, glTF, or FBX files. Clips authored on the Unreal Engine MetaHuman skeleton, the `convai-mha-1` rig, play as they are. Clips authored on a Mixamo or Rigify skeleton are retargeted onto the body when the character loads; see [Use animations from Mixamo and other skeletons](#use-animations-from-mixamo-and-other-skeletons).
- For a file on the MetaHuman skeleton, the name of each animation inside it. Convai Embody finds a clip by that name, not by the file name.

## How clips are found

A character's clips come from two places, and Convai Embody loads both when the character is created:

1. **The character's body.** Its manifest lists clips by name and file. The male default body ships `Hi`, `Idle`, `Talk`, and `Walk`. The female default ships `Hi`, `Idle`, `Talk`, `walk`, `SitDown`, `SitIdle`, and `StandUp`. Names are case-sensitive, so read `character.animations.names` rather than assuming them.
2. **The `animations` option.** A map from clip name to the URL of a GLB, glTF, or FBX file that contains an animation with that name.

A name in `animations` that the body also lists replaces the body's clip. One file can hold several animations; list it once for each name you want from it.

{% hint style="warning" %}
The key in `animations` must equal the animation's name inside the GLB. `animations: { Wave: '/clips/gestures.glb' }` loads nothing if the animation in that file is called `wave_01`. Open the file in a glTF viewer or Blender to read the names.
{% endhint %}

## Load your clips

Pass `animations` when the character is created. In React, pass it as a prop; keep the object stable, because the character reads it once and does not reload when it changes.

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import { ConvaiCharacter } from '@convai/embody/react'

const ANIMATIONS = {
  Wave: '/animations/gestures.glb',
  Idle: '/animations/calm-idle.glb',
}

export default function App() {
  return (
    <ConvaiCharacter
      token={token}
      characterId="YOUR_CHARACTER_ID"
      animations={ANIMATIONS}
    />
  )
}
```
{% endcode %}
{% endtab %}

{% tab title="three.js" %}
{% code title="src/character.ts" %}
```typescript
import { createCharacter } from '@convai/embody'

const character = await createCharacter({
  token,
  characterId: 'YOUR_CHARACTER_ID',
  animations: {
    Wave: '/animations/gestures.glb',
    Idle: '/animations/calm-idle.glb',
  },
})
```
{% endcode %}
{% endtab %}
{% endtabs %}

Here `Idle` replaces the body's own idle, and `Wave` is added next to the body's clips. The files load in parallel with the body. A file on another host needs CORS headers that allow your page.

## Use animations from Mixamo and other skeletons

A clip made for another skeleton is retargeted onto the character's body when the character loads, so you can pass a Mixamo download as it is.

```typescript
const character = await createCharacter({
  token,
  characterId: 'YOUR_CHARACTER_ID',
  animations: {
    Wave: '/animations/Waving.fbx',
    Think: '/animations/Thinking.fbx',
  },
})
```

Convai Embody reads three kinds of skeleton:

| Skeleton | Recognised by |
|---|---|
| Mixamo | Bone names such as `mixamorig:Hips`, with any `mixamorig` prefix or none |
| Rigify | Deform bones such as `DEF-hips`, `DEF-thigh.L`, and `DEF-upper_arm.L` |
| Unreal Engine mannequin | Bone names such as `pelvis`, `spine_01`, and `thigh_l`. These are the MetaHuman names, so a mannequin clip plays on the body as authored, without retargeting. |

A file from a recognised skeleton needs no matching clip name. When the file has no animation named like the key, its only animation is used under the key's name; Mixamo names every clip `mixamo.com`, so this is what makes a Mixamo file work. A file with several animations still needs the key to match one of them.

Retargeting moves each bone the way the source bone moves, measured from each skeleton's own rest pose, so a clip authored in a T-pose plays correctly on a body bound in an A-pose. It also fits the clip to the body:

- Hip movement is scaled by the ratio of the two skeletons' hip heights, so the clip plays at the body's size.
- Feet move from the body's own flat stance, and the neck and head from the body's own build, rather than copying the source skeleton's.
- Elbows and hands are kept outside the torso and thighs. A clip made for a slimmer body otherwise rests its hands inside a wider one.
- In a clip where the character stands, the trunk is pitched forward by at most 6 degrees, bent knees are straightened, and low shoulders are lifted by at most 6 degrees, because Mixamo's standing clips lean back on a MetaHuman body. A clip where the hips drop, such as kneeling or sitting, keeps its posture.

FBX support is loaded only when a URL ends in `.fbx`, so an app that never uses FBX does not ship the FBX loader. A URL without that extension, such as a `blob:` URL, is read as glTF.

{% hint style="info" %}
From Mixamo, download as **FBX Binary (.fbx)** and **Without Skin**: the retargeter reads only the skeleton, and the file is much smaller without the mesh. For a walk or run, tick **In Place** so the clip does not carry the character away.
{% endhint %}

## Choose the clip that plays first

When the character loads, it plays a clip named `idle`, ignoring case. A body with no such clip plays its first clip, so the character is never left in its bind pose. Use `idleClip` to choose another, or `false` to start with no clip playing.

```typescript
const character = await createCharacter({ token, characterId, idleClip: 'SitIdle' })
```

A name the character does not have plays nothing rather than a substitute.

## Play and crossfade clips

`character.animations` controls playback. It plays one clip at a time and blends from the current clip to the next.

```typescript
// Blend from whatever is playing to Wave, play it once, then go back to Idle.
character.animations.crossfadeTo('Wave', { once: true, thenBackTo: 'Idle' })

// Loop a clip, blending in over half a second.
character.animations.crossfadeTo('Walk', { duration: 0.5 })

character.animations.names   // every clip the character has
character.animations.playing // the clip playing now, or null
```

`crossfadeTo` does nothing when the clip is already playing. A clip name the character does not have throws an error that lists the names it does have.

In React, get the character from `onReady`:

```tsx
<ConvaiCharacter
  token={token}
  characterId="YOUR_CHARACTER_ID"
  animations={ANIMATIONS}
  onReady={(character) => character.animations.crossfadeTo('Wave', { once: true, thenBackTo: 'Idle' })}
/>
```

`onReady` runs once for each character that loads, so setup done there is not repeated when your component re-renders.

## Switch to a talking clip while the character speaks

Convai Embody moves the mouth while the character speaks, but it does not change the body clip. To play a talking clip, listen for the client's `speakingChange` event and crossfade.

```typescript
const stop = character.client?.on('speakingChange', (speaking) => {
  character.animations.crossfadeTo(speaking ? 'Talk' : 'Idle')
})

// When the character goes away:
stop?.()
```

Lip sync, gaze, and blinking keep running on top of whichever clip plays, so the talking clip only needs to move the body.

## Add clips after the character loads

To add clips later, load the file yourself and register its animations. `register` returns, for each clip, how many tracks it kept and how many it dropped.

```typescript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js'

const loader = new GLTFLoader()
const draco = new DRACOLoader()
draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.7/')
loader.setDRACOLoader(draco)

const gltf = await loader.loadAsync('/animations/dance.glb')
draco.dispose()

character.animations.register(gltf.animations)
character.animations.crossfadeTo('Dance', { once: true, thenBackTo: 'Idle' })
```

The Draco decoder is needed only when the file is Draco-compressed.

## Verify the clips

Run the app.

{% hint style="success" %}
`character.animations.names` lists your clip names, the character starts in the idle you chose, and a crossfade blends into your clip without snapping.
{% endhint %}

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `[embody] unknown clip "Wave" (have: Hi, Idle, …)` | No animation named `Wave` was loaded. Check that the key in `animations` matches the animation's name inside the file, letter for letter. |
| The console warns `clip "…": N/M tracks target absent bones — dropped` | The clip animates bones the model does not have, such as extra finger, hair, or helper bones. Those tracks are skipped and the rest plays. It is expected for clips exported from a richer rig; if the clip does not move at all, it was authored on a different skeleton. |
| The clip plays but the body does not move, or moves wrongly | The animation was authored on a skeleton that is neither the MetaHuman one nor one Convai Embody retargets from (Mixamo, Rigify). Retarget it to the MetaHuman skeleton in your 3D tool, then export it again. |
| The console warns `clip "…": retargeting from mixamo failed` | The file's skeleton was recognised but could not be measured, for example its hips are not above its feet in the rest pose. The other clips still load. Export the file again from its source. |
| The file never loads | Read the browser's network panel. A file on another host needs CORS headers that allow your page. |
| Your walking clip moves the character away | Clips play as authored, including any forward movement baked into them. The default bodies' `Walk` is exported in place; export yours the same way for a character that stays where you put it. |

## Next steps

{% content-ref url="use-your-own-3d-model.md" %}
[Use your own 3D model](use-your-own-3d-model.md)
{% endcontent-ref %}

{% content-ref url="createcharacter-reference.md" %}
[createCharacter reference](createcharacter-reference.md)
{% endcontent-ref %}
