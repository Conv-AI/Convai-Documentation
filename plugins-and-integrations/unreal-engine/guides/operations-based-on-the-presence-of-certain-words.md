---
description: >-
  This document explains how to detect words and perform certain operations
  based on it.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/guides/operations-based-on-the-presence-of-certain-words
---

# Operations Based on the Presence of Certain Words

* Open your Convai Character blueprint and click on `Class Settings` and then on `ConvaiChatbot` component.&#x20;
* Under the `Details` section scroll down to the `Events` section and add `On Transcription Received` event.&#x20;

<figure><img src="../../../.gitbook/assets/WordDetection.jpg" alt=""><figcaption><p>Add On Transcription Received Event to Event graph. </p></figcaption></figure>

* Once we have the transcription of player input, we can perform a substring search on it.

<figure><img src="../../../.gitbook/assets/image (443).png" alt=""><figcaption><p>Substring search on transciption. </p></figcaption></figure>

{% hint style="info" %}
The Print String at the end is just an example. You can add your logic after the substring match.&#x20;
{% endhint %}

&#x20;
