---
title: Usage examples
description: End-to-end action recipes for navigating to a registered object, following a character, and using parameterized actions in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

These examples show complete action handler setups for the most common scenarios. Each example lists the configuration required in the Details panel and the Blueprint logic needed in the NPC Actor.

## Example 1: Navigate to a registered object

**Scenario:** A training-simulation instructor NPC navigates to a piece of equipment when the trainee asks it to go there.

### Configuration

In the NPC Actor's **Details** panel, under **Convai Chatbot > Environment**:

1. **Enable Actions** is ticked.
2. `Actions` array contains a `Move To` entry with a `destination` parameter of type `Reference` (this is the default).
3. `Objects` array contains an entry:
   - `Name`: `"SafetyValve"`
   - `Ref`: the valve Actor in the level
   - `MoveTargetMode`: `Actor as goal`
   - `AcceptanceRadius`: `100.0`

### Blueprint handler — Move To

Add a **Custom Event** named `Move To` to the NPC Actor Blueprint with one `FConvaiResultAction` input:

```text
Event MoveTo(ActionData: FConvaiResultAction)
    // Read the destination object reference
    DestEntry = GetParamAsRef(ActionData, "destination")

    // Guard: reference must have a live Actor
    ResolveGoalLocation(
        Entry = DestEntry,
        SourceActor = Self,
        // outputs:
        OutGoalActor, OutGoalComponent, OutGoalLocation,
        OutAcceptanceRadius, OutMode,
        bSuccess, bAlreadyThere, bReachable, PathEnd, PathPoints
    )

    if not bSuccess:
        AbortActionSequence(
            EventText = "Destination actor no longer exists",
            ShouldRespond = Always
        )
        return

    if bAlreadyThere:
        HandleActionCompletion(IsSuccessful = true)
        return

    // Branch on Out Mode
    if OutMode == Actor:
        AIMoveTo(Target = OutGoalActor, AcceptanceRadius = OutAcceptanceRadius)
    else:
        AIMoveTo(Destination = OutGoalLocation, AcceptanceRadius = OutAcceptanceRadius)

    // Wait for AIMoveTo to complete via OnMoveCompleted or similar
    // Then call:
    HandleActionCompletion(IsSuccessful = true)
```

{% hint style="info" %}
Always branch on the `bOut Success` and `bOut Already There` outputs from **Resolve Goal Location** before issuing `AI Move To`. Passing a destroyed Actor to `AI Move To` silently no-ops in Actor mode, or sends the pawn to a stale location in Vector mode.
{% endhint %}

---

## Example 2: Follow a character

**Scenario:** A security-training NPC follows the player on a patrol route until told to stop.

### Configuration

1. `Actions` array contains `Follow` (name: `"Follow"`, parameter: `character`, type `Reference`) and `Stop Moving` (name: `"Stop Moving"`, no parameters) — both are defaults.
2. `Characters` array contains:
   - `Name`: `"Player"` or matches the player's `PlayerName` field on the `Convai Player` component.
   - `Ref`: the player pawn Actor.

### Blueprint handler — Follow

```text
Event Follow(ActionData: FConvaiResultAction)
    TargetEntry = GetParamAsRef(ActionData, "character")

    if TargetEntry.Ref is None:
        AbortActionSequence(
            EventText = "Cannot find the character to follow",
            ShouldRespond = Always
        )
        return

    // Start a repeating timer or use a tracking task
    // that keeps issuing AIMoveTo toward TargetEntry.Ref each tick

    // HandleActionCompletion is called later when "Stop Moving" arrives
    // and the follow task is cancelled.
    // Do NOT call HandleActionCompletion here — the action is ongoing.
```

### Blueprint handler — Stop Moving

The event name must match the registered action name exactly (case-sensitive). Because the default action is registered as `"Stop Moving"` (with a space), the Blueprint Custom Event must also be named `Stop Moving`.

```text
Event Stop Moving(ActionData: FConvaiResultAction)
    // Cancel the repeating move timer / task
    StopFollowTask()

    // Stop the pawn movement
    StopMovement on AIController

    HandleActionCompletion(IsSuccessful = true)
```

