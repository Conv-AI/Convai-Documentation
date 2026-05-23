---
title: Publish policies
description: Reference for Vision publish policies, including FPS and bitrate budgets, runtime control methods, auto-publish behavior, and WebGL-specific behavior.
---

`ConvaiVisionPublisher` manages the WebRTC video track that carries the camera feed from Unity to Convai. A publish policy controls the client-side frame rate and bitrate budget; it does not configure any AI model or backend vision provider.

## Inspector reference

The Inspector is divided into two collapsible sections: **FRAME SOURCE** and **PUBLISH POLICY**.

#### FRAME SOURCE

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| **Source** | `MonoBehaviour` | _(auto-discovered)_ | The `IVisionFrameSource` to publish. Leave blank to auto-discover from the same GameObject, children, or scene. Assign explicitly when multiple frame sources are present. |
| **Track Name** | `string` | `"unity-scene"` | The name of the WebRTC track as it appears in the LiveKit room. Change only if your backend routing requires a specific name. |

#### PUBLISH POLICY

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| **Mode** | `VisionPublishPolicy` | `AutoCompatible` | Controls the client-side frame rate and bitrate budget. See [Publish policies](#publish-policies) below. |
| **Max Publish FPS** | `int` (0–30) | `0` | Per-instance frame rate ceiling in fps. `0` uses the selected policy default. |
| **Max Bitrate (bps)** | `int` | `0` | Per-instance maximum bitrate in bits per second. `0` uses the selected policy default. |

## Publish policies

A publish policy is a client-side transport budget. It controls how many frames per second are sent and the maximum bitrate allocated to the video track.

| Policy | FPS | Max bitrate | When to use |
| --- | --- | --- | --- |
| `AutoCompatible` | 10 | 750 kbps | Default. Balanced budget compatible with the current backend processing rate. Use this unless you have a specific reason to change it. |
| `HighResponsiveness` | 15 | 1 000 kbps | Scenes where faster visual updates improve AI response quality (fast-moving objects, gesture recognition). Higher network cost. |
| `LowOverhead` | 5 | 350 kbps | High-volume deployments, mobile devices with limited bandwidth, or scenes where the visual context changes slowly. |
| `Manual` | _(none)_ | _(none)_ | Publishing does not start automatically on room connect. Call `EnablePublishing(true)` from a script to start. Use for session-gated or trigger-based capture. |

To override the policy defaults for a specific instance without changing the policy, set **Max Publish FPS** or **Max Bitrate (bps)** in the Inspector. A value of `0` means "use the policy default".

```csharp
// Runtime override via script
ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();
publisher.publishFrameRateOverride = 12;
publisher.publishBitrateOverride = 600_000;
```

## Control publishing from scripts

**Switch policy at runtime**

Call `SetPublishPolicy` to change the transport budget while a session is running. The change takes effect on the next published frame.

```csharp
ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();

// Switch to low overhead for a bandwidth-constrained user
publisher.SetPublishPolicy(VisionPublishPolicy.LowOverhead);

// Switch back to balanced
publisher.SetPublishPolicy(VisionPublishPolicy.AutoCompatible);
```

**Pause and resume with Manual policy**

`Manual` policy is useful when visual context is only relevant during specific moments — for example, when the player is looking at a particular object.

{% hint style="warning" %}
`EnablePublishing` only has an effect when **Mode** is `Manual`. For other policies, publishing starts and stops with the room connection. Call `SetPublishPolicy(VisionPublishPolicy.Manual)` before calling `EnablePublishing` if you need on-demand control.
{% endhint %}

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

**Check publish state**

Read `IsPublishing` to confirm a video track is actively being sent.

```csharp
ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();

if (publisher.IsPublishing)
    Debug.Log($"Publishing on track '{publisher.VideoTrackName}'");
else
    Debug.Log("Not publishing — check Connection Type and frame source state.");
```

`IsPublishing` becomes `true` after `ConvaiRoomManager` connects with **Connection Type** set to **Video**, the frame source reaches the `Ready` state, and the coordinator successfully opens the WebRTC video track.

## Auto-publish behavior

For `AutoCompatible`, `HighResponsiveness`, and `LowOverhead`, publishing begins automatically when the room connects. The publisher waits for the frame source to signal readiness before opening the track — no script is required.

The sequence on room connect:

1. `ConvaiRoomManager` establishes a Video connection.
2. `ConvaiVisionPublisher` starts and resolves the frame source.
3. The frame source starts capture and signals `Ready`.
4. The coordinator opens a WebRTC video track named `videoTrackName`.
5. `IsPublishing` becomes `true` and the `VideoTrackPublished` domain event fires.

## WebGL

On WebGL, no frame source component is required or used. `ConvaiVisionPublisher` captures the visible browser canvas automatically via `canvas.captureStream()` as soon as the room connects. The assigned **Source** field is ignored.

{% hint style="danger" %}
**WebGL: HTTPS required.** Browsers block `canvas.captureStream()` on non-HTTPS origins. The only exception is `http://localhost`. Deploy your WebGL build to an HTTPS host before testing Vision in production.
{% endhint %}

| Behavior | Detail |
| --- | --- |
| Frame source | None required. Assigned frame source is ignored on WebGL. |
| Frame rate | Clamped to 15 fps regardless of selected policy. |
| Bitrate | Policy bitrate applies (no additional clamping). |
| HTTPS | Required in production. `http://localhost` is the only exception. |

## Next steps

{% content-ref url="scripting-api.md" %}
[Vision scripting API](scripting-api.md)
{% endcontent-ref %}

{% content-ref url="debug-preview.md" %}
[Vision debug preview](debug-preview.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Vision troubleshooting](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
