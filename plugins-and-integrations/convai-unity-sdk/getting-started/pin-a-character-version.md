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

Configure your Editor API key under **Convai > Settings > Credentials**. Set **Character Workspace ID** if the character belongs to a specific workspace, then enter its **Character ID** on the character component.
{% endstep %}

{% step %}
### Choose the version

Select the character and open **Identity > Character Version**. Use **Refresh** to reload releases, then choose a version from the popup. The latest release is labeled **Latest release**. If the service has no releases, **Live** is the only available choice.

To reuse the pin across scenes, set the version on the character prefab.
{% endstep %}

{% step %}
### Save and verify the selection

Save the changed scene or prefab. Select it again and confirm the chosen release remains selected. Connect with that configuration and check for version-related connection errors before distributing the application.
{% endstep %}
{% endstepper %}

<figure><img src="../../../.gitbook/assets/unity-character-version.png" alt="Identity card of the ConvaiCharacter Inspector with Character Version set to the released version 1.0 (Latest release) next to Refresh, with the Character ID blurred"><figcaption><p>A character pinned to its released version 1.0. The drop-down also lists Live and every release the API returns.</p></figcaption></figure>

## Resolve a saved-version warning

The SDK saves the exact release reference returned by the API. Do not manufacture a reference by appending a version to the character ID.

| State | Meaning and action |
| --- | --- |
| Released versions unavailable | Check credentials, workspace, environment, and the Character API URL, then Refresh. |
| No released versions yet | Publish an appropriate character release through your character-management workflow, or use Live. |
| Saved version marked unavailable | The saved reference is absent from the fetched list. It is preserved; choose an available release or Live deliberately. |
| Reselect required | The saved version has no API reference. Choose the release again from the API-backed list. |

The Inspector does not silently change an unavailable pin to Live. A preserved pin is not evidence that the service can still connect it; verify that connection separately.
