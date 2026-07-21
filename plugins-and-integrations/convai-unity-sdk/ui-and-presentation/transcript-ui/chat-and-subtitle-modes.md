---
title: Chat and subtitle modes
last_reviewed: "4.4.0"
description: >-
  Add scrolling chat history, live subtitle captions, or both to a scene, and
  configure how each transcript display looks and behaves.
---

`ConvaiManager.ActiveManager.Transcripts` (`ConvaiTranscripts`) exposes two independent views of a conversation: live speech-aligned captions and durable turn history. This page covers adding `SubtitleTranscriptUI` for captions, `ChatTranscriptUI` for history, or both — the two read from the same facade and update independently, so adding one does not remove or replace the other.

## Choose the projections you need

| Projection | Facade members | Consumed by | Best for |
| --- | --- | --- | --- |
| Captions | `CurrentCaptions`, `CaptionsChanged`, `SubscribeCaptions(...)` | `SubtitleTranscriptUI` (reference script) | Low-latency, speech-aligned text. Ephemeral — not stored as chat history |
| Timeline | `CurrentTimeline`, `Changed`, `Subscribe(...)`, `SubscribeCommitted(...)` | `ChatTranscriptUI` (shipped component) | Durable, scrollable conversation history for review, replay, or export |

There is no single mode switch that activates one projection at the expense of the other. A custom component can subscribe to either projection, or both, from `ConvaiManager.ActiveManager.Transcripts` directly:

```csharp
using System;
using Convai.Domain.Models;
using Convai.Runtime.Components;
using UnityEngine;

public class TranscriptProjectionExample : MonoBehaviour
{
    private IDisposable _captionSubscription;
    private IDisposable _historySubscription;

    private void OnEnable()
    {
        if (!ConvaiManager.ActiveManager.TryGetTranscripts(out ConvaiTranscripts transcripts)) return;

        // Low-latency captions for an on-screen subtitle
        _captionSubscription = transcripts.SubscribeCaptions(OnCaption);

        // Durable turn history for a scrollable chat log
        _historySubscription = transcripts.Subscribe(
            OnHistoryChange,
            new TranscriptSubscriptionOptions { ReplayExisting = true });
    }

    private void OnDisable()
    {
        _captionSubscription?.Dispose();
        _historySubscription?.Dispose();
    }

    private void OnCaption(TranscriptCaption caption) { /* update subtitle text */ }
    private void OnHistoryChange(TranscriptChange change) { /* update chat bubble */ }
}
```

Both shipped display components also respect `ConvaiTranscripts.IsPresentationEnabled`. When the Settings Panel's `Transcript` toggle is off, or a `ConvaiRuntimeSettingsPatch` sets `TranscriptEnabled = false`, `ChatTranscriptUI` and `SubtitleTranscriptUI` both stop rendering — but `CurrentTimeline` keeps recording. Turning display off does not discard history.

## Add chat history display

`ChatTranscriptUI` renders each turn as a message bubble in a scrollable list, with character and player turns in separate columns. Bubbles update in real time while a turn streams and lock in once the turn commits.

{% stepper %}
{% step %}
### Add the prefab to your scene

Drag `TranscriptUI_Chat.prefab` into the scene. Find it at `Prefabs/TranscriptUI/TranscriptUI_Chat.prefab` in the <code class="expression">space.vars.sdk_package_id</code> package. The prefab includes its own `Canvas` — do not nest it inside an existing `Canvas`.

`ChatTranscriptUI` looks up `ConvaiManager.ActiveManager` automatically and calls `Subscribe(...)` on `ConvaiManager.ActiveManager.Transcripts` once it is found. No manual registration is required.
{% endstep %}

{% step %}
### Ensure an EventSystem exists

The chat input field requires an `EventSystem` in the scene. If your scene does not have one, add it via **GameObject → UI → Event System**.
{% endstep %}

{% step %}
### Run your scene

Connect to a character and speak. Character speech appears in one bubble column, player speech in the other, and the panel auto-scrolls to the latest message.
{% endstep %}
{% endstepper %}

### `ChatTranscriptUI` inspector fields

| Field | Description |
| --- | --- |
| `scrollRect` | `ScrollRect` containing the message list. Required for auto-scroll |
| `chatContainer` | `RectTransform` that message bubble GameObjects are parented to |
| `characterMessagePrefab` | Prefab instantiated for each character turn |
| `playerMessagePrefab` | Prefab instantiated for each player turn |
| `chatInputField` | Optional `TMP_InputField` for typed text input |
| `fadeDuration` | Seconds for the panel's fade in/out animation (default `0.5`) |
| `canvasFader` | `CanvasFader` driving the fade animation |
| `canvasGroup` | `CanvasGroup` controlling interactability during fades |

### `ChatMessageBubble` inspector fields

