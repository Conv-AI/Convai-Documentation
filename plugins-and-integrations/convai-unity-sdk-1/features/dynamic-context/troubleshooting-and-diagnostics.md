---
description: >-
  Diagnose Dynamic Context issues with a five-step checklist, a symptom table, a
  character-not-responding decision tree, and the full Console log reference.
---

# Troubleshooting & Diagnostics

## Diagnosing Dynamic Context Issues

Most Dynamic Context problems fall into one of three categories: incorrect timing (calling `Apply()` before a conversation starts), a misconfigured component (missing `ConvaiCharacter` reference or empty required field), or a misunderstanding of what `Reset()` clears. Work through the first-line investigation checklist below — most issues resolve at step 2 or 3.

***

## First-Line Investigation

{% stepper %}
{% step %}
**Check the Unity Console for Warnings**

`ConvaiDynamicContextCommand` logs a warning with the full validation message every time `Execute()` is skipped. Open the Console (**Window → General → Console**) and look for messages tagged `[ConvaiDynamicContextCommand]`.

If you see a warning, find the exact message in the [Console Log Reference](troubleshooting-and-diagnostics.md#console-log-reference) table below and follow the listed fix.
{% endstep %}

{% step %}
**Use the Sample UI to Isolate the Issue**

Before debugging your own integration, verify that the Dynamic Context system itself is working by using the SDK's built-in test UI.

**Prefab path:** `Packages/com.convai.convai-sdk-for-unity/Prefabs/SampleDynamicContextUI.prefab`

Drop it into your scene, assign your `ConvaiCharacter`, enter Play Mode, and use the **Set State** button to send a known value. If the character responds correctly through the Sample UI, the issue is in your integration code — not in the Dynamic Context system itself.
{% endstep %}

{% step %}
**Verify the Character Reference Is Resolved**

Select the `ConvaiDynamicContextCommand` component in the Inspector. If the **Target** section shows a yellow warning, the component cannot find a `ConvaiCharacter`.

* **Auto Resolve Character enabled:** confirm that `ConvaiDynamicContextCommand` and `ConvaiCharacter` are on the **same GameObject**.
* **Auto Resolve Character disabled:** confirm that the **Character** field has a reference assigned.
{% endstep %}

{% step %}
**Check Whether the Character Was in a Conversation**

Context updates sent via `Apply()` are discarded if the character is not in an active conversation. A warning is emitted through the Convai logger — enable Convai debug logging to see it in the Unity Console.

If you are calling `Apply()` in `Awake()`, `Start()`, or before the session connects, switch to `SetState` or `AddEvent` instead. These methods queue automatically and flush when the conversation begins.
{% endstep %}

{% step %}
**Check the Reaction Mode**

If a context update reached the character but it did not respond immediately, verify the **Reaction Mode** setting.

* **`SyncOnly`** — context is stored silently. The character incorporates it into its next natural turn. No immediate response is generated. This is expected behavior.
* **`Auto`** — Convai decides whether to respond. For guaranteed immediate response, use `ReactImmediately`.
* **`ReactImmediately`** — always triggers an immediate LLM turn after the update.
{% endstep %}
{% endstepper %}

***

## Common Issues

| Symptom                                                                | Likely Cause                                                 | Fix                                                                                                                       |
| ---------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Character does not reference context updates at all                    | `Apply()` called before conversation started                 | Switch to `SetState` or `AddEvent` — they queue automatically                                                             |
| Character does not respond immediately after update                    | Reaction mode is `SyncOnly`                                  | Change **Reaction Mode** to `Auto` or `ReactImmediately`                                                                  |
| **On Execution Skipped** fires instead of **On Executed**              | Validation failure — see Console warning                     | Check the [Console Log Reference](troubleshooting-and-diagnostics.md#console-log-reference) for the exact message and fix |
| Inspector shows yellow warning on the component                        | No `ConvaiCharacter` resolved                                | Enable **Auto Resolve** and place both components on the same GameObject, or assign **Character** explicitly              |
| `TryGetStateValue` returns `false` after `Apply()`                     | `Apply()` bypasses the local tracker                         | Use `SetState` if the value needs to be queryable via `TryGetStateValue`                                                  |
| Two `context-update` messages sent for one `SetState` call             | Existing state was updated — expected behavior               | Not a bug. See [Two Messages for One Update](troubleshooting-and-diagnostics.md#two-messages-for-one-update)              |
| Character still references facts after `Reset()`                       | Initial context or system prompt is not cleared by `Reset()` | See [Reset Did Not Clear Everything](troubleshooting-and-diagnostics.md#reset-did-not-clear-everything)                   |
| Character references initial scenario facts only in the first response | `InitialDynamicInfoKeepInContext` is `false` (the default)   | Enable **Initial Dynamic Info Keep In Context** on `ConvaiCharacter`                                                      |
| Cannot add a second Command component to the same GameObject           | `[DisallowMultipleComponent]` restriction                    | Place additional commands on child GameObjects                                                                            |
| `SetStates` list produces a validation warning                         | Duplicate state names or empty entries in list               | Remove duplicates; ensure every entry has a non-empty name                                                                |

***

## Character Does Not Reference Context Updates

When the character appears completely unaware of a state or event you sent, work through the following in order.

**Verify the method used.** `Apply()` is discarded if the character is not in an active conversation. A warning is emitted through the Convai logger (visible in the Console when debug logging is enabled), but no queue is built. Substitute `SetState` or `AddEvent` instead — these queue automatically and flush when the session opens.

**Verify `Execute()` was not skipped.** Wire the `ConvaiDynamicContextCommand` **On Execution Skipped** event to a temporary `Debug.Log` call during development. If it fires, the Console shows the exact validation message that caused the skip.

**Verify the reaction mode.** If reaction mode is `SyncOnly`, the character received the update but will not generate an immediate response — it references the new state in its next natural turn. Switch to `Auto` or `ReactImmediately` if immediate acknowledgement is required.

***

## `Apply()` Has No Effect

`Apply()` has two behaviors that differ from every other `IConvaiDynamicContext` method:

* **No pre-conversation queue.** If the character is not in an active conversation when `Apply()` is called, the update is discarded immediately. A warning is emitted through the Convai logger — enable Convai debug logging to see it in the Unity Console. No queue is built. Use `SetState`, `AddEvent`, or another tracked method if the call may happen before the session starts.
* **No tracker update.** `Apply()` sends directly to transport without touching the local state tracker. A subsequent call to `TryGetStateValue` for a key sent via `Apply()` returns `false`. If the value needs to be readable via `TryGetStateValue`, use `SetState` instead.

{% hint style="warning" %}
`Apply()` is an advanced escape hatch for external systems that construct their own context text. For all standard context management, prefer the tracked methods — `SetState`, `SetStates`, `AddEvent`, `RemoveState`, and `Reset` — which queue automatically and keep the local tracker consistent.
{% endhint %}

***

## Reset Did Not Clear Everything

`Reset()` operates on the **runtime Dynamic Context layer only**. Three sources of character knowledge are outside its scope:

**Initial Dynamic Info Text.** The content of **Initial Dynamic Info Text** on `ConvaiCharacter` is sent once at connection time as part of the session request. `Reset()` does not re-send it and cannot clear it. Ending and restarting the session is the only way to change what was sent at connection time.

**System prompt.** Facts baked into the character's system prompt on the Convai dashboard are not part of the Dynamic Context layer. No SDK call affects them at runtime.

**In-session LLM memory.** The character's language model retains conversational context across turns within the same session. `Reset()` clears the Dynamic Context tracker and sends a Reset message to Convai, but it does not clear the model's in-session conversational memory.

***

## Two Messages for One Update

When you call `SetState` on a state that already exists with a different value, two `context-update` RTVI messages are sent in sequence:

1. A **Replace** message carrying the full canonical context with the updated value in place.
2. An **Append** message carrying the human-readable delta: `"{name} changed from {oldValue} to {newValue}"`.

This is intentional and non-configurable. The Replace gives the character an authoritative complete picture; the Append gives it a natural way to reference the transition in dialogue. If you are monitoring network traffic during debugging, expect this pattern for every existing-state modification.

See [Sync Behavior and Timing — Scenario 2](/broken/pages/fd07c33dbde4c8f46f1472ab841d25ba0bc5951e) for the full sequence.

***

## Cannot Add Multiple Command Components to the Same GameObject

`ConvaiDynamicContextCommand` is marked `[DisallowMultipleComponent]`. Unity prevents a second instance from being added to the same GameObject.

Place each additional command on a **child GameObject** of the NPC. In the **Target** section of each command, disable **Auto Resolve Character** and assign the NPC's `ConvaiCharacter` explicitly — auto-resolve only searches the same GameObject, not parents or children.

***

## Character Not Responding — Decision Tree

The following decision tree covers the full troubleshooting surface for context updates that appear to have no effect.

```mermaid
flowchart TD
    A[Character not responding to context update] --> B{Which entry point?}
    B -- ConvaiDynamicContextCommand --> C{Did OnExecuted fire?}
    C -- No --> D[Check Console for\nvalidation warning\nSee Console Log Reference]
    C -- Yes --> E{Reaction mode?}
    B -- IConvaiDynamicContext script --> F{Which method?}
    F -- Apply --> G{In active conversation?}
    G -- No --> H[Apply discarded\nUse SetState or AddEvent]
    G -- Yes --> E
    F -- SetState / AddEvent / etc --> E
    E -- SyncOnly --> I[Expected — no immediate response\nSwitch to Auto or ReactImmediately]
    E -- Auto or ReactImmediately --> J{Did update reach backend?}
    J -- Yes --> K[Check character system prompt\nand dashboard configuration]
    J -- Unsure --> L[Use Sample UI prefab\nto verify delivery in isolation]
```

***

## Console Log Reference

The following messages appear in the Unity Console during Dynamic Context operations. All `ConvaiDynamicContextCommand` warnings are prefixed with `[ConvaiDynamicContextCommand]`.

| Message                                                                                      | Source                 | Meaning                                                                                                       | Fix                                                                                                        |
| -------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `No ConvaiCharacter found on this GameObject. Assign one or disable Auto Resolve Character.` | `Execute()` validation | **Auto Resolve** is on but no `ConvaiCharacter` is on the same GameObject.                                    | Move the command to the NPC's GameObject, or disable **Auto Resolve** and assign **Character** explicitly. |
| `Assign a ConvaiCharacter or enable Auto Resolve Character.`                                 | `Execute()` validation | **Auto Resolve** is off and **Character** is not assigned.                                                    | Assign the `ConvaiCharacter` reference, or enable **Auto Resolve**.                                        |
| `Set State requires a non-empty state name.`                                                 | `Execute()` validation | **State Name** field is blank or whitespace.                                                                  | Enter a non-empty state name.                                                                              |
| `Set States requires at least one state entry.`                                              | `Execute()` validation | **State Entries** list is empty.                                                                              | Add at least one Name / Value entry.                                                                       |
| `Each state entry requires a non-empty name.`                                                | `Execute()` validation | One or more **State Entries** have a blank name.                                                              | Fill in all entry names.                                                                                   |
| `State entries contain duplicate name '{name}'.`                                             | `Execute()` validation | Two entries in **State Entries** share the same state name. The actual name replaces `{name}` in the Console. | Remove or rename the duplicate.                                                                            |
| `Add Event requires non-empty event text.`                                                   | `Execute()` validation | **Event Text** field is blank or whitespace.                                                                  | Enter the event text.                                                                                      |
| `Remove State requires a non-empty state name.`                                              | `Execute()` validation | **State Name** field is blank or whitespace.                                                                  | Enter the name of the state to remove.                                                                     |
| `Raw Update requires text unless mode is Reset.`                                             | `Execute()` validation | **Raw Text** is empty and **Raw Mode** is not `Reset`.                                                        | Enter text, or set **Raw Mode** to `Reset`.                                                                |

## Next Steps

For the precise message sequences sent for each operation, see [Sync Behavior and Timing](/broken/pages/fd07c33dbde4c8f46f1472ab841d25ba0bc5951e). For method signatures and parameter types, see [Scripting API Reference](/broken/pages/92e033e69c53e803f7296bede3511ff924549b4d).
