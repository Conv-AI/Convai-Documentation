---
title: Pin a character version
description: >-
  Choose a released character version in the Unity Inspector, preserve that
  selection across sessions, and resolve missing or unavailable versions.
last_reviewed: "5.0.0-pre.1"
---

Choose a released **Character Version** to keep a scene tied to a particular character release. **Live** uses the current character. This selects a character configuration version, independently of the Unity SDK package version.

## Select a released version

{% stepper %}
{% step %}
### Prepare access to released versions

Configure your Editor API key under **Convai > Settings > Credentials**, then enter the character's **Character ID** on the character component. The released versions list does not use **Character Workspace ID**.
{% endstep %}

{% step %}
### Choose the version

Select the character and open **Identity > Character Version**. Use **Refresh** to reload releases, then choose a version from the popup. The latest release is labeled **Latest release**. If the service has no releases, **Live** is the only available choice.

To reuse the pin across scenes, set the version on the character prefab.

<figure><img src="../../../.gitbook/assets/unity-character-version.png" alt="Identity settings showing the example character pinned to version 1.0 (Latest release) with a Refresh button."><figcaption><p>(1) Choose a numbered <strong>Character Version</strong> to pin the character. This capture shows <strong>1.0 (Latest release)</strong>. (2) Select <strong>Refresh</strong> to reload the available releases.</p></figcaption></figure>
{% endstep %}

{% step %}
### Save and verify the selection

Save the changed scene or prefab. Select it again and confirm the chosen release remains selected. Connect with that configuration and check for version-related connection errors before distributing the application.
{% endstep %}
{% endstepper %}

## Resolve a saved-version warning

The SDK saves the exact release reference returned by the API. Do not manufacture a reference by appending a version to the character ID.

| State | Meaning and action |
| --- | --- |
| Released versions unavailable | Check the API key, **Environment**, and, for **Custom**, the **Character API Base URL**, then Refresh. |
| No released versions yet | Publish an appropriate character release through your character-management workflow, or use Live. |
| Saved version marked unavailable | The saved reference is absent from the fetched list. It is preserved; choose an available release or Live deliberately. |
| Reselect required | The saved version has no API reference. Choose the release again from the API-backed list. |

The Inspector does not silently change an unavailable pin to Live. A preserved pin is not evidence that the service can still connect it; verify that connection separately.
