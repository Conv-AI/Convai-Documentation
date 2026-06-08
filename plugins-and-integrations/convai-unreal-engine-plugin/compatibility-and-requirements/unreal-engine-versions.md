---
title: Unreal Engine versions
description: Reference for Convai Unreal Engine plugin version support, including module availability per UE version, load phases, and per-version setup notes.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin <code class="expression">space.vars.unreal_plugin_version</code> supports Unreal Engine <code class="expression">space.vars.unreal_min_version</code> and all later UE 5.x releases. All four plugin modules load on every supported version, but the `ConvaiEditor` window is available only on UE 5.2 and later. On UE 5.0 and 5.1 the editor window is disabled automatically; all runtime and animation workflows remain unaffected.

## Supported versions

| UE version | Runtime (`Convai`) | `ConvaiEditor` | `ConvaiAnimGraph` | `ConvaiVisionBase` |
|---|---|---|---|---|
| 5.0 | Supported | Window unavailable | Supported | Supported |
| 5.1 | Supported | Window unavailable | Supported | Supported |
| 5.2 and later | Supported | Supported | Supported | Supported |

{% hint style="info" %}
The `ConvaiEditor` window is built on editor UI APIs — `FAppStyle`, the modern `ToolMenus` system, and editor-initialization delegates — that the plugin enables only on UE 5.2 and later. On UE 5.0 and 5.1 the editor window is disabled automatically; the runtime and animation modules are unaffected.
{% endhint %}

## Module load phases

The plugin declares four modules. Their load phases determine when they become active during the editor or game startup sequence.

| Module | Type | Load phase |
|---|---|---|
| `Convai` | `Runtime` | `PreDefault` |
| `ConvaiEditor` | `Editor` | `PostEngineInit` |
| `ConvaiAnimGraph` | `UncookedOnly` | `Default` |
| `ConvaiVisionBase` | `Runtime` | `Default` |

`ConvaiAnimGraph` is `UncookedOnly`, which means it is available in the Unreal Editor but is not compiled into packaged builds. Animation graph assets that reference its nodes are cooked into the package, but the module code itself is editor-only.

## Version-specific notes

### UE 5.1 and earlier

The `ConvaiEditor` window is unavailable on these versions. All Blueprint-based conversation, audio, and animation workflows remain fully functional; only the in-editor Convai window does not load.

## Next steps

With your engine version confirmed, check which build platforms the plugin supports.

{% content-ref url="platform-support-matrix.md" %}
[Platform support matrix](platform-support-matrix.md)
{% endcontent-ref %}
