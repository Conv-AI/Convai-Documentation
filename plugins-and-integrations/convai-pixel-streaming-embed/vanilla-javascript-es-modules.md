---
description: >-
  Use Convai's Pixel Streaming client directly in browser-based JavaScript apps
  with native ES module support.
icon: js
---

# Vanilla JavaScript (ES Modules)

```html
<!-- index.html -->
<div id="pixel-stream-container" style="width: 100%; height: 600px;"></div>
<script type="module">
  import { PixelStreamClient } from '/path/to/node_modules/@convai/experience-embed/dist/index.js';

  const container = document.getElementById('pixel-stream-container');
  const client = new PixelStreamClient({ container, expId: 'your-experience-id' });

  client.initializeExperience();
</script>
```

