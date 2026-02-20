---
description: Install the Convai Unity SDK from the Unity Asset Store.
hidden: true
---

# Install via Unity Asset Store

## \*

Asset Store installation is ideal if your team prefers Unity’s store distribution and the standard “My Assets” workflow.

## Prerequisites

* A Unity ID signed in to the Asset Store
* Convai package added to your account:
  * `<CONVAI_ASSET_STORE_URL>`&#x20;

## Step-by-step

{% stepper %}
{% step %}
### Add the package to your Unity account

* Open the Convai Asset Store page.
* Click **Add to My Assets**.
* If prompted, sign in to your Unity account.
* **Expected result:** The asset is added to your “My Assets”.
{% endstep %}

{% step %}
### Open Package Manager

In Unity, go to **Window → Package Manager**.
{% endstep %}

{% step %}
### Download & Import (two options)

**Option A — “Open in Unity”**

* If available on the Asset Store page, click **Open in Unity**.
* Unity opens Package Manager to the asset page.

**Option B — via “My Assets”**

* In Package Manager, open **My Assets**.
* Search for **Convai**, select it.
{% endstep %}

{% step %}
### Download then Import

* Click **Download**.
* When finished, click **Import**.
{% endstep %}

{% step %}
### Verify the installation

* Check **Console** for errors.
* **Expected result:** No errors in Console, and a **Convai** menu appears in the top toolbar.
{% endstep %}
{% endstepper %}

## Troubleshooting

* **Convai doesn’t appear in My Assets**
  * Confirm you’re logged into the correct Unity account.
  * Confirm the asset was added to “My Assets” on the store page.
* **Import completes but Convai menu is missing**
  * Restart Unity and re-check Console for errors.

## Conclusion

You’ve installed the SDK through the Asset Store and confirmed the editor compiled successfully. Next, go to **Setup → Configure API Key**.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
