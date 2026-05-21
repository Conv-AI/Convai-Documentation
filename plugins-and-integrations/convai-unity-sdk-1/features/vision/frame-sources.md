# Frame Sources

### Choosing a Frame Source

A frame source is the component responsible for capturing images and making them available to the publisher as a Y-flipped `RenderTexture`. The Convai SDK ships three built-in frame sources — one for Unity scene cameras, one for physical webcams, and one for the Meta Quest passthrough camera.

| Frame source              | Best for                                                                             | Platforms                                |
| ------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------- |
| `CameraVisionFrameSource` | Streaming any Unity scene camera — main camera, security camera, overhead view       | PC, Mac, Android, iOS, console           |
| `WebcamVisionFrameSource` | Streaming a physical camera device attached to the player's machine or mobile device | PC, Mac, Android, iOS                    |
| `QuestVisionFrameSource`  | Streaming the real-world passthrough feed on a Meta Quest 3 or 3S headset            | Meta Quest 3 / 3S (requires Meta XR SDK) |

Add a frame source via **Add Component** and type the class name, or navigate the component menu under **Convai → Vision**.

***

### CameraVisionFrameSource

`CameraVisionFrameSource` captures a Unity `Camera`'s output into a `RenderTexture` and provides it to the publisher on every frame. It automatically selects the correct capture backend for the active render pipeline (Built-in or SRP/URP) when **Camera Capture Mode** is set to `Auto`.

**Component menu path:** `Convai/Vision/Camera Vision Frame Source`

#### Inspector Reference

**Capture Settings**

| Field                   | Type                | Default    | Description                                                                                              |
| ----------------------- | ------------------- | ---------- | -------------------------------------------------------------------------------------------------------- |
| **Capture Preset**      | `CapturePreset`     | `Balanced` | Selects a preconfigured resolution and frame-rate combination. Set to `Custom` to enter values manually. |
| **Capture Width**       | `int`               | —          | Output width in pixels. Active only when preset is `Custom`.                                             |
| **Capture Height**      | `int`               | —          | Output height in pixels. Active only when preset is `Custom`.                                            |
| **Target Fps**          | `int`               | —          | Target capture frame rate. Active only when preset is `Custom`.                                          |
| **Camera Capture Mode** | `CameraCaptureMode` | `Auto`     | Selects the render-pipeline capture strategy. Leave at `Auto` unless the feed is black.                  |

**Camera**

| Field             | Type     | Default           | Description                                                                 |
| ----------------- | -------- | ----------------- | --------------------------------------------------------------------------- |
| **Target Camera** | `Camera` | _(auto-resolved)_ | The camera to capture. If left blank, resolved to `Camera.main` at runtime. |

**Debug**

| Field                                    | Type     | Default    | Description                                                                                                                                                   |
| ---------------------------------------- | -------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Source Id**                            | `string` | `"camera"` | Identifier used in domain events and multi-source scenarios.                                                                                                  |
| **Enable Diagnostic Frame Health Probe** | `bool`   | `false`    | Performs a synchronous per-frame pixel readback to validate frame content. Use only when diagnosing black-frame issues; incurs GPU readback cost every frame. |

{% hint style="warning" %}
If **Target Camera** is blank and no camera in the scene is tagged **MainCamera**, the frame source enters `Failed` state at runtime with `ErrorKind = InvalidConfiguration`. Always assign a camera explicitly or ensure one camera has the **MainCamera** tag.
{% endhint %}

#### Capture Preset Values

| Preset        | Width            | Height           | FPS              | Use case                                                               |
| ------------- | ---------------- | ---------------- | ---------------- | ---------------------------------------------------------------------- |
| `LowOverhead` | 640              | 480              | 10               | High-volume deployments, mobile, or bandwidth-constrained environments |
| `Balanced`    | 1280             | 720              | 15               | General purpose — default for most scenarios                           |
| `HighDetail`  | 1920             | 1080             | 30               | Scenes where fine visual detail is critical to AI comprehension        |
| `Custom`      | _(set manually)_ | _(set manually)_ | _(set manually)_ | Full control over dimensions and frame rate                            |

#### Camera Capture Mode Values

