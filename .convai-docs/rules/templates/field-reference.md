---
title: Knowledge Bank fields
description: Reference for each field on the Knowledge Bank tab of the character editor, with what it changes, its default, and the limit it enforces.
last_reviewed: "<source commit you verified the fields against>"
---

<!--
FIELD REFERENCE TEMPLATE. A reference shape: every field on one panel of a product interface.
Be austere. Mirror the panel: one table per section or sub-tab, rows in the order the screen shows them.
Write each label in bold, spelled exactly as the product spells it, with the panel's own label in
the heading even when the page title differs. Take labels, defaults, limits and messages from the
source the subject file names. Say what a field changes about the character; never restate its label.
A limit the product fetches from Convai at runtime is written as set by Convai, never as the
fallback number in the code. A default or limit you cannot verify is not written; it becomes a
question for the subject's owner. No steps: link to the interface task page for the task.
Replace all content. No body `#`. Delete this comment before publishing.
-->

The **<Tab label>** tab of the character editor holds <what the fields on this tab control, as a fact>.

## <Section or sub-tab label> fields

| Field | What it changes | Default | Limit | Required |
|---|---|---|---|---|
| **<Field label>** | <What changes about the character when this is set.> | <Default, or "None"> | <Limit, or "Set by Convai"> | <Yes or No> |
| **<Field label>** | <What changes about the character.> | <Default> | <Limit> | <Yes or No> |

## <Next section or sub-tab label> fields

<The next table, in the order the screen shows the sections.>

## Messages on this tab

| Message | Shown when |
|---|---|
| `<Exact message text>` | <Condition, as the reader causes it.> |

## Related pages

{% content-ref url="<interface-task-page>.md" %}
[<Interface task page title>](<interface-task-page>.md)
{% endcontent-ref %}
