---
title: Add the chat UI
description: Add the built-in chat overlay to your scene, switch between interface styles, attach the 3D in-world widget to a character, or replace it with a custom widget.
last_reviewed: "4.0.0-beta.21"
---

The Convai plugin ships two chat UI options: a screen-space overlay that appears in the viewport, and a 3D in-world panel that floats above a character in the level. Both display conversation transcripts and push-to-talk feedback. The overlay is bundled into `BP_ConvaiPlayerComponent`; the 3D panel is a separate component you add when needed.

## Screen-space overlay

The screen-space overlay is included in `BP_ConvaiPlayerComponent`. When you added `BP Convai Player Component` to your player pawn (see [Add your first Convai character](add-your-first-character.md)), the widget was already included. It appears automatically in Play mode — no additional setup is required.

### Switch the overlay style

The built-in overlay is the `Chat_WB` widget (`Content/Widgets/Chat_WB`). `BP_ConvaiPlayerComponent` exposes a `UISelection` variable that selects which overlay style the widget switcher displays. Three background textures ship with the plugin: `UI_CBFV1`, `UI_CBFV2`, and `UI_CBFV3` in `Content/Widgets/Images/`.

To change the style:

1. Select the **Convai Player** component in your player pawn Blueprint.
2. In the **Details** panel, find `UISelection` under the **Convai** category. This variable is defined on `BP_ConvaiPlayerComponent` — it does not appear on the bare `UConvaiPlayerComponent` C++ component.
3. Set `UISelection` to `1`, `2`, or `3` to switch styles. Set it to `0` to hide the overlay entirely.

| Value | Effect |
|---|---|
| `0` | Overlay hidden — no screen-space chat widget is shown. |
| `1` | Style 1 — uses the `UI_CBFV1` background texture. |
| `2` | Style 2 — uses the `UI_CBFV2` background texture. |
| `3` | Style 3 — uses the `UI_CBFV3` background texture. |

All styles display the same conversation data and push-to-talk controls. Only the visual treatment changes.

## 3D in-world chat widget

The 3D widget (`BP_Convai3DWidgetComponent` / `WBP_3DChatWidget`, located at `ConvAI > ConvaiConveniencePack > 3DWidget`) renders a floating conversation panel above a character in world space. This is useful for open environments where the player faces different characters and needs to see each character's speech separately, or for kiosk installations where the display is part of the environment.

### Add the 3D widget to a character

{% stepper %}
{% step %}
### Open the character Blueprint

Open the NPC character Blueprint that already has `BP_ConvaiChatbotComponent` attached.
{% endstep %}

{% step %}
### Add the 3D Widget component

In the **Components** panel, click **Add**. Search for `BP Convai 3D Widget Component` and select it. This adds `BP_Convai3DWidgetComponent` to the Blueprint.
{% endstep %}

{% step %}
### Position the widget

Select the **BP Convai 3D Widget Component** in the **Components** panel. In the **Details** panel, adjust **Transform > Location** to position the widget above the character's head. For a standard-height character, `(X=0, Y=0, Z=200)` places the panel roughly above the head.
{% endstep %}

{% step %}
### Compile and save

Click **Compile** and **Save** in the Blueprint editor toolbar.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Enter Play mode and speak to the character. The 3D chat panel appears above the character and updates with the transcript as the conversation progresses.
{% endhint %}

## Replace with a custom widget

If neither the built-in overlay nor the 3D panel matches your project's UI design, wire a fully custom widget to the transcript delegate:

{% stepper %}
{% step %}
### Create a Widget Blueprint

In the **Content Browser**, right-click and select **User Interface > Widget Blueprint**. Design your custom chat display — a scroll box, a subtitle bar, or any layout you need.
{% endstep %}

{% step %}
### Bind the transcript delegate

In your widget's event graph (or in the owning actor Blueprint), bind to `OnTranscriptionReceivedDelegate` on the `UConvaiChatbotComponent`:

- `Transcription` — the transcript text at this point in the utterance.
- `IsFinal` — `true` when this is the last update for the utterance. Use this flag to commit the line to the display and clear any "typing..." indicator.
- `IsTranscriptionReady` — `true` when the text is ready to render.

Append each final transcript to your display panel to build up the conversation history.

`OnTranscriptionReceivedDelegate` is available on both the chatbot component (character response) and the player component (player speech). Bind to the **chatbot component** for what the character says, and to the **player component** for what the player said. See [Event system](../core-concepts/event-system.md) for the full delegate signature.
{% endstep %}

{% step %}
### Disable the built-in overlay

Set `UISelection` to `0` on `BP_ConvaiPlayerComponent` to hide the built-in overlay so it does not overlap your custom widget.
{% endstep %}
{% endstepper %}

## Troubleshooting

### Chat overlay does not appear in Play mode

**Symptom:** Play mode starts but no chat widget is visible.

**Cause:** `UISelection` is set to `0`, or the player pawn uses the bare `UConvaiPlayerComponent` (the C++ component) rather than `BP Convai Player Component` (the Blueprint wrapper that includes the widget).

**Fix:** Confirm `UISelection` is set to `1`, `2`, or `3` on the **Convai Player** component. Confirm the player pawn was set up using `BP Convai Player Component` — if the bare C++ component was added instead, replace it with the Blueprint wrapper.

### 3D widget is visible but shows no text

**Symptom:** The floating panel appears above the character but remains empty during conversation.

**Cause:** The chatbot session has not started, or the Character ID is invalid so no conversation data flows through the session.

**Fix:** Confirm `bAutoInitializeSession` is `true` on the **Convai Chatbot** component, or call `StartSession()` in Blueprint before the conversation begins. Confirm the **Character ID** matches a character in your Convai dashboard.

### Both the overlay and the 3D widget are showing simultaneously

**Symptom:** The screen-space overlay and the floating 3D panel are both visible, creating duplicate transcript displays.

**Cause:** `BP_Convai3DWidgetComponent` was added to the character without disabling the screen-space overlay on the player pawn.

**Fix:** Set `UISelection` to `0` on `BP_ConvaiPlayerComponent` to hide the screen-space overlay, leaving only the 3D widget active.

**Verify:** Enter Play mode and confirm that only the 3D panel above the character is visible — no second overlay appears in the viewport corners.

## Next steps

{% content-ref url="validate-your-setup.md" %}
[Validate your setup](validate-your-setup.md)
{% endcontent-ref %}
