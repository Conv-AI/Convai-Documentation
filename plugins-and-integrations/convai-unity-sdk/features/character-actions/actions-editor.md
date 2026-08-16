---
title: Actions Editor
description: Reference for the Convai Actions Editor window — its four modes, the Add Action catalog, and one-click executor provisioning.
last_reviewed: "4.5.0"
---

The Convai Actions Editor authors what a Convai character can do — every action's name, description, and bound executor — without editing `ConvaiActionConfigSource` directly. Adding a built-in executor from its catalog also provisions the peer component the executor needs, such as `ConvaiGazeController` or `ConvaiBodyAnimationController`, in the same undoable step.

## Open the window

Select **Convai > Actions Editor** to open the window. A **Character** field in the toolbar picks which `ConvaiCharacter`'s actions the window shows, and auto-selects the scene's only character when there is one.

## Modes

A mode switcher under the character picker moves between four views of the same character:

| Mode | Shows |
| --- | --- |
| **Actions** | The default view: the action list and the selected action's detail. |
| **Scene Knowledge** | The character's Known Objects, Known Characters, and initial attention. |
| **Character Settings** | The `ConvaiActionDispatcher` (labeled **Convai Action Runner**) and `ConvaiActionFeedbackRelay` settings. |
| **Live** | Play-mode-only: the batch currently running, a timeline of recent batches, and per-action run counts. Selects itself automatically when Play mode starts, and relabels **Session Review** after Play mode ends while the last session's recording is still available. |

Editing is disabled, with an explanatory banner, in every mode except **Live** while the Editor is in Play mode.

## Action list and detail

The left pane lists one card per action, grouped as **This Character** (actions authored directly on this character) followed by one collapsible group per assigned `ConvaiActionSet`. Selecting a card opens its detail in the right pane, in four boxes:

| Box | Shows |
| --- | --- |
| **Command** | The action's name, description, and a live rendered preview in the form `This Convai Character can be asked to: "..."`. |
| **Scene Behavior** | The bound executor component and its resolved status, a dropdown of every `IConvaiActionExecutor` found on the character's hierarchy, and an object-field fallback. |
| **Try It** | Runs the action without starting a conversation — see [Test an action without a conversation](#test-an-action-without-a-conversation) below. |
| **Advanced** (collapsed by default) | Parameters, valid targets, timeout, failure-policy override, and the speech gate. |

## Add Action catalog

Click **+ Add Action ▾** in the toolbar to open the catalog. It lists every executor carrying `[ConvaiActionArchetype]` — shipped, sample, or project-defined — in a fixed order built by `ConvaiActionArchetypeCatalog.BuildMenuItems()`:

1. **Recommended** — the curated built-in executors that declare a `FeaturedOrder`, sorted by that order.
2. **More Ready-Made Actions** — the remaining shipped executors, alphabetical.
3. **Sample Actions** — executors that ship as SDK samples, in their own submenu.
4. **Project & Package Actions** — third-party or project-defined executors, grouped into a submenu per family.

A **Custom (Empty)** entry at the end starts a blank action with no preset name, behavior, or parameters. Project-defined executors can never push the curated **Recommended** section down the list — built-ins always sort first, regardless of how many project-specific executors exist.

## Starter cards

A character with no actions yet shows an "Add your first action" hero in place of the action list, with four one-click starter cards. Each is a built-in executor that declares itself a starter through `FeaturedOrder` 1–4:

| Order | Starter | Executor |
| --- | --- | --- |
| 1 | Walk To Target | `ConvaiWalkToActionExecutor` |
| 2 | Follow The Player | `ConvaiFollowPlayerActionExecutor` |
| 3 | Look At Target | `ConvaiLookAtActionExecutor` |
| 4 | Play Gesture | `ConvaiPlayGestureActionExecutor` |

Selecting a starter card provisions the executor exactly like picking it from **+ Add Action ▾** — see [One-click provisioning](#one-click-provisioning) below. **Browse all ready-made actions…**, next to the starter cards, opens the same catalog the toolbar button does.

## One-click provisioning

Adding a built-in executor — from a starter card or from the catalog — runs as a single undoable operation:

1. A new `ConvaiActionDefinition` is built from the executor's `[ConvaiActionArchetype]` attribute: its action name, description, target requirement, and any parameters.
2. The executor component is added to the character, or reused if a matching component already exists on the character's hierarchy.
3. If the executor declares a `RequiredPeerHint` — for example `ConvaiGazeController` or `ConvaiNavMeshLocomotion` — and the character has no matching component yet, that component is added too.
4. The new definition is bound to the added or reused executor and appended to the character's action list.

This is what lets the **Look At Target** starter add both `ConvaiLookAtActionExecutor` and `ConvaiGazeController` in one click, and **Walk To Target** add both `ConvaiWalkToActionExecutor` and `ConvaiNavMeshLocomotion`. A component required on the *target* object rather than the character — such as `ConvaiActionTargetGroup` for Count Target Group — is not provisioned this way, since choosing which scene object owns it is an authoring decision the window cannot make on your behalf.

If an executor's peer component is resolvable but was not added automatically — for example, an action created through **Custom (Empty)** and bound to an executor afterward — the **Scene Behavior** box offers a one-click **Add & Bind** button naming the executor, for example **Add & Bind Look At Target**.

## Test an action without a conversation

The selected action's **Try It** box runs the real dispatch path with no backend call:

* **In Edit mode**, it is a **Preview**: type a phrase into the dry-run field and it is checked against the same target-resolution ladder the runtime uses, showing which target it would match and at which step.
* **In Play mode**, it is a **Test Run**: pick a target from **Valid Targets**, fill in any parameters, and click **Run Now**. The run goes through the exact same dispatcher path a real Convai command takes, and reports ✓ or ✗ with a duration and, on failure, a reason.

## Next steps

{% content-ref url="quick-start.md" %}
[Character actions quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="action-executors.md" %}
[Action executors](action-executors.md)
{% endcontent-ref %}

{% content-ref url="configuring-actions.md" %}
[Configure character actions](configuring-actions.md)
{% endcontent-ref %}
