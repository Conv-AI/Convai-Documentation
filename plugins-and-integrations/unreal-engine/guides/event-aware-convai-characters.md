---
description: >-
  This document explains how to make characters respond to events happening in
  their surroundings with a small example.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/guides/event-aware-convai-characters
---

# Event-Aware Convai Characters

## Use of Invoke Speech function&#x20;

Our goal in this example is to have the character welcome the player whenever the player enters a certain area, this can be done by using the `Invoke Speech` node that basically invokes the AI character to talk and a simple collision box.

1. Open your AI character blueprint and select the `Viewport` tab.\
   Note: the character blueprint can be a MetaHuman, ReadyPlayerMe, Reallusion or even a custom one you have created, just ensure that it has the `Convai Chatbot` component.
2. From the `Components` list add a `Box Collision`.&#x20;

<figure><img src="../../../.gitbook/assets/Event awareness 1.jpg" alt=""><figcaption><p>Add box collision to your Convai Character</p></figcaption></figure>

3. Switch back to the `Event Graph` tab.
4. Select the `Box Collision` you just added and scroll down in the `Details panel`.  Under `Events`  add the `On Component Begin Overlap`  event to your event graph.&#x20;

<figure><img src="../../../.gitbook/assets/event awareness 2.jpg" alt=""><figcaption><p>Add On Component Begin Overlap event to EventGraph</p></figcaption></figure>

6. Setup the following blueprint schematic which uses the `Invoke Speech` node from the `Convai Chatbot` component.&#x20;

<figure><img src="../../../.gitbook/assets/image (404).png" alt=""><figcaption><p>Invoke Speech function from Convai Chatbot component</p></figcaption></figure>

7. Enter a `Trigger Message` that expresses what happened (i.e. "Player Approached") and you can add a simple instruction (i.e. Greet the player).
8. Setting the `In Generate Actions` and `In Voice Response` boolean to true will let the Convai Characters perform actions and generate audio responses respectively.
9. Hit `Compile` and `Save` then run the program.&#x20;
10. On approaching a certain vicinity will trigger the event and the Convai Character will greet the character as mentioned in the Trigger Message.&#x20;

<figure><img src="../../../.gitbook/assets/image (405).png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
The above example is just a simple use case. However, the use of Invoke Speech opens new doors to limitless use cases.&#x20;
{% endhint %}
