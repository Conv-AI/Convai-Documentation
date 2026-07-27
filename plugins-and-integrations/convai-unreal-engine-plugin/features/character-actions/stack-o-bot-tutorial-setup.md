---
description: Create the Stack O Bot sample project and apply the Convai tutorial files.
---

# Stack O Bot tutorial setup

This guide starts with a clean copy of Epic Games' Stack O Bot sample and applies only the files added or changed for the Convai tutorial.

{% hint style="info" %}
This tutorial delta was prepared with Unreal Engine 5.8. Create a fresh Stack O Bot project with UE 5.8 so its files match the tutorial.
{% endhint %}

## 1. Create the Stack O Bot project

1. Open [Stack O Bot on Fab](https://www.fab.com/listings/b4dfff49-0e7d-4c4b-a6c5-8a0315831c9c).
2. Sign in with your Epic Games account and select **Add to My Library**. Accept the license if prompted.
3. Open the Epic Games Launcher.
4. Go to **Unreal Engine > Library > Fab Library**.
5. Find **Stack O Bot**, select **Create Project**, and choose Unreal Engine 5.8.
6. Choose a project location that is easy to find. Copy or write down this location before creating the project.

{% hint style="info" %}
**Screenshot placeholder:** Add a screenshot here showing Stack O Bot on Fab and the control used to add it to the library.
{% endhint %}

Wait for the project to finish downloading. Its project folder is the folder that contains `StackOBotTutorial.uproject`.

## 2. Download the tutorial files

1. [Download the Stack O Bot Convai tutorial delta](https://drive.google.com/uc?export=download\&id=1RvlntYxX_Q-pr7Q_O0jYwhzrmob1WEgd).
2. Save the ZIP somewhere easy to find.
3. Close Unreal Editor if the Stack O Bot project is open.

## 3. Apply the delta

1. Back up the project if you have already changed it.
2. Right-click the downloaded ZIP and select **Extract All**.
3. Open the extracted folder.
4. Open the Stack O Bot project folder you saved earlier—the folder containing `StackOBotTutorial.uproject`.
5. Copy everything inside the extracted delta folder into the project folder.
6. When Windows asks, select **Replace the files in the destination**.

{% hint style="warning" %}
Copy the contents of the delta folder, not the outer folder itself. The `Content` and `Config` folders must be directly beside `StackOBotTutorial.uproject`.
{% endhint %}

## 4. Open and test the project

1. Install and enable the matching Convai Unreal Engine plugin release.
2. Open `StackOBotTutorial.uproject` with Unreal Engine 5.8.
3. Allow Unreal Engine to rebuild project files if prompted.
4. In **Project Settings > Plugins > Convai**, enter your own Convai API key. The tutorial delta does not include one.
5. Open `Content/StackOBot/Maps/Convai/Lvl_Convai` and press **Play**.

If files appear to be missing, check that extraction did not create an extra nested folder and that you opened the UE 5.8 copy of the project.
