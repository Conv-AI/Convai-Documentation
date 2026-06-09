---
title: Static context at connection time
description: Configure fixed scenario facts that are sent with the room connection before runtime updates, events, and attention changes begin.
last_reviewed: "4.2.0"
---

Static connection-time context is for facts that are already known before a character session starts. Use it for the facility name, scenario title, trainee role, or initial drill conditions. Use runtime Dynamic Context for values that change after the session begins.

## Inspector fields

The fields are on `ConvaiCharacter` in the connection section.

| Inspector label | Runtime property | Default | Description |
|---|---|---|---|
| **Keep Initial Dynamic Context** | `InitialDynamicContextKeepInContext` | `false` | Enables initial context text for the connection request. |
| **Initial Dynamic Context Text** | `InitialDynamicContextText` | Empty | Fixed text sent in the room connection request when keep is enabled. |

The text field is shown only when **Keep Initial Dynamic Context** is enabled.

{% hint style="warning" %}
When **Keep Initial Dynamic Context** is disabled, Unity does not send the initial context text. Enable the toggle before entering fixed scenario facts.
{% endhint %}

## Example

For a fire suppression certification drill, enable **Keep Initial Dynamic Context** and set **Initial Dynamic Context Text** to:

```text
Facility: Offshore Platform Alpha
Scenario: Fire Suppression Certification Drill
Trainee role: Operator under assessment
```

The SDK serializes this into the room connection request as `dynamic_info.text` with `dynamic_info.keep_in_context` set to `true`.

## Relationship to runtime Dynamic Context

| Context source | When sent | Best for | Runtime API |
|---|---|---|---|
| Initial dynamic context | During room connection | Fixed scenario facts known before the session starts | Read-only properties on `ConvaiCharacter` |
| Runtime Dynamic Context | During the active session | Live state, events, resets, and attention objects | `ConvaiCharacter.DynamicContext` |

The two sources are complementary. Initial context establishes the starting scenario. Runtime Dynamic Context layers live changes on top.

```csharp
character.DynamicContext.SetState("Station", "Chemical Storage Bay");
character.DynamicContext.SetState("HazardLevel", "Extreme");
character.DynamicContext.AddEvent("Trainee bypassed manual lockout procedure");
```

## Reset scope

`Reset()` clears runtime tracked states and events. It does not edit the serialized initial-context fields or dashboard prompt text.

Use `Reset(removeStatic: true)` when the current session should also clear static connect-time context on Convai.

```csharp
character.DynamicContext.Reset(removeStatic: true);
character.DynamicContext.Flush();
```

This request affects the current session. If you reconnect later and **Keep Initial Dynamic Context** is still enabled, Unity can send the configured initial context again.

## Scripting access

Both values are readable at runtime.

```csharp
string initialText = character.InitialDynamicContextText;
bool keepInContext = character.InitialDynamicContextKeepInContext;
```

Set the values in the Inspector before Play mode, or through editor tooling that edits the serialized fields.

## Next steps

{% content-ref url="dynamic-context-scripting-api.md" %}
[Dynamic context scripting API](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-dynamic-context.md" %}
[Troubleshoot dynamic context](troubleshoot-dynamic-context.md)
{% endcontent-ref %}
