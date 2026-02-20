---
description: Install the Convai Unity SDK by importing a .unitypackage release build.
hidden: true
---

# Install via Unity Package

## Introduction

Unity Package installation is a good fallback for offline workflows, quick evaluation, or when you need a pinned version.

## Prerequisites

* A Unity project opened in the Unity Editor
* A downloaded Convai `.unitypackage` file from releases:
  * `<CONVAI_GITHUB_RELEASES_URL>`

## Step-by-step

{% stepper %}
{% step %}
### Download a release package

From the Convai GitHub Releases page, download either:

* the latest version, or
* a specific version you want to pin.
{% endstep %}

{% step %}
### Import into your Unity project

* Double-click the downloaded `.unitypackage`, **or**
* Drag and drop it into your project’s **Assets** folder area.
{% endstep %}

{% step %}
### Import everything

* In the Unity import window, ensure **all items are selected**.
* Click **Import**.
{% endstep %}

{% step %}
### Verify the installation

* After import, check **Console** for errors.
* **Expected result:** No errors in Console, and a **Convai** menu appears in the top toolbar.
{% endstep %}
{% endstepper %}

## Troubleshooting

* **Missing scripts after import**
  * Re-import the package and confirm all items are selected.
* **Console errors after install**
  * Confirm you are using a supported Unity version and render pipeline setup.

## Conclusion

You’ve installed the SDK via UnityPackage and verified the editor compiled successfully. Next, go to **Setup → Configure API Key**.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
