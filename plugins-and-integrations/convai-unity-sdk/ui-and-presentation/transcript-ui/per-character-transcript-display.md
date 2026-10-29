---
title: Per-character transcript display
last_reviewed: "5.0.0-preview"
description: Attach a text label to one character and choose whether it shows the latest conversation entry or the caption aligned with their speech.
---

Add `ConvaiTranscriptDisplay` when one text label should show one character's speech. It reads the room transcript facade and filters by the attached `ConvaiCharacter.CharacterId`. You need a configured character, an initialized `ConvaiManager`, and a TextMesh Pro label.

## Attach and configure the display

{% stepper %}
{% step %}
### Add the component to the character

Select the same `GameObject` that owns `ConvaiCharacter` and add **Convai → Convai Transcript Display**. The component requires a character on that object; it does not select a different character from elsewhere in the scene.
{% endstep %}
{% step %}
### Assign the text label

Assign **Transcript Text** to a `TMP_Text` component. A world-space label can sit above the character, while a screen-space label can sit in your existing Canvas. The Inspector shows **Ready** when a text reference exists; this does not verify a connection or incoming transcript data.
{% endstep %}
{% step %}
### Choose the display mode

Choose **Captions** for text as the character speaks, or **History** for the complete latest entry, including a reply still arriving. Captions is the default.

In Captions mode, **Clear After Seconds** sets a timeout after the last caption update. Its default `0` keeps text until another caption or an explicit clear. History ignores this timeout. Choose a positive timeout longer than the spoken lines you expect; it counts from the last update, not from audio completion.
{% endstep %}
{% step %}
### Verify one spoken reply

Enable the runtime Transcript setting, connect, and have the character speak. Confirm the label displays only that character's text. Toggle Transcript off and verify the label clears. Toggle it back on to replay the relevant retained entry or caption.
{% endstep %}
{% endstepper %}

## Change the display from code

`TranscriptText` exposes the assigned label; `Mode` selects `ConvaiTranscriptDisplayMode.History` or `.Captions`; `CurrentText` reads what is displayed. Setting `Mode` rebuilds the subscription. `Clear()` empties the label without changing history.

The component retries binding when the manager becomes available and resubscribes if the character ID changes. It renders plain text with rich text disabled. A caption cleared from history is removed immediately.

## Troubleshooting

| Symptom | Cause | Fix and verification |
| --- | --- | --- |
| Inspector shows Not set up | No text reference | Assign **Transcript Text** and confirm Ready |
| Ready but no text | Empty character ID, no matching speech, or Transcript disabled | Confirm the ID and presentation setting; test a reply |
| Text disappears mid-sentence | Caption timeout is shorter than the spoken line | Increase **Clear After Seconds** or use `0`; test a longer line |
| Clear seems temporary | A subsequent transcript update replaces the blank label | Disable the display or presentation when it should stay hidden |

## Next steps

{% content-ref url="chat-and-subtitle-modes.md" %}
[Chat and subtitle modes](chat-and-subtitle-modes.md)
{% endcontent-ref %}
