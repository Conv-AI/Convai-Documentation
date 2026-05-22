---
title: Utilities
description: Opt-in presentation modules that enhance character animation, eye tracking, and head movement — running entirely in Unity with no data sent to Convai.
last_reviewed: "4.2.0"
---

Utilities are opt-in modules that enhance how AI characters look and move. They run entirely inside Unity — no data is sent to Convai, and they operate independently of the session lifecycle.

Unlike features, which extend character perception and reasoning by communicating with Convai, utilities focus on visual and behavioral presentation: gesture animation driven by emotion and dialogue state, eye tracking, and natural head movement. Both modules work with or without an active Convai session and can be added to any character that already has a `ConvaiCharacter` component.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Dialogue Animation</strong><br>Drive body and head gesture layers from dialogue state and detected emotion using pooled animation clips — no per-clip animator states required.</td><td><a href="dialogue-animation/README.md">dialogue-animation/README.md</a></td></tr><tr><td><strong>Gaze &amp; Attention</strong><br>Add eye tracking, head rotation, saccades, blinks, and intelligent focus selection with a two-stage Attention → Gaze pipeline.</td><td><a href="gaze-and-attention/README.md">gaze-and-attention/README.md</a></td></tr></tbody></table>
