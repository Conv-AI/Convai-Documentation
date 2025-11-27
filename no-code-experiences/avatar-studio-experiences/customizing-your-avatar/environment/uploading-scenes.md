---
description: >-
  Upload your custom Unreal Engine Levels to Avatar Studio with Convai Modding
  Tool.
hidden: true
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/no-code-experiences/avatar-studio-experiences/customizing-your-avatar/environment/uploading-scenes
---

# Uploading Scenes

## Introduction

This guide explains how to upload **custom scenes (Levels)** from Unreal Engine 5.3 to **Avatar Studio** using the **Convai Modding Tool**. Whether you’re building rich environments or AI-driven stages, you’ll learn how to prepare, tag, and upload them in just a few steps.

***

## Prerequisites

Make sure you have:

* Created your project using the [**Convai Modding Tool**](../../../../asset-uploader/)
  * Selected **`1`** when asked whether you are uploading a Scene or Avatar
* A fully prepared and tested Unreal Engine Level (with all necessary assets)

***

## Step-by-Step Guide

### 1. Open the Project

Open the project created by the Modding Tool by double-clicking the `.uproject` file.

***

### 2. Import the Scene

Import your custom Level and all required assets (meshes, environment packs, etc.) into your project.

Make sure the Level is fully playable and doesn’t contain any broken references.

***

### 3. Editor (Player) Start Point

To set the spawn location of the editor (Player) in the Level

1. Place an **Actor** in your Level
2. Move it to the desired **spawn location**
3. In the **Details** panel, set the **Tag** of the Actor to:

```
EditorSpawn
```

{% hint style="warning" %}
This tag is essential. It helps the system know where to place the editor (player) once the scene is loaded in Avatar Studio.
{% endhint %}

***

### 4. Prepare Files for Upload

1. Navigate to:\
   `Plugins/<random code> Content/`\
   (e.g., `Plugins/AHK3LNKVC7FZA3I5JG3V Content/`)
2. Drag and **Move** your Level’s folder and its dependencies into this directory.

{% hint style="info" %}
This ensures the Level and all its references are included during packaging and upload.
{% endhint %}

***

### 5. Open the AssetUploader Tool

* Go to `Content/Editor/AssetUploader`
* Right-click and choose **Run Editor Utility Widget**

***

### 6. Select the Level Asset

* In the **Content Browser**, go to the directory inside\
  `Plugins/<random code> Content/`
* Select your **Level asset**
* Return to the **Asset Uploader** window and click **Pick Asset**

***

### 7. Capture a Thumbnail

Click **Capture Thumbnail** to generate a preview image that will appear in Avatar Studio.

***

### 8. Upload the Scene

Once everything is ready, click **Create Asset** in the Asset Uploader.

The process includes:

* **Packaging** the Level for Win64
* **Uploading** the Level to Avatar Studio

Check the **Output Log**:

* Look for `Package completed`
* Then `Uploaded Asset` to confirm successful upload

{% hint style="warning" %}
If there’s an error during packaging, check the logs and share them on the [Convai Developer Forum](https://forum.convai.com/) for support.
{% endhint %}

{% hint style="info" %}
To delete a previously uploaded asset, open AssetUploader and click **Delete**.
{% endhint %}

***

## Accessing the Scene

1. Visit [Avatar Studio](https://convai.com/)
2. Open the **Upload Your Custom Scene** section
3. Your Level will appear in the list, ready for testing or integration with avatars

***

## Summary

Uploading custom Levels allows you to create rich environments for your AI avatars in Convai Sim. The Modding Tool automates most of the setup — just make sure to set your spawn point and move your assets to the correct folder.
