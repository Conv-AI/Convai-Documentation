---
title: Import and run sample scenes
description: >-
  Import the bundled sample scenes and verify the SDK is installed and connected
  correctly before building your own scene.
last_reviewed: "4.2.0"
---

The Convai SDK for Unity ships with two sample packages. Running one is the fastest way to confirm your installation, API key, and audio setup are working before you build your own scene.

| Sample package | Scenes | Description |
| --- | --- |
| **Basic Sample** | `Basic Sample.unity`, `Basic Sample 1.unity` | Basic conversation with a robot character. `Basic Sample 1.unity` is an alternate layout that uses the refreshed robot materials. |
| **LipSync Sample** | `LipSync Sample.unity` | High-quality character with real-time lip sync |

The steps for locating the samples differ depending on how you installed the SDK.

{% tabs %}
{% tab title="Package Manager" %}
{% stepper %}
{% step %}
### Open Package Manager

In the Unity Editor, open **Window > Package Manager**. In the top-left dropdown, select **In Project**, then select **Convai SDK for Unity** from the list.
{% endstep %}

{% step %}
### Import a sample

In the detail panel on the right, click the **Samples** tab. Click **Import** next to the sample you want to run.

Unity copies the sample assets into `Assets/Samples/Convai SDK for Unity/<version>/`. A new folder appears under `Assets/Samples/` in the Project window.
{% endstep %}

{% step %}
### Open the scene

In the Project window, navigate to the imported sample folder and open its `.unity` scene file.
{% endstep %}
{% endstepper %}
{% endtab %}

{% tab title="Asset Store" %}
{% stepper %}
{% step %}
### Locate the samples

When installed via the Asset Store, all sample scenes are imported into your project automatically. In the Project window, navigate to:

```text
Assets/Convai SDK For Unity/Samples/
```

Two sample folders are present: `BasicSample` and `LipSyncSample`.
{% endstep %}

{% step %}
### Open the scene

Open the `.unity` scene file inside the sample folder you want to run.
{% endstep %}
{% endstepper %}
{% endtab %}
{% endtabs %}

Once the scene is open:

{% stepper %}
{% step %}
### Enter Play Mode

Press **Play**. The Unity Console logs the following lines as the SDK initializes:

* `[ConvaiRuntime] Started successfully` — SDK initialized all internal services
* `[RoomConnectionRuntimeAdapter] Character <character-id> connected successfully (mode=create).` — character connected to Convai

Speak into your microphone. The character responds with voice and text output.

If no response appears and the Console shows warnings, check [Validate your setup](validate-your-setup.md) for a diagnostic checklist.
{% endstep %}
{% endstepper %}

## Sample render pipeline notes

Sample scenes are built with the Universal Render Pipeline (URP). If your project uses a different render pipeline, materials may appear pink after import. Convert the materials to match your active render pipeline using **Edit > Rendering > Materials**, then select the appropriate conversion option for your pipeline.

## Next steps

Now that you have confirmed the SDK is working, learn what each scene component does before building your own setup.

{% content-ref url="scene-components.md" %}
[Scene components reference](scene-components.md)
{% endcontent-ref %}
