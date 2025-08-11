---
description: >-
  A minimal from scratch example to get you familiar with the plugin main
  components.
---

# Simple Talking Cube

1.  Create a new first person project.\


    <div align="left"><figure><img src="../../../../.gitbook/assets/image (306).png" alt="" width="563"><figcaption></figcaption></figure></div>
2. Enable the Convai plugin and add the API key as [mentioned here](download-and-setup.md#set-up-your-project).\

3. Create a new Actor blueprint that we will be using as the AI character.\
   \
   ![](<../../../../.gitbook/assets/image (307).png>)![](<../../../../.gitbook/assets/image (311).png>)
4.  Open the created blueprint then search for and add the `Convai Chatbot` component in the components list. \
    \
    Note: if you do not find the component then ensure that you have properly installed and enabled the plugin by following the [Installation guide](download-and-setup.md#installing-the-plugin).\


    <div align="left"><figure><img src="../../../../.gitbook/assets/image (312).png" alt="" width="563"><figcaption></figcaption></figure></div>
5.  Select the created component and on the details panel, find the Character ID field and paste your character ID which you can get by creating a new character or using an existing one on the [Convai Playground](broken-reference).\


    <div align="left"><figure><img src="../../../../.gitbook/assets/image (314).png" alt="" width="563"><figcaption></figcaption></figure></div>
6.  Add a box component so that you can see the blueprint when placed in the scene.\


    <div align="left" data-full-width="false"><figure><img src="../../../../.gitbook/assets/image (313).png" alt="" width="563"><figcaption></figcaption></figure></div>
7.  Place the blueprint in the scene.\


    <div align="left"><figure><img src="../../../../.gitbook/assets/image (316).png" alt="" width="563"><figcaption></figcaption></figure></div>
8.  Open the player blueprint which by default in `First Person/Blueprints/BP_FirstPersonCharacter` for the first person template.\


    <div align="left"><figure><img src="../../../../.gitbook/assets/image (319).png" alt="" width="563"><figcaption></figcaption></figure></div>
9.  Search and add the `Convai Player` component in the components list.\


    <div align="left"><figure><img src="../../../../.gitbook/assets/image (321).png" alt="" width="563"><figcaption></figcaption></figure></div>
10. Add the following blueprint schematic to allow the player to talk to the AI character via the V key:

    1. Add a keyboard key event to be used as a push to talk button (i.e. the \`V\` key in this example).
    2. Use `Convai Get Looked At Character` to get the chatbot component of the character that is currently viewed by the player.
    3. Set `Radius` to a reasonable distance or zero if you want the player to be talk the character over an infinite distance.
    4. Set `Plane View` to true to only consider the plane axis (X & Y) and ignore the height axis (Z), this is made to prevent having to look directly at the pivot of the character, instead only looking in the direction of the character is sufficent.
    5. Use the `Start Talking` node from the `Convai Player` component initiates the talking session with the character, ensure you have enabled `Voice Response` to get the character to respond vocally.
    6. On the `Released` event, use the `Finish Talking` node on the `Convai Player` component to let the AI character know that we have finished talking and are now waiting for a response.\


    <div align="left"><figure><img src="../../../../.gitbook/assets/image (328).png" alt="" width="563"><figcaption></figcaption></figure></div>
11. Hit play, approach the AI character and push T to talk through the microphone, the character should then respond after releasing the T key.\


    <div align="left"><figure><img src="../../../../.gitbook/assets/image (323).png" alt="" width="563"><figcaption></figcaption></figure></div>

{% hint style="info" %}
If the character does not respond then make sure your microphone is set properly as the default microphone in the OS settings.
{% endhint %}

## Sending Text instead of Voice

Use the following `Send Text`  node instead if you want to text chat with the character instead of voice.&#x20;

Note, over here we use a hard coded string as input to the character, you will need to create the required UI to get the text input from the user and send it to the AI character.

<figure><img src="../../../../.gitbook/assets/image (327).png" alt=""><figcaption></figcaption></figure>
