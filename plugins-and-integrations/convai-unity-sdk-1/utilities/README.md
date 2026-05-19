---
description: >-
  Presentation modules that enhance character animation, eye tracking, and head
  movement.
---

# Utilities

## Character Presentation Utilities

Utilities are opt-in modules that enhance how AI characters look and move. They run entirely inside Unity — no data is sent to Convai, and they operate independently of the session lifecycle.

Unlike features, which extend character perception and reasoning by communicating with Convai, utilities focus on visual and behavioral presentation: gesture animation driven by emotion and dialogue state, eye tracking, and natural head movement.

Both utilities work with or without an active Convai session and can be added to any character that already has a `ConvaiCharacter` component.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Dialogue Animation</strong><br>Drive body and head gesture layers from dialogue state and detected emotion using pooled animation clips — no per-clip animator states required.</td><td><a href="/broken/pages/7eac05bde76be83d7586d87ed81d70b96b38e1a0">Broken link</a></td></tr><tr><td><strong>Gaze &#x26; Attention</strong><br>Add eye tracking, head rotation, saccades, blinks, and intelligent focus selection with a two-stage Attention → Gaze pipeline.</td><td><a href="/broken/pages/f14b7d08793d9f91583c0749744f54efc69dbb1d">Broken link</a></td></tr></tbody></table>

## Next Steps

Start with Dialogue Animation to add body and head gestures, then layer in Gaze & Attention to bring natural eye contact and head tracking to life. Both can be used independently or together.
