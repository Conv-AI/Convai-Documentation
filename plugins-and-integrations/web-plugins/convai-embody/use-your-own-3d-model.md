---
title: Use your own 3D model
description: Render a Convai character with a MetaHuman GLB model that you host, including Full and Lite files and your own animation clips.
last_reviewed: "1.0.1"
---

Render a Convai character with a 3D model you host yourself, instead of the body Convai serves for the character. Use this page when you have your own MetaHuman exported to GLB. At the end, your model loads in place of the default body and talks with lip sync, gaze, and blinking through the character's normal Convai connection.

## Prerequisites

- A page that already renders a character. See [Add a 3D character to a React app](add-a-3d-character-to-a-react-app.md) or [Add a 3D character to a three.js scene](add-a-3d-character-to-a-three-js-scene.md).
- Your model as a GLB file built on the Unreal Engine MetaHuman rig. The next section lists what the file must contain.
- A place to host the file that your page can fetch, with CORS headers that allow your page when the host differs.

## What the model needs

Convai Embody drives a body through the names of its bones and blendshapes. The one rig it supports is `convai-mha-1`, the Unreal Engine MetaHuman rig, so the file needs the MetaHuman names exactly as Unreal Engine exports them.

| Part | Names | What uses it |
|---|---|---|
| Head and spine bones | `head`, `neck_01`, `neck_02`, `spine_02`, `spine_04` | Gaze and breathing. A missing bone turns off the motion that drives it. |
| Body bones | The rest of the MetaHuman skeleton, from `pelvis` and `spine_01` through `spine_05` to the limbs | Animation clips, which target bones by name. |
| Face blendshapes | MetaHuman expression morph targets, `CTRL_expressions_*` | Lip sync, blinking, and eye movement. |
| Face materials (optional) | Materials named `Eyes*`, `Teeth*`, and `Eyeocclusion*` | Eye and teeth shading. Turn it off with `faceMaterials: false`. |

Draco-compressed files load as they are; the decoder is fetched from `dracoDecoderPath`.

{% hint style="warning" %}
Models on other rigs, such as Ready Player Me, Mixamo, VRoid, or Character Creator, load but do not come alive: their head stays still and their face does not move, because none of these names match. Retarget the model to the MetaHuman rig in your 3D tool first.
{% endhint %}

## Describe your model with a resolver

Convai Embody learns where a body's files are from a resolver: an object with one `resolve` method that returns the body's manifest. The default resolver asks Convai. Supply your own to point at your files.

{% code title="src/myModel.ts" %}
```typescript
import type { CharacterResolver } from '@convai/embody'

export const myModel: CharacterResolver = {
  async resolve(characterId) {
    return {
      characterId,
      avatarId: 'my-model',
      representations: [
        {
          rig: 'convai-mha-1',
          model: [{ url: 'https://assets.example.com/my-model.glb' }],
          clips: {
            Idle: { url: 'https://assets.example.com/my-animations.glb' },
            Talk: { url: 'https://assets.example.com/my-animations.glb' },
          },
        },
      ],
    }
  },
}
```
{% endcode %}

