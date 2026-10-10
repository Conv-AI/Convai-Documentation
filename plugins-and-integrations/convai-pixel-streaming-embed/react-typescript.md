---
title: Embed an experience in a React TypeScript app
description: Install the Pixel Streaming Embed package in a React TypeScript app, render a published experience, and control it from your own interface.
last_reviewed: "0.7.1"
icon: react
---

Render a published Convai Pixel Streaming experience in a React app written in TypeScript, and control its camera, audio, microphone, and chat from your own code. At the end, the experience plays inside your page after the user clicks to start it.

## Prerequisites

- A React 18 app written in TypeScript, with a bundler such as Vite.
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

`PixelStreamComponent` requests a session for the experience and renders it in an iframe. It fills its parent element, so give the parent a size. This example fetches an auth token from a route on your server, `/api/convai-token`, before it renders the component:

{% code title="src/App.tsx" %}
```tsx
import { useEffect, useRef, useState } from 'react';
import {
  PixelStreamComponent,
  type PixelStreamComponentHandles,
} from '@convai/experience-embed';

export default function App() {
  const streamRef = useRef<PixelStreamComponentHandles>(null);
  const [token, setToken] = useState<string>();

  useEffect(() => {
    fetch('/api/convai-token')
      .then((response) => response.json())
      .then((body: { token: string }) => setToken(body.token));
  }, []);

  if (!token) return <p>Loading…</p>;

  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <PixelStreamComponent
        ref={streamRef}
        expId="YOUR_EXPERIENCE_ID"
        authToken={token}
        onIframeLoaded={() => console.log('Experience loaded')}
      />
    </div>
  );
}
```
{% endcode %}

If Convai has allowlisted your domain instead, leave out `authToken` and render the component straight away.

{% hint style="warning" %}
Fetch the token before you render the component, and keep it for the whole session. A new `authToken`, `expId`, or `endUserId` value requests a new session and reloads the experience.
{% endhint %}

## Start the experience

The component first shows a **Click to start your experience** screen, and starts the experience when the user clicks it. To show your own screen, pass it as `InitialScreen`. A custom screen does not start the experience on its own, so call `initializeExperience()` from it:

```tsx
<PixelStreamComponent
  ref={streamRef}
  expId="YOUR_EXPERIENCE_ID"
  authToken={token}
  InitialScreen={
    <button onClick={() => streamRef.current?.initializeExperience()}>
      Start the tour
    </button>
  }
  LoadingScreenComponent={<p>Preparing the experience…</p>}
/>
```

`LoadingScreenComponent` covers the iframe until the stream page reports that it has finished loading.

## Control the experience

Call the methods on the ref once `onIframeLoaded` has fired. A method called before then sends nothing:

```tsx
await streamRef.current?.enableCamera();
streamRef.current?.disableCharacterAudio();
streamRef.current?.sendMessageToCharacter('Where is the fire exit?');
streamRef.current?.muteMicrophone();
streamRef.current?.setChatStyle({ backgroundOpacity: 0.3 });
```

To follow what happens inside the experience, pass callbacks such as `onCharacterMessage` and `onMicStatus` as props. The [Pixel Streaming Embed API reference](api-reference.md) lists every method, callback, and payload.

## Verify the embed

Load the page and click the start screen.

{% hint style="success" %}
The experience replaces the start screen, and the browser console logs `Experience loaded`.
{% endhint %}

## Troubleshooting

### The embed asks you to contact Convai

**Symptom:** The embed shows `Please contact convai to get <origin> whitelisted!` instead of the start screen.

**Cause:** The embed has no `authToken`, and the page's domain is not on your account's allowlist, or the experience ID is wrong.

**Fix:** Pass an auth token, or ask Convai to allowlist the domain. Check the experience ID.

**Verify:** Reload the page. The start screen appears.

### The embed reports an invalid auth token

**Symptom:** The embed shows `This experience couldn't start: the Convai auth token is invalid or has expired.`

**Cause:** Convai rejected the token passed as `authToken`.

**Fix:** Mint a new token on your server and render the component again with it.

**Verify:** Reload the page. The start screen appears.

### A custom start screen does nothing when clicked

**Symptom:** The page shows your `InitialScreen`, and clicking it does not start the experience.

**Cause:** A custom `InitialScreen` replaces the default screen and its click handler.

**Fix:** Call `initializeExperience()` on the ref from your screen.

**Verify:** Clicking your screen shows the experience.

## Next steps

{% content-ref url="api-reference.md" %}
[Pixel Streaming Embed API reference](api-reference.md)
{% endcontent-ref %}
