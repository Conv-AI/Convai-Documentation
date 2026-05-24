---
title: Dialogue Animation
description: Drive body and head gesture animation from dialogue state and emotion using a pooled clip library and an AnimatorOverrideController — no per-clip animator states required.
last_reviewed: "4.2.0"
---

The Dialogue Animation module drives body and head gesture animations on AI characters using dialogue state and detected emotion as inputs. It runs entirely inside Unity — no animation data is sent to Convai.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How Dialogue Animation works</strong><br>Understand the four-layer animator stack, clip injection mechanism, and how dialogue state and emotion drive animation.</td><td><a href="how-dialogue-animation-works.md">how-dialogue-animation-works.md</a></td></tr><tr><td><strong>Dialogue Animation quick start</strong><br>Add the controller, assign a library and config, and see gesture animation in Play Mode.</td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Animation libraries and profiles</strong><br>Author and configure DialogueAnimationLibrary, RuntimeConfig, and bundled Profile assets.</td><td><a href="animation-libraries-and-profiles.md">animation-libraries-and-profiles.md</a></td></tr><tr><td><strong>Animator Controller requirements</strong><br>Layer indices, required state names, placeholder clip names, and DialogueAnimatorContract field reference.</td><td><a href="animator-controller-requirements.md">animator-controller-requirements.md</a></td></tr><tr><td><strong>Build a compatible Animator Controller</strong><br>Step-by-step guide to creating a four-layer Animator Controller from scratch.</td><td><a href="animator-controller-setup.md">animator-controller-setup.md</a></td></tr><tr><td><strong>Dialogue Animation usage examples</strong><br>Inspector-only and scripted examples across training, medical, and corporate simulation scenarios.</td><td><a href="usage-examples.md">usage-examples.md</a></td></tr><tr><td><strong>Dialogue Animation scripting API</strong><br>Complete reference for ConvaiDialogueAnimationController properties and runtime swap methods.</td><td><a href="scripting-api.md">scripting-api.md</a></td></tr><tr><td><strong>Troubleshoot Dialogue Animation</strong><br>Symptom-driven fixes for silent talk layers, missing animation, and layer index errors.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>

## Next steps

Follow the Quick Start to get the module running on your first character, then read Animation Libraries & Profiles to understand how to customize clip selection for your scenario.

{% content-ref url="quick-start.md" %}
[Dialogue Animation quick start](quick-start.md)
{% endcontent-ref %}
