---
title: WebGL
last_reviewed: "5.0.0-pre.1"
description: >-
  Deploy the Convai Unity SDK to WebGL, covering HTTPS, browser audio
  gestures, frame-source Vision, microphone failures, and browser lip-sync timing.
---

WebGL uses the browser for microphone access, voice playback, and Vision publishing. Configure a secure origin and a playback button, then verify capture and playback in the page that hosts the build.

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
| Microphone device selection  | Browser default only |
| Unity `AudioSource` playback | ❌ Not supported — browser audio path only           |
| Microphone test / pre-check  | ❌ Not supported                                     |

## Browser requirements

{% hint style="danger" %}
**HTTPS is required for microphone access.** Browsers block microphone capture on non-secure origins. Serve your WebGL build over HTTPS. `localhost` is also suitable for local testing. A denied or unavailable microphone is reported through the session error path. Your UI should explain the failure and keep typed input available in an ordinary room.
{% endhint %}

**iframe embedding.** For a cross-origin build, delegate microphone access to the iframe. The embedding page's Permissions Policy must also permit access for the frame. If the build uses a physical webcam, use `allow="camera; microphone"` and permit camera access in the parent policy as well.

```html
<iframe src="https://your-host.com/build/" allow="microphone" width="960" height="600"></iframe>
```

The browser controls microphone devices. The SDK exposes one entry, `Default Microphone`. Device switching and the Settings Panel's local recording test are unavailable on WebGL. For embedding and permission details, see [Browser media permissions](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia).

## Audio gesture handling

Browser autoplay policy can block audio playback until a user interacts. Microphone capture separately requires a secure origin and permission; this SDK no longer gates capture on the playback gesture flag. To unlock blocked playback:

After connection, the manager checks eligible pointer gestures outside UI and retries browser playback when it is blocked. For a full-screen menu or welcome screen, add a button that calls the audio facade directly from its click callback.

