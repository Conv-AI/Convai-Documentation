---
description: >-
  Configure Chat mode's scrollable message bubbles or Subtitle mode's
  auto-hiding overlay, switch between them at runtime, and add per-response
  feedback buttons to chat.
---

# Chat and Subtitle Modes

### Choosing Between Chat and Subtitle Display

The Convai Unity SDK ships two built-in transcript display modes. Chat mode accumulates a scrollable conversation history with sender-colored message bubbles and optional feedback buttons. Subtitle mode shows only the current speech segment at a fixed position and hides it automatically when the turn ends. Both modes are configurable, swappable at runtime, and replaceable with a custom `ITranscriptUI` implementation.

***

### Chat Mode vs. Subtitle Mode at a Glance

|                         | Chat                                                           | Subtitle                                               |
| ----------------------- | -------------------------------------------------------------- | ------------------------------------------------------ |
| **Layout**              | Scrollable list of message bubbles with sender labels          | Single centered text block with optional speaker label |
| **History**             | Full conversation retained on screen                           | No history — each turn replaces the previous           |
| **Auto-hide**           | Panel fades in/out with activity                               | Text disappears after a configurable delay             |
| **Partial transcripts** | Bubble updates word-by-word while speaking                     | Text updates word-by-word while speaking               |
| **Feedback buttons**    | Supported via `FeedbackButtons.prefab`                         | Not applicable                                         |
| **Built-in prefab**     | `TranscriptUI_Chat.prefab` (SDK)                               | `SubtitleTranscriptUI` (SamplesShared)                 |
| **Best for**            | Full conversation review, training debriefs, support scenarios | AR/VR overlays, kiosks, cinematic presentations        |

***

### Chat Mode

The chat panel renders each turn as a distinct message bubble in a vertically scrollable container. Character and player turns appear in separate bubble columns with sender-colored name labels. New bubbles update in real time during partial recognition and lock in when the turn completes.

#### `ChatTranscriptUI` Inspector Fields

| Field                    | Description                                                        |
| ------------------------ | ------------------------------------------------------------------ |
| `scrollRect`             | `ScrollRect` containing the message list. Required for auto-scroll |
| `chatContainer`          | `RectTransform` that message bubble GameObjects are parented to    |
| `characterMessagePrefab` | Prefab instantiated for each character turn                        |
| `playerMessagePrefab`    | Prefab instantiated for each player turn                           |
| `chatInputField`         | Optional `TMP_InputField` for typed text input mode                |
| `fadeDuration`           | Seconds for the panel's fade in/out animation (default `0.5`)      |
| `canvasFader`            | `CanvasFader` driving the fade animation                           |
| `canvasGroup`            | `CanvasGroup` controlling interactability during fades             |

#### `ChatMessageBubble` Inspector Fields

Each message bubble prefab must contain a `ChatMessageBubble` component at its root:

| Field       | Description                                      |
| ----------- | ------------------------------------------------ |
| `senderUI`  | `TextMeshProUGUI` displaying the speaker's name  |
| `messageUI` | `TextMeshProUGUI` displaying the transcript text |

The sender name is colored automatically from the character registry — each `ConvaiCharacter` in the scene receives a unique color assigned to its name tag. To override this in script: `bubble.SetSenderColor(Color)`.

#### Clearing the Chat Display

