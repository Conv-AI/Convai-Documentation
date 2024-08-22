---
description: All the information that Convai SDK needs from the player to work properly
---

# Player Data Container

This is a scriptable object which is made automatically after you hit play in the editor with Convai SDK installed and in a Scene where Convai Base Scene Essentials Prefab is present

<figure><img src="../../../.gitbook/assets/image (397).png" alt=""><figcaption></figcaption></figure>

**Default Player Name**

You can provide a default name of your players.

**Player Name**

Current name of your player, out of the box if you use our settings panel, we keep it updated automatically, if you are using some custom logic, it will be your responsibility to keep it updated, as our transcript UI use this name to show it in UI&#x20;

**Speaker ID**

Speaker ID for the player. **Please note that Speaker ID is directly linked with your API key, so for each API key there should be a unique speaker ID associated with it.** We handle the creation of the Speaker ID when it's not found in the Player Prefs if the Boolean is set to true.

**Create Speaker ID If Not Found**&#x20;

This Boolean lets the SDK if it should create a unique Speaker ID for that Player Name if it is not found in the Player Prefs.

### Buttons

#### **Reset Data**

It just makes the **Player Name** and **Speaker ID** fields empty.

#### **Copy Data**

Copies the data into system buffer so you can paste it anywhere for debugging purpose

#### **Player Pref Settings Button**

1. **Load:** Loads the **Player Name** and associated **Speaker ID** from the player Prefs
2. **Save:** Saves the **Player Name** and associated **Speaker ID** from the player Prefs
3. **Delete:** Deletes the **Player Name** and associated **Speaker ID** from the player Prefs

### How to maintain the Player Data

Convai provides a pre-made component which you can add to any `GameObject` to make the `PlayerDataContainer` work out of the box.

Choose an existing GameObject or create a new `GameObject` in the scene and add the `ConvaiPlayerDataHandler` component to your chosen `GameObject` and it should start working

<figure><img src="../../../.gitbook/assets/ConvaiPlayerDataHandler Component.png" alt=""><figcaption></figcaption></figure>

#### Optional Step

You can also create the required Scriptable Object by going to **`Assets > Convai > Resources`** and right clicking in the project panel and navigating to **`Create > Convai > Player Data`** and name it **`ConvaiPlayerDataSO`**

<figure><img src="../../../.gitbook/assets/Creating Player Data SO.png" alt=""><figcaption></figcaption></figure>

{% hint style="danger" %}
Make sure you name the created Scriptable Object exactly **`ConvaiPlayerDataSO`** as our system looks for this exact name
{% endhint %}
