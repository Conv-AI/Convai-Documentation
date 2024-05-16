---
description: >-
  Dive into the detailed guide to understand and utilize the properties that can
  be passed to your Chat Bubble component for enhanced customization and
  control.
---

# ChatBubble Props

In the ChatBubble component, there are three main properties:

1. A chatHistory property to determine whether to display the chat history.
2. A chatUiVariant property to specify the chat variant to display.
3. A set of properties returned by `useConvaiClient` which are essential for fetching user and NPC texts.

The set of properties that are mandatory to be returned by the useConvaiClient (You can follow the JavaScript SDK tutorial to set up your own custom useConvaiClient hook) for the Chat Bubble to work as expected are:

1. npcText : Stores the text returned by Npc.
2. userText: Stores the user text.
3. convaiClient: Stores the state of convai client and is used by Chat Bubble to set session Id.
4. keyPressed: Changes whenever the user presses the key and starts speaking.
5. characterId: Used by the chat bubble to store and retrieve chat history.
6. setUserText: Used by Chat Bubble component to reset the Chat History.
7. setNpcText: Used by the Chat Bubble component to reset the Chat History.
8. setEnter: Used by the textbox to send the textbox content to the client whenever the user press enter.

These are the properties that can be optionally passed by the custom useConvaiClient hook. If you are using the inbuilt useConvaiClient hook you can use these properties:

1. npcName: Name that will be shown on the chat UI for your character.
2. userName: Name that will represent user on the chat UI.
3. gender: Returns the gender of your avatar ( Can be used to set up animations).
4. avatar: Gives the model link of your avatar which can be used to load your 3D model to the scene.
5. actionText:  Returns the action text that represents the action Npc has been asked to perform.

There are 4 types of chat variants that you can choose from:

1. Toggle History Chat&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot (110).png" alt=""><figcaption><p>Toggle History Chat variant features a bottom panel, displaying only the current user and NPC text. It also includes a 'toggle chat history' button, allowing users to choose whether or not to display previous messages.</p></figcaption></figure>

2. Unified Compact Chat

<figure><img src="../../../.gitbook/assets/Screenshot (111).png" alt=""><figcaption><p>Unified Compact chat features a bottom left panel, where both the current messages and the chat history is displayed.</p></figcaption></figure>

3. Sequential Line Chat

<figure><img src="../../../.gitbook/assets/Screenshot (112).png" alt=""><figcaption><p>Sequential line chat version features a bottom panel where only a single line of the most recent output is displayed at a given time, maintaining a minimalist view.</p></figcaption></figure>

4. Expanded Side Chat

<figure><img src="../../../.gitbook/assets/Screenshot (113).png" alt=""><figcaption><p>'Expanded Side Chat' version closely resembles the 'Unified Compact Chat', but it features a larger, rectangular panel at the bottom left, providing a more spacious layout for your chat interactions.</p></figcaption></figure>
