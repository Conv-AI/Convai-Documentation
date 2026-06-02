---
title: Configure conversation input
description: Switch between push-to-talk and hands-free voice capture on UConvaiPlayerComponent, and send text messages without a microphone.
last_reviewed: "4.0.0-beta.21"
---

`UConvaiPlayerComponent` supports two voice capture modes and a text input path. Choose the mode that fits your interaction design before entering Play mode.

## Push-to-talk (default)

In push-to-talk mode the player holds a key to transmit voice input. This is the default behavior when `UConvaiPlayerComponent` is added to a pawn.

The built-in chat widget provided by `BP_ConvaiPlayerComponent` and `BP_ConvaiSamplePlayer` binds push-to-talk to a default key. You can replace this with any input action in your Blueprint by calling:

| Function | Effect |
|---|---|
| `UnmuteStreamingAudio()` | Begin streaming microphone audio to the active chatbot. Call on key press. |
| `MuteStreamingAudio()` | Stop streaming audio. Call on key release. |

Both functions return `bool`. `UnmuteStreamingAudio()` returns `true` if streaming started successfully. Connect them to your input actions in your player pawn's Blueprint event graph.

## Hands-free mode (voice activity detection)

In hands-free mode the character listens continuously and responds whenever the player speaks, without requiring a key press.

To enable hands-free mode:

1. Select the **Convai Player** component on your player pawn.
2. In the **Details** panel, locate **Push to Talk** under the **Convai** category and disable it.

Alternatively, call `UpdateVadBP(true)` from Blueprint to enable voice activity detection at runtime.

You can also toggle mute programmatically without changing the VAD mode. Set the `bMute` property to `true` to silence input and `false` to restore it.

## Send text without a microphone

Use `SendText()` to send a text message to a chatbot without any microphone input. This is useful for text-chat interfaces, accessibility features, or testing character responses without audio hardware.

```
SendText(ChatbotComponent, Text)
```

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiConversationComponent` | Reference to the target `UConvaiChatbotComponent` |
| `Text` | `FString` | The text message to send |

Connect a text input widget to this function and call it on submit.

## Chat UI styles

The `BP_ConvaiPlayerComponent` and `BP_ConvaiSamplePlayer` ship a built-in chat widget. The **Convai Player** component's **Details** panel exposes an **Interface Selection** property with three style options (values 1, 2, and 3). Switch between them to change the visual appearance of the chat overlay without replacing the widget Blueprint.

## Recording audio manually

For workflows where you want to capture a complete audio recording before sending it (rather than streaming in real time), use the recording API:

| Function | Returns | Description |
|---|---|---|
| `StartRecording()` | void | Begin recording microphone audio into a buffer |
| `FinishRecording()` | `USoundWave*` | Stop recording and return the captured audio as a Sound Wave |

You can then process or play back the `USoundWave`, or pass it to other Blueprints. This path is separate from the streaming pipeline and does not interact with the active chatbot session.

## Check streaming and recording state

| Function | Returns | Description |
|---|---|---|
| `GetIsStreaming()` ("Is Streaming") | `bool` | `true` while audio is being streamed to a chatbot |
| `GetIsRecording()` ("Is Recording") | `bool` | `true` while manual recording is in progress |

## Next steps

- [Configure the microphone](configure-microphone.md) — select a capture device or adjust volume.
- [Validate your setup](validate-your-setup.md) — confirm that voice input is reaching the character.
