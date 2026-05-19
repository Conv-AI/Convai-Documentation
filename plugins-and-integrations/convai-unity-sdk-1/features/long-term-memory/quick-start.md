---
description: >-
  Enable Long-Term Memory for a Convai character and verify cross-session recall
  in the Unity Editor in three steps.
---

# Quick Start

## Enable Cross-Session Memory in Three Steps

Long-Term Memory works automatically once two conditions are met: memory is enabled for your character on the Convai dashboard, and the SDK is sending a stable user identifier. This guide walks through both conditions and shows you how to confirm they are working.

## Prerequisites

Before you begin:

* Convai account with at least one character created at [convai.com](https://convai.com/)
* Convai Unity SDK installed and configured with a valid API key
* A scene with `ConvaiManager` and `ConvaiCharacter` components configured
* The character's ID set in the `ConvaiCharacter` Inspector

{% hint style="info" %}
You do not need to write any code for the default LTM experience. The SDK's `DeviceEndUserIdProvider` generates a stable identifier automatically. See [End-User Identity](/broken/pages/8dbe2add478ce0c30fa84a1a2a3fa773a8e349fc) if you have an authentication system and need to supply your own user IDs.
{% endhint %}

***

## Setup

{% stepper %}
{% step %}
**Enable Memory on the Convai Dashboard**

1. Sign in to [convai.com](https://convai.com/) and open the character you want to use.
2. Select the **Memory** tab in the character's settings sidebar.
3. Toggle **Long-Term Memory** to **On**.
4. Save the character.

{% hint style="warning" %}
This setting applies globally to the character. Every application, SDK version, and deployment that connects to this character ID will send and receive memories. Coordinate with your team before enabling on a shared character.
{% endhint %}
{% endstep %}

{% step %}
**Enter Play Mode and Have a Conversation**

Run your scene in the Unity Editor. Start a conversation with the character and share information the character should remember — for example:

> "My name is Jordan and I'm a safety officer on the night shift."

Let the conversation complete naturally, then **stop Play Mode**. The session end triggers Convai to extract and store the facts you shared.
{% endstep %}

{% step %}
**Re-Enter Play Mode and Verify Recall**

Enter Play Mode again and ask the character to reference what it learned:

> "Do you remember who I am?"

The character should acknowledge your name and role without you repeating them.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
If the character references details from the previous session, Long-Term Memory is working correctly.
{% endhint %}

***

## Why This Works in the Editor Without Any Code

The SDK's default `DeviceEndUserIdProvider` handles identity automatically:

1. **Stable GUID in the editor** — In Play Mode, the provider reads or creates a persistent GUID stored in `PlayerPrefs` under the key `"convai.end_user_id"`. Every Play Mode session on the same machine uses the same GUID, so memories accumulate across sessions just as they would for a real user.
2. **Identity sent on connect** — The GUID is transmitted to Convai when the session starts. Convai uses it to look up any stored facts for that user–character pair.
3. **Memory stored after session** — When you stop Play Mode, Convai processes the conversation and extracts facts (names, roles, preferences, history) as `MemoryRecord` entries.
4. **Injected on next connect** — On the next Play Mode session, those records are injected into the character's context before it generates its first response.

{% hint style="info" %}
The GUID persists as long as `PlayerPrefs` is not cleared. Clearing `PlayerPrefs` (or reinstalling the application on a device) generates a new GUID, which the server treats as a new user — no memories carry over. Plan for this in your release strategy. See [End-User Identity](/broken/pages/8dbe2add478ce0c30fa84a1a2a3fa773a8e349fc) for strategies that survive reinstalls.
{% endhint %}

***

## What Happens in Player Builds

In a player build, `DeviceEndUserIdProvider` first tries `SystemInfo.deviceUniqueIdentifier`. If that value is unavailable or invalid (some platforms return all-zero strings), it falls back to the same `PlayerPrefs` GUID approach used in the editor.

| Context                              | Identity Source                             |
| ------------------------------------ | ------------------------------------------- |
| Unity Editor                         | `PlayerPrefs` GUID — stable per project     |
| Player build (device ID available)   | `SystemInfo.deviceUniqueIdentifier`         |
| Player build (device ID unavailable) | `PlayerPrefs` GUID — stable until reinstall |

For applications where users log in with accounts, replace `DeviceEndUserIdProvider` with a custom provider that returns your account IDs. Device-based IDs will not follow a user who switches devices. See [End-User Identity](/broken/pages/8dbe2add478ce0c30fa84a1a2a3fa773a8e349fc) for implementation details.

***

## Next Steps

{% content-ref url="/broken/pages/8dbe2add478ce0c30fa84a1a2a3fa773a8e349fc" %}
[Broken link](/broken/pages/8dbe2add478ce0c30fa84a1a2a3fa773a8e349fc)
{% endcontent-ref %}

{% content-ref url="/broken/pages/0efba5470b7275e3ae81e0c0c74c5e419f42c9c3" %}
[Broken link](/broken/pages/0efba5470b7275e3ae81e0c0c74c5e419f42c9c3)
{% endcontent-ref %}
