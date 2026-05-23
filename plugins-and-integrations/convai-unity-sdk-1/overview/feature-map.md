---
title: Feature map
description: >-
  Find the right Convai Unity SDK feature, module, guide, or reference page for
  any development goal, indexed by use case.
---

Use this table when you know the outcome you want but are not sure which SDK feature, module, or guide covers it.

## Getting started

| I want to...                                        | Feature / Tool      | Documentation                                                                                        |
| --------------------------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------- |
| Install the SDK into my project                     | Installation        | [Installation](../getting-started/installation.md)                                                   |
| Configure my Convai API key                         | API key setup       | [Configure API key](../getting-started/configure-api-key.md)                                         |
| Add my first conversational character to a scene    | Scene setup         | [Build a custom scene](../getting-started/build-a-custom-scene.md)                                   |
| Run a working example without building from scratch | Sample scenes       | [Import and run sample scenes](../getting-started/import-and-run-sample-scenes.md)                   |
| Understand what each component in the scene does    | Component reference | [Understand scene components](../getting-started/understand-scene-components.md)                     |
| Choose between push-to-talk and hands-free input    | Input mode          | [Configure conversation input mode](../getting-started/configure-conversation-input-mode.md)         |
| Configure microphone and audio output               | Audio setup         | [Configure audio](../getting-started/configure-audio.md)                                             |
| Add a chat or subtitle transcript display           | Transcript UI       | [Add chat UI](../getting-started/add-chat-ui.md)                                                     |
| Add real-time lip sync to my character              | Lip sync            | [Add lip sync](../getting-started/add-lip-sync/README.md)                                            |
| Verify my scene is set up correctly before shipping | Scene Validator     | [Validate your setup](../getting-started/validate-your-setup.md)                                     |

## Features

| I want to...                                                                              | Feature          | Documentation                                                                        |
| ----------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------ |
| Let my character execute in-scene commands (trigger animations, open doors, move objects) | Actions          | [Actions](../features/character-actions/README.md)                                   |
| Inject runtime state or events into the character's knowledge                             | Dynamic Context  | [Dynamic Context](../features/dynamic-context/README.md)                             |
| Let the character automatically read information about scene objects                      | Scene Metadata   | [Scene Metadata](../features/scene-metadata/README.md)                               |
| Show facial emotion on my character driven by the AI response                             | Emotion          | [Emotion](../features/emotion/README.md)                                             |
| Make the character remember players between sessions                                      | Long-Term Memory | [Long-Term Memory](../features/long-term-memory/README.md)                           |
| Build branching story sections triggered by conversation                                  | Narrative Design | [Narrative Design](../features/narrative-design/README.md)                           |
| Give my character vision through a camera or webcam                                       | Vision           | [Vision](../features/vision/README.md)                                               |

## Utilities

| I want to...                                                      | Utility            | Documentation                                                                |
| ----------------------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------- |
| Add body and head dialogue animations to my character             | Dialogue Animation | [Dialogue Animation](../utilities/dialogue-animation/README.md)              |
| Make my character look at targets, players, or points of interest | Gaze and Attention | [Gaze and Attention](../utilities/gaze-and-attention/README.md)              |

## UI and presentation

| I want to...                                          | Component           | Documentation                                                                             |
| ----------------------------------------------------- | ------------------- | ----------------------------------------------------------------------------------------- |
| Display a live conversation transcript in my UI       | Transcript UI       | [Transcript UI](../ui-and-presentation/transcript-ui.md)                                  |
| Switch between chat, subtitle, and Q\&A display modes | Presentation modes  | [Chat and subtitle modes](../ui-and-presentation/chat-and-subtitle-modes.md)              |
| Show in-world notification popups                     | Notification System | [Notification System](../ui-and-presentation/notification-system.md)                     |
| Add a runtime settings panel (mic, audio, input mode) | Settings Panel      | [Settings Panel](../ui-and-presentation/settings-panel.md)                               |
| Customize the look and layout of UI components        | UI customization    | [Customizing UI components](../ui-and-presentation/customizing-ui-components.md)          |

## Core concepts

| I want to...                                             | Concept           | Documentation                                                                                         |
| -------------------------------------------------------- | ----------------- | ----------------------------------------------------------------------------------------------------- |
| Understand the system architecture end-to-end            | Architecture      | [Convai Unity SDK architecture](architecture-overview.md)                                             |
| Understand session states, reconnection, and persistence | Session lifecycle | [Session lifecycle](../core-concepts/session-lifecycle.md)  |
| Compare hands-free, push-to-talk turn-taking             | Turn-taking modes | [Turn-taking modes](../core-concepts/turn-taking-modes.md)                                            |
| Subscribe to conversation events from C# or Inspector    | Event system      | [Event System](../core-concepts/event-system.md)                                                      |

## Scripting reference

| I want to...                                                 | API                  | Documentation                                                                      |
| ------------------------------------------------------------ | -------------------- | ---------------------------------------------------------------------------------- |
| Subscribe to session connected / disconnected / error events | Session events       | [Session Events](../scripting-reference/session-events.md)                         |
| Subscribe to transcript, emotion, and turn events            | Character events     | [Character Events](../scripting-reference/character-events.md)                     |
| Read and clear transcript history at runtime                 | Transcript API       | [Transcript API](../scripting-reference/transcript-api.md)                         |
| Use the `ConvaiSDK` and `ConvaiAudio` static facades         | Conversation facades | [ConvaiManager API](../scripting-reference/convaimanager-api.md)                   |
| Understand `IConvaiOperation<T>` and async patterns          | Async patterns       | [Async Patterns](../scripting-reference/async-patterns.md)                         |

## Platform guides

| I want to...                               | Platform        | Documentation                                                        |
| ------------------------------------------ | --------------- | -------------------------------------------------------------------- |
| Ship to a browser with WebGL               | WebGL           | [WebGL](../platform-guides/webgl.md)                                 |
| Ship to Android or iOS                     | Mobile          | [Mobile — iOS and Android](../platform-guides/ios-and-android.md)    |
| Ship to Meta Quest with passthrough vision | Meta Quest / XR | [Meta Quest and XR](../platform-guides/xr-headsets.md)               |

## Advanced topics

| I want to...                                                     | Topic            | Documentation                                                                                    |
| ---------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------ |
| Replace the API credential provider                              | Custom providers | [Custom Credential Provider](../advanced-topics/custom-providers/custom-credential-provider.md)  |
| Replace the end-user identity provider                           | Custom providers | [Custom Identity Provider](../advanced-topics/custom-providers/custom-identity-provider.md)      |
| Replace the session persistence provider                         | Custom providers | [Custom Persistence Provider](../advanced-topics/custom-providers/custom-persistence-provider.md)|
| Measure latency and interpret session metrics                    | Performance      | [Performance and Optimization](../advanced-topics/performance-and-optimization.md)               |
| Extend the SDK with a custom module or replace internal services | Extension points | [Extending the SDK](../advanced-topics/extending-the-sdk.md)                                     |

## Next steps

Start with installation if you have not set up the SDK yet.

{% content-ref url="../getting-started/README.md" %}
[Getting Started](../getting-started/README.md)
{% endcontent-ref %}
