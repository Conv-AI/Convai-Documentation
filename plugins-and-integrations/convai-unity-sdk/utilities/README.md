# Utilities

Utilities are opt-in modules that run entirely inside Unity. They add richness to AI characters — lifelike animation, eye tracking, head movement — without sending any data to Convai. Each utility is independent: you can add one without the other, and neither requires any Feature modules to be present.

## Utilities vs. Features

|                           | Features                                                  | Utilities                               |
| ------------------------- | --------------------------------------------------------- | --------------------------------------- |
| **What they do**          | Extend what an AI character can perceive and reason about | Enhance how a character looks and moves |
| **Backend communication** | Yes — send and receive data via Convai                    | No — run entirely within Unity          |
| **Examples**              | Actions, Emotion, Long-Term Memory, Vision                | Dialogue Animation, Gaze & Attention    |
| **Dependencies**          | Require Convai session to be active                       | Work independently of session state     |

## Available Utilities

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Dialogue Animation</strong><br>Drive character body and head animations from dialogue state and detected emotion.</td><td><a href="/broken/pages/c2f0f7aacc00f17a4a6476388f5edfe059d6074e">Broken link</a></td></tr><tr><td><strong>Gaze &#x26; Attention</strong><br>Give characters lifelike eye tracking, head rotation, saccades, blinks, and intelligent focus selection.</td><td><a href="/broken/pages/78cfd898399d26a4156efe673859abadeed71d76">Broken link</a></td></tr></tbody></table>
