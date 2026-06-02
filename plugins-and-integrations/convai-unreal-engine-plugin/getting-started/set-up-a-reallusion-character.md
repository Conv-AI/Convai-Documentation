---
title: Set up a Reallusion (CC) character
description: Export a Reallusion CC5 avatar, import it into Unreal Engine, configure Convai components, and add the Reallusion animation Blueprint for lip sync.
last_reviewed: "4.0.0-beta.21"
---

This guide covers the full flow for connecting a Reallusion Character Creator 5 (CC5) avatar to the Convai Unreal Engine plugin. The companion video is at [https://www.youtube.com/watch?v=nyPNP-S92QI](https://www.youtube.com/watch?v=nyPNP-S92QI).

## Prerequisites

- Reallusion Character Creator 5 is installed.
- The Convai plugin is installed and your API key is configured (see [Install the Convai plugin](installation.md) and [Configure your API key](configure-api-key.md)).
- You have a Convai character ID from the dashboard.

## Prepare the animation in Character Creator 5

{% stepper %}
{% step %}
### Load your character

Open Character Creator 5. Navigate to **Project > Templates > CC Project** and select the character you want to use. Alternatively, load an existing CC project.
{% endstep %}

{% step %}
### Add an idle animation

Click **Animation** and locate an idle animation. A subtle idle (such as `idle03`) works well. Drag it onto the avatar to apply it. Verify that the animation plays on the avatar.
{% endstep %}

{% step %}
### Add the animation to the Perform List

Right-click on the animation in the animation panel and select **Find File**. This opens the animation's directory in your file system. Right-click the animation file and copy its path.

Go to **Motion > Perform > Perform List Editor**. Click **Add**, paste the path, select the animation, and click **Open**.
{% endstep %}

{% step %}
### Add a talking animation (optional)

Optionally, add a standing-and-talking animation that does not include lip sync (the plugin handles lip sync separately). Repeat the Find File and Perform List steps for the talking animation. Choose animations where the first and last frames are identical so looping plays without a visible cut.
{% endstep %}
{% endstepper %}

## Export the avatar from Character Creator 5

{% stepper %}
{% step %}
### Start the FBX export

In Character Creator 5, go to **File > Export > FBX > Clothed Character (Closed Character)**.
{% endstep %}

{% step %}
### Configure export settings

In the export dialog:

- Set **Target Tool Preset** to **Unreal (UE5)**.
- Set **FBX Option** to **Mesh and Motion**.
- Increase the **Max Texture Size** if you need higher-resolution textures.
- Ensure **Custom** is checked, then click the icon to **Load Perform** and select your animations.
- Check **Delete Hidden Faces**.
{% endstep %}

{% step %}
### Export the file

Click **Export**. Enter a filename, choose a destination folder, and click **Save**. The export takes a few minutes.
{% endstep %}
{% endstepper %}

## Install the Reallusion CC Auto Setup for Unreal Engine

The CC Auto Setup plugin sets up the correct materials and skeleton for Reallusion characters in Unreal Engine.

{% stepper %}
{% step %}
### Download and install CC Auto Setup

Download the CC Auto Setup tool from the link in the Reallusion tutorial video description. Double-click the installer, accept the license, and click **Next**. Note the destination folder path — you will need it in the next step.
{% endstep %}

{% step %}
### Copy the content and plugins folders

After installation, open the destination folder. Navigate to the subfolder matching your Unreal Engine version. Copy the `Content` and `Plugins` folders from that subfolder.
{% endstep %}

{% step %}
### Paste into your Unreal project

Open your Unreal project's root directory. Paste the copied `Content` and `Plugins` folders into the project root, merging with any existing folders.
{% endstep %}

{% step %}
### Launch the project

Open the project in Unreal Engine. The Auto Setup content and plugin are now available.
{% endstep %}
{% endstepper %}

## Import the Reallusion avatar into Unreal Engine

{% stepper %}
{% step %}
### Create a folder and import the FBX

In the **Content Browser**, create a new folder for the character. Drag the exported FBX file from your file system into this folder.
{% endstep %}

{% step %}
### Configure import settings

In the **FBX Import Options** dialog:

- Enable **Import Animations**.
- Set the **Custom Sample Rate** to **30 fps** (some animations import at a very high rate, which can cause playback issues).
- Expand the **Advanced** section and check **Import Morph Targets**.
- Click **Import All**.

Dismiss any warning popups that appear during import.
{% endstep %}

{% step %}
### Verify the import

Open the imported skeletal mesh in the editor. Confirm that the mesh has no deformations and that morph targets appear in the morph target list. Double-click an animation asset and confirm it plays smoothly with matching first and last frames.
{% endstep %}
{% endstepper %}

## Set up Convai in Unreal Engine

{% stepper %}
{% step %}
### Enable the Convai plugin

If you have not already enabled the plugin, go to **Edit > Plugins**, search for `Convai`, enable it, and restart the editor. Sign in through the Convai editor window to authenticate.
{% endstep %}

{% step %}
### Create a character Blueprint

In the character's **Content Browser** folder, right-click and select **Blueprint Class > Actor**. Name the Blueprint (for example, `BP_MyReallusionCharacter`).
{% endstep %}

{% step %}
### Add a Skeletal Mesh component

Open the Blueprint. In the **Components** panel, click **Add** and add a **Skeletal Mesh** component. In the **Details** panel, set the **Skeletal Mesh** to your imported Reallusion avatar.
{% endstep %}

{% step %}
### Add the Convai Chatbot component

Click **Add** in the **Components** panel. Search for `Convai Chatbot` and add `UConvaiChatbotComponent`. In the **Details** panel, paste your **Character ID** from the Convai dashboard into the **Character ID** field.
{% endstep %}

{% step %}
### Place the character in the level

Drag the character Blueprint from the **Content Browser** into the level viewport. Position the character.
{% endstep %}
{% endstepper %}

## Add the Convai Player component to the player pawn

If you have not already done this, open your player pawn Blueprint and add `UConvaiPlayerComponent`. For detailed steps, see [Add your first Convai character](add-your-first-character.md).

To find the player pawn from Play mode: press **Shift+F1** to release the mouse, click **Detach** in the toolbar, then click on the player character in the viewport and click **Edit Blueprint**.

## Test the conversation

Enter Play mode and speak to the character using push-to-talk (default: **V**) or the chat widget. The character should respond with voice audio. Body and idle animations play, but facial animation is not yet configured.

## Add the Reallusion animation Blueprint

The Reallusion character needs a dedicated animation Blueprint to connect the Convai lip sync data with the avatar's skeleton.

{% stepper %}
{% step %}
### Download the animation Blueprint

Download the Reallusion animation Blueprint from the Convai Google Drive folder:

[Convai Reallusion animation Blueprint (Google Drive)](https://drive.google.com/drive/folders/1k3072DH3zJXk2xTg-CJ_najnm0pyvZJS)

{% hint style="warning" %}
This asset is hosted on an external Google Drive folder. If the link is unavailable, contact [Convai support](https://forum.convai.com) to request the file.
{% endhint %}

Download the zip, extract it, and locate the animation Blueprint asset file.
{% endstep %}

{% step %}
### Copy the asset into your project

Copy the animation Blueprint asset into the `Content` folder inside your Unreal project's directory on disk (not through the editor — copy it directly to the file system). Then restart the Unreal Editor so it detects the new asset.
{% endstep %}

{% step %}
### Configure the animation Blueprint

After restart, find the animation Blueprint in the **Content Browser** and double-click it. When prompted, select your Reallusion avatar's skeleton.

Open the **Animation Graph** inside the animation Blueprint. In the **Content Drawer**, navigate to the character's motion folder and import the animation assets you exported from Character Creator 5. Drag and drop them into the animation graph and connect them to the appropriate states.

- If drag and drop does not connect, right-click in the graph, type `Play`, and manually select the animation by name.
- Repeat this for all required animations.
- Set the transition animation (used between states) to the idle animation.
- Talking animations are optional — the idle animation alone is sufficient.
- Ensure all animations are set to **Loop**.

Click **Compile** and **Save**.
{% endstep %}

{% step %}
### Assign the animation Blueprint to the character

Open the character Blueprint. Select the **Skeletal Mesh** component. In the **Details** panel, under **Animation**, set **Anim Class** to the Reallusion animation Blueprint you configured (the one named **Convai Reallusion Animation Blueprint** or similar depending on the downloaded asset).

Compile and save the Blueprint.
{% endstep %}
{% endstepper %}

## Add facial animation with Convai Face Sync

{% stepper %}
{% step %}
### Add the Convai Face Sync component

Open the character Blueprint. In the **Components** panel, click **Add** and search for `Convai Face Sync`. Add `UConvaiFaceSyncComponent`.
{% endstep %}

{% step %}
### Set the lip sync mode

Select the **Convai Face Sync** component. In the **Details** panel, set **Lip Sync Mode**:

- **MetaHuman Blendshapes** — for CC5 characters (which use a MetaHuman-compatible rig).
- **CC4 Extended Blendshapes** — for CC4 characters.
{% endstep %}

{% step %}
### Compile, save, and test

Click **Compile** and **Save**. Enter Play mode and speak to the character. The character now responds with full body animation and synchronized facial animation.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When the setup is complete, the Reallusion character's lips and facial expressions animate in sync with its spoken responses.
{% endhint %}

## Troubleshooting

### No facial animation

- Confirm that the **Convai Face Sync** component is present on the character Blueprint.
- Confirm that **Lip Sync Mode** is correct for your rig (MetaHuman Blendshapes for CC5, CC4 Extended Blendshapes for CC4).
- Confirm that **Import Morph Targets** was checked when importing the FBX.

### Body animation does not play

- Confirm that **Anim Class** on the Skeletal Mesh is set to the Reallusion animation Blueprint.
- Confirm that animations are set to **Loop** in the animation Blueprint.
- Confirm that the first and last frames of each animation match.

## Next steps

- [Configure the microphone](configure-microphone.md) — select a specific capture device.
- [Configure conversation input](configure-conversation-input.md) — enable hands-free mode.
- [Validate your setup](validate-your-setup.md) — full setup verification checklist.
