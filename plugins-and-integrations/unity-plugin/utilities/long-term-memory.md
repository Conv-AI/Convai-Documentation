---
description: >-
  Learn how to enable character retain conversation history across multiple
  sessions
---

# Long Term Memory

Long-Term Memory (LTM) enables the persistent storage of conversational history with NPCs, allowing players to seamlessly continue interactions from where they previously left off, even across multiple sessions. This feature significantly enhances the realism of NPCs, aligning with our goal of creating more immersive and lifelike characters within your game.

{% hint style="info" %}
Prerequisite: Have a project with Convai SDK version 3.1.0 or higher. If you don't have it, check this documentation&#x20;

[setting-up-unity-plugin.md](../setting-up-unity-plugin.md "mention")
{% endhint %}

### Steps to get LTM working

1.  Select your Convai Character&#x20;

    <figure><img src="../../../.gitbook/assets/AddComponent.png" alt=""><figcaption></figcaption></figure>
2.  Add the Long-Term Memory Component onto your character

    <figure><img src="../../../.gitbook/assets/Adding LTM.png" alt=""><figcaption></figcaption></figure>
3.  Make sure that Long Term Memory is enabled for that character&#x20;

    <figure><img src="../../../.gitbook/assets/LTM Enabled.png" alt=""><figcaption></figcaption></figure>

Long Term Memory should now be working for your character.

### Components of the LTM System

#### Convai Long Term Memory Component

This component will enable or disable LTM right from the unity editor

<figure><img src="../../../.gitbook/assets/LTM Disabled.png" alt=""><figcaption></figcaption></figure>

Toggling Long Term Memory

1\) Click the button provided in the component

<figure><img src="../../../.gitbook/assets/LTM Disabled Button Highlighted.png" alt=""><figcaption></figcaption></figure>

2\) It will take some time to update, and after that the new status of the LTM should be visible in the inspector.

<figure><img src="../../../.gitbook/assets/LTM Updating Status.png" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
Since enabling or disabling Long-Term Memory (LTM) for a character is a global action that impacts all players interacting with that character, we strongly recommend against toggling the LTM status at runtime. This functionality should be managed exclusively by developers or designers through the editor to ensure consistent gameplay experiences.
{% endhint %}

### Troubleshooting

{% hint style="danger" %}
Grpc.Core.RpcException: Status(StatusCode=InvalidArgument, Detail="Cannot find speaker with id: 99fbef96-5ecb-11ef-93ce-42010a7be011.")
{% endhint %}

If you encounter this error, ensure that the **SpeakerID** was created using the same API key currently in use. If you're uncertain about the API key used, you can reset the **SpeakerID** and **PlayerName** by accessing the `ConvaiPlayerDataSO` file located in `Assets > Convai > Resources`, allowing you to start the process anew.
