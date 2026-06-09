---
title: WebGL
description: >-
  Configure and validate the Convai Unity SDK for WebGL, including HTTPS,
  browser audio gestures, Vision canvas capture, and lip-sync timing.
last_reviewed: "4.2.0"
---

The Convai Unity SDK supports voice conversation, lip sync, actions, dynamic context, emotion, Vision, and long-term memory on WebGL. The browser introduces three constraints that do not exist on native platforms: a mandatory HTTPS origin for microphone access, a user-gesture requirement before audio playback or microphone capture can begin, and a canvas-based Vision capture path instead of Unity `RenderTexture`. All three are covered on this page.

## Feature support

| Feature                      | WebGL                                               |
| ---------------------------- | --------------------------------------------------- |
| Voice conversation           | ✅ Full                                              |
| Lip sync                     | ⚠️ Supported; intermittent timing drift can occur    |
| Actions                      | ✅ Full                                              |
| Dynamic Context              | ✅ Full                                              |
| Emotion                      | ✅ Full                                              |
| Vision                       | ✅ Canvas capture (browser game view)                |
| Long-Term Memory             | ✅ Full                                              |
| Spatial audio                | ❌ Not supported                                     |
| Screen share                 | ❌ Not supported                                     |
| Microphone device selection  | ❌ Not available — browser controls device selection |
| Unity `AudioSource` playback | ❌ Not supported — browser audio path only           |
| Microphone test / pre-check  | ❌ Not supported                                     |

## Browser requirements

{% hint style="danger" %}
**HTTPS is required for microphone access.** Browsers block microphone capture on non-secure origins. Serve your WebGL build over HTTPS. The only exception is `localhost`, which browsers treat as a secure origin. Deploying to `http://` causes the browser to silently deny microphone permission — no error is shown to the user and voice conversation will not start.
{% endhint %}

**iframe embedding:** When embedding your WebGL build in an iframe, the parent page must include `allow="microphone"` on the `<iframe>` element. Without it, the browser blocks microphone access regardless of HTTPS status.

```html
<iframe src="https://your-host.com/build/" allow="microphone" width="960" height="600"></iframe>
```

**Microphone device selection:** The browser controls all microphone device selection. When conversation starts, the browser displays its own permission prompt and allows the user to select a microphone device. The SDK returns an empty device list on WebGL — the Settings Panel microphone dropdown will show no entries. This is expected behavior, not an error. The microphone test functionality available on native platforms is not supported on WebGL.

### Example: LMS iframe embed

A manufacturing company embeds a safety compliance drill in their Learning Management System. The LMS iframe loads the WebGL build from `https://sim.company.com/safety-drill`. The Convai character plays a site safety officer who tests operator responses to in-scene hazard scenarios.

**Setup:**

1. The LMS page includes the `allow="microphone"` attribute on the `<iframe>` element:

   ```html
   <iframe src="https://sim.company.com/safety-drill/" allow="microphone" width="1280" height="720"></iframe>
   ```
2. The WebGL build is served over HTTPS.
3. An explicit **Begin Drill** button is placed on the scene load screen, wired to `ConvaiManager.EnableAudioAndStartListening()`.

**Outcome:** Operators click **Begin Drill**, grant microphone permission in the browser prompt, and begin the verbal compliance assessment.

## Audio gesture handling

Browsers require a user interaction before allowing audio playback or microphone capture. The SDK handles this in two ways:

**Automatic gesture detection:** After connecting, the SDK listens for the first click or touch that lands outside a UI element and calls `EnableAudioAndStartListening()` on `ConvaiManager` automatically. This works for scenes where users interact directly with the 3D view.

**Explicit Start button (recommended for UI-heavy scenes):** For scenes with full-screen overlays, loading screens, or any UI that covers the view on load, automatic detection may not fire reliably. Add an explicit Start button and wire it to `ConvaiManager.EnableAudioAndStartListening()`.

The automatic gesture detection and the explicit Start button are not mutually exclusive — both can be active at the same time. The Start button approach is more reliable when UI covers the scene on load.

{% tabs %}
{% tab title="Inspector" %}
1. Add a **Button** component to a UI GameObject.
2. In the **On Click ()** list, click **+**.
3. Drag your `ConvaiManager` GameObject into the object field.
4. In the function dropdown, select **ConvaiManager → EnableAudioAndStartListening**.
{% endtab %}

