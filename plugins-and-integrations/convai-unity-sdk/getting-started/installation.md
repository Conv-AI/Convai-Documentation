---
title: Install the Convai Unity SDK
description: >-
  Install the Convai Unity SDK into a Unity project using Package Manager or
  Asset Store so the SDK and its dependencies resolve correctly.
last_reviewed: "4.5.0"
---

The Convai Unity SDK is available through two channels. Use **Package Manager** for new projects or when you prefer not to manage Asset Store downloads — the package resolves directly from the Convai registry with no manual download. Use **Asset Store** if your project already sources packages from your Asset Store library or if your studio manages package versions through My Assets.

Both methods require Unity <code class="expression">space.vars.unity_min_version</code> and install SDK version **<code class="expression">space.vars.unity_sdk_version</code>** and the same six required dependencies.

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

Unity contacts the registry, resolves the package, and begins downloading. Six dependencies install automatically:

| Package                           | Version |
| --------------------------------- | ------- |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> |
| `com.unity.ugui`                  | <code class="expression">space.vars.dep_ugui_version</code> |
| `com.unity.inputsystem`           | <code class="expression">space.vars.dep_inputsystem_version</code> |
| `com.unity.ai.navigation`         | <code class="expression">space.vars.dep_ai_navigation_version</code> |
| `com.unity.collections`           | <code class="expression">space.vars.dep_collections_version</code> |
| `com.unity.modules.xr`            | <code class="expression">space.vars.dep_modules_xr_version</code> |

Wait for the progress bar in the bottom-right of the Unity Editor to complete before continuing.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Dependency conflict:** If your project already pins any of these six packages to an older version in `Packages/manifest.json`, the install will fail or produce a version mismatch. Open `Packages/manifest.json`, remove or update the conflicting version entries, then retry.
{% endhint %}

{% hint style="success" %}
**Installation complete** when the Convai SDK for Unity entry appears in the Package Manager list with a green checkmark and version <code class="expression">space.vars.unity_sdk_version</code>. You will also see a new **Convai** menu item in the Unity menu bar.
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

Unity imports the package and installs six dependencies automatically:

| Package                           | Version |
| --------------------------------- | ------- |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> |
| `com.unity.ugui`                  | <code class="expression">space.vars.dep_ugui_version</code> |
| `com.unity.inputsystem`           | <code class="expression">space.vars.dep_inputsystem_version</code> |
| `com.unity.ai.navigation`         | <code class="expression">space.vars.dep_ai_navigation_version</code> |
| `com.unity.collections`           | <code class="expression">space.vars.dep_collections_version</code> |
| `com.unity.modules.xr`            | <code class="expression">space.vars.dep_modules_xr_version</code> |

Wait for the progress bar in the bottom-right of the Unity Editor to complete before continuing.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
To update the SDK to a newer version, return to **My Assets** in the Package Manager, select the SDK, and click **Update**.
{% endhint %}

{% hint style="success" %}
**Installation complete** when the Convai SDK for Unity entry appears in the Package Manager list with version <code class="expression">space.vars.unity_sdk_version</code>. You will also see a new **Convai** menu item in the Unity menu bar.
{% endhint %}
{% endtab %}
{% endtabs %}

## Next steps

With the SDK installed, connect your project to Convai by entering your API key.

{% content-ref url="configure-api-key.md" %}
[Configure the API key](configure-api-key.md)
{% endcontent-ref %}
