---
title: Long-term memory quick start
description: Enable Long-Term Memory for a Convai character and verify cross-session recall in the Unity Editor in three steps.
last_reviewed: "4.2.0"
---

Long-term memory works automatically once two conditions are met: memory is enabled for your character on the Convai dashboard, and the SDK is sending a stable user identifier. This guide walks through both conditions and shows you how to confirm they are working.

## Prerequisites

Before you begin:

- A Convai account with at least one character created at [convai.com](<code class="expression">space.vars.dashboard_url</code>)
- The Convai Unity SDK installed and configured with a valid API key
- A scene with `ConvaiManager` and `ConvaiCharacter` components configured
- The character's ID set in the `ConvaiCharacter` Inspector

You do not need to write any code for the default LTM experience. The SDK's `DeviceEndUserIdProvider` generates a stable identifier automatically. See [End-user identity](end-user-identity.md) if you have an authentication system and need to supply your own user IDs.

***

## Enable memory for a character

{% stepper %}
{% step %}
### Enable memory on the dashboard

1. Sign in to [convai.com](<code class="expression">space.vars.dashboard_url</code>) and open the character you want to use.
2. Select the **Memory** tab in the character's settings sidebar.
3. Toggle **Long-Term Memory** to **On**.
4. Save the character.

{% hint style="warning" %}
This setting applies globally to the character. Every application, SDK version, and deployment that connects to this character ID will send and receive memories. Coordinate with your team before enabling on a shared character.
{% endhint %}
{% endstep %}

{% step %}
### Start a conversation in Play Mode

Run your scene in the Unity Editor. Start a conversation with the character and share information the character should remember — for example:

> "My name is Jordan and I'm a safety officer on the night shift."

Let the conversation complete naturally, then **stop Play Mode**. The session end triggers Convai to extract and store the facts you shared.
{% endstep %}

{% step %}
### Re-enter Play Mode and verify recall

Enter Play Mode again and ask the character to reference what it learned:

> "Do you remember who I am?"

The character should acknowledge your name and role without you repeating them.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
If the character references details from the previous session, long-term memory is working correctly.
{% endhint %}

***

## How identity works in the editor

The SDK's default `DeviceEndUserIdProvider` handles identity automatically. In Play Mode, it reads or creates a persistent GUID stored in `PlayerPrefs` under the key `"convai.end_user_id"`. Every Play Mode session on the same machine uses the same GUID, so memories accumulate across sessions exactly as they would for a real user. When you stop Play Mode, Convai processes the conversation and extracts facts as `MemoryRecord` entries. On the next session, those records are injected into the character's context before it generates its first response.

The GUID persists as long as `PlayerPrefs` is not cleared. Clearing `PlayerPrefs` or reinstalling the application generates a new GUID, which the server treats as a new user — no memories carry over. See [End-user identity](end-user-identity.md) for strategies that survive reinstalls.

***

## Identity in player builds

In a player build, `DeviceEndUserIdProvider` first tries `SystemInfo.deviceUniqueIdentifier`. If that value is unavailable or invalid, it falls back to the same `PlayerPrefs` GUID approach used in the editor.

| Context | Identity source |
|---|---|
| Unity Editor | `PlayerPrefs` GUID — stable per project |
| Player build (device ID available) | `SystemInfo.deviceUniqueIdentifier` |
| Player build (device ID unavailable) | `PlayerPrefs` GUID — stable until reinstall |

For applications where users log in with accounts, replace `DeviceEndUserIdProvider` with a custom provider that returns your account IDs. Device-based IDs will not follow a user who switches devices. See [End-user identity](end-user-identity.md) for implementation details.

***

## Next steps

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="configure-memory-for-a-character.md" %}
[Configure memory for a character](configure-memory-for-a-character.md)
{% endcontent-ref %}

{% content-ref url="how-long-term-memory-works.md" %}
[How long-term memory works](how-long-term-memory-works.md)
{% endcontent-ref %}
