---
description: >-
  Follow this guide to incorporate Narrative Design into your Convai-powered
  characters. Follow this step-by-step tutorial, open your project, and let's
  begin!
---

# Adding Narrative Design to your Character

## Convai Playground

### Step 1: Select your Character in which you want to enable Narrative Design

{% hint style="info" %}
For this demo, we are using `Seraphine Whisperwind`, you can select whatever character you want to enable Narrative Design.
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 114710.png" alt=""><figcaption><p>Screenshot showing selection of character in <a href="adding-narrative-design-to-your-character.md#convai-playground">Convai Playground</a></p></figcaption></figure>

### Step 2: Open Narrative Design in Convai Playground

Select the Narrative Design option from the side panel and create your narrative design

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 115450.png" alt=""><figcaption><p>Screenshot showing Icon of Narrative Design</p></figcaption></figure>

{% hint style="info" %}
For more information how to create narrative design in the [Convai Playground](adding-narrative-design-to-your-character.md#convai-playground) please refer to the following YouTube video series
{% endhint %}

{% embed url="https://www.youtube.com/playlist?list=PLn_7tCx0Chip2mfSbOkqJLevEbm3jDuNV" %}
Video series showing how to create Narrative Design
{% endembed %}

For this sample we have created the following Narrative design

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 123350.png" alt=""><figcaption></figcaption></figure>

You are all set to bring your character from Convai Playground to Unity, let's hope over to Unity to continue the guide

## Unity Setup

### Step 1: Add the Narrative Design Manager Component

#### Using <mark style="color:green;">Add Components</mark> Button in Convai NPC (Recommended Way)

#### **1:** Select your Convai Character in the scene and look for [ConvaiNPC ](broken-reference)component in the inspector panel. Click on <mark style="color:green;">**Add Components**</mark> button

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 122312.png" alt=""><figcaption><p>Screenshot showing location of <mark style="color:green;">Add Components</mark> button in the Convai NPC inspector panel </p></figcaption></figure>

#### **2:** Select **Narrative Design Manager** checkbox and then click on <mark style="color:green;">Apply Changes</mark> button

<figure><img src="../../.gitbook/assets/ND Component Selected.png" alt=""><figcaption><p>Screenshot showing selection of Narrative design option in the Add Component Window</p></figcaption></figure>

#### Using Unity Inspector

#### **1:**  Select your Convai Character and find Add Component button in the inspector panel&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 122424.png" alt=""><figcaption><p>Screenshot showing location of Add Component button in the inspector panel</p></figcaption></figure>

#### 2: Search for `Narrative Design Manager` in the search box and select it

<figure><img src="../../.gitbook/assets/ND Component Selected (1).png" alt=""><figcaption><p>Screenshot showing which component to select from the search results</p></figcaption></figure>

### Step 2: Setup the Narrative Design Component

After adding the Narrative Design Component, you will be able to be the following component

{% hint style="danger" %}
This component system assumes that API key is setup correctly, so ensure that API key is setup correctly otherwise an error will be thrown.
{% endhint %}

{% hint style="info" %}
After adding, component will retrieve the sections for the character ID taken from the ConvaiNPC, please wait for some time depending upon your network speed
{% endhint %}

{% hint style="warning" %}
The following section events are for character used in demo, and you will see section events corresponding to your character in which Narrative Design is enabled.&#x20;
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 122537.png" alt=""><figcaption><p>Screenshot showing a sample Narrative Design component</p></figcaption></figure>

### Getting to know the Narrative Design Component

Expanding the section event, you will see two unity events you can subscribe to, one is triggered when section starts, and another one is triggered when section ends

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 143301.png" alt=""><figcaption><p>Screenshot showing various unity events user can subscribe to</p></figcaption></figure>

### Getting to know about Section Triggers

Section triggers are a way to directly invoke a section in narrative design and can be used to jump to a different section in your narrative design

#### Step 1: Select the game object you want to make a trigger, in this example we have selected a simple cube, but it's up to your imagination.

{% hint style="info" %}
Make sure that game object you have decided to be a trigger have a collider attach to it
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 144701.png" alt=""><figcaption><p>Screenshot showing a game object with a collider selected</p></figcaption></figure>

#### Step 2: Add Narrative design Trigger from Add Component menu by searching for it

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 145128.png" alt=""><figcaption><p>Screenshot showing selection of Narrative Design Trigger</p></figcaption></figure>

#### Step 3: Make the collider a trigger.

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 145314.png" alt=""><figcaption><p>Screenshot showing Box Collider becoming a trigger box</p></figcaption></figure>

#### Step 4: Assign your Convai NPC to Convai NPC field

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-22 145631.png" alt=""><figcaption><p>Screenshot showing assigning of Convai NPC to trigger component</p></figcaption></figure>

Now you can select from the "Trigger" dropdown which trigger should be invoked when player enters this trigger box.&#x20;

We have added a way for you to manually invoke this trigger also, you can use `InvokeSelectedTrigger` function to invoke the trigger from any where

<figure><img src="../../.gitbook/assets/Screenshot 2024-05-23 123713.png" alt=""><figcaption><p>Screenshot showing ability to select your desired trigger</p></figcaption></figure>
