---
description: >-
  Learn how to install, set up, and run the Convai Unity Plugin Beta to
  integrate conversational AI characters directly within your Unity projects.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin-beta-overview/installation-and-setup
---

# Installation and Setup

## Introduction

The Convai Unity Plugin (Beta) allows you to seamlessly integrate Convai’s advanced conversational AI characters into your Unity projects. This plugin simplifies setup and provides a ready-to-run demo scene so you can start interacting with Convai-powered characters immediately.

{% embed url="https://youtu.be/cEctYXc5Pe8" %}

***

## Installation Guide

Follow these steps to install and configure the Convai Unity Plugin Beta.

### 1. Download the Plugin

Download the ZIP file provided below.

{% file src="../../.gitbook/assets/ConvaiUnityBeta_MR.zip" %}

## **Beta Notice**

{% hint style="danger" %}
This package is an introductory **Beta release** designed to provide a ready-to-use MR-compatible example, including the required Meta packages.\
Please note that **LipSync is not supported in this version**. Additional features, including full LipSync support, will be introduced in upcoming releases.
{% endhint %}

### 2. Extract the Package

Unzip the downloaded `.zip` file to your preferred location on your computer.

### 3. Create a New Unity Project

1. Open **Unity Hub**.
2. Click **New Project**.
3. Select your preferred Unity version (**Unity 6 or later is recommended**).
4. Choose the **Universal 3D** template.
5. Name your project and click **Create Project**.

{% hint style="info" %}
Convai Unity Plugin supports **Unity 2022 and above**.
{% endhint %}

Unity will now create and open your new project.

### 4. Import the Convai Plugin Package

1. Once your project is open, navigate to the top menu and select **Assets → Import Package → Custom Package**.
2. In the file dialog, locate and select the **Convai Unity Package** you extracted from the `.zip` file.
3. Click **Import** to add the Convai Plugin to your project.
4. After the import completes, the Convai Plugin will be ready to configure within Unity.
5. Next, open the **Project Setup Tool** that appears automatically.
6. Select both **PC** and **Meta Quest** platforms, and click **Fix All** for each platform to ensure proper configuration.

***

## Project Setup

### Setting Up Your API Key

1. Go to the **Top Menu** → **Convai**.
2. Select **Account** from the dropdown.
3. In the **API Key** field, paste your Convai API key (you can copy it from your [Convai Dashboard](https://convai.com/)).

***

### Opening the Sample Scene

To explore the Convai sample setup:

1. Navigate to:\
   `Assets/Convai/Demo/Scenes/Convai Sample Scene.unity`
2. Open the scene.
3. In the **Top Menu**, go to **Window → TextMeshPro → Import TMP Essential Resources** to enable text rendering.
4. Once imported, add your **Character Name and ID**:
   * In the **Hierarchy**, select the `ConvaiNPC` GameObject.
   * In the **Inspector**, find the **ConvaiNPC** component.
   * Enter your **Character Name** in the _Character Name_ field.
   * Paste your **Character ID** in the _Character ID_ field.

***

### Preparing for Build

1. Go to **File → Build Profiles**.
2. In the **Scene List**, right-click the default _Sample Scene_ and remove it.
3. Click **Add Open Scenes** to include the _Convai Sample Scene_ instead.
4. Under **Profiles**, select **Meta Quest** and click **Switch Platform** in the bottom-right corner.
5. From the top menu, go to **Meta XR Tools → Project Setup Tool**.
   * In the opened window, click **Fix All** for both **PC** and **Meta Quest**.
6. Return to the **Build Profiles** window.
   * If a device is selected under **Run Device**, click **Build and Run** to deploy directly to your headset.
   * If no device is selected, click **Build** to generate the build manually.

***

## Conclusion

You have now completed the setup of the Convai Unity Plugin (Beta) and prepared your project for MR-ready development.\
From this point forward, you can begin tailoring the sample scene, integrating your own Convai characters, and extending the plugin’s capabilities to fit your project’s interaction, gameplay, or AI-driven design needs.

As new features, improvements, and LipSync support arrive in upcoming releases, you will be able to enhance your experience even further and build more immersive, intelligent, and voice-driven Unity applications.