{% hint style="warning" %}
`Follow` is an ongoing action. Do not call `HandleActionCompletion` inside the Follow handler itself or the queue will immediately advance to the next action. Call it only when the follow behavior ends (user says "Stop" or the sequence is aborted).
{% endhint %}

---

## Example 3: Parameterized action with a string choice

**Scenario:** A medical-simulation NPC administers a treatment chosen from a fixed list when instructed.

### Configuration

Add a custom action to the `Actions` array:

- `Name`: `"Administer Treatment"`
- `Description`: `"Administer a specific treatment to the patient"`
- Parameters:
  - `Name`: `"treatment"`
  - `Type`: `String`
  - `Choices`: `["CPR", "Defibrillation", "IV Fluids", "Oxygen Mask"]`

### Blueprint handler

```text
Event AdministerTreatment(ActionData: FConvaiResultAction)
    TreatmentName = GetParamAsString(ActionData, "treatment")

    // Branch on the treatment type
    switch TreatmentName:
        case "CPR":           PlayCPRAnimation()
        case "Defibrillation": PlayDefibrillationAnimation()
        case "IV Fluids":      PlayIVFluidsAnimation()
        case "Oxygen Mask":    PlayOxygenMaskAnimation()
        default:
            AbortActionSequence(
                EventText = "Unknown treatment: " + TreatmentName,
                ShouldRespond = Always
            )
            return

    // Wait for animation
    Delay 2.0 seconds

    HandleActionCompletion(
        IsSuccessful = true,
        bAutoReport = true,
        AdditionalNote = TreatmentName + " administered"
    )
```

---

## Example 4: Parameterized action with an enum

**Scenario:** A corporate-onboarding NPC changes its posture based on a command.

### Configuration

Assume an existing `UENUM` named `ENPCPosture` with values `Standing`, `Sitting`, `Crouching`.

Add a custom action:

- `Name`: `"Change Posture"`
- Parameters:
  - `Name`: `"posture"`
  - `Type`: `Enum`
  - `EnumType`: `ENPCPosture`

### Blueprint handler

```text
Event ChangePosture(ActionData: FConvaiResultAction)
    PostureByte = GetParamAsByte(ActionData, "posture")
    Posture = ByteToEnum<ENPCPosture>(PostureByte)

    switch Posture:
        case Standing:  SetPostureAnimation(Standing)
        case Sitting:   SetPostureAnimation(Sitting)
        case Crouching: SetPostureAnimation(Crouching)

    HandleActionCompletion(IsSuccessful = true)
```

---

## Example 5: Multi-action sequence with wait-for-speech

**Scenario:** A safety-drill NPC walks to an exit sign and announces it as it arrives.

### Configuration

Two actions in the `Actions` array:

1. `Move To` (default) — `bWaitForBotSpeech = false`.
2. `Announce` — custom action, no parameters, `bWaitForBotSpeech = true`, `DelayAfterBotSpeechSec = 0.5`.

When Convai generates the response `"Move To ExitSign, Announce"`, the plugin:

1. Immediately starts `Move To`.
2. When `Move To` completes and `HandleActionCompletion(true)` is called, the queue advances to `Announce`.
3. Because `Announce` has `bWaitForBotSpeech = true`, the plugin waits until the character's speech for the previous response begins or ends before firing `Announce`.
4. After the speech condition resolves plus `0.5` seconds, the `Announce` handler fires.

### Blueprint handler — Announce

```text
Event Announce(ActionData: FConvaiResultAction)
    // Play the announcement animation / audio cue
    PlayAnnouncementAnim()

    HandleActionCompletion(
        IsSuccessful = true,
        bAutoReport = true,
        ShouldRespond = Never
    )
```

## Next steps

- [Parameterized actions](parameterized-actions.md) — full parameter type reference.
- [Actions Blueprint reference](actions-blueprint-reference.md) — complete struct and function signatures.
- [Troubleshooting and diagnostics](troubleshooting-and-diagnostics.md) — fix common issues with the examples above.
