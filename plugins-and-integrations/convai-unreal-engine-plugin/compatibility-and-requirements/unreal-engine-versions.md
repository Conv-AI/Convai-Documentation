---
title: Unreal Engine versions
description: Reference for Convai Unreal Engine plugin version support, including module availability per UE version, load phases, and per-version setup notes.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin <code class="expression">space.vars.unreal_plugin_version</code> uses Unreal Engine <code class="expression">space.vars.unreal_min_version</code> as its documented minimum engine version. The plugin manifest declares the same runtime, editor, animation graph, and vision modules for the plugin package. The `ConvaiEditor` window is disabled automatically on UE 5.0 and 5.1; it is available on UE 5.2 and later.

## Supported versions

| UE version | Runtime (`Convai`) | `ConvaiEditor` | `ConvaiAnimGraph` | `ConvaiVisionBase` |
|---|---|---|---|---|
| 5.0 | Supported | Window unavailable | Supported | Supported |
| 5.1 | Supported | Window unavailable | Supported | Supported |
| 5.2 and later | Supported | Supported | Supported | Supported |

{% hint style="info" %}
The `ConvaiEditor` window requires UE 5.2 or later. On UE 5.0 and 5.1, the editor module logs `ConvaiEditor: Editor UI disabled - requires UE 5.2 or later` and exits the window setup path at startup.
{% endhint %}

## Module load phases

The plugin declares four modules. Their load phases determine when they become active during the editor or game startup sequence.

| Module | Type | Load phase |
|---|---|---|
| `Convai` | `Runtime` | `PreDefault` |
| `ConvaiEditor` | `Editor` | `PostEngineInit` |
| `ConvaiAnimGraph` | `UncookedOnly` | `Default` |
| `ConvaiVisionBase` | `Runtime` | `Default` |

`ConvaiAnimGraph` is `UncookedOnly`, which means it is available for editor-time animation graph work but should not be treated as runtime module code in packaged builds.

## Version-specific notes

### UE 5.0 and 5.1

The `ConvaiEditor` window is unavailable on these versions. Use Blueprint-based runtime setup and Project Settings configuration instead of the in-editor Convai window.

## Next steps

With your engine version confirmed, check which build platforms the plugin supports.

{% content-ref url="unreal-engine-platform-support-matrix.md" %}
[Unreal Engine platform support matrix](unreal-engine-platform-support-matrix.md)
{% endcontent-ref %}
