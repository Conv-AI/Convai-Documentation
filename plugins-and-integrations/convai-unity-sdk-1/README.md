---
title: Convai Unity SDK
description: >-
  Add real-time AI characters to Unity training simulations, interactive
  experiences, and games — with speech, emotion, actions, and persistent memory.
hidden: true
noIndex: true
---

The Convai Unity SDK connects Unity projects to Convai, bringing conversational AI into training simulations, interactive experiences, and games. Characters process speech in real time, respond with natural language, and synchronize lip movement, facial emotion, and body animation — all configurable per project. Each feature is a self-contained module: add only what your project needs, in the order that fits your workflow.

{% hint style="info" %}
**New to the SDK?** Follow [Getting Started](getting-started/README.md) to install the package, configure your API key, and run your first AI character.
{% endhint %}

## Learn the SDK

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Overview</strong><br>What the SDK is, how it is structured, and when to use each module.</td><td><a href="overview/README.md">overview/README.md</a></td></tr><tr><td><strong>Compatibility and requirements</strong><br>Unity versions, render pipelines, platform support, and network requirements.</td><td><a href="compatibility-and-requirements/README.md">compatibility-and-requirements/README.md</a></td></tr><tr><td><strong>Core concepts</strong><br>Session lifecycle, turn-taking modes, and the SDK event system.</td><td><a href="core-concepts/README.md">core-concepts/README.md</a></td></tr></tbody></table>

## Features

Each feature is a self-contained module you opt into.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Actions</strong><br>Characters execute structured in-scene commands dispatched by Convai.</td><td><a href="features/character-actions/README.md">features/character-actions/README.md</a></td></tr><tr><td><strong>Emotion</strong><br>Map Convai emotion signals to facial blendshapes or Animator parameters.</td><td><a href="features/emotion/README.md">features/emotion/README.md</a></td></tr><tr><td><strong>Long-term memory</strong><br>Characters remember each player across separate sessions.</td><td><a href="features/long-term-memory/README.md">features/long-term-memory/README.md</a></td></tr><tr><td><strong>Vision</strong><br>Characters see through a Unity camera, webcam, or Meta Quest passthrough.</td><td><a href="features/vision/README.md">features/vision/README.md</a></td></tr><tr><td><strong>Dynamic context</strong><br>Inject runtime state and events into character knowledge at any time.</td><td><a href="features/dynamic-context/README.md">features/dynamic-context/README.md</a></td></tr><tr><td><strong>Narrative design</strong><br>Trigger-based story section progression tied to conversation flow.</td><td><a href="features/narrative-design/README.md">features/narrative-design/README.md</a></td></tr><tr><td><strong>Scene metadata</strong><br>Characters automatically read contextual information about scene objects.</td><td><a href="features/scene-metadata/README.md">features/scene-metadata/README.md</a></td></tr></tbody></table>

## Utilities

Helper modules that run entirely within Unity — no Convai communication required.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Dialogue animation</strong><br>Four-layer animator stack driving body and head movement during speech.</td><td><a href="utilities/dialogue-animation/README.md">utilities/dialogue-animation/README.md</a></td></tr><tr><td><strong>Gaze and attention</strong><br>Eye and head gaze blended toward focus targets and conversation partners.</td><td><a href="utilities/gaze-and-attention/README.md">utilities/gaze-and-attention/README.md</a></td></tr></tbody></table>

## Reference and guides

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>UI and presentation</strong><br>Transcript UI, subtitle modes, notification system, and settings panel.</td><td><a href="ui-and-presentation/README.md">ui-and-presentation/README.md</a></td></tr><tr><td><strong>Scripting reference</strong><br>Full API reference for session events, character events, and the transcript system.</td><td><a href="scripting-reference/README.md">scripting-reference/README.md</a></td></tr><tr><td><strong>Platform guides</strong><br>WebGL, Android, iOS, and Meta Quest deployment guides.</td><td><a href="platform-guides/README.md">platform-guides/README.md</a></td></tr><tr><td><strong>Advanced topics</strong><br>Custom providers, performance, and SDK extension points.</td><td><a href="advanced-topics/README.md">advanced-topics/README.md</a></td></tr><tr><td><strong>Troubleshooting</strong><br>Common failure modes, diagnostic steps, and known issues.</td><td><a href="troubleshooting/README.md">troubleshooting/README.md</a></td></tr></tbody></table>

## Latest release

**v{{ unity_sdk_version }}** introduces Structured Actions for precise in-scene command dispatch, Meta Quest passthrough vision for AR character awareness, runtime turn-taking mode switching, and expanded dynamic context for richer NPC knowledge.

## Next steps

Install the Convai Unity SDK and connect your first AI character using the Getting Started section. If you are evaluating the SDK before installing, review [Compatibility and requirements](compatibility-and-requirements/README.md) to confirm platform and Unity version support.

{% content-ref url="getting-started/README.md" %}
[Getting Started](getting-started/README.md)
{% endcontent-ref %}
