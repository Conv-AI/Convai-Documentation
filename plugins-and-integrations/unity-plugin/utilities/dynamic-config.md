# Dynamic Config

The **Dynamic Config** feature enables you to pass variables to NPCs in real time, allowing them to react dynamically to changes in the game environment. This can include the player’s current health, inventory items, or contextual world information, greatly enhancing interactivity and immersion.



## **Step-by-Step Guide to Setting Up Dynamic Config**

Firs&#x74;**, Add the Dynamic Info Controller** Component to your Convai NPC.

<figure><img src="../../../.gitbook/assets/Unity_DynamicInfoControllerComponent (1).png" alt=""><figcaption></figcaption></figure>

Create a new script or use an existing script to define a variable that will store a reference to the **Dynamic Info Controller** Component you added to your NPC.

### **Example: Passing Player Health to the NPC**

* **Initialize the Dynamic Info**: In the script’s **Start** method, call the `SetDynamicInfo` method on the **Dynamic Info Controller** reference. This will set the dynamic information that the NPC will use. In this example, we’ll initialize the Player’s health as a dynamic variable.
* **Updating the Dynamic Info**: Whenever you need to update the NPC with new information (such as a change in Player Health), call the `SetDynamicInfo` method on the Dynamic Info Controller.

### **Sample Scenario**

* At the start of the game, we set the Player’s health to 100 and send this information to the NPC as the initial value.
* Then, when the player takes damage (simulated here by pressing the "K" key), we reduce the Player’s health and update the **Dynamic Info** in real time so that the NPC remains aware of the Player's current health status.

<figure><img src="../../../.gitbook/assets/Unity_DynamicInfo_ExampleCode (3).png" alt=""><figcaption></figcaption></figure>

### **Example Conversation**

Below, we provide a sample conversation showcasing how the NPC can react based on the dynamic health information of the Player. By dynamically updating the Player's health, NPCs can deliver responses that feel personalized and relevant to the current gameplay.

### **In summary**&#x20;

Add the **Dynamic Info Controller** to your NPC. Use `SetDynamicInfo` to initialize the dynamic variable at the start, and call `SetDynamicInfo` again whenever updates are needed.

This feature provides a powerful tool for creating NPC interactions that respond in real-time to the state of the game world, creating a more immersive experience for the player. :tada::sunglasses:

<figure><img src="../../../.gitbook/assets/Unity_DynamicInfoConversation (1).png" alt=""><figcaption></figcaption></figure>

