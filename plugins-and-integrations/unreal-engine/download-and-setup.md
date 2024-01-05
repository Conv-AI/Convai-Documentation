---
description: Install the Unreal Engine Plugin with your project.
---

# Download and Setup

## Getting Started

{% hint style="info" %}
Before getting started with plugin its recommended to install Visual Studio, by referring to this [<mark style="color:green;">guide</mark>](https://docs.unrealengine.com/5.1/en-US/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine/).
{% endhint %}

### Installing Visual Studio for Windows

* Download  [Visual Studio from here](https://visualstudio.microsoft.com/downloads/).
* Once downloaded make sure that you have the required C++ toolchains as mentioned [<mark style="color:green;">**here**</mark>](https://docs.unrealengine.com/5.1/en-US/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine/) for Unreal Engine. If you already have Visual Studio installed, you may open the installer and select **'Modify'** to add the above mentioned toolchains.&#x20;

### Installing XCode for Mac

* Download [XCode from the app store](https://apps.apple.com/us/app/xcode/id497799835?mt=12)
* For UE 5.3 and UE 5.0, you will need to follow this [guide to enable microphone permissions](mac-microphone-permission-required-for-ue-5.0-and-5.3.md).

### There are two options to install the plugin:

* **For UE 5.1 - 5.3** install directly from the Marketplace\
  Go to the plugin's [Marketplace link](https://www.unrealengine.com/marketplace/en-US/product/convai) and choose your engine version.
* **For UE 4.26, 4.27 and 5.0** install to engine manually\
  These versions are not on the Marketplace, so you need to do an [**Engine Install**](download-and-setup.md#engine-install) as described below.

## **Engine Install**

1. [**Download the Plugin matching your target Unreal Engine version**](https://drive.google.com/drive/u/4/folders/1bhWisnnlD-gfeo5QQ65Tpbl\_GMXoFoc-)
2. Extract the contents of the downloaded Zip file.&#x20;
3. In a file explorer, navigate to your Unreal Engine installation.&#x20;
   * Windows default: `Program Files/Epic Games/[ENGINE_NUMBER]`.
   * Mac default: `/Users/Shared/Epic Games/[ENGINE_NUMBER]`.
4. Copy the plugin folder **Convai to** `ENGINE_VERSION/Engine/Plugins` folder.

## Set up your project

1. Start or restart UE and open your Project.
2. From the top toolbar, go to **Edit > Plugins**.&#x20;
3. Find the **Convai** plugin.
4.  Click the checkbox to enable the plugin.\


    <div align="left">

    <figure><img src="../../.gitbook/assets/image (130).png" alt=""><figcaption></figcaption></figure>

    </div>
5. Restart Unreal Engine.&#x20;

## Set up the API key

1. [Find your API key.](../../convai-playground/get-started.md#get-your-unique-api-key)
2. Go to **Edit > Project Settings**.
3.  Choose **Convai** under the **Plugins** section on the left bar.\


    <div align="left">

    <figure><img src="../../.gitbook/assets/image (196).png" alt=""><figcaption></figcaption></figure>

    </div>
4. Paste the API key into the **API Key** field.
