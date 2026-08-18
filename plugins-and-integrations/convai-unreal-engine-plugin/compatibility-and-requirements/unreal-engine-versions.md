---
title: Unreal Engine versions
description: Reference for Convai Unreal Engine plugin version support, including module availability per UE version, load phases, and per-version setup notes.
last_reviewed: "4.0.0-beta.27"
---

The Convai Unreal Engine plugin <code class="expression">space.vars.unreal_plugin_version</code> supports Unreal Engine <code class="expression">space.vars.unreal_min_version</code> through UE <code class="expression">space.vars.unreal_max_version</code>. The plugin manifest declares five modules: runtime, editor, animation graph, vision, and toolset. The `ConvaiEditor` window is disabled automatically on UE 5.0 and 5.1; it is available on UE 5.2 and later. UE 5.8 support shipped in `4.0.0-beta.23` and the `ConvaiToolset` module in `4.0.0-beta.24`; every release since is smoke-tested on UE 5.6, 5.7, and 5.8.

## Supported versions

| UE version | Runtime (`Convai`) | `ConvaiEditor` | `ConvaiAnimGraph` | `ConvaiVisionBase` | `ConvaiToolset` |
|---|---|---|---|---|---|
| 5.0 | Supported | Window unavailable | Supported | Supported | Not available |
| 5.1 | Supported | Window unavailable | Supported | Supported | Not available |
| 5.2–5.7 | Supported | Supported | Supported | Supported | Loads with no AI-callable actions or MCP tooling |
| 5.8 | Supported | Supported | Supported | Supported | Supported, with AI-callable actions and MCP tooling active |

UE <code class="expression">space.vars.unreal_max_version</code> is the highest engine version the plugin currently supports. `ConvaiToolset` and the MCP tooling it backs only activate on UE 5.8 and later; on UE 5.0 through 5.7 the module still loads but exposes none of that functionality.

{% hint style="info" %}
The `ConvaiEditor` window requires UE 5.2 or later. On UE 5.0 and 5.1, the editor module logs `ConvaiEditor: Editor UI disabled - requires UE 5.2 or later` and exits the window setup path at startup.
{% endhint %}

## Module load phases

The plugin declares five modules. Their load phases determine when they become active during the editor or game startup sequence.

| Module | Type | Load phase |
|---|---|---|
| `Convai` | `Runtime` | `PreDefault` |
| `ConvaiEditor` | `Editor` | `PostEngineInit` |
| `ConvaiAnimGraph` | `UncookedOnly` | `Default` |
| `ConvaiVisionBase` | `Runtime` | `Default` |
| `ConvaiToolset` | `Editor` | `PostEngineInit` |

`ConvaiAnimGraph` is `UncookedOnly`, which means it is available for editor-time animation graph work but should not be treated as runtime module code in packaged builds. `ConvaiToolset` builds only for Editor targets; it is not present in packaged builds on any engine version.

## Version-specific notes

### UE 5.0 and 5.1

The `ConvaiEditor` window is unavailable on these versions. Use Blueprint-based runtime setup and Project Settings configuration instead of the in-editor Convai window.

### UE 5.8

UE 5.8 is required for the Convai Toolset's AI-callable editor actions and for MCP support. On earlier supported versions (5.2 through 5.7), the `ConvaiToolset` module still loads, but the engine's `ToolsetRegistry` plugin and the reflection types the toolset depends on do not exist below 5.8, so no AI-callable actions or MCP tooling are available.

## Next steps

With your engine version confirmed, check which build platforms the plugin supports.

{% content-ref url="unreal-engine-platform-support-matrix.md" %}
[Unreal Engine platform support matrix](unreal-engine-platform-support-matrix.md)
{% endcontent-ref %}
