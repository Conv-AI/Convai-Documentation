---
description: >-
  Integrate Convai's Pixel Streaming into your web app using the UMD build
  directly from a CDN
icon: js
---

# CDN (UMD Script)

{% hint style="info" %}
Pass an `authToken` minted on your server to run the embed on any origin, including `localhost`, without whitelisting your domain. See [Authorize embeds with an auth token](authorize-embeds-with-an-auth-token.md).
{% endhint %}

```html
<script src="https://unpkg.com/@convai/experience-embed/dist/core/convai-embed.umd.js"></script>
```

```html
<!-- index.html -->
<div id="pixel-stream-container" style="width: 100%; height: 600px;"></div>
<script src="https://unpkg.com/@convai/experience-embed/dist/core/convai-embed.umd.js"></script>
<script>
  const container = document.getElementById('pixel-stream-container');

  const pixelStream = new window.PixelStreamClient({
    container: container,
    expId: 'your-experience-id',
  });

  pixelStream.enableCamera();
</script>
```
