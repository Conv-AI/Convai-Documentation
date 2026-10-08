---
title: Add a 3D character to a three.js scene
description: Add a Convai character to an existing 3D web scene with the framework-free Convai Embody API and update it from your own render loop.
last_reviewed: "0.4.2"
---

Add a Convai character to a three.js scene you already render, without React. Use this page when your app owns the renderer, scene, and camera. At the end, the character stands in your scene and speaks with lip sync, driven from your render loop.

## Prerequisites

- A three.js app with a renderer, a scene with lights, a camera, and a render loop.
- Node.js 18 or later and a bundler.
- A Convai API key or auth token, and a character ID. The character's avatar needs a published web body, or a default body must apply to it.

## Install the packages

The root entry point of `@convai/embody` imports neither React nor `@react-three/fiber`, so this path needs only the two required peer dependencies.

```bash
npm install @convai/embody @convai/web-sdk three
```

## Create the character

`createCharacter` resolves the character's body, loads it, opens the Convai Web SDK connection, and returns a handle. Add the handle's `root` to your scene and give it your camera so the character's gaze can track it.

{% code title="src/character.ts" %}
```typescript
import * as THREE from 'three'
import { createCharacter } from '@convai/embody'

export async function addCharacter(
  scene: THREE.Scene,
  camera: THREE.Camera,
  renderer: THREE.WebGLRenderer,
  token: string,
) {
  const character = await createCharacter({ token, characterId: 'YOUR_CHARACTER_ID' })

  scene.add(character.root)
  character.camera = camera

  const clock = new THREE.Clock()
  renderer.setAnimationLoop(() => {
    character.update(clock.getDelta())
    renderer.render(scene, camera)
  })

  return character
}
```
{% endcode %}

`update` advances the animation, lip sync, gaze, breathing, and blinking by the elapsed seconds. Call it once per frame, before rendering.

{% hint style="warning" %}
Without `character.camera`, gaze tracking does nothing and the character looks straight ahead. Set it once your camera exists.
{% endhint %}

## Send a message to the character

`character.client` is the Convai Web SDK `ConvaiClient` that Convai Embody opened. Use it for the conversation. It is `null` only when the character was created with `connect: false`.

```typescript
character.client?.sendUserTextMessage('Walk me through the lockout procedure.')
```

## Release the character

Call `dispose` when the character leaves the page. It releases the model, its materials and textures, and the animation mixer, and closes the connection Convai Embody opened.

```typescript
scene.remove(character.root)
character.dispose()
```

A client you passed in through the `client` option is left connected. Your app owns its lifetime.

## Verify the character

Run the app and send a message.

{% hint style="success" %}
The character plays its idle animation, its eyes follow the camera, and its mouth moves in time with the spoken reply.
{% endhint %}

If `createCharacter` rejects, read the error message. The [troubleshooting section of the React guide](add-a-3d-character-to-a-react-app.md#troubleshooting) covers the same errors, because both paths share one loader.

## Next steps

{% content-ref url="createcharacter-reference.md" %}
[createCharacter reference](createcharacter-reference.md)
{% endcontent-ref %}

{% content-ref url="how-convai-embody-works.md" %}
[How Convai Embody works](how-convai-embody-works.md)
{% endcontent-ref %}
