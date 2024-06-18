---
description: Follow these instructions to setup the Unity Plugin into your project.
---

# Setting Up Unity Plugin

{% hint style="info" %}
The file structure belongs to the Core version of the plugin downloaded from the documentation.
{% endhint %}

### Setting up Unity Plugin

In the Menu Bar, go the Convai > Convai Setup.

<figure><img src="../../.gitbook/assets/image (291).png" alt=""><figcaption></figcaption></figure>

Go to [convai.com](https://convai.com), and sign in to your Convai account. Signing in will redirect you to the Dashboard. From the dashboard, grab your API key.

<figure><img src="../../.gitbook/assets/image (288).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (289).png" alt=""><figcaption></figcaption></figure>

Enter the API Key and click begin.

<figure><img src="../../.gitbook/assets/image (120).png" alt=""><figcaption><p>Screenshot showing the API Key setup window</p></figcaption></figure>

This will create an APIKey asset in the resources folder. This contains your API Key.&#x20;

<figure><img src="../../.gitbook/assets/image (292).png" alt=""><figcaption><p>Screenshot showing where is the API Key in the project folder</p></figcaption></figure>

Open the demo scene by going to Convai > Demo > Scenes&#x20;

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>



Click the Convai NPC Amelia and add the Character ID (or you can keep the default character ID). You can get the character ID for your custom character from this page [create-character.md](../../convai-playground/character-creator-tool/create-character.md "mention"). Now you can converse with the character. The script is set up so that you have to go near the character for them to hear you.

<figure><img src="../../.gitbook/assets/image (296).png" alt=""><figcaption></figcaption></figure>

Now you can test out the Convai Demo Scene and talk to the character present there. Her name is Amelia and she loves hiking!

<figure><img src="../../.gitbook/assets/image (293).png" alt=""><figcaption></figcaption></figure>

You can open the Convai NPC Script to replicate or build on the script to create new NPCs.

{% hint style="warning" %}
Edit the ConvaiNPC.cs script directly to maintain compatibility with the Utility scripts.
{% endhint %}
