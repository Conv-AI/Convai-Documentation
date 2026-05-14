---
description: >-
  Control how Vision frames are delivered to the backend. Covers publish
  policies, frame rate and bitrate configuration, and manual publishing control.
---

# Publishing & Policies

## Controlling How Vision Frames Are Published

`ConvaiVisionPublisher` is the component that bridges the frame source and the Convai backend. It manages the WebRTC video track lifecycle — starting, maintaining, and stopping the stream in response to room connection events — and exposes a set of policies and overrides for tuning the transport characteristics. This page explains every Inspector field, describes each publish policy, and shows how to take manual control of publishing via script.

### ConvaiVisionPublisher Inspector Reference

#### Frame Source

<table><thead><tr><th width="142.5">Field</th><th width="138.50006103515625">Type</th><th width="142">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Frame Source Component</strong></td><td><code>MonoBehaviour</code></td><td><em>(auto-resolved)</em></td><td>The <code>IVisionFrameSource</code> implementation to publish. Leave blank to auto-discover the first available frame source in the scene. If multiple frame sources exist, assign this explicitly.</td></tr></tbody></table>

#### Publish Policy

<table><thead><tr><th width="139.5">Field</th><th width="189.00006103515625">Type</th><th width="147">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Publish Policy</strong></td><td><code>VisionPublishPolicy</code></td><td><code>AutoCompatible</code></td><td>Controls the client-side frame rate and bitrate. See the policy table below.</td></tr></tbody></table>

#### Video Settings

<table><thead><tr><th width="245.99993896484375">Field</th><th width="108.50006103515625">Type</th><th width="145">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Video Track Name</strong></td><td><code>string</code></td><td><code>"unity-scene"</code></td><td>The name of the WebRTC video track published to the room. The Convai backend uses this name to associate the video stream with the session. Change it only if you have a specific multi-track configuration.</td></tr><tr><td><strong>Publish Frame Rate Override</strong></td><td><code>int</code> (0–30)</td><td><code>0</code></td><td>Overrides the frame rate specified by the publish policy. <code>0</code> means "use the policy default".</td></tr><tr><td><strong>Publish Bitrate Override</strong></td><td><code>int</code></td><td><code>0</code></td><td>Overrides the maximum bitrate (bits per second) specified by the publish policy. <code>0</code> means "use the policy default".</td></tr></tbody></table>

***

### Publish Policy Comparison

`VisionPublishPolicy` is a client-side transport setting. It controls how aggressively frames are sampled and how much bandwidth is allocated. It does **not** determine which AI model or vision provider processes the stream on the backend.

<table><thead><tr><th width="182.5">Policy</th><th width="84.99993896484375">Value</th><th width="90.00006103515625">Frame rate</th><th width="134.5">Max bitrate</th><th>Recommended for</th></tr></thead><tbody><tr><td><code>AutoCompatible</code></td><td><code>0</code></td><td>10 fps</td><td>750 000 bps</td><td>General use — a balanced default that works across most backend configurations</td></tr><tr><td><code>HighResponsiveness</code></td><td><code>1</code></td><td>15 fps</td><td>1 000 000 bps</td><td>Live multimodal interactions where the character must react quickly to visual changes</td></tr><tr><td><code>LowOverhead</code></td><td><code>2</code></td><td>5 fps</td><td>350 000 bps</td><td>High-volume deployments, cost-sensitive sessions, or scenarios where snapshots are more important than motion</td></tr><tr><td><code>Manual</code></td><td><code>3</code></td><td>—</td><td>—</td><td>Explicit control over when publishing starts and stops; uses <code>AutoCompatible</code> rates when enabled</td></tr></tbody></table>

{% hint style="warning" %}
`VisionPublishPolicy` describes only the **client-side transport** — frame rate and bitrate sent over the network. It does not expose or control the backend AI model, vision provider, or processing latency. Do not use it as a proxy for backend behaviour.
{% endhint %}

***

### Frame Rate and Bitrate Overrides

When you need a specific value that falls between policies, use the override fields:

* **Publish Frame Rate Override** accepts values from `1` to `30`. Setting `0` restores the policy default.
* **Publish Bitrate Override** accepts any positive integer in bits per second. Setting `0` restores the policy default.

Example: `AutoCompatible` policy with a 12 fps override produces 12 fps at 750 000 bps.

{% hint style="info" %}
On WebGL, the frame rate is clamped to a maximum of **15 fps** regardless of policy or override. This is a platform constraint imposed by `canvas.captureStream()`.
{% endhint %}

***

### Auto-Publish Lifecycle

By default (any policy except `Manual`) publishing follows the room connection:

1. Room connects with `Connection Type = Video` → publishing starts automatically.
2. Room disconnects or the module stops → publishing stops and the video track is unpublished.
3. The component is disabled → publishing stops.
4. The component is re-enabled while the room is connected → publishing resumes.

You do not need to call any method to trigger this behaviour.

***

### Manual Policy

Set **Publish Policy** to `Manual` when you want explicit control — for example, to start publishing only when a user action occurs, or to pause the stream between training modules.

#### Starting and stopping manually

```csharp
using Convai.Modules.Vision;

ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();

// Begin publishing (uses AutoCompatible rates)
publisher.EnablePublishing(true);

// Stop publishing without disconnecting the room
publisher.EnablePublishing(false);
```

#### Switching policies at runtime

```csharp
// Switch to HighResponsiveness mid-session
publisher.SetPublishPolicy(VisionPublishPolicy.HighResponsiveness);
```

`SetPublishPolicy` takes effect immediately. If publishing is active, the current track is unpublished and a new one is started with the updated profile.

***

### WebGL Platform Notes

{% hint style="info" %}
On WebGL the `ConvaiVisionPublisher` captures the visible Unity browser canvas via `canvas.captureStream()` instead of reading from a frame source component. You do not need to add a frame source component to your scene for WebGL builds.

Publish policy selection still applies — use `LowOverhead` for performance-sensitive WebGL deployments. Frame rate is capped at 15 fps on all WebGL builds regardless of the policy or override value.
{% endhint %}

***

## Conclusion

`ConvaiVisionPublisher` manages the full video track lifecycle — it starts publishing when the room connects, stops when it disconnects, and exposes a policy system for controlling frame rate and bandwidth. With publishing configured, add [Debug Preview](debug-preview.md) to verify the stream visually before deploying. For the full scripting API, see [Advanced Topics](advanced-topics.md).
