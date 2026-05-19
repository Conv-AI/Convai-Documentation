---
description: Every Convai Unity SDK feature and guide organized by what you want to build.
---

# Feature Map

## Find the Right Feature for Your Project

Use this table when you know the outcome you want but are not sure which SDK feature, module, or guide covers it. Each row links to the relevant documentation section.

***

## Getting Started

| I want to...                                        | Feature / Tool      | Documentation                                                                               |
| --------------------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------- |
| Install the SDK into my project                     | Installation        | [Installation](/broken/pages/971a2eb9c757d5f76732b9c6b6543f56be6586c4)                      |
| Configure my Convai API key                         | API key setup       | [Configure API Key](/broken/pages/be89f4223dcfdffaf270ef972c5e564cd96d5eb1)                 |
| Add my first conversational character to a scene    | Scene setup         | [Custom Scene Setup](/broken/pages/477f3e0fbffc248414da1eaa9b83f8ca3a186c06)                |
| Run a working example without building from scratch | Sample scenes       | [Import and Run Sample Scenes](/broken/pages/9aa6f43a1301ed35a35c54ebd8ce913435ab4c1e)      |
| Understand what each component in the scene does    | Component reference | [Understanding Scene Components](/broken/pages/1d9cd0aa1ddc4cd45c224d992f28b9502fe0b062)    |
| Choose between push-to-talk and hands-free input    | Input mode          | [Configure Conversation Input Mode](/broken/pages/ca110b3413d787ae6ac298e2b8400531a54d4961) |
| Configure microphone and audio output               | Audio setup         | [Configure Audio](/broken/pages/0d408c37bf34a5da43c2688a0223397061e55383)                   |
| Add a chat or subtitle transcript display           | Transcript UI       | [Add Chat UI](/broken/pages/242a10aadc11fdde2c8d21864aa9bb2e3a94d23c)                       |
| Add real-time lip sync to my character              | Lip sync            | [Add Lip Sync](/broken/pages/a62272a38692dfc9722dc4f7152ae9bd4ae08154)                      |
| Verify my scene is set up correctly before shipping | Scene Validator     | [Validate Your Setup](/broken/pages/e8609e65c2bc1e0a46b3fb04544dd4981f0083ee)               |

***

## Features

| I want to...                                                                              | Feature          | Documentation                                                              |
| ----------------------------------------------------------------------------------------- | ---------------- | -------------------------------------------------------------------------- |
| Let my character execute in-scene commands (trigger animations, open doors, move objects) | Actions          | [Actions](/broken/pages/46d20373036c3c1a8d7d4088901c20f1baa78a4c)          |
| Inject runtime state or events into the character's knowledge                             | Dynamic Context  | [Dynamic Context](/broken/pages/ff229409c9d35525aedff2c5f5d53a1d4a34c251)  |
| Let the character automatically read information about scene objects                      | Scene Metadata   | [Scene Metadata](/broken/pages/6e344994669498c23f0f2c05289f6ca482b4f3a7)   |
| Show facial emotion on my character driven by the AI response                             | Emotion          | [Emotion](/broken/pages/9e79412f5557438ae87fa4f4e671bd21c482f012)          |
| Make the character remember players between sessions                                      | Long-Term Memory | [Long-Term Memory](/broken/pages/619f2f226f019074c170deb80032e5b335d1bfb8) |
| Build branching story sections triggered by conversation                                  | Narrative Design | [Narrative Design](/broken/pages/c1c9528f02873c7dc5d600c093e000d990f67c02) |
| Give my character vision through a camera or webcam                                       | Vision           | [Vision](/broken/pages/5059f9d12a243034d63efcd728392be7f895f82a)           |

***

## Utilities

| I want to...                                                      | Utility            | Documentation                                                                |
| ----------------------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------- |
| Add body and head dialogue animations to my character             | Dialogue Animation | [Dialogue Animation](/broken/pages/ff77f34a646330af24aa9406fde945ca6d9a706c) |
| Make my character look at targets, players, or points of interest | Gaze & Attention   | [Gaze & Attention](/broken/pages/b2099522c591f11b1e1613c2324c18530073c9f4)   |

***

## UI & Presentation

| I want to...                                          | Component           | Documentation                                                                       |
| ----------------------------------------------------- | ------------------- | ----------------------------------------------------------------------------------- |
| Display a live conversation transcript in my UI       | Transcript UI       | [Transcript UI](/broken/pages/73414f05e15918400287fcb55e73626f2f42c83e)             |
| Switch between chat, subtitle, and Q\&A display modes | Presentation modes  | [Chat vs. Subtitle Mode](/broken/pages/0bfff212067c65d8ff6b3061371052945e0fe379)    |
| Show in-world notification popups                     | Notification System | [Notification System](/broken/pages/e088e3e97787b76780420129c11a7d21485d6367)       |
| Add a runtime settings panel (mic, audio, input mode) | Settings Panel      | [Settings Panel](/broken/pages/be2b7d7c1cf1ff14ddde43a3dbfae7851dbbfdb4)            |
| Customize the look and layout of UI components        | UI customization    | [Customizing UI Components](/broken/pages/2edd94efe6cba88bd50c4d6a6bc1f9b673c95a60) |

