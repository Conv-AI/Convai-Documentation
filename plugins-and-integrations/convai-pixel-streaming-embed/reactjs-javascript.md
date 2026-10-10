---
title: Embed an experience in a React JavaScript app
description: Install the Pixel Streaming Embed package in a React app written in JavaScript, render a published experience, and start it from your own button.
last_reviewed: "0.7.1"
icon: react
---

Render a published Convai Pixel Streaming experience in a React app written in JavaScript. The component and its options are the same as in TypeScript, without the type annotations. At the end, the experience plays inside your page after the user starts it.

## Prerequisites

- A React 18 app with a bundler such as Vite.
- The experience ID of a published experience, and a way to authorize it: a server route that returns a Convai auth token, or a domain that Convai has allowlisted. See [Publish and authorize an experience](whitelisting-and-publishing-an-experience.md).

## Install the package

The current release is <code class="expression">space.vars.experience_embed_version</code>.

{% tabs %}
{% tab title="npm" %}
```bash
npm install @convai/experience-embed
```
{% endtab %}

{% tab title="pnpm" %}
```bash
pnpm add @convai/experience-embed
```
{% endtab %}

{% tab title="yarn" %}
```bash
yarn add @convai/experience-embed
```
{% endtab %}
{% endtabs %}

## Render the experience

This example fetches an auth token from a route on your server, `/api/convai-token`, then renders the experience with its own start button. `PixelStreamComponent` fills its parent element, so give the parent a size:

{% code title="src/App.jsx" %}
```jsx
import { useEffect, useRef, useState } from 'react';
import { PixelStreamComponent } from '@convai/experience-embed';

export default function App() {
  const streamRef = useRef(null);
  const [token, setToken] = useState();

  useEffect(() => {
    fetch('/api/convai-token')
      .then((response) => response.json())
      .then((body) => setToken(body.token));
  }, []);

  if (!token) return <p>Loading…</p>;

  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <PixelStreamComponent
        ref={streamRef}
        expId="YOUR_EXPERIENCE_ID"
        authToken={token}
        InitialScreen={
          <button onClick={() => streamRef.current?.initializeExperience()}>
            Start the experience
          </button>
        }
        onIframeLoaded={() => console.log('Experience loaded')}
      />
    </div>
  );
}
```
{% endcode %}

If Convai has allowlisted your domain instead, leave out `authToken` and render the component straight away. Without `InitialScreen`, the component shows a **Click to start your experience** screen that starts the experience on click.

## Control the experience

Once `onIframeLoaded` has fired, call the methods on the ref, for example `streamRef.current?.enableCamera()` or `streamRef.current?.sendMessageToCharacter('Hello')`. The [Pixel Streaming Embed API reference](api-reference.md) lists every method and callback.

## Verify the embed

Load the page and select **Start the experience**.

{% hint style="success" %}
The experience replaces the button, and the browser console logs `Experience loaded`.
{% endhint %}

If the embed shows an error message instead, see [Troubleshooting](react-typescript.md#troubleshooting) on the TypeScript page; the causes are the same.

## Next steps

{% content-ref url="api-reference.md" %}
[Pixel Streaming Embed API reference](api-reference.md)
{% endcontent-ref %}
