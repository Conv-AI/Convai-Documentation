---
description: Add Descriptions to Actions - Custom Actions Guide for Unreal Engine.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/guides/actions-guide/stage-2-custom-actions/adding-descriptions-to-actions
---

# Adding Descriptions to Actions

### Overview

This document details the process for adding descriptions to actions within Convai characters, improving AI understanding and action execution. Action descriptions provide contextual information, aiding in more accurate and contextually appropriate behaviors.

### Why Add Action Descriptions?

Action descriptions offer contextual hints to the AI, helping determine when and how to trigger actions based on gameplay and conversation scenarios, enhancing the gaming experience through more accurate AI responses.

### How to Add Descriptions to Actions

1. **Identify the Action**: Determine the action needing a description, such as "**Sit Down**" or "**Crouch**".
2. **Format for Adding Descriptions**: Use the format `Action Name <Description>` to add descriptions. The description should be clear and concise, providing exact indications for the AI.
3. **Examples**:
   *   **Sit Down:**

       ```
       sit down <Use this action to make the character sit, suitable for resting, healing, or engaging in conversations with NPCs. Ideal for safe zones or interaction points>
       ```
   *   **Crouch:**

       ```
       crouch <This action lowers the character's profile, used for stealth or navigating low spaces>
       ```
   *   **Attack Enemy:**

       ```
       attack enemy <Trigger this action when the player chooses to attack an enemy unit>
       ```
   *   **Send Email:**

       ```
       send email <Initiate this action to allow the user to compose and send an email>
       ```

### Implementing Action Descriptions

1.  **Navigate to Convai Info Section**: Select your Convai character in the editor and access the Convai Info section.<br>

    <div data-full-width="false"><figure><img src="../../../../../.gitbook/assets/image (446).png" alt="" width="296"><figcaption></figcaption></figure></div>
2. **Adding Action with Description**: Click the Add Element (+) icon to input the action along with its description as previously formatted.

<figure><img src="../../../../../.gitbook/assets/image (459).png" alt=""><figcaption></figcaption></figure>

### Additional Tips

* **Clear and Specific Descriptions**: Ensure descriptions are straightforward, precisely indicating action triggering conditions.
* **Use English.**
