---
description: >-
  Verify Vision capture in the Unity Editor with a live overlay showing the
  active frame source, capture statistics, and source state.
---

# Debug Preview

## Visualising Vision Capture with Debug Preview

`VisionDebugPreview` renders the active frame source's output as an on-screen overlay inside the Unity Editor, giving you immediate visual confirmation that capture is working correctly. It also displays a live statistics panel showing frame rate, total frame count, and source state. Because this component is designed for development use, it automatically disables itself in player builds — it has zero runtime cost when you ship your project.

{% hint style="warning" %}
`VisionDebugPreview` is an **Editor-only** component. It disables itself automatically when running in a player build. Do not rely on it for in-game UI or production diagnostics.
{% endhint %}

### Adding Debug Preview to Your Scene

{% stepper %}
{% step %}
#### Add the Component

Select any GameObject in the scene — the same one as your frame source, or a dedicated debug object. Click **Add Component** → **Convai/Vision/Vision Debug Preview (Editor Only)**.

<figure><img src="../../../../.gitbook/assets/image (69).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
#### Assign a Frame Source (Optional)

In the **Frame Source Component** field, drag in the `IVisionFrameSource` component you want to preview. If you leave this blank and **Fallback to Active Frame Source** is enabled, the component automatically selects the first capturing source in the scene.
{% endstep %}

{% step %}
#### Enter Play Mode

Press **Play**. An overlay appears in the Game view showing the live texture and a statistics panel. Adjust position and size using the Inspector fields described below.

<figure><img src="../../../../.gitbook/assets/image (70).png" alt=""><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

***

### Inspector Reference

#### Frame Source

<table><thead><tr><th width="170.49993896484375">Field</th><th width="149.99993896484375">Type</th><th width="143.5">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Frame Source Component</strong></td><td><code>MonoBehaviour</code></td><td><em>(auto-resolved)</em></td><td>The frame source to preview. Leave blank to use fallback auto-discovery.</td></tr><tr><td><strong>Fallback to Active Frame Source</strong></td><td><code>bool</code></td><td><code>true</code></td><td>When the assigned source is idle or unassigned, automatically find and display the first actively capturing source in the scene.</td></tr></tbody></table>

#### Overlay Layout

<table><thead><tr><th width="156.49993896484375">Field</th><th width="162">Type</th><th width="133.5">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Overlay Position</strong></td><td><code>PreviewPosition</code></td><td><code>BottomRight</code></td><td>Corner of the Game view where the overlay is anchored.</td></tr><tr><td><strong>Overlay Width</strong></td><td><code>int</code> (160–640)</td><td><code>320</code></td><td>Width of the preview overlay in pixels.</td></tr><tr><td><strong>Offset X</strong></td><td><code>int</code> (0–200)</td><td><code>10</code></td><td>Horizontal distance in pixels between the overlay edge and the screen edge.</td></tr><tr><td><strong>Offset Y</strong></td><td><code>int</code> (0–200)</td><td><code>10</code></td><td>Vertical distance in pixels between the overlay edge and the screen edge.</td></tr></tbody></table>

#### Aspect Ratio

<table><thead><tr><th width="198.99993896484375">Field</th><th width="127.99993896484375">Type</th><th width="125.5">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Use Source Aspect Ratio</strong></td><td><code>bool</code></td><td><code>true</code></td><td>Derives the overlay height from the frame source's actual capture dimensions.</td></tr><tr><td><strong>Custom Aspect Ratio</strong></td><td><code>float</code> (1–3)</td><td><code>1.778</code> (16:9)</td><td>The aspect ratio used to calculate overlay height when <strong>Use Source Aspect Ratio</strong> is disabled.</td></tr></tbody></table>

#### Preview Settings

<table><thead><tr><th width="141.5">Field</th><th width="83.5">Type</th><th width="100.5">Default</th><th>Description</th></tr></thead><tbody><tr><td><strong>Show Preview</strong></td><td><code>bool</code></td><td><code>true</code></td><td>Enables or disables the image overlay. Can be toggled at runtime.</td></tr><tr><td><strong>Show Stats</strong></td><td><code>bool</code></td><td><code>true</code></td><td>Enables or disables the statistics overlay. Can be toggled at runtime.</td></tr></tbody></table>

### PreviewPosition Values

<table><thead><tr><th width="330.49993896484375">Value</th><th>Overlay anchor</th></tr></thead><tbody><tr><td><code>TopLeft</code></td><td>Upper-left corner of the Game view</td></tr><tr><td><code>TopRight</code></td><td>Upper-right corner</td></tr><tr><td><code>BottomLeft</code></td><td>Lower-left corner</td></tr><tr><td><code>BottomRight</code></td><td>Lower-right corner (default)</td></tr></tbody></table>

***

### Statistics Overlay

When **Show Stats** is enabled, the overlay displays the following live values:

<table><thead><tr><th width="192.5">Statistic</th><th>Description</th></tr></thead><tbody><tr><td><strong>FPS</strong></td><td>Frames per second currently being produced by the frame source</td></tr><tr><td><strong>Frame count</strong></td><td>Total frames captured since capture started</td></tr><tr><td><strong>State</strong></td><td>Current <code>VisionSourceState</code> of the frame source (e.g., <code>Ready</code>, <code>Degraded</code>)</td></tr><tr><td><strong>Dimensions</strong></td><td>Capture resolution in pixels</td></tr></tbody></table>

***

### Runtime Scripting

`VisionDebugPreview` exposes a small scripting API for toggling the overlay and reading current statistics:

```csharp
using Convai.Runtime.Vision.Debug;

VisionDebugPreview preview = GetComponent<VisionDebugPreview>();

// Toggle overlay visibility
preview.ShowPreview = false;
preview.ShowStats = true;

// Read current capture statistics
float fps = preview.CurrentFps;
long frames = preview.FrameCount;
bool capturing = preview.IsCapturing;
```

***

### Known Limitations

{% hint style="warning" %}
`VisionDebugPreview` previews `IVisionFrameSource.CurrentRenderTexture`. It does **not** show the WebGL canvas capture path. On WebGL the overlay will appear blank or not initialise, because there is no frame source component in WebGL builds.
{% endhint %}

If no frame source is active and **Fallback to Active Frame Source** is `false`, the overlay shows a placeholder indicating that no capturing source was found. Enable fallback or assign the frame source explicitly to resolve this.

***

## Conclusion

`VisionDebugPreview` gives you a live view of exactly what the character sees, along with capture statistics, at zero cost to your production build. Use it throughout development to verify frame source health, confirm capture is running at the expected frame rate, and catch issues before they reach players. Continue to [Scripting API](scripting-api.md) for the full publisher API and domain events, or see [Usage Examples](../../../unity-plugin-beta-overview/features/vision/usage-examples.md) for end-to-end implementation scenarios.
