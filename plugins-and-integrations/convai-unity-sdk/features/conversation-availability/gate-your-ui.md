---
title: Gate your UI on availability
description: Gate a custom chat field or microphone button on conversation availability so player input waits until a character can hear it.
last_reviewed: "5.0.0-preview"
---

Bind your own chat field, microphone button, or send action to `ConvaiManager.ConversationAvailability` so it only accepts input once the addressed character can actually hear it. Use this page when you are building custom input UI rather than using the shipped chat field, which already gates itself — see [Customise the chat field prompts](customise-chat-prompts.md) if that is what you are configuring.

## Prerequisites

- A scene with `ConvaiManager` and at least one active `ConvaiCharacter`. See [Scene components reference](../../getting-started/scene-components.md).
- Familiarity with the conversation availability states. See [How conversation availability works](how-availability-works.md).

## Read the current verdict

`ConvaiManager.ConversationAvailability` returns the current `ConvaiConversationAvailability` for `ConvaiManager.AddressedCharacter`. For a text-send button, combine availability with the group-room restriction. Keep the send call authoritative: `TrySendTextMessage` can still refuse if state changes between a UI refresh and the click.

```csharp
using Convai.Domain.DomainEvents.Session;
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.UI;

public class SendButtonGate : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;
    [SerializeField] private Button _sendButton;
    [SerializeField] private bool _groupConversationMode; // Match your app's connection mode.

    private void Update()
    {
        if (_sendButton == null) return;
        _sendButton.interactable = _manager != null &&
            !_groupConversationMode &&
            _manager.ConversationAvailability.CanAcceptPlayerInput();
    }
}
```

Set **Group Conversation Mode** to match the room your application connects. For runtime mode changes, update this application-owned state before accepting input. Do not infer it from internal SDK room fields.

## React to availability changes

`ConvaiManager.ConversationAvailabilityChanged` fires when the verdict changes. An event-based UI must also refresh on initialization and room-mode changes; the group text restriction can change independently of the availability value. The polling example above checks both every frame. A microphone button should call `ConvaiPushToTalkController.Press()` and display `BlockedReason` when refused rather than use the text-send gate.

## Gate on a specific character instead of the addressed one

A UI element tied to one particular character — a name plate, a per-character indicator in a multi-character scene — should read `ConvaiCharacter.ConversationAvailability` on that character directly, rather than `ConvaiManager.ConversationAvailability`, which always answers for whoever is currently addressed:

```csharp
[SerializeField] private ConvaiCharacter _character;
[SerializeField] private Image _indicator;

private void Update()
{
    _indicator.color = _character.CanAcceptPlayerInput ? Color.green : Color.gray;
}
```

{% hint style="warning" %}
`ConvaiCharacter.ConversationAvailability` is not the same as `ConvaiCharacter.IsCharacterReady`. `IsCharacterReady` is set once by the character-ready signal from Convai and does not clear when the character later loses its seat in the room. Use `ConversationAvailability` for anything that gates player input.
{% endhint %}

## Verify the gate

Enter Play mode, connect, and try to type or press send before the character has been confirmed. The gate should block the action until availability reports `Ready` or `Answering`. Disconnect the character mid-conversation and confirm the gate closes again. In a group room, confirm the text-send button stays disabled even in `Ready`.

## Next steps

{% content-ref url="local-player-activity.md" %}
[React to the player starting to speak](local-player-activity.md)
{% endcontent-ref %}

{% content-ref url="availability-reference.md" %}
[Conversation availability reference](availability-reference.md)
{% endcontent-ref %}
