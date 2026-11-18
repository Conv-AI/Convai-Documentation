---
title: Chat and subtitle modes
last_reviewed: "5.0.0-pre.1"
description: >-
  Add scrolling chat history, live subtitle captions, or both to a scene, and
  configure how each transcript display looks and behaves.
---

`ConvaiManager.ActiveManager.Transcripts` (`ConvaiTranscripts`) exposes two independent views of a conversation: live speech-aligned captions and retained entry history. Use `ChatTranscriptUI` for chat history and a separate display for live captions. Both read from the same facade.

## Choose the displays you need

| Display | Facade members | Component |
| --- | --- | --- |
| Chat history | `CurrentTimeline`, `Subscribe`, `SubscribeFinalized` | `ChatTranscriptUI` |
| Speech captions | `CurrentCaptions`, `SubscribeCaptions` | `ConvaiTranscriptDisplay` per character or a custom room-wide display |

Both can run together. `Subscribe` receives `TranscriptChangeBatch`; `SubscribeFinalized` receives `TranscriptChange`; `SubscribeCaptions` receives `TranscriptCaption`. Subscription examples and replay options are in [Transcript history and queries](transcript-history-and-queries.md).

Both displays respect `IsPresentationEnabled`. Disabling Transcript hides presentation without clearing retained history. History can still be evicted by its retention limits. A custom subscriber must handle this visibility setting itself.

## Add chat history display

`ChatTranscriptUI` renders each turn as a message bubble in a scrollable list, with character and player turns in separate columns. Bubbles update while text arrives and can receive corrections even after an entry becomes final.

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

Connect to a character and speak. Character speech appears in one bubble column, player speech in the other, and the panel follows new messages while scrolled to the end.
{% endstep %}
{% endstepper %}

### `ChatTranscriptUI` inspector fields

| Field | Description |
| --- | --- |
| `scrollRect` | `ScrollRect` containing the message list. Required for auto-scroll |
| `chatContainer` | `RectTransform` that message bubble GameObjects are parented to |
| `characterMessagePrefab` | Template object instantiated for each character entry |
| `playerMessagePrefab` | Template object instantiated for each player entry |
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

`ChatTranscriptUI` colors a character bubble's sender name using that character's configured `NameTagColor` from `ConvaiCharacter`. To override this from script, call `bubble.SetSenderColor(Color)`.

Call `ChatTranscriptUI.ClearAll()` to clear the rendered message bubbles and reset the panel. This clears the visual display only — the underlying turn history in `ConvaiManager.ActiveManager.Transcripts.CurrentTimeline` is unaffected. A later replay can rebuild those bubbles. To remove retained data, use [ClearHistory](transcript-history-and-queries.md#export-and-clear-transcript-history).

## Gate chat input on availability

The chat field uses character availability, not transport connectivity alone. These Inspector fields control its feedback:

| Field | Default | Purpose |
| --- | --- | --- |
| **Gate Input On Availability** (`_gateInputOnAvailability`) | `true` | Disable input until the addressed character can receive it |
| **Notice Text** (`_noticeText`) | Unassigned | Optional label for a refused-message reason |
| **Refusal Notice Seconds** (`_refusalNoticeSeconds`) | `4` | How long the refusal label remains visible |
| **Slow Connect Hint Seconds** (`_slowConnectHintSeconds`) | `35` | When the prompt changes to the slower-connection wording; `0` disables it |

The configurable prompts cover no character, offline, connecting, connecting to a named character, slow connecting, preparing, ready, answering, and unavailable. `{0}` inserts the character name where applicable. A refusal keeps the typed message. Disabling the visual gate does not bypass `ConvaiPlayer`'s send checks.

In a group conversation, the chat field displays `Use push-to-talk to speak`. See [Conversation availability](../../features/conversation-availability/) for custom input controls.

## Add subtitle captions

For one character, attach the [Per-character transcript display](per-character-transcript-display.md) and select **Captions**. For a room-wide view, use `ConvaiManager.Transcripts.SubscribeCaptions` with the speaker or participant filters needed by your UI. The development repository’s custom transcript tutorial includes `SubtitleDialogTranscriptUI` and `TranscriptUI_SubtitleDialog.prefab` under `Assets/Convai/Tutorials/CustomTranscriptUI/`. The SDK package ships the chat prefabs.

Keep captions keyed by speaker and match the turn before clearing a cue. Remove a matching `Cleared` cue immediately. The display chooses how long to hold a completed caption. Caption changes can contain a full sentence. For replay, presentation visibility, and cleanup, see [Transcript API](../../scripting-reference/transcript-api.md).

## Plain text and font coverage

Chat bubbles disable rich text for both names and messages. `Use System Font Fallback` adds available device fonts to TextMesh Pro's fallback list. It does not add fonts in a WebGL player, so include suitable font assets for the languages your browser build needs. Device font availability does not guarantee complete language coverage.

## Feedback migration

The preview removes `FeedbackHandler`, `FeedbackButtons.prefab`, and the bubble methods `SetInteractionID`, `SetAgentRegistry`, and `SendFeedback`. Remove those references from copied chat prefabs and scripts. The prior local button behavior was not evidence that response feedback reached Convai. See [Transcript migration](../../scripting-reference/migrate-transcripts-to-5-0.md).

## Troubleshooting

| Symptom | Cause | Fix and verification |
| --- | --- | --- |
| `chatContainer is not assigned - messages will not display` | Missing message parent | Assign the container and send another message |
| `scrollRect is not assigned - auto-scroll will not work` | Missing scroll reference | Assign it and confirm a later message scrolls into view |
| The text field is disabled while connected | The addressed character is still preparing or unavailable | Inspect the availability prompt and wait for readiness; verify a message can be sent |
| A refusal has no visible explanation | No notice label is assigned | Assign **Notice Text**, retry, and confirm the message is retained alongside the reason |
| Captions do not appear | Missing text references or mismatched speaker filters | Assign the labels, clear filters, and test a spoken line |
| Both displays are hidden | Transcript presentation is disabled | Enable Transcript and confirm retained entries replay |
| Browser text contains missing glyph boxes | System font fallback is unavailable on WebGL | Include a TextMesh Pro font covering the required script and retest the build |

## Next steps

{% content-ref url="../customizing-ui-components.md" %}
[Customizing UI components](../customizing-ui-components.md)
{% endcontent-ref %}

{% content-ref url="per-character-transcript-display.md" %}
[Per-character transcript display](per-character-transcript-display.md)
{% endcontent-ref %}
