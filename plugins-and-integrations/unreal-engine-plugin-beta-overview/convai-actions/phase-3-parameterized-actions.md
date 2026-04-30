# Phase 3: Parameterized Actions

Phase 2 added a no-parameter custom action. Most real actions need to carry data — _"wait 5 seconds"_, _"pick up the cube"_, _"put the ball on the table"_. This phase walks through:

1. A simple numeric param (`Wait For` revisited).
2. An actor reference (single param resolves to an `AActor*`).
3. A compound action with two params + a connector word (`Put ... on ...`).
4. Constrained values via `Choices` (manual list) and `Enum` (drawn from a `UENUM`).
5. The live editor preview — both as a debugging aid and as a way to author the template directly.

### The parameter type matrix

Every `FConvaiActionParam` has a **`Type`** that drives both the wire-format hint sent to the LLM and how the parser interprets the response:

| Type          | Wire hint  | Parser                                                                       |
| ------------- | ---------- | ---------------------------------------------------------------------------- |
| **Auto**      | (none)     | Try Reference → Number → Bool → fall back to String. Default for new params. |
| **Reference** | `: ref`    | Look up the value against `Environment.Objects` then `.Characters`.          |
| **String**    | `: string` | Treat as text.                                                               |
| **Number**    | `: number` | `Atof`.                                                                      |
| **Bool**      | `: bool`   | `true` for "true"/"yes"/"1", false otherwise.                                |
| **Enum**      | `: enum`   | Constrain to a `UEnum` you pick (auto-fills `Choices`).                      |

> Whatever the declared type, **all value fields on `FConvaiResultParam` are populated best-effort**. A `String`-typed param whose value happens to be the name of a scene Object will still have `RefValue` set. Read whichever field is convenient — `Type` only signals which slot was the LLM's intended target.

### Example A — A numeric parameter

We'll redo `Wait For` to show the typed-param flow end to end.

#### Declare the template

1. Select the Convai chatbot, open **Environment → Actions**.
2. The shipped **`Wait For`** entry already has one param `time in seconds` typed `Number` with description _"How long to wait, in seconds"_. Use it as-is, or add your own.

The rendered preview (auto-populated below the structured fields) reads:

```
Wait For "<time in seconds: number>" — Wait for a duration. time in seconds: How long to wait, in seconds.
```

The `: number` hint tells the LLM to send back a numeric value. The `"<...>"` quote-wrapping tells it to emit response values in double quotes so the parser can split unambiguously even when values contain spaces.

#### Read the param in BP

In your `OnActionReceivedEvent_V2` handler, in the `Wait For` switch case:

1. Drag a **`Get Param As Number`** node off the chatbot reference.
   * **Action**: the current `FConvaiResultAction` from the loop.
   * **Name**: `time in seconds`.
2. Wire the returned `float` to a **`Delay (Duration)`** node.
3. After the delay, call `Handle Action Completion(true, 0, EventText="Done waiting", ShouldRespond=Auto)`.

The `EventText` parameter lets you tell the bot _"that finished"_ in the same call — handy for keeping its context up to date without a separate `Add Context Event`.

#### Test

