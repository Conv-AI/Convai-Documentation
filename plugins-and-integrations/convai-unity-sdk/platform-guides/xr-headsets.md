# xr headsets

The Convai Unity SDK runs on Android-based XR headsets (Meta Quest, Android XR) and Windows XR headsets without extra configuration for core features. Voice conversation, lip sync, actions, emotion, and long-term memory work the same as on any other supported platform. Vision is the only feature that requires XR-specific integration work — and only when you want the AI character to see the real world through the headset's cameras.

***

## Core Feature Support on XR

All core SDK features work on XR headsets without additional SDK configuration:

* **Android-based XR** (Meta Quest, Horizon OS, Android XR): Follows the same setup as any Android build. See [iOS and Android](/broken/pages/665d1a02c31405b646ea5620c1cde76157d769ae) for `RECORD_AUDIO` manifest requirement and runtime permission flow.
* **Windows XR** (standalone PC VR): No additional setup beyond a standard Windows build configuration.

Vision is the only feature that varies between XR platforms. The decision tree below shows when and what extra setup is needed:

```mermaid
graph TD
    A[XR Deployment] --> B{Vision needed?}
    B -->|No| C[Follow Android or Windows guide for permissions]
    C --> D[Done — all core features work]
    B -->|Yes| E{Meta Quest 3 or 3S?}
    E -->|Yes| F[Use QuestVisionFrameSource]
    F --> G[Add Meta XR SDK + permissions]
    E -->|No - other XR headset| H[Implement custom IVisionFrameSource]
    H --> I[See Vision docs for custom frame source]
```

***

## Vision on Meta Quest

`QuestVisionFrameSource` streams the passthrough camera feed from a Meta Quest headset to Convai, enabling the AI character to see and respond to the real world the learner or user is looking at.

**Supported hardware:** Meta Quest 3 and Quest 3S running Horizon OS with the Passthrough Camera API available.

The component uses reflection to bind to Meta XR SDK's `PassthroughCameraAccess` at runtime. The Convai SDK itself has no hard dependency on any Meta SDK package — you can update or swap the Meta XR SDK version without changes to the Convai SDK.

{% hint style="info" %}
`QuestVisionFrameSource` produces no frames in the Unity Editor or on non-Quest builds. This is expected behavior — `PassthroughCameraAccess` is only available on Horizon OS. Test Vision on a physical device.
{% endhint %}

For full Vision configuration — publishing policies, debug preview, vision-aware character prompts — see the Vision feature documentation.

{% content-ref url="/broken/pages/f04925fe1f1f751ffbc1007ce465bfb5dcf08309" %}
[Broken link](/broken/pages/f04925fe1f1f751ffbc1007ce465bfb5dcf08309)
{% endcontent-ref %}

### Required Permissions

{% hint style="danger" %}
Both permissions must be declared in your `AndroidManifest.xml`. The passthrough camera will not start without them, and the component will enter the `Failed` state after three retry attempts.
{% endhint %}

{% code title="AndroidManifest.xml" %}
```xml
<uses-permission android:name="horizonos.permission.HEADSET_CAMERA" />
<uses-permission android:name="android.permission.CAMERA" />
```
{% endcode %}

### Setup

{% stepper %}
{% step %}
**Import the Meta XR SDK**

Install the Meta XR SDK package from the Meta XR Developer Hub or the Unity Asset Store. Add a `PassthroughCameraAccess` component to a GameObject in your scene — this component is provided by Meta's SDK and handles the low-level passthrough camera API.
{% endstep %}

{% step %}
**Add QuestVisionFrameSource**

Add the `QuestVisionFrameSource` component to a GameObject in your scene. This can be the same GameObject as `PassthroughCameraAccess` or a separate one.
{% endstep %}

{% step %}
**Assign the Reference (Optional)**

Drag the `PassthroughCameraAccess` component into the **Passthrough Camera Access** field on `QuestVisionFrameSource`. If left empty, the component searches the active scene automatically on `StartCapture()`. Auto-discovery works for single-camera setups; assign explicitly when multiple `PassthroughCameraAccess` instances are present.
{% endstep %}

{% step %}
**Add a Vision Publisher**

Add `ConvaiVisionPublisher` to the same GameObject. It discovers `QuestVisionFrameSource` in the scene automatically, or you can assign the frame source reference in the publisher's Inspector.
{% endstep %}

{% step %}
**Declare Manifest Permissions**

Add `horizonos.permission.HEADSET_CAMERA` and `android.permission.CAMERA` to your `AndroidManifest.xml` at `Assets/Plugins/Android/AndroidManifest.xml`.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Build and deploy to your Quest device. After the scene loads, the Vision status in the Convai Settings Panel should show **Ready**. The character will begin receiving passthrough frames and can respond to what it sees.
{% endhint %}

### Inspector Reference

| Field                         | Default             | Description                                                                                                                                                                 |
| ----------------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Passthrough Camera Access** | None                | Optional reference to the `PassthroughCameraAccess` component. Auto-discovered from the active scene if left empty.                                                         |
| **Source Id**                 | `quest-passthrough` | Identifier used by `ConvaiVisionPublisher` to select this frame source.                                                                                                     |
| **Max Output Width**          | 1280                | Maximum pixel width of frames sent to Convai. Reduce to lower bandwidth usage.                                                                                              |
| **Max Output Height**         | 720                 | Maximum pixel height of frames sent to Convai.                                                                                                                              |
| **Target Frame Rate**         | 15                  | Frames per second cap for the passthrough capture loop. Lower values reduce bandwidth and processing load.                                                                  |
| **Flip Y**                    | true                | Flips the passthrough texture vertically so the published frame is top-down. Disable only if your Meta SDK version handles orientation before handing the texture to Unity. |

