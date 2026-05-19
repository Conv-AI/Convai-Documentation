# install via upm

The Unity Package Manager (UPM) is the fastest way to install the Convai SDK for Unity. No download required — Unity fetches and installs the package and its dependencies automatically.

## Prerequisites

* Unity 2023.1 or later
* An active internet connection

## Install the Package

{% stepper %}
{% step %}
**Open the Package Manager**

In the Unity Editor, open **Window > Package Manager**.
{% endstep %}

{% step %}
**Add Package by Name**

Click the **+** button in the top-left corner and select **Add package by name**.
{% endstep %}

{% step %}
**Enter the Package ID**

Enter the package name and click **Add**:

```
com.convai.convai-sdk-for-unity
```

Unity resolves and installs the package along with its required dependencies:

* `com.unity.nuget.newtonsoft-json` 3.2.2
* `com.unity.ugui` 2.0.0
* `com.unity.inputsystem` 1.18.0

**Convai SDK for Unity** appears in the Package Manager list with a checkmark. The version is shown in the detail panel on the right.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
If Unity shows a dependency conflict with `com.unity.inputsystem` or `com.unity.ugui`, check that your project does not pin an older version of these packages in `Packages/manifest.json`. Remove any version pins that conflict and let UPM resolve them.
{% endhint %}

## Next Steps

With the SDK installed, connect your project to Convai by adding your API key.

{% content-ref url="/broken/pages/3938fef30c28921cf6d473bc3830fc1eccdf1573" %}
[Broken link](/broken/pages/3938fef30c28921cf6d473bc3830fc1eccdf1573)
{% endcontent-ref %}
