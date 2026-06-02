---
title: Unreal Engine versions
description: Supported UE 5.x versions for the Convai Unreal Engine plugin, with module availability notes and known per-version caveats.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin <code class="expression">space.vars.unreal_plugin_version</code> supports Unreal Engine <code class="expression">space.vars.unreal_min_version</code> and all later UE 5.x releases. There is no declared upper-bound version limit in the plugin manifest.

## Supported versions

| UE version | Runtime (`Convai`) | `ConvaiEditor` | `ConvaiAnimGraph` | `ConvaiVisionBase` |
|---|---|---|---|---|
| 5.0 | Supported | Not available | Supported | Supported |
| 5.1 | Supported | Not available | Supported | Supported |
| 5.2 and later | Supported | Supported | Supported | Supported |

{% hint style="info" %}
`ConvaiEditor` requires a property-binding editor feature that is not available in UE 5.1 and earlier. On those versions, the module is disabled automatically; the runtime and animation modules are unaffected.
{% endhint %}

## Module load phases

The plugin declares four modules. Their load phases determine when they become active during the editor or game startup sequence.

| Module | Type | Load phase |
|---|---|---|
| `Convai` | Runtime | `PreDefault` |
| `ConvaiEditor` | Editor | `PostEngineInit` |
| `ConvaiAnimGraph` | UncookedOnly | `Default` |
| `ConvaiVisionBase` | Runtime | `Default` |

`ConvaiAnimGraph` is `UncookedOnly`, which means it is available in the Unreal Editor but is not compiled into packaged builds. Animation graph assets that reference its nodes are cooked into the package, but the module code itself is editor-only.

## Version-specific notes

### UE 5.0

The plugin builds and runs on UE 5.0. Several compilation and compatibility issues were resolved for UE 5.0 (alongside UE 5.4, 5.5, and 5.7) so the plugin builds clean on all supported engine versions. The gaze-highlight material was also regenerated under UE 5.0 to ensure it loads correctly across all supported engine versions.

### UE 5.1 and earlier

The `ConvaiEditor` module is disabled on these versions. All Blueprint-based conversation, audio, and animation workflows remain fully functional. Only the in-editor Convai configuration window is unavailable; the API key must be set manually in **Project Settings > Plugins > Convai**.

### UE 5.4, 5.5, and 5.7

Release <code class="expression">space.vars.unreal_plugin_version</code> included compilation and compatibility fixes targeting these specific engine versions. No additional steps are required.

## Related reference

{% content-ref url="platform-support-matrix.md" %}
[Platform support matrix](platform-support-matrix.md)
{% endcontent-ref %}
