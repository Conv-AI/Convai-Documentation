# Troubleshooting

This section covers problems that occur at the SDK level — before or during the connection to Convai — regardless of which features you are using. If the SDK connects successfully but a specific feature like Actions, Emotion, or Vision is not working as expected, the troubleshooting page inside that feature's section is the right starting point.

The pages here address four categories of general issues: package installation and import, API key and connection failures, audio and microphone problems, and the full suite of built-in diagnostic tools.

***

{% hint style="info" %}
**Not sure where to start?** Open the Unity Console and look for the first error or warning tagged with `[Convai]`. If the message contains an error code in dot-notation format — for example `connection.connect_invalid_api_key` or `audio.mic_permission_denied` — go directly to the page that matches its prefix. If you see a plain English message from `Convai Bootstrapper`, start with Installation & Package Issues.
{% endhint %}

***

## What Is Covered Here

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Installation &#x26; Package Issues</strong><br>Package import failures, missing dependencies, ConvaiSettings not found, API key warning at startup.</td><td><a href="/broken/pages/e20dbff6dcf8de8a5f20569963ea508d58e9c486">Broken link</a></td></tr><tr><td><strong>Connection &#x26; API Issues</strong><br>API key rejections, character not found, timeout, rate limiting, transport errors, retry behavior, and runtime diagnostics.</td><td><a href="/broken/pages/93b13085426d96b61f8772c1e0cb789eaaae382c">Broken link</a></td></tr><tr><td><strong>Audio &#x26; Microphone Issues</strong><br>Microphone permission failures, unavailable devices, audio publish errors, and platform-specific setup for Android, iOS, and WebGL.</td><td><a href="/broken/pages/32887ee2a148ad21dd8669ac67bc349b5ecd25af">Broken link</a></td></tr><tr><td><strong>Debug Tools Reference</strong><br>Logging configuration, log categories, ConvaiActionDebugProbe, session diagnostics, latency metrics, and custom log sinks.</td><td><a href="/broken/pages/8e2f054437e02e724e4a7f0920fbfd49d6e1de52">Broken link</a></td></tr></tbody></table>

***

## Feature-Specific Troubleshooting

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

## Next Steps

When a problem is hard to diagnose from a single error message, start with the debug tools. Enabling verbose logging for a specific category and reading the `ConvaiRoomManager` runtime state narrows down most issues in minutes.

{% content-ref url="/broken/pages/8e2f054437e02e724e4a7f0920fbfd49d6e1de52" %}
[Broken link](/broken/pages/8e2f054437e02e724e4a7f0920fbfd49d6e1de52)
{% endcontent-ref %}
