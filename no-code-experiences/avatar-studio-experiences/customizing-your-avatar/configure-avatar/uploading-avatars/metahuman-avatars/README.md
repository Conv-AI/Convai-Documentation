---
description: >-
  Upload custom Metahuman characters from Unreal Engine to Avatar Studio using
  the Convai Asset Uploader.
---

# Metahuman Avatars

## Introduction

This guide walks you through uploading **custom Metahuman avatars** to **Avatar Studio** using the **Convai Asset Uploader**. You'll generate a new project tailored for Metahumans, import your Metahuman asset, configure it, and finally upload it using Convai’s built-in tools.

## Prerequisites

Before you begin:

* Create your project using the [**Convai Asset Uploader**](../../../../../../plugins-and-integrations/asset-uploader/), and answer **`Y`** when asked if you’re using a Metahuman.
* Ensure you have a downloadable Metahuman available via **Quixel Bridge**.

***

## Step-by-Step Guide

### 1. Open the Project

Navigate to the folder where your project was created. Double-click the `YourProjectName.uproject` file to open it in Unreal Engine.

***

### 2. Add a Metahuman via Quixel Bridge

* Go to **Window > Quixel Bridge**.
* In Bridge, select **Metahumans** from the left-hand menu.
* Pick a Metahuman and click:
  * **Download** (if not already downloaded)
  * Then **Add** to include it in your project.

***

### 3. Locate and Open the Character Blueprint

After importing:

* Go to `Content/Metahumans/<CharacterName>/`.
*   Open the Blueprint: `BP_<CharacterName>`

    > ⏳ This may take some time to load.

***

### 4. Fix Compile Errors

If you see compile errors:

* In the bottom-right, click **Enable Missing** under any **Missing Plugins** or **Missing Project Settings** notices.

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2025-04-18 224336.png" alt=""><figcaption></figcaption></figure>

* Click **Restart Now** when prompted.
* Reopen the Blueprint and ensure it compiles successfully.

***

### 5. Prepare the Asset for Upload

1. Locate the folder:\
   `Plugins/<random code> Content/`\
   (e.g., `Plugins/AHK3LNKVC7FZA3I5JG3V Content/`)
2. Move the entire `Content/Metahumans/` folder into this directory.
   * Use **Move Here** to complete the action.
   * The final structure should mirror what’s shown in the screenshot.

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2025-04-18 231010.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
This folder determines what gets packaged and uploaded. Make sure everything is placed correctly.
{% endhint %}

***

### 6. Open the Asset Uploader Tool

* Navigate to `Content/Editor/AssetUploader`.
* Right-click on `AssetUploader` and select **Run Editor Utility Widget**.

***

### 7. Select the Character Asset

* Navigate to the `Plugins/<random code> Content/Metahumans/<CharacterName>/` directory.
* Select the `BP_<CharacterName>` Blueprint.
* Then, in the **Asset Uploader** window, click **Pick Asset**.

***

### 8. Capture a Thumbnail

* In the Asset Uploader window, click **Capture Thumbnail** to generate a preview image for your avatar.

***

### 9. Verify Functionality Before Upload

1. Drag `BP_<CharacterName>` into the Level.
2. Select the character and locate `BP_ConvaiChatbotComponent` in the **Details** panel.
3. Input a test **Character ID**.
4. Press **Play** and confirm:
   * Animations are working
   * Lip sync is functional
   * Character behaves as expected

{% hint style="info" %}
Before uploading, review the [MetaHuman hair and skin appearance guidelines](metahuman-hair-and-skin-appearance-guidelines.md) to check the groom and materials in Avatar Studio's target rendering profile.
{% endhint %}

***

### 10. Upload the Avatar

* In the Asset Uploader, click **Create Asset**.
* This will:
  * Package the avatar for Win64
  * Upload it to Avatar Studio

Monitor the **Output Log**:

* Look for `Package completed`
* Then wait for `Uploaded Asset`

{% hint style="warning" %}
If there’s an error during packaging, check the logs and share them on the [Convai Developer Forum](https://forum.convai.com/) for support.
{% endhint %}

{% hint style="info" %}
To delete a previously uploaded asset, open AssetUploader and click **Delete**.
{% endhint %}

***

## Performance considerations and limitations

{% hint style="warning" %}
Avatar Studio has a fixed real-time CPU, GPU, and memory budget. Convai's sample avatars are optimized for this environment, but custom MetaHumans are uploaded with the assets and logic you provide. A successful upload does not guarantee smooth hosted performance.
{% endhint %}

There is no single asset limit that suits every character. Performance depends on the combined cost of the avatar, animation, background, and custom behavior. Review the complete experience:

* **Hair and grooms:** Hair and facial grooms can be expensive to render. Keep strand, curve, point, and group complexity only as high as the intended look requires. Remove unused groom components, disable simulation where it is not needed, and use shadow and material features carefully. See Epic's [groom performance guidance](https://dev.epicgames.com/documentation/unreal-engine/groom-scalability-and-performance-with-unreal-engine).
* **Geometry and accessories:** Remove hidden, duplicate, or unused geometry and components. Keep custom clothing, accessories, cloth, and deformation complexity appropriate for what the learner will actually see.
* **Textures and materials:** Use texture resolutions appropriate for the intended framing, and remove unnecessary material slots or expensive shader features. Do not rely on ray tracing- or Lumen-specific appearance; review hair and skin materials under the hosted lighting and rendering setup.
* **Blueprints and animation:** Prefer event-driven Blueprint behavior. Avoid unnecessary work on **Event Tick**, per-frame searches or allocations, and components that keep ticking when they are not in use. Limit simultaneous animation, physics, control-rig, and procedural systems to those needed for the current interaction.
* **Check the hosted experience:** After uploading, use the experience through Avatar Studio on the website. Check loading and interaction responsiveness, animation smoothness, lip-sync and audio timing, and visual consistency.

If performance is lower than expected, simplify one costly feature at a time and upload again. Start with the groom, followed by geometry, materials, textures, and custom Blueprint effects.

***

## Accessing the Avatar

1. Go to [Avatar Studio](https://convai.com/)
2. Open the **Upload Your Custom Avatar** section
3. Your Metahuman will appear, ready for use.

***

## Summary

Using the Convai Asset Uploader, uploading custom Metahuman avatars is quick and reliable. With proper setup and a few clicks, your characters are live in Avatar Studio and ready for real-time AI interaction.
