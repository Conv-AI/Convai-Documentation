---
description: >-
  This guide walks you through downloading, installing, and setting up the basic
  features of the Convai Beta plugin in your Unreal Engine project, including
  conversational AI and vision.
---

# \[Backup] Installation and Setup

{% embed url="https://www.youtube.com/watch?v=xgdjLJJmHIE" %}

#### 1. Download & Installation

First, you need to download and install the plugin. Choose one of the two methods below.

1. Download the Plugin:
   * Go to the official GitHub releases page: [https://github.com/Conv-AI/Convai-UnrealEngine-SDK-V4/releases](https://github.com/Conv-AI/Convai-UnrealEngine-SDK-V4/releases)
   * Download the latest plugin release.\

2.  Extract and Install:

    * Extract the downloaded `.zip` file. You should have a folder named `Convai`.
    * Copy this `Convai` folder to one of the following locations:

    **Method A: Engine-Level Installation (Works for All Projects)**

    This method makes the plugin available to all your Unreal Engine projects for that specific engine version.

    * Navigate to your Unreal Engine installation directory.
    * Place the `Convai` folder inside `Engine\Plugins\Marketplace`.
    * Default Path (Windows): `C:\Program Files\Epic Games\UE_5.x\Engine\Plugins\Marketplace`

    **Method B: Project-Level Installation (C++ Projects Only)**

    This method installs the plugin only for a specific project.

    * Navigate to your project's root folder (where your `.uproject` file is).
    * Create a folder named `Plugins` if one doesn't already exist.
    * Place the `Convai` folder inside the `Plugins` folder.
    * Path: `YourProject\Plugins\Convai`
    * Note: This method requires your project to be a C++ project. If you have a Blueprint-only project, you must use Method A.\

3. Enable the Plugin in-Editor:
   * Launch your Unreal Engine project.
   * Once the project opens, go to `Edit` > `Plugins`.
   * Search for "Convai" and enable it.
   * Restart the editor as prompted.

***

#### 2. Basic Setup: Adding AI to Your Player

Next, add the necessary components to your player's Blueprint to enable the AI.

1.  Open Your Player Blueprint:

    * Locate and open your main player character's Blueprint (e.g., `BP_MarsPlayer` in the video).

    > Tip: If you can't find your Player Blueprint, press Play, select your character in the World Outliner, and click the Edit Blueprint button in the `Details` panel.


2.  Add the Convai Player Component:

    * In the `Components` panel of your Blueprint, click + Add.
    * Search for and add the `BP_ConvaiPlayerComponent`.
    * This component handles the player-side interactions, such as the input and the chat UI.


3.  Add the Convai Chatbot Component:

    * Click + Add again.
    * Search for and add the `BP_ConvaiChatbotComponent`.
    * This component is the "brain" of the AI, handling conversation, vision, and other functionalities.


4.  Link Your Convai Character:

    * Go to the [Convai website playground](https://www.convai.com/) and log in.
    * Select the character you want to use or create a new one.
    * Find and copy the Character ID.
    * Back in your Player Blueprint, select the `BP_ConvaiChatbotComponent`.
    * In the `Details` panel, find the Character ID field and paste your copied ID into it.


5. Compile and Save your Blueprint.

> Note on This Tutorial's Setup:
>
> This video shows a specific use case where the AI acts as an assistant inside the player's suit (like Jarvis). This is why the BP\_ConvaiChatbotComponent is added directly to the BP\_MarsPlayer Blueprint.
>
> For a traditional in-world NPC, you would follow a similar process, but instead, you would add the `BP_ConvaiChatbotComponent` to that NPC's own Blueprint, not the player's. The `BP_ConvaiPlayerComponent` always stays on the player.

***

#### 3. Testing & Configuration

You can now test the basic setup and configure it to your liking.

*   Test (Push-to-Talk):

    * Press Play in the editor.
    * By default, the plugin is in Push-to-Talk mode. Press and hold the T key to talk to your AI.


*   Configure Hands-Free Mode:

    * Stop the game and go back to your Player Blueprint.
    * Select the `BP_ConvaiPlayerComponent`.
    * In the `Details` panel, find the `Default` category and uncheck Enable Push To Talk.
    * Compile and play again. You can now speak to the AI without pressing any key.


* Configure UI Style:
  * Select the `BP_ConvaiPlayerComponent` again.
  * In the `Details` panel, change the Chat Widget Style from `0` to `1` or `2` to change the appearance and screen location of the chat UI.

***

#### 4. Adding Vision to Your AI

Follow these steps to allow your AI to see and describe the game world.

1.  Add the Webcam Component:

    * In your Player Blueprint's `Components` panel, click + Add.
    * Search for and add the `EnvironmentWebcam` component.


2.  Attach to Camera:

    * Drag the new `EnvironmentWebcam` component onto your player's camera (e.g., `FirstPersonCamera`) to parent it. This ensures the webcam moves with the player's view.


3.  Position the Webcam:

    * With the `EnvironmentWebcam` still selected, go to the `Details` panel.
    * Reset its Location and Rotation to `0, 0, 0`. This will place it exactly where your player's camera is.


4.  Create a Vision Render Target:

    * Go to the Content Browser.
    * Right-click, and from the menu, select `Convai` > `Vision Render Target`.
    * Give the new asset a name, for example, `RT_Vision`.


5.  Link the Render Target:

    * Go back to your Player Blueprint and select the `EnvironmentWebcam` component.
    * In the `Details` panel, find the Convai Render Target setting.
    * Click the dropdown and select the `RT_Vision` asset you just created.


6.  Enable Vision:

    * On the same `EnvironmentWebcam` component, ensure the Auto Start Vision checkbox is enabled.


7.  Compile, Save, and Test:

    * Press Play.
    * Look at a distinct object in the world.
    * Ask your AI about it.



You now have a fully functional Convai AI in your project with both conversational and vision capabilities.
