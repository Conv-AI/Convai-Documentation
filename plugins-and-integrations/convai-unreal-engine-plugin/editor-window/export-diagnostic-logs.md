---
title: Export diagnostic logs
description: Package engine logs, crash reports, and diagnostics into a ZIP file from the Convai editor window to attach to a support request.
last_reviewed: "4.0.0-beta.21"
---

The Convai editor window includes a log-export action that collects engine logs, crash reports, network diagnostics, performance metrics, and system information into a single ZIP archive. Use it when filing a support request or bug report.

## Prerequisites

- Convai Unreal Engine plugin installed and enabled.
- Signed in through the Convai editor window (see [Sign in and manage your account](sign-in-and-account.md)).

## Export the logs

{% stepper %}
{% step %}
### Open the Convai editor window

Click **Convai Editor** in the Level Editor toolbar, or select **Window > Convai > Open Convai Editor**.
{% endstep %}

{% step %}
### Click the settings icon

Click the **⚙️** icon in the top-right corner of the editor window. A dropdown appears with **Export Logs** and **Check for Updates**.

<figure><img src="../../../.gitbook/assets/TODO-convai-editor-settings-dropdown.png" alt="The settings dropdown in the Convai editor window showing Export Logs and Check for Updates options"><figcaption><p>TODO: Replace with screenshot of the ⚙️ settings dropdown showing the Export Logs option.</p></figcaption></figure>
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

The export runs in the background. A progress notification **Exporting Logs…** appears in the editor.

{% hint style="success" %}
When the export is complete, the notification updates to confirm the file count and size. The system file explorer opens automatically to the folder containing the ZIP archive.
{% endhint %}

## What the archive contains

| Item | Notes |
|---|---|
| Engine logs | Logs from the last 24 hours |
| Crash logs | Unreal Engine crash reports |
| Network diagnostics | Connectivity and latency information |
| Performance metrics | CPU, memory, and frame-time data |
| Project info | Project name, engine version, plugin version |
| System info | OS, hardware, and driver details |
| Screenshots | Captured at export time if available |

{% hint style="info" %}
The ZIP file is created on your local machine. Attach it to your support ticket or forum post — it is not uploaded automatically.
{% endhint %}

## Troubleshooting

### The export fails

**Symptom:** The progress notification changes to **Log Export Failed**.

**Cause:** A disk-write error, insufficient disk space, or a missing log directory.

**Fix:** Ensure the project directory is writable and that you have enough free disk space. Try the export again. If the problem persists, manually collect logs from `<ProjectRoot>/Saved/Logs/` and attach them to your support ticket.

### The privacy notice does not appear

**Symptom:** Clicking **Export Logs** starts the export immediately without showing a privacy notice dialog.

**Cause:** The privacy notice was already accepted in a previous export.

**Fix:** No action required — the export proceeds normally.

## Next steps

{% content-ref url="../troubleshooting/README.md" %}
[Troubleshooting](../troubleshooting/README.md)
{% endcontent-ref %}
