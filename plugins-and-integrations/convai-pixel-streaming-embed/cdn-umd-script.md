---
description: >-
  Integrate Convai's Pixel Streaming into your web app using the UMD build
  directly from a CDN
icon: js
---

# CDN (UMD Script)

```html
<script src="https://unpkg.com/@convai/experience-embed/dist/convai-embed.umd.js"></script>
```

```html
<!-- index.html -->
<div id="pixel-stream-container" style="width: 100%; height: 600px;"></div>
<script src="https://unpkg.com/@convai/experience-embed/dist/convai-embed.umd.js"></script>
<script>
  const container = document.getElementById('pixel-stream-container');

  const pixelStream = new window.PixelStreamClient({
    container: container,
    expId: 'your-experiment-id',
  });

  pixelStream.enableCamera();
</script>
```
