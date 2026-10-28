---
title: UI and Presentation
description: >-
  Optional, scene-level UI for displaying transcripts, surfacing notifications,
  and giving users a runtime settings panel — add only what your project needs.
last_reviewed: "5.0.0-preview"
---

The Convai Unity SDK ships a set of optional, scene-level UI components. The displays render runtime data locally. Chat input sends typed messages to Convai, and the settings panel can request a conversation-mode change through the room service.

Each component is independent. Add only what your training simulation, interactive experience, or game requires.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Transcript UI</strong><br>Add scrollable chat or fixed-position subtitle display to your scene with the built-in prefab or a custom implementation.</td><td><a href="transcript-ui/">transcript-ui</a></td></tr><tr><td><strong>Transcript History and Queries</strong><br>Query the retained room transcript history, filter by participant, and react to transcript changes from code.</td><td><a href="transcript-ui/transcript-history-and-queries.md">transcript-history-and-queries.md</a></td></tr><tr><td><strong>Chat and Subtitle Modes</strong><br>Compare the two built-in display modes, configure Inspector fields, and inspect chat input availability.</td><td><a href="transcript-ui/chat-and-subtitle-modes.md">chat-and-subtitle-modes.md</a></td></tr><tr><td><strong>Notification System</strong><br>Surface toast-style alerts for session errors, status changes, and custom in-scene events.</td><td><a href="notification-system/">notification-system</a></td></tr><tr><td><strong>Settings Panel</strong><br>Give users a runtime panel to adjust microphone, transcript visibility, and conversation preferences.</td><td><a href="settings-panel/">settings-panel</a></td></tr><tr><td><strong>Customizing UI components</strong><br>Restyle the built-in transcript, notification, and settings panel UI using transcript subscriptions or prefab swapping.</td><td><a href="customizing-ui-components.md">customizing-ui-components.md</a></td></tr><tr><td><strong>Notification system reference</strong><br>Reference for SONotification, SONotificationGroup, UINotificationController, and error map assets.</td><td><a href="notification-system/notification-system-reference.md">notification-system-reference.md</a></td></tr><tr><td><strong>Runtime settings API</strong><br>Reference for IConvaiRuntimeSettingsService — read, apply, and react to runtime settings changes from code.</td><td><a href="settings-panel/runtime-settings-api.md">runtime-settings-api.md</a></td></tr></tbody></table>

## Focused displays

Use [Per-character transcript display](transcript-ui/per-character-transcript-display.md) for a label attached to one character. Add [Connection and audio indicators](show-connection-and-audio-levels.md) to show connection progress or microphone activity. The shipped chat prefabs also include a clickable settings area.
