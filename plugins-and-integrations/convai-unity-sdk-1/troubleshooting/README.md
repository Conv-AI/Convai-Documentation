---
description: >-
  Diagnose and fix Convai Unity SDK issues using the console error code system,
  platform-specific audio guides, and built-in debug tools.
---

# Troubleshooting

### SDK-Level Troubleshooting

This section covers problems that occur at the SDK level — before or during the connection to Convai — regardless of which features you are using. If the SDK connects successfully but a specific feature like Actions, Emotion, or Vision is not working as expected, the troubleshooting page inside that feature's section is the right starting point.

The pages here address four categories of general issues: package installation and import, API key and connection failures, audio and microphone problems, and the full suite of built-in diagnostic tools.

***

{% hint style="info" %}
**Not sure where to start?** Open the Unity Console and look for the first error or warning tagged with `[Convai]`. If the message contains an error code in dot-notation format — for example `connection.connect_invalid_api_key` or `audio.mic_permission_denied` — go directly to the page that matches its prefix. If you see a plain English message from `Convai Bootstrapper`, start with Installation & Package Issues.
{% endhint %}

***

### Troubleshooting Categories

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Installation &#x26; Package Issues</strong><br>Package import failures, missing dependencies, ConvaiSettings not found, and API key warnings at startup.</td><td><a href="/broken/pages/196d320838999c2eaa9874672a5b76829f6dfa37">Broken link</a></td></tr><tr><td><strong>Connection &#x26; API Issues</strong><br>API key rejections, character not found, timeout, rate limiting, transport errors, retry behavior, and runtime diagnostics.</td><td><a href="/broken/pages/8123f896927e80b6d89f50754db09fa85f9a6fe5">Broken link</a></td></tr><tr><td><strong>Audio &#x26; Microphone Issues</strong><br>Microphone permission failures, unavailable devices, audio publish errors, and platform-specific setup for Android, iOS, and WebGL.</td><td><a href="/broken/pages/6aff087fae4fc4fc266f55714a1824b8f8418325">Broken link</a></td></tr><tr><td><strong>Debug Tools Reference</strong><br>Logging configuration, log categories, ConvaiActionDebugProbe, session diagnostics, latency metrics, and custom log sinks.</td><td><a href="/broken/pages/16158cc3d1025b8e0607e5ee221361ecf96a2c7a">Broken link</a></td></tr></tbody></table>

***

### Feature-Specific Troubleshooting

Problems that occur after a successful connection — where the SDK is running but a specific feature behaves incorrectly — are documented inside each feature's own section.

| Feature            | Troubleshooting Page                                         |
| ------------------ | ------------------------------------------------------------ |
| Actions            | `features/actions/troubleshooting.md`                        |
| Emotion            | `features/emotion/troubleshooting.md`                        |
| Long-Term Memory   | `features/long-term-memory/troubleshooting.md`               |
| Dynamic Context    | `features/dynamic-context/troubleshooting.md`                |
| Narrative Design   | `features/narrative-design/troubleshooting.md`               |
| Vision             | `features/vision/troubleshooting.md`                         |
| Scene Metadata     | `features/scene-metadata/troubleshooting-and-diagnostics.md` |
| Dialogue Animation | `utilities/dialogue-animation/troubleshooting.md`            |
| Gaze & Attention   | `utilities/gaze-and-attention/troubleshooting.md`            |

***

### Next Steps

When a problem is hard to diagnose from a single error message, start with the debug tools. Enabling verbose logging for a specific category and reading the `ConvaiRoomManager` runtime state narrows down most issues in minutes.

{% content-ref url="/broken/pages/16158cc3d1025b8e0607e5ee221361ecf96a2c7a" %}
[Broken link](/broken/pages/16158cc3d1025b8e0607e5ee221361ecf96a2c7a)
{% endcontent-ref %}
