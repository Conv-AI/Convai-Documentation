---
description: >-
  This document explains how to change the audio gain through blueprints in
  Unreal Engine.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/microphone-settings/set-audio-gain
---

# Set Audio Gain

{% hint style="info" %}
The Audio Gain feature proves beneficial in scenarios where the incoming audio from the microphone is notably low in volume.
{% endhint %}

### Steps to change Audio Gain: -&#x20;

* Open the Player blueprint or the blueprint which has the <mark style="color:green;">`ConvaiPlayer`</mark> component in it.&#x20;
* From the ConvaiPlayer component search for <mark style="color:green;">`Set Microphone Volume Multiplier`</mark>function.&#x20;
* Enter any float value in the <mark style="color:green;">`In Volume Multiplier`</mark> property of the function which makes the audio loud and clear.&#x20;

<figure><img src="../../../.gitbook/assets/image (444).png" alt=""><figcaption><p>Use of Set Microphone Volume Multiplier function</p></figcaption></figure>