| Mode                          | When to use                                                                                                                                                                                                                                            |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Auto`                        | Default. On Built-in Render Pipeline, uses render hooks (`Camera.onPreRender` / `Camera.onPostRender`). On SRP/URP, uses the explicit render path (`TargetCamera.Render()` in `LateUpdate`). Select this first and override only if the feed is black. |
| `BuiltInHooks`                | Forces Built-in Render Pipeline capture hooks. Only compatible with the Built-in RP — selecting this on SRP/URP produces a black feed.                                                                                                                 |
| `ExplicitRenderCompatibility` | Forces an explicit per-frame camera render. Use when `Auto` produces a black feed on SRP/URP, or with highly customised render setups. Adds a bounded extra camera render at the configured capture FPS.                                               |
| `SrpNative`                   | **Not available in this SDK build.** See note below.                                                                                                                                                                                                   |

{% hint style="danger" %}
**`SrpNative` is not functional in the current SDK build.** Selecting it causes `CameraVisionFrameSource` to enter `Failed` state immediately with `ErrorKind = UnsupportedPlatform`. If `Auto` is producing a black feed on your SRP/URP project, use `ExplicitRenderCompatibility` instead.
{% endhint %}

{% hint style="warning" %}
Leave **Camera Capture Mode** at `Auto` unless you have a specific reason to override it. Selecting the wrong backend for your render pipeline results in a black or blank video feed.
{% endhint %}

{% hint style="warning" %}
**Enable Diagnostic Frame Health Probe** performs a synchronous GPU-to-CPU pixel readback every frame. Enable it only during debugging and disable it before shipping. In production, the SDK performs lighter-weight frame health checks internally.
{% endhint %}

***

### WebcamVisionFrameSource

`WebcamVisionFrameSource` captures a physical camera device using Unity's `WebCamTexture` API and converts the output to a `RenderTexture`. It handles device selection, permission requests (on Android and iOS), automatic rotation correction, and resolution clamping.

**Component menu path:** `Convai/Vision/Webcam Vision Frame Source`

#### Inspector Reference

**Webcam Settings**

| Field                  | Type     | Default | Description                                                                                                         |
| ---------------------- | -------- | ------- | ------------------------------------------------------------------------------------------------------------------- |
| **Webcam Device Name** | `string` | `""`    | Name of the webcam device to open. An empty string selects the first available device.                              |
| **Requested Width**    | `int`    | `640`   | Requested capture width sent to the driver. Actual resolution may differ.                                           |
| **Requested Height**   | `int`    | `480`   | Requested capture height sent to the driver.                                                                        |
| **Requested Fps**      | `int`    | `15`    | Requested frame rate sent to the driver.                                                                            |
| **Max Output Width**   | `int`    | `1280`  | Maximum width of the output `RenderTexture`. Frames wider than this are scaled down. Set to `0` to disable scaling. |
| **Max Output Height**  | `int`    | `720`   | Maximum height of the output `RenderTexture`.                                                                       |

**Source Identification**

| Field         | Type     | Default    | Description                                                  |
| ------------- | -------- | ---------- | ------------------------------------------------------------ |
| **Source Id** | `string` | `"webcam"` | Identifier used in domain events and multi-source scenarios. |

#### Listing Available Devices

To enumerate connected webcam devices at runtime:

```csharp
string[] deviceNames = WebcamVisionFrameSource.GetAvailableDeviceNames();
foreach (string name in deviceNames)
    Debug.Log(name);
