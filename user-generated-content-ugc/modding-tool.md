---
description: >-
  Upload Metahumans, Reallusion characters, and Scenes from Unreal Engine to
  Convai Sim and Avatar Studio with ease.
---

# Modding Tool

## Introduction

The **Convai Modding Tool** enables developers to upload their custom avatars and levels directly from **Unreal Engine 5.3** to **Avatar Studio** and **Convai Sim**. It automates project creation, plugin integration, and asset packaging through a command-line interface, making the entire process simple and reliable.

Whether you're uploading a scene, a Metahuman, or a custom Reallusion character, this tool ensures your assets are packaged and transferred in a compatible and Convai-ready format.

***

## Prerequisites

Before getting started, ensure you have the following:

* **Unreal Engine 5.3**
* **Convai API Key** – You can generate one from your [Convai Dashboard](https://convai.com/)
* **.NET 6.0 Runtime (Console Applications)** – [Download it here](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime?cid=getdotnetcore\&os=windows\&arch=x64)

{% hint style="info" %}
Currently, only Unreal Engine 5.3 is supported. Support for other versions is in progress.
{% endhint %}

***

{% embed url="https://youtu.be/LaoREaFoYx8" %}
This is a video explaining the whole process.
{% endembed %}

***

## Getting Started

### 1. Download & Launch

* Download `ConvaiModdingTool`from here.

{% file src="../.gitbook/assets/ConvaiModdingTool.zip" %}

* Move the `.exe` file to the directory where you want your new Unreal project to be created.
* Double-click to run it.
* If you see a “Windows protected your PC” screen, click **More Info** > **Run Anyway**.

{% hint style="success" %}
Don’t worry! The executable is safe to use. The warning appears because the tool is currently in beta and not digitally signed.
{% endhint %}

***

### 2. Follow the Prompts

The Modding Tool will open in a terminal window. You’ll go through the following steps:

1. **Unreal Engine Path Detection**\
   You'll see a message like:\
   `Found Valid Unreal Engine Path: C:/Program Files/Epic Games/UE_5.3`
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

* [Uploading Metahuman Avatars](avatar-studio/uploading-avatars/metahuman-avatars.md)
* [Uploading Reallusion Avatars](avatar-studio/uploading-avatars/reallusion-avatars.md)

{% hint style="info" %}
Currently, only Metahuman and Reallusion avatars are supported for upload.
{% endhint %}

***

## Need Help?

If you run into any issues or have questions, don’t hesitate to reach out via the [Convai Developer Forum](https://forum.convai.com/).&#x20;
