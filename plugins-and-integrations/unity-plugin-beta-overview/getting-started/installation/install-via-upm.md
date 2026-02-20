---
description: >-
  Install the Convai Unity SDK via the Unity Package Manager using the package
  name.
---

# Install via UPM (Recommended)

## Introduction

UPM installation is the recommended approach because it’s easy to maintain, update, and keep consistent across a team.

## Prerequisites

* A Unity project opened in the Unity Editor

## Step-by-step

{% stepper %}
{% step %}
### Open Package Manager

In Unity, go to **Window → Package Manager**.
{% endstep %}

{% step %}
### Add the package from Git URL

* Click the **+** button (top-left).
* Select **Install package by name**
* Copy the package name below and paste it into the Package Name field. Then click **Install**.
  * `com.convai.convai-sdk-for-unity`&#x20;

<figure><img src="../../../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Verify the installation

* Wait for Unity to finish importing and compiling.
* Open **Console** (if needed): **Ctrl + Shift + C** (Windows) / **Cmd + Shift + C** (macOS)
* **Expected result:** No errors in Console, and a **Convai** menu appears in the top toolbar.
{% endstep %}
{% endstepper %}

## Troubleshooting

* **Console errors after install**
  * Confirm you are using a supported Unity version.

## Conclusion

You’ve installed the Convai Unity SDK via UPM and confirmed the editor compiled successfully. Next, go to **Setup → Configure API Key**.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
