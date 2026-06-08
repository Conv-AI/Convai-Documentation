---
title: Platform support matrix
description: Reference for Convai Unreal Engine plugin platform support, including build targets, engine plugin dependencies, and Android setup requirements.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin supports Win64 and Android build targets.

## Supported platforms

| Platform | Runtime support | Editor support | Notes |
|---|---|---|---|
| Win64 | ✅ Full | ✅ Yes | Full feature set; no additional setup required. |
| Android | ✅ Full | ❌ No | Requires microphone permission handling; see below. |
| Other platforms | ❌ Not supported | ❌ Not supported | Not supported in this release. |

{% hint style="info" %}
Mac, Linux, and iOS are not supported in the current release.
{% endhint %}

## Engine plugin dependencies

The Convai plugin declares the following engine plugin dependencies. These are enabled automatically when the Convai plugin is active; you do not need to enable them manually.

| Dependency | Enabled by default | Required for |
|---|---|---|
| `AudioCapture` | ✅ Yes | Microphone input on Win64 and Android |
| `AndroidPermission` | ✅ Yes | Requesting microphone permission at runtime on Android |
| `EditorScriptingUtilities` | ✅ Yes | In-editor automation used by the Convai editor window |
| `PropertyAccessEditor` | ✅ Yes | Property-binding UI in the Convai editor window |
| `AndroidFileServer` | ❌ No | Optional file serving for Android development; not required for shipping |

## Android platform notes

Android builds require microphone access. The plugin uses the `AndroidPermission` dependency to request the `RECORD_AUDIO` permission at runtime. The Convai subsystem requests the permission automatically when it first needs the microphone, so you do not need to add a separate permission call in Blueprint.

{% hint style="warning" %}
Packaging for Android requires the Android SDK and NDK configured in **Project Settings > Platforms > Android SDK**. This is a standard Unreal Engine packaging requirement and is not specific to the Convai plugin.
{% endhint %}

## Next steps

With platform dependencies confirmed, check which character rigs are compatible with the plugin.

{% content-ref url="character-rig-support.md" %}
[Character rig support](character-rig-support.md)
{% endcontent-ref %}
