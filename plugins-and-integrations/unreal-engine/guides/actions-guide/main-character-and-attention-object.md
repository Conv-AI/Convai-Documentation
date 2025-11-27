---
description: >-
  This page gives an overview of how to use set the Main character the AI is
  talking to and the Object In Attention
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/guides/actions-guide/main-character-and-attention-object
---

# Main Character and Attention Object

1. Navigate to your AI character blueprint.
2. Drag the `Convai Chatbot` component into the event graph.
3. Get the `Environment` Object and make sure it is valid.
   1. Use the function `Set Main Character` to define the current speaker to the AI character. Additionally, if you're using Convai's animation blueprints then setting the Main Character would cause the AI character to look at the Main Character reference.
   2. Use the function `Set Attention Object` to set which object is currently being talked about, this function also automatically adds the input object to the list of already existing objects in the environment.

{% hint style="info" %}
The character blueprint can be a MetaHuman, ReadyPlayerMe, Reallusion or even a custom one you have created, just ensure that it has the `Convai Chatbot` component.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/image (448).png" alt=""><figcaption><p>Illustrative schematic for the Set Main Character and Set Attention Object functions</p></figcaption></figure>
