---
description: >-
  Build goal‑oriented conversation flows using sections, decisions, and triggers
  that move the story forward without rigid dialogue trees.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/convai-playground/character-customization/narrative-design
---

# Narrative Design

## Introduction

Narrative Design lets you guide a character with high‑level objectives while keeping conversations flexible. Instead of hard coding a tree of lines, you define goals and decision points, then allow the character to respond dynamically. This approach works for many domains such as games, learning and training simulations, tourism, retail assistants, and customer support kiosks. You can read more about the considerations behind Narrative Design [here.](https://convai.com/blog/convai-narrative-design)

<figure><img src="../../.gitbook/assets/image (17).png" alt=""><figcaption></figcaption></figure>

***

## Videos

Watch this series of videos to learn how to create a Narrative Design Graph in the Convai Playground.\
The demo features a Tour Guide scenario, showing step-by-step how to design, connect, and implement your own Narrative Design flow.

{% embed url="https://youtube.com/playlist?feature=shared&list=PLn_7tCx0Chip2mfSbOkqJLevEbm3jDuNV" %}

***

## Accessing Narrative Design

Open your character in the Convai Playground and select '**Narrative Design**' from the left sidebar. You will see a graph editor where you can connect the flow using nodes.

***

## Narrative Graph

A narrative graph is made of four building blocks:

## Sections

A Section contains:

* **Objectives** – The goal the character aims to achieve in this part of the narrative.\
  &#xNAN;_&#x45;xample:_ A virtual tour guide’s objective could be to welcome the user and ask if they want to begin the tour.
* **Decisions** – Choices based on user interaction that direct the character to different sections.\
  &#xNAN;_&#x45;xample:_ If the user says “yes” to a tour, the next section might start the tour route; if “no,” the character might offer alternative information.

{% hint style="warning" %}
Ensure decisions are clear and unambiguous; otherwise, the intended section may not be triggered.
{% endhint %}

Each Section has a **unique ID**.

<figure><img src="../../.gitbook/assets/image (19).png" alt=""><figcaption></figcaption></figure>

***

## Triggers

A trigger is a simple signal from your application indicating that a certain condition has been met. When fired, triggers advance the graph to the next connected section.

Each Trigger has a **unique ID**.

**Examples**

* **Location Based (Spatial):** your app detects the user entered a zone and fires the trigger associated with that Section.
* **Time Based:** a timer in your app expires and fires the trigger.
* **Event Based:** an in‑app event occurs such as “safety demo completed” and you fire the trigger.

<figure><img src="../../.gitbook/assets/image (20).png" alt=""><figcaption></figcaption></figure>

***

## Example Scenarios

To better understand how Narrative Design works in practice, here are two example characters you can explore directly in Convai Playground.\
Open each link, navigate to the **Narrative Design** tab, and review how the graph is structured with Sections and Triggers.

### Factory Tour Guide – [View Character](https://convai.com/pipeline/dashboard/character?id=8cd9fa0c-384b-11ef-a852-42010a7be00e)

A training simulation scenario set in a manufacturing facility.\
This character uses location-based triggers (e.g., entering the conveyor belt area or assembly line) to guide users through the workspace, explain safety protocols, and progress the tour.\
Ideal for **industrial training** and **onboarding simulations**.

<figure><img src="../../.gitbook/assets/image (17).png" alt=""><figcaption></figcaption></figure>

### Real Estate Home Tour Guide – [View Character](https://convai.com/pipeline/dashboard/character?id=4d31ce84-8c6a-11ef-bc7a-42010a7be011)

A real estate simulation where the character guides potential buyers through different rooms in a property.\
Similar to the factory example, it uses **location-based triggers** — for instance, when the user enters a specific room (e.g., kitchen, bathroom, bedroom), the corresponding Section in the Narrative Graph is triggered.\
This allows the character to dynamically adapt its dialogue to the user’s movement through the property.\
Useful for **virtual property tours**, **sales presentations**, and **customer onboarding**.

<figure><img src="../../.gitbook/assets/image (18).png" alt=""><figcaption></figcaption></figure>

***

## Syntax Instructions

These special characters can be added to nodes in your Narrative Design graph to control specific outcomes and behavior.

| Special Characters | Example                                      | Use                                                                                                                    |
| ------------------ | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| \<speak>           | \<speak> I'll say this exact line! \</speak> | Forces the character to respond exactly with the phrase inside the tags, without paraphrasing or adding extra context. |
| \*                 |                                              | Forces an immediate transition to the next node, bypassing further decision checks.                                    |
