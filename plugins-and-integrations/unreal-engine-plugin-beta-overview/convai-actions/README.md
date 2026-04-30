# Convai Actions

Convai characters can do more than talk: they can **perform physical actions** in your scene. The action system lets the LLM that drives a Convai character emit structured commands (move to a target, pick up an object, wait, run a custom animation, etc.) which your gameplay code then executes.

This guide is split into **three phases**, each one introducing the next layer of capability:

| Phase                               | Goal                                                                        | What you'll learn                                                                                                                                              |
| ----------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phase 1 — Default Actions**       | Get the bot moving in the level with zero scripting.                        | Enable actions on the chatbot, register objects, set up locomotion, run on a NavMesh.                                                                          |
| **Phase 2 — Custom Actions**        | Add a new action with no parameters and wire it to a Blueprint event.       | The `FConvaiAction` template, `OnActionReceived` event, `HandleActionCompletion`.                                                                              |
| **Phase 3 — Parameterized Actions** | Add typed parameters, connectors, choices, and use the live editor preview. | Parameter types (`Auto` / `Reference` / `String` / `Number` / `Bool` / `Enum`), `Get Param As X` accessors, the rendered-string preview, abort vs. completion. |

### Mental model

The action system has three moving parts you'll see throughout the guide:

1. **The chatbot's `Environment`** — a struct on the chatbot component that declares the world the bot can act on:
   * `Actions` — the list of `FConvaiAction` templates the bot is allowed to use.
   * `Objects` — props in the scene the bot can target (cube, lever, door, …).
   * `Characters` — NPCs / the player. These are sent to the server at `/connect` time as the bot's "action contract".
2. **`bEnableActions`** — a per-chatbot toggle that decides whether the `Environment` is sent at all. Off = conversational-only. On = the bot can emit action sequences.
3. **The action-response pipeline** — when the bot decides to act, the server sends back a list of `FConvaiResultAction`s. The plugin matches each one against your declared templates, parses out parameter values, resolves any actor references against `Environment.Objects` / `.Characters`, and fires `OnActionReceivedEvent_V2` with the parsed sequence. Your handler runs the action and calls back into `HandleActionCompletion` or `AbortActionSequence` to advance / retry / abort.

### What's new in V2

If you've used Convai actions before this overhaul, here's what changed at a glance:

* Action templates moved from raw `FString` (`"Wait For <time in seconds>"`) to a structured `FConvaiAction` with typed `Parameters`, optional `Connector`, optional `Choices` / `EnumType`.
* A live, two-way **rendered preview** in the Details panel shows exactly what the LLM will receive — and you can edit either side.
* Action results unify everything into `Parameters: TMap<Name, FConvaiResultParam>` with always-best-effort string / number / bool / actor-ref coercion. Legacy `RelatedObjectOrCharacter` and `ConvaiExtraParams` are still populated as deprecated mirrors so existing handlers keep working.

If you have legacy graphs, follow the migration notes in Phase 3.
