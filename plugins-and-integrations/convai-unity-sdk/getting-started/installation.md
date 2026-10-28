---
title: Install the Convai Unity SDK
description: >-
  Install the Convai Unity SDK into a Unity project using Package Manager or
  Asset Store so the SDK and its dependencies resolve correctly.
last_reviewed: "5.0.0-preview"
---

These instructions describe the SDK <code class="expression">space.vars.unity_sdk_version</code> preview. Use the release package supplied for your preview, and confirm public channel availability before following either installation path.

Use **Package Manager** when the intended package version is available in a registry already configured for your project, or install the preview package supplied by the release owner. Use **Asset Store** only after that version is listed in your library. This source snapshot does not establish that the 5.0 preview is available on either public channel.

Both methods require Unity <code class="expression">space.vars.unity_min_version</code> and use the dependencies declared by the installed package. Confirm the version shown by each channel before installing; a Package Manager release and an Asset Store release can become available at different times.

{% tabs %}
{% tab title="Package Manager" %}
{% stepper %}
{% step %}
### Open Package Manager

In the Unity Editor menu bar, select **Window > Package Manager**.

The Package Manager window opens. Confirm you are connected to the internet before proceeding.
{% endstep %}

{% step %}
### Add package by name

Click the **+** button in the top-left corner of the Package Manager window. Select **Add package by name** from the dropdown.

A text field appears prompting for the package name.
{% endstep %}

{% step %}
### Enter the package name

Type or paste the following identifier into the Name field, then click **Add**:

```text
com.convai.convai-sdk-for-unity
```

If your configured registry contains the requested version, Unity resolves and downloads it. Otherwise use the package source or registry configuration supplied with that release. Seven dependencies install automatically:

| Package                           | Version |
| --------------------------------- | ------- |
| `com.unity.ai.inference`          | <code class="expression">space.vars.dep_ai_inference_version</code> |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> |
| `com.unity.ugui`                  | <code class="expression">space.vars.dep_ugui_version</code> |
| `com.unity.inputsystem`           | <code class="expression">space.vars.dep_inputsystem_version</code> |
| `com.unity.collections` | <code class="expression">space.vars.dep_collections_version</code> |
| `com.unity.modules.ai` | <code class="expression">space.vars.dep_modules_ai_version</code> |
| `com.unity.modules.xr` | <code class="expression">space.vars.dep_modules_xr_version</code> |

Wait for the progress bar in the bottom-right of the Unity Editor to complete before continuing.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Dependency conflict:** If your project already pins any of these packages to an older version in `Packages/manifest.json`, the install will fail or produce a version mismatch. Open `Packages/manifest.json`, remove or update the conflicting version entries, then retry.
{% endhint %}

{% hint style="success" %}
**Installation complete** when the Convai SDK for Unity entry appears in the Package Manager list with the expected installed version. You will also see a new **Convai** menu item in the Unity menu bar.
{% endhint %}
{% endtab %}

{% tab title="Asset Store" %}
{% stepper %}
{% step %}
### Add the SDK to your Asset Store account

Open the [Unity Asset Store](https://assetstore.unity.com/) in your browser. Search for **Convai SDK for Unity** and open the listing. Click **Add to My Assets**, signing in with your Unity ID if prompted.

The button changes to **Open in Unity** when the asset has been added to your account.
{% endstep %}

{% step %}
### Open Package Manager

In the Unity Editor menu bar, select **Window > Package Manager**.
{% endstep %}

{% step %}
### Switch to My Assets

In the Package Manager window, click the packages source dropdown in the top-left (it shows **Packages: In Project** or similar) and select **My Assets**.

Your Asset Store library loads. Locate **Convai SDK for Unity** in the list.
{% endstep %}

{% step %}
### Download and import

Select **Convai SDK for Unity** in the list. Click **Download**, then click **Import** once the download completes.

Unity imports the package and installs seven dependencies automatically:

| Package                           | Version |
| --------------------------------- | ------- |
| `com.unity.ai.inference`          | <code class="expression">space.vars.dep_ai_inference_version</code> |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> |
| `com.unity.ugui`                  | <code class="expression">space.vars.dep_ugui_version</code> |
| `com.unity.inputsystem`           | <code class="expression">space.vars.dep_inputsystem_version</code> |
| `com.unity.collections` | <code class="expression">space.vars.dep_collections_version</code> |
| `com.unity.modules.ai` | <code class="expression">space.vars.dep_modules_ai_version</code> |
| `com.unity.modules.xr` | <code class="expression">space.vars.dep_modules_xr_version</code> |

Wait for the progress bar in the bottom-right of the Unity Editor to complete before continuing.
{% endstep %}
{% endstepper %}

To update the SDK to a newer version later, return to **My Assets** in the Package Manager, select the SDK, and click **Update**.

Installation is complete when the Convai SDK for Unity entry appears in the Package Manager list with the expected installed version. You will also see a new **Convai** menu item in the Unity menu bar.
{% endtab %}
{% endtabs %}

## Next steps

With the SDK installed, connect your project to Convai by entering your API key.

{% content-ref url="configure-api-key.md" %}
[Configure the API key](configure-api-key.md)
{% endcontent-ref %}
