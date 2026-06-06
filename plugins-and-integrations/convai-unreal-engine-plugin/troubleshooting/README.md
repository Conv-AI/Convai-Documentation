---
title: Troubleshooting
description: Find fixes for installation, API key, audio, lip sync, and connection problems in the Convai Unreal Engine plugin, plus log export and diagnostic guidance.
last_reviewed: 2026-06-06
---

This section covers problems that occur at the plugin level — during installation, authentication, or audio capture — regardless of which features you are using. If the plugin connects successfully but a specific feature such as Lip Sync, Character Actions, or Vision is not working as expected, start with the troubleshooting page inside that feature's section. The pages here address five categories: plugin installation and load failures, API key and session errors, audio and microphone problems, lip sync and animation issues, and log export for self-diagnosis and support.

{% hint style="info" %}
**Not sure where to start?** Open the Unreal Editor Output Log (**Window > Output Log**) and look for the first error or warning. The log category prefix tells you which page to use: `ConvaiAudioLog` → Audio and microphone issues; `ConvaiChatbotComponentLog` → Connection and API key issues; `ConvaiFaceSyncLog` → Lip sync and animation issues; `LogConvai` or `LogConvaiEditorConfig` → Installation or connection issues. If you see no Convai entries at all, the plugin may not have loaded — start with Installation and plugin issues.
{% endhint %}

## Troubleshooting categories

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Installation and plugin issues</strong><br>Plugin not found, module load failures, Blueprint-only project limitations, and Android packaging errors.</td>
<td><a href="installation-and-plugin-issues.md">installation-and-plugin-issues.md</a></td>
</tr>
<tr>
<td><strong>Connection and API key issues</strong><br>Authentication failures, missing API key, session timeout errors, and firewall configuration.</td>
<td><a href="connection-and-api-key-issues.md">connection-and-api-key-issues.md</a></td>
</tr>
<tr>
<td><strong>Audio and microphone issues</strong><br>No audio input, wrong capture device, Android permission failures, and audio playback errors.</td>
<td><a href="audio-and-microphone-issues.md">audio-and-microphone-issues.md</a></td>
</tr>
<tr>
<td><strong>Lip sync and animation issues</strong><br>No mouth movement, wrong blendshape curves, frame starvation, and packaged build animation failures.</td>
<td><a href="lip-sync-and-animation-issues.md">lip-sync-and-animation-issues.md</a></td>
</tr>
<tr>
<td><strong>Diagnostics and log export</strong><br>Log categories, verbosity control, configuration defaults, Blueprint diagnostic nodes, and log file export for support.</td>
<td><a href="diagnostics-and-log-export.md">diagnostics-and-log-export.md</a></td>
</tr>
</tbody>
</table>

## Feature-specific troubleshooting

Problems that occur after the plugin connects successfully — where a specific feature behaves incorrectly — are documented inside each feature's own section.

| Feature | Troubleshooting page |
| --- | --- |
| Lip Sync | [Lip sync troubleshooting and diagnostics](../features/lip-sync/troubleshooting-and-diagnostics.md) |
| Character Actions | [Character actions troubleshooting](../features/character-actions/troubleshooting-and-diagnostics.md) |
| Emotion | [Emotion troubleshooting](../features/emotion/troubleshooting-and-diagnostics.md) |
| Gaze and Attention | [Gaze and attention troubleshooting](../features/gaze-attention/troubleshooting-and-diagnostics.md) |
| Narrative Design | [Narrative design troubleshooting](../features/narrative-design/troubleshooting-and-diagnostics.md) |
| Dynamic Context | [Dynamic context troubleshooting](../features/dynamic-context/troubleshooting-and-diagnostics.md) |
| Long-Term Memory | [Long-term memory troubleshooting](../features/long-term-memory/troubleshooting-and-diagnostics.md) |
| Vision | [Vision troubleshooting](../features/vision/troubleshooting-and-diagnostics.md) |
| Scene Metadata | [Scene metadata troubleshooting](../features/scene-metadata/troubleshooting-and-diagnostics.md) |

## Next steps

When a problem is hard to diagnose from a single error message, enable verbose logging for the relevant category and inspect the Output Log. The diagnostics page also covers the Convai Editor Window log export tool, which bundles logs and network diagnostics into a shareable package.

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
