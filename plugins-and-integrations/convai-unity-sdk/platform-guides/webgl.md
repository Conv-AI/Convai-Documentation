---
title: WebGL
last_reviewed: "5.0.0-preview"
description: >-
  Deploy the Convai Unity SDK to WebGL, covering HTTPS, browser audio
  gestures, frame-source Vision, microphone failures, and browser lip-sync timing.
---

The Convai Unity SDK supports voice conversation, lip sync, actions, dynamic context, emotion, Vision, and long-term memory on WebGL. The browser introduces three constraints that do not exist on native platforms: a mandatory HTTPS origin for microphone access, a possible user-gesture requirement for blocked audio playback, and browser-based media playback and publishing. All three are covered on this page.

{% embed url="https://youtu.be/SbQ-Kfi7yg4" %}
Convai-Powered Unity 6 Web Projects (previously referred to as WebGL builds)
{% endembed %}

## Feature support

| Feature                      | WebGL                                               |
| ---------------------------- | --------------------------------------------------- |
| Voice conversation           | ✅ Implemented                                              |
| Lip sync                     | ✅ Browser playback timing         |
| Actions                      | ✅ Implemented                                              |
| Dynamic Context              | ✅ Implemented                                              |
| Emotion                      | ✅ Implemented                                              |
| Vision                       | ✅ Configured Frame Source by default                |
| Long-Term Memory             | ✅ Implemented                                              |
| Spatial audio                | ❌ Not supported                                     |
| Microphone device selection  | ❌ Not available — browser controls device selection |
| Unity `AudioSource` playback | ❌ Not supported — browser audio path only           |
| Microphone test / pre-check  | ❌ Not supported                                     |

## Browser requirements

{% hint style="danger" %}
**HTTPS is required for microphone access.** Browsers block microphone capture on non-secure origins. Serve your WebGL build over HTTPS. The only exception is `localhost`, which browsers treat as a secure origin. A denied or unavailable microphone is reported through the session error path. Your UI should explain the failure and keep typed input available in an ordinary room.
{% endhint %}

**iframe embedding:** When embedding your WebGL build in an iframe, the parent page must include `allow="microphone"` on the `<iframe>` element. Without it, the browser blocks microphone access regardless of HTTPS status.

```html
<iframe src="https://your-host.com/build/" allow="microphone" width="960" height="600"></iframe>
```

**Microphone device selection:** The browser controls all microphone device selection. When conversation starts, the browser displays its own permission prompt and allows the user to select a microphone device. The SDK's Unity microphone enumeration returns an empty device list on WebGL — the Settings Panel microphone dropdown will show no entries. This is expected behavior, not an error. The microphone test functionality available on native platforms is not supported on WebGL.

### Example: LMS iframe embed

A manufacturing company embeds a safety compliance drill in their Learning Management System. The LMS iframe loads the WebGL build from `https://sim.company.com/safety-drill`. The Convai character plays a site safety officer who tests operator responses to in-scene hazard scenarios.

**Setup:**

1.  The LMS page includes the `allow="microphone"` attribute on the `<iframe>` element:

    ```html
    <iframe src="https://sim.company.com/safety-drill/" allow="microphone" width="1280" height="720"></iframe>
    ```
2. The WebGL build is served over HTTPS.
3. An explicit **Begin Drill** button is placed on the scene load screen, wired to `ConvaiManager.EnableAudioAndStartListening()`.

**Outcome:** Operators click **Begin Drill**, grant microphone permission in the browser prompt, and begin the verbal compliance assessment.

## Audio gesture handling

Browser autoplay policy can block audio playback until a user interacts. Microphone capture separately requires a secure origin and permission; this SDK no longer gates capture on the playback gesture flag. To unlock blocked playback:

