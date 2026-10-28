---
title: Publish policies
description: Reference for Vision publish policies, including FPS and bitrate budgets, runtime control methods, auto-publish behavior, and WebGL-specific behavior.
last_reviewed: "5.0.0-preview"
---

`ConvaiVisionPublisher` manages the WebRTC video track that carries the camera feed from Unity to Convai. A publish policy controls the client-side frame rate and bitrate budget; it does not configure any AI model or backend vision provider.

## Inspector reference

The Inspector contains **Frame Source**, **Publish Policy**, and **Live**. Validation can show **Frame Source Required** with **Auto-Find**, or **More Than One Frame Source Here**. Inspector Auto-Find can search parents; runtime discovery is limited as described below.

### Frame source

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| **Source** | `MonoBehaviour` | _(auto-discovered)_ | The `IVisionFrameSource` to publish. Leave blank to auto-discover from the same GameObject or its children. On WebGL a local page-canvas source is preferred; otherwise a same-object camera source precedes other sources. Assign explicitly when multiple frame sources are present. |
| **Track Name** | `string` | `"unity-scene"` | The name of the WebRTC track as it appears in the LiveKit room. Match the room's resolved **Video Track Name**. Its profile or inline value wins, otherwise it uses a child publisher's name, then `unity-scene`. |

### Publish policy

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
| `Manual` | `10` once enabled | `750` kbps once enabled | Publishing does not start automatically on room connect. Call `EnablePublishing(true)` from a script to start. Use for session-gated or trigger-based capture. |

To override the policy defaults for a specific instance without changing the policy, set **Max Publish FPS** or **Max Bitrate (bps)** in the Inspector. A value of `0` means "use the policy default".

Configure caps in the Inspector before runtime initialization. The public `publishFrameRateOverride` and `publishBitrateOverride` fields are read during setup, module start, and Editor validation; assigning them on a running publisher is not an immediate runtime control. `SetPublishPolicy` reuses the coordinator's cached caps.

## Control publishing from scripts

**Switch policy at runtime**

Call `SetPublishPolicy` to change the transport budget while a session is running. A changed policy restarts an active or pending publication by unpublishing and publishing again. Switching to Manual stops automatic publication unless an explicit EnablePublishing choice already overrides it.

```csharp
ConvaiVisionPublisher publisher = GetComponent<ConvaiVisionPublisher>();

// Switch to low overhead for a bandwidth-constrained user
publisher.SetPublishPolicy(VisionPublishPolicy.LowOverhead);

// Switch back to balanced
publisher.SetPublishPolicy(VisionPublishPolicy.AutoCompatible);
```

**Pause and resume with Manual policy**

`Manual` policy is useful when visual context is only relevant during specific moments — for example, when the player is looking at a particular object.

`EnablePublishing` takes effect under every policy, not only `Manual`. Under an auto-publishing policy, publishing otherwise starts and stops with the room connection, and `EnablePublishing(false)` stops it anyway.

Calling it once is a decision for this publisher component's lifetime, including reconnects: from that point on your explicit value wins, and the policy no longer decides whether publishing runs. Switching to another policy afterwards changes the frame rate and bitrate, but not the on-or-off state. Use `Manual` when you want on-demand control to be the visible intent in the Inspector.

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

`IsPublishing` becomes `true` after the room connects with effective connection type Video, the frame source reaches the `Ready` state, and the coordinator successfully opens the WebRTC video track.

## Auto-publish behavior

For `AutoCompatible`, `HighResponsiveness`, and `LowOverhead`, publishing begins automatically when the room connects. The publisher waits for the frame source to signal readiness before opening the track — no script is required.

The sequence on room connect:

1. `ConvaiRoomManager` establishes a Video connection.
2. `ConvaiVisionPublisher` starts and resolves the frame source.
3. The frame source starts capture and signals `Ready`.
4. The coordinator opens a WebRTC video track named `videoTrackName`.
5. `IsPublishing` becomes `true` and the `VideoTrackPublished` domain event fires.

## Raw RenderTexture bypass orientation

`ConvaiVisionPublisher` normally reads frames through an `IVisionFrameSource` — `CameraVisionFrameSource`, `WebcamVisionFrameSource`, `QuestVisionFrameSource`, or a custom implementation. The interface contract requires every `IVisionFrameSource` to expose a `RenderTexture` that is already top-down (Y-flipped from Unity's default bottom-up orientation), because that is what the WebRTC video track requires.

Advanced setups that bypass every `IVisionFrameSource` and assign a raw `RenderTexture` directly to the LiveKit `TextureVideoSource` must supply a texture that is already top-down: use `Graphics.Blit` with `scale: Vector2(1, -1)` and `offset: Vector2(0, 1)`, or route the frame through a Convai `IVisionFrameSource` implementation instead. See [Custom frame sources](custom-frame-sources.md) for the `Graphics.Blit` pattern.

## WebGL

**WebGL Publishes** selects **Frame Source** (default) or **Game View**. A frame source texture is copied to a hidden page canvas; Game View captures the rendered game with its UI. With no source, the game view is the fallback. An `IVisionPageCanvasSource` always uses its own page canvas, even when Game View is selected.

The policy default is capped at `15` fps on WebGL; a positive **Max Publish FPS** override is used as configured. Policy bitrate still applies. See [WebGL vision](webgl.md) for selection and browser verification.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture Convai Vision Publisher with Frame Source, WebGL Publishes, Track Name, Publish Policy, Max Publish FPS, and Max Bitrate visible with the WebGL build target active.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-vision-publisher.png" alt="Convai Vision Publisher with Frame Source, WebGL Publishes, Track Name, Publish Policy, Max Publish FPS, and Max Bitrate visible with the WebGL build target active"><figcaption><p>TODO: Replace with screenshot showing Convai Vision Publisher with Frame Source, WebGL Publishes, Track Name, Publish Policy, Max Publish FPS, and Max Bitrate visible with the WebGL build target active.</p></figcaption></figure>

## Next steps

{% content-ref url="scripting-api.md" %}
[Vision scripting API](scripting-api.md)
{% endcontent-ref %}

{% content-ref url="debug-preview.md" %}
[Vision debug preview](debug-preview.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot vision](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
