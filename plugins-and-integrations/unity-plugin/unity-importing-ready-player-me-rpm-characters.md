---
description: >-
  This guide walks you through the process of importing Ready Player Me (RPM)
  characters into a Convai-powered Unity project, configuring them, and
  integrating Convai NPC components.
---

# Importing Ready Player Me (RPM) Characters

## **Introduction**

Ready Player Me (RPM) allows users to create and customize 3D avatars easily. By integrating RPM characters into Convai's Unity SDK, you can bring dynamic NPCs to life with advanced AI-driven interactions. This guide covers the step-by-step process to set up RPM characters in your Unity project with Convai.

## **Prerequisites**

Before getting started, ensure you have the following:

* A [**Ready Player Me**](https://readyplayer.me/) account
* A **model link** for your RPM character
* A **Unity project** with the **Convai SDK** installed and working

## Step-by-Step Guide

### Step 1: Install Ready Player Me SDK in Unity

1. Open **Unity** and navigate to **Window > Package Manager**.

<figure><img src="../../.gitbook/assets/Untitled (30).png" alt=""><figcaption></figcaption></figure>

2. Click the **(+)** icon and select **Install Package from Git URL**.

<figure><img src="../../.gitbook/assets/Untitled (31).png" alt=""><figcaption></figcaption></figure>

3. Enter the following Git URL and click **Install**:

&#x20;`https://github.com/readyplayerme/rpm-unity-sdk-core.git#f6ea3c4b0a8891b7c4c1d7b269cee545185549fb`&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-03-23 034148.png" alt=""><figcaption></figcaption></figure>

4. Wait for the installation to complete.

### Step 2: Configure the RPM Avatar

1. In the **Project Panel**, navigate to: **Assets > Ready Player Me > Resources > Settings**

<figure><img src="../../.gitbook/assets/Untitled (33).png" alt=""><figcaption></figcaption></figure>

2. Right-click inside the folder and go to **Create > Ready Player Me > Avatar Configuration**.

<figure><img src="../../.gitbook/assets/Untitled (34).png" alt=""><figcaption></figcaption></figure>

3. This will generate an **Avatar Config** asset.
4. Select the created asset and, under the **Inspector Panel**, locate the **Morph Targets** section.
5. Click **Add**, select the required morph targets **(Oculus Visemes or ARKit)**, and save the asset.

<figure><img src="../../.gitbook/assets/Untitled (35).png" alt=""><figcaption></figcaption></figure>

6. Locate **Assets > Ready Player Me > Resources > Settings > AvatarLoaderSettings** and assign the **Avatar Config** asset to the **Avatar Config** field.

<figure><img src="../../.gitbook/assets/Untitled (36).png" alt=""><figcaption></figcaption></figure>

7. Save the asset.

### Step 3: Import the RPM Character

1. Navigate to **Tools > Ready Player Me > Avatar Loader**.

<figure><img src="../../.gitbook/assets/Untitled (37).png" alt=""><figcaption></figcaption></figure>

2. Paste or enter your **RPM Model Link** in the provided input field.

<figure><img src="../../.gitbook/assets/Untitled (38).png" alt=""><figcaption></figcaption></figure>

3. Click **Load Avatar into Current Scene** to import your character.

### Step 4: Integrate Convai Components

1. Select your imported **RPM GameObject** in the **Hierarchy Panel**.
2. Add the **Convai NPC** component to the GameObject.
3. Fill in the **name and ID** of the Convai NPC you wish to integrate.

<figure><img src="../../.gitbook/assets/Untitled (39).png" alt=""><figcaption></figcaption></figure>

4. Click **Add Components** inside the **Convai NPC** component.

<figure><img src="../../.gitbook/assets/Untitled (40).png" alt=""><figcaption></figcaption></figure>

5. Choose the components you want and click **Apply Changes**.

<figure><img src="../../.gitbook/assets/Untitled (41).png" alt=""><figcaption></figcaption></figure>

6. Attach a **Capsule Collider** to the GameObject and configure its **size** and **center** to align with the character's body proportions. Ensure that the collider accurately encapsulates the character for optimal physics interactions and collision detection.

<figure><img src="../../.gitbook/assets/image (428).png" alt=""><figcaption></figcaption></figure>

7. Assign an **Animation Controller** to the Animator component of the GameObject. The **Convai SDK** offers two predefined animation controllers (**Feminine** and **Masculine**) that you can use. Alternatively, you can integrate a custom controller tailored to your requirements.

<figure><img src="../../.gitbook/assets/image (429).png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
**Enhance your character with additional features:**

* **Add LipSync**: Follow [this guide](adding-lip-sync-to-your-character.md) to integrate LipSync into your character.
* **Implement Narrative Design**: Check out [this guide](adding-narrative-design-to-your-character/) to add Narrative Design.
* **Set up Actions**: Explore action-based interactions using [this guide](adding-actions-to-your-character.md).
{% endhint %}

### Conclusion

You have successfully integrated a Ready Player Me character into your Convai-powered Unity project. You can now leverage Convai’s capabilities to bring intelligent, interactive NPCs to life. :tada::sunglasses:

{% hint style="info" %}
For more details about Ready Player Me, visit [Ready Player Me](https://docs.readyplayer.me/ready-player-me/integration-guides/unity).
{% endhint %}
