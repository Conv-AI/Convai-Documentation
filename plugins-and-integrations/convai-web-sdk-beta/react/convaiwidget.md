---
description: >-
  ConvaiWidget is an all-in-one interface for voice, text, video, and screen
  sharing.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/web-plugins/convai-web-sdk-beta/react/convaiwidget
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