Each message bubble prefab must contain a `ChatMessageBubble` component at its root:

| Field | Description |
| --- | --- |
| `senderUI` | `TextMeshProUGUI` displaying the speaker's name |
| `messageUI` | `TextMeshProUGUI` displaying the transcript text |

`ChatTranscriptUI` colors a character bubble's sender name using that character's configured `NameTagColor` (from `ConvaiCharacter` or its character config asset). To override this from script, call `bubble.SetSenderColor(Color)`.

Call `ChatTranscriptUI.ClearAll()` to destroy all rendered message bubbles and reset the panel. This clears the visual display only — the underlying turn history in `ConvaiManager.ActiveManager.Transcripts.CurrentTimeline` is unaffected. See [Transcript UI — Clear the transcript display](./#clear-the-transcript-display) for the caveats.

## Add subtitle captions

`SubtitleTranscriptUI` shows a single block of text at a fixed position, driven by `SubscribeCaptions`. When a caption finalizes, the text auto-hides after a configurable delay.

{% hint style="warning" %}
`SubtitleTranscriptUI` ships as a script only — there is no companion prefab. It is a reference implementation in `SamplesShared`; copy it into your own assembly before modifying it, since `SamplesShared` scripts are overwritten on SDK updates.
{% endhint %}

{% stepper %}
{% step %}
### Add the script to a UI GameObject

Add `SubtitleTranscriptUI` (from `Scripts/UI/Transcript/Subtitle/SubtitleTranscriptUI.cs` in `SamplesShared`) to a `GameObject` under a `Canvas`. Create or reuse two `TMP_Text` elements for the caption body and speaker name, plus a container `GameObject` to toggle visibility.
{% endstep %}

{% step %}
### Wire the inspector fields

Assign `subtitleText`, `speakerLabel`, and `subtitleContainer`. Add a `CanvasFader` and `CanvasGroup` if you want fade transitions.
{% endstep %}

{% step %}
### Run your scene

Speak, or have a character speak. The caption fades in, updates word-by-word while the turn streams, and hides `autoHideDelay` seconds after the turn finalizes.
{% endstep %}
{% endstepper %}

### `SubtitleTranscriptUI` inspector fields

| Field | Default | Description |
| --- | --- | --- |
| `subtitleText` | — | `TMP_Text` rendering the caption body |
| `speakerLabel` | — | `TMP_Text` rendering the speaker's name |
| `subtitleContainer` | — | `GameObject` wrapping both text elements, toggled on/off |
| `fadeDuration` | `0.3` | Seconds for fade in/out animation |
| `canvasFader` | — | `CanvasFader` driving the fade animation |
| `canvasGroup` | — | `CanvasGroup` controlling interactability |
| `autoHideDelay` | `3.0` | Seconds to wait after a caption finalizes before hiding |

**Filters:**

| Field | Default | Description |
| --- | --- | --- |
| `finalOnly` | `false` | When `true`, only finalized captions are shown; streaming text is skipped |
| `filterBySpeakerType` | `false` | When `true`, restrict captions to `speakerType` |
| `speakerType` | `Character` | `TranscriptSpeakerType` to filter by when `filterBySpeakerType` is on (`Player`, `Character`, or `System`) |
| `speakerIdFilter` | — | Restrict captions to a specific speaker ID |
| `participantIdFilter` | — | Restrict captions to a specific room participant ID (multi-user rooms) |

**Speaker label colors:** Character speech — cyan; player speech — green.

## Add feedback buttons to chat messages

Chat bubbles can include thumbs-up / thumbs-down feedback buttons that let users rate individual AI responses.

{% stepper %}
{% step %}
### Add FeedbackButtons to your bubble prefab

Add `FeedbackButtons.prefab` as a child of your character message bubble prefab. Find it at `Prefabs/TranscriptUI/FeedbackButtons.prefab` in the <code class="expression">space.vars.sdk_package_id</code> package. The prefab contains the feedback button visuals and a `FeedbackHandler` component.
{% endstep %}

{% step %}
### Set the interaction ID before the user can rate a message

Call `ChatMessageBubble.SetInteractionID(string)` for the turn you want to make ratable. The interaction ID is available from `ConvaiManager.ActiveManager.Events.OnInteractionCreated` (`InteractionCreated.InteractionId`, keyed by `CharacterId`).
{% endstep %}

{% step %}
### Run your scene

Rate a character response using the thumb buttons. The selected button highlights; the opposite button deactivates. `FeedbackHandler.ResetState()` resets both buttons to neutral when called.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
No shipped component calls `ChatMessageBubble.SetInteractionID(string)` automatically. Until your code calls it for a turn, `ChatMessageBubble.SendFeedback(bool)` returns `false` and the buttons never highlight for that message.
{% endhint %}

### `ChatMessageBubble` feedback API

| Method | Description |
| --- | --- |
| `SetInteractionID(string interactionID)` | Required before feedback can be sent for this bubble |
| `SetAgentRegistry(IAgentRegistry agentRegistry)` | Required for character lookup. Injected automatically by `ChatTranscriptUI` |
| `bool SendFeedback(bool isPositiveFeedback)` | Returns `true` if `interactionID` is set and the character is found in the agent registry. Returns `false` otherwise |

`FeedbackHandler.ResetState()` deactivates both the positive and negative button fill visuals, returning the buttons to their neutral state. Feedback buttons are relevant only for character message bubbles — player bubbles do not receive interaction IDs.

## Usage examples

### Safety training — chat history for post-session review

A workplace safety training simulation uses chat history so trainees can review the full AI instructor dialogue after completing a scenario:

* Drag `TranscriptUI_Chat.prefab` into the scene `Canvas`
* Set `fadeDuration` to `0.3` for responsive transitions during active scenarios
* Call `ChatTranscriptUI.ClearAll()` when a new scenario starts so stale messages do not carry over

At runtime, the trainee sees a persistent record of everything the AI instructor said and scrolls through it during the debrief before advancing to the next module.

### Medical simulation — subtitle captions for a clean overlay

A procedural medical simulation uses subtitle captions so the AI patient's speech appears as a clean overlay above the patient model without obscuring clinical readings on screen:

* Add `SubtitleTranscriptUI` with `subtitleContainer` anchored bottom-center
* Set `autoHideDelay` to `2.0` — quick clearance between patient responses keeps the screen uncluttered
* Leave `filterBySpeakerType` off so both the patient's and the trainee's speech appear as captions

At runtime, each patient response appears briefly as a caption and clears without accumulating history, keeping the simulation interface clean throughout the procedure.

### Museum kiosk — captions and history running together

A natural history museum runs an exhibit screen for visitors and a separate docent review station, both driven by the same conversation:

* Add `SubtitleTranscriptUI` to the exhibit screen's `Canvas`, with `filterBySpeakerType` on and `speakerType` set to `Character`, so only the exhibit character's speech becomes a caption
* Add `TranscriptUI_Chat.prefab` to the docent station's `Canvas`
* Both read from the same `ConvaiManager.ActiveManager.Transcripts` and update independently — no per-mode configuration is required

At runtime, visitors see clean rolling captions at the exhibit while the docent station accumulates the full conversation for review, from a single session.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `[ChatTranscriptUI] chatContainer is not assigned - messages will not display` | `chatContainer` not wired in Inspector | Assign the `RectTransform` that message bubbles should parent to |
| `[ChatTranscriptUI] scrollRect is not assigned - auto-scroll will not work` | `scrollRect` not wired in Inspector | Assign the `ScrollRect` component; auto-scroll is absent but bubbles still appear |
| `[ChatTranscriptUI] No active ConvaiManager found.` | `ConvaiManager` missing or not yet initialized | Add `ConvaiManager` to the scene and confirm it initializes before this component looks it up |
| `[ChatTranscriptUI] Cannot send message - dependencies not injected` | Text typed in `chatInputField` before dependencies were injected | Ensure `ConvaiManager` and a `ConvaiPlayer` are present and initialized in the scene |
| `[SubtitleTranscriptUI] No active ConvaiManager found.` | Same cause as above, for the subtitle script | Add `ConvaiManager` to the scene |
| Captions never appear | No component is calling `SubscribeCaptions` in the scene, or the caption's speaker does not match the configured filters | Add `SubtitleTranscriptUI`, confirm its `TMP_Text` fields are assigned, and check `filterBySpeakerType`/`speakerIdFilter`/`participantIdFilter` |
| Neither chat nor subtitle display updates | `ConvaiTranscripts.IsPresentationEnabled` is `false` | Check the Settings Panel's `Transcript` toggle, or apply `TranscriptEnabled = true` through a `ConvaiRuntimeSettingsPatch` |
| Feedback buttons never highlight | `SendFeedback` is returning `false` | Confirm your code calls `ChatMessageBubble.SetInteractionID(string)` for that turn — no shipped component does this automatically |

## Next steps

You have added chat history display, subtitle captions, or both, and wired feedback buttons on chat messages. For customizing the visual appearance of bubbles or building a fully custom transcript display, see Customizing UI Components. For letting users show or hide transcript display at runtime, see the Settings Panel.

{% content-ref url="../customizing-ui-components.md" %}
[customizing-ui-components.md](../customizing-ui-components.md)
{% endcontent-ref %}

{% content-ref url="../settings-panel/" %}
[settings-panel](../settings-panel/)
{% endcontent-ref %}

{% content-ref url="transcript-history-and-queries.md" %}
[transcript-history-and-queries.md](transcript-history-and-queries.md)
{% endcontent-ref %}
