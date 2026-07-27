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

<figure><img src="../../../../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

## 2. Download the tutorial files

1. [Download the Stack O Bot Convai tutorial delta](https://drive.google.com/uc?export=download\&id=1RvlntYxX_Q-pr7Q_O0jYwhzrmob1WEgd).
2. Right-click the downloaded ZIP and select **Extract All**.
3. Open the extracted folder.
4. Open the Stack O Bot project folder you created earlier.
5. Copy everything inside the extracted delta folder into the project folder.
6. When Windows asks, select **Replace the files in the destination**.

{% hint style="warning" %}
Copy the contents of the delta folder, not the outer folder itself. The `Content` and `Config` folders must be directly beside `StackOBot.uproject`.
{% endhint %}

## 4. Open and test the project

1. Install and enable the matching Convai Unreal Engine plugin release [install-the-convai-plugin.md](../../getting-started/install-the-convai-plugin.md "mention").
2. Open `StackOBot.uproject` with Unreal Engine 5.8.
3. Open the Convai Editor and sign in.
4. Open `Content/StackOBot/Maps/Convai/Lvl_Convai` and press **Play**.

If files appear to be missing, check that extraction did not create an extra nested folder and that you opened the UE 5.8 copy of the project.
