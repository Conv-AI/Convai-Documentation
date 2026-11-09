---
title: Actions Editor
description: Reference for the Convai Actions Editor window — its four modes, the Add Action catalog, and one-click executor provisioning.
last_reviewed: "5.0.0-preview"
---

The Convai Actions Editor authors what a Convai character can do — every action's name, description, and bound executor — without editing `ConvaiActionConfigSource` directly. Adding a built-in executor from its catalog also provisions the peer component the executor needs, such as `ConvaiGazeController` or `ConvaiBodyAnimationController`, in the same undoable step.

## Open the window

Select **Convai > Actions Editor** to open the window. A **Character** field in the toolbar picks which `ConvaiCharacter`'s actions the window shows, and auto-selects the scene's only character when there is one.

## Modes

A mode switcher under the character picker moves between four views of the same character:

| Mode | Shows |
| --- | --- |
| **Actions** | The default view: the action list and the selected action's detail. |
| **Scene Knowledge** | **Find Targets In Your Scene**, **Add From Your Scene**, **Known Objects**, **Known Characters**, initial attention, and **Sent To Convai** payload preview. Known entries include **Scene Object** and **Extras** for aliases and interaction points. |
| **Character Settings** | **Running Actions** (**Actions Are Run By**), **How Actions Run**, **Reactions & Interruptions**, **Action Feedback**, and **Events**. |
| **Live** | **Now Performing**, **Timeline**, **Scene Knowledge — Live**, **Commands That Never Ran**, **Feedback Log**, **Insights**, and separate expandable cards under **Advanced**. Automatically selected on entering Play mode only if the character has an Action Runner in its hierarchy. The prior mode is restored on leaving Play mode; the retained recording is labeled **Session Review**. |

Editing is disabled, with an explanatory banner, in every mode except **Live** while the Editor is in Play mode.

## Action list and detail

The left pane lists one card per action, grouped as **This Character** (actions authored directly on this character) followed by one collapsible group per assigned `ConvaiActionSet`. Selecting a card opens its detail in the right pane, in four boxes:

| Box | Shows |
| --- | --- |
| **Command** | **Name**, **Description**, **Target** (`No target`, `Object`, `Character`, `Either`), **When It Finishes**, **Offer This Action**, and **Command Preview**. |
| **Scene Behavior** | The bound executor component and its resolved status, a dropdown of every `IConvaiActionExecutor` found on the character's hierarchy, and an object-field fallback. |
| **Try It** | Runs the action without starting a conversation — see [Test an action without a conversation](#test-an-action-without-a-conversation) below. |
| **Advanced** (collapsed by default) | Parameter rows, **Timeout (Seconds)**, **If This Fails**, **Wait For Speech To Finish**, and **Delay After Speech (Seconds)**. |

## Toolbar

Use **Search actions…** to filter names. **Show** offers **All Actions**, **Needs Attention**, **Not Offered**, **This Character**, and **From Action Sets**. **Group** organizes cards by **Source**, **Category**, **Status**, or **Behavior**. Categories select Category grouping automatically only while grouping remains the uncustomized Source default.

Ctrl/Shift selection enables bulk editing. **Extract To Action Set** and **New Action Set…** create reusable definitions. **Export Actions…**, **Export Actions + Scene Knowledge…**, and **Import Actions…** exchange authored configuration as JSON.

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
2. The executor component is added to the configured action behaviors object (the character root unless a child is assigned), or reused if a matching component already exists on the character's hierarchy.
3. If the executor declares a `RequiredPeerHint` — for example `ConvaiGazeController` or `ConvaiNavMeshLocomotion` — and the character has no matching component yet, that component is added on the character root; an existing child peer is reused.
4. The new definition is bound to the added or reused executor and appended to the character's action list.

This is what lets the **Look At Target** starter add both `ConvaiLookAtActionExecutor` and `ConvaiGazeController` in one click, and **Walk To Target** add both `ConvaiWalkToActionExecutor` and `ConvaiNavMeshLocomotion`. A component required on the *target* object rather than the character — such as `ConvaiActionTargetGroup` for Count Target Group — is not provisioned this way, since choosing which scene object owns it is an authoring decision the window cannot make on your behalf.

If an executor's peer component is resolvable but was not added automatically — for example, an action created through **Custom (Empty)** and bound to an executor afterward — the **Scene Behavior** box offers a one-click **Add & Bind** button naming the executor, for example **Add & Bind Look At Target**.

## Test an action without a conversation

The selected action's **Try It** box runs the real dispatch path with no backend call:

* **In Edit mode**, enter a phrase in **Try A Target Name** and select **Check** to inspect the target-resolution result.
* **In Play mode**, choose **Target**, fill **Values To Send**, and select **Run Now**. This runs local dispatch and reports the result and duration. The explicit test can bypass **Offer This Action** being disabled; that does not make the action available to normal incoming commands.

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
