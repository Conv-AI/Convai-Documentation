---
description: >-
  Set up and integrate Convai's Pixel Streaming component in your React
  TypeScript app using @convai/experience-embed.
icon: react
---

# React Typescript

{% embed url="https://www.npmjs.com/package/@convai/experience-embed" %}

## Installation Instructions

To install `@convai/experience-embed` using your preferred package manager, use one of the following commands:

#### npm

```bash
npm install @convai/experience-embed
```

#### yarn

```bash
yarn add @convai/experience-embed
```

#### pnpm

```bash
pnpm add @convai
```

## Quick Start (React Ts)

### 1. Import the Component

```tsx
import { PixelStreamComponent } from '@convai/experience-embed';
```

***

### 2. Set Up a Ref to Access Methods

<pre class="language-tsx"><code class="lang-tsx"><strong>import { useRef } from 'react';
</strong>import { PixelStreamComponentHandles } from '@convai/experience-embed';

const pixelStreamRef = useRef&#x3C;PixelStreamComponentHandles>(null);
</code></pre>

### 3. Use the Component in JSX

```tsx
<PixelStreamComponent
  ref={pixelStreamRef}
  expId="your-experiment-id"
  InitialScreen={<div>Loading your experience...</div>}
/>
```

{% hint style="info" %}
`expId` is your unique experiment ID from Convai's dashboard.
{% endhint %}

### 4. Interact Using Available Methods

**Enable/Disable Camera**

```tsx
await pixelStreamRef.current?.enableCamera();
await pixelStreamRef.current?.disableCamera();
```

**Enable/Disable Character Audio**

```tsx
await pixelStreamRef.current?.enableCharacterAudio();
await pixelStreamRef.current?.disableCharacterAudio();
```

**Initialise the Experience**

```tsx
await pixelStreamRef.current?.initializeExperience();
```

### 5. Customise the Loading Screen (Optional)

```tsx
const CustomLoadingScreen = () => (
  <div style={{
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#000',
    color: '#fff',
  }}>
    <h2>Loading your experience...</h2>
  </div>
);
```

Usage:

```tsx
<PixelStreamComponent
  ref={pixelStreamRef}
  expId="your-experiment-id"
  InitialScreen={<CustomLoadingScreen />}
/>
```

## Full Example

```tsx
import React, { useRef } from 'react';
import {
  PixelStreamComponent,
  PixelStreamComponentHandles,
} from '@convai/experience-embed';

function App() {
  const pixelStreamRef = useRef<PixelStreamComponentHandles>(null);

  const handleEnableCamera = async () => {
    await pixelStreamRef.current?.enableCamera();
  };

  const handleDisableCamera = async () => {
    await pixelStreamRef.current?.disableCamera();
  };

  return (
    <div>
      <PixelStreamComponent
        ref={pixelStreamRef}
        expId="your-experiment-id"
        InitialScreen={<div>Loading your experience...</div>}
      />
      <button onClick={handleEnableCamera}>Enable Camera</button>
      <button onClick={handleDisableCamera}>Disable Camera</button>
    </div>
  );
}

export default App;
```
