---
title: Tune body animation personality
description: Give one character its own animation settings, choose an archetype, and tune gestures, calmness, and ambient activity without changing shared content.
last_reviewed: "5.0.0-preview"
---

Use the Body Animation Inspector's **Personality** controls for everyday tuning. The animation set supplies clips; the config controls how they are selected and blended.

## Create or isolate settings

{% stepper %}
{% step %}
### Open Personality

Complete [Body animation quick start](quick-start.md), then open **Personality** on the configured controller. **Using SDK Defaults** means the runtime is working without a personal config asset.
{% endstep %}
{% step %}
### Give the character its own settings

Select **Give This Character Its Own Settings** to create `<Character>_BodyAnimationSettings.asset` and assign it through the character's profile/config path. Inspect the copy receipt for the actual project location.

If a project config is shared, read the ownership notice. Choose **Make Unique For This Character** when the change should affect only this character. Editing package content through the supported controls creates an editable project copy rather than changing the package asset.
{% endstep %}
{% step %}
### Choose an archetype and tune

Choose **Composed**, **Warm**, **Energetic**, or **Reserved**, then adjust **How expressive** and **How calm**. Enable **Keeps busy when alone** only when the set contains Ambient-tagged actions; **How often** controls their average interval.
{% endstep %}
{% step %}
### Verify in Play mode

Compare idle, short speech, long speech, and unengaged behavior. Use the Editor's Live mode to inspect selection and weight if the difference is unclear. Confirm that another character sharing the old config did not change when you intended a personal edit.
{% endstep %}
{% endstepper %}

## Archetype values

| Archetype | Gesture liveliness | Calmness | Ambient interval |
| --- | --- | --- | --- |
| Composed | 0.7 | 1.4 | 30 s |
| Warm, the SDK default | 1 | 1 | 20 s |
| Energetic | 1.5 | 0.6 | 12 s |
| Reserved | 0.4 | 1.6 | 45 s |

Applying an archetype writes these three values, not all config fields. It does not enable ambient activity or create clips. For movement performances, separately enable turn-in-place or planted stops with suitable measured content. For lower-level timing and overlay controls, open **Advanced settings & content → > Feel**.

## Next steps

{% content-ref url="config-reference.md" %}
[Body animation config reference](config-reference.md)
{% endcontent-ref %}
{% content-ref url="body-animation-editor.md" %}
[Body Animation Editor](body-animation-editor.md)
{% endcontent-ref %}
