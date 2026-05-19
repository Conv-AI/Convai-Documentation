---
description: >-
  Layer-based body and head animation system that responds to dialogue state and
  emotion — drives gesture clips from a pooled library without building
  individual animator states.
---

# Dialogue Animation

## Drive Gesture Animation from Dialogue State and Emotion

The Dialogue Animation module drives body and head gesture animations on AI characters using dialogue state and detected emotion as inputs. Instead of hard-coded animator states for every clip, it uses an `AnimatorOverrideController` to inject clips from a pooled library at runtime — swapping candidates as dialogue progresses.

The module runs entirely inside Unity. No animation data is sent to Convai.

## How the System Works

Each frame the module reads two signals: the current **dialogue state** (idle, listening, thinking, speaking, reacting) and the current **emotion reading** from the Emotion module. It uses those signals to select and crossfade clips from a `DialogueAnimationLibrary` across a four-layer animator stack.

```mermaid
graph LR
    A[Dialogue State] --> C[ConvaiDialogueAnimationController]
    B[Emotion Reading] --> C
    C --> D[Layer 0: Base Idle]
    C --> E[Layer 1: Idle Overlay]
    C --> F[Layer 2: Body Talk]
    C --> G[Layer 3: Head Talk]
```

The four layers are additive and masked: the base idle plays continuously, the idle overlay adds variation, and the two talk layers fade in when the character speaks. Talk layer clips are routed by `DialogueTalkBodyCoverage` — clips can target head only, body only, or both simultaneously.

## Configuration Assets

The module is driven by four ScriptableObject types:

| Asset                            | Purpose                                                                             |
| -------------------------------- | ----------------------------------------------------------------------------------- |
| `DialogueAnimationLibrary`       | Pool of idle and talk clips, each tagged with emotion affinity and character gender |
| `DialogueAnimationRuntimeConfig` | Timing, blend durations, layer weights, and selection parameters                    |
| `DialogueAnimatorContract`       | Maps layer indices and state names to your Animator Controller                      |
| `ConvaiDialogueAnimationProfile` | Bundles the three assets above into a single character preset                       |

Three bundled profiles ship with the SDK: **Balanced**, **Expressive**, and **Subtle**. They cover most characters without custom authoring.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Quick Start</strong><br>Add the controller, assign a library and config, and see gesture animation in Play Mode.</td><td><a href="/broken/pages/749579ca90c5642a521545ecfb8a38801312161b">Broken link</a></td></tr><tr><td><strong>Animation Libraries &#x26; Profiles</strong><br>Author and configure DialogueAnimationLibrary, RuntimeConfig, and bundled Profile assets.</td><td><a href="/broken/pages/ddf05dd182e8070118b69660e1e2402406274705">Broken link</a></td></tr><tr><td><strong>Animator Controller Setup</strong><br>Wire your Animator Controller to the four-layer contract the module expects.</td><td><a href="/broken/pages/ae1d6461733ecfa8204b65061e9f0ef122c13ded">Broken link</a></td></tr><tr><td><strong>Usage Examples</strong><br>Inspector-only and scripted examples across training, medical, and corporate simulation scenarios.</td><td><a href="/broken/pages/f25409bd4283cc496195d5926bf38c7f1f18fde4">Broken link</a></td></tr><tr><td><strong>Scripting API</strong><br>Complete reference for ConvaiDialogueAnimationController properties and runtime swap methods.</td><td><a href="/broken/pages/5df0d73ec1bc7b8646a70cc77b28e455d37a7c36">Broken link</a></td></tr><tr><td><strong>Troubleshooting</strong><br>Symptom-driven fixes for silent talk layers, missing animation, and layer index errors.</td><td><a href="/broken/pages/33be83ff0bc50c3eca671d873c33036739e6e3ec">Broken link</a></td></tr></tbody></table>

## Next Steps

Follow the Quick Start to get the module running on your first character, then read Animation Libraries & Profiles to understand how to customize clip selection for your scenario.

{% content-ref url="/broken/pages/749579ca90c5642a521545ecfb8a38801312161b" %}
[Broken link](/broken/pages/749579ca90c5642a521545ecfb8a38801312161b)
{% endcontent-ref %}
