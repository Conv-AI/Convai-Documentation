---
description: >-
  Integrate Convai's Pixel Streaming into your React JavaScript app using the
  @convai/experience-embed component.
icon: react
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/convai-pixel-streaming-embed/reactjs-javascript
---

# ReactJS (JavaScript)

```javascript
import React, { useRef } from 'react';
import { PixelStreamComponent } from '@convai/experience-embed';

function App() {
  const pixelStreamRef = useRef(null);

  const handleStart = async () => {
    await pixelStreamRef.current?.initializeExperience();
  };

  return (
    <>
      <PixelStreamComponent
        ref={pixelStreamRef}
        expId="your-experience-id"
        InitialScreen={<div>Loading...</div>}
      />
      <button onClick={handleStart}>Start Experience</button>
    </>
  );
}
```
