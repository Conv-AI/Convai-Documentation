---
title: Static context at connection time
description: >-
  Configure fixed scenario facts a character receives once at the start of a
  conversation, separate from updates sent while the conversation is running.
last_reviewed: "5.0.0-preview"
---

Initial Dynamic Info supplies fixed scenario facts when a character connects. Enable it on the character to include its text in the connection flow; runtime Dynamic Context handles facts that change afterward.

Use this mechanism for facts that are true before the conversation begins and will not change during the session: the facility name, the character's role, the training scenario type, or the starting conditions of a drill. Use runtime Dynamic Context (`ConvaiDynamicContextRelay` or `IConvaiDynamicContext`) for everything that evolves as the session progresses.

## Inspector configuration

Select `ConvaiCharacter`, open **Session → Opening Context**, and enable **Initial Dynamic Info**. The **Text** field appears only while the toggle is enabled.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the 5.0 `ConvaiCharacter` Inspector with **Session → Opening Context** expanded, **Initial Dynamic Info** enabled, and **Text** showing the scenario example below.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-initial-dynamic-info-5.png" alt="ConvaiCharacter Session section with Initial Dynamic Info enabled and its Text field visible"><figcaption><p>TODO: Replace with the 5.0 Opening Context controls and example scenario text.</p></figcaption></figure>

| Field | Type | Default | Description |
|---|---|---|---|
| **Initial Dynamic Info** | `bool` | `false` | Enables sending the configured text and sets the request's keep-in-context flag. |
| **Text** | `string` | _(empty)_ | Scenario text included when the toggle is enabled. Write plain sentences or key-value lines. |

With **Initial Dynamic Info** disabled, the SDK sends an empty text value. Disabling it does not send the saved text for the first response only. The keep-in-context flag requests retention by Convai; it is not proof that every later response will mention these facts.

### Example configuration

For a fire suppression certification drill, enable **Initial Dynamic Info** and set **Text** to:

```text
Facility: Offshore Platform Alpha
Scenario: Fire Suppression Certification Drill
Trainee role: Operator under assessment
```

Connect and ask the character about the facility and scenario. Check that the opening facts are available before adding runtime updates.

## Relationship to runtime Dynamic Context

Initial context and runtime Dynamic Context are complementary — not alternatives.

| | Initial Dynamic Info | Runtime Dynamic Context |
|---|---|---|
| **When sent** | During connection or group member initialization | During the session, on demand |
| **Content** | Fixed facts set at design time | Live state and events set at runtime |
| **Suitable for** | Facility name, scenario type, character role | Trainee location, equipment state, hazard level |
| **Modifiable at runtime** | No — sent once per connection | Yes — via `SetState`, `AddEvent`, `Reset` |

In an ordinary multi-character room, the connection request includes the active character's initial text. Group conversations use an empty shared initial text and seed each member separately. Do not assume one shared connection request sends every character's private opening text. See [Context in multi-character and group rooms](multi-character-and-group-rooms.md).

```csharp
// These complement the initial context — not replace it
_character.DynamicContext.SetState("Station", "Chemical Storage Bay");
_character.DynamicContext.SetState("HazardLevel", "Extreme");
_character.DynamicContext.AddEvent("Trainee bypassed manual lockout procedure");
```

## What `Reset()` does and does not clear

Calling `Reset()` on the runtime Dynamic Context layer clears all tracked states and events. By default it leaves initial dynamic info in place:

* **Initial Dynamic Info** is excluded from the default reset request. `Reset(removeStatic: true)` also requests removal of static dynamic context for the session.
* **Dashboard configuration and conversation history** are separate from the local tracker. A reset request is not an erasure guarantee for facts present in those sources.

{% hint style="info" %}
To change the initial context for a new session, end the current conversation, update the **Text** field, and reconnect. The next connection uses the updated configuration.
{% endhint %}

## Scripting access

Both fields are readable via C# properties on `ConvaiCharacter`:

```csharp
string initialText = _character.InitialDynamicInfoText;
bool keepInContext = _character.InitialDynamicInfoKeepInContext;
```

These properties are read-only at runtime. Set the values in the Inspector before the scene is played, or via `SerializedObject` in a custom Editor tool.

## Next steps

{% content-ref url="relay-component-reference.md" %}
[Relay component reference](relay-component-reference.md)
{% endcontent-ref %}

{% content-ref url="dynamic-context-scripting-api.md" %}
[Dynamic context scripting API](dynamic-context-scripting-api.md)
{% endcontent-ref %}

{% content-ref url="sync-behavior-and-timing.md" %}
[Sync behavior and timing](sync-behavior-and-timing.md)
{% endcontent-ref %}
