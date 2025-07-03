---
description: >-
  Upload custom Reallusion characters from Unreal Engine 5.3 to Avatar Studio
  using the Convai Asset Uploader.
---

# Reallusion Avatars

## Introduction

This guide explains how to prepare and upload **Reallusion-based avatars** using the **Convai Asset Uploader**. You’ll import your Reallusion character and animations, apply Convai’s animation and lipsync systems, and then upload your avatar to Avatar Studio using the built-in AssetUploader tool.

***

## Prerequisites

Make sure you have the following ready:

* A project created with the [**Convai Asset Uploader**](../../../../../asset-uploader.md), where you answered **`N`** to “Are you using a Metahuman?”
* A custom Reallusion character exported and ready for import

***

## Step-by-Step Guide

### 1. Open the Project

Navigate to your project directory and open the `.uproject` file to launch it in Unreal Engine 5.3.

***

### 2. Import Reallusion Character & Animations

Follow this [video tutorial](https://youtu.be/UyxNliF8LKU?feature=shared) to import your Reallusion assets:

* **\[00:00 – 07:25]**: Import your character and animations
* **\[07:50 – 08:20]**: Create a new Blueprint Class for your character

***

### 3. Connect Convai Animations

Now we’ll bind the correct animation logic to your character.

We’ve already added the necessary Animation Blueprint for you:

* Go to `Content/ConvaiReallusion/`
* Locate and assign the **ConvaiReallusion Animation Blueprint** to your character’s Skeletal Mesh

{% hint style="info" %}
This blueprint ensures that your Reallusion character plays proper idle/talking animations in sync with Convai interactions.
{% endhint %}

* Refer to the [tutorial](https://youtu.be/UyxNliF8LKU?feature=shared) for this step: **\[10:12 – 12:48]**

***

### 4. Add FaceSync for Lipsync

To enable lipsync:

* Add the `FaceSync` component to your character’s Blueprint
* See how in the same [video](https://youtu.be/UyxNliF8LKU?feature=shared): **\[12:48 – 12:56]**

***

### 5. Set Correct Rotation

Reallusion characters typically face the wrong direction by default. Fix this by:

* Opening the character Blueprint
* Selecting the **SkeletalMesh** component
* Set the **Z Rotation** to `-90` in the **Details** panel

***

### 6. Prepare Files for Upload

1. Go to:\
   `Plugins/<random code> Content/`\
   (e.g., `Plugins/AHK3LNKVC7FZA3I5JG3V Content/`)
2. Drag and **Move** both of the following folders into this directory:
   * Your character’s folder (containing the Blueprint and animations)
   * `Content/ConvaiReallusion/` (contains the animation blueprint)
   * The final structure should mirror what’s shown in the screenshot.

<figure><img src="../../../../../.gitbook/assets/Screenshot 2025-04-19 143603.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
This folder determines what gets packaged and uploaded. Make sure everything is placed correctly.
{% endhint %}

***

### 7. Open the AssetUploader Tool

* Navigate to `Content/Editor/AssetUploader`
* Right-click and select **Run Editor Utility Widget**

***

### 8. Select the Character Asset

* Navigate to `Plugins/<random code> Content/YourCharacterFolder/`
* Select your character’s **Blueprint Class**
* Then, in the Asset Uploader window, click **Pick Asset**

***

### 9. Capture a Thumbnail

Click **Capture Thumbnail** to create a preview image that will appear in Avatar Studio.

***

### 10. Verify Before Upload

Before uploading, do a quick functional test:

1. Drag the character into your Level
2. Select it and locate the `BP_ConvaiChatbotComponent` in the **Details** panel
3. Paste in a test **Character ID**
4. Press **Play** and verify:
   * Animation is working
   * Lipsync is functioning
   * Character is correctly positioned and oriented

***

### 11. Upload the Avatar

* In the Asset Uploader, click **Create Asset**
* This triggers:
  * Packaging the asset for **Win64**
  * Uploading to **Avatar Studio**

Monitor the **Output Log**:

* Wait for `Package completed`
* Then look for `Uploaded Asset`

{% hint style="warning" %}
If there’s an error during packaging, check the logs and share them on the [Convai Developer Forum](https://forum.convai.com/) for support.
{% endhint %}

{% hint style="info" %}
To delete a previously uploaded asset, open AssetUploader and click **Delete**.
{% endhint %}

***

## Accessing the Avatar

1. Visit [Avatar Studio](https://convai.com/)
2. Go to **Upload Your Custom Avatar**
3. Your Reallusion character will now be available for selection and use

***

## Summary

Using the Convai Asset Uploader, uploading Reallusion avatars is quick and reliable. With proper setup and a few clicks, your characters are live in Avatar Studio and ready for real-time AI interaction.