{% hint style="info" %}
`QuestVisionFrameSource` retries finding `PassthroughCameraAccess` up to three times with one-second intervals between attempts before entering the `Failed` state. If your scene initializes `PassthroughCameraAccess` asynchronously or after a delay, ensure it is ready before `QuestVisionFrameSource` begins capture.
{% endhint %}

***

## Vision on Other XR Platforms

No built-in frame source exists for non-Meta XR headsets — OpenXR-only devices, Windows Mixed Reality, HoloLens, or other Android XR platforms that do not expose a passthrough camera through the Meta XR SDK.

To enable Vision on these devices, implement `IVisionFrameSource` and supply frames from your XR SDK's camera API:

{% code title="CustomXRVisionFrameSource.cs" %}
```csharp
using System;
using Convai.Runtime.Vision.Sources;
using UnityEngine;

public class CustomXRVisionFrameSource : MonoBehaviour, IVisionFrameSource
{
    [SerializeField] private float _targetFrameRate = 15f;
    [SerializeField] private string _sourceId = "custom-xr";

    private RenderTexture _renderTexture;

    public bool IsCapturing { get; private set; }
    public long FrameCount { get; private set; }
    public (int Width, int Height) FrameDimensions => (_renderTexture ? _renderTexture.width : 0,
                                                       _renderTexture ? _renderTexture.height : 0);
    public float TargetFrameRate => _targetFrameRate;
    public string SourceId => _sourceId;
    public RenderTexture CurrentRenderTexture => _renderTexture;
    public bool IsFrameReady { get; private set; }

    public event Action FrameReady;

    public void StartCapture()
    {
        // Initialize your XR SDK camera and RenderTexture here.
        // Each time a new frame is available, blit it into _renderTexture (top-down / Y-flipped),
        // then increment FrameCount, set IsFrameReady = true, and raise FrameReady?.Invoke().
        IsCapturing = true;
    }

    public void StopCapture()
    {
        IsCapturing = false;
        IsFrameReady = false;
    }
}
```
{% endcode %}

Assign your custom source to `ConvaiVisionPublisher` via its Inspector field. See the Vision feature documentation for the full `IVisionFrameSource` contract, publishing policies, and debug preview setup.

***

## Usage Examples

### Medical Training with Passthrough Scene Awareness

A surgical resident training application on Quest 3 places learners in a mock operating environment. The Convai AI character plays a surgical team member who can see and comment on physical props the resident holds up — anatomical models, instruments, procedure reference cards.

**Setup:** `QuestVisionFrameSource` on a scene GameObject with **Passthrough Camera Access** auto-discovered. `ConvaiVisionPublisher` on the same object. Both permissions declared in the manifest. The character's Convai configuration includes a vision-aware system prompt instructing it to acknowledge and respond to what it sees in the passthrough feed.

**Outcome:** The character responds to visual context alongside conversation — "I can see you're preparing the scalpel — let's review the incision depth for this procedure." The resident practices both verbal and physical task execution without any object detection code in the Unity project.

***

### Industrial Safety Inspection with Environmental Object Recognition

A factory safety training application on Quest 3S guides equipment operators through machinery inspection. The AI character identifies physical components visible in the passthrough feed and adapts its safety guidance based on what the operator is looking at.

**Setup:** Same configuration as the medical training example. **Target Frame Rate** is set to 10 (reduced from 15) to accommodate the industrial network environment. **Max Output Width** is set to 960 to reduce per-frame payload size without meaningful quality loss for object recognition tasks.

**Outcome:** The character identifies machinery in the passthrough view and provides component-specific safety instructions — no hardcoded object detection, no custom computer vision pipeline. The SDK streams passthrough frames to Convai, which handles scene understanding and generates contextually appropriate guidance.

***

## Troubleshooting

| Symptom                                                | Likely Cause                                                              | Fix                                                                                                                     |
| ------------------------------------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Source status shows `Failed / DeviceUnavailable`       | `PassthroughCameraAccess` not found after three attempts                  | Add the component to the scene, or assign the reference explicitly in the **Passthrough Camera Access** Inspector field |
| Source stays in `Starting`; no frames captured         | Missing manifest permissions                                              | Add `horizonos.permission.HEADSET_CAMERA` and `android.permission.CAMERA` to `AndroidManifest.xml`                      |
| `QuestVisionFrameSource` shows no output in the Editor | Expected — `PassthroughCameraAccess` only runs on Horizon OS              | Test on a physical Quest device                                                                                         |
| Character does not respond to visual context           | Vision publisher not connected, or Vision not enabled in character config | Verify `ConvaiVisionPublisher` is in the scene and the character's Vision capability is enabled in the Convai dashboard |
| Passthrough feed correct but image appears upside down | **Flip Y** was disabled                                                   | Re-enable **Flip Y** in the `QuestVisionFrameSource` Inspector                                                          |

***

## Next Steps

{% content-ref url="/broken/pages/ff400377bdbe8a12298f59c05337311a5c570cc2" %}
[Broken link](/broken/pages/ff400377bdbe8a12298f59c05337311a5c570cc2)
{% endcontent-ref %}

{% content-ref url="/broken/pages/665d1a02c31405b646ea5620c1cde76157d769ae" %}
[Broken link](/broken/pages/665d1a02c31405b646ea5620c1cde76157d769ae)
{% endcontent-ref %}
