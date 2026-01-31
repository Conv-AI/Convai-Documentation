---
description: >-
  Explore the Convai Web SDK — Fast, low-latency, voice-first AI character
  interaction for the browser
---

# Convai Web SDK \[Beta]

## Introduction

The **Convai Web SDK (`@convai/web-sdk`)** brings the new Convai backend to the browser, enabling fast, natural, hands-free AI interactions across modern web experiences.\
Built for production apps, immersive sites, and interactive worlds, the SDK handles real-time audio, text, optional video, character actions, and emotion signals — giving developers the tools to create responsive, intelligent AI characters directly on the web.

With built-in voice capture, speech detection, a ready-to-use chat widget, and full custom UI support, Convai makes it simple to integrate lifelike assistants, companions, and NPCs into any web environment.

{% hint style="warning" %}
## Beta Release

This is the **Beta** release of the Convai Web SDK.\
We’re actively improving performance, expanding capabilities, and delivering new interaction features. Your feedback plays an important role — share insights and suggestions in the [Convai Developer Forum](https://forum.convai.com/).
{% endhint %}

{% include "../../../.gitbook/includes/separation-line.md" %}

## What’s New

The Web SDK introduces a streamlined, high-performance interaction pipeline powered by Convai’s newest backend:

* **Hands-free voice conversations**\
  Natural, continuous dialogue without push-to-talk.
* **Low-latency responses**\
  Faster streaming replies for smooth, real-time interaction.
* **Emotion and action signalling**\
  Characters can express mood and trigger contextual behaviours.
* **Optional video and screen sharing**\
  Add richer visual context when your experience requires it.
* **Pre-built ConvaiWidget**\
  A polished, complete UI for audio, text, and video chat.
* **Custom UI and full control APIs**\
  Build your own interface and behaviour logic with exposed hooks and state.
* **Modern web integration**\
  Designed for Web-based frameworks and tooling.

{% include "../../../.gitbook/includes/separation-line.md" %}

### Core Concepts

At a high level, the SDK is organised into a few core pieces:

1. **ConvaiClient**\
   The brain. Manages connection, state, messages, audio/video/screen-share control, and blendshape queue.
2. **ConvaiWidget**\
   A complete, prebuilt interface for text + voice + optional video/screen share.
3. **AudioRenderer** **(Critical for audio playback)**\
   Attaches the bot's audio tracks to the user's speakers.
   * Required for custom UIs
   * Already built in to `ConvaiWidget`
4. **BlendshapeQueue** **(Essential for facial animation)**\
   Manages buffering and time-based retrieval of facial blendshape data.
   * Provides 60fps blendshape streams synchronized with speech
   * Supports ARKit (61 elements) and MetaHuman (251 elements) formats
   * Optional custom mapping for any character rig
5. **Connection Type**\
   Determines what's possible:
   * `"audio"` (default) – audio-only conversations
   * `"video"` – audio + video + screen share

***

### Architecture

```
┌─────────────────────────────────────────────────┐
│  ConvaiWidget (UI Layer)                        │
│  ├─ Chat Interface                              │
│  ├─ Voice Mode                                  │
│  └─ Video/Screen Share UI                       │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│  ConvaiClient (Core Logic)                      │
│  ├─ Connection Management                       │
│  ├─ Message Handling                            │
│  ├─ State Management                            │
│  └─ Audio/Video Controls                        │
│  └─ Blendshape Queue Management                 │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│  WebRTC Room (Communication Layer)              │
│  ├─ Real-time Audio/Video Streaming             │
│  ├─ Blendshape Data Streaming (60fps)           │
│  ├─ Track Management                            │
│  └─ Network Communication                       │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│  AudioRenderer (Critical for Playback)         │
│  ├─ Attaches audio tracks to DOM               │
│  ├─ Manages audio elements                     │
│  └─ Enables bot voice playback                 │
└─────────────────────────────────────────────────┘
```

***

#### What's Included

* **React SDK**
  * `useConvaiClient` hook for easy client lifecycle
  * `<ConvaiWidget />` for full UI
  * `<AudioRenderer />` + `AudioContext` for custom UIs
  * Access to `blendshapeQueue` for facial animation
* **Vanilla SDK**
  * `ConvaiClient` class for direct control
  * `AudioRenderer` class for playback
  * Optional `createConvaiWidget()` helper
  * `BlendshapeQueue` API for facial animation
* **Lipsync & Facial Animation**
  * Real-time blendshape streaming at 60fps
  * Support for ARKit (61) and MetaHuman (251) formats
  * Declarative name-based mapping system
  * Helper functions and preset configurations
  * Works with Three.js, Babylon.js, Unity WebGL, and custom engines
* **Video & Screen Share**
  * Camera and screen share support when `enableVideo: true`
  * Fine-grained video and screen share controls
* **TypeScript-first**
  * Full type definitions for configs, state, messages, and control APIs<br>

{% hint style="success" %}
## Performance Optimization&#x20;

To achieve the lowest possible latency, we recommend configuring your Core AI settings to use the `gemini-flash-2.5-beta` model. This model is optimized for speed and is ideal for real-time applications where response time is critical.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Core AI.png" alt=""><figcaption></figcaption></figure>

## Conclusion

The **Convai Web SDK (`@convai/web-sdk`)** marks a major step forward in bringing real-time AI interaction to the browser. With speech, actions, emotions, and optional video all running on the latest Convai backend, you can build fast, responsive, and deeply interactive AI characters across any web experience.

Start building today and bring the next generation of AI-powered interaction to the open web.
