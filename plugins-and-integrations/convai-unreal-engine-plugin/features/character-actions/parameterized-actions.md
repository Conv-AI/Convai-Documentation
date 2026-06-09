---
title: Parameterized actions
description: Declare typed inputs for character actions and read resolved values in Blueprint handlers for movement, timing, choices, and custom behavior.
last_reviewed: "4.0.0-beta.21"
---

Parameterized actions let Convai fill in typed values when it chooses an action. A `Move To` action needs a destination; a `Wait For` action needs a duration; a `Set Emotion` action needs an emotion name. Parameters give Convai structured guidance on what to supply and how to interpret the response.

## FConvaiActionParam

Each parameter on an `FConvaiAction` template is an `FConvaiActionParam` struct with the following fields:

| Field | Type | Purpose |
|---|---|---|
| `Name` | `FString` | Placeholder name rendered in the wire format, for example `"destination"` or `"time in seconds"`. |
| `Description` | `FString` | Optional plain-language hint for Convai, for example `"The number of seconds to wait"`. |
| `Type` | `EConvaiActionParamType` | The declared type. Controls both the prompt hint and how the parser interprets the response. |
| `Connector` | `FString` | Optional joining text rendered before this parameter in the wire format, for example `"on"` for a `"Put ball on table"` action. |
| `Choices` | `TArray<FString>` | Optional fixed-choice list. Rendered as `[choice1\|choice2\|...]` in the wire format. |
| `EnumType` | `UEnum*` | Required when `Type == Enum`. The engine enum whose display names serve as the choice list. |

## Parameter types

`EConvaiActionParamType` controls how the plugin interprets the LLM's filled-in response:

| Enum value | Display name | How the value is parsed |
|---|---|---|
| `Auto` | Auto | Infer type at parse time: try exact Reference, then Number, then Bool; fall back to String. |
| `Reference` | Actor Reference | Resolve the value against `Environment.Objects` and `Environment.Characters` by exact registered name. |
| `String` | String | Treat the value as a raw string. |
| `Number` | Number | Parse the value as a float. |
| `Bool` | Bool | `"true"`, `"yes"`, or `"1"` → `true`; anything else → `false`. |
| `Enum` | Enum | Match the value against the display names of `EnumType`. The matched enum value is stored in `ByteValue`. |

Regardless of the declared type, the plugin populates all value fields (`StringValue`, `NumberValue`, `BoolValue`, `RefValue`) on a best-effort basis. The declared type signals which field is the intended slot.

## Connectors

The `Connector` field adds a preposition or conjunction that links a parameter to the preceding content. For example, to model the action `"Put <object> on <surface>"`:

- Parameter 1: `Name = "object"`, no connector.
- Parameter 2: `Name = "surface"`, `Connector = "on"`.

The wire format rendered to Convai becomes `Put {object} on {surface}`, and the response `"Put ball on table"` maps `ball` → `object` and `table` → `surface`.

## Choices and enums

### String choices

Set `Choices` to constrain the LLM to a fixed set of values:

```text
// Details panel values
Name = "emotion"
Type = String
Choices = ["Happy", "Sad", "Angry", "Calm"]
```

The wire format includes `[Happy|Sad|Angry|Calm]` as a hint. Values not in the list still flow through with a warning logged.

### Enum choices

When you have an existing Unreal `UENUM` you want to mirror:

1. Set `Type` to `Enum`.
2. Set `EnumType` to your `UEnum` asset (use the picker in the Details panel).
3. Leave `Choices` empty. When parsing an enum parameter, the plugin uses the selected enum's display names instead of the `Choices` array.

In your handler, read the matched enum value from `ByteValue` using **Byte to Enum** in Blueprint:

```text
// Blueprint pseudocode
// In the action handler
ParamByte = GetParamAsByte(ActionData, "emotion")
Emotion = ByteToEnum<EMyEmotionEnum>(ParamByte)
```

## Reading parameters in Blueprint

Use the `UConvaiActions` function library (Blueprint category **Convai | Action API**) to read parameters from `FConvaiResultAction`:

| Node | Returns | Use when |
|---|---|---|
| **Get First Param** | `FConvaiResultParam` | You have exactly one parameter and want the full result struct. |
| **Get Param** | `FConvaiResultParam` | You need the full result struct for a named parameter. |
| **Get Param As String** | `FString` | The parameter type is `String` or `Auto`. |
| **Get Param As Number** | `float` | The parameter type is `Number`. |
| **Get Param As Bool** | `bool` | The parameter type is `Bool`. |
| **Get Param As Ref** | `FConvaiObjectEntry` | The parameter type is `Reference` or `Auto`. |
| **Get Param As Byte** | `uint8` | The parameter type is `Enum`. Convert with Byte to Enum after reading. |
| **Has Param** | `bool` | Check whether a named parameter was filled in before reading it. |
| **Get Param Type** | `EConvaiActionParamType` | Inspect the resolved type when using `Auto`. |

All named accessor nodes take the `FConvaiResultAction` struct and a `Name` string matching the parameter's `Name` field. `Get First Param` only takes the `FConvaiResultAction` struct.

## FConvaiResultParam fields

`FConvaiResultParam` has the following Blueprint-readable fields:

| Field | Type | Description |
|---|---|---|
| `Type` | `EConvaiActionParamType` | The declared or inferred type. |
| `StringValue` | `FString` | Raw value as a string. Always populated. |
| `NumberValue` | `float` | `Atof(StringValue)`. `0` if not numeric. |
| `BoolValue` | `bool` | `true` if `StringValue` is `"true"`, `"yes"`, or `"1"`. |
| `RefValue` | `FConvaiObjectEntry` | Resolved from `Environment.Objects` / `Environment.Characters` by exact registered name. Empty when no match. |
| `ByteValue` | `uint8` | Matched enum value when `Type == Enum` and `EnumType` was set; `0` otherwise. |

## AbortActionSequence from a handler

If a required parameter resolves to an empty value (for example a Reference that could not be matched), call `AbortActionSequence` with a descriptive message so Convai can try again:

```text
// Blueprint pseudocode
RefEntry = GetParamAsRef(ActionData, "destination")
if RefEntry.Ref is None:
    AbortActionSequence(
        EventText = "Destination not found in scene",
        ShouldRespond = Always
    )
    return
```

## Next steps

{% content-ref url="actions-blueprint-reference.md" %}
[Actions Blueprint reference](actions-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="attention-and-reference-grounding.md" %}
[Attention and reference grounding](attention-and-reference-grounding.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Usage examples](usage-examples.md)
{% endcontent-ref %}
