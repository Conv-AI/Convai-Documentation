---
title: Troubleshooting
description: Find fixes for installation, API key, audio, lip sync, and connection problems in the Convai Unreal Engine plugin, plus log export and diagnostic guidance.
last_reviewed: 2026-06-06
---

This section covers problems that occur at the plugin level: installation, authentication, session startup, microphone capture, general lip sync setup, and diagnostics. If the Convai Unreal Engine plugin connects successfully but one feature behaves incorrectly, start with that feature's troubleshooting page.

{% hint style="info" %}
**Not sure where to start?** Open the Unreal Editor Output Log (**Window > Output Log**) and look for the first Convai error or warning. Use the log category as the route: `LogConvai` or `LogConvaiEditor` → Installation and plugin issues; `ConvaiConnectionManagerLog`, `ConvaiSubsystemLog`, or `ConvaiChatbotComponentLog` → Connection and API key issues; `ConvaiAudioLog`, `ConvaiAudioStreamerLog`, or `ConvaiPlayerLog` → Audio and microphone issues; `ConvaiFaceSyncLog` → Lip sync and animation issues. If no Convai category appears, start with Installation and plugin issues.
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
| Lip sync | [Troubleshoot lip sync](../features/lip-sync/troubleshooting-and-diagnostics.md) |
| Character actions | [Troubleshoot character actions](../features/character-actions/troubleshooting-and-diagnostics.md) |
| Emotion | [Troubleshoot emotion](../features/emotion/troubleshooting-and-diagnostics.md) |
| Gaze attention | [Troubleshoot gaze attention](../features/gaze-attention/troubleshooting-and-diagnostics.md) |
| Narrative design | [Troubleshoot narrative design](../features/narrative-design/troubleshooting-and-diagnostics.md) |
| Dynamic context | [Troubleshoot dynamic context](../features/dynamic-context/troubleshooting-and-diagnostics.md) |
| Long-term memory | [Troubleshoot long-term memory](../features/long-term-memory/troubleshooting-and-diagnostics.md) |
| Vision | [Troubleshoot vision](../features/vision/troubleshooting-and-diagnostics.md) |
| Scene metadata | [Troubleshoot scene metadata](../features/scene-metadata/troubleshooting-and-diagnostics.md) |

## Next steps

When a problem is hard to diagnose from a single error message, enable verbose logging for the relevant category and inspect the Output Log. The diagnostics page also explains where Unreal writes logs and how to create a shareable support package from the Convai editor window.

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
