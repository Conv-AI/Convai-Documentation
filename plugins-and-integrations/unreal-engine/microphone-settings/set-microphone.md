---
description: This document explains how to set microphone through blueprints
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/microphone-settings/set-microphone
---

# Set Microphone

### Follow the steps below to set active microphone&#x20;

* Open the player blueprint or the blueprint that has the Convai Player component in it.&#x20;
* Drag the `ConvaiPlayer` component in your `Event Graph` and search for `Set Capture Device by Name` or `Set Capture Device by Index`. These functions are used to set the microphone by its index or by its name.&#x20;

<figure><img src="../../../.gitbook/assets/image (451).png" alt=""><figcaption><p>Example to set Microphone in Unreal Engine using Convai</p></figcaption></figure>
