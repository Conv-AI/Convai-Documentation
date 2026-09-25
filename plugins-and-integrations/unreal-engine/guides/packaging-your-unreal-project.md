---
title: Host your Unreal project with Cloud Projects
description: Package and upload an Unreal project from the Convai plugin, manage its versions and runtime settings, and share the streamed experience.
last_reviewed: 2026-09-25
---

Use **Cloud Projects** to upload the open Unreal project and stream it in a browser.

## Before you begin

- Open the Unreal project with the Convai plugin enabled. Sign in when prompted.
- Install the Windows platform SDK. The plugin packages a `Win64` `Development` build.
- Install Unreal's Pixel Streaming plugin. Cloud Projects enables it for this project during preparation if needed.
- Keep enough disk space for the packaged build and its compressed archive.

## Create and upload a cloud project

{% stepper %}
{% step %}
### Open Cloud Projects

In Unreal Editor, select **Tools > Convai > Cloud Projects**. Sign in if prompted.
{% endstep %}

{% step %}
### Name the project

Select **+ New project**. Edit **PROJECT NAME** if needed; it starts with the open Unreal project's name.

<figure><img src="../../../.gitbook/assets/convai-cloud-projects-create-and-upload.png" alt="Cloud Projects upload form with a project name field and Create and upload button"><figcaption><p>Name the open Unreal project before starting its upload.</p></figcaption></figure>
{% endstep %}

{% step %}
### Start the upload

Select **Create and upload**. The panel shows the stage, progress, and elapsed time. The first package can take 30–45 minutes while Unreal cooks the project's assets. Unreal's packaging notification provides the packaging log.
{% endstep %}
{% endstepper %}

Cloud Projects runs these stages in order:

| Stage | What the plugin does |
| --- | --- |
| **Prepare** | Enables Pixel Streaming if needed and tries to add `ConvaiPSAudioCapture` to project-owned Blueprints with a Convai player component. |
| **Package** | Packages the open project as a `Win64` `Development` build. |
| **Compress** | Creates an archive from the packaged build. |
| **Upload** | Reserves a version and sends the archive to Convai. |
| **Cloud build** | Builds the uploaded version for streaming. |
| **Activate** | Requests that the new build serve the project. |

- Preparation may update `.uproject` and project-owned Blueprints under `/Game/`. It does not change plugin sample content.
- If Pixel Streaming was enabled during preparation, restart the Editor before testing it there.
- If `ConvaiPSAudioCapture` was unavailable, restart the Editor and select **Upload changes**.
- **Cancel** stops local packaging or upload. A cloud build continues after you close the tab.

## Check the project and open the stream

1. Select the project and use **Refresh** while it builds. **Live** means a build is available to stream.
2. Check **VERSIONS** for the **Active** version. The project list shows the newest upload, which may be different.
3. Select **Open in browser**. The plugin creates an experience page if needed and opens a stream session.
4. Check the stream. If the project uses a Convai character, test the browser microphone.

## Upload changes and manage versions

To update a project, select it and choose **Upload changes**. The plugin packages the open Unreal project and assigns the next version number. If its name differs from the selected cloud project's name, the panel shows a warning before upload.

In **VERSIONS**, check the build state, archive size, and rollout state:

| State | Meaning |
| --- | --- |
| **Uploaded** / **Building** | The archive is stored / the cloud build is running. |
| **Built** / **Build failed** | Ready to activate / open **Logs** to investigate. |
| **Active** | Serving viewers. |
| **Preparing** / **Waiting to start** | A rollout is in progress. |

<figure><img src="../../../.gitbook/assets/convai-cloud-projects-versions.png" alt="Cloud Projects Versions section showing three builds with Make active and Logs actions and a rollout waiting to start"><figcaption><p>Inspect each version's build and rollout state before activating it.</p></figcaption></figure>

- Select **Make active** on a built version to serve it. A new activation request replaces a pending one.
- Select **Cancel rollout and keep active** to retain the version currently serving.
- Select **Logs** on a version to inspect its build report.

## Change runtime settings

Select a project and scroll to **RUNTIME SETTINGS**. These settings control how its streamed process starts; changing them does not require a new package or archive upload.

<figure><img src="../../../.gitbook/assets/convai-cloud-projects-runtime-settings.png" alt="Cloud Projects runtime settings showing browser choices, Unreal resolution fields, advanced controls, and save actions"><figcaption><p>Browser and Unreal runtime settings for a selected project.</p></figcaption></figure>

Under **Browser**, each choice offers **Use runtime default**, **On**, and **Off**. **Use runtime default** omits the override; it does not force **Off**.

| Browser setting | Effect |
| --- | --- |
| `UseMic` | Enables browser microphone capture. |
| `HoveringMouse` | Sends pointer movement without locking the pointer. |
| `MatchViewportRes` | Matches the browser viewport and hides explicit resolution fields when **On**. |
| `TimeoutIfIdle` | Disconnects an idle session. |

**AFK timeout (seconds)** sets the idle window. Leaving it empty removes that override.

Under **Unreal**, enter **Width** and **Height** together for an explicit resolution. If `MatchViewportRes` is **On**, those fields are hidden. **Screen percentage** sets the internal render scale, and **Extra arguments** are passed to the Unreal process.

**Advanced** exposes the browser settings as a JSON object and a **Disable VPX compute shader** control. The JSON accepts boolean, number, or text values. The VPX control writes `-PixelStreamingVPXUseCompute=false` to **Extra arguments**.

Select **Save and redeploy** to save changes and restart a version marked **Active**, without packaging or uploading again. Select **Save only** to apply the settings at the next deployment. An unchanged save may queue no redeploy. Hosting capacity and sleep settings are managed in the Convai dashboard's **Hosting** tab.

## Publish the experience page

The first **Open in browser** action creates an experience page for the project if needed. In **PUBLISH**, enter a **Page name** and **Short description**, then choose **Public**, **Unlisted**, or **Private**. **Live now:** shows the audience already in effect, which may differ from your unsaved choice.

Select **Publish** to make the page live at the selected audience. Select **Save draft** to store its details without making it live.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| `Sign in to Convai to manage your uploaded projects.` | Use **Sign in** in the panel, then select **Refresh**. |
| `This editor cannot package for Win64.` | Install the Windows platform SDK for this engine, restart the Editor, and try again. |
| Packaging fails | Open Unreal's packaging log from its notification, fix the reported problem, and select **Upload changes**. |
| An archive entry is too large | Split the packaged content into smaller files or pak chunks. The archiver rejects a single entry above 1.5 GB before upload. |
| A version says **Build failed** | Select **Logs** on that version to read the build report. |
| The build succeeds but activation fails | Use **Make active** on the built version to retry activation; the archive is already uploaded. |
| **Save and redeploy** is unavailable | Wait for a version row to show **Active**, or use **Make active** on a built version. |
| The browser stream works but the Convai character cannot hear speech | Check the preparation notes for an audio-component warning. Restart the Editor and use **Upload changes** so the plugin can add `ConvaiPSAudioCapture` to a project Blueprint with a Convai player component. |

### Use a different Convai environment

Cloud Projects uses the Convai plugin's API host (`CustomBetaURL` or `-ConvaiBetaURL=`). Use `-ConvaiProjectApiURL=` to override only Cloud Projects. If the browser player has a separate host, use `-ConvaiExperienceURL=`. Sign in to the selected environment.
