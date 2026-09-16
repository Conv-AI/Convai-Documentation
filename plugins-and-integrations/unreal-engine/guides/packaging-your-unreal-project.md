---
description: >-
  Enable Pixel Streaming, add the audio capture component, package a Windows
  build, and upload it to Convai so your experience streams in a browser.
last_reviewed: 2026-09-16
---

# Packaging your Unreal project for deployment

Convai hosts your packaged Unreal experience and streams it to a browser. You enable Pixel Streaming, package a Windows build, compress it, and upload that archive to Convai. This page is for developers whose project already runs in the Unreal Editor.

{% hint style="warning" %}
Enable Pixel Streaming before you package. Unreal compiles plugins into the build, so enabling the plugin afterwards has no effect on a build that already exists.
{% endhint %}

## Before you start

* [ ] An Unreal Engine project that opens and runs in the Editor
* [ ] A Windows machine with Visual Studio 2022 and the **Game development with C++** workload
* [ ] Free disk space of roughly three times your project size

## Prepare and package the project

{% stepper %}
{% step %}
### Enable Pixel Streaming

In the Unreal Editor, open **Edit > Plugins** and search for Pixel Streaming. Enable one version:

* **Pixel Streaming 2** on Unreal Engine 5.5 and later
* **Pixel Streaming** on earlier versions, or where **Pixel Streaming 2** is not listed

Restart the Editor when it prompts you.
{% endstep %}

{% step %}
### Add the audio capture component, if you use the Convai plugin

Skip this step when your project does not use the Convai Unreal Engine plugin. Nothing else on this page depends on it.

If your project does use the plugin, and you have not installed it yet, follow [Convai Unreal Engine plugin](https://docs.convai.com/api-docs/plugins-and-integrations/convai-unreal-engine-plugin) first.

Open the blueprint that holds `BP_ConvaiPlayerComponent`, select **Add** in the **Components** panel, and add `ConvaiPSAudioCapture` under that component. It routes microphone audio from the browser into your character, so the character hears a viewer who is talking through the stream.

<figure><img src="../../../.gitbook/assets/convai-ps-audio-capture-component.png" alt="The Components panel showing ConvaiPSAudioCapture nested under BP_ConvaiPlayerComponent"><figcaption><p><code>ConvaiPSAudioCapture</code> added under <code>BP_ConvaiPlayerComponent</code></p></figcaption></figure>

Compile and save the blueprint.
{% endstep %}

{% step %}
### Package the project for Windows

Open **Platforms > Windows > Build Configuration** and select **Shipping**, then open **Platforms > Windows > Package Project** and choose an empty output folder.

The first package can take 30 to 45 minutes, because Unreal cooks every asset in the project. Later packages reuse that work and finish faster.

When packaging finishes, the output folder holds `YourProject.exe` alongside the `Engine` and `YourProject` folders.
{% endstep %}

{% step %}
### Compress the build

Compress the packaged folder into a single `.zip` or `.tar` archive. Convai accepts either format.
{% endstep %}
{% endstepper %}

## Upload the build to Convai

{% stepper %}
{% step %}
### Open your experiences

Sign in at [convai.com](https://convai.com) and select **My Experiences**.

<figure><img src="../../../.gitbook/assets/convai-my-experiences-nav.png" alt="The Convai navigation sidebar with My Experiences selected"><figcaption><p>Selecting <strong>My Experiences</strong></p></figcaption></figure>
{% endstep %}

{% step %}
### Upload the archive

Select **Upload application**, enter an **Application name** and a **Version**, then select **Choose archive** and pick the archive you compressed.

<figure><img src="../../../.gitbook/assets/convai-upload-application-dialog.png" alt="The Upload application dialog with fields for application name and version and an area to drop the archive"><figcaption><p>The <strong>Upload application</strong> dialog</p></figcaption></figure>

Select **Upload &#x26; build**.
{% endstep %}

{% step %}
### Wait for the deployment

Convai builds and deploys the uploaded application. This takes a few minutes.
{% endstep %}

{% step %}
### Test the stream

When the deployment finishes, select the test button on your application. It opens your experience on its `convai.com` address, where your packaged project streams in the browser.
{% endstep %}
{% endstepper %}

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| The deployed application loads and no stream reaches the browser | Pixel Streaming was not enabled when the project was packaged | Enable the plugin in the Editor, package the project again, and upload the new archive |
| The stream plays and the character does not respond to speech from the browser | `ConvaiPSAudioCapture` is missing from the blueprint that holds `BP_ConvaiPlayerComponent` | Add the component, compile the blueprint, then package and upload again |
| Packaging fails with `The following action paths are longer than 260 characters. Please move the engine to a directory with a shorter path.` | Unreal enforces a 260-character limit on build paths, and Pixel Streaming stages a deeply nested web server folder that passes it when the project sits far from the drive root | Move the project closer to the drive root, such as `C:\Projects\MyGame`, and package again |
