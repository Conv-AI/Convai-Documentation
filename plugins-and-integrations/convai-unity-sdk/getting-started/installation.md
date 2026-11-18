---
title: Install the Convai Unity SDK
description: >-
  Install the Convai Unity SDK into a Unity project using Package Manager or
  Asset Store so the SDK and its dependencies resolve correctly.
last_reviewed: "5.0.0-pre.1"
---

Install the Convai SDK for Unity <code class="expression">space.vars.unity_sdk_version</code> in Unity <code class="expression">space.vars.unity_min_version</code>. Choose the source that supplies this exact preview. If you received a package file from Convai, you can install it directly.

{% tabs %}
{% tab title="Package file (.tgz)" %}
Open **Window > Package Manager**. Select **+ > Install package from tarball**, then choose the supplied `.tgz` file. Wait for Unity to resolve the package and its dependencies. In **In Project**, select **Convai SDK for Unity** and confirm its installed version matches <code class="expression">space.vars.unity_sdk_version</code>. [Unity's tarball installation guide](https://docs.unity3d.com/6000.0/Documentation/Manual/upm-ui-tarball.html)
{% endtab %}

{% tab title="Package registry" %}
Use this route if the registry configured for your project provides the preview.

{% stepper %}
{% step %}
### Open Package Manager

In Unity, open **Window > Package Manager** and select **+ > Install package by name**.
{% endstep %}

{% step %}
### Enter the package name and version

Enter `com.convai.convai-sdk-for-unity` in **Name**. Enter <code class="expression">space.vars.unity_sdk_version</code> in **Version** and select **Install**. Specifying the version selects the preview even if a different release is available. [Unity's package installation guide](https://docs.unity3d.com/6000.0/Documentation/Manual/upm-ui-quick.html)
{% endstep %}

{% step %}
### Confirm the installed version

Select **Convai SDK for Unity** under **In Project**. If the registry cannot resolve this version, check the registry settings supplied with your preview or use the supplied package file.
{% endstep %}
{% endstepper %}
{% endtab %}

{% tab title="Asset Store" %}
Use this route only if your Asset Store library lists this SDK version. In **Window > Package Manager**, open **My Assets**, select the Convai package, and follow the install or import action for that listing. Confirm the version before importing it into your project.
{% endtab %}
{% endtabs %}

## Package dependencies

The SDK package declares these seven dependencies. If Package Manager reports a conflict, compare your project's `Packages/manifest.json` with these versions and resolve the conflicting requirement.

| Package                           | Version |
| --------------------------------- | ------- |
| `com.unity.ai.inference`          | <code class="expression">space.vars.dep_ai_inference_version</code> |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> |
| `com.unity.ugui`                  | <code class="expression">space.vars.dep_ugui_version</code> |
| `com.unity.inputsystem`           | <code class="expression">space.vars.dep_inputsystem_version</code> |
| `com.unity.collections` | <code class="expression">space.vars.dep_collections_version</code> |
| `com.unity.modules.ai` | <code class="expression">space.vars.dep_modules_ai_version</code> |
| `com.unity.modules.xr` | <code class="expression">space.vars.dep_modules_xr_version</code> |

## Next steps

With the SDK installed, connect your project to Convai by entering your API key.

{% content-ref url="configure-api-key.md" %}
[Configure the API key](configure-api-key.md)
{% endcontent-ref %}
