---
title: Convai Toolset reference
description: Reference for the seven editor actions a connected coding agent can call to set up Convai characters, players, and actions.
last_reviewed: "4.0.0-beta.27"
---

The Convai Toolset registers seven `AICallable` editor actions with the engine's `ToolsetRegistry` plugin, split across `UConvaiSetupToolset` and `UConvaiActionToolset` in `Source/ConvaiToolsetGated/Private/ConvaiToolset.h`. Requires **Unreal Engine 5.8 or later** and an **Editor** build — the `ConvaiToolset` module throws a build error on any non-Editor target, and its gated half compiles out entirely below UE 5.8.

{% hint style="warning" %}
These seven actions are `AICallable`, not `BlueprintCallable`. A connected coding agent invokes them through the engine's MCP server — they do not appear in the Blueprint node palette, and no Blueprint graph can call them.
{% endhint %}

## All seven actions

| Action | Toolset class | What it does |
|---|---|---|
| `SetupConvaiCharacter` | `UConvaiSetupToolset` | Turns a character Blueprint into a talking Convai character |
| `SetupConvaiPlayer` | `UConvaiSetupToolset` | Adds the Convai player component to a player Pawn Blueprint |
| `SetupConvaiPawnMovement` | `UConvaiSetupToolset` | Sets up Convai-tuned movement on a character/pawn Blueprint |
| `AddNavMeshVolumeForCurrentLevel` | `UConvaiSetupToolset` | Spawns a nav mesh bounds volume sized to the current level |
| `SetBlueprintPropertyAndPropagate` | `UConvaiSetupToolset` | Sets one Blueprint property and propagates it to already-placed level instances |
| `AddConvaiAction` | `UConvaiActionToolset` | Appends a parameterized action to a chatbot's action list |
| `CreateConvaiActionHandler` | `UConvaiActionToolset` | Synthesizes a Blueprint event handler for a named action |

Every action returns a human-readable status string describing what it changed, and is idempotent — calling it again with the same inputs re-uses existing components or values instead of duplicating them.

## `SetupConvaiCharacter`

Turns a character Blueprint into a talking Convai character. Adds `BP_ConvaiChatbotComponent` and a native `ConvaiFaceSyncComponent` if either is missing, sets the chatbot's Character ID, enables `bAutoFillConversationPartnerFromPlayer`, sets the face-sync lip sync mode to the MetaHuman blendshape mode (`BS_MHA`) with interpolation enabled, and assigns the Convai MetaHuman face and body animation Blueprints to the skeletal mesh components named `Face` and `Body`. Compiles and saves the Blueprint.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `CharacterBlueprintPath` | `FString` | — (required) | Object path of the MetaHuman/character Blueprint, for example `/Game/NPCs/BP_Guard` |
| `CharacterId` | `FString` | — (required) | The Convai backend Character ID to assign to the chatbot component |

Returns a human-readable status string describing what was changed.

## `SetupConvaiPlayer`

Adds the Convai player component to the player's Pawn Blueprint — the controllable character the player possesses — so the player can speak to Convai characters. Adds `BP_ConvaiPlayerComponent` if missing, then compiles and saves the Blueprint.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `PlayerBlueprintPath` | `FString` | — (required) | Object path of the player Pawn Blueprint (the possessed/controllable character that owns the camera and input), for example `/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter` |

Returns a human-readable status string describing what was changed.

## `SetupConvaiPawnMovement`

Sets up Convai-tuned movement on a character/pawn Blueprint so it can navigate. If the Blueprint's parent is a plain `AActor`, it is reparented to `APawn`. A `UFloatingPawnMovement` component is added if one is not already present or inherited, and Convai movement defaults are applied (`MaxSpeed=375`, `Acceleration=200`, `Deceleration=250`, `TurningBoost=3`, plus nav-path-following defaults). For Character-based Blueprints, the inherited `CharacterMovementComponent` is tuned with the equivalent walk-speed and nav-agent defaults instead. Compiles the Blueprint when safe and saves it.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `CharacterBlueprintPath` | `FString` | — (required) | Object path of the character/pawn Blueprint, for example `/Game/NPCs/BP_Guard` |

Returns a human-readable status string describing what was changed.

## `AddNavMeshVolumeForCurrentLevel`

Spawns a `NavMeshBoundsVolume` into the current editor level so Convai characters can path-find. By default the volume is centered and sized to cover the combined bounds of the level's actors. Navigation is rebuilt after the volume is spawned.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `Location` | `TOptional<FVector>` | unset | Optional world-space center for the volume. If unset, the level bounds center is used |
| `Extent` | `TOptional<FVector>` | unset | Optional half-extent (cm) of the volume box. If unset, derived from the level bounds with a margin |

