---
title: Import and run sample scenes
description: >-
  Import the bundled sample scenes and verify the SDK is installed and connected
  correctly before building your own scene.
last_reviewed: "4.2.0"
---

The Convai SDK for Unity ships with sample scenes that demonstrate core features. Importing and running a sample is the fastest way to confirm that your installation, API key, and audio setup are all working before you build your own scene.

{% stepper %}
{% step %}
### Open Package Manager

In the Unity Editor, open **Window > Package Manager** and select **Convai SDK for Unity** from the list.
{% endstep %}

{% step %}
### Import a sample

In the detail panel on the right, click the **Samples** tab. Find the sample you want to try and click **Import**.

Unity copies the sample assets into `Assets/Samples/Convai SDK for Unity/<version>/`. A new folder appears under `Assets/Samples/` in the Project window.
{% endstep %}

{% step %}
### Open the scene

In the Project window, navigate to the imported sample folder and open its scene file (`.unity`).
{% endstep %}

{% step %}
### Set the Character ID

Select the NPC GameObject in the Hierarchy. In the Inspector, find the `ConvaiCharacter` component and set the **Character ID** field to a valid ID from your [Convai dashboard](<code class="expression">space.vars.dashboard_url</code>).

{% hint style="warning" %}
Sample scenes ship without a Character ID — the scene will not connect to Convai until you set one. Each character on your Convai dashboard has a unique ID shown on its profile page.
{% endhint %}
{% endstep %}

{% step %}
### Enter Play Mode

Press **Play**. The Unity Console logs the following lines as the SDK initializes:

* `[ConvaiRuntime] Started successfully` — SDK initialized all internal services
* `[RoomConnectionRuntimeAdapter] Character <character-id> connected successfully (mode=create).` — character connected to Convai

Speak into your microphone. The character responds with voice and text output.

If no response appears and the Console shows warnings, check [Validate Your Setup](validate-your-setup.md) for a diagnostic checklist.
{% endstep %}
{% endstepper %}

## Sample render pipeline notes

Sample scenes are built with the Universal Render Pipeline (URP). If your project uses the Built-in Render Pipeline or HDRP, materials may appear pink after import. Reassign the materials using your active render pipeline's shaders, or run **Edit > Rendering > Materials > Convert All Built-in Materials to URP** if switching to URP.

## Next steps

Now that you have confirmed the SDK is working, learn what each scene component does before building your own setup.

{% content-ref url="scene-components.md" %}
[Scene components reference](scene-components.md)
{% endcontent-ref %}
