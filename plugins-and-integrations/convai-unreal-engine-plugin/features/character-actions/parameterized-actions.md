---
title: Parameterized actions
description: Declare typed action parameters and read resolved values in Blueprint handlers for text, references, choices, and animations.
last_reviewed: "4.0.0-beta.21"
---

Parameterized actions let Convai fill in typed values when it chooses an action. A `Move To` action needs a destination; a `Print` action can carry dynamic text; a `Dance` action can pick from a fixed list of animation styles. Parameters give Convai structured guidance and give your handler typed values to read.

{% embed url="https://www.youtube.com/watch?v=cOiG863n3lA" %}
Parameterized actions walkthrough
{% endembed %}

The following examples show the most common parameter patterns. The full field reference is at the end of this page.

## Prerequisites

- You completed [Building custom action handlers](building-custom-action-handlers.md) for a no-parameter action.
- The action template is compiled on the character Blueprint before you test in Play mode.

## Choosing a parameter type

Use `String` for free-form text, **Actor Reference** for a registered object or character, `Number` for a numeric value, and `String` with **Choices** when only a few values are valid (for example a fixed list of dance styles). The full type list is in the reference table below.

| Type | Use when |
|---|---|
| `String` | The value is open-ended text. |
| Actor Reference | The value must resolve to a registered object or character in the scene. |
| `Number` | The value is a number (distance, duration, count). |
| `Bool` | The value is a true/false flag. |
| `String` + Choices | The value must be one of a fixed list of options. |
| `Enum` | A `UENUM` already exists in your project and you want Convai to match against its display names. |

## Example: Print with a string parameter

Start from a no-parameter `Print` action and add one typed input so Convai can supply the message.

### Declare the parameter

On the `Print` action entry, expand **Parameters** and click **+**:

| Field | Value |
|---|---|
| `Name` | `text` |
| `Type` | `String` |
| `Description` | Leave empty or use a short hint such as `"Text to print"`. |

Compile the Blueprint.

### Read the value in the handler

```text
// Blueprint pseudocode
Event Print(ActionData: FConvaiResultAction)
    Message = GetParamAsString(ActionData, "text")
    Print String(Message)
    HandleActionCompletion(IsSuccessful = true, ShouldRespond = Never)
```

Test in Play mode: `"Print your name on the screen"` or `"Print breathe"`. Convai fills the `text` parameter and the handler prints the resolved string.

## Example: Dance with animation montages

For actions that play skeletal animations, use an `Anim Montage` and call `Handle Action Completion` on both **On Completed** and **On Interrupted** montage pins.

### Prepare montages

1. Import or locate animation sequences in the **Content Browser**.
2. Right-click an animation, select **Create > Create Anim Montage**.
3. Open the montage and tune **Blend In** and **Blend Out** times (for example `1.0` seconds) so transitions look smooth.
4. Repeat for each dance style you want to support.

### Declare the action

Add an action named `Dance` with no parameters for a single-style dance, or add a `type` parameter with **Choices** when multiple styles share one action (see the next section).

### Handler with Play Montage

```text
// Blueprint pseudocode — single montage
Event Dance(ActionData: FConvaiResultAction)
    Play Montage(
        Mesh = BodySkeletalMesh,
        Montage = GrooveDanceMontage,
        OnCompleted → HandleActionCompletion(IsSuccessful = true),
        OnInterrupted → HandleActionCompletion(IsSuccessful = true)
    )
```

{% hint style="warning" %}
If `Handle Action Completion` is missing on the **On Interrupted** pin, a new montage or movement action can leave the queue stalled because the plugin still considers the dance action in progress.
{% endhint %}

## Example: Dance with Choices and a fallback

When one action covers multiple animation variants, add a `String` parameter with a **Choices** array instead of duplicating the action template.

### Declare

Action `Dance`, one parameter:

| Field | Value |
|---|---|
| `Name` | `type` |
| `Type` | `String` |
| `Choices` | `groove`, `disco`, `g-style` (one entry per supported montage) |

The wire format includes `[groove|disco|g-style]` so Convai picks from the list.

### Handler with Switch on String

