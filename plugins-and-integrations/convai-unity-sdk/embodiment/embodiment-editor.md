---
title: Embodiment Editor window
description: Reference for the Convai Embodiment Editor window, covering the Setup, Presets, and Live tabs and what each one shows about a character.
last_reviewed: "4.5.0"
---

The Convai Embodiment Editor is a `Convai/Embodiment Editor` window with three tabs: `Setup`, `Presets`, and `Live`. Its subtitle reads "Set up a character's gaze, emotion and body." Use it to check whether a character's rig and modules are configured correctly, to see every `ConvaiEmbodimentPreset` in the project, and to watch a running character's conversation and emotion state during Play mode.

## Open the window

Select **Convai > Embodiment Editor** to open the window.

At the top of the window, a **Follow Selection** toggle (tooltip: "Track whatever character is selected in the scene.") controls which character the window inspects. When enabled, the window follows whatever `GameObject` is selected in the Hierarchy — resolving up to the nearest `ConvaiCharacter` if the selection is a child object. When disabled, drag a `GameObject` into the character field manually.

Below the character picker, the three tabs read, in order: `Setup`, `Presets`, `Live`.

## Setup tab

The `Setup` tab (tooltip: "Get this character's expressive features working.") shows two sections for the selected character.

### Rig

The `Rig` section header shows one of three status words, taken from the worst finding reported for the character:

| Header status | Meaning |
|---|---|
| `Ready` | Nothing wrong was found. |
| `Needs Attention` | The character still works, but not as well as it could — for example, a low-confidence face rig detection. |
| `Not Set Up` | The character will not behave correctly until the listed issue is fixed — for example, no `ConvaiCharacter` component. |

Below the header, the tab lists each finding as a short title and message. Findings include: the face rig's detected `RigConvention` and its detection confidence, whether facial meshes were found, and whether the `Head`, `LeftEye`, and `RightEye` bones resolved. A finding that can be corrected automatically shows a fix button next to it, such as **Set Up Rig Now** or **Add Convai Character**.

A **Set Up This Character** button at the bottom of the section adds a `StandardRigBinding` component if the character does not already have one, then rebuilds it.

### Features

The `Features` section lists every embodiment module registered in the project — `Conversation Flow`, `Gaze`, `Body Animation`, `Body Language`, and `Emotion` — one row per module. Each row shows the module's display name and a status indicator for whether the module's controller component is present on the character:

- **Present** — the row shows a **Select** button that selects the component in the Inspector.
- **Absent** — the row shows an **Add** button that adds the module's controller component to the character.

## Presets tab

The `Presets` tab (tooltip: "Preset assets in this project and whether they are valid.") opens with an info box: "Presets Are Optional — A preset hands one set of settings to each feature at once. Every feature also works on its own, so presets are optional."

Below it, the tab lists every `ConvaiEmbodimentPreset` asset found in the project. If none exist, the tab shows "No presets in this project." and a **Create A Preset** button that opens a save dialog for a new preset asset.

Each listed preset shows a status pill using the same three-word vocabulary as the `Setup` tab's `Rig` section (`Ready`, `Needs Attention`, `Not Set Up`), computed by inspecting the preset's slots: duplicate module IDs, slots with no matching feature installed, slots pointing at the wrong profile type, and — when the window is also tracking a character — features present on that character but missing from the preset, or slots naming a feature the character does not have. Selecting **Open** on any row selects the preset asset so its full diagnostics and slot list are visible in the Inspector.

## Live tab

The `Live` tab (tooltip: "What the character is doing right now, in Play Mode.") only reports state while the Unity Editor is in Play mode.

| Condition | What the tab shows |
|---|---|
| Not in Play mode | "Enter Play Mode to watch the character's live state." |
| In Play mode, no running `EmbodimentContext` resolved for the selected character | "No Running Character Selected — Select a running Convai character to see what it is doing." |
| In Play mode, a character is resolved | The `Conversation` and `Emotion` sections below. |

### Conversation

If the character has no Conversation Flow module, the section shows "Conversation Flow is not on this character." Otherwise it reads the module's current `DialogueStateReading` and shows:

- **State** — the current `DialogueState` value.
- **Blending To** — the state the character is transitioning toward.
- A progress bar labeled with the blend weight between the two states.
- **Time In State** — seconds spent in the current state.
- **Energy** — the current energy level.

### Emotion

If the character has no Emotion module, the section shows "Emotion is not on this character." If the module is present but has not detected anything yet, it shows "No emotion detected yet." Otherwise it shows up to five emotion labels as progress bars, strongest first, each labeled with the emotion name and its score.

The `Live` tab refreshes automatically about ten times per second while it is the active tab and the Editor is in Play mode.

## Next steps

{% content-ref url="character-rig-setup.md" %}
[character-rig-setup.md](character-rig-setup.md)
{% endcontent-ref %}

{% content-ref url="embodiment-presets.md" %}
[embodiment-presets.md](embodiment-presets.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[troubleshooting.md](troubleshooting.md)
{% endcontent-ref %}
