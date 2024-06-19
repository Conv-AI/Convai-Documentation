---
description: Building for VR - Unity Plugin Guide for VR development with Convai.
---

# Building for VR

## VR Installation

If you want to make your Convai Plugin compatible with VR, you can do so using the automatic or manual process. Please see the instructions below or check out our [_latest tutorial video_](https://www.youtube.com/watch?v=Q0TUT5vtEyg) on YouTube.

{% embed url="https://www.youtube.com/watch?v=Q0TUT5vtEyg" %}
Unleash the Power of Convai AI NPCs in Your Unity VR Game
{% endembed %}

### Method 1 : Automatic Setup

{% hint style="success" %}
Recommended for new projects.
{% endhint %}

{% hint style="danger" %}
The following processes will be performed:

* Universal Render Pipeline (URP)
* OpenXR Plugin
* XR Interaction Toolkit
* Convai Custom VR Package
* Convai URP Converter

**If these packages are not present, they will be installed.**
{% endhint %}

{% hint style="danger" %}
**If the target build platform is not Android, it will be switched to **_**Android.**_
{% endhint %}

1. Click on " _Convai / Convai Custom Package Installer / Install VR Package_ "

<figure><img src="../../../.gitbook/assets/ConvaiCustomPackageInstaller (2).png" alt=""><figcaption></figcaption></figure>

2. Confirm the changes and processes to be made. If you agree, the process will start.                     Click " **Yes, Proceed** " and the process will begin. You'll see logs in the console.

<figure><img src="../../../.gitbook/assets/ConvaiCustomPackageInstallerConfirmWindow.png" alt=""><figcaption></figcaption></figure>

3. If you encounter an error like " Failed to Resolve Packages " don't worry. The process will continue and the error will be resolved automatically after the package installations are complete.

<figure><img src="../../../.gitbook/assets/VRLogs.png" alt=""><figcaption></figcaption></figure>

4. Open the " _Convai / Scenes / Convai Demo - VR_ " demo scene. If the TMP Importer window appears, click " **Import TMP Essentials** " to install TextMeshPro for UI text objects.

<figure><img src="../../../.gitbook/assets/AutomaticallyImportTMPEssentials.png" alt=""><figcaption></figcaption></figure>

Alternatively, you can use the " _Window / TextMeshPro / Import TMP Essential Resources_ " to install it.

<figure><img src="../../../.gitbook/assets/ManualImportTMPEssentialsResources.png" alt=""><figcaption></figcaption></figure>

5. Build your project by going to " _File /Build Settings / Build_ " Ensure that the " **Convai Demo - VR** " scene is included in the Scenes in Build section.

Now everything is ready for testing. 🙂✅

{% hint style="warning" %}
Ensure you've set up your API Key. ( Convai / Convai Setup )
{% endhint %}

### Method 2 : Manual Setup&#x20;

{% hint style="danger" %}
Ensure you have the following packages installed in your project:

* OpenXR or Oculus XR
* XR Interaction Toolkit
* URP (Universal Render Pipeline)
{% endhint %}

1. Double-click on " _Convai / Convai Custom Unity Packages / ConvaiVRUpgrader.unitypackage_ "

<figure><img src="../../../.gitbook/assets/ConvaiVRUpgrader.png" alt=""><figcaption></figcaption></figure>

2. You'll see a warning that the settings will overwrite your project settings. You can either allow it by clicking " **Import** " or create a temporary project by clicking " **Switch Project** "

<figure><img src="../../../.gitbook/assets/VRUpgraderWarning (1).png" alt=""><figcaption></figcaption></figure>

3. In the Import Unity Package window, review the assets to be imported and click " **Next** "

<figure><img src="../../../.gitbook/assets/ConvaiVRUpgraderimport_1.png" alt=""><figcaption></figcaption></figure>

4. In this window, select the project settings you want to import and complete the installation by clicking " **Import** ".

<figure><img src="../../../.gitbook/assets/ConvaiVRUpgraderimport_2.png" alt=""><figcaption></figcaption></figure>

5. Open the " _Convai / Scenes/ Convai Demo - VR_ " demo scene. If the TMP Importer window appears, click " **Import TMP Essentials** " to install TextMeshPro for UI text objects.

<figure><img src="../../../.gitbook/assets/AutomaticallyImportTMPEssentials.png" alt=""><figcaption></figcaption></figure>

6. If you see 3D objects in pink, it's a shader issue. If you're using URP, convert the materials to URP by double-clicking on " _Convai / Convai Custom Unity Packages / ConvaiURPConverter_ " and importing all assets in the window that appears.

<figure><img src="../../../.gitbook/assets/ConvaiURPConverter.png" alt=""><figcaption></figcaption></figure>

7. Build your project by going to " _File / Build Settings / Build_ " Ensure that the " **Convai Demo - VR** " scene is included in the Scenes in **Build** section.

<figure><img src="../../../.gitbook/assets/VRBuildSettings.png" alt=""><figcaption></figcaption></figure>

Now everything is ready for testing. 🙂✅

{% hint style="warning" %}
Ensure you've set up your API Key (Convai/Convai Setup).
{% endhint %}



### Convai Default VR Controller Scheme

<figure><img src="../../../.gitbook/assets/ConvaiDefaultVRControllerScheme.png" alt=""><figcaption></figcaption></figure>
