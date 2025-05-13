---
description: https://www.npmjs.com/package/@convai/experience-embed
---

# Using the NPM Package

### Installation

```bash
npm install @convai/experience-embed
```

#### React (TypeScript) Example

```jsx
import React, { useRef } from 'react';
import {
  PixelStreamComponent,
  PixelStreamComponentHandles
} from '@convai/experience-embed';

function App() {
  const streamRef = useRef<PixelStreamComponentHandles>(null);

  const handleEnableCamera = async () => {
    if (streamRef.current) {
      const success = await streamRef.current.enableCamera();
      console.log('Camera enabled:', success);
    }
  };

  return (
    <div style={{ width: '800px', height: '600px' }}>
      <PixelStreamComponent ref={streamRef} expId="your_experience_id_here" />
      <button onClick={handleEnableCamera}>Enable Camera</button>
    </div>
  );
}
```

#### React (JavaScript) Example

```javascript
import React, { useRef } from 'react';
import { PixelStreamComponent } from '@convai/experience-embed';

function App() {
  const streamRef = useRef(null);

  const handleEnableCamera = async () => {
    if (streamRef.current) {
      const success = await streamRef.current.enableCamera();
      console.log('Camera enabled:', success);
    }
  };

  return (
    <div style={{ width: '800px', height: '600px' }}>
      <PixelStreamComponent ref={streamRef} expId="your-experience-id" />
      <button onClick={handleEnableCamera}>Enable Camera</button>
    </div>
  );
}
```

#### Vanilla JS via CDN

```javascript
<!DOCTYPE html>
<html>
  <head>
    <title>Pixel Streaming</title>
    <script src="https://www.unpkg.com/@convai/experience-embed/dist/convai-embed.umd.js"></script>
  </head>
  <body>
    <div id="pixel-stream-container" style="width: 100%; height: 600px;"></div>

    <script>
      const container = document.getElementById('pixel-stream-container');
      const pixelStream = new PixelStreamClient.default({
        container,
        expId: 'your-experience-id',
      });

      pixelStream.enableCamera().then(success => {
        console.log('Camera enabled:', success);
      });
    </script>
  </body>
</html>
```

#### API Summary

**React Component Props**

| Prop  | Type   | Required | Description               |
| ----- | ------ | -------- | ------------------------- |
| expId | string | ✅ Yes    | Experience ID from Convai |

**React Ref Methods**

| Method                  | Returns | Description             |
| ----------------------- | ------- | ----------------------- |
| enableCamera()          | Promise | Turns on user camera    |
| disableCamera()         | Promise | Turns off user camera   |
| enableCharacterAudio()  | void    | Unmutes character audio |
| disableCharacterAudio() | void    | Mutes character audio   |

**Vanilla JS PixelStreamClient Options**

| Option    | Type        | Required | Description               |
| --------- | ----------- | -------- | ------------------------- |
| container | HTMLElement | ✅ Yes    | DOM element for embedding |
| expId     | string      | ✅ Yes    | Experience ID             |
