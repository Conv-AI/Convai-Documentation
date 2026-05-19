# install via asset store

The Convai SDK for Unity is available on the Unity Asset Store. Once you add it to your account, Unity manages it through the Package Manager — updates and dependency resolution work the same as with any UPM package.

## Prerequisites

* Unity 2023.1 or later
* A Unity ID (required to access the Asset Store)

## Install the Package

{% stepper %}
{% step %}
**Add to Your Asset Store Account**

Open the Convai SDK for Unity listing on the [Unity Asset Store](https://assetstore.unity.com/) and click **Add to My Assets**. Sign in with your Unity ID if prompted.

The asset is added to your account. You should see the button change to **Open in Unity**.
{% endstep %}

{% step %}
**Open the Package Manager**

In the Unity Editor, open **Window > Package Manager**.
{% endstep %}

{% step %}
**Switch to My Assets**

In the top-left dropdown, switch the package source to **My Assets**.

The list refreshes to show packages in your Asset Store account.
{% endstep %}

{% step %}
**Download and Import**

Locate **Convai SDK for Unity** in the list, click **Download**, then click **Import**.

Unity imports the package and installs all required dependencies:

* `com.unity.nuget.newtonsoft-json` 3.2.2
* `com.unity.ugui` 2.0.0
* `com.unity.inputsystem` 1.18.0

**Convai SDK for Unity** appears under **In Project** in the Package Manager.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
Update the package from the same **My Assets** view whenever a new version is published to the Asset Store.
{% endhint %}

## Next Steps

With the SDK installed, connect your project to Convai by adding your API key.

{% content-ref url="/broken/pages/3938fef30c28921cf6d473bc3830fc1eccdf1573" %}
[Broken link](/broken/pages/3938fef30c28921cf6d473bc3830fc1eccdf1573)
{% endcontent-ref %}