| Field | Description |
|---|---|
| `characterId` | The character ID you were asked to resolve. Return it unchanged. |
| `avatarId` | Any stable identifier for this model. It appears as `character.bundle.avatarId`. |
| `representations` | The model for each rig. List one, with `rig: 'convai-mha-1'`. |
| `representations[].model` | The model files. One entry is enough; see [Ship a Full and a Lite file](#ship-a-full-and-a-lite-file) for two. |
| `representations[].clips` | Animation clips, name to `{ url }`. Each name must equal an animation's name inside that file. Optional; see [Add your own animations](add-your-own-animations.md). |

## Render the character with your model

Pass the resolver with the character ID and credential you already use. The model comes from your resolver, and the conversation still comes from the character's Convai connection, so the character keeps its voice, knowledge, and memory.

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import { ConvaiCharacter } from '@convai/embody/react'
import { myModel } from './myModel'

export default function App() {
  return <ConvaiCharacter token={token} characterId="YOUR_CHARACTER_ID" resolver={myModel} />
}
```
{% endcode %}
{% endtab %}

{% tab title="three.js" %}
{% code title="src/character.ts" %}
```typescript
import { createCharacter } from '@convai/embody'
import { myModel } from './myModel'

const character = await createCharacter({
  token,
  characterId: 'YOUR_CHARACTER_ID',
  resolver: myModel,
})
```
{% endcode %}
{% endtab %}
{% endtabs %}

In React, define the resolver outside the component or wrap it in `useMemo`. A new resolver object loads the model again, so a resolver written inline in the component reloads the model on every render. Change it only when the model should change.

## Keep Convai's animations with your model

To use your model with the animations Convai serves for the character, ask the default resolver for the character's manifest and replace only its model files.

```typescript
import { httpResolver, type CharacterResolver } from '@convai/embody'

const convai = httpResolver({ authToken: token })

export const myModelWithConvaiClips: CharacterResolver = {
  async resolve(characterId) {
    const bundle = await convai.resolve(characterId)
    for (const rep of bundle.representations) {
      rep.model = [{ url: 'https://assets.example.com/my-model.glb' }]
    }
    return { ...bundle, avatarId: 'my-model', fallback: false }
  },
}
```

The clips are made for the MetaHuman skeleton, so they fit any model on the same rig.

## Ship a Full and a Lite file

Many phones allow 256 vertex-shader uniforms in all, and three.js spends one on each blendshape, so a head with all 251 MetaHuman blendshapes fails to draw on them. A body can ship two files: **Full**, with every blendshape, and **Lite**, with a reduced set. List both, with `lod` 0 for Full and 1 for Lite, and the most blendshapes on any one mesh as `morphTargets`.

```typescript
model: [
  { lod: 0, url: 'https://assets.example.com/my-model.glb', morphTargets: 251 },
  { lod: 1, url: 'https://assets.example.com/my-model-lite.glb', morphTargets: 103 },
],
```

Convai Embody loads Lite on phones and tablets, and on any GPU too small for Full's blendshapes, and Full everywhere else. Keep Lite at 192 blendshapes or fewer, which leaves room for the rest of the shader on a 256-uniform phone. `character.model` reports which file loaded, and `modelVariant: 'full'` or `'lite'` forces one, for example to check Lite on a desktop.

## Preview a model without a conversation

To render a model with no Convai connection, for example in an asset review page, pass `connect: false`. With a resolver and `connect: false`, no credential is needed.

```typescript
const character = await createCharacter({ characterId: 'preview', resolver: myModel, connect: false })
```

The model plays its clips, breathes, blinks, and follows the camera, but it has no voice and no lip sync. `character.client` is `null`.

## Verify the model

Run the app and send the character a message.

{% hint style="success" %}
Your model stands in the scene, `character.model.url` is your file, `character.rig.missing` is empty, and the mouth moves with the spoken reply.
{% endhint %}

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `no supported representation: character offers [<rigs>], embody supports [convai-mha-1]` | The resolver's representation names another rig. Set `rig: 'convai-mha-1'` for a MetaHuman model. |
| The console warns `rig "convai-mha-1": missing required bone(s) — …` | The model lacks the head or spine bones listed in the warning, so gaze or breathing is off for them. Export the full MetaHuman skeleton with its Unreal Engine bone names. |
| The body loads but the face stays still while the character talks | The model's blendshapes do not have MetaHuman `CTRL_expressions_*` names. Export the face's expression morph targets from the MetaHuman. |
| The head is not drawn on some phones | The model has more blendshapes than the phone's GPU allows. Ship a Lite file, as in [Ship a Full and a Lite file](#ship-a-full-and-a-lite-file). |
| The model is the wrong size or below the floor | The model is scaled to `targetHeight` (1.7 meters) and its feet placed at `groundY`. Set either option to change them. |
| The file never loads, or the Draco decoder fails | Read the browser's network panel. Files on another host need CORS, and a page whose content security policy blocks `gstatic.com` needs `dracoDecoderPath` pointed at a self-hosted decoder. |

## Next steps

{% content-ref url="add-your-own-animations.md" %}
[Add your own animations to a character](add-your-own-animations.md)
{% endcontent-ref %}

{% content-ref url="createcharacter-reference.md" %}
[createCharacter reference](createcharacter-reference.md)
{% endcontent-ref %}
