---
title: Asset Uploader
description: Upload Metahumans, Reallusion characters, and scenes from Unreal Engine to Convai Sim and Avatar Studio using the Convai Asset Uploader tool.
last_reviewed: "5.8"
---

The Convai Asset Uploader uploads Metahumans, Reallusion characters, and scenes from Unreal Engine directly to Avatar Studio and Convai Sim. The tool automates project creation, plugin integration, and asset packaging through a command-line interface. Use this page to install the tool, run it against an Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code> project, and upload your first asset.

{% hint style="danger" %}
The Asset Uploader is available only on the Professional Plan and above.
{% endhint %}

{% embed url="https://youtu.be/eFK9RFHDdco" %}
Convai Asset Uploader tool walkthrough
{% endembed %}

***

## Prerequisites

Before running the Asset Uploader, confirm the following:

* Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code>
* A Convai API key from the [Convai Dashboard](https://convai.com/)
* .NET 6.0 Runtime (Console Applications) — [download the .NET 6.0 console runtime](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime?cid=getdotnetcore\&os=windows\&arch=x64)
* The Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code> [cross-compile toolchain requirements](https://dev.epicgames.com/documentation/en-us/unreal-engine/linux-development-requirements-for-unreal-engine?application_version=5.8), including the [toolchain version history](https://dev.epicgames.com/documentation/en-us/unreal-engine/linux-development-requirements-for-unreal-engine#version-history)
* The Linux binaries for Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code>, available from the Epic Games Launcher

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Epic Games Launcher engine options screen showing the Linux binaries entry for Unreal Engine 5.8 selected for installation. The image must show the exact UI label for the Linux binaries option in the 5.8 engine options list.
{% endhint %}

<figure><img src="../../.gitbook/assets/TODO-linux-binaries-unreal-5-8.png" alt="Epic Games Launcher engine options showing the Linux binaries entry for Unreal Engine 5.8"><figcaption><p>TODO: Replace with a screenshot of the Linux binaries option for Unreal Engine 5.8 in the Epic Games Launcher.</p></figcaption></figure>

***

## Download and run the tool

{% stepper %}
{% step %}
### Download the Asset Uploader

Download the latest `AssetUploaderTool.exe` from the [Convai Asset Uploader GitHub Releases](https://github.com/Conv-AI/Convai-UnrealEngine-ModdingTool/releases). Move the file to the directory where you want your new Unreal Engine project to be created — the tool creates and configures the Convai Unreal Engine project automatically.
{% endstep %}

{% step %}
### Run the uploader tool

Double-click `AssetUploaderTool.exe` to run it. If Windows shows a "Windows protected your PC" screen, select **More info > Run anyway**. The tool is safe to run — the warning appears because the tool is currently in beta and not digitally signed.
{% endstep %}

{% step %}
### Follow the prompts

The tool opens in a terminal window and walks through:

1. **Unreal Engine path detection** — confirm a message such as `Found Valid Unreal Engine Path: C:/Program Files/Epic Games/UE_5.8`. Enter `Y` to confirm the path or `N` to provide a different path.
2. **Project configuration** — enter the project name and your Convai API key.
3. **Asset type selection** — press `1` to upload a scene or `2` to upload an avatar.
4. **Avatar type selection** (avatars only) — respond to `Are you using a Metahuman for your Avatar?` with `Y` for a MetaHuman setup or `N` for a Reallusion setup.
{% endstep %}
{% endstepper %}

***

## Verify the upload

Once configuration is complete, the tool generates a new Unreal Engine project, installs and configures the Convai plugins, and begins compiling the project. The upload is complete once the terminal shows:

```text
Unreal Compilation completed successfully
```

Press `Enter` to exit.

The new project is created in the same directory as `AssetUploaderTool.exe`. For example, if the tool is placed in `Downloads`, the project is generated inside `Downloads`.

***

## Troubleshooting

### .NET Runtime error appears when running the tool

**Symptom:** The tool reports a missing .NET Runtime error.

**Cause:** The .NET 6.0 Runtime for console applications is not installed.

**Fix:** Install the [.NET 6.0 Runtime for console apps](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime?cid=getdotnetcore\&os=windows\&arch=x64).

**Verify:** Rerun `AssetUploaderTool.exe` — the tool starts without the runtime error.

***

## Project and plugin constraints

* Do not delete or rename the `ConvaiEssentials` folder.
* Do not change global project settings outside the plugin folder.
* Support for other Unreal Engine versions is in development.

***

## Next steps

Only MetaHuman and Reallusion avatars are supported for upload.

{% content-ref url="../../no-code-experiences/avatar-studio-experiences/customizing-your-avatar/configure-avatar/uploading-avatars/metahuman-avatars.md" %}
[Uploading MetaHuman avatars](../../no-code-experiences/avatar-studio-experiences/customizing-your-avatar/configure-avatar/uploading-avatars/metahuman-avatars.md)
{% endcontent-ref %}

{% content-ref url="../../no-code-experiences/avatar-studio-experiences/customizing-your-avatar/configure-avatar/uploading-avatars/reallusion-avatars.md" %}
[Uploading Reallusion avatars](../../no-code-experiences/avatar-studio-experiences/customizing-your-avatar/configure-avatar/uploading-avatars/reallusion-avatars.md)
{% endcontent-ref %}

***

## Need help?

If you run into issues or have questions, reach out through the [Convai Developer Forum](https://forum.convai.com/).
