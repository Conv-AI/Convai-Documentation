---
title: Export diagnostic logs
description: Export Convai diagnostics from Unreal Editor and attach the generated log package to a Convai Developer Forum support request.
last_reviewed: "4.0.0-beta.21"
---

The Convai editor window includes support tools for checking plugin updates and exporting diagnostics. Use **Export Logs** before posting on the Convai Developer Forum so your report includes Unreal Engine logs, Convai plugin logs, crash reports, configuration files, and environment details.

## Prerequisites

- Convai Unreal Engine plugin installed and enabled in Unreal Engine 5.2 or later. The full Convai editor window UI is not available on earlier Unreal Engine 5 versions.
- Convai editor window available from **Window > Convai > Open Convai Editor** or the **Convai Editor** toolbar button.
- A reproducible issue, error message, or support question to share with Convai support.

## Check for plugin updates

Before exporting logs, check whether a newer plugin release is available. The update check compares your installed plugin version with the latest GitHub release.

{% stepper %}
{% step %}
### Open the settings menu

Open the Convai editor window and click the settings icon in the top-right corner.
{% endstep %}

{% step %}
### Click Check for Updates

Click **Check for Updates**. Unreal Editor shows a notification while the plugin checks GitHub.
{% endstep %}

{% step %}
### Review the result

If an update is available, the notification shows your current version, the available version, and a link to the release page. If no update is available, the notification confirms that the current stable version is installed.
{% endstep %}
{% endstepper %}

## Export the logs

{% stepper %}
{% step %}
### Open the Convai editor window

Click **Convai Editor** in the Level Editor toolbar, or select **Window > Convai > Open Convai Editor**.
{% endstep %}

{% step %}
### Click the settings icon

Click the **⚙️** icon in the top-right corner of the editor window. A dropdown appears with **Export Logs** and **Check for Updates**.
{% endstep %}

{% step %}
### Click Export Logs

Click **Export Logs** in the dropdown.
{% endstep %}

{% step %}
### Accept the privacy notice

A privacy notice dialog titled **Export Logs - Privacy Notice** appears. Review the notice and accept it to proceed. If you decline, the export is cancelled.
{% endstep %}
{% endstepper %}

The export runs in the background. A progress notification appears with **Exporting Logs... Please wait while we package your log files.**

{% hint style="success" %}
When the export completes, the notification changes to **Logs Exported Successfully** and shows the file count and archive size. The system file explorer opens to the generated package location. If it does not open, check `<ProjectRoot>/Saved/ConvaiLogExports/`.
{% endhint %}

## What the archive contains

| Item | Notes |
|---|---|
| Convai plugin logs | Recent `.log` files from `<ProjectRoot>/Saved/ConvaiLogs/` |
| Unreal Engine logs | Recent `.log` files from `<ProjectRoot>/Saved/Logs/` |
| Crash reports | `.log`, `.txt`, and `.xml` files from up to five recent folders under `<ProjectRoot>/Saved/Crashes/` |
| Config files | Selected project and plugin config files, including `DefaultEngine.ini`, `DefaultGame.ini`, and `ConvaiEditorSettings.ini` when present |
| Project info | Project name, Unreal Engine version, plugin metadata, and project configuration |
| System info | Operating system, CPU, GPU, RAM, screen, locale, and language information |
| Network and performance data | Network adapter information, session uptime, FPS, and memory usage statistics |

{% hint style="info" %}
The export package is created on your local machine. It is not uploaded automatically. Review your support post before attaching the file.
{% endhint %}

## Share the package on the Developer Forum

Open the Convai editor window, click **Support**, and choose **Convai Developer Forum**. When you create a forum post, include:

- Unreal Engine version and Convai plugin version.
- What you expected to happen.
- What happened instead.
- The smallest set of steps that reproduces the issue.
- Any exact Output Log message shown in Unreal Editor.
- The exported log package from **Export Logs**.

## Troubleshooting

### The export fails

**Symptom:** The progress notification changes to **Log Export Failed**.

**Cause:** The exporter could not create the package folder, copy collected files, write the manifest, write metadata, or create the archive.

**Fix:** Ensure the project `Saved/` directory is writable, then try the export again. If the problem persists, manually collect logs from `<ProjectRoot>/Saved/Logs/` and attach them to your support ticket.

**Verify:** The notification changes to **Logs Exported Successfully** and the file explorer opens to the package location.

### No log files are found

**Symptom:** The export fails with `No log files found to export`.

**Cause:** The exporter found no files to package from recent Convai logs, Unreal Engine logs, crash reports, or selected config files.

**Fix:** Reproduce the issue once in the editor, save the project if needed so config files exist, then run **Export Logs** again.

**Verify:** The generated package contains log files and metadata.

### Update check fails

**Symptom:** The notification shows **Update Check Failed**.

**Cause:** Unreal Editor cannot reach GitHub releases, or the update check service could not complete the request.

**Fix:** Confirm your internet connection and allow Unreal Editor to access GitHub over HTTPS. Retry **Check for Updates**.

**Verify:** The notification either reports an available update or confirms that the installed version is current.

## Next steps

{% content-ref url="../troubleshooting/README.md" %}
[Troubleshooting](../troubleshooting/README.md)
{% endcontent-ref %}

{% content-ref url="../troubleshooting/diagnostics-and-log-export.md" %}
[Diagnostics and log export](../troubleshooting/diagnostics-and-log-export.md)
{% endcontent-ref %}
