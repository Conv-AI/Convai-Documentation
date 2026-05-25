---
title: Troubleshooting
description: Find troubleshooting guides for installation errors, API issues, audio failures, and debug tools in the Convai Unity SDK.
last_reviewed: "4.2.0"
---

This section covers problems that occur at the SDK level — before or during the connection to Convai — regardless of which features you are using. If the SDK connects successfully but a specific feature like Actions, Emotion, or Vision is not working as expected, start with the troubleshooting page inside that feature's section. The pages here address four categories of general issues: package installation and import, API key and connection failures, audio and microphone problems, and the full suite of built-in diagnostic tools.

{% hint style="info" %}
**Not sure where to start?** Open the Unity Console and look for the first error or warning tagged with `[Convai]`. If the message contains an error code in dot-notation format — for example `connection.connect_invalid_api_key` or `audio.mic_permission_denied` — go directly to the page that matches its prefix. If you see a plain English message from `Convai Bootstrapper`, start with Installation & Package Issues.
{% endhint %}

## Troubleshooting categories

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Installation and package issues</strong><br>Package import failures, missing dependencies, ConvaiSettings not found, and API key warnings at startup.</td><td><a href="installation-and-package-issues.md">installation-and-package-issues.md</a></td></tr><tr><td><strong>Connection and API issues</strong><br>API key rejections, character not found, timeout, rate limiting, transport errors, retry behavior, and runtime diagnostics.</td><td><a href="connection-and-api-issues.md">connection-and-api-issues.md</a></td></tr><tr><td><strong>Audio and microphone issues</strong><br>Microphone permission failures, unavailable devices, audio publish errors, and platform-specific setup for Android, iOS, and WebGL.</td><td><a href="audio-and-microphone-issues.md">audio-and-microphone-issues.md</a></td></tr><tr><td><strong>Debug tools reference</strong><br>Logging configuration, log categories, ConvaiActionDebugProbe, session diagnostics, latency metrics, and custom log sinks.</td><td><a href="debug-tools-reference.md">debug-tools-reference.md</a></td></tr></tbody></table>

## Feature-specific troubleshooting

Problems that occur after a successful connection — where the SDK is running but a specific feature behaves incorrectly — are documented inside each feature's own section.

| Feature | Troubleshooting page |
| --- | --- |
| Actions | `features/actions/troubleshooting.md` |
| Emotion | `features/emotion/troubleshooting.md` |
| Long-Term Memory | `features/long-term-memory/troubleshooting.md` |
| Dynamic Context | `features/dynamic-context/troubleshooting.md` |
| Narrative Design | `features/narrative-design/troubleshooting.md` |
| Vision | `features/vision/troubleshooting.md` |
| Scene Metadata | `features/scene-metadata/troubleshooting-and-diagnostics.md` |
| Dialogue Animation | `utilities/dialogue-animation/troubleshooting.md` |
| Gaze & Attention | `utilities/gaze-and-attention/troubleshooting.md` |

## Next steps

When a problem is hard to diagnose from a single error message, start with the debug tools. Enabling verbose logging for a specific category and reading the `ConvaiRoomManager` runtime state narrows down most issues in minutes.

{% content-ref url="debug-tools-reference.md" %}
[Debug tools reference](debug-tools-reference.md)
{% endcontent-ref %}
