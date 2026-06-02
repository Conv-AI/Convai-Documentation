---
title: Install the Convai plugin
description: Install the Convai Unreal Engine plugin from Fab or GitHub Releases, enable it in your project, and restart the Unreal Editor.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin is available through two channels. Choose the one that fits your workflow, then enable the plugin in your project.

{% hint style="info" %}
The quick-setup video at [Watch the installation walkthrough video](https://youtu.be/n-UG3nmMeZQ) shows the full install and first-character flow end to end.
{% endhint %}

## Install from Fab

Fab updates lag slightly behind GitHub Releases but provide the most stable builds.

{% stepper %}
{% step %}
### Open the Fab listing

Open the Epic Games Launcher and navigate to the Fab store, or go directly to the plugin listing:

[Convai plugin on Fab](https://www.fab.com/listings/ba3145af-d2ef-434a-8bc3-f3fa1dfe7d5c)
{% endstep %}

{% step %}
### Install the plugin for your engine version

On the listing page, click **Install Plugin**. Select the Unreal Engine version that matches your project and click **Install**. The download takes a few seconds.
{% endstep %}

{% step %}
### Launch your project

Open your project in Unreal Engine. The plugin will be available for enabling in the next step.
{% endstep %}
{% endstepper %}

## Install from GitHub Releases

GitHub Releases ships new features and fixes sooner than Fab. Use this method when you need the latest build or a specific version.

{% stepper %}
{% step %}
### Download the release zip

Go to [Convai Unreal Engine SDK releases on GitHub](https://github.com/Conv-AI/Convai-UnrealEngine-SDK/releases) and find the release that matches the version you want. Download the zip file for your Unreal Engine version.
{% endstep %}

{% step %}
### Extract the plugin

Extract the zip file. The extracted folder should be named `Convai` and contain `ConvAI.uplugin` at its root.
{% endstep %}

{% step %}
### Create a Plugins folder in your project

In your project's root directory (the folder that contains your `.uproject` file), create a `Plugins/` folder if one does not already exist.
{% endstep %}

{% step %}
### Move the plugin into your project

Copy or move the `Convai` folder into `Plugins/`. The final path should be:

```text
YourProject/
  Plugins/
    Convai/
      ConvAI.uplugin
```
{% endstep %}

{% step %}
### Open your project

Launch the Unreal Editor with your project. If prompted to rebuild modules, click **Yes**.
{% endstep %}
{% endstepper %}

## Enable the plugin

Both install methods require you to enable the plugin inside the editor:

{% stepper %}
{% step %}
### Open the Plugins panel

In the Unreal Editor menu bar, select **Edit > Plugins**.
{% endstep %}

{% step %}
### Find and enable Convai

In the search box, type `Convai`. Locate the **Convai** plugin in the results and check the **Enabled** checkbox.
{% endstep %}

{% step %}
### Restart the editor

A restart prompt appears. Click **Restart Now**. After the editor reopens, a sign-in prompt from the Convai editor window may appear automatically. If it does not, click the Convai icon in the toolbar to open it.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When the plugin loads correctly, the Convai toolbar icon appears in the Unreal Editor toolbar and the Convai editor window opens or is accessible via the icon.
{% endhint %}

## Fab vs GitHub: which to choose

| Factor | Fab | GitHub Releases |
|---|---|---|
| Update frequency | Less frequent | More frequent |
| Stability | Most stable builds | Latest features, may include pre-release fixes |
| Install method | Epic Games Launcher | Manual: download, extract, copy to `Plugins/` |
| Engine version selection | Handled by launcher | Choose the zip matching your UE version |

## Next steps

After the plugin is enabled, configure your API key: [Configure your API key](configure-api-key.md).
