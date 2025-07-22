---
description: >-
  Upload Metahumans, Reallusion characters, and Scenes from Unreal Engine to
  Convai Sim and Avatar Studio with ease.
---

# Asset Uploader

## Introduction

The **Convai Asset Uploader** enables developers to upload their custom avatars and levels directly from **Unreal Engine 5.5** to **Avatar Studio** and **Convai Sim**. It automates project creation, plugin integration, and asset packaging through a command-line interface, making the entire process simple and reliable.

Whether you're uploading a scene, a Metahuman, or a custom Reallusion character, this tool ensures your assets are packaged and transferred in a compatible and Convai-ready format.

***

## Prerequisites

Before getting started, ensure you have the following:

* **Unreal Engine 5.5**
* **Convai API Key** – You can get it from the [Convai Dashboard](https://convai.com/)
* **.NET 6.0 Runtime (Console Applications)** – [Download it here](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime?cid=getdotnetcore\&os=windows\&arch=x64)
* **Unreal Engine 5.5** [**Cross-Compile Toolchain**](https://dev.epicgames.com/documentation/en-us/unreal-engine/linux-development-requirements-for-unreal-engine?application_version=5.5) **-** [Download it here](https://cdn.unrealengine.com/CrossToolchain_Linux/v23_clang-18.1.0-rockylinux8.exe)
* **Download Linux Binaries for Unreal Engine 5.5 -** You can download it from Epic Games Launcher

<figure><img src=".gitbook/assets/image (433).png" alt=""><figcaption><p><strong>Linux Binaries for Unreal Engine 5.5</strong></p></figcaption></figure>

***

## Getting Started

### Step 1: Download the Asset Uploader

Download the latest version of `AssetUploaderTool.exe` from our [GitHub Releases](https://github.com/Conv-AI/Convai-UnrealEngine-ModdingTool/releases).

{% hint style="info" %}
Asset Uploader Tool will create and configure your Convai Unreal project automatically.
{% endhint %}

***

### Step 2: Update `BuildConfiguration.xml`

Before running the tool, you must update your Unreal Engine Build Configuration settings.

1.  Navigate to the following path:

    ```
    <USER>/AppData/Roaming/Unreal Engine/UnrealBuildTool/BuildConfiguration.xml
    ```
2. Open the file in a text editor (e.g., Notepad).
3.  Add the following block **inside the `<Configuration>` tag**:

    ```xml
    <BuildConfiguration>
        <bAllowUBALocalExecutor>false</bAllowUBALocalExecutor>
    </BuildConfiguration>
    ```

{% hint style="warning" %}
In most cases, your file might look like this initially:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
</Configuration>
```

But in some cases, there may already be other settings inside the `<Configuration>` tag. That’s perfectly fine.\
Just make sure to add the `<BuildConfiguration>` block anywhere inside the `<Configuration>` section.
{% endhint %}

This change is required to avoid errors during project compilation caused by Unreal’s parallel executor.

***

### Step 3: Run the Uploader Tool

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
