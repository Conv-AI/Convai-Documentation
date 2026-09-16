---
description: >-
  Enable Pixel Streaming, package a Windows build of your Unreal project, and
  upload it so Convai can host and stream your experience in a browser.
last_reviewed: 2026-09-16
---

# Packaging your Unreal project for deployment

Convai hosts your Unreal experience and streams it to a browser. To get there, you package a Windows build of your project with Pixel Streaming enabled, then upload that build. This page is for developers whose project already runs in the Unreal Editor.

{% hint style="warning" %}
Enable Pixel Streaming before you package. Unreal compiles plugins into the build, so enabling the plugin afterwards has no effect on a build that already exists.
{% endhint %}

## Before you start

* [ ] An Unreal Engine project that opens and runs in the Editor
* [ ] A Windows machine with Visual Studio 2022 and the **Game development with C++** workload
* [ ] Free disk space of roughly three times your project size

## Package the build

{% stepper %}
{% step %}
### Enable Pixel Streaming

In the Unreal Editor, open **Edit > Plugins** and search for Pixel Streaming. Enable one version:

* **Pixel Streaming 2** on Unreal Engine 5.5 and later
* **Pixel Streaming** on earlier versions, or where **Pixel Streaming 2** is not listed

Restart the Editor when it prompts you.

<figure><img src="https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2FW2YTsOSE7FyBrR5nNSkk%2Fimage.png?alt=media&#x26;token=542dc8d7-a998-4507-ae76-0e5a781ff093" alt="The Unreal Editor Plugins window with the Pixel Streaming plugin enabled"><figcaption><p>Enabling Pixel Streaming in the Plugins window</p></figcaption></figure>
{% endstep %}

{% step %}
### Set the build configuration

Open **Platforms > Windows > Build Configuration** and select **Shipping**.
{% endstep %}

{% step %}
### Package the project

Open **Platforms > Windows > Package Project** and choose an empty output folder.

The first package can take 30 to 45 minutes, because Unreal cooks every asset in the project. Later packages reuse that work and finish faster.

When packaging finishes, the output folder holds `YourProject.exe` alongside the `Engine` and `YourProject` folders.
{% endstep %}
{% endstepper %}

## Confirm Pixel Streaming is in the build

A package that succeeds does not prove the plugin reached the build. Unreal links plugin modules directly into the executable for a Shipping build, so the packaged `Plugins` folder shows nothing either way.

Read the build receipt instead:

```powershell
$receipt = "Windows\YourProject\Binaries\Win64\YourProject-Win64-Shipping.target"
(Get-Content $receipt -Raw | ConvertFrom-Json).BuildPlugins
```

The returned list names `PixelStreaming` or `PixelStreaming2` when the plugin compiled into the build. If neither appears, the build cannot stream.

## Troubleshooting

### The build renders but nothing streams

**Symptom:** the packaged build launches and draws a window, and no stream reaches the browser.

**Cause:** Pixel Streaming was not enabled when the project was packaged.

**Fix:** enable the plugin in the Editor, then package the project again.

**Verification:** run the build receipt check described earlier on this page and confirm the plugin is listed.

### Packaging stops with a path length error

**Symptom:** packaging fails with `The following action paths are longer than 260 characters. Please move the engine to a directory with a shorter path.`

**Cause:** Unreal enforces a 260-character limit on build paths. Pixel Streaming stages a deeply nested web server folder, which pushes paths past that limit when the project sits far from the drive root.

**Fix:** move the project closer to the drive root, such as `C:\Projects\MyGame`, and package again.

**Verification:** packaging passes the build stage and starts cooking content.

## Next steps

* [Convai Pixel Streaming Embed](../../convai-pixel-streaming-embed) embeds the deployed experience in a React or JavaScript application.
* [Integration with Pixel Streaming](integration-with-pixel-streaming) connects Pixel Streaming audio to the Convai player component.
