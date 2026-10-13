---
title: Start from the Convai Embody template
description: Run a PlayCanvas scene where Convai Embody resolves a character's 3D body from its character ID and drives its lip sync and blinking while it talks.
last_reviewed: "0.4.2"
---

Run the PlayCanvas Convai Embody template: a PlayCanvas scene in which Convai Embody loads the character's 3D body from its character ID. Use this template when the body should come from the character, not from a model file in your app. At the end, the character stands in your scene, answers through a chat widget, and moves its lips, eyelids, and body while it speaks.

The template uses `@convai/embody` <code class="expression">space.vars.embody_version</code> and `@convai/web-sdk` <code class="expression">space.vars.web_sdk_version</code>. Its default character has no body of its own, so it shows the default female body, Japanese F.

## Prerequisites

- Node.js 18 or later and `pnpm`.
- A Convai API key, and a character ID from the same environment as the hosts you configure.
- Git, to clone the template.

## Clone and run the template

{% stepper %}
{% step %}
### Clone the repository

```bash
git clone https://github.com/Conv-AI/convai-playcanvas-embody.git
cd convai-playcanvas-embody
pnpm install
```
{% endstep %}

{% step %}
### Add your credentials

Copy `.env.example` to `.env`, then set your API key and, optionally, your character ID and hosts.

{% code title=".env" %}
```bash
VITE_CONVAI_API_KEY=your-api-key
VITE_CONVAI_CHARACTER_ID=your-character-id
VITE_CONVAI_API_HOST=https://api-stg.convai.com
VITE_CONVAI_REALTIME_URL=https://realtime-api-stg.convai.com
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
The template defaults to Convai's staging environment, which serves web bodies and has its own character database. The character ID, `VITE_CONVAI_API_HOST`, and `VITE_CONVAI_REALTIME_URL` must all come from the same environment. A staging character ID sent to a production host fails with `Character not found`.
{% endhint %}

## Talk to the character

Select the chat button in the bottom-right corner of the page and send a message. The widget connects to Convai on first use, shows the character's name, and plays the character's voice. Drag across the scene to turn around the character, and scroll to zoom.

## Understand how the template works

The template resolves the body first, then loads it into PlayCanvas, then shares one `ConvaiClient` between the chat widget and Convai Embody.

| Step | API | What happens |
|---|---|---|
| Resolve the body | `httpResolver`, `pickRepresentation` | Turns the character ID into a model URL and animation clip URLs for the `convai-mha-1` rig. |
| Load the body | `loadCharacter` in `src/character.ts` | Loads the model and its `Idle` and `Talk` clips into PlayCanvas. |
| Connect | `ConvaiClient`, `adoptSession` | The widget connects the client. `adoptSession` gives Convai Embody the client's lip sync queue without opening a second connection. |
| Animate the face | `LipsyncSystem`, `BlinkSystem` | Shape the mouth from the MetaHuman blendshape stream, then blink and settle the eyelids. |

Convai Embody's face systems write to `morphTargetDictionary` and `morphTargetInfluences`. `src/morphs.ts` exposes PlayCanvas morph targets through those two properties, so the systems run unchanged on PlayCanvas. Convai Embody's gaze and breathing systems move bones with three.js math, so the template leaves them out. The body's own clips carry the head and torso motion.

## Verify the body and lip sync

Open the browser console after the page loads. For the default character, the template logs which body it used and how many MetaHuman channels it bound:

```text
[convai] 655b3529-09a8-4276-a0d3-8aa19adfe46a uses the default female body
[convai] 2259 MetaHuman channels bound
```

Send a message. While the character answers, its mouth moves, it blinks, and its body switches from the idle animation to the talking animation.

{% hint style="success" %}
A channel count above zero, moving lips, and the talking animation together confirm that the body, the client, and Convai Embody are connected.
{% endhint %}

## Troubleshooting

### The page says the character ID is incorrect

**Symptom:** The page shows `embodiment resolve failed for <character ID>: HTTP 404 — Incorrect Character ID provided. Please check the Character ID.`

**Cause:** The character ID does not exist in the environment that `VITE_CONVAI_API_HOST` points to.

**Fix:** Use a character ID from that environment, or point both hosts at the environment the character belongs to.

**Verify:** The character loads and the chat button appears.

### The page shows that the character has no 3D embodiment

**Symptom:** The page shows `embodiment resolve failed for <character ID>: HTTP 404 — Character has no 3D embodiment configured.`

**Cause:** The character's avatar has no published web body, and no default body applies to it in that environment.

**Fix:** Use a character with a web body, or the staging hosts, where default bodies apply.

**Verify:** The console logs a channel count above zero.

## Next steps

{% content-ref url="start-from-the-web-sdk-template.md" %}
[Start from the Web SDK template](start-from-the-web-sdk-template.md)
{% endcontent-ref %}

{% content-ref url="../convai-embody/README.md" %}
[Convai Embody](../convai-embody/README.md)
{% endcontent-ref %}
