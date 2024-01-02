---
description: >-
  Follow these steps to import and configure the nightly version of the Unity
  SDK.
---

# Import and Setup (nightly)

{% hint style="info" %}
[**Download the nightly version Unity Package from this link.** ](https://drive.google.com/file/d/1dslrRcI6e02LvL-coupUoTFRlBDLjvMA/view)\
The package contains sample scenes to get started.
{% endhint %}

{% hint style="info" %}
Download the WebGL version of the plugin, if you want to build for WebGL.
{% endhint %}

{% hint style="info" %}
The file structure belongs to the nightly version of the plugin downloaded from the documentation.
{% endhint %}

1. If you haven't already done so, download the SDK [here](https://convai.com/download/UnityPlugin).
2. Start the Unity Hub.
3. Verify that your project uses Unity 2022.3.0f1 LTS or later (check the Pre-Requisites section of the documentation).
4. Open your project.
5. &#x20;Select **Assets > Import Package > Custom Package.**\
   ![](<../../.gitbook/assets/image (68).png>)
6. In the file explorer, select the Convai Unity package. \
   The filename is similar to `ConvaiforUnity_vX.Y.Z.unitypackage`. X, Y, and Z are numbers containing the version information of the plugin.
7. Click **Import.** Wait for the import to complete.
8. If you are using a Unity Version pre-2022.3.0f1, Disable Assembly Version Validation (use this troubleshooting page: [enabled-assembly-validation.md](troubleshooting-guide/enabled-assembly-validation.md "mention"))
9. Verify there were no compiler errors.&#x20;

{% hint style="info" %}
If you face any errors, visit our [troubleshooting-guide](troubleshooting-guide/ "mention") page to resolve our most common issues.
{% endhint %}

## Package contents

After importing, by default, the Convai folder will be in your project. It should look something like this.

{% hint style="info" %}
The file structure belongs to the Core version of the plugin downloaded from the documentation.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (289).png" alt=""><figcaption></figcaption></figure>

Open the Convai Streaming Demo scene in the Scenes folder you'll see a Scene setup with Convai Tools and a Default character (named Ellen) with whom you can converse. This will not work right now, since you have not added the API key yet. Continue to see how you can talk to this character and set up your own character.