**Automatic gesture detection:** After connection, each eligible click or touch outside UI rechecks whether browser playback is blocked. When it is, the manager calls `EnableAudioAndStartListening()`. This also handles blocking detected after the initial connection. This works for scenes where users interact directly with the 3D view.

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

    private void OnEnable()
    {
        if (_startButton != null) _startButton.onClick.AddListener(OnStartClicked);
    }

    private void OnDisable()
    {
        if (_startButton != null) _startButton.onClick.RemoveListener(OnStartClicked);
    }

    private void OnStartClicked()
    {
        if (_convaiManager != null) _convaiManager.EnableAudioAndStartListening();
        // Hide the start UI only after your application confirms audio is ready.
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

**Outcome:** Employees click **Start Conversation** on the welcome screen. The browser displays a microphone permission prompt. After granting permission, the Convai character begins the onboarding dialogue. Keep the welcome screen available until your application confirms that audio is ready or displays the failure.

## Vision on WebGL

In 5.0, **Convai Vision Publisher > WebGL Publishes > Frame Source** publishes the configured source. **Game View** explicitly publishes the visible Unity canvas, including chat, menus and other UI. With Frame Source selected but no source assigned or discovered, the publisher falls back to the Game view. A source implementing `IVisionPageCanvasSource` publishes its own page canvas.

| Setting | WebGL behavior |
| --- | --- |
| Frame Source with a supported source | Publishes the source's picture. |
| Game View | Publishes the Unity canvas; does not start the assigned frame source. |
| Frame Source with no source | Falls back to the Unity canvas, including UI. |
| Publish Frame Rate Override | `0` follows policy; explicit overrides range up to 30 fps. |
| Default policy rates | Auto Compatible 10 fps, High Responsiveness 15 fps, Low Overhead 5 fps. |

`WebcamVisionFrameSource` is not the supported WebGL webcam integration. Use a native player for that component. See [WebGL vision](../features/vision/webgl.md) for frame-source and page-canvas requirements.

## Microphone policy and playback

Set **Allow Microphone** off for a text-only ordinary room. It prevents opening the microphone; remote character voice remains a separate setting. A denied browser prompt does not have to end the session: present `audio.mic_permission_denied`, `audio.mic_unavailable` or `audio.mic_publish_failed` and allow typed input where the room supports it.

`ConvaiAudioOutput.Volume` and `IsMuted` reach browser playback in 5.0. Unity's distance rolloff and `AudioListener.volume` do not. iOS Safari controls nonzero media volume itself, although mute and zero volume still silence playback.

WebGL uses Legacy push-to-talk release because it does not supply native capture drain. Group conversation requires correlated push-to-talk and is not supported by this path. Ordinary push-to-talk rooms remain available.

## Build validation checklist

Before shipping a WebGL build, verify each item:

* [ ] WebGL is the active build target before building, including in CI or an automated build script
* [ ] Build is served over HTTPS (or tested on `localhost`)
* [ ] If embedded in an iframe: parent page includes `allow="microphone"` on the `<iframe>` element
* [ ] Explicit Start button present (especially for UI-heavy scenes)
* [ ] Microphone permission prompt tested in Chrome, Firefox, and Safari
* [ ] Character audio confirmed playing (browser audio path — not `AudioSource`)
* [ ] Microphone dropdown empty in Settings Panel — confirm this is expected, not an error
* [ ] Lip-sync timing evaluated visually in-browser across a full conversation turn
* [ ] Vision response validated if Vision is enabled using the intended source, with no unintended UI in the published image

## Troubleshooting

| Symptom                                                       | Likely cause                                             | Fix                                                                                   |
| ------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Microphone never activates; character does not hear input     | Build is served over HTTP, not HTTPS                     | Serve the build over HTTPS. `localhost` is exempt.                                    |
| Microphone blocked in iframe; permission prompt never appears | Missing `allow="microphone"` on the `<iframe>` element   | Add `allow="microphone"` to the iframe tag on the embedding page.                     |
| Character audio is silent; no playback                        | No user gesture received before audio playback attempted | Add an explicit Start button wired to `ConvaiManager.EnableAudioAndStartListening()`. |
| Microphone dropdown is empty in Settings Panel                | Expected — browser controls device selection on WebGL    | No fix needed. The browser permission prompt handles device selection.                |
| Microphone test fails or is unavailable                       | Not supported on WebGL                                   | Expected behavior — inform users that mic testing is unavailable on browser builds.   |
| No spatial audio; voices lack 3D positioning                  | Spatial audio not supported on WebGL                     | Expected. Consider communicating this in UI (e.g., headphone prompt).                 |

### Lip-sync timing

The WebGL path uses `RealtimePlaybackClock` and measured browser voice onset. It waits up to two seconds while initial browser playback is silent. This replaces older blanket guidance that WebGL always has an unfixable drift defect.

If speech and mouth motion diverge, confirm browser audio has been unlocked, inspect the lip-sync playback status and test several complete turns in the target hosting environment. Record the browser, device and reproduction; native Editor playback is not evidence for browser timing.

### Build target mismatch

The 5.0 build guard rejects a WebGL build when WebGL is not the active target. Switch the active target or pass the appropriate build-target argument in automation before building; selecting an inactive profile is not sufficient.

## Next steps

Use the checklist as a browser validation baseline, then complete your application's deployment checks. If you are also deploying to iOS, Android, or XR headsets, those platforms have their own permission requirements.

{% content-ref url="ios-and-android.md" %}
[iOS and Android](ios-and-android.md)
{% endcontent-ref %}

{% content-ref url="xr-headsets.md" %}
[XR headsets](xr-headsets.md)
{% endcontent-ref %}
