---
title: Long-term memory quick start
last_reviewed: "4.5.0"
description: Enable long-term memory for a Convai character in three steps and verify that recall survives across separate sessions in the Unity Editor.
---

This guide configures the two Unity-side prerequisites for long-term memory: the character setting and a stable user identifier. It then uses two live sessions to validate the backend result.

**Validation boundary:** Extraction and recall are backend behavior, not guaranteed by the Unity 4.5 client source. Treat the final step as a live staging test and record the character ID, end-user ID, and session timestamps if the result differs.

## Prerequisites

Before starting, verify:

* [ ] A `ConvaiCharacter` is in the scene with its Character ID set in the Inspector
* [ ] Long-term memory is enabled for your character on the [Convai dashboard](https://convai.com)

You do not need to write any code for the default LTM experience. The SDK's `DeviceEndUserIdProvider` generates a stable identifier automatically. See [End-user identity](end-user-identity.md) if you have an authentication system and need to supply your own user IDs.

***

## Enable memory for a character

{% stepper %}
{% step %}
### Enable memory on the dashboard

1. Sign in to [convai.com](https://convai.com) and open the character you want to use.
2. Select the **Memory** tab in the character's settings sidebar.
3. Toggle **Long-Term Memory** to **On**.
4. Save the character.

{% hint style="warning" %}
The request is keyed by character ID, not by Unity scene. Coordinate before changing a shared character and confirm the effective backend scope in staging.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/image (470).png" alt="Long-Term Memory toggle enabled in the Convai dashboard"><figcaption><p>Long-Term Memory toggle enabled in the Convai dashboard.</p></figcaption></figure>
{% endstep %}

{% step %}
### Start a conversation in Play Mode

Run your scene in the Unity Editor. Start a conversation with the character and share information the character should remember — for example:

> "My name is Jordan and I'm a safety officer on the night shift."

Let the conversation complete naturally, then **stop Play Mode**. This ends the client session. Backend extraction eligibility and completion timing require live verification; wait for your normal processing window before the next check.
{% endstep %}

{% step %}
### Re-enter Play Mode and verify recall

Enter Play Mode again and ask the character to reference what it learned:

> "Do you remember who I am?"

Check whether the character acknowledges your name and role without you repeating them. If it does not, use the diagnostics page to query records and confirm identity stability.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
If the character references details from the previous session, long-term memory is working correctly.
{% endhint %}

***

## How identity works in the editor

The SDK's default `DeviceEndUserIdProvider` handles identity automatically. In the Editor, it reads or creates a persistent GUID stored in `PlayerPrefs` under the key `"convai.end_user_id"`. Play Mode sessions in that project/editor environment reuse the GUID until the preference is cleared. Whether a completed conversation produces records and when those records are recalled must be confirmed against the live backend.

The GUID persists as long as `PlayerPrefs` is not cleared. Clearing the preference generates a new GUID. Test how your backend handles old and new IDs; use an account-backed provider when continuity across reinstalls is required.

***

## Identity in player builds

In a player build, `DeviceEndUserIdProvider` first tries `SystemInfo.deviceUniqueIdentifier`. If that value is unavailable or invalid, it falls back to the same `PlayerPrefs` GUID approach used in the editor.

| Context                              | Identity source                             |
| ------------------------------------ | ------------------------------------------- |
| Unity Editor                         | `PlayerPrefs` GUID — stable per project     |
| Player build (device ID available)   | `SystemInfo.deviceUniqueIdentifier`         |
| Player build (device ID unavailable) | `PlayerPrefs` GUID — stable until reinstall |

For applications where users log in with accounts, replace `DeviceEndUserIdProvider` with a custom provider that returns your account IDs. Device-based IDs will not follow a user who switches devices. See [End-user identity](end-user-identity.md) for implementation details.

***

## Next steps

{% content-ref url="end-user-identity.md" %}
[end-user-identity.md](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="configure-memory-for-a-character.md" %}
[configure-memory-for-a-character.md](configure-memory-for-a-character.md)
{% endcontent-ref %}

{% content-ref url="how-long-term-memory-works.md" %}
[how-long-term-memory-works.md](how-long-term-memory-works.md)
{% endcontent-ref %}
