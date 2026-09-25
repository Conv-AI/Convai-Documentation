---
title: Host your Unreal project with Cloud Projects
description: Upload an Unreal project from the Convai plugin, let Cloud Projects package and activate the build, and open the streamed experience in a browser.
last_reviewed: 2026-09-25
---

Use **Cloud Projects** in the Convai Unreal Engine plugin to host the project open in your Unreal Editor. The tool prepares the project, packages a Windows build, uploads it to Convai, and activates it for browser streaming.

## Before you begin

You need the Convai Unreal Engine plugin installed in a project that opens in Unreal Editor. Sign in to your Convai account from the Editor when prompted. The Editor also needs the Windows platform SDK to package this project for Windows.

Cloud Projects needs the engine's Pixel Streaming plugin. If it is installed but disabled, Cloud Projects enables it for the project during preparation. If the tool enables it in this Editor session, restart the Editor before testing Pixel Streaming in the Editor.

## Create and upload a cloud project

{% stepper %}
{% step %}
### Open Cloud Projects

In Unreal Editor, select **Tools > Convai > Cloud Projects**. If the panel asks you to sign in, select **Sign in** and complete the account sign-in flow.
{% endstep %}

{% step %}
### Name the project

Select **+ New project**. Enter a name in **PROJECT NAME**. This is the name shown in your Convai dashboard.

<figure><img src="../../../.gitbook/assets/convai-cloud-projects-create-and-upload.png" alt="Cloud Projects panel showing the project name field and Create and upload button"><figcaption><p>The upload form in the Convai Unreal Engine plugin.</p></figcaption></figure>
{% endstep %}

{% step %}
### Start the upload

Select **Create and upload**. Cloud Projects prepares the Unreal project, packages it for Windows, compresses the build, uploads the archive, runs the build on Convai, and requests activation. The panel shows each stage as it progresses. The first package can take 30–45 minutes while Unreal cooks the project's assets.
{% endstep %}
{% endstepper %}

If your project has a Convai player component in one of its own Blueprints, preparation also adds `ConvaiPSAudioCapture` when the component is available in this Editor session. This component passes microphone audio from the browser stream to the Convai player. If the panel says the audio component is unavailable, restart Unreal Editor and select **Upload changes** for the project after it reopens.

## Open the streamed project

After the upload, select your project in **Cloud Projects**. Wait until its status is **Live** and the version is **Active**. Select **Open in browser** to start a stream session in the Convai player. The browser should display your Unreal project; if your project uses a Convai character, test the browser microphone as well.

If the panel still shows **Preparing** or **Waiting to start**, select **Refresh** and check again after activation finishes.

## Publish an experience page

**Open in browser** creates an experience page for the project if one does not exist. To share that page, use the **PUBLISH** section in **Cloud Projects**. Enter a **Page name** and, if useful, a **Short description**. Choose **Public**, **Unlisted**, or **Private**, then select **Publish**. Select **Save draft** if you want to save those details without making the page live.

## Upload changes

After changing your Unreal project, select it in **Cloud Projects** and choose **Upload changes**. The plugin packages and uploads the current project as another version, builds it, and requests activation. Wait for the new version to become **Active**, then use **Open in browser** to check the update.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| Cloud Projects says the Pixel Streaming plugin is not installed | Install Pixel Streaming for this Unreal Engine installation, restart the Editor, and try **Create and upload** or **Upload changes** again. |
| **Create and upload** or **Upload changes** is unavailable because Windows packaging is unavailable | Install the Windows platform SDK for this engine, restart the Editor, and try again. |
| The packaging stage fails | Open Unreal's packaging log from its notification, fix the reported error, and select **Upload changes** again. |
| The cloud build fails | Select **Logs** on that version to inspect the build report. |
| The stream opens, but the Convai character does not hear the browser microphone | Check the preparation notes for the audio component warning. Restart the Editor and select **Upload changes** to let the plugin add `ConvaiPSAudioCapture` to a project Blueprint with a Convai player component. |
