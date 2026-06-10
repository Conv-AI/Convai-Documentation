---
title: Add chat UI
description: >-
  Add a transcript UI component to display conversation text on screen during
  character interactions.
last_reviewed: "4.2.0"
---

The Convai SDK for Unity includes a ready-made transcript UI prefab that displays conversation text in real time. The prefab includes its own Canvas — drag it into the scene, and the UI connects to the SDK automatically.

## Transcript display modes

The SDK supports three presentation modes for conversation text.

| Mode               | Identifier         | Description                                                                 |
| ------------------ | ------------------ | --------------------------------------------------------------------------- |
| **Chat**           | `"Chat"`           | Scrolling message bubbles — separate entries for player and character turns |
| **Subtitle**       | `"Subtitle"`       | Single text line at the bottom of the screen, replaced each turn            |
| **QuestionAnswer** | `"QuestionAnswer"` | Split display — question above, answer below                                |

## Add the chat UI prefab

{% stepper %}
{% step %}
### Locate the prefab

In the Project window, navigate to:

```
Packages/Convai SDK for Unity/Prefabs/TranscriptUI/TranscriptUI_Chat.prefab
```
{% endstep %}

{% step %}
### Drag the prefab into the scene

Drag `TranscriptUI_Chat.prefab` into the Hierarchy. The prefab includes its own Canvas — no separate Canvas setup is required.

The chat UI overlay appears in the Game view. The component finds `ConvaiManager` automatically when the scene starts — no manual wiring is needed.

{% hint style="warning" %}
The chat input field requires an **EventSystem** in the scene. If your scene does not already have one, add it via **GameObject > UI > Event System**.
{% endhint %}

{% hint style="warning" %}
If no `ConvaiManager` is found at startup, the Console logs: `[ChatTranscriptUI] Dependencies not injected - ensure ConvaiManager is present in scene`. Check that `ConvaiManager` is in the scene.
{% endhint %}
{% endstep %}
{% endstepper %}

## ChatTranscriptUI Inspector fields

If you need to customize the layout, select the prefab instance and inspect the `ChatTranscriptUI` component.

**UI References:**

| Field                    | Type             | Description                                             |
| ------------------------ | ---------------- | ------------------------------------------------------- |
| `scrollRect`             | `ScrollRect`     | The scroll container for the message list               |
| `chatContainer`          | `RectTransform`  | Parent transform where message bubbles are instantiated |
| `characterMessagePrefab` | `GameObject`     | Template for character speech bubbles                   |
| `playerMessagePrefab`    | `GameObject`     | Template for player speech bubbles                      |
| `chatInputField`         | `TMP_InputField` | Text field for typed input (optional)                   |

**Fade Settings:**

| Field          | Default | Description                         |
| -------------- | ------- | ----------------------------------- |
| `fadeDuration` | `0.5`   | Seconds for fade-in/out transitions |

{% hint style="warning" %}
If `chatContainer` is not assigned, messages will not appear and the Console logs: `[ChatTranscriptUI] chatContainer is not assigned - messages will not display`. The bundled prefab has all references pre-wired.
{% endhint %}

## Usage examples

### Example 1: Full-screen chat overlay in a corporate training simulation

**Scenario:** A corporate onboarding experience displays a full-screen chat history so trainees can review everything the AI mentor said.

**Setup:**

* Drag `TranscriptUI_Chat.prefab` into the Hierarchy
* Leave all references at prefab defaults

**Expected outcome:** Each turn appears as a new bubble — player text on the right, character text on the left. The list scrolls automatically as the conversation grows.

## Next steps

With the transcript UI in place, add lip sync to drive character blendshapes from audio.

{% content-ref url="add-lip-sync/README.md" %}
[Add lip sync](add-lip-sync/README.md)
{% endcontent-ref %}
