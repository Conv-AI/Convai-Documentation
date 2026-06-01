---
title: Compatibility and requirements
description: What you need before installing the Convai Unreal Engine plugin: UE 5.x, a Convai account with an API key, and the AudioCapture dependency.
last_reviewed: "4.0.0-beta.21"
---

This section covers every requirement for running the Convai Unreal Engine plugin {{ unreal_plugin_version }} in a UE 5.x project, including engine version support, platform targets, and character rig compatibility.

## In this section

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Unreal Engine versions</strong><br>Supported UE 5.x range, module availability notes per version, and known per-version caveats.</td>
<td><a href="unreal-engine-versions.md">unreal-engine-versions.md</a></td>
</tr>
<tr>
<td><strong>Platform support matrix</strong><br>Win64 and Android build targets, required plugin dependencies, and Android microphone permission handling.</td>
<td><a href="platform-support-matrix.md">platform-support-matrix.md</a></td>
</tr>
<tr>
<td><strong>Character rig support</strong><br>Which character rigs work out of the box, which need additional setup, and links to the rig setup guides.</td>
<td><a href="character-rig-support.md">character-rig-support.md</a></td>
</tr>
</tbody>
</table>

## Minimum requirements at a glance

| Requirement | Minimum |
|---|---|
| Unreal Engine | {{ unreal_min_version }} (any UE 5.x release) |
| Convai account | Required — create one at {{ dashboard_url }} |
| API key | Required — generated in the Convai dashboard |
| AudioCapture plugin | Bundled engine plugin; enabled automatically as a dependency |
| AndroidPermission plugin | Bundled engine plugin; required for Android builds only |
| Build target | Win64 or Android |

## Next steps

Once your environment meets these requirements, install the plugin by following the Getting Started section.