Call `ClearAll()` on `ChatTranscriptUI` to destroy all message bubbles and reset the panel. See [Transcript UI — Clearing the Transcript Display](/broken/pages/c52d4cb60535b8216ea991245fcc9f102eb1e88b#clearing-the-transcript-display) for access patterns and important caveats about the underlying turn history.

***

### Feedback on Chat Messages

Chat bubbles can include thumbs-up / thumbs-down feedback buttons that let users rate individual AI responses. This is useful in corporate training and support scenarios where response quality tracking matters.

{% stepper %}
{% step %}
**Add FeedbackButtons to Your Bubble Prefab**

Add `Packages/com.convai.convai-sdk-for-unity/Prefabs/TranscriptUI/FeedbackButtons.prefab` as a child of your character message bubble prefab. The prefab contains the feedback button visuals and a `FeedbackHandler` component.
{% endstep %}

{% step %}
**Ensure the Bubble Sets the Interaction ID**

`ChatTranscriptUI` calls `ChatMessageBubble.SetInteractionID(string)` automatically when the character turn contains an interaction ID from Convai. Without a valid ID, feedback submissions return `false` and the visual state does not change.
{% endstep %}

{% step %}
**Run Your Scene**

Rate a character response using the thumb buttons. The selected button highlights; the opposite button deactivates. `FeedbackHandler.ResetState()` resets both buttons to neutral when called.
{% endstep %}
{% endstepper %}

#### `ChatMessageBubble` Feedback API

| Method                                           | Description                                                                                                                        |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `SetInteractionID(string interactionID)`         | Required before feedback can be sent. Set automatically by `ChatTranscriptUI`                                                      |
| `SetAgentRegistry(IAgentRegistry agentRegistry)` | Required for character lookup. Injected automatically by `ChatTranscriptUI`                                                        |
| `bool SendFeedback(bool isPositiveFeedback)`     | Returns `true` if feedback was sent successfully. Returns `false` if `interactionID` is empty or the agent registry is unavailable |

`FeedbackHandler.ResetState()` deactivates both the positive and negative button fill visuals, returning the buttons to their neutral state.

{% hint style="info" %}
Feedback buttons are meaningful only for character message bubbles — player message bubbles do not receive interaction IDs. The visual state is local only; the feedback is sent to Convai for response quality tracking.
{% endhint %}

***

### Subtitle Mode

Subtitle mode shows a single block of text at a fixed screen position. When a turn completes, the text auto-hides after a configurable delay. Speaker name and color provide quick attribution without requiring a full bubble layout.

#### `SubtitleTranscriptUI` Inspector Fields

| Field               | Default | Description                                              |
| ------------------- | ------- | -------------------------------------------------------- |
| `subtitleText`      | —       | `TMP_Text` rendering the transcript content              |
| `speakerLabel`      | —       | `TMP_Text` rendering the speaker's name                  |
| `subtitleContainer` | —       | `GameObject` wrapping both text elements, toggled on/off |
| `fadeDuration`      | `0.3`   | Seconds for fade in/out animation                        |
| `canvasFader`       | —       | `CanvasFader` driving the fade animation                 |
| `canvasGroup`       | —       | `CanvasGroup` controlling interactability                |
| `autoHideDelay`     | `3.0`   | Seconds to wait after a turn completes before hiding     |

**Speaker label colors:**

* Character speech — cyan
* Player speech — green

{% hint style="warning" %}
`SubtitleTranscriptUI` is in `SamplesShared` and is provided as a reference implementation. Copy it into your own assembly before modifying it — changes to `SamplesShared` scripts are overwritten on SDK updates.
{% endhint %}

***

### Switching Modes

{% tabs %}
{% tab title="Settings Panel" %}
Users can switch between Chat and Subtitle at runtime using the built-in Settings Panel. The panel exposes a **Transcript Style** dropdown.

{% hint style="info" %}
The Settings Panel only exposes Chat mode in its dropdown by default. To activate Subtitle mode from the panel, switch it programmatically first (see the Scripting tab), then the panel will reflect the current state. See [Settings Panel](/broken/pages/370b1c4aa1c4466f3f070e13b5fd640823500165) for setup.
{% endhint %}
{% endtab %}

{% tab title="Scripting" %}
Switch modes through the runtime settings service. The `ConvaiRuntimeSettingsApplyResult` indicates whether the switch succeeded.

```csharp
using Convai.Runtime.Components;
using Convai.Shared.Types;
using UnityEngine;

public class ModeSwitcher : MonoBehaviour
{
    public void SwitchToSubtitle()
    {
        if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings))
        {
            var result = settings.Apply(new ConvaiRuntimeSettingsPatch
            {
                TranscriptMode = ConvaiTranscriptMode.Subtitle
            });

            if (!result.Success)
                Debug.LogWarning($"Mode switch failed: {result.ValidationMessage}");
        }
    }

    public void SwitchToChat()
    {
        if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings))
        {
            settings.Apply(new ConvaiRuntimeSettingsPatch
            {
                TranscriptMode = ConvaiTranscriptMode.Chat
            });
        }
    }
}
```

The patch is applied atomically — any field left `null` remains unchanged.
{% endtab %}
{% endtabs %}

***

### Usage Examples

#### Safety Training — Chat Mode with Post-Session Review

A workplace safety training simulation uses Chat mode so trainees can review the full AI instructor dialogue after completing a scenario:

* Use `TranscriptUI_Chat.prefab` in the scene Canvas
* Set `fadeDuration` to `0.3` for responsive transitions during active scenarios
* After each scenario ends, pause the simulation so the trainee can scroll through the full conversation
* Call `ClearAll()` on `ChatTranscriptUI` when starting a new scenario so stale messages do not carry over

At runtime, the trainee sees a persistent record of everything the AI instructor said, which they scroll through during the debrief before advancing to the next module.

#### Customer Service Training — Feedback Buttons for Response Quality

A customer service training simulation enables feedback buttons on AI character message bubbles so supervisors can flag high-quality or low-quality AI responses during session review:

* Add `FeedbackButtons.prefab` to the `characterMessagePrefab` used by `ChatTranscriptUI`
* Feedback buttons appear on every character bubble automatically
* `SetInteractionID` is set by the SDK — no additional code needed to enable the button behavior

At runtime, each AI response has thumbs-up / thumbs-down buttons. Supervisor ratings feed back to Convai to improve response quality over time.

#### Medical Simulation — Subtitle Mode for Clean Overlay

A procedural medical simulation uses Subtitle mode so the AI patient's speech appears as a clean overlay above the patient model without obscuring clinical readings on screen:

* Place `SubtitleTranscriptUI` with `subtitleContainer` anchored bottom-center
* Set `autoHideDelay` to `2.0` — quick clearance between patient responses keeps the screen uncluttered
* `speakerLabel` shows the patient's name when they speak; the container hides automatically between turns

At runtime, each patient response appears briefly as a subtitle and clears without accumulating history, keeping the simulation interface clean throughout the procedure.

***

### Troubleshooting

| Symptom                                                                                     | Likely Cause                                                           | Fix                                                                                                                      |
| ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `"[ChatTranscriptUI] chatContainer is not assigned - messages will not display"`            | `chatContainer` not wired in Inspector                                 | Assign the `RectTransform` that message bubbles should parent to                                                         |
| `"[ChatTranscriptUI] scrollRect is not assigned - auto-scroll will not work"`               | `scrollRect` not wired in Inspector                                    | Assign the `ScrollRect` component; auto-scroll absent but bubbles still appear                                           |
| `"[ChatTranscriptUI] Dependencies not injected - ensure ConvaiManager is present in scene"` | `ConvaiManager` missing or not initialized when chat UI `Start()` runs | Add `ConvaiManager` to the scene; ensure it initializes before `ChatTranscriptUI.Start()`                                |
| `"[ChatTranscriptUI] Cannot send message - dependencies not injected"`                      | Text typed in `chatInputField` but no player found                     | Ensure `ConvaiPlayer` is in the scene and `ConvaiManager` has initialized                                                |
| Feedback buttons do not highlight                                                           | `interactionID` not set or registry unavailable                        | Both are set by `ChatTranscriptUI` automatically — ensure `ConvaiManager` is initialized and the character is registered |
| Subtitle text not disappearing                                                              | `autoHideDelay` value too high                                         | Reduce `autoHideDelay` in the `SubtitleTranscriptUI` Inspector                                                           |
| Subtitle mode not activating                                                                | No `SubtitleTranscriptUI` in scene with `Identifier == "Subtitle"`     | Add the sample or a custom `ITranscriptUI` with `Identifier = "Subtitle"`                                                |

***

### Next Steps

You have configured Chat or Subtitle display and can switch between them at runtime. For customizing the visual appearance of bubbles or building a fully custom transcript UI, see Customizing UI Components. To give users control over which mode is active, see the Settings Panel.

{% content-ref url="/broken/pages/106f10287b1cd8acd8da84d129861df8161489a7" %}
[Broken link](/broken/pages/106f10287b1cd8acd8da84d129861df8161489a7)
{% endcontent-ref %}

{% content-ref url="/broken/pages/370b1c4aa1c4466f3f070e13b5fd640823500165" %}
[Broken link](/broken/pages/370b1c4aa1c4466f3f070e13b5fd640823500165)
{% endcontent-ref %}
