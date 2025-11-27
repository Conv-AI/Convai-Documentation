---
description: >-
  Learn how to import animations recorded in VR and apply them to your AI
  avatars in Unity.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/no-code-experiences/convai-xr-animation-capture-app/adding-your-recorded-animations-to-ai-avatars-inside-unity
---

# Adding Your Recorded Animations to AI Avatars Inside Unity

## **Overview**

Bring your Convai avatars to life inside Unity by integrating animations recorded via the **Convai XR Animation Capture App**. This guide walks you through importing those animations and attaching them to AI-powered characters in your Unity project.

{% embed url="https://youtu.be/dI3xf4gQPRE" %}

## **How to Add Recorded Animations to AI Avatars in Unity**

### **Step 1: Set Up Unity & Convai**

Before importing animations, ensure your Unity project is correctly set up with Convai:

* Install the **Convai Unity SDK**.
* Retrieve your **API key** from the Convai Playground.
* Add the API key to your project settings.

{% hint style="success" %}
**Need help setting up the SDK?**\
Check out our [Unity SDK Documentation](https://docs.convai.com/api-docs/plugins-and-integrations/unity-plugin) or follow the [video](https://youtu.be/anb9ityi0MQ) walkthrough above.
{% endhint %}

***

### **Step 2: Import the Animation**

1. Go to the **Convai Dashboard** and navigate to the **Server Animations** tab.
2. Locate the animations you recorded in VR.
3. Click **Import** and select a location **within your Unity project's `Assets/` directory**.

{% hint style="warning" %}
The files **must be placed inside the Unity project folder** for them to be detected and used properly.
{% endhint %}

***

### **Step 3: Apply the Animation to a Character**

1. In Unity, drag your AI character model into the **scene hierarchy**.
2. Adjust the character’s position if needed.
3. Open or create an **Animator Controller**.
4. Drag the imported animation clip into the **Animator Controller**.
5. If the animation should repeat, enable **Loop Time** in the Animation settings.

***

### **Step 4: Test the Scene**

1. Run your Unity scene.
2. Start a conversation with the avatar or trigger the assigned action.
3. Watch your AI avatar perform the recorded animation in real-time!

***

#### **Done!**

You’ve now successfully connected a custom VR-recorded animation to an AI-powered avatar in Unity.\
Repeat the process to add more animations and create rich, expressive characters in your simulations or games.
