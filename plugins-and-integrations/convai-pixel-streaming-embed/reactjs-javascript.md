---
description: >-
  Integrate Convai's Pixel Streaming into your React JavaScript app using the
  @convai/experience-embed component.
icon: react
---

# ReactJS (JavaScript)

{% hint style="info" %}
Pass an `authToken` minted on your server to run the embed on any origin, including `localhost`, without whitelisting your domain. See [Authorize embeds with an auth token](authorize-embeds-with-an-auth-token.md).
{% endhint %}

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
