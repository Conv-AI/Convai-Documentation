---
description: Integrating Convai character chatbot services in Roblox game.
---

# Roblox

## Overview

Roblox is an online game platform and game creation system developed by Roblox Corporation that allows users to program games and play games created by other users. This provides a perfect platform to develop games with intelligent AI-based NPCs with which the player can interact and experience a new way of story progression or gameplay altogether.

<figure><img src="../../.gitbook/assets/logo1.png" alt=""><figcaption></figcaption></figure>

## Constraints

Roblox environment doesn't support many essential features required to enjoy the power of the character API endpoints to their full potential.

{% hint style="warning" %}
Roblox doesn't allow the creation of audio files
{% endhint %}

We cannot utilize the audio response from Convai as there is no easy way to create an audio file and play it within the game.

{% hint style="info" %}
Roblox doesn't allow microphone access
{% endhint %}

We cannot record audio from the user and pass that directly to the server for processing and generating a response. We are limited to sending only text data through the request body and receive and display only text-data from the response.
