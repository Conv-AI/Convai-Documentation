---
title: Character actions examples
description: End-to-end action recipes for navigating to a registered object, following a character, and using parameterized actions in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

Each example below is self-contained: it lists the Details panel configuration and the Blueprint handler pseudocode needed to implement a working action. Start with Example 1 if you are new to character actions. The examples progress from default navigation to custom actions with typed parameters.

## Example 1: Navigate to a registered object

**Scenario:** A training-simulation instructor NPC navigates to a piece of equipment when the trainee asks it to go there.

### Configuration

In the NPC Actor's **Details** panel, under **Convai Chatbot > Environment**:

1. **Enable Actions** is ticked.
2. `Actions` array contains a `Move To` entry with a `destination` parameter of type **Actor Reference** (this is the default).
3. `Objects` array contains an entry:
   - `Name`: `"SafetyValve"`
   - `Ref`: the valve Actor in the level
   - `MoveTargetMode`: `Actor as goal`
   - `AcceptanceRadius`: `100.0`

### Blueprint handler — Move To

Add a **Custom Event** named `Move To` to the NPC Actor Blueprint with one `FConvaiResultAction` input:

```text
// Blueprint pseudocode
Event Move To(ActionData: FConvaiResultAction)
    // Read the destination object reference
    DestEntry = GetParamAsRef(ActionData, "destination")

    // Resolve the entry to AI Move To inputs
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

    // Branch on Out Mode — wire the correct pin to AI Move To
    if OutMode == Actor:
        AIMoveTo(Target = OutGoalActor, AcceptanceRadius = OutAcceptanceRadius)
    else:
        AIMoveTo(Destination = OutGoalLocation, AcceptanceRadius = OutAcceptanceRadius)

    // Wait for AIMoveTo to complete via OnMoveCompleted
    // Then call:
    HandleActionCompletion(IsSuccessful = true)
```

{% hint style="info" %}
Always branch on `bOut Success` and `bOut Already There` before issuing `AI Move To`. Passing a destroyed Actor to `AI Move To` silently no-ops in Actor mode, or sends the pawn to a stale location in Vector mode.
{% endhint %}

---

## Example 2: Follow a character

**Scenario:** A security-training NPC follows the player on a patrol route until told to stop.

### Configuration

1. `Actions` array contains `Follow` (name: `"Follow"`, parameter: `character`, type **Actor Reference**) and `Stop Moving` (name: `"Stop Moving"`, no parameters) — both are defaults.
2. `Characters` array contains:
   - `Name`: `"Player"` or matches the player's `PlayerName` field on the `Convai Player` component.
   - `Ref`: the player pawn Actor.

### Blueprint handler — Follow

```text
// Blueprint pseudocode
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

    // Complete the Follow action after the loop starts.
    // The timer/task keeps running until Stop Moving fires later.
    HandleActionCompletion(IsSuccessful = true)
```

### Blueprint handler — Stop Moving

The event name must match the registered action name, including spaces. Because the default action is registered as `"Stop Moving"` (with a space), the Blueprint Custom Event must also be named `Stop Moving` — not `StopMoving`.

```text
// Blueprint pseudocode
Event Stop Moving(ActionData: FConvaiResultAction)
    // Cancel the repeating move timer / task
    StopFollowTask()

    // Stop the pawn movement
    StopMovement on AIController

    HandleActionCompletion(IsSuccessful = true)
```

{% hint style="warning" %}
`Follow` starts an ongoing behavior, but the action itself should complete after the follow loop starts. This lets later actions, including `Stop Moving`, dispatch normally.
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
// Blueprint pseudocode
Event Administer Treatment(ActionData: FConvaiResultAction)
    TreatmentName = GetParamAsString(ActionData, "treatment")

    // Branch on the treatment type
    switch TreatmentName:
        case "CPR":            PlayCPRAnimation()
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
// Blueprint pseudocode
Event Change Posture(ActionData: FConvaiResultAction)
    PostureByte = GetParamAsByte(ActionData, "posture")
    Posture = ByteToEnum<ENPCPosture>(PostureByte)

    switch Posture:
        case Standing:  SetPostureAnimation(Standing)
        case Sitting:   SetPostureAnimation(Sitting)
        case Crouching: SetPostureAnimation(Crouching)

    HandleActionCompletion(IsSuccessful = true)
```

---

## Example 5: Print with a dynamic string parameter

**Scenario:** A training NPC prints Convai-supplied text to the screen when asked.

### Configuration

Add a custom action to the `Actions` array:

- `Name`: `"Print"`
- Parameters:
  - `Name`: `"text"`
  - `Type`: `String`
  - `Description`: leave empty or use a short hint

Compile the Blueprint, then scaffold the handler with **Create Convai Action Handler**.

### Blueprint handler

```text
// Blueprint pseudocode
Event Print(ActionData: FConvaiResultAction)
    Message = GetParamAsString(ActionData, "text")
    Print String(Message)
    HandleActionCompletion(IsSuccessful = true, ShouldRespond = Never)
```

**Test prompt:** `"Print your name on the screen."`

---

## Example 6: Dance with Choices and a fallback

**Scenario:** A character plays one of several dance montages from a single action.

### Configuration

1. Create an `Anim Montage` for each dance style. Tune blend in/out on each montage.
2. Add action `Dance` with one parameter:
   - `Name`: `"type"`
   - `Type`: `String`
   - `Choices`: `["groove", "disco", "g-style"]`

### Blueprint handler

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

    // Wire onComplete and onInterrupted to:
    HandleActionCompletion(IsSuccessful = true, ShouldRespond = Never)
```

**Test prompts:** `"Show me the groove dance."` (plays montage), `"Do the ballet dance."` (fallback branch — character explains the style is unavailable).

---

## Example 7: Start a sequence after speech begins

**Scenario:** A safety-drill NPC gestures toward an exit sign after its spoken warning begins, then walks to the sign.

### Configuration

Two actions in the `Actions` array:

1. `Announce` — custom action, no parameters, `bWaitForBotSpeech = true`, `DelayAfterBotSpeechSec = 0.5`.
2. `Move To` (default) — `bWaitForBotSpeech = false`.

When Convai generates the response `"Announce, Move To ExitSign"` while the action queue is empty, the plugin:

1. Receives `Announce` as the first action in the new sequence.
2. Because `Announce` has `bWaitForBotSpeech = true`, waits until the character's speech begins, speech finishes, the no-response path fires, or the action wait timeout expires.
3. Fires `Announce` after the wait condition resolves plus `0.5` seconds.
4. Advances to `Move To` after the `Announce` handler calls `HandleActionCompletion(true)`.

### Blueprint handler — Announce

```text
// Blueprint pseudocode
Event Announce(ActionData: FConvaiResultAction)
    // Play the announcement animation / audio cue
    PlayAnnouncementAnim()

    HandleActionCompletion(
        IsSuccessful = true,
        bAutoReport = true,
        ShouldRespond = Never
    )
```

---

## Next steps

{% content-ref url="parameterized-actions.md" %}
[Parameterized actions](parameterized-actions.md)
{% endcontent-ref %}

{% content-ref url="actions-blueprint-reference.md" %}
[Actions Blueprint reference](actions-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshoot-character-actions.md" %}
[Troubleshoot character actions](troubleshoot-character-actions.md)
{% endcontent-ref %}
