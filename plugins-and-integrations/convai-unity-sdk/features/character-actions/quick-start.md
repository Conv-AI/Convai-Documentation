---
title: Character actions quick start
description: >-
  Add a ready-made action to a Convai character from the Actions Editor's
  starter catalog, with no scripting, and confirm it runs in Play mode.
last_reviewed: "4.5.0"
---

Open the Actions Editor and add one of its four ready-made starter actions to a Convai character, with no scripting required. By the end, the character responds to a natural-language request — such as "look at the chair" — by physically performing the behavior in your scene.

## Prerequisites

* [ ] A `ConvaiCharacter` component already on your NPC's `GameObject`, connecting and responding to conversation.
* [ ] At least one scene object the character should be able to act on.

## The four starter actions

The Actions Editor offers the same four starters to every character that has no actions yet, ranked in this order:

| Starter | Adds | Needs on the character | What it does |
| --- | --- | --- | --- |
| Walk To Target | `ConvaiWalkToActionExecutor` | `ConvaiNavMeshLocomotion` and a baked NavMesh | Walks to the named object, person, or place and stops nearby |
| Follow The Player | `ConvaiFollowPlayerActionExecutor` | `ConvaiNavMeshLocomotion` and a baked NavMesh | Follows the player at a comfortable distance until told to stop |
| Look At Target | `ConvaiLookAtActionExecutor` | `ConvaiGazeController` (Gaze module) | Turns the character's eyes, head, and body toward a named target |
| Play Gesture | `ConvaiPlayGestureActionExecutor` | `ConvaiBodyAnimationController` (Body Animation module) | Plays a named gesture from the character's Animation Set |

This page uses **Look At Target**: it needs no NavMesh bake, and the result — the character turning to look at something — is immediately obvious in Play mode. Walk To Target and Follow The Player need a NavMesh baked in the scene (**Window > AI > Navigation**) before the character can actually reach anywhere; pick one of those instead once your scene has one.

## Add the Look At Target starter

{% stepper %}
{% step %}
### Mark a target object

Select the object the character should look at — for example a chair. Click **Add Component**, search for **Convai Action Target** (`Convai/Actions/Convai Action Target`), leave **Kind** as `Object`, and give it a clear **Name**, for example `chair`.
{% endstep %}

{% step %}
### Open the Actions Editor

Select **Convai > Actions Editor**. The window opens with the scene's only `ConvaiCharacter` picked automatically — pick a different one from the **Character** field in the toolbar if your scene has more than one.
{% endstep %}

{% step %}
### Enable actions on the character

If this is the character's first action, the window shows a one-step prompt: click **Enable Actions**. This adds `ConvaiActionConfigSource` (labeled **Convai Actions** in the Inspector) to the character — one click, fully undoable.
{% endstep %}

{% step %}
### Add the Look At Target starter

With no actions yet, the window shows four starter cards: **Walk To Target**, **Follow The Player**, **Look At Target**, and **Play Gesture**. Select **Look At Target**.

Convai creates a `Look At` action pre-filled from the starter, adds `ConvaiLookAtActionExecutor` to the character, and — since the character has no `ConvaiGazeController` yet — adds that too, in the same undoable step.
{% endstep %}

{% step %}
### Add a Convai Action Runner

Switch the mode selector under the character picker from **Actions** to **Character Settings**. If no dispatcher is listed, click **Add Action Runner** to add `ConvaiActionDispatcher` (labeled **Convai Action Runner** in the Inspector) to the character.
{% endstep %}
{% endstepper %}

## Verify the setup

Switch back to the **Actions** mode and select the `Look At` action in the left pane. Its **Try It** box lets you run the action without starting a conversation:

* **In Edit mode**, this is a **Preview**: type `chair` into the dry-run field and confirm it resolves to the target you marked.
* **In Play mode**, this is a **Test Run**: pick `chair` from **Valid Targets** and click **Run Now**. The character should turn toward the chair immediately, with no conversation and no backend call involved.

{% hint style="success" %}
**Expected result:** enter Play mode and say "look at the chair." The character's eyes, head, and body turn toward it, and the action reports success as soon as the gaze settles.
{% endhint %}

If the character does not turn, open [Troubleshoot character actions](debugging-and-troubleshooting.md) for the diagnostic checklist, or select **Convai > Troubleshooter** for a one-click, checklist-style diagnosis of the whole character.

## Next steps

{% content-ref url="actions-editor.md" %}
[Actions Editor](actions-editor.md)
{% endcontent-ref %}

{% content-ref url="action-executors.md" %}
[Action executors](action-executors.md)
{% endcontent-ref %}

{% content-ref url="writing-custom-executors.md" %}
[Write a custom action executor](writing-custom-executors.md)
{% endcontent-ref %}
