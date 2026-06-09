---
title: Unreal Engine platform support matrix
description: Reference for Convai Unreal Engine plugin platform support, including build targets, engine plugin dependencies, and Android microphone access.
last_reviewed: "4.0.0-beta.21"
---

Use this reference to confirm which build targets the Convai Unreal Engine plugin supports, which engine plugin dependencies it enables, and what Android microphone access requires before packaging.

## Supported platforms

| Platform | Runtime support | Editor support | Notes |
|---|---|---|---|
| `Win64` | Supported | Yes | Supported by the `Convai` and `ConvaiVisionBase` module allowlists. |
| `Android` | Supported | No | Supported by the runtime module allowlists; requires microphone permission handling. |
| Other platforms | Not supported | Not supported | Not listed in the runtime module allowlists for this release. |

{% hint style="info" %}
macOS, Linux, and iOS are not supported in the current release.
{% endhint %}

## Engine plugin dependencies

The Convai plugin declares the following engine plugin dependencies. These are enabled automatically when the Convai plugin is active; you do not need to enable them manually.

| Dependency | Enabled by default | Required for |
|---|---|---|
| `AudioCapture` | Yes | Microphone input on Win64 and Android |
| `AndroidPermission` | Yes | Requesting microphone permission at runtime on Android |
| `EditorScriptingUtilities` | Yes | Editor tooling dependency; no user configuration required |
| `PropertyAccessEditor` | Yes | `FConvaiTrackedProperty.PropertyPath` Bind picker and property-binding details UI |

## Android microphone permission

Android builds require microphone access. The plugin declares `android.permission.RECORD_AUDIO` and uses the `AndroidPermission` dependency to request that permission at runtime, so the standard plugin flow does not require a separate Blueprint permission request.

Android toolchain setup is outside this plugin-specific reference. This page only describes the Convai plugin dependencies and microphone permission handling visible in the plugin source.

## Next steps

With platform dependencies confirmed, check which character rigs are compatible with the plugin.

{% content-ref url="character-rig-support.md" %}
[Character rig support](character-rig-support.md)
{% endcontent-ref %}
