---
description: Convai UI Prefabs - Utilize ready-to-use UI elements for Convai integration.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/utilities/convai-ui-prefabs
---

# Pre-built UI Prefabs

We provide several UI options to display character and user's transcript out of the box that players can use with the Convai Plugin. You can use and customize these prefabs.&#x20;

The ConvaiNPC and ConvaiGRPCAPI scripts look for GameObjects with Convai Chat UI Handler as a component, and send any transcripts to the script so that it can be displayed on screen.

## Types of UI

<figure><img src="../../../.gitbook/assets/image (379).png" alt=""><figcaption></figcaption></figure>

### ChatBox

**Prefab Name**: Convai Transcript Canvas - Chat

Both the user's and the character's transcripts are displayed one after other in a scrollable chat box.

<figure><img src="../../../.gitbook/assets/image (383).png" alt=""><figcaption></figcaption></figure>

### Subtitle

**Prefab Name**: Convai Transcript Canvas - Subtitle

The user and character transcripts are displayed in the bottom like subtitles.

<figure><img src="../../../.gitbook/assets/image (385).png" alt=""><figcaption></figcaption></figure>

### Question-Answer

**Prefab Name**: Convai Transcript Canvas - QA

The user's transcript is displayed in the top where as the character's transcript is displayed in the bottom.

<figure><img src="../../../.gitbook/assets/image (388).png" alt=""><figcaption></figcaption></figure>

### Mobile Optimised UI Styles

**Prefab Name**: Convai Transcript Canvas - Mobile Subtitle

Identical to [#subtitle](convai-ui-prefabs.md#subtitle "mention") UI. Includes a button that can be pressed and held for the user to speak. Ideal for portrait orientation of screen.

<figure><img src="../../../.gitbook/assets/image (382).png" alt="" width="328"><figcaption></figcaption></figure>

**Prefab Name**: Convai Transcript Canvas - Mobile QA

<figure><img src="../../../.gitbook/assets/image (381).png" alt="" width="331"><figcaption></figcaption></figure>

**Prefab Name**: Convai Transcript Canvas - Mobile Chat

<figure><img src="../../../.gitbook/assets/image (380).png" alt="" width="327"><figcaption></figcaption></figure>

## [Convai Chat UI Handler Component](transcript-ui-system.md)

<figure><img src="../../../.gitbook/assets/image 2.png" alt=""><figcaption></figcaption></figure>

### Functions to Know

<table><thead><tr><th width="265"></th><th></th></tr></thead><tbody><tr><td>SendCharacterText</td><td>A public function that sends a string of text to be displayed  as character transcript along with the name of the character who said it. </td></tr><tr><td>SendUserText</td><td>A public function that sends a string of text to be displayed  as user transcript.</td></tr></tbody></table>