Attach this script to a GameObject and assign the scene's manager. In the Button's **On Click ()** list, add that GameObject and select **WebGLStartButton > EnableVoice**.

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public sealed class WebGLStartButton : MonoBehaviour
{
    [SerializeField] private ConvaiManager manager;

    public void EnableVoice()
    {
        if (manager != null && manager.IsInitialized)
            manager.Audio.EnableAudioAndStartListening();
    }
}
```

Check `manager.Audio.RequiresUserGesture`, `CanEnableAudioPlayback`, and `IsAudioPlaybackActive` when deciding whether the button is needed and when to dismiss its overlay. For playback only, call `manager.Audio.EnableAudioPlayback()`. A session with microphone capture disabled still uses the normal browser playback unlock when required.

## Vision on WebGL

In 5.0, **Convai Vision Publisher > WebGL Publishes > Frame Source** publishes the configured source. **Game View** explicitly publishes the visible Unity canvas, including chat, menus and other UI. With Frame Source selected but no source assigned or discovered, the publisher falls back to the Game view. A source implementing `IVisionPageCanvasSource` publishes its own page canvas.

| Setting | WebGL behavior |
| --- | --- |
| Frame Source with a supported source | Publishes the source's picture. |
| Game View | Publishes the Unity canvas; does not start the assigned frame source. |
| Frame Source with no source | Falls back to the Unity canvas, including UI. |
| Publish Frame Rate Override | `0` follows policy; explicit overrides range up to 30 fps. |
| Default policy rates | Auto Compatible 10 fps, High Responsiveness 15 fps, Low Overhead 5 fps. |

To publish a physical webcam with `WebcamVisionFrameSource`, request camera access with `Application.RequestUserAuthorization(UserAuthorization.WebCam)` and wait for permission before starting the source. Serve the build from HTTPS or `localhost`. See [Unity’s WebCamTexture API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/WebCamTexture.html) and [Vision in WebGL](../features/vision/webgl.md).

Texture publishing uses the WebGL 2 graphics path or asynchronous GPU readback on other graphics backends that support it. If the SDK reports that it cannot read the configured source’s texture, use a WebGL 2 build or choose **Game View** when publishing the visible Unity canvas is appropriate.

For a texture source, the publisher waits for a fresh frame before publishing and unpublishes if frames stall. A new frame allows it to publish again. The visible Game view and browser-owned page canvas paths do not use this texture-source stall check. See [WebGL vision](../features/vision/webgl.md).

## Microphone policy and playback

Set **Allow Microphone** off for a text-only ordinary room. It prevents opening the microphone; remote character voice remains a separate setting. A denied browser prompt does not have to end the session: present `audio.mic_permission_denied`, `audio.mic_unavailable` or `audio.mic_publish_failed` and allow typed input where the room supports it.

`ConvaiAudioOutput.Volume` and `IsMuted` control browser playback. Unity's distance rolloff and `AudioListener.volume` do not. iOS Safari controls nonzero media volume itself, although mute and zero volume still silence playback.

Push-to-talk release remains correlated on WebGL. The browser microphone lacks native capture drain, so the SDK keeps capturing for `ReleaseTailMs`, then mutes the published track and leaves it available for the next press. The tail does not confirm that the server received the last audio samples. Validate ordinary and group push-to-talk from the hosted build you plan to distribute.

## Build validation checklist

Before shipping a WebGL build, verify each item:

* [ ] WebGL is the active build target before building, including in CI or an automated build script
* [ ] Build is served over HTTPS or from `localhost` for testing
* [ ] If embedded in an iframe: embedding permissions allow microphone access for the frame
* [ ] Explicit Start button present (especially for UI-heavy scenes)
* [ ] Microphone permission prompt tested in Chrome, Firefox, and Safari
* [ ] Character audio confirmed playing (browser audio path — not `AudioSource`)
* [ ] Settings Panel shows the browser default microphone
* [ ] Lip-sync timing evaluated visually in-browser across a full conversation turn
* [ ] Vision response validated if Vision is enabled using the intended source, with no unintended UI in the published image

## Troubleshooting

| Symptom                                                       | Likely cause                                             | Fix                                                                                   |
| ------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Microphone never activates; character does not hear input     | Build is served over HTTP, not HTTPS                     | Serve the build over HTTPS. `localhost` is exempt.                                    |
| Microphone blocked in iframe; permission prompt never appears | Missing `allow="microphone"` on the `<iframe>` element   | Add `allow="microphone"` to the iframe tag on the embedding page.                     |
| Character audio is silent; no playback                        | No user gesture received before audio playback attempted | Add an explicit Start button wired to `ConvaiManager.Audio.EnableAudioAndStartListening()`. |
| Only Default Microphone appears in Settings Panel                | The browser controls device selection    | No fix needed. The browser permission prompt handles device selection.                |
| Microphone test fails or is unavailable                       | Not supported on WebGL                                   | Expected behavior — inform users that mic testing is unavailable on browser builds.   |
| No spatial audio; voices lack 3D positioning                  | Spatial audio not supported on WebGL                     | Expected. Consider communicating this in UI (e.g., headphone prompt).                 |

### Lip-sync timing

The WebGL path uses the browser media clock and measured voice onset. When the browser audio analyser detects silence, the SDK waits up to two seconds for audible speech before starting from a fallback time.

If speech and mouth motion diverge, confirm browser audio has been unlocked, inspect the lip-sync playback status and test several complete turns in the target hosting environment. Record the browser, device and reproduction; native Editor playback is not evidence for browser timing.

### Build target mismatch

The SDK build guard rejects builds across the WebGL and native boundary when the Editor target differs. Switch to the intended Build Profile. For automation, start Unity with `-buildTarget WebGL` or call `EditorUserBuildSettings.SwitchActiveBuildTarget` before building.

## Next steps

Use the checklist as a browser validation baseline, then complete your application's deployment checks. If you are also deploying to iOS, Android, or XR headsets, those platforms have their own permission requirements.

{% content-ref url="ios-and-android.md" %}
[iOS and Android](ios-and-android.md)
{% endcontent-ref %}

{% content-ref url="xr-headsets.md" %}
[XR headsets](xr-headsets.md)
{% endcontent-ref %}
