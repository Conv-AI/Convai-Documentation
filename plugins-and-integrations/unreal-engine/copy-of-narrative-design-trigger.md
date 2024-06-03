---
description: >-
  This document explains how to use Narrative Design Triggers with Unreal
  Engine.
---

# Copy of Narrative Design Trigger

{% hint style="info" %}
Before proceeding with this section, it is advisable to familiarize yourself with the Narrative Design system, as elucidated in this [tutorial](https://youtu.be/C0JdmBTmZ9g?si=dImNu2-fBwKW1Frx).
{% endhint %}

## Use of Invoke Narrative Design Trigger in Unreal Engine.&#x20;

1. Develop the logical flow for your specific use case. In this instance, we have created a simple museum tour guide scenario.

<figure><img src="../../.gitbook/assets/image (347).png" alt=""><figcaption></figcaption></figure>

1. Once the logic is decided we can move to Unreal Engine. (In this guide we will use the same setup described in this [<mark style="color:green;">guide</mark>](guides/event-aware-convai-characters.md))
2. Our goal is to invoke the trigger `Start Tour` in the narrative Design graph, using the `Invoke Narrative Design Trigger` .
3. The `Trigger Name` in  the function should be the same as  the `Trigger` name on the graph.

<div align="left">

<figure><img src="../../.gitbook/assets/websiteTrigger (2).jpg" alt="" width="343"><figcaption><p>Website</p></figcaption></figure>

 

<figure><img src="../../.gitbook/assets/UE Trigger (2).jpg" alt=""><figcaption><p>Unreal Engine</p></figcaption></figure>

</div>

3. The above example showcased only one Trigger. The use of more than one Trigger is also possible based on execution logic.&#x20;

