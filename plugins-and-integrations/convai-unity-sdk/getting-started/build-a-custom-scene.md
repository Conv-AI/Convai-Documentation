---
title: Build a custom scene
last_reviewed: "4.6.0"
description: >-
  Add required Convai components to a new Unity scene using the Setup Required
  Components command and configure your first character.
---

This page walks you through setting up a new scene with a Convai AI character from scratch. By the end, your scene will have the minimum required components for a character to receive voice input and respond.

## Minimum required hierarchy

Every working Convai scene needs these three things:

```text
[Manager GameObject]  → ConvaiManager + ConvaiRoomManager
[NPC GameObject]      → ConvaiCharacter + ConvaiAudioOutput + AudioSource
[Player GameObject]   → ConvaiPlayer
```

The setup wizard creates the first and third automatically. You add the NPC components yourself.

{% stepper %}
{% step %}
### Add the required manager components

In the Unity Editor menu bar, select **GameObject > Convai > Setup Required Components**.

Unity creates a **ConvaiManager** GameObject with `ConvaiManager` and `ConvaiRoomManager` attached, and a **ConvaiPlayer** GameObject with `ConvaiPlayer` attached. Both appear in the Hierarchy.

`ConvaiRoomManager` always lives on the same GameObject as `ConvaiManager`. Do not move it to a separate GameObject.
{% endstep %}

{% step %}
### Add ConvaiCharacter to your NPC

In the Hierarchy, select the NPC GameObject you want to make conversational. In the Inspector, click **Add Component** and add `ConvaiCharacter`.
{% endstep %}

{% step %}
### Add AudioSource and ConvaiAudioOutput

On the same NPC GameObject, add `AudioSource`, then add `ConvaiAudioOutput`.

All three components — `ConvaiCharacter`, `ConvaiAudioOutput`, and `AudioSource` — should now appear on the same GameObject in the Inspector.
{% endstep %}

{% step %}
### Set the Character ID

In the `ConvaiCharacter` component, set the **Character ID** field to the ID of your character from the [Convai dashboard](https://convai.com).

{% hint style="warning" %}
The Character ID field is required. If it is empty, the character cannot connect to Convai and the Scene Validator will report an error.
{% endhint %}
{% endstep %}

{% step %}
### Validate the scene

In the menu bar, select **GameObject > Convai > Validate Scene Setup**.

A dialog appears listing errors, warnings, and recommended next steps.

**Errors (must fix):**

| Error                                 | Fix                                          |
| ------------------------------------- | -------------------------------------------- |
| No `ConvaiManager` found              | Run **Setup Required Components**            |
| No `ConvaiCharacter` found            | Add `ConvaiCharacter` to your NPC GameObject |
| `ConvaiCharacter` has no Character ID | Set the Character ID from your dashboard     |
| No `ConvaiPlayer` found               | Run **Setup Required Components**            |

**Warnings:**

| Warning                | Fix                                          |
| ---------------------- | -------------------------------------------- |
| API key not configured | Open **Convai > Settings > Credentials** and enter your key |

When the validator reports no errors, the scene is ready for Play Mode.
{% endstep %}

{% step %}
### Enter Play Mode

Press **Play**. The Unity Console logs:

* `[ConvaiRuntime] Started successfully` — SDK initialized
* `[RoomConnectionRuntimeAdapter] Character <character-id> connected successfully (mode=create).` — character connected to Convai

Speak into your microphone. The character responds within a few seconds.

If you later add a Gaze, Body Animation, Body Language, or Emotion module component to the NPC, Convai adds supporting infrastructure components to the same GameObject automatically. See [Scene components reference](scene-components.md) for what each one does.
{% endstep %}
{% endstepper %}

## Editing settings that ship with the SDK

Some optional modules point a character at a default settings asset that ships inside the Convai package. The first time you change a field on one of these assets from a character's Inspector, Convai copies the asset into your project, points the character at the copy, and applies your edit there — the packaged original is never edited in place.

The copy is created next to the character's prefab when it has one, or under `Assets/Convai/<module>` otherwise. You do not create this copy yourself; changing a field is enough, and the Inspector reports where the copy was written.

## Usage examples

### Example 1: Safety training simulation

**Scenario:** An industrial safety trainer NPC responds to trainee questions about equipment procedures.

**Setup:**

* NPC GameObject: `SafetyTrainer` with `ConvaiCharacter`, `ConvaiAudioOutput`, `AudioSource`
* Character ID: ID of your safety trainer character from the Convai dashboard
* `ConvaiCharacter._characterName`: `"Safety Trainer"`
* `ConvaiCharacter._enableRemoteAudio`: `true`

**Expected outcome:** Trainees speak to the NPC and receive voice responses about safety procedures. The character name appears in the transcript UI.

### Example 2: Multiple characters in one scene

**Unity SDK <code class="expression">space.vars.unity_sdk_preview_version</code> preview:** This shared-room example is staged ahead of the current <code class="expression">space.vars.unity_sdk_version</code> Asset Store release.

**Scenario:** A medical training simulation with two characters — a supervising doctor and a nurse.

**Setup:**

* Two separate NPC GameObjects, each with `ConvaiCharacter`, `ConvaiAudioOutput`, `AudioSource`
* Each `ConvaiCharacter` has its own unique Character ID
* Only one `ConvaiManager` and one `ConvaiPlayer` in the scene
* One character is assigned as the explicit startup character before `ConvaiRoomManager` connects

The startup character becomes both the initial roster entry and the first interaction target. Set it during `Awake`, before the room manager's `Start` connection:

```csharp
using System;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public sealed class MedicalConversationRouter : MonoBehaviour
{
    [SerializeField] private ConvaiManager _manager;
    [SerializeField] private ConvaiCharacter _doctor;
    [SerializeField] private ConvaiCharacter _nurse;

    private void Awake()
    {
        _manager.SetExplicitConversationTarget(_doctor);
    }

    // Call from a UI button, raycast hit, proximity trigger, or your own selection system.
    public async void SelectNurse()
    {
        if (!_manager.TryGetRoomConnectionService(out IConvaiRoomConnectionService room))
            return;

        try
        {
            await room.SetInteractionTargetAsync(_nurse);
            Debug.Log("Nurse is the acknowledged interaction target.");
        }
        catch (Exception exception)
        {
            Debug.LogError($"Interaction target did not change: {exception.Message}");
        }
    }
}
```

Call `SetInteractionTargetAsync(...)` only after the shared room is connected and the selected character is ready in its roster. The operation completes after the backend acknowledges the route change. Keep routing-sensitive UI on the last acknowledged target when the operation fails, is cancelled, or times out; after a timeout, treat the result as unknown until you reread the session or reconnect.

**Expected outcome:** Both enabled characters join one shared room and retain distinct character identities and `character_session_id` values. Player and character transcript updates arrive on the room-wide transcript timeline. The SDK keeps the current target until your application changes or clears it; it does not switch targets automatically based on gaze, proximity, or speech.

## Next steps

With the scene built, run the validator to confirm everything is wired correctly before adding features.

{% content-ref url="validate-your-setup.md" %}
[Validate your setup](validate-your-setup.md)
{% endcontent-ref %}
