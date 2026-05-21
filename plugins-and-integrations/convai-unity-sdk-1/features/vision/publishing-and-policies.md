# Publishing & Policies

### Publishing & Policies

`ConvaiVisionPublisher` manages the WebRTC video track that carries the camera feed from Unity to Convai. Once a frame source is in the `Ready` state and `ConvaiRoomManager` is connected with **Connection Type** set to **Video**, the publisher begins streaming automatically under the selected policy.

***

### Inspector Reference

| Field                           | Type                  | Default             | Description                                                                                                                                                                |
| ------------------------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frame Source Component**      | `MonoBehaviour`       | _(auto-discovered)_ | The `IVisionFrameSource` to publish. Leave blank to auto-discover from the same GameObject, children, or scene. Assign explicitly when multiple frame sources are present. |
| **Publish Policy**              | `VisionPublishPolicy` | `AutoCompatible`    | Controls the client-side frame rate and bitrate budget. See [Publish Policies](publishing-and-policies.md#publish-policies) below.                                         |
| **Video Track Name**            | `string`              | `"unity-scene"`     | The name of the WebRTC track as it appears in the LiveKit room. Change only if your backend routing requires a specific name.                                              |
| **Publish Frame Rate Override** | `int` (0–30)          | `0`                 | Per-instance frame rate cap in fps. `0` uses the selected policy default.                                                                                                  |
| **Publish Bitrate Override**    | `int`                 | `0`                 | Per-instance maximum bitrate in bits per second. `0` uses the selected policy default.                                                                                     |

{% hint style="info" %}
On WebGL, `ConvaiVisionPublisher` ignores the assigned **Frame Source Component** and publishes the visible browser canvas via `canvas.captureStream()` instead. All other inspector fields still apply.
{% endhint %}

***

### Publish Policies

A publish policy is a client-side transport budget. It controls how many frames per second are sent and the maximum bitrate allocated to the video track. It does not select or configure any AI model or backend vision provider.

#### Policy Values

| Policy               | FPS      | Max bitrate | When to use                                                                                                                                                    |
| -------------------- | -------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AutoCompatible`     | 10       | 750 kbps    | Default. Balanced budget compatible with the current backend processing rate. Use this unless you have a specific reason to change it.                         |
| `HighResponsiveness` | 15       | 1 000 kbps  | Scenes where faster visual updates improve AI response quality (fast-moving objects, gesture recognition). Higher network cost.                                |
| `LowOverhead`        | 5        | 350 kbps    | High-volume deployments, mobile devices with limited bandwidth, or scenes where the visual context changes slowly.                                             |
| `Manual`             | _(none)_ | _(none)_    | Publishing does not start automatically on room connect. Call `EnablePublishing(true)` from a script to start. Use for session-gated or trigger-based capture. |

{% hint style="info" %}
On WebGL, the frame rate is clamped to a maximum of 15 fps regardless of the selected policy. The bitrate is unchanged.
{% endhint %}

#### Overriding Frame Rate or Bitrate

Set **Publish Frame Rate Override** or **Publish Bitrate Override** in the Inspector to override the policy defaults for a specific GameObject without changing the policy. A value of `0` means "use the policy default".

```csharp
// Runtime override via script
ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();
publisher.publishFrameRateOverride = 12;
publisher.publishBitrateOverride = 600_000;
```

***

### Switching Policy at Runtime

Call `SetPublishPolicy` to change the transport budget while a session is running. The change takes effect on the next published frame.

```csharp
ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();

// Switch to low overhead for a bandwidth-constrained user
publisher.SetPublishPolicy(VisionPublishPolicy.LowOverhead);

// Switch back to balanced
publisher.SetPublishPolicy(VisionPublishPolicy.AutoCompatible);
```

***

### Pausing and Resuming with Manual Policy

`Manual` policy is useful when visual context is only relevant during specific moments — for example, when the player is looking at a particular object.

```csharp
ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();

// Start publishing when the player focuses on an object
void OnPlayerLookAt(GameObject target)
{
    publisher.EnablePublishing(true);
}

// Stop publishing when focus is lost
void OnPlayerLookAway()
{
    publisher.EnablePublishing(false);
}
```

{% hint style="warning" %}
`EnablePublishing` only has an effect when **Publish Policy** is `Manual`. For other policies, publishing starts and stops with the room connection. Use `SetPublishPolicy(VisionPublishPolicy.Manual)` before calling `EnablePublishing` if you need on-demand control.
{% endhint %}

***

### Checking Publish State

Read `IsPublishing` to confirm a video track is actively being sent.

```csharp
ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();

if (publisher.IsPublishing)
    Debug.Log($"Publishing on track '{publisher.VideoTrackName}'");
else
    Debug.Log("Not publishing — check Connection Type and frame source state.");
```

`IsPublishing` becomes `true` after:

1. `ConvaiRoomManager` connects with **Connection Type** set to **Video**.
2. The frame source reaches the `Ready` state.
3. The coordinator successfully opens the WebRTC video track.

***

### Auto-Publish Behaviour

For `AutoCompatible`, `HighResponsiveness`, and `LowOverhead`, publishing begins automatically when the room connects. The publisher waits for the frame source to signal readiness before opening the track — no script is required.

The sequence on room connect:

1. `ConvaiRoomManager` establishes a Video connection.
2. `ConvaiVisionPublisher` starts and resolves the frame source.
3. The frame source starts capture and signals `Ready`.
4. The coordinator opens a WebRTC video track named `videoTrackName`.
5. `IsPublishing` becomes `true` and the `VideoTrackPublished` domain event fires.

***

### WebGL

On WebGL, no frame source component is required or used. `ConvaiVisionPublisher` captures the visible browser canvas automatically via `canvas.captureStream()` as soon as the room connects.

{% hint style="danger" %}
**WebGL: HTTPS required.** Browsers block `canvas.captureStream()` on non-HTTPS origins. The only exception is `http://localhost`. Deploy your WebGL build to an HTTPS host before testing Vision in production.
{% endhint %}

WebGL-specific behaviour:

| Behaviour    | Detail                                                            |
| ------------ | ----------------------------------------------------------------- |
| Frame source | None required. Assigned frame source is ignored on WebGL.         |
| Frame rate   | Clamped to 15 fps regardless of selected policy.                  |
| Bitrate      | Policy bitrate applies (no additional clamping).                  |
| HTTPS        | Required in production. `http://localhost` is the only exception. |

***

### Next Steps

With publishing configured, use [Scripting API](/broken/pages/66ae09f082490e6e22eeabcf09762855075b37c0) to monitor publish state and react to domain events from scripts, or add [Debug Preview](/broken/pages/4e429711446d44660df42fc75a9c4e132a861ea9) to verify the live feed in the Editor. If publishing is not starting, see [Troubleshooting & Diagnostics](/broken/pages/ce72ed1f95d78e73f4af5a61fbeaeb221e86e25d).
