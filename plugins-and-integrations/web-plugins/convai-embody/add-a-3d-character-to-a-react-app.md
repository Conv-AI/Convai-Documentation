---
title: Add a 3D character to a React app
description: Install Convai Embody in a React app and render a Convai character that speaks with lip sync, gaze, and blinking from its character ID.
last_reviewed: "0.4.2"
---

Render a Convai character as a 3D body in a React app with one component. Use this page when adding Convai Embody to a project for the first time. At the end, the character stands on the page, follows the camera with its eyes, and moves its mouth in sync with its voice.

## Prerequisites

- A React 18 or later app with a bundler, and Node.js 18 or later.
- A Convai account, an API key from <code class="expression">space.vars.dashboard_url</code>, and a character ID.
- A character whose avatar has a published web body, or a default body that applies to it. A character with neither cannot be rendered. See [Troubleshooting](#troubleshooting).

## Install the packages

`@convai/web-sdk` and `three` are peer dependencies, so install them alongside `@convai/embody`. The React path also needs `react` and `@react-three/fiber`.

{% tabs %}
{% tab title="npm" %}
```bash
npm install @convai/embody @convai/web-sdk three @react-three/fiber
```
{% endtab %}

{% tab title="pnpm" %}
```bash
pnpm add @convai/embody @convai/web-sdk three @react-three/fiber
```
{% endtab %}

{% tab title="yarn" %}
```bash
yarn add @convai/embody @convai/web-sdk three @react-three/fiber
```
{% endtab %}
{% endtabs %}

## Render the character

`ConvaiCharacter` brings its own canvas, camera, lights, and orbit controls. It resolves the character's body, opens the Convai Web SDK connection, plays the character's audio, and drives its face.

{% code title="src/App.tsx" %}
```tsx
import ConvaiCharacter from '@convai/embody/react'

export default function App() {
  return (
    <ConvaiCharacter
      apiKey={import.meta.env.VITE_CONVAI_API_KEY}
      characterId="YOUR_CHARACTER_ID"
    />
  )
}
```
{% endcode %}

The component fills its parent and is at least as tall as the viewport. Drag to turn around the character and scroll to move closer. Pass `orbit={false}` for a fixed camera.

{% hint style="danger" %}
An API key is a workspace-wide credential. Anyone who opens a page that ships it can read it. For a public page, create a short-lived auth token on your server and pass `token` instead of `apiKey`. See [Auth Tokens](../convai-web-sdk/auth-tokens.md).
{% endhint %}

## Place the character in your own scene

When the character joins a scene you already compose with `@react-three/fiber`, use `CharacterModel` inside your `<Canvas>` instead. It takes the same credential and character props, and adds no canvas, camera, or lights of its own.

{% code title="src/Scene.tsx" %}
```tsx
import { Canvas } from '@react-three/fiber'
import { CharacterModel } from '@convai/embody/react'

export function Scene({ token }: { token: string }) {
  return (
    <Canvas camera={{ position: [0, 1.45, 3.6], fov: 35 }}>
      <ambientLight intensity={0.6} />
      <directionalLight position={[2, 3, 2]} />
      <CharacterModel token={token} characterId="YOUR_CHARACTER_ID" />
    </Canvas>
  )
}
```
{% endcode %}

## Verify the character

Load the page and wait for the model to download. Then talk to the character, for example through the chat widget described in [Add a chat widget to a character](add-a-chat-widget-to-a-character.md).

{% hint style="success" %}
The character stands centered with its idle animation playing, its eyes follow the camera as you orbit, and its mouth moves in time with its voice when it answers.
{% endhint %}

To observe loading in code, pass `onReady`, which receives the character handle once the body is loaded and the connection is live, and `onError`, which receives the error that stopped it.

## Troubleshooting

### The character never appears

**Symptom:** `onError` receives an error whose message ends with the reason Convai gave:

```text
embodiment resolve failed for YOUR_CHARACTER_ID: HTTP 404 — Character has no 3D embodiment configured.
```

**Cause:** The character's avatar has no published web body, and no default body applies to it.

**Fix:** Choose a character whose avatar has a published web body. If none of your characters has one, contact Convai support.

**Verify:** Reload the page. The character renders.

### A credential error is thrown before anything loads

**Symptom:** Creating the character throws:

```text
@convai/embody: a credential is required — pass `token` (recommended for browsers) or `apiKey`. There is no anonymous access to Convai.
```

**Cause:** Neither `token`, `authToken`, nor `apiKey` was set, or the variable that should hold it is empty at build time.

**Fix:** Pass a credential. Check that the environment variable is defined for the build you are running.

**Verify:** The error no longer appears and the character loads.

### The model fails to load on a page with a strict Content Security Policy

**Symptom:** The body never renders, and the browser console reports a blocked request to `https://www.gstatic.com/draco/`.

**Cause:** Character models are Draco-compressed, and Convai Embody loads the Draco decoder from `https://www.gstatic.com/draco/versioned/decoders/1.5.7/` by default.

**Fix:** Allow that origin in your policy, or host the decoder files yourself and pass their URL as `dracoDecoderPath`.

**Verify:** The character renders and the console shows no blocked decoder request.

## Next steps

{% content-ref url="add-a-chat-widget-to-a-character.md" %}
[Add a chat widget to a character](add-a-chat-widget-to-a-character.md)
{% endcontent-ref %}

{% content-ref url="react-api-reference.md" %}
[React API reference](react-api-reference.md)
{% endcontent-ref %}
