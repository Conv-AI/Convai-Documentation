---
description: >-
  Learn how to install, set up, and run the Convai Unity Plugin Beta to
  integrate conversational AI characters directly within your Unity projects.
---

# Installation and Setup

## **Introduction**

The Convai Unity Plugin (Beta) allows you to seamlessly integrate Convai’s advanced conversational AI characters into your Unity projects. This plugin simplifies setup and provides a ready-to-run demo scene so you can start interacting with Convai-powered characters immediately.

***

## **Installation Guide**

Follow these steps to install and configure the Convai Unity Plugin Beta.

### **1. Download the Plugin**

Download the latest Convai Unity Beta Plugin package from the provided link.

### **2. Extract the Package**

Unzip the downloaded `.zip` file to your preferred location on your computer.

### **3. Add the Project to Unity Hub**

1. Open **Unity Hub**.
2. Click **Add** next to the _New Project_ button.
3. Select **Add Project from Disk**.
4. Browse to the extracted Convai Unity Plugin folder and click **Open**.
5. In the version selection dialog, choose a Unity version installed on your system or download the latest **LTS (Long-Term Support)** version.

{% hint style="info" %}
Convai Unity Plugin supports **Unity 2022 and above**.
{% endhint %}

Unity will now create a new project based on the plugin files.

***

## **Initial Setup**

Once the project loads, Unity will automatically begin downloading additional files required for the plugin to function correctly.\
This download process ensures that the initial plugin package remains lightweight.

After the setup completes:

1. Go to the **Top Menu** → **Convai**.
2. Select **Account** from the dropdown.
3. In the **API Key** field, paste your Convai API key (you can copy it from your [Convai Dashboard](https://convai.com/)).

***

### **Running the Demo Scene**

To verify that the plugin is correctly installed:

1. Navigate to:\
   `Assets/Convai/Demo/Scenes/Convai Sample Scene.unity`
2. Open the scene.
3. Press the **Play** button in Unity.

You’ll see a default demo character appear in the scene.\
After a few seconds, the character will initialize and be ready for conversation.\
You can monitor the session initialization status through the **Console Window**.

***

### **Changing the Character ID**

To use your own Convai character instead of the default demo character:

1. In the **Hierarchy**, select the `ConvaiNPC` GameObject.
2. In the **Inspector**, locate the **ConvaiNPC** component.
3. Replace the **Character ID** field with your own character’s ID.

Your new character will now load and respond in the same demo scene.

***

### **Conclusion**

You’ve successfully set up and run the Convai Unity Plugin (Beta).\
From here, you can begin customizing the sample scene or integrate Convai characters directly into your own Unity environments.
