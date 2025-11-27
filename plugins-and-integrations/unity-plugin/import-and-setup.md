---
description: Follow these steps to import and configure the Unity SDK.
hidden: true
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/import-and-setup
---

# Import and Setup (nightly)

{% hint style="info" %}
[**Download the nightly version Unity Package from this link.** ](https://github.com/Conv-AI/Convai-Unity-Nightly-SDK/releases/latest)\
The package contains sample scenes to get started.
{% endhint %}

{% hint style="info" %}
[Download the WebGL version of the plugin, if you want to build for WebGL.](building-for-supported-platforms/building-for-webgl.md)
{% endhint %}

{% hint style="info" %}
The file structure belongs to the nightly version of the plugin downloaded from the documentation.
{% endhint %}

1. If you haven't already done so, download the SDK [here](https://drive.google.com/file/d/1dslrRcI6e02LvL-coupUoTFRlBDLjvMA).
2. Start the Unity Hub.
3. Verify that your project uses Unity 2022.3.0f1 LTS or later (check the Pre-Requisites section of the documentation).
4. Open your project.
5.  &#x20;Select **Assets > Import Package > Custom Package.**<br>

    <figure><img src="../../.gitbook/assets/image (200).png" alt="" width="375"><figcaption></figcaption></figure>
6. In the file explorer, select the Convai Unity package. \
   The filename is similar to `ConvaiforUnity_vX.Y.Z.unitypackage`. X, Y, and Z are numbers containing the version information of the plugin.
7. Click **Import.**&#x20;
8.  When the Import begins, a prompt for using the new Unity Input System will appear. Press **Yes**.<br>

    <figure><img src="../../.gitbook/assets/image (102).png" alt="" width="295"><figcaption></figcaption></figure>
9. The project will automatically restart. After the project is restarted, you need to import the package in the same way.
10. If you are using a Unity Version pre-2022.3.0f1, Disable Assembly Version Validation (use this troubleshooting page: [enabled-assembly-validation.md](troubleshooting-guide/enabled-assembly-validation.md "mention"))
11. Verify there were no compiler errors.&#x20;

{% hint style="info" %}
If you face any errors, visit our [troubleshooting-guide](troubleshooting-guide/ "mention") page to resolve our most common issues.
{% endhint %}

## Package contents

After importing, by default, the Convai folder will be in your project. It should look something like this.

{% hint style="info" %}
The file structure belongs to the Core version of the plugin downloaded from the documentation.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (506).png" alt=""><figcaption></figcaption></figure>
