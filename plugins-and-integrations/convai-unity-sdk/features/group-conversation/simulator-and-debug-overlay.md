---
title: Simulator and debug overlay
description: Rehearse group conversation without a backend, inspect event and spatial state, and keep player transcripts out of diagnostic captures by default.
last_reviewed: "5.0.0-preview"
---

Use the simulator to exercise client behavior without a service connection, and the debug overlay to inspect either simulated or live group state. Neither tool grants preview service access.

## Run the simulator

Add **Convai > Group Conversation Simulator** beside a configured group component. Turn off **Starts Connected** on `ConvaiRoomManager` and enter Play mode in the Editor or a development build. The selected roster must contain 2–4 active characters with distinct Character IDs.

Turning off **Starts Connected** also blocks each character's **Auto Connect**, including characters enabled later during play. Explicit `ConnectAsync` and `StartConversationAsync` calls still work. To use the service, disable the simulator, then turn **Starts Connected** on or connect with your project's normal flow.

The simulator uses synthetic membership IDs, canned text, and the manager's push-to-talk key (T by default). It exercises client events, head-turn behavior, and the overlay but produces no character voice. Hold and release the key while looking toward a member or standing near one to rehearse player-turn handling.

It refuses ordinary release builds and disables itself when a live connection or group session exists. A reconnecting live session also keeps ownership; the simulator must not replace it.

## Inspect the overlay

Add **Convai > Group Conversation Debug Overlay**. F9 toggles visibility by default. The Editor can show it when Play mode starts; player builds start hidden. Non-development builds require the explicit **Allow In Release Builds** setting.

The overlay reports group state, topic, floor, member distances/visibility, and the last addressing decision. Use event counts and state transitions to locate ordering or setup problems, then compare with the actual operation result and audio behavior.

**Show Transcript** is off by default. Keep it off for shared screenshots and recordings unless displaying the player's utterance is explicitly intended. Do not mistake hiding this field for a broader application data-retention policy.

## What this verifies

| Check | Offline simulator | Live environment required |
| --- | --- | --- |
| UI subscriptions and snapshot rendering | Yes | Also verify with real event timing |
| Gaze and spatial client wiring | Yes | Verify actual character rigs/platforms |
| Push-to-talk key transitions | Simulated | Microphone capture, drain, transcription, and service correlation |
| Speaker state | Canned events | Service arbitration and participant voice |
| Authorization and account capacity | No | Yes |

For a complete starting scene, see [Run the group conversation sample](run-the-sample.md).

## Next steps

{% content-ref url="troubleshooting.md" %}
[Troubleshoot group conversation](troubleshooting.md)
{% endcontent-ref %}
