---
description: Transcript UI System - Integrate transcript UI with Convai's Unity plugin.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/utilities/transcript-ui-system
---

# Transcript UI System

## Overview

The Dynamic UI system is a feature within the Convai Unity SDK that provides developers a robust system for in-game communication. This feature allows for displaying messages from characters and players and supports various UI components for chat, Q\&A sessions, subtitles, and custom UI types. This document will guide you through the integration, usage, and creation of custom UI types of the Dynamic UI feature in your Unity project.

## Usage

### Accessing the Chat UI Handler

To interact with the chat system, you need to reference the `ConvaiChatUIHandler` in your scripts. You can find the Transcript UI prefab in the Prefabs folder.&#x20;

<figure><img src="../../../.gitbook/assets/image 1.png" alt="" width="338"><figcaption></figcaption></figure>

\
Here's an example of how to find and assign the handler:

```csharp
private ConvaiChatUIHandler _convaiChatUIHandler;

private void OnEnable()
{
    // Find and assign the ConvaiChatUIHandler component in the scene
    _convaiChatUIHandler = ConvaiChatUIHandler.Instance;
    if (_convaiChatUIHandler != null) _convaiChatUIHandler.UpdateCharacterList();
}
```

### Sending Messages

Once you have a reference to the `ConvaiChatUIHandler`, you can send messages using the following methods:

**Sending Player Text**

To send text as the player:

```csharp
_convaiChatUIHandler.SendPlayerText(input);
```

* `input`: The string containing the player's message.

### **Sending Character Text**

To send text as a character:

{% code overflow="wrap" %}
```csharp
_convaiChatUIHandler.SendCharacterText(characterName, currentResponseAudio.AudioTranscript.Trim());
```
{% endcode %}

* `characterName`: The name of the character sending the message.
* `currentResponseAudio.AudioTranscript`: The transcript of the audio response from the character, trimmed of any leading or trailing whitespace.

## Adding Custom UI Types to the Dynamic Chatbox

While the Dynamic UI system within the [SDK provides several pre-built UI types](convai-ui-prefabs.md), you may want to create a custom UI that better fits the style and needs of your game and it designed to be extensible, allowing developers to add their custom UI types. This is achieved by inheriting from the `ChatUIBase` class and implementing the required methods. The `ConvaiChatUIHandler` manages the different UI types and provides a system to switch between them.

### Creating a Custom UI Class

To create a custom UI type, follow these steps:

#### Step 1: Define Your Custom Class

Create a new C# script in your Unity project and define your class to inherit from `ChatUIBase`. For example:

```csharp
using Convai.Scripts.Utils;
using UnityEngine;

public class CustomChatUI : ChatUIBase
{
    // Implement the required methods from ChatUIBase here.
}
```

#### Step 2: Implement Required Methods

Implement the abstract methods from `ChatUIBase`. You must provide implementations for `Initialize`, `SendCharacterText`, and `SendPlayerText`:

{% code overflow="wrap" lineNumbers="true" %}
```csharp
public override void Initialize(GameObject uiPrefab)
{
    // Instantiate and set up your custom UI prefab here.
}

public override void SendCharacterText(string charName, string text, Color characterTextColor)
{
    // Handle sending character text to your custom UI here.
}

public override void SendPlayerText(string playerName, string text, Color playerTextColor)
{
    Handle sending player text to your custom UI here.
}
```
{% endcode %}

#### Step 3: Add Custom Functionality

Add any additional functionality or customization options that your custom UI may require.

#### Step 4: Assign and Use Your Custom UI

To use your custom UI class within the dictionary`ConvaiChatUIHandler`, you need to add it to the `GetUIAppearances` dictionary. This involves creating a prefab for your custom UI and assigning it in the `ConvaiChatUIHandler`.

Here's an example of how to do this:

1. Create a prefab for your custom UI and add your `CustomChatUI` component to it.
2. Assign the prefab to a public variable in the `ConvaiChatUIHandler` script.
3. Modify the `InitializeUIStrategies` method in the `ConvaiChatUIHandler` script to include your custom UI type.

{% code overflow="wrap" lineNumbers="true" %}
```csharp
[Tooltip (Prefab for the customChatUI.")]
public GameObject customChatUIPrefab;

private void InitializeUIStrategies()
{
    Existing UI types
    InitializeUI(chatBoxPrefab, UIType.ChatBox);
    InitializeUI(questionAnswerPrefab, UIType.QuestionAnswer);
    InitializeUI(subtitlePrefab, UIType.Subtitle);

    // Custom UI type
    InitializeUI(customChatUIPrefab, UIType.Custom); // Make sure to define UIType.Custom in the UIType enum
}

private void InitializeUI (GameObject uiPrefab, UIType uiType)
{
    // existing code...

    Add your custom UI initialization here
    if (uiType == UIType.Custom)
    {
        CustomChatUI customUIComponent = uiPrefab.GetComponent<CustomChatUI>();
        if (customUIComponent == null)
        {
            Debug.LogError("CustomChatUI component not found on prefab.");
            return;
        }

        customUIComponent.Initialize(uiPrefab);
        GetUIAppearances[uiType] = customUIComponent;
    }
}
```
{% endcode %}

4. Ensure that your custom UI type is added to the `UIType` enum:

```csharp
public enum UIType
{
    ChatBox,
    QuestionAnswer,
    Subtitle,
    CustomUI // Your custom UI type
}
```

5. Now you can set your custom UI type as the active UI from the Settings Panel [settings-panel.md](settings-panel.md "mention").

By following these steps, you can integrate your custom UI type into the Dynamic Chatbox system and switch between different UI types at runtime.