```text
// Blueprint pseudocode
Event Dance(ActionData: FConvaiResultAction)
    DanceType = GetParamAsString(ActionData, "type")

    Switch on String(DanceType):
        case "groove":  PlayMontage(GrooveMontage, onComplete, onInterrupted)
        case "disco":   PlayMontage(DiscoMontage, onComplete, onInterrupted)
        case "g-style": PlayMontage(GStyleMontage, onComplete, onInterrupted)
        default:
            HandleActionCompletion(
                IsSuccessful = false,
                bAutoReport = true,
                ShouldRespond = Always,
                AdditionalNote = "That dance style is not available",
                Delay = 1.5
            )
            return

    // onComplete and onInterrupted both call:
    HandleActionCompletion(IsSuccessful = true, ShouldRespond = Never)
```

When the player asks for a style outside **Choices** (for example `"ballet"`), the **default** branch reports failure. Convai can respond using the `AdditionalNote` context instead of playing an unsupported montage.

## Connectors

Use **Connector** to link a parameter to preceding text. For `"Put <object> on <surface>"`:

- Parameter 1: `Name = "object"`, no connector.
- Parameter 2: `Name = "surface"`, `Connector = "on"`.

## Enum parameters

When a `UENUM` already exists in your project:

1. Set `Type` to `Enum`.
2. Set `EnumType` to the enum asset.
3. Leave `Choices` empty — display names come from the enum.

Read the matched value with `Get Param As Byte`, then convert with **Byte to Enum**.

## Reading parameters in Blueprint

Use the `UConvaiActions` function library (**Convai | Action API**):

| Node | Returns | Use when |
|---|---|---|
| **Get First Param** | `FConvaiResultParam` | Exactly one parameter. |
| **Get Param** | `FConvaiResultParam` | Full struct for a named parameter. |
| **Get Param As String** | `FString` | `String` or `Auto`. |
| **Get Param As Number** | `float` | `Number`. |
| **Get Param As Bool** | `bool` | `Bool`. |
| **Get Param As Ref** | `FConvaiObjectEntry` | `Reference` or `Auto`. |
| **Get Param As Byte** | `uint8` | `Enum`. |
| **Has Param** | `bool` | Guard before reading. |

## Abort when a required parameter is empty

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

## FConvaiActionParam fields reference

Each parameter on an `FConvaiAction` template is an `FConvaiActionParam` struct:

| Field | Type | Purpose |
|---|---|---|
| `Name` | `FString` | Placeholder name, for example `"destination"` or `"text"`. |
| `Description` | `FString` | Optional hint for Convai. Keep short or leave empty to reduce context size. |
| `Type` | `EConvaiActionParamType` | Declared type. Controls the wire-format hint and parser behavior. |
| `Connector` | `FString` | Joining text before this parameter, for example `"on"` in `"Put ball on table"`. |
| `Choices` | `TArray<FString>` | Fixed-choice list rendered as `[choice1\|choice2\|...]` in the wire format. |
| `EnumType` | `UEnum*` | Required when `Type == Enum`. |

Full type behavior:

| Enum value | Display name | How the value is parsed |
|---|---|---|
| `Auto` | Auto | Infer: Reference, then Number, then Bool; fall back to String. |
| `Reference` | Actor Reference | Resolve against registered `Objects` and `Characters` by exact name. |
| `String` | String | Raw string. |
| `Number` | Number | Parse as `float`. |
| `Bool` | Bool | `"true"`, `"yes"`, or `"1"` → `true`; otherwise `false`. |
| `Enum` | Enum | Match display names of `EnumType`; value stored in `ByteValue`. |

Regardless of declared type, all value fields on `FConvaiResultParam` are populated on a best-effort basis.

## Next steps

{% content-ref url="actions-blueprint-reference.md" %}
[Actions Blueprint reference](actions-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="attention-and-reference-grounding.md" %}
[Attention and reference grounding](attention-and-reference-grounding.md)
{% endcontent-ref %}

{% content-ref url="usage-examples.md" %}
[Character actions examples](usage-examples.md)
{% endcontent-ref %}
