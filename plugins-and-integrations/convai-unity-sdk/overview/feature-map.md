---
title: Feature map
description: >-
  Find the right Convai Unity SDK feature, module, guide, or reference page for
  any development goal, indexed by use case.
last_reviewed: "4.6.0"
---

Use this table when you know the outcome you want but are not sure which SDK feature, module, or guide covers it.

Rows labeled **Multi-character** point to staging documentation planned for Unity SDK <code class="expression">space.vars.unity_sdk_preview_version</code>. That feature is not included in the current <code class="expression">space.vars.unity_sdk_version</code> Asset Store release.

## Getting started

| I want to...                                         | Feature / Tool      | Documentation                                                                                |
| ---------------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------------- |
| Install the SDK into my project                      | Installation        | [Installation](../getting-started/installation.md)                                           |
| Configure my Convai API key                          | API key setup       | [Configure API key](../getting-started/configure-api-key.md)                                 |
| Add my first conversational character to a scene     | Scene setup         | [Build a custom scene](../getting-started/build-a-custom-scene.md)                           |
| Run a working example without building from scratch  | Sample scenes       | [Import and run sample scenes](../getting-started/import-and-run-sample-scenes.md)           |
| Understand what each component in the scene does     | Component reference | [Scene components reference](../getting-started/scene-components.md)                         |
| Choose between push-to-talk and hands-free input     | Input mode          | [Configure conversation input mode](../getting-started/configure-conversation-input-mode.md) |
| Configure character audio output                     | Audio setup         | [Configure character audio](../getting-started/configure-character-audio.md)                 |
| Configure microphone device and platform permissions | Audio setup         | [Configure microphone](../getting-started/configure-microphone.md)                           |
| Add a chat or subtitle transcript display            | Transcript UI       | [Add chat UI](../getting-started/add-chat-ui.md)                                             |
| Add real-time lip sync to my character               | Lip sync            | [Add lip sync](../getting-started/add-lip-sync/)                                             |
| Verify my scene is set up correctly before shipping  | Scene Validator     | [Validate your setup](../getting-started/validate-your-setup.md)                             |
| Connect two or more owned characters in one room     | Multi-character     | [Multi-character quick start](../features/multi-character-conversations/quick-start.md)      |

## Features

| I want to...                                                                              | Feature          | Documentation                                     |
| ----------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------- |
| Let my character execute in-scene commands (trigger animations, open doors, move objects) | Actions          | [Actions](../features/character-actions/)         |
| Inject runtime state or events into the character's knowledge                             | Dynamic Context  | [Dynamic Context](../features/dynamic-context/)   |
| Let the character automatically read information about scene objects                      | Scene Metadata   | [Scene Metadata](../features/scene-metadata/)     |
| Show facial emotion on my character driven by the AI response                             | Emotion          | [Emotion](../embodiment/emotion/)                 |
| Make the character remember players between sessions                                      | Long-Term Memory | [Long-Term Memory](../features/long-term-memory/) |
| Build branching story sections triggered by conversation                                  | Narrative Design | [Narrative Design](../features/narrative-design/) |
| Give my character vision through a camera or webcam                                       | Vision           | [Vision](../features/vision/)                     |
| Route one player between several characters in a shared room                              | Multi-character  | [Multi-character conversations](../features/multi-character-conversations/) |

## Embodiment

| I want to...                                                                | Module            | Documentation                                                                   |
| --------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------- |
| Make my character look at the player, at objects, or around the scene       | Gaze              | [Gaze](../embodiment/gaze/)                                                     |
| Time a character's behavior to the phase of the conversation                | Conversation Flow | [Conversation flow](../embodiment/conversation-flow/)                           |
| Share one set of behavior settings across several characters                | Presets           | [Embodiment presets](../embodiment/embodiment-presets.md)                       |
| Decide how much of the face emotion and lip sync each control while speaking | Facial composition | [Facial composition](../embodiment/facial-composition.md)                      |
| Move from the retired Attention module to Convai Gaze                       | Migration         | [Migrate from Attention](../embodiment/gaze/migrate-from-attention.md)          |

## UI and presentation

