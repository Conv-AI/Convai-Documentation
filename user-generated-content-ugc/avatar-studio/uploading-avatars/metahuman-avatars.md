---
description: >-
  Upload custom Metahuman characters from Unreal Engine 5.3 to Avatar Studio
  using the Convai Modding Tool.
---

# Metahuman Avatars

## Introduction

This guide walks you through uploading **custom Metahuman avatars** to **Avatar Studio** using the **Convai Modding Tool**. You'll generate a new project tailored for Metahumans, import your Metahuman asset, configure it, and finally upload it using Convai’s built-in tools.

## Prerequisites

Before you begin:

* Create your project using the [**Convai Modding Tool**](../../modding-tool.md), and answer **`Y`** when asked if you’re using a Metahuman.
* Ensure you have a downloadable Metahuman available via **Quixel Bridge**.

***

## Step-by-Step Guide

### 1. Open the Project

Navigate to the folder where your project was created. Double-click the `YourProjectName.uproject` file to open it in Unreal Engine.

***

### 2. Add a Metahuman via Quixel Bridge

* Go to **Window > Quixel Bridge**.
* In Bridge, select **Metahumans** from the left-hand menu.
* Pick a Metahuman and click:
  * **Download** (if not already downloaded)
  * Then **Add** to include it in your project.

***

### 3. Locate and Open the Character Blueprint

After importing:

* Go to `Content/Metahumans/<CharacterName>/`.
*   Open the Blueprint: `BP_<CharacterName>`

    > ⏳ This may take some time to load.

***

### 4. Fix Compile Errors

If you see compile errors:

* In the bottom-right, click **Enable Missing** under any **Missing Plugins** or **Missing Project Settings** notices.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-04-18 224336 (1).png" alt=""><figcaption></figcaption></figure>

* Click **Restart Now** when prompted.
* Reopen the Blueprint and ensure it compiles successfully.

***

### 5. Prepare the Asset for Upload

1. Locate the folder:\
   `Plugins/<random code> Content/`\
   (e.g., `Plugins/AHK3LNKVC7FZA3I5JG3V Content/`)
2. Move the entire `Content/Metahumans/` folder into this directory.
   * Use **Move Here** to complete the action.
   * The final structure should mirror what’s shown in the screenshot.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-04-18 231010.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
This folder determines what gets packaged and uploaded. Make sure everything is placed correctly.
{% endhint %}

***

### 6. Open the Asset Uploader Tool

* Navigate to `Content/Editor/AssetUploader`.
* Right-click on `AssetUploader` and select **Run Editor Utility Widget**.

***

### 7. Select the Character Asset

* Navigate to the `Plugins/<random code> Content/Metahumans/<CharacterName>/` directory.
* Select the `BP_<CharacterName>` Blueprint.
* Then, in the **Asset Uploader** window, click **Pick Asset**.

***

### 8. Capture a Thumbnail

* In the Asset Uploader window, click **Capture Thumbnail** to generate a preview image for your avatar.

***

### 9. Verify Functionality Before Upload

1. Drag `BP_<CharacterName>` into the Level.
2. Select the character and locate `BP_ConvaiChatbotComponent` in the **Details** panel.
3. Input a test **Character ID**.
4. Press **Play** and confirm:
   * Animations are working
   * Lip sync is functional
   * Character behaves as expected

***

### 10. Upload the Avatar

* In the Asset Uploader, click **Create Asset**.
* This will:
  * Package the avatar for Win64
  * Upload it to Avatar Studio

Monitor the **Output Log**:

* Look for `Package completed`
* Then wait for `Uploaded Asset`

{% hint style="warning" %}
If there’s an error during packaging, check the logs and share them on the [Convai Developer Forum](https://forum.convai.com/) for support.
{% endhint %}

{% hint style="info" %}
To delete a previously uploaded asset, open AssetUploader and click **Delete**.
{% endhint %}

***

## Accessing the Avatar

1. Go to [Avatar Studio](https://convai.com/)
2. Open the **Upload Your Custom Avatar** section
3. Your Metahuman will appear, ready for use.

***

## Summary

Using the Convai Modding Tool, uploading custom Metahuman avatars is quick and reliable. With proper setup and a few clicks, your characters are live in Avatar Studio and ready for real-time AI interaction.
