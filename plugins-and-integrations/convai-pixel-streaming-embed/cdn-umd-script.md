---
title: Embed an experience with a script tag
description: Load the Pixel Streaming Embed package from a CDN with a script tag and render a published experience in a plain HTML page, with no build step.
last_reviewed: "0.7.1"
icon: js
---

Render a published Convai Pixel Streaming experience in a plain HTML page by loading the package's UMD build from a CDN. Use this page when the site has no bundler. At the end, the page shows the experience's start screen.

## Prerequisites

- The experience ID of a published experience, and a way to authorize it: a server route that returns a Convai auth token, or a domain that Convai has allowlisted. See [Publish and authorize an experience](whitelisting-and-publishing-an-experience.md).
- A web server for the page, since the example fetches the token from a route on the same server.

## Add the script and the container

The UMD build is `dist/core/convai-embed.umd.js`. It is self-contained, and it defines one global, `PixelStreamCore`, whose `PixelStreamClient` property is the class that renders the experience. The client fills its container, so give the container a size:

{% code title="index.html" %}
```html
<!doctype html>
<html>
  <body>
    <div id="experience" style="width: 100%; height: 600px"></div>

    <script src="https://unpkg.com/@convai/experience-embed/dist/core/convai-embed.umd.js"></script>
    <script>
      fetch('/api/convai-token')
        .then((response) => response.json())
        .then((body) => {
          window.experience = new PixelStreamCore.PixelStreamClient({
            container: document.getElementById('experience'),
            expId: 'YOUR_EXPERIENCE_ID',
            authToken: body.token,
          });
        });
    </script>
  </body>
</html>
```
{% endcode %}

The example fetches an auth token from a route on your server, `/api/convai-token`. If Convai has allowlisted your domain instead, leave out `authToken` and create the client without fetching anything.

{% hint style="warning" %}
The URL above always loads the newest release. To stay on one release, add its version to the URL, for example `@convai/experience-embed@` followed by <code class="expression">space.vars.experience_embed_version</code>.
{% endhint %}

## Control the experience

The client shows a **Click to start your experience** screen and starts the experience when the user clicks it. Once the experience has loaded, call its methods from your own controls:

```html
<button onclick="experience.enableCamera()">Turn on camera</button>
<button onclick="experience.disableCharacterAudio()">Mute character</button>
<button onclick="experience.muteMicrophone()">Mute microphone</button>
```

The [Pixel Streaming Embed API reference](api-reference.md#pixelstreamclient-methods) lists every method, option, and callback.

## Verify the embed

Open the page through your web server.

{% hint style="success" %}
The container shows **Click to start your experience**, and clicking it shows the experience.
{% endhint %}

If the container shows `Please contact convai to get <origin> whitelisted!` or a message about the auth token, see [Troubleshooting](react-typescript.md#troubleshooting); the causes are the same.

## Next steps

{% content-ref url="vanilla-javascript-es-modules.md" %}
[Embed an experience with JavaScript modules](vanilla-javascript-es-modules.md)
{% endcontent-ref %}

{% content-ref url="api-reference.md" %}
[Pixel Streaming Embed API reference](api-reference.md)
{% endcontent-ref %}
