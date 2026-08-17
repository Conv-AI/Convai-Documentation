---
title: Convai Troubleshooter
description: Reference for the Convai Troubleshooter window, including how it reports findings, applies fixes, and lets a project add its own checks.
last_reviewed: "4.5.0"
---

The Convai Troubleshooter is an Editor window that lists what is stopping a `ConvaiCharacter` from working, module by module, with a fix beside each finding. Open it from `Convai → Troubleshooter` before reading the Unity Console when a character does not behave as expected — it is the SDK's first-line diagnostic.

## Open the Troubleshooter

Select `Convai → Troubleshooter` in the menu bar. The window opens on the `ConvaiCharacter` nearest the current Hierarchy selection — the selected object itself, or its nearest ancestor carrying `ConvaiCharacter`. With nothing selected, it falls back to the only `ConvaiCharacter` in the scene when there is exactly one.

The Troubleshooter also opens from elsewhere in the SDK: status chips in other Convai component inspectors open this same window already scrolled to the module the chip was reporting on, with the specific finding highlighted briefly. Selecting a different `ConvaiCharacter` in the Hierarchy while the window is open switches its report to that character automatically.

## Check one character or the whole scene

A toggle in the top-right corner of the window switches between two modes:

| Mode | What it shows |
| --- | --- |
| **This Character** | The report for one `ConvaiCharacter`, picked from the Hierarchy selection or from the **Character** object field |
| **This Scene** | A card for every `ConvaiCharacter` in the open scene — active and inactive — each with its worst finding and a status pill |

Selecting a card in **This Scene** mode switches back to **This Character** mode for that character. With no character selected, the window shows **Pick A Convai Character** and asks you to select one in the Hierarchy or the **Character** field. With **This Scene** selected and no `ConvaiCharacter` in the open scene, it shows **No Convai Characters**.

## Read a finding

Findings are grouped into a collapsible section per module. Each finding carries one of four severities:

| Severity | Meaning | Counts toward "N to fix"? |
| --- | --- | --- |
| `Error` | The module cannot do its job until someone acts | Yes |
| `Warning` | The module runs, but not as well as it could | Yes |
| `Info` | Worth knowing, but nothing is wrong | No — listed under **Checked And Fine** |
| `Ok` | Already correct; reported so a passing check is visible rather than assumed | No — listed under **Checked And Fine** |

A module's section header shows a right-aligned summary. When the module has no errors or warnings, the summary is a readiness phrase; otherwise it is an issue count:

| Module readiness | Section summary |
| --- | --- |
| Component not present on this character | `Not set up` |
| Present, but something stops it working entirely | `Blocked` |
| Present and unblocked, but nothing is configured to run | `Nothing will happen yet` |
| Set up and working | `Ready` |
| One or more errors or warnings present | `1 to fix` / `N to fix` |

The window's header chip mirrors this at the character level — `Nothing to fix`, or `1 to fix` / `N to fix` for the current character's combined issue count.

{% hint style="info" %}
In this release, `ConvaiActionSetupHealthProvider` (`SDK/Editor/Actions/ConvaiActionSetupHealthProvider.cs`) is the only module that reports through the full `IConvaiSetupHealthProvider` interface, so Actions findings are the only ones that can carry a **Fix**, **Show Me**, or **Open** button. Gaze, Body Animation, Body Language, Emotion, and Embodiment still register only as the older, read-only `IConvaiModuleSurveyor`. The Troubleshooter still shows a section for each of these when the module applies to the selected character — their findings are informational text, with no button attached.
{% endhint %}

## Act on a finding

A finding row shows up to four actions, depending on what the module that raised it supplied:

* **Fix** — runs the finding's one-click repair and records one Undo step
* **Show Me** — selects and pings the object the finding is about, in the Hierarchy or Project window
* **Open** — opens the authoring surface that answers the finding, such as the Actions Editor, focused on the relevant action
* **Learn More** — opens the finding's documentation link, when one is set

