---
description: >-
  This guide will walk you through setting up the NPC to NPC conversation
  feature in the Convai SDK.
---

# Adding NPC to NPC Conversation

## **Step 1: Setting up Convai NPC**

1. **Go to your Convai NPCs**:
   * Select the NPCs you want to include in the conversation.
2. **Enable Group NPC Controller**:
   * Click on the `Group NPC Controller` checkbox in the inspector panel.
   *   Click `Apply Changes` to add the group NPC controller script.\


       <figure><img src="https://lh7-us.googleusercontent.com/JUlMGlkifNW_8JQ1FJO-55h_c754kh1kgepM0gJFaZ0Ek6FNUyCLvrn2EqtfDORjY8k6-2fsSTzry9LLEWihFhnv0ZGFBSMFIkQ6xGFd0qk9z87p4pz91O6Bvc1vzMqBi_hpxaTvPwvjTMg70iaAm9U" alt=""><figcaption></figcaption></figure>
3. **Create or Find the Speech Bubble Prefab**:
   *   Create a new speech bubble prefab or use the one provided in the `Prefabs` folder.\


       <figure><img src="../../.gitbook/assets/image (373).png" alt=""><figcaption></figcaption></figure>
4. **Attach Required Components**:
   * Add the speech bubble prefab and the player transform (optional, defaults to the main camera if not provided).
   *   Set the conversation distance threshold variable (set it to zero to disable this feature, meaning NPC to NPC conversations will always happen regardless of the player’s distance).\


       <figure><img src="../../.gitbook/assets/image (374).png" alt=""><figcaption></figcaption></figure>
5. **Add Relevant Components**:
   * Add components like lip sync, eye and head tracking, character blinking, etc., to the Convai NPC.

## **Step 2: Setting up NPC Manager**

1. **Create an NPC To NPC Manager GameObject**:
   * Add an empty GameObject and rename it to `NPC to NPC Manager` (optional).
2. **Add the NPC2NPC Conversation Manager Script**:
   *   Attach the `NPC2NPCConversationManager` script to the GameObject.\


       <figure><img src="../../.gitbook/assets/Screenshot 2024-05-27 184719.png" alt=""><figcaption></figcaption></figure>
3. **Configure the NPC Group List**:
   * In the `NPC Group List`, click on the `+` icon to add a new list element.
   * Add the NPCs you want to include in the group conversation.
   *   Set the group discussion topic.\


       <figure><img src="../../.gitbook/assets/image (377).png" alt=""><figcaption></figcaption></figure>
4. Post configuration of NPCs
   * Bring the NPCs close together
   *   Play the to make sure everything is working as intended.\


       <figure><img src="../../.gitbook/assets/Screenshot 2024-05-27 185141 (1).png" alt=""><figcaption></figcaption></figure>

By following these steps you can set up and manage NPC to NPC conversations in your Convai-powered application. For further customization and integration, refer to the complete implementation code and adjust it as needed for your specific use case.
