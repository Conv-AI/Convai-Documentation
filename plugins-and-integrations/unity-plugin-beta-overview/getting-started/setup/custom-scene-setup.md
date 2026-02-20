---
description: >-
  Add the required Convai objects, set up a player, and connect characters to
  Convai.
---

# Custom Scene Setup

## Introduction

This guide integrates Convai into your own scene by adding the required core objects, creating a Convai player, and configuring Convai characters.

## Prerequisites

* Convai SDK installed
* API key configured successfully
* Your scene opened in Unity

## Step-by-step

{% stepper %}
{% step %}
### Add required Convai scene objects

* In Unity top menu, go to **GameObject → Convai → Setup Required Components**\
  **or** Right-click in the **Hierarchy** → **Convai → Setup Required Components**

<figure><img src="../../../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

* Confirm and proceed in the popup.
* **Expected result:** These objects exist in your scene:
  * **\[Convai Service Bootstrap]**
  * **\[Convai Composition Root]**
  * **\[Convai Room Manager]**

<figure><img src="../../../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Create or select your Player object

* Select your existing player GameObject, or create an empty one.
* Add **Convai Player Component**.
* Set **Player Name**.
* **Expected result:** The scene has exactly one configured Convai Player.

<figure><img src="../../../../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Add Convai Character components

For each character GameObject you want to make conversational:

* Add **Convai Character** component
* Set **Character ID**

<figure><img src="../../../../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Get your Character ID from Convai

* [In Convai dashboard](https://docs.convai.com/api-docs/convai-playground/character-customization/character-description#id-1.-character-name-and-id), open your character and copy its ID.
{% endstep %}

{% step %}
### Validate your scene setup

* Use one of the validation options:
  * Top menu: **GameObject → Convai → Validate Scene Setup**
  * Hierarchy right-click: **Convai → Validate Scene Setup**

<figure><img src="../../../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

* **Expected result:** A success message like:
  * “Scene setup is correct!” and the number of Convai Characters found.

<figure><img src="../../../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Run a conversation test

* Press **Play**
* Speak using microphone or use Chat UI if present
* **Expected result:** Characters respond. Microphone conversation is **hands-free** (no push-to-talk required).
{% endstep %}
{% endstepper %}

## Troubleshooting

* **Validation fails**
  * Confirm the required objects exist in the scene.
  * Ensure you added Convai Player Component to a player object.
  * Ensure each character has a valid Character ID.
* **Characters don’t respond**
  * Confirm API key is set.
  * Check Console for network/auth errors.

## Conclusion

You’ve integrated Convai into your custom scene, validated the setup, and confirmed characters can respond. Next, optionally add **Chat UI** to support text input and transcripts.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