## Re-check and fix everything

The footer shows how long ago the report was built (a fresh-result label, `Checked N seconds ago`, or `Checked N min ago`) and a **Re-check** button that reruns every check immediately, ignoring the cached report.

A **Fix All** button appears in the footer whenever more than one finding across the whole report has a one-click fix. Pressing it opens a confirmation dialog listing every fix it is about to apply, then applies all of them as a single Undo step — `Ctrl+Z` reverts every one of them together. A module's own section shows a smaller **Fix These (N)** button under the same rule, scoped to the fixable findings visible in that section.

Everything that passed — `Ok` and `Info` findings — collapses into a **Checked And Fine** section at the bottom of the report, so a character with no issues can still be inspected rather than taken on trust.

## Report your own findings

A project can add its own checks to the Troubleshooter by implementing `IConvaiSetupHealthProvider` and registering it with `ConvaiSetupHealthRegistry.Register`. A registered provider's findings appear beside Convai's own, with the same **Fix**, **Show Me**, and **Open** support when the provider supplies them. Registration also makes the findings visible to the `Convai.InspectScene` and `Convai.ValidateSetup` MCP tools, so an AI coding assistant reads the same report a person sees in the window.

`IConvaiSetupHealthProvider` requires:

| Member | Description |
| --- | --- |
| `string ModuleId { get; }` | Stable dotted id, for example `myproject.quest-giver` |
| `string DisplayName { get; }` | What a user calls the module in the window |
| `int Order { get; }` | Where the section sits in the report; lower comes first |
| `bool AppliesTo(GameObject characterRoot)` | Whether this module has anything to say about the character; must be cheap |
| `ConvaiSetupHealthResult Inspect(GameObject characterRoot)` | Read-only report for the character; never mutates the scene |

{% code title="Assets/Editor/MyCustomSetupHealthProvider.cs" %}
```csharp
using Convai.Editor.AI;
using Convai.Editor.Diagnostics;
using UnityEditor;
using UnityEngine;

[InitializeOnLoad]
internal sealed class MyCustomSetupHealthProvider : IConvaiSetupHealthProvider
{
    static MyCustomSetupHealthProvider() =>
        ConvaiSetupHealthRegistry.Register(new MyCustomSetupHealthProvider());

    public string ModuleId => "myproject.quest-giver";
    public string DisplayName => "Quest Giver";
    public int Order => 100;

    public bool AppliesTo(GameObject characterRoot) =>
        characterRoot.GetComponent<QuestGiver>() != null;

    public ConvaiSetupHealthResult Inspect(GameObject characterRoot)
    {
        var questGiver = characterRoot.GetComponent<QuestGiver>();
        if (questGiver.ActiveQuest == null)
        {
            var finding = new ConvaiSetupFinding(
                id: "myproject.quest-giver.no-active-quest",
                severity: ConvaiModuleFindingSeverity.Warning,
                title: "No active quest",
                message: "This quest giver has no active quest, so it will not offer one.",
                fixLabel: "Assign default quest",
                fix: () => questGiver.ActiveQuest = QuestGiver.DefaultQuest);

            return new ConvaiSetupHealthResult(
                ModuleId, DisplayName, ConvaiCapabilityReadiness.Inert,
                summary: "No quest", findings: new[] { finding });
        }

        return new ConvaiSetupHealthResult(
            ModuleId, DisplayName, ConvaiCapabilityReadiness.Working,
            summary: questGiver.ActiveQuest.Title);
    }
}
```
{% endcode %}

Registration is idempotent — a provider registered again with the same `ModuleId` replaces the previous registration rather than duplicating it, so a domain reload never produces two sections for the same module.

## Next steps

Use the debug tools reference for the diagnostic surfaces that sit alongside the Troubleshooter — logging, latency metrics, and the per-module editor windows.

{% content-ref url="debug-tools-reference.md" %}
[Debug tools reference](debug-tools-reference.md)
{% endcontent-ref %}