| I want to...                                                         | Component           | Documentation                                                                                            |
| -------------------------------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------------- |
| Display a live conversation transcript in my UI                      | Transcript UI       | [Transcript UI](../ui-and-presentation/transcript-ui/)                                                   |
| Switch between chat and subtitle display modes                       | Presentation modes  | [Chat and subtitle modes](../ui-and-presentation/transcript-ui/chat-and-subtitle-modes.md)               |
| Query transcript history or react to transcript changes from code    | Transcript history  | [Transcript history and queries](../ui-and-presentation/transcript-ui/transcript-history-and-queries.md) |
| Show in-world notification popups                                    | Notification system | [Notification system](../ui-and-presentation/notification-system/)                                       |
| Add a runtime settings panel (mic, transcript, notifications, input) | Settings panel      | [Settings panel](../ui-and-presentation/settings-panel/)                                                 |
| Read or apply runtime settings from code                             | Runtime settings    | [Runtime settings API](../ui-and-presentation/settings-panel/runtime-settings-api.md)                    |
| Customize the look and layout of UI components                       | UI customization    | [Customizing UI components](../ui-and-presentation/customizing-ui-components.md)                         |

## Core concepts

| I want to...                                             | Concept           | Documentation                                                     |
| -------------------------------------------------------- | ----------------- | ----------------------------------------------------------------- |
| Understand the system architecture end-to-end            | Architecture      | [Convai Unity SDK architecture](convai-unity-sdk-architecture.md) |
| Understand session states, reconnection, and persistence | Session lifecycle | [Session lifecycle](../core-concepts/session-lifecycle.md)        |
| Compare hands-free, push-to-talk turn-taking             | Turn-taking modes | [Turn-taking modes](../core-concepts/turn-taking-modes.md)        |
| Subscribe to conversation events from C# or Inspector    | Event system      | [Event System](../core-concepts/event-system.md)                  |
| Understand shared-room readiness, identity, and routing   | Multi-character  | [How multi-character conversations work](../features/multi-character-conversations/how-it-works.md) |

## Scripting reference

| I want to...                                                 | API                  | Documentation                                                    |
| ------------------------------------------------------------ | -------------------- | ---------------------------------------------------------------- |
| Subscribe to session connected / disconnected / error events | Session events       | [Session Events](../scripting-reference/session-events.md)       |
| Subscribe to transcript, emotion, and turn events            | Character events     | [Character Events](../scripting-reference/character-events.md)   |
| Read and clear transcript history at runtime                 | Transcript API       | [Transcript API](../scripting-reference/transcript-api.md)       |
| Use manager and audio facades                                | Conversation facades | [ConvaiManager API](../scripting-reference/convaimanager-api.md) |
| Understand `IConvaiOperation<T>` and async patterns          | Async patterns       | [Async Patterns](../scripting-reference/async-patterns.md)       |
| Change the acknowledged interaction target or room roster   | Room connection API  | [Multi-character room connection API](../features/multi-character-conversations/room-connection-api.md) |
| Observe membership readiness, results, epochs, and events    | Session and roster   | [Multi-character session and roster API](../features/multi-character-conversations/session-and-roster-api.md) |
| Attribute room transcripts and route participant audio      | Transcript and audio | [Multi-character transcripts and events](../features/multi-character-conversations/transcripts-and-events.md) |

## Platform guides

| I want to...                               | Platform        | Documentation                                                     |
| ------------------------------------------ | --------------- | ----------------------------------------------------------------- |
| Ship to a browser with WebGL               | WebGL           | [WebGL](../platform-guides/webgl.md)                              |
| Ship to Android or iOS                     | Mobile          | [Mobile — iOS and Android](../platform-guides/ios-and-android.md) |
| Ship to Meta Quest with passthrough vision | Meta Quest / XR | [Meta Quest and XR](../platform-guides/xr-headsets.md)            |

## Advanced topics

| I want to...                                                     | Topic            | Documentation                                                                                     |
| ---------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------- |
| Replace the API credential provider                              | Custom providers | [Custom Credential Provider](../advanced-topics/custom-providers/custom-credential-provider.md)   |
| Replace the end-user identity provider                           | Custom providers | [Custom Identity Provider](../advanced-topics/custom-providers/custom-identity-provider.md)       |
| Replace the session persistence provider                         | Custom providers | [Custom Persistence Provider](../advanced-topics/custom-providers/custom-persistence-provider.md) |
| Measure latency and interpret session metrics                    | Performance      | [Performance and Optimization](../advanced-topics/performance-and-optimization.md)                |
| Extend the SDK with a custom module or replace internal services | Extension points | [Extending the SDK](../advanced-topics/extending-the-sdk.md)                                      |

## Next steps

Start with installation if you have not set up the SDK yet.

{% content-ref url="../getting-started/" %}
[getting-started](../getting-started/)
{% endcontent-ref %}