{% tab title="C#" %}
```csharp
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.UI;

public class WebGLStartButton : MonoBehaviour
{
    [SerializeField] private ConvaiManager _convaiManager;
    [SerializeField] private Button _startButton;

    private void Start()
    {
        _startButton.onClick.AddListener(OnStartClicked);
    }

    private void OnStartClicked()
    {
        _convaiManager.EnableAudioAndStartListening();
        _startButton.gameObject.SetActive(false);
    }
}
```
{% endtab %}
{% endtabs %}

### Example: Corporate onboarding training

An enterprise L\&D team hosts a company policy training simulation on their corporate intranet at `https://training.company.internal/onboarding`. A Convai character plays an HR representative who guides new hires through policy scenarios.

**Setup:**

1. Build is served over HTTPS from the corporate intranet server.
2. A **Start Conversation** button is placed on a welcome screen using the Inspector approach above. `ConvaiManager.EnableAudioAndStartListening()` is wired to the button's **On Click ()** event.
3. Standard SDK configuration — no additional WebGL-specific steps.

**Outcome:** Employees click **Start Conversation** on the welcome screen. The browser displays a microphone permission prompt. After granting permission, the Convai character begins the onboarding dialogue. The welcome screen hides automatically after the button is clicked.

## Vision on WebGL

On WebGL, Vision captures the Unity game view as rendered in the browser canvas. The SDK uses an internal `WebGLCanvasVideoSource` to publish the browser canvas as the vision frame source — standard `CameraVisionFrameSource` components are not used on this platform.

Key differences from native Vision:

| Behavior                   | Native                                                 | WebGL                 |
| -------------------------- | ------------------------------------------------------ | --------------------- |
| Frame source               | `CameraVisionFrameSource` or `WebcamVisionFrameSource` | Browser canvas        |
| Max frame rate             | Configurable                                           | 15 fps (fixed)        |
| Webcam access              | Supported                                              | Not available via SDK |
| `RenderTexture` publishing | Supported                                              | Not used              |

WebGL Vision captures what the player sees in the browser — the game view. For scenarios where the character needs to see the learner's physical environment via webcam, use a desktop or mobile build with `WebcamVisionFrameSource` instead.

## Build validation checklist

Before shipping a WebGL build, verify each item:

* [ ] Build is served over HTTPS (or tested on `localhost`)
* [ ] If embedded in an iframe: parent page includes `allow="microphone"` on the `<iframe>` element
* [ ] Explicit Start button present (especially for UI-heavy scenes)
* [ ] Microphone permission prompt tested in Chrome, Firefox, and Safari
* [ ] Character audio confirmed playing (browser audio path — not `AudioSource`)
* [ ] Microphone dropdown empty in Settings Panel — confirm this is expected, not an error
* [ ] Lip-sync timing evaluated visually in-browser across a full conversation turn
* [ ] Vision response validated if Vision is enabled (canvas capture path)

## Troubleshooting

| Symptom                                                       | Likely cause                                                                      | Fix                                                                                   |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Microphone never activates; character does not hear input     | Build is served over HTTP, not HTTPS                                              | Serve the build over HTTPS. `localhost` is exempt.                                    |
| Microphone blocked in iframe; permission prompt never appears | Missing `allow="microphone"` on the `<iframe>` element                            | Add `allow="microphone"` to the iframe tag on the embedding page.                     |
| Character audio is silent; no playback                        | No user gesture received before audio playback attempted                          | Add an explicit Start button wired to `ConvaiManager.EnableAudioAndStartListening()`. |
| Microphone dropdown is empty in Settings Panel                | Expected — browser controls device selection on WebGL                             | No fix needed. The browser permission prompt handles device selection.                |
| Microphone test fails or is unavailable                       | Not supported on WebGL                                                            | Expected behavior — inform users that mic testing is unavailable on browser builds.   |
| No spatial audio; voices lack 3D positioning                  | Spatial audio not supported on WebGL                                              | Expected. Consider communicating this in UI (e.g., headphone prompt).                 |
| Lip sync does not start with character audio                  | Browser audio unlock or playback start happened before the user gesture completed | Start audio from an explicit button and validate a full response turn in the browser. |
| Lip sync drifts from speech audio during longer turns         | Known intermittent WebGL timing issue                                             | Validate in the target browser and keep the SDK updated. If drift appears, retry with an explicit Start button and a fresh browser session. |

## Next steps

Your WebGL build is ready once HTTPS is confirmed, the gesture requirement is handled, and the validation checklist passes. If you are also deploying to iOS, Android, or XR headsets, those platforms have their own permission requirements.

{% content-ref url="ios-and-android.md" %}
[iOS and Android](ios-and-android.md)
{% endcontent-ref %}

{% content-ref url="xr-headsets.md" %}
[XR headsets](xr-headsets.md)
{% endcontent-ref %}