Ask: _"Wait for 3 seconds."_ The bot should pause, then say _"Done waiting"_ or similar (depending on `ShouldRespond` and the LLM's mood).

### Example B — An actor reference

`Move To` already does this with the shipped defaults, but here's the recipe for a custom one.

#### Declare

Add an action `Greet` with one param:

* **Name**: `target`
* **Type**: `Reference`
* **Description**: `Who to greet`

The preview becomes:

```
Greet "<target: ref>" — <action description if any>. target: Who to greet.
```

#### Read in BP

1. **`Get Param As Ref`** with `Name = "target"` returns an `FConvaiObjectEntry`. The `Ref` field is the resolved `AActor*` (set automatically because the value matched something in `Environment.Objects` or `.Characters`).
2. Use the actor — face them, play an animation, whatever your `Greet` means.

### Example C — A compound action with a connector

_"Put the ball on the table"_ models cleanly with two `Reference` params and a connector word for the second:

#### Declare

Action `Put`, two params:

| Name    | Type      | Connector             | Description       |
| ------- | --------- | --------------------- | ----------------- |
| `ball`  | Reference | (empty — first param) | What to pick up   |
| `table` | Reference | `on`                  | Where to place it |

The preview:

```
Put "<ball: ref>" on "<table: ref>" — Place one object on another. ball: What to pick up. table: Where to place it.
```

The `Connector` field is **not** limited to prepositions — it's "any text that links the param to what came before." `to`, `with`, `using`, `for`, etc. all work.

#### Read in BP

```
Get Param As Ref(action, "ball")  → FConvaiObjectEntry (the ball)
Get Param As Ref(action, "table") → FConvaiObjectEntry (the table)
```

Both have their `Ref` populated as long as the LLM picked names that match your `Environment.Objects`.

### Example D — Constrained values (Choices)

If you want the LLM to pick from a **fixed list**, populate `Choices`:

#### Declare

Action `Set Mood`, one param:

* **Name**: `mood`
* **Type**: `String`
* **Description**: `How the bot should feel`
* **Choices**: `happy`, `sad`, `angry`

Preview:

```
Set Mood "<mood [happy|sad|angry]: string>" — Set the bot's mood. mood: How the bot should feel.
```

The `[choices]` block in the wire format constrains the LLM. The parser also validates against the list on receipt — values not in the set still flow through to the result, but a warning logs.

### Example E — Enum-typed values

When your Blueprint already has a `UENUM` you want to use, switch the param **Type** to **`Enum`**. The Details panel hides the manual `Choices` field and shows an **`Enum Type`** picker.

#### Declare

```cpp
UENUM(BlueprintType)
enum class EBotMood : uint8 { Happy, Sad, Angry };
```

Action `Set Mood`, one param:

* **Type**: `Enum`
* **Enum Type**: `EBotMood`
* **Name** / **Description**: as before.

Preview:

```
Set Mood "<mood [Happy|Sad|Angry]: enum>" — Set the bot's mood. mood: How the bot should feel.
```

The choice block is auto-derived from the enum's display names. If you forget to set `Enum Type`, the preview embeds `[ERROR: EnumType not set]` inline so the misconfiguration is loud at edit time.

#### Read in BP

`Get Param As String(action, "mood")` returns `"Happy"` / `"Sad"` / `"Angry"`. Convert to the enum value with **`Convert String to Byte`** or the BP node UE generates for `EBotMood`.

### The rendered string — debug + author

The **`Rendered String`** field on each `FConvaiAction` is a multi-line text box that's bidirectional:

* **Read it** to see exactly what gets sent to the LLM. Useful for:
  * Sanity-checking your descriptions before connecting.
  * Pasting into a separate tool to test prompt variations.
  * Comparing two characters' action contracts side-by-side.
* **Write to it** and the structured fields update. The plugin parses the format `Name <connector> "<param: type>"… — Description. param: desc.` back into Name / Description / Parameters. This is handy for:
  * Pasting templates between characters.
  * Quickly editing a long description without scrolling through nested struct fields.

> **If your edit doesn't parse cleanly** (broken brackets, unrecognized type word, etc.), the preview silently reverts to the canonical render of the structured fields on the next refresh. Stick to the format rules and you'll be fine.

The two-way sync is conservative: it only re-parses when the rendered string actually differs from what the structured fields would produce, so incidental commits (focus changes, accidental clicks) don't downgrade types.

### Migrating from the legacy fields

If you have older handler graphs that read `FConvaiResultAction.RelatedObjectOrCharacter` or `.ConvaiExtraParams.Number/Text`, they still compile — those fields are populated as deprecated mirrors of the new `Parameters` map. BP node tooltips show the deprecation message pointing at the replacement:

| Legacy                                | New                                                              |
| ------------------------------------- | ---------------------------------------------------------------- |
| `Result.RelatedObjectOrCharacter.Ref` | `Get Param As Ref(action, "<name>").Ref` (or `Get First Param`). |
| `Result.ConvaiExtraParams.Number`     | `Get Param As Number(action, "<name>")`.                         |
| `Result.ConvaiExtraParams.Text`       | `Get Param As String(action, "<name>")`.                         |
| `Get Action Param(extraParams, name)` | `Get Param As String(action, name)`.                             |

You can migrate handler-by-handler at your own pace; nothing forces an immediate rewrite.

### Where to go next

You now know:

* The parameter type matrix and the wire format it produces.
* How to use connectors for compound actions.
* How to constrain values with `Choices` or `Enum`.
* How to read parameters in Blueprint via the typed accessors.
* How to use the rendered preview for debugging or direct authoring.

That's the whole action authoring surface. For the runtime contract that drives everything (the four server prompt lanes, the dynamic-context pipeline, scene-metadata updates, conversation partner, look-at target), see the in-plugin reference at **`Convai/Docs/ActionsAndEnvironment.md`** and the deeper V2 reference at **`Convai/Docs/ActionsV2.md`**.
