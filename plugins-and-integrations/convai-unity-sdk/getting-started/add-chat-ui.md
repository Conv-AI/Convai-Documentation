---
title: Add chat UI
description: >-
  Add the shipped chat transcript prefab to display scrolling conversation
  history on screen during character interactions.
last_reviewed: "4.4.0"
---

The Convai SDK for Unity includes a ready-made `ChatTranscriptUI` prefab that displays scrolling chat history in real time. The prefab includes its own `Canvas` — drag it into the scene, and it connects to `ConvaiManager` automatically.

## Chat history and captions

`ConvaiManager.ActiveManager.Transcripts` (`ConvaiTranscripts`) exposes two independent, combinable projections of a conversation: durable chat history and live speech-aligned captions. This page adds chat history using the shipped `ChatTranscriptUI` prefab. Captions use a separate, sample-only script with no shipped prefab — see [Chat and subtitle modes](../ui-and-presentation/transcript-ui/chat-and-subtitle-modes.md) to add captions or combine both displays in the same scene.

| Projection | Consumed by | Description |
| --- | --- | --- |
| Chat history | `ChatTranscriptUI` (shipped prefab, covered on this page) | Scrolling message bubbles — separate entries for player and character turns |
| Captions | `SubtitleTranscriptUI` (reference script, no shipped prefab) | A single caption block that updates as each turn streams, then auto-hides |

## Add the chat UI prefab

{% stepper %}
{% step %}
### Locate the prefab

In the Project window, navigate to:

```text
Packages/Convai SDK for Unity/Prefabs/TranscriptUI/TranscriptUI_Chat.prefab
```
{% endstep %}

{% step %}
### Drag the prefab into the scene

Drag `TranscriptUI_Chat.prefab` into the Hierarchy. The prefab includes its own `Canvas` — no separate `Canvas` setup is required.

The chat UI overlay appears in the Game view. The component finds `ConvaiManager` automatically when the scene starts — no manual wiring is needed.

{% hint style="warning" %}
The chat input field requires an `EventSystem` in the scene. If your scene does not already have one, add it via **GameObject > UI > Event System**.
{% endhint %}

{% hint style="warning" %}
If no `ConvaiManager` is found at startup, the Console logs: `[ChatTranscriptUI] No active ConvaiManager found.`. Check that `ConvaiManager` is in the scene.
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