***

## Core Concepts

| I want to...                                             | Concept           | Documentation                                                                                    |
| -------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------ |
| Understand the system architecture end-to-end            | Architecture      | [Architecture Overview](/broken/pages/4e3f79376d38cb723bf69a615076ffdfb6556f2d)                  |
| Understand session states, reconnection, and persistence | Session lifecycle | [Session Lifecycle and State Management](/broken/pages/aa5f3f58650f16be74d56d2c1932c0b071be5799) |
| Compare hands-free, push-to-talk, and smart turn-taking  | Turn-taking modes | [Turn-Taking Modes](/broken/pages/43d2a627f3db81eba35c332edf2ffbb98a923065)                      |
| Subscribe to conversation events from C# or Inspector    | Event system      | [Event System](/broken/pages/86463d44d092d5de5f86edac1ca0b5f76010c968)                           |

***

## Scripting Reference

| I want to...                                                 | API                  | Documentation                                                                  |
| ------------------------------------------------------------ | -------------------- | ------------------------------------------------------------------------------ |
| Subscribe to session connected / disconnected / error events | Session events       | [Session Events](/broken/pages/fe918a57682d27ee01e9f1ad004be448f12745af)       |
| Subscribe to transcript, emotion, and turn events            | Character events     | [Character Events](/broken/pages/5152d2e0085ce2045fc2cc6cc951f25e29355eff)     |
| Read and clear transcript history at runtime                 | Transcript API       | [Transcript API](/broken/pages/c07ea22e3499df4a8772b002a55fa8df3420b820)       |
| Use the `ConvaiSDK` and `ConvaiAudio` static facades         | Conversation facades | [Conversation Facades](/broken/pages/88061036d80b09df61d17d0eff376a9503a5c51c) |
| Understand `IConvaiOperation<T>` and async patterns          | Async patterns       | [Async Patterns](/broken/pages/842066c62478b0db9cda8279a5b8330cf9b9ce2c)       |

***

## Platform Guides

| I want to...                               | Platform        | Documentation                                                                      |
| ------------------------------------------ | --------------- | ---------------------------------------------------------------------------------- |
| Ship to a browser with WebGL               | WebGL           | [WebGL](/broken/pages/e3153c43245d7ddef170b652abc9239b81a2ad3b)                    |
| Ship to Android or iOS                     | Mobile          | [Mobile — iOS and Android](/broken/pages/7de9eacfd02cf19bcf7f20e28e7fe25836d3b246) |
| Ship to Meta Quest with passthrough vision | Meta Quest / XR | [Meta Quest and XR](/broken/pages/ac62bd17dc46419227411aff09adcd23b4020ea7)        |

***

## Advanced Topics

| I want to...                                                     | Topic            | Documentation                                                                          |
| ---------------------------------------------------------------- | ---------------- | -------------------------------------------------------------------------------------- |
| Run multiple independent AI characters in one scene              | Multi-character  | [Multi-Character Scenarios](/broken/pages/b1d9d7ce3161ef8c43c9640e0067d955cd0c9015)    |
| Replace the API credential provider                              | Custom providers | [Custom Credential Provider](/broken/pages/7ef069b9a9c78bf01155f22d47a24346a5f70e3b)   |
| Replace the end-user identity provider                           | Custom providers | [Custom Identity Provider](/broken/pages/c0e54a1a80c41f7c8f99aeeb7385f719f792fa71)     |
| Replace the session persistence provider                         | Custom providers | [Custom Persistence Provider](/broken/pages/207698a68b20b6b53e8da58372440c25ab854908)  |
| Measure latency and interpret session metrics                    | Performance      | [Performance and Optimization](/broken/pages/c109c95c856e48e97c8e7dbb4f3d34d7407af91a) |
| Extend the SDK with a custom module or replace internal services | Extension points | [Extending the SDK](/broken/pages/459afbf29f297889828cbd41d8a12d905017edd5)            |

***

## Next Steps

Start with installation if you haven't set up the SDK yet.

{% content-ref url="/broken/pages/63e79c1ce45c5fae027b5b1e1b756bbfd5e332d0" %}
[Broken link](/broken/pages/63e79c1ce45c5fae027b5b1e1b756bbfd5e332d0)
{% endcontent-ref %}
