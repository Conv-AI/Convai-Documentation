---
title: Run the group conversation sample
description: Open the shipped workshop scene, rehearse its offline group simulation, then prepare a separate live preview test with the required service access.
last_reviewed: "5.0.0-preview"
---

`GroupConversationSample.unity` provides a three-character workshop scene configured for offline rehearsal. It belongs to the **Multi Character Sample**, alongside the classic multi-character scene.

## Import the sample prerequisites

Use a project configured for the Universal Render Pipeline; the scene and volume profile use URP components. URP is a sample dependency, not a package-wide SDK requirement. Import **LipSync Sample** first for the shared Sofia assets, then import **Multi Character Sample** from the package's Samples list.

Open `Scenes/GroupConversationSample.unity` in the imported sample directory. Keep the original scene available and save deliberate changes in your project copy.

## Rehearse offline

The scene has Tuesday, Friday, and Wednesday, with Friday as the initial character. Automatic connection is off: **Starts Connected** on the Room Manager and each character's **Auto Connect** are both off. Turning **Starts Connected** off also blocks each character's **Auto Connect**, including characters enabled later during play. Explicit `ConnectAsync` and `StartConversationAsync` calls still work with **Starts Connected** off. The group component, simulator, and overlay are enabled, and character audio is configured for 3D playback when used live.

Enter Play mode. Use **F9** to show or hide the overlay and hold **T** to exercise a player turn. Move and look toward different characters to inspect spatial and addressing state. Expect canned lines without spoken character audio from the simulator.

Keep **Show Transcript** off for screenshots and recordings unless the user explicitly wants their utterance shown. A working offline rehearsal verifies client event/UI wiring only.

## Prepare a live preview test

Exit Play mode, disable the simulator, and turn **Starts Connected** on in the Room Manager. Turning on a character's **Auto Connect** alone does not connect while **Starts Connected** is off. Verify that the selected 2–4 characters use distinct IDs accessible to the configured account and Live versions. Keep Push To Talk with a compatible correlated release policy and audio-only connection.

Confirm group-conversation preview availability with the service owner, then enter Play mode. To connect from your own code instead, leave **Starts Connected** off and call `ConnectAsync` or `StartConversationAsync`. The [Simulator and debug overlay](simulator-and-debug-overlay.md) page covers how the simulator and **Starts Connected** interact. Verify actual speech recognition, service state, each character's voice, player recipient decisions, pause/resume, and reconnect behavior. Do not report the offline run as live voice or account validation.

## Verify the sample's two modes

| Mode | Expected evidence |
| --- | --- |
| Simulator | Synthetic room/membership state, canned lines, no character voice |
| Service-backed preview | Authorized connection, reported group state, actual participant audio and player transcript/recipient behavior |

If the room connects while the simulator is active, the simulator disables itself instead of taking over the live session. Start each test with the intended mode explicit.

## Next steps

{% content-ref url="simulator-and-debug-overlay.md" %}
[Simulator and debug overlay](simulator-and-debug-overlay.md)
{% endcontent-ref %}
{% content-ref url="quick-start.md" %}
[Set up group conversation](quick-start.md)
{% endcontent-ref %}
