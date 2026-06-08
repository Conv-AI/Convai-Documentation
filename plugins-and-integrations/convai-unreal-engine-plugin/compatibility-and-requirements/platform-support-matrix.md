---
title: Platform support matrix
description: Reference for Convai Unreal Engine plugin platform support, including build targets, engine plugin dependencies, and Android setup requirements.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin <code class="expression">space.vars.unreal_plugin_version</code> supports two build targets: Win64 and Android. The runtime modules restrict their compiled output to these two platforms via the `PlatformAllowList` in the plugin manifest.

## Supported platforms

| Platform | Runtime support | Editor support | Notes |
|---|---|---|---|
| Win64 | ✅ Full | ✅ Yes | Full feature set; no additional setup required. |
| Android | ✅ Full | ❌ No | Requires microphone permission handling; see below. |
| Other platforms | ❌ Not supported | ❌ Not supported | Not listed in the plugin `PlatformAllowList`. |

{% hint style="info" %}
Mac, Linux, and iOS are not supported in the current release. The `Convai` and `ConvaiVisionBase` modules list only Win64 and Android in their `PlatformAllowList`, so they are excluded from builds for any other platform.
{% endhint %}

## Engine plugin dependencies

The Convai plugin declares the following engine plugin dependencies in `ConvAI.uplugin`. These are enabled automatically when the Convai plugin is active; you do not need to enable them manually.

| Dependency | Enabled by default | Required for |
|---|---|---|
| `AudioCapture` | ✅ Yes | Microphone input on Win64 and Android |
| `AndroidPermission` | ✅ Yes | Requesting microphone permission at runtime on Android |
| `EditorScriptingUtilities` | ✅ Yes | In-editor automation used by `ConvaiEditor` |
| `PropertyAccessEditor` | ✅ Yes | Property-binding UI in `ConvaiEditor` |
| `AndroidFileServer` | ❌ No | Optional file serving for Android development; not required for shipping |

## Android platform notes

Android builds require microphone access. The plugin bundles `AndroidPermission` as an enabled dependency and uses it to request the `RECORD_AUDIO` permission at runtime. The `UConvaiSubsystem` requests the permission automatically when it first needs the microphone, so you do not need to add a separate permission call in Blueprint.

{% hint style="warning" %}
Packaging for Android requires the Android SDK and NDK configured in **Project Settings > Platforms > Android SDK**. This is a standard Unreal Engine packaging requirement and is not specific to the Convai plugin.
{% endhint %}

## Modules and platform scope

The `PlatformAllowList` in the plugin manifest applies at the module level. The following modules are restricted to Win64 and Android:

- `Convai` (Runtime, `PreDefault`)
- `ConvaiVisionBase` (Runtime, `Default`)

The `ConvaiEditor` module has no `PlatformAllowList` because it loads only in the editor and is never part of a packaged runtime build. `ConvaiAnimGraph` is declared as `UncookedOnly` and also has no `PlatformAllowList`; the editor includes it, but packaging excludes it from the compiled output.

## Next steps

With platform dependencies confirmed, check which character rigs are compatible with the plugin.

{% content-ref url="character-rig-support.md" %}
[Character rig support](character-rig-support.md)
{% endcontent-ref %}
