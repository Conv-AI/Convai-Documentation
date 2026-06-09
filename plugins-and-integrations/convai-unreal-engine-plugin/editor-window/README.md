---
title: The Convai editor window
description: Open the Convai editor window, understand its main sections, and find account, update, support, and log export workflows.
last_reviewed: "4.0.0-beta.21"
---

The Convai editor window is a floating Unreal Editor window for account connection, API key management, update checks, support links, and diagnostic log export. Use it after installing the Convai Unreal Engine plugin to connect the project to Convai and collect support information without leaving the editor.

{% hint style="info" %}
The Convai editor window requires Unreal Engine 5.2 or later. On earlier Unreal Engine 5 versions, the editor module loads without the full window UI.
{% endhint %}

## How to open the window

Two entry points are available:

- Select **Window > Convai > Open Convai Editor** from the Unreal Editor menu bar.
- Click **Convai Editor** in the Level Editor toolbar.

The window opens as a standalone floating window. If the welcome flow has not been completed, the plugin shows the **Welcome to Convai** screen first.

## Window sections

The header contains routed pages, hover menus, and window controls.

| Section | What it shows |
|---|---|
| **Home** | Dashboard, configurations, Convai Experiences, announcements, changelogs, latest YouTube content, and characters detected in the current level |
| **Samples** | Hover menu that currently shows a **Coming Soon** message for sample projects and templates |
| **Features** | Hover menu that currently shows a **Coming Soon** message for feature shortcuts |
| **Account** | API key field, plan information, quota renewal, and per-feature usage bars |
| **Support** | Documentation, YouTube Tutorials, and Convai Developer Forum cards |

The account icon opens an account menu. The settings icon in the top-right corner opens **Export Logs** and **Check for Updates**.

## Connect the project

The welcome screen starts with **Connect Convai Account**. The login flow opens a Convai authentication window and stores the API key after authentication completes. You can review or edit the stored key later from the **Account** section.

See [Sign in and manage your account](sign-in-and-account.md) for the full setup path.

## Update and support tools

Use the settings menu when you need to check whether a newer plugin release is available or collect diagnostics for support.

| Tool | Where to find it | Use it when |
|---|---|---|
| **Check for Updates** | Settings icon | You want to compare the installed plugin version with the latest GitHub release |
| **Export Logs** | Settings icon | You need to attach Unreal Engine logs, crash reports, config files, and diagnostics to a support request |
| **Convai Developer Forum** | **Support** section | You want to share a reproducible issue and the exported log package with Convai support or the developer community |

## Related pages

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Sign in and manage your account</strong><br>Complete the welcome flow and review your plan and usage quotas.</td>
<td><a href="sign-in-and-account.md">sign-in-and-account.md</a></td>
</tr>
<tr>
<td><strong>Browse samples and content</strong><br>Check the current Samples area and understand what will be added in future plugin updates.</td>
<td><a href="browse-samples-and-content.md">browse-samples-and-content.md</a></td>
</tr>
<tr>
<td><strong>Export diagnostic logs</strong><br>Package engine logs and diagnostics into a local archive for support requests.</td>
<td><a href="export-diagnostic-logs.md">export-diagnostic-logs.md</a></td>
</tr>
</tbody>
</table>
