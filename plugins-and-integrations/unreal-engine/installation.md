---
description: >-
  Install Convai plugin for Unreal Engine. Follow step-by-step instructions for
  Visual Studio and XCode setup.
---

# Installation

## Prerequisites

### Installing Visual Studio for Windows

* Download  [Visual Studio from here](https://visualstudio.microsoft.com/downloads/).
* Ensure having the required C++ toolchains mentioned [<mark style="color:green;">**here**</mark>](https://docs.unrealengine.com/5.1/en-US/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine/). If you already have Visual Studio installed, you may open the installer and select **'Modify'** to add the above mentioned toolchains.&#x20;

### Installing XCode for Mac

* Download [XCode from the app store](https://apps.apple.com/us/app/xcode/id497799835?mt=12)
* For UE 5.3 and UE 5.0, follow this [guide to enable microphone permissions](mac-microphone-permission-required-for-ue-5.0-and-5.3.md).

## Installing the plugin

There are two methods to install the plugin depending on your requirements

1. [Directly from the Marketplace Link](https://www.unrealengine.com/marketplace/en-US/product/convai): Recommended for easy installation and tracking updates to the plugin. (UE 5.1 - 5.3)
2. [Building from Github Source](https://github.com/Conv-AI/Convai-UnrealEngine-SDK?tab=readme-ov-file#installation): For source UE builds and for unsupported UE versions on the marketplace, but not guranteed as the marketplace approach. (UE 4.26 - 5.0)

## Set up your project

1. From the top toolbar, go to **Edit > Plugins**.&#x20;
2. Find the **Convai** plugin.
3.  Click the checkbox to enable the plugin.\


    <div align="left">

    <figure><img src="../../.gitbook/assets/image (130).png" alt=""><figcaption></figcaption></figure>

    </div>
4. Restart Unreal Engine.&#x20;

## Set up the API key

1. [Find your API key.](../../convai-playground/get-started.md#get-your-unique-api-key)
2. Go to **Edit > Project Settings**.
3.  Choose **Convai** under the **Plugins** section on the left bar.\


    <div align="left">

    <figure><img src="../../.gitbook/assets/image (196).png" alt=""><figcaption></figcaption></figure>

    </div>
4. Paste the API key into the **API Key** field.
