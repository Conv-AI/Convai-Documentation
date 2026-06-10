---
title: Configure conversation input
description: Switch between push-to-talk and hands-free voice capture modes, tune VAD settings, and send text messages to a character without a microphone.
last_reviewed: "4.0.0-beta.21"
---

`UConvaiPlayerComponent` supports three input modes. Review the comparison below to choose the mode that fits your interaction design, then follow the tab for that mode.

## Input mode comparison

|  | Push-to-talk | Hands-free | Send text |
|---|---|---|---|
| **How it works** | Player holds a key to transmit voice. | Voice activity detection triggers automatically. | Text string sent directly to the chatbot. |
| **Best for** | Controlled input, game UX, shared-mic scenarios. | Ambient NPCs, kiosk installations, always-on experiences. | Accessibility features, text-chat UI, automated testing. |
| **Microphone required** | Yes | Yes | No |
| **Default** | Yes — `Enable Push to Talk` is `true` on `BP_ConvaiPlayerComponent` in the **Details** panel | No — disable **Enable Push to Talk** or call `UpdateVadBP(true)` | No — call `SendText()` as needed. |
| **Where to configure** | **Details** panel on `BP_ConvaiPlayerComponent` under the **Convai** category, or Blueprint nodes | Same **Details** panel — set **Enable Push to Talk** to `false`, or call `UpdateVadBP(true)` | Blueprint `SendText()` node |

## Configure your mode

On `BP_ConvaiPlayerComponent`, open the **Details** panel and expand the **Convai** category. The **Enable Push to Talk** checkbox controls the default input mode:

- **Enable Push to Talk** checked (`true`) — push-to-talk is active.
- **Enable Push to Talk** unchecked (`false`) — hands-free (VAD) mode is active.

You can change this in the **Details** panel without editing Blueprint graphs, or override it at runtime with Blueprint nodes as described in each tab below.

{% tabs %}
{% tab title="Push-to-talk" %}
Push-to-talk is the default mode. The player holds a key to stream voice input; releasing the key stops the stream.

`BP_ConvaiPlayerComponent` ships with push-to-talk input and a default talk key pre-wired in its Blueprint graph. To change the key, open the player pawn Blueprint, select **BP Convai Player Component**, and edit the input binding in the component's event graph — or replace the default binding with your own input action.

You can also set **Enable Push to Talk** to `true` in the **Details** panel under the **Convai** category to confirm push-to-talk mode is active.

To wire push-to-talk manually, call:

| Function | Returns | Description |
|---|---|---|
| `UnmuteStreamingAudio()` | `bool` — `true` if streaming started. | Begin streaming microphone audio to the active chatbot. Call on key press. |
| `MuteStreamingAudio()` | `void` | Stop streaming audio. Call on key release. |

Connect these to your input actions in the player pawn's Blueprint event graph.

You can also toggle mute without changing the mode: set the `bMute` property on `UConvaiPlayerComponent` to `true` to silence input and `false` to restore it.
{% endtab %}

{% tab title="Hands-free" %}
In hands-free mode the character listens continuously and responds whenever the player speaks, without requiring a key press.

Disable **Enable Push to Talk** on `BP_ConvaiPlayerComponent` in the **Details** panel under the **Convai** category, or call `UpdateVadBP(true)` from Blueprint — for example in the player pawn's **BeginPlay** event. This requires an attached audio-processing component (`ConvaiAudioProcessing`); `BP_ConvaiPlayerComponent` includes this wiring. The call returns `false` if the audio-processing component is missing.

To return to push-to-talk, enable **Enable Push to Talk** in the **Details** panel or call `UpdateVadBP(false)`.

You can still mute input programmatically regardless of the active mode: set the `bMute` property on `UConvaiPlayerComponent` to `true` to silence input and `false` to restore it.
{% endtab %}

{% tab title="Send text" %}
Use `SendText()` to send a text message to a chatbot without any microphone input. This is useful for text-chat interfaces, accessibility features, or testing character responses without audio hardware.

| Parameter | Type | Description |
|---|---|---|
| `ChatbotComponent` | `UConvaiConversationComponent` | Present in the function signature for API compatibility. The current implementation sends through this player component's active session and does not route by this parameter. |
| `Text` | `FString` | The text message to send. |

Connect a text input widget to this function and call it on submit. Ensure the player component has an active session with the target character before calling `SendText()`.
{% endtab %}
{% endtabs %}

## Fine-tune voice activity detection

Hands-free mode uses voice activity detection (VAD) to decide when the player has started and stopped speaking. The default VAD settings work in most environments. If the character fires on background noise or misses quiet speech, tune the `FConvaiVADSettings` struct.

