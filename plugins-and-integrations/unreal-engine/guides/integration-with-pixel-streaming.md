---
description: >-
  This mini-guide provides instructions for setting up Convai with pixel
  streaming in Unreal Engine
---

# Integration with Pixel Streaming

{% hint style="info" %}
To setup the Pixel Streaming server, we recommend taking a look over [this excellent guide](https://github.com/TensorWorks/PixelStreamingCloudGuide/blob/main/Pixel%20Streaming%20UE5.md).
{% endhint %}

1. Ensure you have the latest Convai 3.1.0 plugin or later.
2.  Enable Unreal Engine's `Pixel Streaming` and the `Pixel Streaming Player` Plugins from the Plugins window.\


    <figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
3.  In the player blueprint which has the Convai Player component, add the PixelStreamingAudio component to the list of components.\


    <figure><img src="../../../.gitbook/assets/image (3) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
4.  Click on PixelStreamingAudio component, and in the details panel find Base Submix and choose AudioInput sound submix.\


    <figure><img src="../../../.gitbook/assets/image (5) (1) (1).png" alt=""><figcaption></figcaption></figure>
5. On Begin Play in the event graph, add the following blueprint function to initialize Pixel Streaming with the Player Component.

<figure><img src="../../../.gitbook/assets/image (6) (1) (1).png" alt=""><figcaption></figcaption></figure>

<div data-full-width="false"><figure><img src="../../../.gitbook/assets/SetPixelStreamingAudioComponent.png" alt=""><figcaption><p>To Get <em><strong>Set Pixel Streaming Audio Component</strong></em> Node</p></figcaption></figure></div>

{% hint style="info" %}
Now, pixel streaming mic input should be working. However, system microphone will no longer work. To change back and forth to and from system microphone, set Use Pixel Streaming Mic Input to true for enabling pixel streaming microphone and false to enable system microphone. This is found in the ConvaiPlayer component.
{% endhint %}

<figure><img src="../../../.gitbook/assets/image (7) (1) (1).png" alt=""><figcaption></figcaption></figure>
