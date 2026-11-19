---
title: Configure narrative template keys
description: >-
  Set narrative template keys so a Convai character can reference runtime values
  — player name, scenario parameters, or session state — in its objectives.
last_reviewed: "5.0.0-pre.1"
---

Template keys are runtime key-value pairs that fill placeholders in your character's narrative objectives. Define placeholders in the [Convai dashboard](https://convai.com) using curly-brace syntax — for example, `{PlayerName}` or `{CurrentTask}` — and the SDK sends the actual values from Unity at runtime, so the character can reference them naturally in conversation. A single narrative graph can then serve many sessions with different participants or dynamic state without editing the graph each time.

## Define keys in the Inspector

Open `ConvaiNarrativeDesignManager` in the Inspector and expand the **Template Keys** foldout.

Click **+** to add an entry. Each entry has two fields:

| Field     | Description                                                                                                                    |
| --------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Key**   | The placeholder name, exactly as written in the narrative design section objective (case-sensitive, without the curly braces). |
| **Value** | The initial value. You can override this at runtime from code.                                                                 |

See the current manager Inspector in [Configure the narrative design manager](setting-up-the-narrative-design-manager.md).

At startup, the manager sends named Inspector entries through the character’s narrative API. In Play mode, select **Send to Server** to send the Inspector values again.

## Update keys at runtime

Use `character.NarrativeDesign.SetTemplateKey` for one value or `SetTemplateKeys` for a batch. The character API merges values by key. This example sets two values before the narrative uses them.

```csharp
// Method-body fragment. Import System.Collections.Generic.
bool accepted = character.NarrativeDesign.SetTemplateKeys(new Dictionary<string, string>
{
    ["PlayerName"] = "Alex",
    ["ScenarioPhase"] = "Handwashing"
});
```

`TemplateKeys` exposes the character’s locally tracked values. Use the exact case and spelling from the narrative placeholder, without the braces. Blank names are refused. An empty value is valid.

## Verify the update

The character sends the values when it can. In an ordinary shared room, it holds them until ready and selected. The SDK replays tracked keys on the next connection after disconnect. A `true` return means the update was sent or held locally. Check `Events.OnServerCommandResultReceived` for `update-template-keys` and exercise the relevant narrative objective to verify the result.

## Next steps

{% content-ref url="scripting-narrative-design.md" %}
[Narrative design scripting reference](scripting-narrative-design.md)
{% endcontent-ref %}
