---
description: >-
  Allows sending dynamic information about the current environment to the
  character without having to receive a response from the character - Supported
  in Plugin Version 3.5.1 or later.
---

# Dynamic Environment Info

## Overview

Dynamic Environment Info is a powerful feature in our Convai plugin that allows users to pass additional environmental data to characters without direct interaction. This enables more immersive and creative gameplay scenarios by enhancing how characters perceive their surroundings.

For example:

* The character can understand the **time of day** (e.g., "time of day is night").
* The character can access **inventory details** (e.g., "You currently have a gun and a healing potion").
* The feature supports structured data formats for richer information exchange.

***

Follow the steps below to integrate Dynamic Environment Info into your project.

**Step 1: Modify the Character Blueprint**

1. Open the **Character Blueprint** in your project.
2. In the **Begin Play** event, locate the `ConvaiChatbot` component.

<figure><img src="../../../.gitbook/assets/image (415).png" alt=""><figcaption></figcaption></figure>

1.  Set the `Dynamic Environment Info` variable with a string value of your choice.

    *   Example 1 (Simple):

        ```
        time of day is night
        ```

    <div align="left"><figure><img src="../../../.gitbook/assets/image (416).png" alt=""><figcaption></figcaption></figure></div>

    *   Example 2 (Structured Format):

        ```
        inventory: {weapon: gun, tools: [flashlight, rope]}
        ```

<div align="left"><figure><img src="../../../.gitbook/assets/image (418).png" alt=""><figcaption></figcaption></figure></div>

**Step 2: Save and Play**

1. Save your blueprint changes.
2. Hit **Play** to test the interaction.
3. Observe how the character dynamically responds based on the information passed.

<figure><img src="../../../.gitbook/assets/image (417).png" alt=""><figcaption></figcaption></figure>

***

By following these simple steps, you can unlock more engaging gameplay mechanics and enrich the interactions.
