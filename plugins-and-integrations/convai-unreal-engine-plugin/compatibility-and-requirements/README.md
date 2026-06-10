---
title: Compatibility and requirements
description: Find the Unreal Engine version support, platform targets, character rig compatibility, and network requirements for the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

Confirm your environment meets these requirements before installing the Convai Unreal Engine plugin <code class="expression">space.vars.unreal_plugin_version</code>. The pages below cover Unreal Engine version support, platform targets, character rig compatibility, and network requirements.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Unreal Engine versions</strong><br>Supported Unreal Engine range, module availability per version, and known per-version caveats.</td>
<td><a href="unreal-engine-versions.md">unreal-engine-versions.md</a></td>
</tr>
<tr>
<td><strong>Unreal Engine platform support matrix</strong><br>Win64 and Android build targets, required plugin dependencies, and Android microphone permission handling.</td>
<td><a href="unreal-engine-platform-support-matrix.md">unreal-engine-platform-support-matrix.md</a></td>
</tr>
<tr>
<td><strong>Character rig support</strong><br>Which character rigs work out of the box, which need additional setup, and links to the rig setup guides.</td>
<td><a href="character-rig-support.md">character-rig-support.md</a></td>
</tr>
<tr>
<td><strong>Network and API requirements</strong><br>Required domains, protocols, ports, and firewall rules for runtime plugin operation.</td>
<td><a href="network-and-api-requirements.md">network-and-api-requirements.md</a></td>
</tr>
</tbody>
</table>

## Minimum requirements at a glance

| Requirement | Minimum |
|---|---|
| Unreal Engine | <code class="expression">space.vars.unreal_min_version</code> minimum |
| Convai account | Required — create one at <code class="expression">space.vars.dashboard_url</code> |
| API key | Required for standard setup — generated in the Convai dashboard |
| `AudioCapture` plugin | Bundled engine plugin; enabled automatically as a dependency |
| `AndroidPermission` plugin | Bundled engine plugin; required for Android builds only |
| Build target | `Win64` or `Android` |

## Next steps

Once your environment meets these requirements, install the plugin.

{% content-ref url="../getting-started/install-the-convai-plugin.md" %}
[Install the Convai Unreal Engine plugin](../getting-started/install-the-convai-plugin.md)
{% endcontent-ref %}
