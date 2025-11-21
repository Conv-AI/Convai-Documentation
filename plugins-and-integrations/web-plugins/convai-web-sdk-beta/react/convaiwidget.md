---
description: >-
  ConvaiWidget is an all-in-one interface for voice, text, video, and screen
  sharing.
---

# ConvaiWidget

## Props

```tsx
interface ConvaiWidgetProps {
  convaiClient: ConvaiClient;
  showVideo?: boolean;        
  showScreenShare?: boolean;
}
```

***

## Example

```tsx
<ConvaiWidget
  convaiClient={convaiClient}
  showVideo={true}
  showScreenShare={true}
/>
```

## Use This When:

* You want a complete, ready-made UI
* You want built-in audio/video controls
* You want to integrate quickly
