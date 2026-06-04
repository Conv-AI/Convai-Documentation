---
title: The Convai editor window
description: Understand the Convai editor window — what each section does, how to open it, and how the first-time sign-in flow works.
last_reviewed: "4.0.0-beta.21"
---

The Convai editor window is a docked panel inside Unreal Editor that centralises account management, character browsing, sample content, documentation access, and diagnostic tools for the Convai Unreal Engine plugin. It is provided by the `ConvaiEditor` module and requires Unreal Engine 5.2 or later.

## How to open the window

Two entry points are available:

- **Menu bar:** select **Window > Convai > Open Convai Editor**.
- **Toolbar button:** click the **Convai Editor** button in the Level Editor toolbar (beside the Play controls).

The window opens as a standard dockable Unreal Editor tab. If you have not signed in yet, the welcome flow launches immediately.

## Window sections

The window has a navigation sidebar on the left. Each entry routes to a different section.

| Section | What it shows |
|---|---|
| **Home** | Announcements, changelogs, characters present in the current level, and the latest Convai YouTube video |
| **Dashboard** | Integrated web view of your convai.com dashboard |
| **Experiences** | Integrated web view of the Experiences area on convai.com |
| **Documentation** | Integrated web view of Convai docs |
| **Forum** | Integrated web view of the Convai forum |
| **Samples** | Browseable list of sample projects and content items |
| **Account** | Account details, plan information, and per-feature usage quotas |
| **Support** | Support resources and the log-export dialog |
| **Settings** | Theme configuration for the window |

## First-time sign-in

The first time you open the window, a two-step welcome flow appears:

1. **Welcome screen** — an introductory screen that introduces the plugin.
2. **API key input** — enter your API key; the window validates it before storing it.

After completing the welcome flow the window opens to the Home section. Your API key is stored in `UConvaiSettings.API_Key`. See [Configure your API key](../getting-started/configure-api-key.md) for full sign-in instructions.

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
<td><strong>Browse samples and content</strong><br>Find and open sample projects from the Samples section of the window.</td>
<td><a href="browse-samples-and-content.md">browse-samples-and-content.md</a></td>
</tr>
<tr>
<td><strong>Export diagnostic logs</strong><br>Package engine logs and diagnostics into a ZIP file for support requests.</td>
<td><a href="export-diagnostic-logs.md">export-diagnostic-logs.md</a></td>
</tr>
</tbody>
</table>