Returns a human-readable status string including the final volume location and extent.

## `SetBlueprintPropertyAndPropagate`

Sets one property on a Blueprint and propagates the new value to every already-placed level instance that still holds the old value, preserving per-instance overrides. Handles both a component-template property (pass the component's variable name in `ComponentName`) and an actor/Blueprint-level property (leave `ComponentName` empty). Use this instead of a raw property set and compile when the change must also reach characters already placed in the level — neither the engine's own property-set tool nor a plain Blueprint compile propagates template or class-default-object edits to already-placed instances. The value is parsed through the property's own text importer, so any type works: `300.0` (float), `true` (bool), `Hello` (string/name), `(X=0,Y=0,Z=300)` (vector/struct), `/Game/P.A` (object). Compiles and saves the Blueprint.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `BlueprintPath` | `FString` | — (required) | Object path of the Blueprint, for example `/Game/NPCs/BP_Guard` |
| `ComponentName` | `FString` | — (required, may be empty) | The component's Blueprint variable name, for example `ProximitySphere`. Leave empty for an actor/Blueprint-level property |
| `PropertyName` | `FString` | — (required) | The property name, for example `SphereRadius` (component) or `MyVar` (actor-level) |
| `ValueAsString` | `FString` | — (required) | The new value in Unreal text form, parsed by the property importer |

Returns a human-readable status string including how many placed instances were updated.

{% hint style="info" %}
Edit a property through `SetBlueprintPropertyAndPropagate` from the start. A value already desynced by a prior raw property set looks like a per-instance override to the propagation logic and will not be updated.
{% endhint %}

## `AddConvaiAction`

Appends a parameterized action to a chatbot's Environment action list. Locates `BP_ConvaiChatbotComponent` (or any `UConvaiChatbotComponent`) on the given Blueprint, enables `EnvironmentData.bEnableActions`, and adds an `FConvaiAction` with the given name, description, and parameters, preserving any existing actions. An action with the same name is replaced in place. Compiles and saves the Blueprint. These actions take effect at the chatbot's next connect — they prepare the next session, not a live one.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `CharacterBlueprintPath` | `FString` | — (required) | Object path of the Blueprint that owns the chatbot component |
| `ActionName` | `FString` | — (required) | Canonical action name, for example `Wave`, `Pick Up`, `Say`. Should match the handler event name |
| `Description` | `FString` | — | Human-language description of what the action does |
| `Parameters` | `TArray<FConvaiToolsetActionParam>` | — | Ordered list of declared parameters (name, description, type, and choices) the agent should fill in at call time |

`FConvaiToolsetActionParam` mirrors the agent-facing subset of `FConvaiActionParam`:

| Field | Type | Description |
|---|---|---|
| `Name` | `FString` | Placeholder name as the agent sees it, for example `text`, `destination`, `time in seconds` |
| `Description` | `FString` | Optional human-language description of what the parameter means |
| `Type` | `EConvaiActionParamType` | How the value is interpreted: `String`, `Number`, `Reference` (resolves against the chatbot's known Objects/Characters), `Bool`, `Enum`, or `Auto` (default, infers at parse time) |
| `Choices` | `TArray<FString>` | For a fixed choice-set parameter, the allowed values, used with `Type=String`. `AddConvaiAction` cannot supply a `UEnum`, so a `Type=Enum` parameter is coerced to `String` with its options listed in `Choices` |

Returns a human-readable status string describing what was changed.

## `CreateConvaiActionHandler`

Synthesizes a Convai action handler in a Blueprint's event graph. Creates a Custom Event named exactly `ActionName` with a single input pin of type `FConvaiResultAction`, and wires its exec output to a `HandleActionCompletion` call on the Blueprint's chatbot component, auto-wiring the chatbot self pin from the component variable when present. This is the runtime contract that `UConvaiChatbotComponent::TriggerNamedBlueprintAction` expects. Compiles the Blueprint.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `BlueprintPath` | `FString` | — (required) | Object path of the Blueprint to add the handler to |
| `ActionName` | `FString` | — (required) | The exact action name; the created Custom Event is named the same |

Returns the created event name on success, or an error string prefixed with `Error:`.

## Next steps

{% content-ref url="README.md" %}
[AI coding assistant](README.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[AI coding assistant quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="convai-agent-skills.md" %}
[Convai AgentSkills](convai-agent-skills.md)
{% endcontent-ref %}