```

#### Switching Devices at Runtime

To switch to a different webcam without stopping the session:

```csharp
WebcamVisionFrameSource webcam = GetComponent<WebcamVisionFrameSource>();
await webcam.SwitchWebcamAsync("Front Camera");
```

#### Permission Flow (Android / iOS)

On Android and iOS the component requests camera permission asynchronously when `StartCapture()` is called. The `State` property transitions through:

`Idle → AwaitingPermission → Starting → Ready`

If the user denies permission, `State` becomes `Failed` and `ErrorKind` is set to `PermissionDenied`. Monitor this via `IVisionFrameSourceStatusProvider.StatusChanged` — see [Scripting API](/broken/pages/66ae09f082490e6e22eeabcf09762855075b37c0) for the state monitor pattern.

{% hint style="info" %}
On Android and iOS the system camera permission dialog appears the first time `StartCapture()` runs. Ensure your app's `AndroidManifest.xml` declares `android.permission.CAMERA` and your iOS `Info.plist` includes `NSCameraUsageDescription` before submitting to app stores.
{% endhint %}

***

### QuestVisionFrameSource

`QuestVisionFrameSource` streams the real-world passthrough feed from a Meta Quest 3 or 3S headset, giving Convai characters a live view of the physical environment. The component binds to Meta's `PassthroughCameraAccess` API via reflection so the SDK does not take a hard compile-time dependency on the Meta XR package.

**Component menu path:** `Convai/Vision/Quest Vision Frame Source`

{% hint style="warning" %}
`QuestVisionFrameSource` requires **Meta Quest 3 or 3S** running Horizon OS with the Passthrough Camera API. Quest 2 and Quest Pro do not support `PassthroughCameraAccess`. In the Editor or on other platforms, the component enters `Failed` state with `ErrorKind = UnsupportedPlatform` and produces no frames.
{% endhint %}

{% hint style="danger" %}
**AndroidManifest.xml permissions required.** Your manifest must declare both `horizonos.permission.HEADSET_CAMERA` and `android.permission.CAMERA`. Without these declarations, passthrough capture fails silently on device and the frame source enters `Failed` state.
{% endhint %}

#### Inspector Reference

**Quest Camera Access**

| Field                         | Type            | Default             | Description                                                                                |
| ----------------------------- | --------------- | ------------------- | ------------------------------------------------------------------------------------------ |
| **Passthrough Camera Access** | `MonoBehaviour` | _(auto-discovered)_ | Reference to a `PassthroughCameraAccess` component in the scene. Leave blank to auto-find. |

**Output Settings**

| Field                 | Type     | Default               | Description                                                                                                                                         |
| --------------------- | -------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Source Id**         | `string` | `"quest-passthrough"` | Identifier used in domain events.                                                                                                                   |
| **Max Output Width**  | `int`    | `1280`                | Maximum width of the output `RenderTexture`.                                                                                                        |
| **Max Output Height** | `int`    | `720`                 | Maximum height of the output `RenderTexture`.                                                                                                       |
| **Target Frame Rate** | `int`    | `15`                  | Target frames per second for capture.                                                                                                               |
| **Flip Y**            | `bool`   | `true`                | Flips the passthrough texture vertically. Required for correct video orientation — disable only if the Meta SDK changes its coordinate conventions. |

{% hint style="info" %}
The binding to `PassthroughCameraAccess` is established via reflection at runtime. If the Meta XR package is updated and `PassthroughCameraAccess` changes its API, the component will log an error and enter `Failed` state. Check for SDK updates in that case.
{% endhint %}

***

### Source State Reference

All three frame sources implement `IVisionFrameSourceStatusProvider`, which exposes a `State` property and a `StatusChanged` event. Use these to monitor capture health from scripts.

#### VisionSourceState

| State                | Meaning                                                                                           |
| -------------------- | ------------------------------------------------------------------------------------------------- |
| `Idle`               | Capture has not been started.                                                                     |
| `AwaitingPermission` | Waiting for the user to grant camera permission (Android / iOS).                                  |
| `Starting`           | Capture is initialising — device is opening, `RenderTexture`s are being created.                  |
| `Ready`              | Capture is running and frames are being produced.                                                 |
| `Degraded`           | Capture is running but frame health checks are detecting issues (e.g., consecutive blank frames). |
| `Stopped`            | Capture was stopped normally.                                                                     |
| `Failed`             | Capture failed and cannot continue. Check `ErrorKind` and `StatusMessage` for details.            |

#### VisionSourceErrorKind

| Error kind             | Cause                                                                                                                      |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `None`                 | No error.                                                                                                                  |
| `Timeout`              | The source did not produce a usable frame within the expected time window.                                                 |
| `PermissionDenied`     | Camera permission was denied by the user or the OS.                                                                        |
| `UnsupportedPlatform`  | The source is not supported on this platform (e.g., `QuestVisionFrameSource` on PC, or `SrpNative` capture mode selected). |
| `DeviceUnavailable`    | The requested camera device could not be opened.                                                                           |
| `InvalidConfiguration` | A field value is out of range or inconsistent (check `StatusMessage`).                                                     |
| `Unknown`              | An unexpected error occurred.                                                                                              |

For scripting against these states and responding to `StatusChanged` events, see [Scripting API](/broken/pages/66ae09f082490e6e22eeabcf09762855075b37c0).

***

### Platform Compatibility Matrix

| Feature                   | PC / Mac        | Android / iOS       | WebGL                      | Meta Quest 3 / 3S        |
| ------------------------- | --------------- | ------------------- | -------------------------- | ------------------------ |
| `CameraVisionFrameSource` | ✅               | ✅                   | ❌ (no frame source needed) | ✅                        |
| `WebcamVisionFrameSource` | ✅               | ✅ (permission flow) | ❌                          | ❌                        |
| `QuestVisionFrameSource`  | ❌               | ❌                   | ❌                          | ✅ (Meta XR SDK required) |
| WebGL canvas capture      | ❌               | ❌                   | ✅ (automatic)              | ❌                        |
| `VisionDebugPreview`      | ✅ (Editor only) | ✅ (Editor only)     | ⚠️ blank                   | ✅ (Editor only)          |
| Max publish FPS           | 30              | 30                  | 15                         | 30                       |

{% hint style="info" %}
On WebGL no frame source component is required or used. `ConvaiVisionPublisher` captures the visible browser canvas automatically via `canvas.captureStream()`. See [Publishing & Policies](/broken/pages/1538f07b55ab5c719a79be190e1c775c62b5bd3c) for WebGL-specific behaviour and the HTTPS requirement.
{% endhint %}

***

### Next Steps

Each frame source targets a specific platform and capture scenario — use `CameraVisionFrameSource` for Unity scene cameras, `WebcamVisionFrameSource` for physical devices on desktop and mobile, and `QuestVisionFrameSource` for Meta Quest passthrough. With your frame source configured and in the `Ready` state, proceed to [Publishing & Policies](/broken/pages/1538f07b55ab5c719a79be190e1c775c62b5bd3c) to control how and when frames are sent to Convai.
