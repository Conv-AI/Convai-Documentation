---
description: >-
  Upload Metahumans, Reallusion characters, and Scenes from Unreal Engine to
  Convai Sim and Avatar Studio with ease.
---

# Asset Uploader

## Introduction

The **Convai Asset Uploader** enables developers to upload their custom avatars and levels directly from **Unreal Engine 5.5** to **Avatar Studio** and **Convai Sim**. It automates project creation, plugin integration, and asset packaging through a command-line interface, making the entire process simple and reliable.

Whether you're uploading a scene, a Metahuman, or a custom Reallusion character, this tool ensures your assets are packaged and transferred in a compatible and Convai-ready format.

{% embed url="https://youtu.be/LaoREaFoYx8?feature=shared" %}

***

## Prerequisites

Before getting started, ensure you have the following:

* **Unreal Engine 5.5**
* **Convai API Key** – You can generate one from your [Convai Dashboard](https://convai.com/)
* **.NET 6.0 Runtime (Console Applications)** – [Download it here](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime?cid=getdotnetcore\&os=windows\&arch=x64)
* **Unreal Engine 5.5** [**Cross-Compile Toolchain**](https://dev.epicgames.com/documentation/en-us/unreal-engine/linux-development-requirements-for-unreal-engine?application_version=5.5) **-** [Download it here](https://cdn.unrealengine.com/CrossToolchain_Linux/v23_clang-18.1.0-rockylinux8.exe)
* **Download Linux Binaries for Unreal Engine 5.5 -** You can download it from Epic Games Launcher

<figure><img src=".gitbook/assets/image (433).png" alt=""><figcaption><p><strong>Linux Binaries for Unreal Engine 5.5</strong></p></figcaption></figure>

***

## Getting Started

### Step 1: Download Required Files

To get started, you’ll need to download two files from our [GitHub repository](https://github.com/Conv-AI/Convai-UnrealEngine-ModdingTool/releases):

* `UploaderTool.exe`
* `dump_syms.exe`

{% hint style="info" %}
These tools are essential for initializing and configuring your Convai Unreal project.
{% endhint %}

***

### Step 2: Replace Existing `dump_syms.exe`



Before launching the tool, you **must** replace Unreal Engine’s existing `dump_syms.exe` with the one you just downloaded.

*   Navigate to your UE5.5 installation folder:

    <pre><code><strong>&#x3C;UE5.5 Installation Path>/Engine/Binaries/Linux/dump_syms.exe
    </strong></code></pre>

{% hint style="danger" %}
**Make a backup** of the original `dump_syms.exe` file before replacing it.
{% endhint %}

* Replace the existing `dump_syms.exe` file with the downloaded one.

{% hint style="info" %}
**What is `dump_syms.exe` and why replace it?**\
This file is used to generate symbol files for debugging during the packaging process.\
The version bundled with Unreal Engine 5.5 has some issues that can cause packaging to fail.\
Replacing it with the provided version ensures stable behavior and successful packaging.
{% endhint %}

***

### Step 3: Run the Uploader Tool

Once `dump_syms.exe` has been replaced:

1. Move the downloaded `UploaderTool.exe` file to the directory where you want your new Unreal project to be created.
2. Double-click to run the `.exe`.
3. If you see a “Windows protected your PC” screen, click **More Info** > **Run Anyway**.

{% hint style="success" %}
Don’t worry! The executable is safe to use. The warning appears because the tool is currently in beta and not digitally signed.
{% endhint %}

***

### Step 4: Follow the Prompts

The Asset Uploader will open in a terminal window. You’ll go through the following steps:

1. **Unreal Engine Path Detection**\
   You'll see a message like:\
   `Found Valid Unreal Engine Path: C:/Program Files/Epic Games/UE_5.5`
   * Confirm with `Y` if correct
   * Enter `N` to provide a different path manually
2. **Project Configuration**
   * **Enter the Project Name** (this will be your new Unreal project)
   * **Enter your Convai API Key** from your Convai account
3. **Select Asset Type**
   * Press `1` for uploading a **Scene**
   * Press `2` for uploading an **Avatar**
4. **Choose Avatar Type** If you selected Avatar:
   * You’ll be asked: `Are you using a Metahuman for your Avatar?`
     * Press `Y` for Metahuman setup
     * Press `N` for Reallusion setup

***

## What Happens Next

Once your configuration is complete, the tool will:

* Generate a new Unreal Engine project
* Automatically install and configure all necessary **Convai Plugins**
* Begin compiling the project

When you see the message:

```
Unreal Compilation completed successfully
```

your setup is complete. Press `Enter` to exit.

***

## Project Location

Your new project will be created in the same directory as the `.exe`.

> Example: If the tool is placed in `Downloads`, your project will be generated inside `Downloads`.

***

## .NET Runtime Errors

If you encounter an error related to the .NET Runtime:

* Install the **.NET 6.0 Runtime for Console Apps** from [this link](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime?cid=getdotnetcore\&os=windows\&arch=x64).

***

## Important Notes

* Do **not** delete or rename the `ConvaiEssentials` folder.
* Do **not** change global project settings outside the plugin folder.
* Support for other Unreal Engine versions is in development.

***

## Next Steps

Continue to one of the following guides:

* [Uploading Metahuman Avatars](no-code-experiences/avatar-studio-experiences/customizing-your-avatar/configure-avatar/uploading-avatars/metahuman-avatars.md)
* [Uploading Reallusion Avatars](no-code-experiences/avatar-studio-experiences/customizing-your-avatar/configure-avatar/uploading-avatars/reallusion-avatars.md)

{% hint style="info" %}
Currently, only Metahuman and Reallusion avatars are supported for upload.
{% endhint %}

***

## Need Help?

If you run into any issues or have questions, don’t hesitate to reach out via the [Convai Developer Forum](https://forum.convai.com/).&#x20;
