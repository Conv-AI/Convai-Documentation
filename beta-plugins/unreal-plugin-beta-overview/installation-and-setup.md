---
description: >-
  Learn how to install, configure, and integrate the Convai Unreal Plugin Beta
  to bring conversational AI and real-time vision into your Unreal Engine
  projects.
---

# Installation and Setup

## Introduction

The **Convai Unreal Plugin (Beta)** brings powerful, real-time conversational AI directly into **Unreal Engine**.\
Rebuilt from the ground up, offering low-latency dialogue, environment-aware interactions, and hands-free communication.

Whether you’re building immersive NPCs or AI companions inside player suits, the plugin enables natural, voice-driven experiences powered by Convai characters.

***

{% embed url="https://youtu.be/xgdjLJJmHIE" %}

## Installation Guide

You can install the Convai Unreal Plugin using one of two methods, depending on whether you want a project-specific or engine-wide setup.

### 1. Download the Plugin

1. Visit the official Convai Unreal SDK GitHub Releases page:\
   [https://github.com/Conv-AI/Convai-UnrealEngine-SDK-V4/releases](https://github.com/Conv-AI/Convai-UnrealEngine-SDK-V4/releases)
2. Download the latest release `.zip` file.
3. Extract the archive — you should see a folder named **Convai**.

***

### 2. Install the Plugin

#### Method A — Engine-Level Installation (Recommended for Most Users)

This method makes the plugin available to all Unreal projects using the same engine version.

1. Navigate to your Unreal Engine installation directory.
2.  Place the **Convai** folder in the following path:

    ```
    Engine\Plugins\Marketplace
    ```

    **Default Windows Path:**

    ```
    C:\Program Files\Epic Games\UE_5.x\Engine\Plugins\Marketplace
    ```

#### Method B — Project-Level Installation (C++ Projects Only)

This installs the plugin for a single Unreal project.

1. Navigate to your project’s root directory (where the `.uproject` file is located).
2. Create a folder named **Plugins** if it doesn’t exist.
3.  Copy the **Convai** folder into this new directory:

    ```
    YourProject\Plugins\Convai
    ```

{% hint style="info" %}
This method requires your project to be a **C++ project**.\
Blueprint-only projects must use **Method A**.
{% endhint %}

***

### 3. Enable the Plugin in Unreal

1. Launch your Unreal Engine project.
2. Go to **Edit → Plugins**.
3. Search for **Convai** and enable it.
4. Restart the editor when prompted.

***

## Configuring Your Player Blueprint

Once the plugin is enabled, you’ll need to add two main components to your **Player Blueprint** to enable AI interactions.

### 1. Add the Player Component

1. Open your main player Blueprint (for example, `BP_MarsPlayer`).
   * If unsure, press **Play**, select your character in the **World Outliner**, and click **Edit Blueprint** in the **Details** panel.
2. In the **Components** panel, click **+ Add → BP\_ConvaiPlayerComponent**.
   * This handles player-side input, microphone control, and chat UI management.

### 2. Add the Chatbot Component

1. Click **+ Add** again and select **BP\_ConvaiChatbotComponent**.
   * This is the AI "brain," managing conversation logic, speech, and vision capabilities.
2. Open the [Convai Playground](https://convai.com/playground) and select or create a character.
3. Copy the **Character ID**.
4. Back in Unreal, select the **BP\_ConvaiChatbotComponent** and paste the ID into the **Character ID** field in the **Details** panel.
5. **Compile** and **Save** your Blueprint.

{% hint style="info" %}
In this tutorial setup, the AI acts as an in-suit assistant (similar to “Jarvis”).\
For traditional NPCs, add **BP\_ConvaiChatbotComponent** to the NPC’s Blueprint instead.\
The **BP\_ConvaiPlayerComponent** should always remain on the player.
{% endhint %}

***

## Testing the Setup

### Push-to-Talk Mode

1. Press **Play** in the editor.
2. By default, the plugin uses **Push-to-Talk** mode.
3. Hold the **T** key to speak with your AI.

### Hands-Free Mode

1. Stop the game and open your Player Blueprint.
2. Select **BP\_ConvaiPlayerComponent**.
3. In the **Details** panel, under the **Default** category, uncheck **Enable Push To Talk**.
4. Compile and play again — you can now speak freely without pressing any key.

### Adjusting the Chat UI

You can change the chat interface’s look and position:

1. Select the **BP\_ConvaiPlayerComponent**.
2. In the **Details** panel, adjust **Chat Widget Style** (0, 1, or 2) to modify appearance and placement.

***

## Enabling Vision

To allow your AI character to “see” and describe the environment, follow these steps:

1. In your Player Blueprint, click **+ Add → EnvironmentWebcam**.
2. Drag the **EnvironmentWebcam** onto your player’s main camera (e.g., `FirstPersonCamera`) to parent it.
3. With **EnvironmentWebcam** selected, set its **Location** and **Rotation** to **0, 0, 0** in the **Details** panel.
4. In the **Content Browser**, right-click and select **Convai → Vision Render Target**.
   * Name it something like `RT_Vision`.
5. Return to your Blueprint, select the **EnvironmentWebcam**, and set **Convai Render Target** to `RT_Vision`.
6. Ensure **Auto Start Vision** is checked.
7. Press **Play**, look at an object in the world, and ask your AI about it.

***

## Conclusion

You’ve successfully set up the **Convai Unreal Plugin (Beta)** and connected your first Convai character.\
With just a few steps, you’ve enabled voice-based conversation, environmental awareness, and real-time interaction within Unreal Engine.

Continue exploring to customize your setup, integrate multiple characters, or connect advanced Convai features. For feedback and community discussions, visit the [Convai Developer Forum](https://forum.convai.com/).
