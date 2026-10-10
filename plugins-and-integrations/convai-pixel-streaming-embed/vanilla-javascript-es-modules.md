---
title: Embed an experience with JavaScript modules
description: Render a published Pixel Streaming experience from a JavaScript module script without React, using the framework-free client the package provides.
last_reviewed: "0.7.1"
icon: js
---

Render a published Convai Pixel Streaming experience from a `<script type="module">` without React, with the framework-free `PixelStreamClient` class. At the end, the page shows the experience's start screen.

## Prerequisites

- The experience ID of a published experience, and a way to authorize it: a server route that returns a Convai auth token, or a domain that Convai has allowlisted. See [Publish and authorize an experience](whitelisting-and-publishing-an-experience.md).
- A web server for the page, since the example fetches the token from a route on the same server.

## How the client is packaged

`PixelStreamClient` lives at the `@convai/experience-embed/core` entry point. The root entry point, `@convai/experience-embed`, exports the React component instead. The core entry point carries no React code, and it resolves as an ES module, as CommonJS, and as a UMD script:

| How you load the page | What to import |
| --- | --- |
| A bundler, such as Vite, webpack, or esbuild | `import { PixelStreamClient } from '@convai/experience-embed/core'` |
| A `<script type="module">` with no bundler | The ES build by URL: `dist/core/convai-embed.es.js` |
| A plain `<script>` tag | The UMD build, `dist/core/convai-embed.umd.js`, which defines the global `PixelStreamCore` |

A browser cannot resolve the bare specifier `@convai/experience-embed/core` on its own, so a module script with no bundler imports the file by URL, as below.

{% hint style="info" %}
Versions before 0.7.1 published `PixelStreamClient` only as a UMD build, so `import { PixelStreamClient } from '@convai/experience-embed/core'` failed in bundlers and in Node. Upgrade to 0.7.1 or later, or import the UMD file for its side effects and read `globalThis.PixelStreamCore`.
{% endhint %}

## Create the client

{% code title="index.html" %}
```html
<div id="experience" style="width: 100%; height: 600px"></div>

<script type="module">
  import { PixelStreamClient } from 'https://unpkg.com/@convai/experience-embed/dist/core/convai-embed.es.js';

  const { token } = await fetch('/api/convai-token').then((response) => response.json());

  const experience = new PixelStreamClient({
    container: document.getElementById('experience'),
    expId: 'YOUR_EXPERIENCE_ID',
    authToken: token,
    onIframeLoaded: () => console.log('Experience loaded'),
  });
</script>
```
{% endcode %}

The client fills its container, so give the container a size. If Convai has allowlisted your domain instead of using a token, leave out `authToken` and the fetch.

To serve the file yourself instead of from unpkg, install the package with `npm install @convai/experience-embed` and import the same file from wherever your server exposes `node_modules/@convai/experience-embed/dist/core/convai-embed.es.js`. With a bundler, import `@convai/experience-embed/core` by name and let the bundler resolve it.

## Control the experience

The client shows a **Click to start your experience** screen. To start the experience from your own control instead, pass an `InitialScreen` element and call `experience.initializeExperience()` from it. Once `onIframeLoaded` has fired, call methods such as `experience.enableCamera()` or `experience.sendMessageToCharacter('Hello')`. When you remove the experience from the page, call `experience.destroy()` and clear the container.

The [Pixel Streaming Embed API reference](api-reference.md#pixelstreamclient-options) lists every option, method, and callback.

## Verify the embed

Open the page through your web server and click the start screen.

{% hint style="success" %}
The experience replaces the start screen, and the browser console logs `Experience loaded`.
{% endhint %}

If the container shows an error message instead, see [Troubleshooting](react-typescript.md#troubleshooting); the causes are the same.

## Next steps

{% content-ref url="api-reference.md" %}
[Pixel Streaming Embed API reference](api-reference.md)
{% endcontent-ref %}
