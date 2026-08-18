---
title: Stack O Bot tutorial setup
description: Build the sample project used by the Convai character actions tutorial, starting from Epic's free Stack O Bot and applying the Convai tutorial files.
last_reviewed: "4.0.0-beta.27"
---

Convai's AI player tutorial series is filmed in Epic Games' free Stack O Bot sample with a set of Convai files applied on top. In it, a human player and a Convai-powered teammate solve a two-player puzzle that neither can finish alone. This page builds that project from scratch so your editor matches the video. You need it only if you want to follow along in the same scene; every feature the series covers works in any project.

{% embed url="https://youtu.be/KcJETVhI7KM" %}
Part one of the AI player series, filmed in this project
{% endembed %}

## Before you start

- **Unreal Engine 5.8.** The tutorial files were prepared against 5.8. A project created with a different engine version will not match the tutorial.
- **An Epic Games account**, to claim Stack O Bot from Fab.
- **The Convai plugin installed and your API key configured.** See [Install the Convai plugin](install-the-convai-plugin.md) and [Configure your API key](configure-your-api-key.md).

{% hint style="info" %}
Stack O Bot is published by Epic Games and is free. The Convai tutorial files are a separate download that only adds the maps, Blueprints, and configuration the tutorial uses.
{% endhint %}

## Create the Stack O Bot project

{% stepper %}
{% step %}
### Claim Stack O Bot on Fab

Open [Stack O Bot on Fab](https://www.fab.com/listings/b4dfff49-0e7d-4c4b-a6c5-8a0315831c9c), sign in with your Epic Games account, and select **Add to My Library**. Accept the license if prompted.

<figure><img src="../../../.gitbook/assets/image (15).png" alt="The Stack O Bot listing on Fab, showing the Add to My Library button"><figcaption><p>Stack O Bot is free and published by Epic Games.</p></figcaption></figure>
{% endstep %}

{% step %}
### Create the project from the Epic Games Launcher

Open the Epic Games Launcher and go to **Unreal Engine > Library > Fab Library**. Find **Stack O Bot**, select **Create Project**, and choose Unreal Engine 5.8.
{% endstep %}

{% step %}
### Note the project location

Copy or write down the project folder before creating the project. You need this path in the next section, and the launcher does not show it again afterwards.
{% endstep %}
{% endstepper %}

## Apply the Convai tutorial files

The tutorial files are a delta: they contain only what was added or changed for the Convai tutorial, laid out to be copied over the project you created above.

{% stepper %}
{% step %}
### Download the tutorial files

Download the Convai Stack O Bot tutorial delta from [the Convai tutorial delta download](https://drive.google.com/uc?export=download\&id=1RvlntYxX_Q-pr7Q_O0jYwhzrmob1WEgd). The archive contains a `Content` folder and a `Config` folder.
{% endstep %}

{% step %}
### Extract the archive

Right-click the downloaded ZIP, select **Extract All**, and open the extracted folder. Confirm you can see `Content` and `Config` directly inside it.
{% endstep %}

{% step %}
### Copy the delta into the project

Open the Stack O Bot project folder you recorded earlier. Copy everything **inside** the extracted folder into the project folder, and select **Replace the files in the destination** when Windows asks.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Copy the contents of the delta folder, not the folder itself. When the copy is correct, `Content` and `Config` sit directly beside `StackOBot.uproject`. A nested extra folder is the most common reason the maps do not appear.
{% endhint %}

## Open and test the project

{% stepper %}
{% step %}
### Open the project

Open `StackOBot.uproject` with Unreal Engine 5.8. If the editor asks to rebuild modules, allow it.
{% endstep %}

{% step %}
### Sign in to Convai

Open the Convai Editor window and sign in. See [Sign in and manage your account](../editor-window/sign-in-and-manage-your-account.md).
{% endstep %}

{% step %}
### Play the tutorial level

Open `Content/StackOBot/Maps/Convai/Lvl_Convai` and press **Play**.
{% endstep %}
{% endstepper %}

## Verify the setup

The project is ready when `Lvl_Convai` appears in the **Content Browser** under `Content/StackOBot/Maps/Convai`, the level opens without missing-asset warnings, and the Convai character responds when you speak to it in Play mode.

If the map is missing, the delta was copied one level too deep — check that `Content` and `Config` are beside `StackOBot.uproject` rather than inside another folder. If the map opens but the character does not respond, the plugin is installed but not authenticated; work through [Configure your API key](configure-your-api-key.md).

## Next steps

With the sample project running, follow the series in the scene it was filmed in. Part one brings the AI teammate into the level, enables actions, and tags the pressure plates and the moving platform; part two adds the custom pickup and drop actions for the crate. The pages below cover the same ground in written form.

{% content-ref url="../features/character-actions/character-actions-quick-start.md" %}
[Character actions quick start](../features/character-actions/character-actions-quick-start.md)
{% endcontent-ref %}
