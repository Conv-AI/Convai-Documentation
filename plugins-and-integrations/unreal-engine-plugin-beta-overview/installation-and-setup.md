---
description: >-
  Learn how to install, configure, and integrate the Convai Unreal Plugin Beta
  to bring conversational AI and real-time vision into your Unreal Engine
  projects.
---

# Installation and Setup

## Introduction

The **Convai Unreal Engine Plugin (Beta)** brings powerful, real-time conversational AI directly into **Unreal Engine**.\
Rebuilt from the ground up, offering low-latency dialogue, environment-aware interactions, and hands-free communication.

Whether you’re building immersive NPCs or AI companions inside player suits, the plugin enables natural, voice-driven experiences powered by Convai characters.

{% embed url="https://www.youtube.com/watch?v=n-UG3nmMeZQ" %}

***

### Installation Guide

There are **two ways to install the Convai Unreal Plugin**:

1. **Install via FAB (Recommended)** – easiest method
2. **Manual Installation (Advanced)** – use if you need the latest version from GitHub

{% hint style="danger" %}
## Beta Notice

This package is currently in **beta, y**ou may encounter **unexpected issues or behavior**.

If you experience any problems, please report them via the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}

***

### 1. Install via FAB (Recommended)

1. Open the Convai plugin page on FAB: [https://www.fab.com/listings/ba3145af-d2ef-434a-8bc3-f3fa1dfe7d5c](https://www.fab.com/listings/ba3145af-d2ef-434a-8bc3-f3fa1dfe7d5c)
2. Click **Add to Library**.
3. In **Epic Games Launcher → Library**, install the plugin to your Unreal Engine version.
4. Open your Unreal project and continue to **Enable the Plugin** below.

***

### 2. Manual Installation (Latest Version)

Use this method if you want the **latest SDK release**.

#### Step 1 — Download the Plugin

1. Go to the GitHub releases page: [https://github.com/Conv-AI/Convai-UnrealEngine-SDK-V4/releases](https://github.com/Conv-AI/Convai-UnrealEngine-SDK-V4/releases)
2. Download the latest `.zip` file.
3. Extract the archive — it will contain a folder named **Convai**.

***

#### Step 2 — Install the Plugin

You can install the plugin **engine-wide** or **per project**.

**Option A — Engine-Level Installation (Recommended)**

Makes the plugin available to **all Unreal projects** using the same engine version.

1. Navigate to your Unreal Engine installation folder.
2. Copy the **Convai** folder to:

```
Engine/Plugins/Marketplace
```

Example (Windows):

```
C:\Program Files\Epic Games\UE_5.x\Engine\Plugins\Marketplace
```

***

**Option B — Project-Level Installation**

Installs the plugin **for a single project**.

1. Navigate to your project root (where the `.uproject` file is).
2. Create a folder called **Plugins** if it does not exist.
3. Copy the **Convai** folder here:

```
YourProject/Plugins/Convai
```

***

### 3. Enable the Plugin in Unreal

1. Open your Unreal project.
2. Go to:

```
Edit → Plugins
```

3. Search for **Convai**.
4. Enable the plugin.
5. Restart Unreal when prompted.

***

## Configuring Your Player Blueprint

Once the plugin is enabled, you’ll need to add two main components to your **Player Blueprint** to enable AI interactions.

### 1. Add the Player Component

1. Open your main player Blueprint (for example, `BP_FirstPersonCharacter`).
   * If unsure, press **Play**, select your character in the **World Outliner**, and click **Edit Blueprint** in the **Details** panel.
2. In the **Components** panel, click **+ Add → BP\_ConvaiPlayerComponent**.
   * This handles player-side input, microphone control, and chat UI management.

### 2. Add the Chatbot Component

1. Open your character Blueprint.
2. Click **+ Add** again and select **BP\_ConvaiChatbotComponent**.
   * This is the AI "brain," managing conversation logic, speech, and vision capabilities.
3. Open the [Convai Playground](https://convai.com/playground) and select or create a character.
4. Copy the **Character ID**.
5. Back in Unreal, select the **BP\_ConvaiChatbotComponent** and paste the ID into the **Character ID** field in the **Details** panel.
6. **Compile** and **Save** your Blueprint.

{% hint style="info" %}
**Note:** This is a bare minimum setup with no animations, lipsync or facial expressions — There are dedicated tutorials that shows how to integrate with different kinds of Avatars (i.e.  Metahumans, Reallusion, etc..)
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

1. In your Character Blueprint, click **+ Add → EnvironmentWebcam**.
2. Adjust the **EnvironmentWebcam** position and rotation to align with the Character's head.
   * Needs to be slightly in front of the character's head so it does not collide.
3. In the **Content Browser**, right-click and select **Convai → Vision Render Target**.
   * Name it something like `RT_Vision`.
4. Return to your Blueprint, select the **EnvironmentWebcam**, and set **Convai Render Target** to `RT_Vision`.
5. Ensure **Auto Start Vision** is checked.
6. Press **Play**, look at an object in the world, and ask your AI about it.

***

## Conclusion

You’ve successfully set up the **Convai Unreal Engine Plugin (Beta)** and connected your first Convai character.\
With just a few steps, you’ve enabled voice-based conversation, environmental awareness, and real-time interaction within Unreal Engine.

Continue exploring to customize your setup, integrate multiple characters, or connect advanced Convai features. For feedback and community discussions, visit the [Convai Developer Forum](https://forum.convai.com/).
