---
title: Migrate to 4.0.0-beta.27
description: Update an existing Unreal project from the previous plugin beta, covering every removed pin, retired enum, and Blueprint node that needs refreshing.
last_reviewed: "4.0.0-beta.27"
---

Moving a project from `4.0.0-beta.21` to <code class="expression">space.vars.unreal_plugin_version</code> takes a single pass through the Blueprints that touch Convai. Three changes break existing graphs: two Blueprint nodes lost pins, one enum was removed, and the goal-resolution node's pins were renamed. Nothing else in the range requires an edit. A project that only calls `Invoke Speech`, sends text, and plays lip sync compiles unchanged.

## Before you start

- Branch or back up the project. Blueprint pin removals cannot be undone by reinstalling the old plugin once assets are resaved.
- Confirm the engine version. The plugin supports Unreal Engine <code class="expression">space.vars.unreal_min_version</code> through <code class="expression">space.vars.unreal_max_version</code>.
- Upgrade in one step. There is no intermediate version to stop at between `4.0.0-beta.21` and <code class="expression">space.vars.unreal_plugin_version</code>.

{% hint style="warning" %}
Compile every Convai Blueprint before saving anything. A graph with a removed pin still opens, but the node carries an orphaned pin until it is refreshed, and saving in that state persists the broken connection.
{% endhint %}

## What changed

Two of these changes came from the same design decision: behavior that used to be set per call is now read from the chatbot's own configuration, so the per-call pins were removed. The third replaced a two-value movement enum with a richer model — an object reference plus optional designer-authored destinations — which made the old enum and its companion flag redundant.

## Breaking changes

| Old | New | What to do |
|---|---|---|
| The generate-actions input on `Invoke Speech` and `Invoke Narrative Design Trigger` (parameter `InGenerateActions`) | — | Remove the wire. Action generation now follows `Enable Actions` on the chatbot component. |
| The replicate-on-network input on `Invoke Speech` and `Invoke Narrative Design Trigger` (parameter `InReplicateOnNetwork`) | — | Remove the wire. Replication follows the chatbot component's own configuration. |
| `EConvaiMoveTarget` (`Actor as goal`, `Component as goal`) | `EConvaiObjectReference` (`Whole Actor`, `Specific Component`) | Rebuild any variable, cast, or `Switch on Enum` node against the new enum. The Details-panel field is now labelled **Object Is**. |
| `bStepOntoBounds` on `FConvaiObjectEntry` | — | Delete the check. `Whole Actor` already stops at the object's bounds. |
| `MoveTargetMode` on `FConvaiObjectEntry` | `ObjectReference` | Rename the field access. |
| `Out Mode` output on `Resolve Goal Location` | `Uses Destination` | Delete the branch. Wire `Target Actor` and `Destination` into a single `AI Move To`; `Target Actor` is `null` exactly when the goal is a fixed location. |
| `Out Goal Actor` output on `Resolve Goal Location` | `Object Actor` | Renamed, and no longer the pin to wire into `AI Move To`. Use `Target Actor` for movement. |
| `Out Goal Location` output on `Resolve Goal Location` | `Destination` | Renamed. |
| `bForceRefresh` input on `Resolve Goal Location` | — | Remove the wire. The node revalidates its resolved component on its own. |

`Invoke Speech` also gained a `Delivery` input (`Send Normally` or `Wait Until Conversation Is Idle`) and now speaks its message exactly once rather than leaving it in the conversation context. Neither is a breaking change, but both change what a reader observes after upgrading.

## Migrate the project

{% stepper %}
{% step %}
### Install the new plugin

Replace the plugin folder and restart the editor. See [Install the Convai plugin](../getting-started/install-the-convai-plugin.md).
{% endstep %}

{% step %}
### Refresh the nodes that lost pins

Open every Blueprint that calls `Invoke Speech` or `Invoke Narrative Design Trigger`. Right-click each node and select **Refresh Node**, then delete the wires that fed the two removed boolean inputs, `InGenerateActions` and `InReplicateOnNetwork`.
{% endstep %}

{% step %}
### Replace the removed enum

Search the project for `EConvaiMoveTarget`, `MoveTargetMode`, and `bStepOntoBounds`. Rebuild each `Switch on Enum` against `EConvaiObjectReference`, rename `MoveTargetMode` accesses to `ObjectReference`, and delete `bStepOntoBounds` checks outright.
{% endstep %}

{% step %}
### Rewire Resolve Goal Location

Refresh every `Resolve Goal Location` node. Remove the branch on the old `Out Mode` output and wire `Target Actor` and `Destination` into one `AI Move To` node. See [Built-in action handlers](../features/character-actions/built-in-action-handlers.md) for the current pattern.
{% endstep %}

{% step %}
### Compile and resave

Compile every touched Blueprint, then save. Resave only after a clean compile.
{% endstep %}
{% endstepper %}

## Verify the migration

The migration is complete when every Convai Blueprint compiles with no errors, a project-wide search for `EConvaiMoveTarget`, `MoveTargetMode`, `bStepOntoBounds`, and `Out Mode` returns nothing, and a character still walks to a registered object in Play mode.

If a Blueprint still fails to compile after the first four steps, the `Resolve Goal Location` rewiring is the usual cause: a graph that still branches on the removed `Out Mode` output cannot resolve that pin, and the error names the node rather than the missing output.

## Next steps

Two features arrived during this version range that an upgraded project can adopt immediately: spatial awareness, which replaced the retired per-object proximity mechanism, and the movement nodes that replaced hand-wired `AI Move To` graphs.

{% content-ref url="../features/spatial-awareness/README.md" %}
[Spatial awareness](../features/spatial-awareness/README.md)
{% endcontent-ref %}

{% content-ref url="../features/character-movement/README.md" %}
[Character movement](../features/character-movement/README.md)
{% endcontent-ref %}
