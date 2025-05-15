---
icon: building
---

# On Premise Deployment

Customising Service URLs (for On-Premise or Self-Hosted Deployments)

By default, the `@convai/experience-embed` library connects to Convai’s hosted backend services and virtual machines. However, for **on-premise development**, or enterprise setups, you may want to route traffic through your own backend and virtual machines.

To support this, you can override the default service URLs using the `serviceUrls` prop (React) or option (Vanilla/TS/CDN).

#### Available Service URL Overrides

| Key               | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| `sessionFetch`    | URL to fetch session data for the experience               |
| `pixelStreamBase` | Base URL where the Unreal Pixel Streaming server is hosted |

#### React Example

```tsx
<PixelStreamComponent
  expId="your-experiment-id"
  InitialScreen={<div>Loading...</div>}
  serviceUrls={{
    sessionFetch: 'https://your-backend.example.com/api/session',
    pixelStreamBase: 'https://your-streaming-server.example.com',
  }}
/>
```

#### Vanilla JS Example

```ts
const pixelStream = new PixelStreamClient({
  container: document.getElementById('pixel-stream-container'),
  expId: 'your-experiment-id',
  serviceUrls: {
    sessionFetch: 'https://your-backend.example.com/api/session',
    pixelStreamBase: 'https://your-streaming-server.example.com',
  }
});
```

#### When to Use This

* You're running **Pixel Streaming servers locally** or on a **private cloud**.
* You want full control over **session management and security**.
* You are integrating the experience into a **larger enterprise application** with custom networking.

This flexibility allows the SDK to be integrated into diverse environments without requiring changes to the core library.