### Access VAD settings

Use these Blueprint-callable functions from `UConvaiUtils` (no component reference required — call them as utility functions):

| Function | Category | Description |
|---|---|---|
| `GetVADSettings()` | `Convai\|Settings` | Returns the current `FConvaiVADSettings` struct. BlueprintPure. |
| `SetVADSettings(VADSettings)` | `Convai\|Settings` | Applies a new `FConvaiVADSettings` to the VAD pipeline. |

### VAD settings fields

| Field | Type | Default | Description |
|---|---|---|---|
| `bUseServerDefault` | `bool` | `true` | When `true`, the server's default VAD parameters are used and all other fields are ignored. Set to `false` to apply local overrides. |
| `Confidence` | `float` | `0.7` | Speech confidence threshold (0.0–1.0). Higher values require more certainty before the character begins listening. Raise this to reduce false triggers from background noise. |
| `StartSecs` | `float` | `0.2` | Seconds of continuous speech required before the listener activates. Increase to avoid triggering on very short sounds. |
| `StopSecs` | `float` | `2.2` | Seconds of silence before the listener closes the audio stream. Increase to avoid early cutoffs for speakers who pause mid-sentence. |
| `MinVolume` | `float` | `0.6` | Minimum audio level (0.0–1.0) that counts as speech. Raise this to filter out quiet ambient noise. |

{% hint style="info" %}
Set `bUseServerDefault` to `false` before assigning any other field — otherwise the server ignores all local values. You can also configure VAD defaults project-wide in **Edit > Project Settings > Plugins > Convai > Audio Settings | VAD** (available from plugin version 4.0.0-beta.20).
{% endhint %}

## Recording and state inspection

For workflows where you want to capture a complete audio clip before sending — rather than streaming in real time — use the recording API:

| Function | Returns | Description |
|---|---|---|
| `StartRecording()` | `void` | Begin recording microphone audio into a buffer. |
| `FinishRecording()` | `USoundWave*` | Stop recording and return the captured audio as a Sound Wave asset. |

You can process or play back the returned `USoundWave`, or pass it to other Blueprints. This path is separate from the streaming pipeline and does not interact with the active chatbot session.

To check streaming and recording state at any time:

| Function | Returns | Description |
|---|---|---|
| `GetIsStreaming()` | `bool` | `true` while audio is being streamed to a chatbot. |
| `GetIsRecording()` | `bool` | `true` while manual recording is in progress. |

For full details on the built-in chat overlay, the 3D in-world widget, and wiring a custom transcript UI, see [Add the chat UI](add-the-chat-ui.md).

## Troubleshooting

### Hands-free mode fires on background noise

**Symptom:** The character begins listening when no one is speaking — ambient sound, keyboard clicks, or music triggers it.

**Cause:** The VAD `Confidence` or `MinVolume` threshold is too low for the environment.

**Fix:** Call `GetVADSettings()`, set `bUseServerDefault` to `false`, raise `Confidence` (try `0.85`–`0.95`) and raise `MinVolume` above the default of `0.6` (try `0.7`–`0.8`), then apply with `SetVADSettings()`.

**Verify:** Enter Play mode in a quiet environment and confirm the character no longer triggers on ambient noise.

### Hands-free mode cuts off the player mid-sentence

**Symptom:** The character interrupts listening while the player is still speaking — common with speakers who pause between thoughts.

**Cause:** `StopSecs` is too short for the speaking style.

**Fix:** Call `GetVADSettings()`, set `bUseServerDefault` to `false`, increase `StopSecs` above the default of `2.2` (try `3.0`–`4.0` seconds), then apply with `SetVADSettings()`.

**Verify:** Speak with natural pauses and confirm the character waits for you to finish.

### Push-to-talk produces no response

**Symptom:** The player holds the key and speaks, but the character never responds.

**Cause:** `UnmuteStreamingAudio()` is not wired to the key press, or `bMute` is `true` on the player component.

**Fix:** Confirm your input action calls `UnmuteStreamingAudio()` on key press and `MuteStreamingAudio()` on key release. Confirm `bMute` is `false` in the **Details** panel.

**Verify:** Hold the push-to-talk key, speak, and confirm `GetIsStreaming()` returns `true`.

## Next steps

{% content-ref url="add-the-chat-ui.md" %}
[Add the chat UI](add-the-chat-ui.md)
{% endcontent-ref %}

{% content-ref url="validate-your-setup.md" %}
[Validate your setup](validate-your-setup.md)
{% endcontent-ref %}
