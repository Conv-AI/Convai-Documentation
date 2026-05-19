---
description: >-
  Add a transcript UI component to display conversation text on screen during
  character interactions.
---

# Add Chat UI

## Display Conversation Transcripts in Your Scene

The Convai SDK for Unity includes a ready-made transcript UI prefab that displays conversation text in real time. Drop the prefab into a Canvas, assign your references, and the UI connects to the SDK automatically.

## Transcript Display Modes

The SDK supports three presentation modes for conversation text.

| Mode               | Identifier         | Description                                                                 |
| ------------------ | ------------------ | --------------------------------------------------------------------------- |
| **Chat**           | `"Chat"`           | Scrolling message bubbles — separate entries for player and character turns |
| **Subtitle**       | `"Subtitle"`       | Single text line at the bottom of the screen, replaced each turn            |
| **QuestionAnswer** | `"QuestionAnswer"` | Split display — question above, answer below                                |

***

## Add the Chat UI Prefab

{% stepper %}
{% step %}
**Locate the Prefab**

In the Project window, navigate to:

```
Packages/Convai SDK for Unity/Prefabs/TranscriptUI/TranscriptUI_Chat.prefab
```
{% endstep %}

{% step %}
**Add a Canvas**

If your scene does not have a Canvas, create one via **GameObject > UI > Canvas**. Unity also adds an **EventSystem** automatically — verify it exists, as the chat input field requires it.
{% endstep %}

{% step %}
**Drag the Prefab into the Canvas**

Drag `TranscriptUI_Chat.prefab` onto the **Canvas** in the Hierarchy.

The chat UI overlay appears in the Game view. The component finds `ConvaiManager` automatically when the scene starts — no manual wiring is needed.

{% hint style="warning" %}
If no `ConvaiManager` is found at startup, the Console logs: `[ChatTranscriptUI] Dependencies not injected - ensure ConvaiManager is present in scene`. Check that `ConvaiManager` is in the scene.
{% endhint %}
{% endstep %}
{% endstepper %}

***

## ChatTranscriptUI Inspector Fields

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

***

## Per-Character Subtitle Display

For per-character subtitle text (not scrolling chat), use `ConvaiTranscriptDisplay` instead. Add it to any GameObject with a `TextMeshPro` component and assign the character whose speech it should show.

**Inspector fields:**

| Field                     | Default      | Description                                              |
| ------------------------- | ------------ | -------------------------------------------------------- |
| `_transcriptText`         | _(required)_ | The `TMP_Text` component to write to                     |
| `_showPartialTranscripts` | `true`       | Display interim (non-final) speech results               |
| `_appendMode`             | `false`      | Append text instead of replacing each turn               |
| `_clearOnNewFinal`        | `true`       | Clear buffered text when a new final transcript arrives  |
| `_maxCharacters`          | `1000`       | Maximum characters stored in append mode (0 = unlimited) |

***

## Usage Examples

### Example 1: Full-Screen Chat Overlay in a Corporate Training Simulation

**Scenario:** A corporate onboarding experience displays a full-screen chat history so trainees can review everything the AI mentor said.

**Setup:**

* Add `TranscriptUI_Chat.prefab` to a full-screen Canvas set to **Screen Space - Overlay**
* Leave all references at prefab defaults

**Expected outcome:** Each turn appears as a new bubble — player text on the right, character text on the left. The list scrolls automatically as the conversation grows.

***

### Example 2: Subtitle Bar in a Medical Simulation

**Scenario:** A medical simulation uses a narrow subtitle bar at the bottom of the screen — minimizing screen real estate while still showing what the AI doctor says.

**Setup:**

* Create a small `RectTransform` anchored to the bottom of the Canvas
* Add `ConvaiTranscriptDisplay` to a `TextMeshPro` child inside it
* Set `_showPartialTranscripts`: `true` so the subtitle updates continuously as the character speaks

**Expected outcome:** A single line of text at the bottom updates in real time during character speech. When a new turn starts, the previous text clears automatically.

***

## Next Steps

With the transcript UI in place, add lip sync to drive character blendshapes from audio.

{% content-ref url="/broken/pages/ab42452535e8606c09d3fef04f1bc39471378bf3" %}
[Broken link](/broken/pages/ab42452535e8606c09d3fef04f1bc39471378bf3)
{% endcontent-ref %}
