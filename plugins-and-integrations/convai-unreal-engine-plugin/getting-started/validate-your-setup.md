---
title: Validate your setup
description: Run through a checklist of plugin, component, audio, and API key checks to confirm your Convai Unreal Engine setup is working before adding features.
last_reviewed: "4.0.0-beta.21"
---

Use this page to confirm that every part of your Convai setup is working before you proceed to add features. Work through each section in order. A failure at any step usually points to a specific problem with a clear fix.

## Plugin check

| Check | How to verify |
|---|---|
| Plugin is enabled | Go to **Edit > Plugins**, search for `Convai`, and confirm the **Enabled** checkbox is checked. |
| Toolbar icon is visible | The Convai icon appears in the Unreal Editor toolbar after the plugin loads. |
| No load errors | The **Output Log** does not show errors mentioning `Convai` or `AudioCapture` on editor startup. |

## API key check

| Check | How to verify |
|---|---|
| Signed in | Open the Convai editor window (click the Convai toolbar icon) and confirm your account details are shown. |
| Key is stored | `UConvaiSettings.API_Key` is populated — readable under **Edit > Project Settings > Plugins > Convai**. |

If you are not signed in, see [Configure your API key](configure-api-key.md).

## Component check

| Check | How to verify |
|---|---|
| Character has Convai Chatbot | Open the character Blueprint and confirm `UConvaiChatbotComponent` appears in the **Components** panel. |
| Character ID is set | Select the **Convai Chatbot** component and confirm the **Character ID** field is non-empty and matches a character in your dashboard. |
| Player pawn has Convai Player | Open the player pawn Blueprint and confirm `UConvaiPlayerComponent` appears in the **Components** panel. |
| Face Sync is present (if using lip sync) | Confirm `UConvaiFaceSyncComponent` is in the character Blueprint and **Lip Sync Mode** is correct for your rig. |

## Audio check

| Check | How to verify |
|---|---|
| Microphone is available | Call `GetAvailableCaptureDeviceNames()` on the `UConvaiPlayerComponent` at runtime (for example in BeginPlay with a Print String node) and confirm the list is non-empty. |
| Default device opens | Enter Play mode and confirm that `GetIsStreaming()` returns `true` after triggering push-to-talk or enabling hands-free mode. |
| Android permission granted | On Android, confirm the `android.permission.RECORD_AUDIO` permission was requested and granted before starting a conversation. |

## Conversation check

Run this check after all others pass.

{% stepper %}
{% step %}
### Enter Play mode

Press **Play** in the Unreal Editor toolbar.
{% endstep %}

{% step %}
### Start a conversation

Hold push-to-talk (default: **T**) and speak a short phrase, then release. Alternatively, type a message in the chat widget and press **Enter**.
{% endstep %}

{% step %}
### Observe the character state

While you are speaking, `IsListening()` on `UConvaiChatbotComponent` returns `true`. While the character is generating a response, `IsProcessing()` ("Is Thinking") returns `true`. While the character is speaking, `GetIsTalking()` ("Is Talking") returns `true`.

Add **Print String** nodes in Blueprint connected to these functions to observe state transitions in the viewport.
{% endstep %}

{% step %}
### Confirm audio output

The character speaks an audible response. If lip sync is configured, the character's mouth moves in sync with the speech.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When validation passes, the character responds with audio and — if configured — lip sync. Proceed to the feature pages to add actions, emotions, dynamic context, and other capabilities.
{% endhint %}

## Common failure points

| Symptom | Likely cause | Fix |
|---|---|---|
| Character does not respond at all | API key not set, or Character ID missing | See [Configure your API key](configure-api-key.md); confirm the **Character ID** field on the Chatbot component. |
| No audio from character | Audio output device issue or session not started | Confirm `bAutoInitializeSession` is `true` on the Chatbot component, or call `StartSession()` manually. |
| Character does not hear the player | Microphone not captured, or Player component missing | Confirm `UConvaiPlayerComponent` is on the pawn; see [Configure the microphone](configure-microphone.md). |
| Lip sync does not play | Face Sync component missing or wrong lip sync mode | Add `UConvaiFaceSyncComponent` and set the correct `LipSyncMode` for your rig. |
| `OnFailureEvent` fires | Network error or invalid Character ID | Check the **Output Log** for details; verify network access and Character ID. |

## Next steps

{% content-ref url="configure-microphone.md" %}
[Configure the microphone](configure-microphone.md)
{% endcontent-ref %}

{% content-ref url="configure-character-audio.md" %}
[Configure character audio](configure-character-audio.md)
{% endcontent-ref %}

{% content-ref url="configure-conversation-input.md" %}
[Configure conversation input](configure-conversation-input.md)
{% endcontent-ref %}

{% content-ref url="add-chat-ui.md" %}
[Add the chat UI](add-chat-ui.md)
{% endcontent-ref %}
