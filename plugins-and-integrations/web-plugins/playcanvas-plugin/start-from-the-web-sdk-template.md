---
title: Start from the Web SDK template
description: Run a PlayCanvas scene where a Convai character talks with MetaHuman lip sync, using the Convai Web SDK and a character model you ship yourself.
last_reviewed: "1.9.1"
---

Run the PlayCanvas Web SDK template: a PlayCanvas scene with a talking Convai character, built on the Convai Web SDK. Use this template when you ship the character's 3D model with your app. At the end, the character stands in your scene, answers through a chat widget, and moves its lips and body while it speaks.

The template uses `@convai/web-sdk` <code class="expression">space.vars.web_sdk_version</code> and includes Japanese F, a MetaHuman-rig character, as the default model.

## Prerequisites

- Node.js 18 or later and `pnpm`.
- A Convai API key and a character ID from the Convai dashboard.
- Git, to clone the template.

## Clone and run the template

{% stepper %}
{% step %}
### Clone the repository

```bash
git clone https://github.com/Conv-AI/convai-playcanvas-web-sdk.git
cd convai-playcanvas-web-sdk
pnpm install
```
{% endstep %}

{% step %}
### Add your credentials

Copy `.env.example` to `.env`, then set your API key and, optionally, your character ID.

{% code title=".env" %}
```bash
VITE_CONVAI_API_KEY=your-api-key
VITE_CONVAI_CHARACTER_ID=your-character-id
```
{% endcode %}

Vite reads `.env` at build time. Restart the dev server after you change it.
{% endstep %}

{% step %}
### Start the dev server

```bash
pnpm dev
```

Open the URL that Vite prints.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
The API key is bundled into the page that the browser downloads. Keep `apiKey` for local development. For a public deployment, create a short-lived auth token on your server and pass `authToken` to `ConvaiClient` instead.
{% endhint %}

## Talk to the character

Select the chat button in the bottom-right corner of the page and send a message. The widget connects to Convai on first use and plays the character's voice. Drag across the scene to turn around the character, and scroll to zoom.

## Use the template in the PlayCanvas Editor

The template is also a public PlayCanvas Editor project, [Convai Web SDK](https://playcanvas.com/project/1619450/overview/convai-web-sdk). It needs no build step: its `convaiCharacter` script imports `@convai/web-sdk` from esm.sh.

1. Open the project and fork it.
2. Select the **Japanese F** entity.
3. In the `convaiCharacter` script, set **API Key** and, optionally, **Character ID**.
4. Select **Launch**.

To add the character to your own Editor project, upload `editor/convai-character.mjs` from the repository, add the `convaiCharacter` script to a MetaHuman-rig model's entity, and set **Idle Animation** and **Talk Animation** to the names of the animation assets the model's import created.

## Understand how the template works

The template creates one `ConvaiClient` and shares it between the chat widget and the scene. The client asks Convai for MetaHuman blendshapes with `enableLipsync: true` and `blendshapeConfig: { format: 'mha' }`.

| File | Role |
|---|---|
| `src/main.ts` | Creates the scene, loads the character, creates the `ConvaiClient`, and mounts the widget with `createConvaiWidget`. |
| `src/lipsync.ts` | Reads `client.blendshapeQueue` at the stream's frame rate and shapes each frame with `createLipsyncProcessor('mha')` from `@convai/web-sdk/lipsync-helpers`. |
| `src/morphs.ts` | Exposes PlayCanvas morph targets through `morphTargetDictionary` and `morphTargetInfluences`, which are the only properties the lip sync helpers use. `flush()` copies the weights to each PlayCanvas `MorphInstance`. |
| `src/character.ts` | Loads the GLB and its animation pack, scales centimeter rigs to meters, and cross-fades between clips. |
| `src/scene.ts` | Creates the PlayCanvas application, camera, lights, and orbit controls. |

Each frame, the scene plays the `Talk` clip while the character speaks and the `Idle` clip otherwise.

## Use your own character model

Any GLB on the MetaHuman rig works if its face mesh carries the `CTRL_expressions_*` morph targets. Add the model and its animation pack to `public/models`, then point `loadCharacter` at them in `src/main.ts`:

{% code title="src/main.ts" %}
```typescript
const character = await loadCharacter(app, '/models/my-character.glb', {
  Idle: '/models/my-character-animations.glb',
  Talk: '/models/my-character-animations.glb',
})
```
{% endcode %}

Each key selects the animation with the same name from its file. For a model on the ARKit rig, set `blendshapeConfig: { format: 'arkit' }` on the client and use `createLipsyncProcessor('arkit')`.

## Verify the character speaks with lip sync

Open the browser console after the page loads. The template logs how many MetaHuman channels it bound to the model:

```text
[convai] 2259 MetaHuman channels bound
```

Send a message. While the character answers, its mouth moves and its body switches from the idle animation to the talking animation.

{% hint style="success" %}
A channel count above zero, moving lips, and the talking animation together confirm that the client, the lip sync processor, and the model are connected.
{% endhint %}

## Troubleshooting

### The page shows a message about the API key

**Symptom:** The page shows `Set VITE_CONVAI_API_KEY in .env (see .env.example), then restart the dev server.`

**Cause:** `.env` is missing, the key is empty, or the dev server started before you saved the file.

**Fix:** Set `VITE_CONVAI_API_KEY` in `.env`, then restart `pnpm dev`.

**Verify:** The character loads and the chat button appears.

### The character talks but its lips do not move

**Symptom:** The console logs `[convai] 0 MetaHuman channels bound`.

**Cause:** The model has no `CTRL_expressions_*` morph targets, so it is not on the MetaHuman rig.

**Fix:** Use a MetaHuman-rig model, or switch the client and the processor to the format your model's morph targets use.

**Verify:** The console logs a channel count above zero.

## Next steps

{% content-ref url="start-from-the-convai-embody-template.md" %}
[Start from the Convai Embody template](start-from-the-convai-embody-template.md)
{% endcontent-ref %}

{% content-ref url="../convai-web-sdk/README.md" %}
[Convai Web SDK](../convai-web-sdk/README.md)
{% endcontent-ref %}
