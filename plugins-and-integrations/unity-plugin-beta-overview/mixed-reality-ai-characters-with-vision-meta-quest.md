---
description: >-
  Build a Convai-powered AI character that runs in a Meta Quest passthrough
  Mixed Reality app and can see and describe the real world around the user
  through the Quest camera.
---

# Mixed Reality AI Characters with Vision (Meta Quest)

{% hint style="info" %}
**Prerequisites:**

* A Unity URP project already converted to Android build target
* Convai Unity SDK installed and verified working
* Meta Quest 3 or Pro device for deployment

If you have not set up the Convai SDK yet, start with the [Unity SDK Installation Guide](https://docs.convai.com/api-docs/plugins-and-integrations/unity-plugin-beta-overview/getting-started) before continuing.
{% endhint %}

### Required Packages

Three packages are needed for this setup:

| Package             | Git URL                              |
| ------------------- | ------------------------------------ |
| Convai Unity SDK    | `com.convai.convai-sdk-for-unity`    |
| Meta MR Utility Kit | `com.meta.xr.mrutilitykit@85`        |
| OVR Interaction     | `com.meta.xr.sdk.interaction.ovr@85` |

The Meta MR Utility Kit automatically installs the XR Core SDK as a dependency. You do not need to install it separately.

### Step 1 — Install MR Packages

<figure><img src="../../.gitbook/assets/image (467).png" alt=""><figcaption></figcaption></figure>

1. Go to **Window > Package Manager**.
2. Click the **+** icon and select **Install Package from Git URL**.
3. Paste in the **Meta MR Utility Kit** package name and let it install. This also installs the XR Core SDK automatically.
4. Repeat the process to install the **OVR Interaction** package.

You may see a few warnings after installation. These are safe to ignore.

***

### Step 2 — Convert the Project for XR

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-28 152845.png" alt=""><figcaption></figcaption></figure>

1. Go to **File > Build Profiles > Player Settings > XR Plugin Management** and click **Install**.
2. When prompted to choose a plugin provider, select **OpenXR**.
3. When asked to enable the **Meta XR feature set**, select **Yes**.
4. Click **Fix** on any warning messages that appear.
5. Under OpenXR settings, add the following interaction profiles:
   * Meta Quest Touch Pro
   * Meta Quest Touch Plus
6. Enable **Meta Quest Support**.
7. Remove **Quest** and **Quest 2** from the target device list.

***

### Step 3 — Configure the Scene for Passthrough

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-28 152934.png" alt=""><figcaption></figcaption></figure>

The default Convai sample scene uses a Unity camera and environment object that conflict with Meta's passthrough camera rig. Disable both before adding the MR building blocks.

1. In the hierarchy, navigate to **Convai > Camera** and uncheck the camera component in the **Inspector**.
2. Do the same for the **Environment** object under Convai.
3. Go to **Meta Quest Tools > Building Blocks**.
4. Under the **Core** filter, add **Camera Rig** and **Passthrough**.
5. Under the **Passthrough** filter, add **Passthrough Camera Access** — this is required because the vision feed must be sent to the Convai server.
6. When prompted, click **Overwrite**.

{% hint style="info" %}
If your Convai character is not visible after adding the camera rig, select it in the hierarchy and manually update the **Transform position** values until it appears correctly in the scene view.
{% endhint %}

***

### Step 4 — Enable Vision

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-28 153013.png" alt=""><figcaption></figcaption></figure>

This step connects the Meta Quest passthrough camera to the Convai character, enabling it to see and respond to the real world around the user.

1. Select **Convai Manager** in the hierarchy.
2. Change **Connection Type** to **Video**.
3. When prompted, click **Add Components** to add the **Convai Vision Publisher** and **Camera Frame Source**. These appear as child components under the Convai Manager in the hierarchy.
4. By default, the Camera Frame Source uses a Unity camera. Replace it with the **Quest Vision Frame Source**:
   * Drag the **Passthrough Camera Access** object from the hierarchy into the frame source field.
5. Click **Auto Find** inside the **Convai Vision Publisher**.
6. In the **Camera Rig**, locate the **Passthrough** and **Camera Access** toggles and ensure both are enabled.

**How it works:** The Convai Vision Publisher sends a live feed from the Quest camera to the Convai server. The character receives this feed and can describe, reason about, and respond to physical objects and spatial layout in real time.

***

### Step 5 — Set Up the Chat UI for Mixed Reality

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-28 153056.png" alt=""><figcaption></figcaption></figure>

The default Convai canvas UI is built for flat screens. In a MR scene it needs to be converted to world space and scaled down to sit naturally next to the character inside the headset.

1. Select the **canvas** in the hierarchy.
2. Change **Render Mode** to **World Space**.
3. Set the **Position** values to `0, 0, 0` so it appears in front of the player.
4. If the UI is invisible, set its **Alpha** value to `1`.
5. Change the canvas **Scale** from `1` to `0.001` — this brings it to a readable size within the headset.
6. Reposition the **Status Container**, **Recording prefab**, and **Settings prefab** to the left of the character.
7. Add a slight tilt to match the natural viewing angle inside the headset.
8. Tweak position values in the scene view until the layout looks right alongside the character.

{% hint style="info" %}
You can also use Unity canvas components and modules from the Meta SDK for a more integrated UI. The values above are a quick baseline to get the default Convai UI working inside the headset.
{% endhint %}

***

### Step 6 — Build and Deploy to Meta Quest

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-28 153230.png" alt=""><figcaption></figcaption></figure>



1. Go to **File > Build Profiles**.
2. Click **Open Scene List** and add the **Lip Sync scene**.
3. Click **Build**, select your destination folder, and hit **Save**.
4. Connect your Meta Quest device via USB.
5. The built app appears in **Unknown Sources** on the headset. Launch it from there.

{% hint style="info" %}
Add a **Directional Light** to the scene before building. Real-world lighting conditions vary significantly and a directional light helps the character look consistent across different environments
{% endhint %}

#### Testing Vision

Once inside the headset, test the vision connection by asking the character what it can see:

* _"What do you see around me?"_
* _"How many chairs are in this room?"_
* _"Can you describe what's on my desk?"_

The character will describe the physical environment in real time using the Quest passthrough camera feed.&#x20;

### Component Reference

| Component                   | Role                                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| `Convai Vision Publisher`   | Sends the camera frame feed to the Convai server for processing                            |
| `Quest Vision Frame Source` | Meta Quest-specific input that replaces the default Unity camera with the passthrough feed |
| `Passthrough Camera Access` | Meta building block that grants the app access to the Quest passthrough camera             |
| `Camera Rig`                | Meta building block that replaces the standard Unity camera for XR use                     |
