# Narrative Design

## Introduction

Narrative Design enables game developers to outline high-level objectives for NPCs, thereby guiding the narrative flow without constraining it to traditionally rigid dialogue trees. This approach allows for similar behaviour as a state machine but with support for scripted as well as dynamic responses as the NPC progresses through the decision making process from interactions with the player or via triggers from the game state. You can read more about the considerations behind Narrative Design [here.](https://convai.com/blog/convai-narrative-design)

## Narrative Graph

<figure><img src="../../.gitbook/assets/image (355).png" alt=""><figcaption></figcaption></figure>

You can find this tool under the "Narrative Design" tab on the Convai [Playground](../playground-walkthrough.md).\
\
\
There are three fundamental elements to the graph, [Sections](narrative-design.md#sections), [Triggers ](narrative-design.md#triggers)and [Decisions](narrative-design.md#decisions).\


### Sections

<figure><img src="https://lh7-us.googleusercontent.com/deI0u_G_0x9SW1UXR_KrctHYu6EwhyI8Q-9zYfYD_WYJZbBFngMNX7nhZNGiSzpzTmti9BJEnO0Dtk9tSBfAV7vcl42Co9AFblg1bSlH4inaqFqZbTQUW3SPQ0sgtI_VZF_dHimLiHCihtFErYfU20E" alt=""><figcaption></figcaption></figure>

Sections consist of two components [Objectives ](narrative-design.md#objectives)and [Decisions](narrative-design.md#decisions); and each Section also has a unique ID for ease of reference and tracking.

#### Objectives

This defines the overarching goal that the character aims to fulfill. For example, the initial objective for a museum tour guide NPC, is to extend a warm welcome and inquire whether the player is interested in taking a guided tour.

#### Decisions

As the conversation unfolds, it becomes essential to adapt to the player's preferences and responses, adjusting the NPC's objectives accordingly. Decisions are critical in this context. Taking the tour guide example further, when the NPC poses the question about taking a tour, the player's affirmative or negative response will lead the NPC to pursue a different objective, tailored to the player's choice. Decisions lead to new sections and allow for the storyline or experience to progress.

<figure><img src="../../.gitbook/assets/image (358).png" alt=""><figcaption><p>In this example, you can see the the branching paths of a decision when the player tells the AI character their opinion on pineapple.</p></figcaption></figure>

{% hint style="info" %}
You can have a variety of decisions that result from the same Section, each with their own corresponding connection and new objective.
{% endhint %}

### Triggers

<figure><img src="../../.gitbook/assets/image (359).png" alt=""><figcaption><p>You can see a variety of trigger types in this example.</p></figcaption></figure>

There are three types of triggers currently: Spatial, Time-Based, and Event-Based. These are essential mechanisms that enable NPCs to discern when certain conditions have been met or events have occurred before proceeding to the next [Section.](narrative-design.md#sections) Each trigger has a unique ID for referencing and tracking.

#### Spatial

Spatial triggers are activated when characters or players are in the correct location in the experience. For example, standing in front of an information booth could be the Spatial trigger for the NPC to ask the player if they require assistance.

#### Time-Based

These triggers would occur after a set amount of time has elapsed. For example, if the player has not said anything or responded after a certain number of seconds, the character could repeat the question or inquire what was the delay. Adding more dimensions and natural engagement to the experience.

#### Event-Based

Event-based triggers correspond to events that occur in the experience or game engine that you would want the characters to respond to. For example, if there was an explosion event in the game, you could have that trigger responses and new Sections from the characters within the range of the explosion event.
